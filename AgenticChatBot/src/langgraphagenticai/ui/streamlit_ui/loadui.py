import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        print(self.config)
        self.user_controls= {}

    def sidebar_components(self):
        st.header("🧙🏻‍♂️" + "test")#self.config.get_page_title())
        with st.sidebar:            
            self.user_controls["llmoptions"]=st.selectbox("LLM Options",self.config.get_llm_options())
            self.user_controls["models"]=st.selectbox("Models",self.config.get_llm_models())
            self.user_controls["LLM-Key"] = st.text_input("Please Enter Key to use LLM",type="password")
            if not self.user_controls["LLM-Key"]:
                st.warning("Please provide the key")

            self.user_controls["usecases"]=st.selectbox("Use Cases",self.config.get_use_cases())
        return  self.user_controls

