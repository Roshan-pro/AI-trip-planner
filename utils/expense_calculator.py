class Caculator:
    @staticmethod
    def multiply(a:int , b: int )->int:
        return a * b
    @staticmethod
    def calculate_expense(*amount:float|int)-> float|int:
        return sum(amount)
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget

        Args:
            total (float): Total cost.
            days (int): Total number of days

        Returns:
            float: Expense for a single day
        """
        return total / days if days > 0 else 0
    