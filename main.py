from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse

import os
import datetime
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="Agentic Workflow API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        graph_builder = GraphBuilder(model_provider="groq")
        react_app = graph_builder()
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_graph)
        print("Graph image saved as graph.png")
        messages = {"messages":[query.question]}
        output = react_app.invoke(messages)
        if isinstance(output, dict) and "messages" in output:
            response_message = output["messages"][-1].content 
        else:
            response_message = str(output)
        return {"response": response_message}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})