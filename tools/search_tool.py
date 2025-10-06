import json 
import os 
import requests
# from langchain.tools import tool
from crewai.tools import tool

class SearchTool:
    @tool("Search the internet")
    def search_internet( query):
        """Search the internet using Perplexity's Search API."""
        try:
            print(f"\n[Tool Execution] SearchTool - search_internet")
            # print(f"Arguments: query='{query}'")
            
            api_key = os.getenv("Perplexity_API_KEY")
            if not api_key:
                return "ERROR: Perplexity API key not found"
            
            # ✅ CORRECT: Use the official Search API endpoint
            url = "https://api.perplexity.ai/search"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # ✅ CORRECT: Use proper Search API parameters
            data = {
                "query": query,          # Single query string
                "max_results": 5,        # 1-20 results
                "max_tokens_per_page":  1024  # Content extraction control
            }
            
            # ✅ CORRECT: Use json parameter, not json.dumps()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code != 200:
                return f"Perplexity Search API Error {response.status_code}: {response.text}"
            
            result = response.json()
            
            # ✅ Process the search results
            if 'results' in result:
                search_results = []
                for item in result['results']:
                    search_results.append(
                        f"Title: {item.get('title', '')}\n"
                        f"URL: {item.get('url', '')}\n"
                        f"Snippet: {item.get('snippet', '')}\n"
                        f"Date: {item.get('date', '')}\n"
                        f"---"
                    )
                
                return '\n'.join(search_results)
            else:
                return "No search results found"
                
        except Exception as e:
            error_msg = f"Search error: {str(e)}"
            print(f"[Tool Error] {error_msg}")
            return error_msg



# class SearchTool:
#     @tool("Search the internet")
#     def search_internet(query):  # Remove self parameter since CrewAI tool decorator handles it
#         """Useful to search the internet about a topic or a given topic and return relevant results."""
#         print(f"\n[Tool Execution] SearchTool - search_internet")
#         print(f"Arguments: query='{query}'")
#         top_result_to_return = 4
#         api_key = os.getenv("Perplexity_API_KEY")
#         url = "https://api.perplexity.ai/search"
#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
#         payload = json.dump({ "q": query,"source": "web"})
#         response = requests.request("POST", url, headers=headers, data=payload)
#         # check if there is an organic key
#         if 'organic' not in response.json():
#             return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
#         else:
#             results = response.json()['organic']
#             string = []
#             for result in results[:top_result_to_return]:
#                 try:
#                     string.append('\n'.join([
#                         f"Title: {result['title']}", f"Link: {result['link']}",
#                         f"Snippet: {result['snippet']}", "\n-----------------"
#                     ]))
#                 except KeyError:
#                     next

#             return '\n'.join(string)


"""
data = {
    "q": "What is LangChain?",
    "source": "web"
}

response = requests.post(url, headers=headers, json=data)

data .it will create payload of format dict,byte,string etc
payload . it will create payload of format dict(automatically)

"""