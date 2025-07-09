import streamlit as st
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
import uuid
from ui.loadui import LoadStreamlitUI





async def  load_app():
    """
        This will load strealit app
    
    """

    ui=LoadStreamlitUI()
    controls= await ui.side_components()
    



    # if "user-session" not in st.session_state :              
    #           st.session_state["memory"] = InMemorySaver()
    #           st.session_state["user-session"]= str(uuid.uuid4())
    #           print(st.session_state["user-session"])

    # thread_id = st.session_state["user-session"]
    # memory = st.session_state["memory"]
    # # Load UI
    # ui = LoadStreamlitUI()    
    # user_control_inputs = ui.sidebar_components()
    # if not user_control_inputs:
    #     st.error("Error: Failed to load user input from the UI")
    #     return
    
    # user_message = st.chat_input("Enter the message")
    
    # if user_message:
    #     try:
    #         if not user_control_inputs["LLM-Key"]:
    #             st.error("Error : please provide llm key") 
    #          ## configure LLM
    #         azure_llm = AzureLLM(user_control_inputs) 
    #         selectedmodel = azure_llm.get_llm_model()
    #         if not selectedmodel:
    #             st.error("Error : LLM Model could not be initialized")

    #         ## Select UseCase
    #         usecase = user_control_inputs.get("usecases")
    #         if not usecase:
    #             st.error("Error : No Usecase selected")
    #         ## Graph Builder
    #         graph_builder = GraphBuilder(azure_llm.get_llm_model(),memory=memory)
    #         graph=graph_builder.setup_graph(usecase)

    #         ## Display results
    #         print(user_message)
    #         display_module= DisplayStreamLitMessages(graph=graph,userinput=user_message,thread_id=thread_id)
    #         display_module.display_on_ui()


    #     except Exception as e:
    #         st.error(e)