import streamlit as st
from src.langgraphagenticai.ui.streamlit_ui.loadui import LoadStreamlitUI
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.llms.azurellm import AzureLLM
from src.langgraphagenticai.ui.streamlit_ui.display_result import DisplayStreamLitMessages
import uuid
from langgraph.checkpoint.memory import InMemorySaver

token_provider= get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
model= AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    azure_deployment= "gpt-4o-mini"
)



def  load_app():
    """
        This will load strealit app
    
    """
    if "user-session" not in st.session_state :              
              st.session_state["memory"] = InMemorySaver()
              st.session_state["user-session"]= str(uuid.uuid4())
              print(st.session_state["user-session"])

    thread_id = st.session_state["user-session"]
    memory = st.session_state["memory"]
    # Load UI
    ui = LoadStreamlitUI()    
    user_control_inputs = ui.sidebar_components()
    if not user_control_inputs:
        st.error("Error: Failed to load user input from the UI")
        return
    
    user_message = st.chat_input("Enter the message")
    
    if user_message:
        try:
            if not user_control_inputs["LLM-Key"]:
                st.error("Error : please provide llm key") 
             ## configure LLM
            azure_llm = AzureLLM(user_control_inputs) 
            selectedmodel = azure_llm.get_llm_model()
            if not selectedmodel:
                st.error("Error : LLM Model could not be initialized")

            ## Select UseCase
            usecase = user_control_inputs.get("usecases")
            if not usecase:
                st.error("Error : No Usecase selected")
            ## Graph Builder
            graph_builder = GraphBuilder(azure_llm.get_llm_model(),memory=memory)
            graph=graph_builder.setup_graph(usecase)

            ## Display results
            print(user_message)
            display_module= DisplayStreamLitMessages(graph=graph,userinput=user_message,thread_id=thread_id)
            display_module.display_on_ui()


        except Exception as e:
            st.error(e)