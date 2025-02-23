from src.retrieval_graph import graph
from IPython.display import display, Image
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
import asyncio
from dotenv import load_dotenv
load_dotenv()

# display(Image(graph.get_graph(xray=True).draw_mermaid_png()))  // Works in jupyter notebook only use the below code to generate an image of the graph

# # Save the graph as a PNG file
# graph_image = graph.get_graph(xray=True).draw_mermaid_png()
# with open("retrieval_graph.png", "wb") as f:
#     f.write(graph_image)

# print("Graph saved as 'retrieval_graph.png'. Open this file to view the graph.")





async def run_graph():
    config = {
        "configurable": {
            "thread_id": "1",
            "retriever_provider": "mongodb"
        }
    }
    
    
    config = {"configurable" : {
                    "thread_id" :  "1",
                    "retriever_provider": "mongodb"
                }
            }
    async for chunk in graph.astream({"messages": [HumanMessage(content = "Explain Establishment of GHG emission intensity trajectory?")]}, config, stream_mode="values"):
        # print(chunk)
        for m in chunk['messages']:
                m.pretty_print()
        print("---"*25)
    

# Run the async function using asyncio
asyncio.run(run_graph())