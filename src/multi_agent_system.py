import os
import sys
import json
import uuid
from typing import Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno antes de importar componentes
load_dotenv()

from langchain_openai import ChatOpenAI
from src.database import VectorDatabaseManager
from src.agents.orchestrator import Orchestrator
from src.agents.clarification_agent import ClarificationAgent
from src.agents.hr_agent import HRAgent
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.evaluator import EvaluatorAgent
from src.config import Config

# Intento seguro de importación de Langfuse
LANGFUSE_ENABLED = False
try:
    from langfuse import Langfuse
    from langfuse.langchain import CallbackHandler
    LANGFUSE_ENABLED = True
except Exception as e:
    print(f"⚠️ Advertencia: No se pudo importar Langfuse: {e}")

class MultiAgentOrchestratorSystem:
    def __init__(self):
        print("⚙️ Inicializando modelo de lenguaje centralizado...")
        self.llm = ChatOpenAI(model=Config.MODEL_NAME, temperature=0)
        
        # Inicializar cliente de Langfuse con salvaguarda
        self.langfuse_client = None
        if LANGFUSE_ENABLED:
            try:
                self.langfuse_client = Langfuse(
                    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
                )
                print("📡 Cliente de Langfuse inicializado correctamente.")
            except Exception as e:
                print(f"⚠️ No se pudo conectar con Langfuse (se continuará sin monitoreo): {e}")

        print("📦 Cargando base de datos vectorial Chroma...")
        self.db_manager = VectorDatabaseManager()
        self.db_manager.build_or_load_vector_stores()
        
        self.orchestrator = Orchestrator(llm=self.llm)
        self.evaluator = EvaluatorAgent(llm=self.llm, langfuse_client=self.langfuse_client)
        
        self.agents = {
            "Clarification": ClarificationAgent(llm=self.llm),
            "HR": HRAgent(llm=self.llm, retriever=self.db_manager.get_retriever("hr")),
            "Tech": TechAgent(llm=self.llm, retriever=self.db_manager.get_retriever("tech")),
            "Finance": FinanceAgent(llm=self.llm, retriever=self.db_manager.get_retriever("finance")),
        }

    def process_customer_query(self, query: str, run_evaluator: bool = True) -> Dict[str, Any]:
        trace_id = str(uuid.uuid4())
        
        # 1. Instanciación correcta de CallbackHandler para Langfuse v4
        callbacks = []
        if self.langfuse_client:
            try:
                # En v4 se usa sin 'trace_id' en el constructor
                langfuse_handler = CallbackHandler()
                callbacks.append(langfuse_handler)
            except Exception as e:
                print(f"⚠️ Error al crear CallbackHandler: {e}")

        print(f"\n📥 [Entrada de Ticket]: '{query}'")
        
        # Paso 1: Clasificación mediante el Orquestador
        route_decision = self.orchestrator.route(query)
        dept = route_decision.department
        reason = route_decision.reasoning
        
        print(f"🔀 [Orquestador]: Enrutado a -> {dept}\n   💡 Motivo: {reason}")
        
        # Paso 2: Selección y ejecución del Agente Especialista
        agent = self.agents.get(dept)
        
        if not agent:
            final_response = (
                f"[Sistema Central]: Se determinó que la consulta corresponde al área [{dept}], "
                f"pero el Agente especializado no se encuentra disponible."
            )
        else:
            if hasattr(agent, "run"):
                final_response = agent.run(query)
            elif hasattr(agent, "chain"):
                # Intentamos invocar con string si la chain espera string o pasamos dict si la chain usa RunnablePassthrough
                try:
                    res = agent.chain.invoke(query, config={"callbacks": callbacks})
                except Exception:
                    res = agent.chain.invoke({"query": query}, config={"callbacks": callbacks})
                
                final_response = res.content if hasattr(res, "content") else str(res)
            else:
                final_response = str(agent(query))
                
        print(f"💬 [Respuesta del Agente]: {final_response}\n")

        # Paso 3: Auditoría y métricas en EvaluatorAgent
        eval_results = None
        if run_evaluator and self.langfuse_client:
            eval_results = self.evaluator.evaluate_and_log(
                query=query,
                response=final_response,
                trace_id=trace_id
            )
            
        return {
            "query": query,
            "assigned_department": dept,
            "routing_reason": reason,
            "response": final_response,
            "evaluation": eval_results
        }

# =====================================================================
# EJECUCIÓN DEL SISTEMA
# =====================================================================
if __name__ == "__main__":
    system = MultiAgentOrchestratorSystem()

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_queries_path = "test_queries.json"
        
        if os.path.exists(test_queries_path):
            with open(test_queries_path, "r", encoding="utf-8") as f:
                test_cases = json.load(f)
                
            print(f"\n🚀 Ejecutando pruebas sobre {len(test_cases)} consultas del Golden Dataset...")
            
            for index, case in enumerate(test_cases, start=1):
                print(f"\n=== Prueba {index}/{len(test_cases)} ===")
                system.process_customer_query(query=case["query"], run_evaluator=True)
        else:
            print(f"⚠️ No se encontró '{test_queries_path}'.")

    else:
        print("\n🤖 ¡Sistema Multi-Agente Activo! Escribe 'salir' para finalizar.\n")
        while True:
            try:
                user_input = input("👤 Tú: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["salir", "exit", "quit"]:
                    print("👋 ¡Hasta luego!")
                    break
                
                system.process_customer_query(user_input, run_evaluator=True)
                
            except KeyboardInterrupt:
                print("\n👋 Sesión finalizada.")
                break

    if system.langfuse_client:
        try:
            system.langfuse_client.flush()
        except Exception:
            pass