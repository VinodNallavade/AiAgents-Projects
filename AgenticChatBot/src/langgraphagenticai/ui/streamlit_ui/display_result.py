import streamlit as st
import uuid


class DisplayStreamLitMessages:
     def __init__(self,graph,userinput,thread_id):
          self.graph=graph
          self.useinput = userinput
          self.thread_id = thread_id
        

     def  display_on_ui(self):
         try:              
          input = {"messages":("user",self.useinput)}
          print("Thread id - " , self.thread_id)
          events= self.graph.stream(input,{"configurable": {"thread_id": self.thread_id}})          
          for event in events:
              for value in event.values():
                   with st.chat_message('user'):
                        st.write(self.useinput)
                   with st.chat_message('assistant'):
                        st.write(value["messages"].content)
         except Exception as e:
             raise e