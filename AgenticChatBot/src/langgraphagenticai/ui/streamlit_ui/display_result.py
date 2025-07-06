import streamlit as st


class DisplayStreamLitMessages:
     def __init__(self,graph,userinput):
          self.graph=graph
          self.useinput = userinput
        

     def  display_on_ui(self):
         try:
          input = {"messages":("user",self.useinput)}
          events= self.graph.stream(input)          
          for event in events:
              for value in event.values():
                   with st.chat_message('user'):
                        st.write(self.useinput)
                   with st.chat_message('assistant'):
                        st.write(value["messages"].content)
         except Exception as e:
             raise e