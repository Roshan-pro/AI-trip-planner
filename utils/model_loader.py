import os
from dotenv import load_dotenv
from typing import Any,Literal,Optional
from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from utils.config_loader import load_config

class ConfigLoader:
    def __init__(self):
        self.config = load_config()
    def __getitem__(self, key: str) -> Any:
        return self.config[key]
    
class ModelLoader(BaseModel):
    model_provider: Literal['groq','openai'] ="groq"
    config : Optional[ConfigLoader] = Field(default=None,exclude=True)
    
    def model_post_init(self,  __context:Any) -> None:
        self.config = ConfigLoader()
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self)->Any:
        """
        Load and return the appropriate language model based on the specified provider.
        """
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == 'groq':
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name=self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(
                model=model_name,
                api_key=groq_api_key,
                temperature=0.7,
                max_tokens=1024
            )
            return llm
        elif self.model_provider == 'openai':
            openai_api_key = os.getenv("OPENAI_API_KEY", self.config['openai_api_key'])
            llm = ChatOpenAI(
                model_name="gpt-4o",
                openai_api_key=openai_api_key,
                temperature=0.7,
                max_tokens=1024
            )
            return llm
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")