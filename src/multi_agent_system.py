import os
import json
import sys
from pathlib import Path
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langfuse import observe, get_client

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.database import VectorDatabaseManager
from src.agents.orchestrator import Orchestrator
from src.agents.clarification_agent import ClarificationAgent
from src.agents.hr_agent import HRAgent
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from src.config import Config

class MultiAgentOrchestratorSystem:
    def __init__(self):
        print(" Inicializando modelo de lenguaje centralizado...")
        self.llm = ChatOpenAI(model=Config.MODEL_NAME, temperature=0)
        
        print(" Cargando base de datos vectorial Chroma...")
        self.db_manager = VectorDatabaseManager()
        self.db_manager.build_or_load_vector_stores()
        
        self.orchestrator = Orchestrator(llm=self.llm)
        
        self.agents = {
            "Clarification": ClarificationAgent(llm=self.llm),
            "HR": HRAgent(llm=self.llm, retriever=self.db_manager.get_retriever("hr")),
            "Tech": TechAgent(llm=self.llm, retriever=self.db_manager.get_retriever("tech")),
            "Finance": FinanceAgent(llm=self.llm, retriever=self.db_manager.get_retriever("finance")),
        }

    @observe(name="Multi-Agent Customer Query Process")
    def process_customer_query(self, query: str) -> Dict[str, Any]:
        """
        Recibe la consulta del usuario, la clasifica mediante el Orquestador
        y delega la resolución al agente especializado correspondiente.
        Todo el flujo es capturado automáticamente por Langfuse.
        """
        print(f"\n [Entrada de Ticket]: '{query}'")
        
        get_client().update_current_trace(
            tags=["multi-agent", Config.MODEL_NAME],
            metadata={"user_query": query}
        )
        
        # Paso 1: Clasificación mediante el Orquestador
        route_decision = self.orchestrator.route(query)
        dept = route_decision.department
        reason = route_decision.reasoning
        
        print(f" [Orquestador]: Enrutado a -> {dept} | Motivo: {reason}")
        get_client().update_current_trace(metadata={"assigned_department": dept})
        
        # Paso 2: Selección y ejecución del Agente Especialista
        agent = self.agents.get(dept)
        
        if not agent:
            final_response = (
                f"[Sistema Central]: Se determinó que la consulta corresponde al área [{dept}], "
                f"pero el Agente especializado no se encuentra disponible. Derivando a analista humano..."
            )
        else:
            if hasattr(agent, "run"):
                final_response = agent.run(query)
            elif hasattr(agent, "chain"):
                final_response = agent.chain.invoke({"query": query}).content
            else:
                final_response = str(agent(query))
                
        print(f" [Respuesta del Agente]: {final_response}")
        
        return {
            "query": query,
            "assigned_department": dept,
            "routing_reason": reason,
            "response": final_response
        }

# =====================================================================
# EJECUCIÓN DEL FLUJO PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    system = MultiAgentOrchestratorSystem()
    langfuse_client = get_client()

    # Si se pasa la bandera '--test', corre el Golden Dataset
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_queries_path = "test_queries.json"
        
        if os.path.exists(test_queries_path):
            with open(test_queries_path, "r", encoding="utf-8") as f:
                test_cases = json.load(f)
                
            print(f"\n🚀 Ejecutando pruebas sobre {len(test_cases)} consultas del Golden Dataset...")
            
            for index, case in enumerate(test_cases, start=1):
                print(f"\n=== Prueba {index}/{len(test_cases)} ===")
                print(f"🎯 Categoría Esperada: {case['expected_department']}")
                
                output = system.process_customer_query(case["query"])
                
                status = "✅ MATCH" if output["assigned_department"] == case["expected_department"] else "❌ MISCLASSIFICATION"
                print(f"📊 Resultado Clasificación: {status}")
        else:
            print(f"⚠️ No se encontró '{test_queries_path}'.")

    # Por defecto, inicia la consola interactiva en vivo
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
                
                system.process_customer_query(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Sesión finalizada.")
                break

    # Asegura que todas las trazas se envíen a Langfuse antes de terminar
    langfuse_client.flush()