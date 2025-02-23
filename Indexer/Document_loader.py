from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
from langchain_core.documents import Document



def document_loaders(file_path: str):
  
  loader = PyPDFLoader(
    file_path = file_path,
  )

  docs_list_ICM = [] # stores processed content into docs_ICM list
  docs_lazy = loader.lazy_load() # loads a PDF incrementally

  for doc in docs_lazy:
    docs_list_ICM.append(doc)

  text_splitter_ICM = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200
    )
  # splited documents
  doc_splits_ICM = text_splitter_ICM.split_documents(docs_list_ICM)

  # Converting splitted documents in the "Documemnt" format (suited for storage in vector_store)
  documenting = []
  for doc in doc_splits_ICM:
    documenting.append(Document(page_content=doc.page_content, metadata= doc.metadata))


  uuids = [str(uuid4()) for _ in range(len(documenting))]
  # returns documents and their corresponding universally unique ids
  return (documenting, uuids)


