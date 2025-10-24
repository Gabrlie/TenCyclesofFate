from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# 确定 .env 文件的位置
# 优先使用根目录的 .env，如果不存在则使用 backend/.env
def get_env_file():
    # 在 Docker 容器中，环境变量会直接注入，不需要 .env 文件
    if os.environ.get('OPENAI_API_KEY'):
        return None
    
    root_env = Path(__file__).parent.parent.parent / ".env"
    backend_env = Path(__file__).parent.parent / ".env"
    
    if root_env.exists():
        return str(root_env)
    elif backend_env.exists():
        return str(backend_env)
    return None

class Settings(BaseSettings):
    # OpenAI API Settings
    OPENAI_API_KEY: str | None = None # Allow key to be optional to enable server startup
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MODEL_CHEAT_CHECK: str = "qwen3-235b-a22b"

    # JWT Settings for OAuth2
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600

    # Database URL
    DATABASE_URL: str = "sqlite:///./veloera.db"

    # Linux.do OAuth Settings
    LINUXDO_CLIENT_ID: str | None = None
    LINUXDO_CLIENT_SECRET: str | None = None
    LINUXDO_SCOPE: str = "read"
    ENABLE_LINUXDO_OAUTH: bool = True

    # Local Registration Toggle
    ENABLE_LOCAL_LOGIN: bool = True
    ENABLE_LOCAL_REGISTRATION: bool = True

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    UVICORN_RELOAD: bool = False

    # 自动检测 .env 文件位置
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding='utf-8',
        extra='ignore'
    )

# Create a single instance of the settings
settings = Settings()
