import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langfuse.model import CallbackHandler

# Importaciones de nuestros módulos internos
from src.database import VectorDatabaseManager
from src.agents.orchestrator import Orchestrator
from src.agents.clarification_agent import ClarificationAgent
from src.agents.hr_agent import HRAgent
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from src.config import Config

class MultiAgentOrchestratorSystem:
    def __init__(self):
        
        self.langfuse_callback = CallbackHandler()
        self.llm = ChatOpenAI(model= Config.MODEL_NAME, temperature=0)
        
        print(" Inicializando almacenamiento de conocimiento corporativo...")
        self.db_manager = VectorDatabaseManager()
        self.db_manager.build_or_load_vector_stores()
        
        self.orchestrator = Orchestrator(llm=self.llm)
        
        self.agents = {
            "Clarification": ClarificationAgent(llm=self.llm),
            "HR": HRAgent(llm=self.llm, retriever=self.db_manager.get_retriever("hr")),
            "Tech": TechAgent(llm=self.llm, retriever=self.db_manager.get_retriever("tech")),
            "Finance": FinanceAgent(llm=self.llm, retriever=self.db_manager.get_retriever("finance")),
        }

    def process_customer_query(self, query: str) -> Dict[str, Any]:
        """
        Recibe una consulta de cliente, ejecuta el ruteo inteligente, 
        delega al agente correcto y traza todo el flujo hacia Langfuse.
        """
        print(f"\n [Entrada de Ticket]: '{query}'")
        
        config = {
            "callbacks": [self.langfuse_callback],
            "metadata": {"user_query": query}
        }
        
        # Paso 1: Clasificación de intención mediante el Orquestador estructurado
        route_decision = self.orchestrator.chain.invoke({"query": query}, config=config)
        
        dept = route_decision.department
        reason = route_decision.reasoning
        print(f" [Orquestador]: Enrutado a -> {dept} | Motivo: {reason}")
        
        self.langfuse_callback.auth_check() # Verifica conexión activa
        
        # Paso 2: Enrutamiento Condicional y Selección del Agente Experto
        agent = self.agents.get(dept)
        
        if not agent:
            final_response = (
                f"[Sistema Central]: Se determinó que la consulta corresponde al área [{dept}], "
                f"pero el Agente especializado está en mantenimiento corporativo. Derivando a analista humano..."
            )
        else:
            # Paso 3: Ejecución del agente especialista (RAG o Clarificación)
            if hasattr(agent, "chain"):
                if dept == "Clarification":
                    final_response = agent.chain.invoke({"query": query}, config=config).content
                else:
                    final_response = agent.chain.invoke(query, config=config)
            else:
                final_response = agent.run(query)
                
        print(f" [Respuesta Agente]: {final_response}")
        
        return {
            "query": query,
            "assigned_department": dept,
            "routing_reason": reason,
            "response": final_response
        }

# =====================================================================
# EJECUCIÓN DEL FLUJO PRINCIPAL CON EL GOLDEN DATASET
# =====================================================================
if __name__ == "__main__":
    import json
    
    system = MultiAgentOrchestratorSystem()
    
    test_queries_path = "test_queries.json"
    if os.path.exists(test_queries_path):
        with open(test_queries_path, "r", encoding="utf-8") as f:
            test_cases = json.load(f)
            
        print(f"\n🚀 Iniciando pruebas automatizadas sobre {len(test_cases)} consultas del Golden Dataset...")
        
        for index, case in enumerate(test_cases, start=1):
            print(f"\n=== Prueba {index}/{len(test_cases)} ===")
            print(f"🎯 Categoría Esperada: {case['expected_department']}")
            
            output = system.process_customer_query(case["query"])
            
            status = "✅ MATCH" if output["assigned_department"] == case["expected_department"] else "❌ MISCLASSIFICATION"
            print(f"📊 Resultado Clasificación: {status}")
    else:
        print(f"⚠️ No se encontró el archivo '{test_queries_path}'. Ejecutando consulta de prueba básica.")
        system.process_customer_query("Hola, buenas tardes a todos.")