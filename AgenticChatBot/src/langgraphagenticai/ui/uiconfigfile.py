from configparser import ConfigParser



class Config:
    def __init__(self,config_file = "./src/langgraphagenticai/ui/uiconfigfile.ini"):
        self.config= ConfigParser()
        self.config.read(config_file)


    def get_llm_options(self):
        print(self.config["DEFAULT"].get("LLM_Options"))
        return self.config["DEFAULT"].get("LLM_Options").split(",")    
    
    def get_use_cases(self):
        return self.config["DEFAULT"].get("Use_Cases").split(",")  
    
    def get_llm_models(self):
        return self.config["DEFAULT"].get("LLM_Models").split(",")  
    
    def get_page_title(self):
        print(self.config["DEFAULT"])
        return self.config["DEFAULT"].get("PAGE_TITLE")