"""Define the configurable parameters for the agent """

from __future__ import annotations

from dataclasses import dataclass, field
from typing_extensions import Annotated
from src.retrieval_graph import prompts
from src.shared.configuration import BaseConfiguration

@dataclass(kw_only=True)
class AgentConfiguration(BaseConfiguration):

  # models
  query_model: Annotated[
      str,
      {"_template_metadata_": {"kind":"llm"}}
  ] = field(
      default="openai/gpt-3.5-turbo",
      metadata={
          "description":"The language model used for processing and refining queries. Should be in the form: provider/model-name"
      }
  )

  response_model: Annotated[str, {"_template_metadata_":{"kind":"llm"}}] = field(
      default="openai/gpt-3.5-turbo",
      metadata={
          "description":"The language model used for generating responses."
      }
  )

  # prompts
  router_system_prompt: str = field(
        default=prompts.ROUTER_SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt used for classifying user questions to route them to the correct node."
        },
    )

  more_info_system_prompt: str = field(
        default=prompts.MORE_INFO_SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt used for asking for more information from the user."
        },
    )

  general_system_prompt: str = field(
      default=prompts.GENERAL_SYSTEM_PROMPT,
      metadata={
          "description": "The system prompt used for responding to general questions."
      },
  )

  research_plan_system_prompt: str = field(
      default=prompts.RESEARCH_PLAN_SYSTEM_PROMPT,
      metadata={
          "description": "The system prompt used for generating a research plan based on the user's question."
      },
  )

  generate_queries_system_prompt: str = field(
      default=prompts.GENERATE_QUERIES_SYSTEM_PROMPT,
      metadata={
          "description": "The system prompt used by the researcher to generate queries based on a step in the research plan."
      },
  )

  response_system_prompt: str = field(
      default=prompts.RESPONSE_SYSTEM_PROMPT,
      metadata={"description": "The system prompt used for generating responses."},
  )