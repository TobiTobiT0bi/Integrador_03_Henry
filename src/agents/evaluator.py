from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import Langfuse, observe

class QualityScores(BaseModel):
    """Puntajes de calidad asignados a la respuesta del asistente."""
    relevance: float = Field(description="Puntuación de 0 a 1 de qué tan bien responde a la duda exacta del usuario.")
    completeness: float = Field(description="Puntuación de 0 a 1 de si la respuesta cubre todos los puntos solicitados o queda incompleta.")
    accuracy: float = Field(description="Puntuación de 0 a 1 de si la respuesta suena segura, precisa y libre de alucinaciones vagas.")
    reasoning: str = Field(description="Breve justificación de los puntajes asignados.")

class EvaluatorAgent:
    def __init__(self, llm: ChatOpenAI, langfuse_client: Langfuse):
        self.langfuse = langfuse_client
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres un Auditor de Calidad de Inteligencia Artificial independiente.\n"
                "Tu trabajo es evaluar las respuestas generadas por los agentes de soporte de la empresa.\n"
                "Analiza la consulta original del cliente y la respuesta entregada, y califica "
                "estrictamente de 0 a 1 (con solo un decimal) las dimensiones de: Relevance, Completeness y Accuracy.\n"
                "Sé crítico y objetivo. Si la respuesta evade la pregunta o es demasiado vaga, penaliza el puntaje."
            )),
            ("human", "Consulta Original: {query}\nRespuesta Entregada: {response}")
        ])
        
        self.chain = self.prompt | llm.with_structured_output(QualityScores)

    @observe(name="Score Evaluating")
    def evaluate_and_log(self, trace_id: str, query: str, response: str):
        """Evalúa la respuesta y sube las métricas a Langfuse asociadas al Trace."""
        print(f" [Evaluador]: Evaluando calidad de la respuesta para el Trace ID: {trace_id}...")
        
        scores: QualityScores = self.chain.invoke({"query": query, "response": response})
        
        print(f" [Resultados de Auditoría]:\n"
              f"   - Relevancia: {scores.relevance}/10\n"
              f"   - Completitud: {scores.completeness}/10\n"
              f"   - Precisión: {scores.accuracy}/10\n"
              f"   - Razón: {scores.reasoning}")

        try:
            self.langfuse.score(
                trace_id=trace_id,
                name="relevance",
                value=scores.relevance,
                comment=scores.reasoning
            )
            self.langfuse.score(
                trace_id=trace_id,
                name="completeness",
                value=scores.completeness
            )
            self.langfuse.score(
                trace_id=trace_id,
                name="accuracy",
                value=scores.accuracy
            )
            print(" [Evaluador]: Métricas de calidad sincronizadas exitosamente en el panel de Langfuse.")
        except Exception as e:
            print(f" Error al enviar los scores a Langfuse: {e}")
            
        return scores