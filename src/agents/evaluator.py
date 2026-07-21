from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import Langfuse

class QualityScores(BaseModel):
    relevance: float = Field(description="Puntuación entre 0.0 y 1.0.")
    completeness: float = Field(description="Puntuación entre 0.0 y 1.0.")
    accuracy: float = Field(description="Puntuación entre 0.0 y 1.0.")
    reasoning: str = Field(description="Breve justificación.")

class EvaluatorAgent:
    def __init__(self, llm: ChatOpenAI, langfuse_client: Langfuse):
        self.langfuse = langfuse_client
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres un Auditor de Calidad de Sistemas Multi-Agente extremadamente exigente y crítico.\n"
                "Tu trabajo es encontrar fallas, omisiones, ambigüedades y redundancias en las respuestas de los agentes.\n\n"
                
                "### REGLAS RIGUROSAS DE EVALUACIÓN:\n"
                "1. **Puntaje Perfecto (1.0):** Reservado ÚNICAMENTE para respuestas excepcionales que resuelvan la consulta con absoluta precisión, claridad y con todos los detalles necesarios sin ningún relleno.\n"
                "2. **Punto de Partida (0.7 - 0.8):** Una respuesta correcta pero estándar o genérica debe ser calificada entre 0.7 y 0.8.\n"
                "3. **Criterios de Penalización:**\n"
                "   - **Respuestas genéricas/saludos (-0.2 a -0.4 en Completitud):** Si la consulta era específica (ej. 'cómo cambio mi contraseña') y la respuesta solo da un saludo o pide más datos en lugar de dar los pasos, penaliza severamente.\n"
                "   - **Verborragia / Relleno (-0.1 a -0.2 en Relevancia):** Si la respuesta incluye explicaciones innecesarias o mensajes corporativos vacíos.\n"
                "   - **Falta de pasos concretos (-0.2 a -0.3 en Completitud):** Si omite enlaces, requisitos prevíos o instrucciones paso a paso.\n"
                "   - **Instrucciones ambiguas o dudosas (-0.3 a -0.5 en Precisión).**\n\n"
                
                "Escribe tu 'reasoning' mencionando explícitamente qué puntos restaste y por qué. Sé crítico y analítico."
            )),
            ("human", (
                "📥 **Consulta del Usuario:** {query}\n\n"
                "💬 **Respuesta entregada por el Agente:** {response}\n\n"
                "Evalúa de 0.0 a 1.0 la Relevancia, Completitud y Precisión aplicando el criterio estricto."
            ))
        ])
        self.chain = self.prompt | llm.with_structured_output(QualityScores)

    def evaluate_and_log(self, query: str, response: str, trace_id: str) -> QualityScores:
        print("\n🧐 [Evaluador]: Evaluando calidad de la respuesta...")
        
        scores: QualityScores = self.chain.invoke({"query": query, "response": response})
        
        if scores.relevance > 1.0: scores.relevance = round(scores.relevance / 10.0, 2)
        if scores.completeness > 1.0: scores.completeness = round(scores.completeness / 10.0, 2)
        if scores.accuracy > 1.0: scores.accuracy = round(scores.accuracy / 10.0, 2)

        print(f"📊 [Resultados de Auditoría]:\n"
              f"   - Relevancia: {scores.relevance}\n"
              f"   - Completitud: {scores.completeness}\n"
              f"   - Precisión: {scores.accuracy}\n"
              f"   - Razón: {scores.reasoning}\n")

        # create_score es el método compatible en v4
        try:
            self.langfuse.create_score(
                trace_id=trace_id,
                name="relevance",
                value=float(scores.relevance),
                comment=scores.reasoning
            )
            self.langfuse.create_score(
                trace_id=trace_id,
                name="completeness",
                value=float(scores.completeness)
            )
            self.langfuse.create_score(
                trace_id=trace_id,
                name="accuracy",
                value=float(scores.accuracy)
            )
            print(f"🚀 [Evaluador]: Métricas sincronizadas en Langfuse (trace_id: {trace_id}).")
        except Exception as e:
            print(f"❌ Error al enviar scores a Langfuse: {e}")
            
        return scores