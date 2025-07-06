from src.langgraphagenticai.state.aistate import AIState

class chatbot_node:
    def __init__(self,model):
        self.model = model


    def process(self,state: AIState) -> dict:
        """
            Process the request using LLM and generate response
        """
        response = self.model.invoke(state["messages"])
        print(response.content)
        return {"messages" : response}
