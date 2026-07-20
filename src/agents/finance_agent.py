from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class FinanceAgent:
    """
    El agente financiero requiere precisión numérica absoluta. No puede asumir datos ni estimar reembolsos o facturas si las políticas no lo expresan textualmente.
    """
    def __init__(self, llm: ChatOpenAI, retriever):
        self.retriever = retriever
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres el Agente de Finanzas y Contabilidad de la empresa.\n"
                "Resuelves consultas sobre facturación, flujos de reembolso, reportes financieros corporativos y pasarelas de pago.\n\n"
                "Reglas estrictas:\n"
                "1. Sé extremadamente preciso. En finanzas no hay espacio para la ambigüedad.\n"
                "2. Si la consulta involucra montos, plazos de pago o aprobaciones, cíñete rigurosamente al texto del contexto.\n"
                "3. Si el contexto no detalla la política exacta para este caso, solicita al usuario que adjunte sus comprobantes y menciona que el equipo contable auditará la solicitud.\n\n"
                "Políticas Financieras Vigentes:\n"
                "{context}"
            )),
            ("human", "{query}")
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
            
        self.chain = (
            {
                "context": self.retriever | format_docs,
                "query": RunnablePassthrough()
            }
            | self.prompt
            | llm
            | StrOutputParser()
        )

    def run(self, query: str) -> str:
        return self.chain.invoke(query)