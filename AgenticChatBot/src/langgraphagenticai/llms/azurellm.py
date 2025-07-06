from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureChatOpenAI


class AzureLLM:
    def __init__(self,user_controls):
        self.user_controls = user_controls

    
    def get_llm_model(self):
        llm_model = self.user_controls["models"]
        llm_options = self.user_controls["llmoptions"]
        llm_key = self.user_controls["LLM-Key"]
        try:
            if(llm_options == "Azure"):
                token_provider = get_bearer_token_provider(DefaultAzureCredential(),"https://cognitiveservices.azure.com/.default")
                chat_model = AzureChatOpenAI(
                                api_version="2024-12-01-preview",
                                azure_endpoint="https://azopenai-langchain.openai.azure.com/",
                                model= llm_model,
                                api_key= llm_key
                            )
                return chat_model
        except Exception as e:
            raise e
            
