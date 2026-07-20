import os
from typing import Dict
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class VectorDatabaseManager:
    def __init__(self, data_dir: str = "data", persist_dir: str = "data/chroma_db"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        
        # modelo de embeddings estándar de la industria (3-small por costo/eficiencia)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=60,
            length_function=len,
            is_separator_regex=False,
        )
        
        self.retrievers: Dict[str, any] = {}

    def build_or_load_vector_stores(self):
        """
        Escanea las carpetas de datos, procesa los documentos si no existen en la base
        de datos persistida, e indexa las colecciones por dominio.
        """
        domains = ["hr", "tech", "finance"]
        
        for domain in domains:
            domain_data_path = os.path.join(self.data_dir, f"{domain}_docs")
            
            if not os.path.exists(domain_data_path):
                os.makedirs(domain_data_path)
                print(f"Creada carpeta vacía para el dominio: {domain_data_path}. Agrega tus archivos .txt allí.")
            
            domain_persist_path = os.path.join(self.persist_dir, domain)
            
            if os.path.exists(domain_persist_path) and len(os.listdir(domain_persist_path)) > 0:
                print(f" Cargando índice existente de Chroma para el dominio: [{domain.upper()}]")
                vector_store = Chroma(
                    persist_directory=domain_persist_path,
                    embedding_function=self.embeddings,
                    collection_name=f"{domain}_collection"
                )
            else:
                print(f" Indexando nuevos documentos para el dominio: [{domain.upper()}]...")
                loader = DirectoryLoader(
                    domain_data_path, 
                    glob="**/*.txt", 
                    loader_cls=TextLoader,
                    loader_kwargs={"encoding": "utf-8"}
                )
                documents = loader.load()
                
                if not documents:
                    print(f" [Advertencia] No se encontraron archivos .txt en {domain_data_path}. Generando base vacía provisional.")
                    vector_store = Chroma(
                        persist_directory=domain_persist_path,
                        embedding_function=self.embeddings,
                        collection_name=f"{domain}_collection"
                    )
                else:
                    chunks = self.text_splitter.split_documents(documents)
                    print(f" Documentos de [{domain.upper()}] divididos en {len(chunks)} fragmentos (chunks).")
                    
                    vector_store = Chroma.from_documents(
                        documents=chunks,
                        embedding=self.embeddings,
                        persist_directory=domain_persist_path,
                        collection_name=f"{domain}_collection"
                    )
            
            self.retrievers[domain] = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
        print("✅ Inicialización de Base de Datos Vectorial completada exitosamente.")

    def get_retriever(self, domain: str):
        """Retorna el componente Retriever de LangChain para el agente solicitado."""
        return self.retrievers.get(domain.lower())

# =====================================================================
# SCRIPT DE PRUEBA INDEPENDIENTE (Para debuggear localmente)
# =====================================================================
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    db_manager = VectorDatabaseManager()
    db_manager.build_or_load_vector_stores()