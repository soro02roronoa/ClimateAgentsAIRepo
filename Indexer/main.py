from Document_loader import document_loaders
from vector_store import initialize_vectorStore_temp
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from glob import glob
from argparse import ArgumentParser
import os
import json
from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)




def main(args):
    logger.info("Initializing vectore store Clinet...")
    vector_store_client = initialize_vectorStore_temp()
    logger.info("MongoDB client initialized...")
    DB_NAME = "PDF_Embeddings"
    DataBase = vector_store_client.get_database(DB_NAME)

    try:
        # Read frameworks.json instead of trying to parse TypeScript
        with open(os.path.join(os.path.dirname(__file__), 'frameworks.json'), 'r') as f:
            frameworks_config = json.load(f)['frameworks']
        logger.info("Loaded frameworks configuration from JSON file")
    except Exception as e:
        logger.error(f"Error loading frameworks configuration: {str(e)}")
        raise

    # print(frameworks_config)





    """"Getting the name of the collection, similar to get_collection_name function from vector_store_init.py"""
    logger.info("finding the names of collections to be created in the database from the json config file")
    collection_name_list = []
    for framework_id in ["1","2","3","4","5"]:
        framework = next(
            (f for f in frameworks_config if str(f['id']) == framework_id),
            None
        )
        if not framework:
            raise ValueError(f"Framework {framework_id} not found in configuration")
        collection_name_list.append(framework['collection_name'])
        # print(framework['collection_name'])
    print(f"List of collection names : {collection_name_list}")
    logger.info(f"Collection names found are : {collection_name_list}")


    """Creating the collections in the database using collection names found above"""

    for framework_id in ["1","2","3","4","5"]:
        framework = next(
            (f for f in frameworks_config if str(f['id']) == framework_id),
            None
        )
        if not framework:
            raise ValueError(f"Framework {framework_id} not found in configuration")
        
        collection_name = framework["collection_name"]
        print(f"Collection Name : {collection_name}")
        

        try:
            # First, check if the collection exists and create it if needed
            if collection_name not in DataBase.list_collection_names():
                DataBase.create_collection(collection_name)
                logger.info(f"Created collection: {collection_name}")

            else:
                logger.info(f"Using existing collection: {collection_name}")


            MondoDB_Collection = vector_store_client[DB_NAME][collection_name]

            vector_store_object = MongoDBAtlasVectorSearch(
                collection=MondoDB_Collection,
                embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
                index_name=collection_name+"_index",
                relevance_score_fn='cosine',
            )


            """Extraing the pdfs content..."""
            logger.info(f"Extraing the pdfs content for the {collection_name}...")
            # for framework_id in ["1","2","3","4","5"][0:2]:
            #     framework = next(
            #         (f for f in frameworks_config if str(f['id']) == framework_id),
            #         None
            #     )
            #     if not framework:
            #         raise ValueError(f"Framework {framework_id} not found in configuration")

            pdf_paths = framework['pdfs']
            # print(type(pdf_paths))
            

            for pdf in pdf_paths:
                path = pdf["pdfUrl"]
                print(f"path : {path}")
                ## load the documents usign the "path" and store them in the mongodb
                document , uids = document_loaders(path)
                # print(f"document : \n {document}")
                # print("==="*25)
                vector_store_object.add_documents(documents=document,ids=uids)
                logger.info(f"Pdf named {path} added successfully to vector_store...")



            try : 
                logger.info(f"Trying to create vector seach index...")
                vector_store_object.create_vector_search_index(dimensions=1536)
                logger.info(f"Successfully created the vector index with name {collection_name}_index")
            except:
                logger.info(f"Either Failed to create vector index : {collection_name + 'index'} \n or it has been already created... Please check Manually")


        except Exception as e:
            logger.error(f"Error creating/checking collection: {str(e)}")
            raise
    
    print("---"*25)






if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--create_index",type=bool, default=False, required=False,help="Set true if you want to create a vector index")
    args = parser.parse_args()
    main(args)
