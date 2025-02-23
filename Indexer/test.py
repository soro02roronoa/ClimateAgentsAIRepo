# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv
# load_dotenv()

# # os.environ["MONGODB_URI"] = "mongodb+srv://pchandrode2002:EWKdfnuy6MmdLWQx@cluster0.j3z2u.mongodb.net/"
# client = MongoClient(os.getenv("MONGODB_URI"))
# client.admin.command('ping')
# print("ok")

from Document_loader import document_loaders

import logging
import os
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


try:
    # Read frameworks.json instead of trying to parse TypeScript
    with open(os.path.join(os.path.dirname(__file__), 'frameworks.json'), 'r') as f:
        frameworks_config = json.load(f)['frameworks']
    logger.info("Loaded frameworks configuration from JSON file")
except Exception as e:
    logger.error(f"Error loading frameworks configuration: {str(e)}")
    raise

# print(type(frameworks_config))
for framework_id in ["1","2","3","4","5"][0:2]:

    framework = next(
        (f for f in frameworks_config if str(f['id']) == framework_id),
        None
    )
    if not framework:
        raise ValueError(f"Framework {framework_id} not found in configuration")

    pdf_paths = framework['pdfs']
    # print(type(pdf_paths))
    print("---"*25)

    for pdf in pdf_paths:
        path = pdf["pdfUrl"]
        print(f"path : {path}")
        ## load the documents usign the "path" and store them in the mongodb
        document , uids = document_loaders(path)
        print(f"document : \n {document}")
        print("==="*25)