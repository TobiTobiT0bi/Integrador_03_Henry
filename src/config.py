import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración centralizada y validación del entorno del sistema multiagente."""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL", "gpt-4o-mini")
    
    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    DATA_DIR = "data"
    CHROMA_PERSIST_DIR = "data/chroma_db"

    @classmethod
    def validate_environment(cls):
        """Valida que las credenciales críticas estén configuradas antes de iniciar el workflow."""
        missing_vars = []
        
        if not cls.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")
        if not cls.LANGFUSE_PUBLIC_KEY:
            missing_vars.append("LANGFUSE_PUBLIC_KEY")
        if not cls.LANGFUSE_SECRET_KEY:
            missing_vars.append("LANGFUSE_SECRET_KEY")
            
        if missing_vars:
            raise ValueError(
                f"❌ Error catastrófico de configuración: Faltan las siguientes variables esenciales en tu archivo .env:\n"
                f"   {', '.join(missing_vars)}\n"
                f"Por favor, revisa tu configuración basándote en .env.example."
            )
        
        print(f" Configuración validada con éxito. Utilizando el modelo: [{cls.MODEL_NAME}]")

# Ejecutamos la validación en el momento exacto en el que el resto del software importe este módulo
Config.validate_environment()