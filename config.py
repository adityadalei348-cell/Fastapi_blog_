from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config= SettingsConfigDict( env_file =".env", env_file_encoding="UTF-8")

    database_url: str 
    
    secret_key:SecretStr
    algorithm:str ="HS256"
    access_token_expire_minutes: int= 30

    #Cloudinary Configuration
    cloudinary_cloud_name: str
    cloudinary_api_key: str | None=None
    cloudinary_api_secret: SecretStr | None=None


    max_upload_size_bytes: int= 5 * 1024 * 1024
    
    posts_per_page:int= 10
    
    reset_token_expire_minutes:int=60
    
    mail_server: str = "localhost" #smtp server host name
    mail_port: int = 2525
    mail_username: str = ""
    mail_password: SecretStr = SecretStr("")
    mail_from: str = "noreply@example.com"
    mail_use_tls: bool = True

    frontend_url: str = "http://localhost:8000"
        
settings= Settings() #load from .env file


