import os
import sys

from pathlib import Path

# Forzar que el directorio raíz del proyecto sea el primero en sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import uuid
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI

from langfuse import get_client

from src.database import VectorDatabaseManager
from src.agents.orchestrator import Orchestrator
from src.agents.clarification_agent import ClarificationAgent
from src.agents.hr_agent import HRAgent
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.evaluator import EvaluatorAgent
from src.config import Config

import src.agents.evaluator as eval_module
print(f"DEBUG EVALUATOR PATH: {eval_module.__file__}")

class MultiAgentOrchestratorSystem:
    def __init__(self):
        print("⚙️ Inicializando modelo de lenguaje centralizado...")
        self.llm = ChatOpenAI(model=Config.MODEL_NAME, temperature=0)
        self.langfuse_client = get_client()
        
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
        """
        Recibe la consulta del usuario, la clasifica mediante el Orquestador,
        delega al agente especializado y la audita mediante el Evaluator.
        """
        # Generar un ID único para asociar los eventos y scores en Langfuse
        trace_id = str(uuid.uuid4())

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
                final_response = agent.chain.invoke({"query": query}).content
            else:
                final_response = str(agent(query))
                
        print(f"💬 [Respuesta del Agente]: {final_response}\n")

        # Paso 3: Auditoría con el EvaluatorAgent
        eval_results = None
        if run_evaluator:
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
    langfuse_client = get_client()

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_queries_path = "test_queries.json"
        
        if os.path.exists(test_queries_path):
            with open(test_queries_path, "r", encoding="utf-8") as f:
                test_cases = json.load(f)
                
            print(f"\n🚀 Ejecutando pruebas sobre {len(test_cases)} consultas del Golden Dataset...")
            
            for index, case in enumerate(test_cases, start=1):
                print(f"\n=== Prueba {index}/{len(test_cases)} ===")
                system.process_customer_query(case["query"], run_evaluator=True)
        else:
            print(f"⚠️ No se encontró '{test_queries_path}'.")

    else:
        print("\n🤖 ¡Sistema Multi-Agente Activo! Escribe 'salir' for finalizar.\n")
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

    langfuse_client.flush()