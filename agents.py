from crewai import Agent , LLM
import os
from textwrap import dedent  ##extra whitespaces removed
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
# from langchain_perplexity import ChatPerplexity
from tools.search_tool import SearchTool
from tools.calculator_tool import CalculatorTool

load_dotenv()



"""
Creating Agent:
-Think like a boss. whork backward from the goal and think which employee you need to hire to do get 
the job done.
-define the captain of the crew whi orients the crew toward the goal
-define which experts the captain need to communicate with and delegate task to.
  Build top down structure of the crew

Goal:
 -Create the 7 days travel itenerary with detailed per day plans,
 including budget , packing suggestions, and safety tips

Captain/Manager/Boss:
 -Expert Taverl Agent

Exployees/Experts to hire:
 -City Selection Expert
 -Local Tour Guide


Note:
Agent should be result driven and clear about the goal.
Role is their job title
Goal Should Actionableq and clear
Backstory should be relevant to the goal and role

"""


class TravelAgents:
    def __init__(self):
        api_key=os.environ["Perplexity_API_KEY"]
        # self.GEMINI =LLM(model="gemini/gemini-2.5-flash", temperature=0.65, api_key=api_key)
        # self.GEMINI =LLM(model="groq/llama-3.3-70b-versatile", temperature=0.65)
        self.GEMINI =LLM(model="perplexity/sonar-reasoning", temperature=0.65, api_key=api_key)
        # self.GEMINI =LLM(model="huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", temperature=0.65, api_key=api_key)

        
        # # Create tool instances 
        # self.search_tool = SearchTool()
        # self.calculator = CalculatorTool()

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(
                f"""Expert in travel planning and logistics.
                i have decades of experience making travel iteneraries.""" ),
            goal=dedent(F""""
                        Create a 7-days tavel itinerary wit detailed per-day plans, including budget,
                        packing suggestions, and safety tips.
                        """),
            tools=[ 
                # self.search_tool.search_internet,
                # self.calculator.calculator
                SearchTool.search_internet,
                CalculatorTool.calculator
                ],
            verbose=True,
            llm=self.GEMINI,
            system_message='''You have access to real-time web search through Google. Use web search to f
                          ind current information about travel destinations, weather, hotels, and attractions.'''
        )
    
    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory=dedent(
                f"""Expert at analyzing travel data to pick ideal destinations."""),
            goal=dedent(
                f"""Select the best cities based  on weather , season , prices , and travel interests.""" ),
            tools=[
                # self.search_tool.search_internet,
                SearchTool.search_internet,
            
                ],
            verbose=True,
            llm=self.GEMINI,
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(f"""Knowledgeable local guide with extensive information
                about the city, it's attractions and customs"""),
            goal=dedent(f"""Provide the BEST insights about the selected city"""),  
            tools=[
                #self.search_tool.search_internet,
                SearchTool.search_internet,
            
                ],
            verbose=True,   
            llm=self.GEMINI,
        )   
