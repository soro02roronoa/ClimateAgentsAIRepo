from langchain_core.vectorstores import VectorStoreRetriever
from typing import Generator
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
import os

def initialize_vectorStore_temp():
    client = MongoClient(os.getenv("MONGODB_URI"))
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
    
    return client
    

def initialize_vectorStore(COLLECTION_NAME: str, ATLAS_VECTOR_SEARCH_INDEX_NAME: str, create_Index = False)-> Generator[VectorStoreRetriever, None, None]:
    client = MongoClient(os.getenv("MONGODB_URI"))
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
    DB_NAME = "PDFs_Embeddings"

    MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )
    
    if create_Index == True:
        try: 
            vector_store.create_vector_search_index(dimensions=1536)
            print("Vector Index Created")
        except Exception as e:
            print(e)
    

    return vector_store.as_retriever()


# def create_Vector_Index(COLLECTION_NAME: str, ATLAS_VECTOR_SEARCH_INDEX_NAME: str):    
    
#     vector_store = MongoDBAtlasVectorSearch(
#         collection=MONGODB_COLLECTION,
#         embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
#         index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
#         relevance_score_fn="cosine",
#     )
#     ## currenlty not working with our database (name -> ServerlessInstance0)
#     try: 
#         vector_store.create_vector_search_index(dimensions=1536)
#         print("Vector Index Created")
#     except Exception as e:
#         print(e)
        