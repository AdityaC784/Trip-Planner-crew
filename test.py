#%%
import os
from dotenv import load_dotenv
from tools.search_tool import  search_internet

load_dotenv()

# Test the search tool directly
# search_tool_instance = SearchTool()
result =search_internet("best restaurants in Pune")
print("Search Result:")
print(result)
# %%
