# from langchain.tools import tool
from crewai.tools import tool

class CalculatorTool:
    @tool("Make a Calculation") 
    def calculator(operation):  # Remove self parameter since CrewAI tool decorator handles it
        """Useful to perform any mathematical calculations,
        like sum, minus, multiplication, division, etc.
        The input to this tool should be a mathematical
        expression, a couple examples are `200*7` or `5000/2*10`
        """
        print(f"\n[Tool Execution] CalculatorTool - calculator")
        # print(f"Arguments: operation='{operation}'")
        try:
            return eval(operation)
        except Exception:
            return "Error: Invalid syntax in mathematical expression"
          
    
# from pydantic import BaseModel, Field
# from langchain.tools import tool

# # Define a Pydantic model for the tool's input parameters
# class CalculationInput(BaseModel):
#     operation: str = Field(..., description="The mathematical operation to perform")
#     factor: float = Field(..., description="A factor by which to multiply the result of the operation")

# # Use the tool decorator with the args_schema parameter pointing to the Pydantic model
# @tool("perform_calculation", args_schema=CalculationInput, return_direct=True)
# def perform_calculation(operation: str, factor: float) -> str:
#     """
#     Performs a specified mathematical operation and multiplies the result by a given factor.

#     Parameters:
#     - operation (str): A string representing a mathematical operation (e.g., "10 + 5").
#     - factor (float): A factor by which to multiply the result of the operation.

#     Returns:
#     - A string representation of the calculation result.
#     """
#     # Perform the calculation
#     result = eval(operation) * factor

#     # Return the result as a string
#     return f"The result of '{operation}' multiplied by {factor} is {result}."