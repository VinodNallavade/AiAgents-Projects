from configparser import ConfigParser



class Config:
    def __init__(self,config_file = "./src/langgraphagenticai/ui/uiconfigfile.ini"):
        self.config= ConfigParser()
        self.config.read(config_file)


    def get_llm_options(self):
        return "Azure"   
    
    def get_use_cases(self):
        return "Basic Chatbot,Chatbot with Tool,Ai News,Blog Generator".split(",")  
    
    def get_llm_models(self):
        return "gpt-4o-mini,gpt-35-turbo,gpt-35-turbo-instruct".split(",")  
    
    def get_page_title(self):
        return "LangGraph: Basic ChatBot"