from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureOpenAIEmbeddings,AzureChatOpenAI

class models:
    def __init__(self,chat_model_name,embedding_model,api_key):
        self.chat_model_name = chat_model_name
        self.embedding_model=embedding_model
        self.api_key = api_key

    def get_llm_model(self):
     try:
        return  AzureChatOpenAI(
            api_key= self.api_key,
            api_version="2024-12-01-preview",
            azure_endpoint="https://azopenai-langchain.openai.azure.com/",
            model= self.chat_model_name
             )
     except Exception as e:
         print(e)
         raise e 

     

    def get_embedding_model(self):
     try:
        return  AzureOpenAIEmbeddings(
            api_key= self.api_key,
            api_version="2024-12-01-preview",
            azure_endpoint="https://azopenai-langchain.openai.azure.com/",
            model= self.embedding_model
             )
     except Exception as e:
         print(e)
         raise e 
           