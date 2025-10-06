
from crewai import Crew
from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks

from dotenv import load_dotenv
load_dotenv()

class TripCrew:
    def __init__(self,origin,cities,date_range,interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents()
        tasks = TravelTasks()

        # Define your custom agents and tasks here

        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        # Custom tasks include agent name and variables as input
        
        identify_city = tasks.identify_city(
            city_selection_expert,
            self.origin,
            self.cities,
            self.date_range,
            self.interests,
        )

        gather_city_info = tasks.gather_city_info(
            local_tour_guide,
            "{{identify_city.output}}", # ✅Use output from previous task
            self.date_range,
            self.interests
        )

        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent,
            "{{identify_city.output}}",  # ✅ Use selected city
            self.date_range,
            self.interests,
            
        )
        
        # Set up dependencies **here** (after instantiation, before running Crew)
        plan_itinerary.context = [identify_city, gather_city_info]

        # [Optional] add context for gather_city_info if needed
        # gather_city_info.context = [identify_city]
         

         # Define your custom crew here

        crew =Crew(
            agents=[
                expert_travel_agent,
                city_selection_expert,
                local_tour_guide
            ],
            tasks=[
                identify_city,
                gather_city_info,
                plan_itinerary
            ],
            verbose=True
        )

        result = crew.kickoff()
        return result
    

# This is the main function that you will use to run your custom crew.

if __name__ == "__main__":
    try:

        print("## Welcome to Trip Planner Crew")
        print('-------------------------------')
        origin = input(
            dedent("""
        From where will you be traveling from?
        """))
        cities = input(
            dedent("""
        What are the cities options you are interested in visiting?
        """))
        date_range = input(
            dedent("""
        What is the date range you are interested in traveling?
        """))
        interests = input(
            dedent("""
        What are some of your high level interests and hobbies?
        """))

        trip_crew = TripCrew(origin, cities, date_range, interests)
        result = trip_crew.run()

        print("\n" + "="*50)
        print("## YOUR PERSONALIZED TRIP PLAN")
        print("="*50 + "\n")
        print(result)
        
        # Optional: Save to file
        with open(f"trip_plan_{date_range.replace(' ', '_')}.txt", "w") as f:
            f.write(str(result))
        print(f"\n✅ Trip plan saved to file!")
    
    except Exception as e:
            print(f"❌ Error creating trip plan: {str(e)}")


        



# %%

'''Both "{{identify_city.output}}" in your task arguments and .context = [identify_city, gather_city_info] 
serve different—but complementary—roles. Here’s why both are needed:'''

#1. "{{identify_city.output}}" in Arguments
#Purpose:This tells CrewAI that the value for this parameter should come from the output of another task.
#Effect:The planner task will receive the result (city name, etc.) returned by the identify_city task as its input.



#2. .context = [...] Between Tasks
#Purpose: This tells CrewAI about task dependencies—i.e., which tasks must run first, and whose outputs are 
#         available to subsequent tasks.
#Effect: CrewAI knows that plan_itinerary should wait for identify_city and gather_city_info to complete, and 
#        makes their outputs available for templating (e.g., inside "{{identify_city.output}}").


"""   So you only specify "{{identify_city.output}}" as a parameter if that's all that is needed for that explicit 
field. For broader context and info, the LLM can access other task outputs via the .context mechanism during 
reasoning!   """