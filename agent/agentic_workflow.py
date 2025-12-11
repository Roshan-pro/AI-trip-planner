from utils.model_loader import ModelLoader
from prompt_library.system_prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode,tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.currency_conversion_tool import CurrencyConversionTool
from tools.expense_calculator_tool import CalculatorTool
from tools.place_search_tool import PlaceSearchTool
import os
import getpass
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGSMITH_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_WORKSPACE_ID"] = os.environ.get("LANGSMITH_WORKSPACE_ID")

class GraphBuilder:
    def __init__(self,model_provider :str="groq"):
        self.model_loader= ModelLoader(model_provider=model_provider)
        self.llm= self.model_loader.load_llm()
        self.tools=[]
        
        self.weather_tool= WeatherInfoTool()
        self.currency_tool= CurrencyConversionTool()
        self.calculator_tool= CalculatorTool()
        self.place_search_tool= PlaceSearchTool()
        
        self.tools.extend([*self.weather_tool.weather_tool_list,
                           *self.currency_tool.currency_tool_list,
                           *self.calculator_tool.calculator_tool_list,
                           *self.place_search_tool.place_search_tool
                           ])
        self.llm_with_tools= self.llm.bind_tools(tools=self.tools)
        self.graph = None
        self.system_prompt= SYSTEM_PROMPT
    def agent_function(self,state : MessagesState):
        """Main agent function to process user input and generate responses using LLM and tools."""
        user_queston=state["messages"]
        input_prompt= [self.system_prompt]+ user_queston
        response= self.llm_with_tools.invoke(input_prompt)
        return {"messages": [response]}
    def build_graph(self)-> StateGraph:
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        self.graph = graph_builder.compile()
        return self.graph
        
    def __call__(self):
        return self.build_graph()