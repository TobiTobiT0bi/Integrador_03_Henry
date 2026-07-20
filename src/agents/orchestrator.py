from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import observe

class RouteIntent(BaseModel):
    """Clasifica la consulta del usuario al departamento correcto o solicita aclaración."""
    department: Literal["HR", "Tech", "Finance", "Legal", "Clarification"] = Field(
        description="El departamento destino de la consulta. Si es un saludo, frase corta vaga o pide ayuda sin dar detalles, elige 'Clarification'."
    )
    reasoning: str = Field(
        description="Breve justificación de una frase del por qué se eligió este destino."
    )

class Orchestrator:
    def __init__(self, llm: ChatOpenAI):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres el clasificador central de tickets de soporte de la empresa.\n"
                "Evalúa la entrada del usuario y asígnala a una de las siguientes áreas:\n"
                "- HR: Licencias, vacaciones, nóminas, beneficios corporativos, contratos internos.\n"
                "- Tech: Accesos, VPN, credenciales, fallos de software/hardware, herramientas IT.\n"
                "- Finance: Facturas, reembolsos, pasarelas de pago, contabilidad.\n"
                "- Legal: Contratos con clientes, términos de servicio, políticas de privacidad.\n"
                "- Clarification: Saludos, texto genérico, o prompts donde la intención es insuficiente para decidir un área."
            )),
            ("human", "{query}")
        ])
        self.chain = self.prompt | llm.with_structured_output(RouteIntent)

    @observe(name="Orchestrator Routing")
    def route(self, query: str) -> RouteIntent:
        return self.chain.invoke({"query": query})