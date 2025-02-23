"""State management for the retrieval graph

This module defines the state structures used in the retrieval graph. It includes
definition for agent state, input state, and router classification schema.
"""

from dataclasses import dataclass, field
from typing_extensions import Annotated, Literal, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

from src.shared.state import reduce_docs

@dataclass(kw_only=True)
class InputState:
  """Represents the input state for the agent

  This class defines the structure of the input state, which includes
  the messages exchanged between the user and the agent. It serves as a restricted
  version of the full state, providing a narrower interface to the outside world
  compared to what is maintained internally.
  """
  messages: Annotated[list[AnyMessage], add_messages]


class Router(TypedDict):
  """Classify user query """
  logic: str
  type: Literal["more-info", "relevant", "general"]



# This is the primary state of your agent, where you can store any information

@dataclass(kw_only=True)
class AgentState(InputState):

  router: Router = field(default_factory=lambda: Router(type="general", logic=" "))
  # """The router's classification of the user's query"""

  steps: list[str] = field(default_factory=list)
  """A list of steps in the research plan"""

  documents: Annotated[list[Document], reduce_docs] = field(default_factory=list)
  """Populated by the retriever. This is a list of document that the agent can reference"""
