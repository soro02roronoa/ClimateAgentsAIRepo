from dotenv import load_dotenv
load_dotenv()
from vector_store import initialize_vectorStore
import asyncio
COLLECTION_NAME="D1_AccreditationProcedureandEligibilityCriteriaforAccreditedCarbonVerificationAgency"
ATLAS_VECTOR_SEARCH_INDEX_NAME="D1_AccreditationProcedureandEligibilityCriteriaforAccreditedCarbonVerificationAgency_Index"
vector_store = initialize_vectorStore(COLLECTION_NAME=COLLECTION_NAME, ATLAS_VECTOR_SEARCH_INDEX_NAME=ATLAS_VECTOR_SEARCH_INDEX_NAME)

async def query(query  :str):
    results = await vector_store.ainvoke(
        "what is ghg emissions?", k=1
    )
    for res in results:
        print(res)

    
asyncio.run(query("Explain Team Members (Compliance Mechanism) (2 members)"))