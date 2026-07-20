from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class ClarificationAgent:
    """
    Este agente toma el prompt insuficiente y repregunta de forma proactiva y cordial, exponiendo sutilmente los departamentos disponibles para guiar al usuario.
    """
    def __init__(self, llm: ChatOpenAI):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres un asistente de atención inicial de soporte corporativo.\n"
                "El usuario te ha saludado o ha enviado una consulta con intención insuficiente o ambigua.\n"
                "Tu objetivo es responder amablemente y pedirle de forma concisa que especifique su problema.\n"
                "Menciónale sutilmente que puedes ayudarle en temas de Recursos Humanos (HR), Soporte Técnico (Tech), Finanzas o Legal."
            )),
            ("human", "{query}")
        ])
        self.chain = self.prompt | llm

    def run(self, query: str) -> str:
        response = self.chain.invoke({"query": query})
        return response.content