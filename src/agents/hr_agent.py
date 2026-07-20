from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class HRAgent:
    """
    Este agente se encarga de responder de manera empática y clara sobre políticas internas de personal, vacaciones y nóminas, basándose estrictamente en los documentos recuperados.
    """
    def __init__(self, llm: ChatOpenAI, retriever):
        self.retriever = retriever
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres el Agente de Inteligencia Artificial especializado en Recursos Humanos (HR) de la empresa.\n"
                "Tu objetivo es ayudar a los empleados con dudas sobre vacaciones, nóminas, beneficios y políticas internas.\n\n"
                "Reglas estrictas:\n"
                "1. Utiliza ÚNICAMENTE el siguiente contexto recuperado de los manuales internos para responder.\n"
                "2. Si el contexto no contiene la respuesta, di cordialmente que no tienes esa información en tus manuales y que derivarás el caso a un especialista humano de HR.\n"
                "3. Mantén un tono profesional, empático y servicial.\n\n"
                "Contexto interno de HR:\n"
                "{context}"
            )),
            ("human", "{query}")
        ])

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
            
        # Construimos el pipeline usando LangChain Expression Language (LCEL)
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