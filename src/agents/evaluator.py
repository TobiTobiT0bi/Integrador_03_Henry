from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import Langfuse

class QualityScores(BaseModel):
    """Puntajes de calidad asignados a la respuesta del asistente."""
    relevance: float = Field(
        description="Puntuación entre 0.0 y 1.0. Ejemplo: 0.9 (significa 90%). NUNCA uses escala de 0 a 10."
    )
    completeness: float = Field(
        description="Puntuación entre 0.0 y 1.0. Ejemplo: 0.8 (significa 80%). NUNCA uses escala de 0 a 10."
    )
    accuracy: float = Field(
        description="Puntuación entre 0.0 y 1.0. Ejemplo: 1.0 (significa 100%). NUNCA uses escala de 0 a 10."
    )
    reasoning: str = Field(
        description="Breve justificación de los puntajes asignados."
    )

class EvaluatorAgent:
    def __init__(self, llm: ChatOpenAI, langfuse_client: Langfuse):
        self.langfuse = langfuse_client
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres un Auditor de Calidad de Inteligencia Artificial independiente.\n"
                "Tu trabajo es evaluar las respuestas generadas por los agentes de soporte de la empresa.\n"
                "Analiza la consulta original del cliente y la respuesta entregada.\n"
                "REGLA CRÍTICA DE CALIFICACIÓN:\n"
                "- Califica estrictamente en un rango decimal de 0.0 a 1.0 (donde 0.0 es el mínimo y 1.0 es la perfección absoluta).\n"
                "- NO utilices la escala del 1 al 10 ni fracciones tipo /10."
            )),
            ("human", "Consulta Original: {query}\nRespuesta Entregada: {response}")
        ])
        
        self.chain = self.prompt | llm.with_structured_output(QualityScores)

    def evaluate_and_log(self, query: str = "", response: str = "", trace_id: str = None, **kwargs) -> QualityScores:
        """
        Evalúa la respuesta y registra los puntajes en Langfuse asociándolos al trace_id.
        """
        query = query or kwargs.get("query", "")
        response = response or kwargs.get("response", "")

        print(f"\n🧐 [Evaluador]: Evaluando calidad para Trace ID: {trace_id}...")
        
        # 1. Ejecutar la evaluación con el LLM
        scores: QualityScores = self.chain.invoke({"query": query, "response": response})
        
        # Normalización de seguridad: Si por alguna razón el LLM devuelve > 1.0 (ej. 9.0), lo normalizamos a 0.9
        if scores.relevance > 1.0:
            scores.relevance = round(scores.relevance / 10.0, 2)
        if scores.completeness > 1.0:
            scores.completeness = round(scores.completeness / 10.0, 2)
        if scores.accuracy > 1.0:
            scores.accuracy = round(scores.accuracy / 10.0, 2)

        print(f"📊 [Resultados de Auditoría]:\n"
              f"   - Relevancia: {scores.relevance}\n"
              f"   - Completitud: {scores.completeness}\n"
              f"   - Precisión: {scores.accuracy}\n"
              f"   - Razón: {scores.reasoning}\n")

        # 2. Registrar puntajes en Langfuse
        if trace_id:
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
                print("🚀 [Evaluador]: Métricas de calidad sincronizadas exitosamente en Langfuse.")
            except Exception as e:
                print(f"❌ Error al enviar los scores a Langfuse: {e}")
        else:
            print("⚠️ [Evaluador]: No se proporcionó trace_id, omitiendo envío a Langfuse.")
            
        return scores