from utils.expense_calculator import Caculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Caculator()
        self.calculator_tool_list = self._setup_tool()
    
    def _setup_tool(self) -> List:
        """Sets up the calculator tool for expense calculations."""
        @tool(name_or_callable="expense_calculator_tool", description="Calculates total expense based on given inputs.")
        def expense_calculator_tool(*query: int|float) -> int|float:
            return self.calculator.calculate_expense(*query)
        
        @tool(name_or_callable="estimate_total_hostel_cost", description="Estimates total hostel cost based on price per night and total days.")
        def estimate_total_hostel_cost(price_per_night: int|float, total_days: int|float) -> int|float:
            return self.calculator.multiply(price_per_night, total_days)
        
        @tool(name_or_callable="daily_budget_calculator", description="Calculates daily budget based on total expense and total days.")
        def daily_budget_calculator(total_expense: int|float, total_days: int|float) -> int|float:
            return self.calculator.calculate_daily_budget(total_expense, total_days)
        
        return [expense_calculator_tool, 
                estimate_total_hostel_cost,
                daily_budget_calculator]