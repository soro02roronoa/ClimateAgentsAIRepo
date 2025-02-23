from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing_extensions import Any, Annotated, Literal, Optional, Type, TypeVar

from langchain_core.runnables import RunnableConfig, ensure_config

@dataclass(kw_only=True)
class BaseConfiguration:
  """configuration class for indexing and retrieval operations

    This class defines the parameters needed for configuring the indexing and
    retrieval processes, including embedding model selection, retriever provider choice, and search parameters.
  """

  embedding_model: Annotated[
      str,
      {"_template_metadata_":{"kind":"embeddings"}},
  ] = field(
      default="openai/text-embedding-3-small",
      metadata={
          "description":"Name of the embedding model to use. Must be a valid embedding model name. "
      }
  )


## will be usign mongoDb
  retriever_provider: Annotated[
      Literal["elastic-loacl", "elastic", "pinecone", "mongodb"],
      {"_template_metadata": {"kind": "retriever"}}
  ] = field(
      default="mongodb",  ## Changed the default to mongodb
      metadata={
          "description":"The vector store provider to use for retrieval. "
      }
  )

  search_kwargs: dict[str, Any] = field(
      default_factory=dict,
      metadata={
          "description": "Additional keyword arguments to pass to the search function of the retriever."
      }
  )


  @classmethod
  def from_runnable_config(
        cls: Type[T], config: Optional[RunnableConfig] = None
    ) -> T:
      """
      Create an IndexConfiguration instance from a RunnableConfig object.

      Args:
          cls (Type[T]): The class itself.
          config (Optional[RunnableConfig]): The configuration object to use.

      Returns:
          T: An instance of IndexConfiguration with the specified configuration.
      """
      config = ensure_config(config)
      configurable = config.get("configurable") or {}
      _fields = {f.name for f in fields(cls) if f.init}
      return cls(**{k: v for k, v in configurable.items() if k in _fields})


T = TypeVar("T", bound=BaseConfiguration)
