from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.aistate import AIState
from src.langgraphagenticai.nodes.chatbot_node import chatbot_node


class GraphBuilder:

    def __init__(self,model):
        self.llm = model
        self.graph =  StateGraph(AIState)

    def get_basic_chatbot(self):
        self.basic_chatbot = chatbot_node(self.llm)    

        self.graph.add_node("chatbot",self.basic_chatbot.process)
        self.graph.add_edge(START,"chatbot")
        self.graph.add_edge("chatbot",END)
        return self.graph.compile()
    
    def setup_graph(self, usecase): 
        if usecase =="Basic Chatbot" :
            return self.get_basic_chatbot()
        elif usecase == "Chatbot with Tool" : 
            pass
        elif usecase == "Ai News":
            pass
        elif usecase == "Blog Generator":
            pass





