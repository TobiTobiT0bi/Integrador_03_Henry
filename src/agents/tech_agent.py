from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langfuse import observe

class TechAgent:
    """
    Para el equipo de tecnología, el tono debe ser directo, estructurado y orientado a la resolución sistemática de problemas informáticos (paso a paso).
    """
    def __init__(self, llm: ChatOpenAI, retriever):
        self.retriever = retriever
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres el Agente de Soporte Técnico (Tech Support) de la empresa.\n"
                "Ayudas a los empleados a resolver problemas de accesos, software, VPN, credenciales y hardware.\n\n"
                "Reglas estrictas:\n"
                "1. Responde de forma concisa, estructurada (usa viñetas o pasos si es necesario) y técnica.\n"
                "2. Guíate estrictamente por la documentación provista abajo.\n"
                "3. Si la solución no está en el contexto, indica los pasos para abrir un ticket de Nivel 2 con el equipo de IT de guardia.\n\n"
                "Documentación Técnica de Referencia:\n"
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

    @observe(name="Tech agent RAG")
    def run(self, query: str) -> str:
        return self.chain.invoke(query)