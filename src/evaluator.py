from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import Langfuse

class QualityScores(BaseModel):
    """Puntajes de calidad asignados a la respuesta del asistente."""
    relevance: int = Field(description="Puntuación de 1 a 10 de qué tan bien responde a la duda exacta del usuario.")
    completeness: int = Field(description="Puntuación de 1 a 10 de si la respuesta cubre todos los puntos solicitados o queda incompleta.")
    accuracy: int = Field(description="Puntuación de 1 a 10 de si la respuesta suena segura, precisa y libre de alucinaciones vagas.")
    reasoning: str = Field(description="Breve justificación de los puntajes asignados.")

class EvaluatorAgent:
    def __init__(self, llm: ChatOpenAI, langfuse_client: Langfuse):
        self.langfuse = langfuse_client
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres un Auditor de Calidad de Inteligencia Artificial independiente.\n"
                "Tu trabajo es evaluar las respuestas generadas por los agentes de soporte de la empresa.\n"
                "Analiza la consulta original del cliente y la respuesta entregada, y califica "
                "estrictamente de 1 a 10 las dimensiones de: Relevance, Completeness y Accuracy.\n"
                "Sé crítico y objetivo. Si la respuesta evade la pregunta o es demasiado vaga, penaliza el puntaje."
            )),
            ("human", "Consulta Original: {query}\nRespuesta Entregada: {response}")
        ])
        
        self.chain = self.prompt | llm.with_structured_output(QualityScores)

    def evaluate_and_log(self, trace_id, query: str = "", response: str = "", **kwargs) -> QualityScores:
        """
        Evalúa la respuesta y registra los puntajes en Langfuse.
        Recibe 'trace_id' como primer argumento posicional para satisfacer el wrapper de Langfuse.
        """
        # Si por alguna razón query o response vinieron dentro de kwargs
        if not query and "query" in kwargs:
            query = kwargs["query"]
        if not response and "response" in kwargs:
            response = kwargs["response"]

        print("🧐 [Evaluador]: Evaluando calidad de la respuesta...")
        
        # 1. Ejecutar la evaluación con el LLM
        scores: QualityScores = self.chain.invoke({"query": query, "response": response})
        
        print(f"📊 [Resultados de Auditoría]:\n"
              f"   - Relevancia: {scores.relevance}/10\n"
              f"   - Completitud: {scores.completeness}/10\n"
              f"   - Precisión: {scores.accuracy}/10\n"
              f"   - Razón: {scores.reasoning}\n")

        # 2. Registrar puntajes en Langfuse
        try:
            score_kwargs = {}
            if trace_id:
                score_kwargs["trace_id"] = trace_id

            self.langfuse.score(
                name="relevance",
                value=scores.relevance,
                comment=scores.reasoning,
                **score_kwargs
            )
            self.langfuse.score(
                name="completeness",
                value=scores.completeness,
                **score_kwargs
            )
            self.langfuse.score(
                name="accuracy",
                value=scores.accuracy,
                **score_kwargs
            )
            print("🚀 [Evaluador]: Métricas de calidad sincronizadas exitosamente en Langfuse.")
        except Exception as e:
            print(f"❌ Error al enviar los scores a Langfuse: {e}")
            
        return scores