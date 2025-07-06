from typing import Annotated,Sequence,TypedDict
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AIState(TypedDict):
    messages : Annotated[list,add_messages]

