import math
from itertools import combinations

data = list(map(int, open("01.txt").readlines()))


class ExpenseCalculator:
    def __init__(self, expense_report: list[int]):
        self.expense_report = expense_report

    def get_target_expenses(self, target_sum: int, expense_count: int) -> tuple[int, ...]:
        """Return expenses which sum up to the target value"""
        for combination in combinations(self.expense_report, expense_count):
            if sum(combination) == target_sum:
                return combination


calculator = ExpenseCalculator(expense_report=data)
expense_2020_by_2 = calculator.get_target_expenses(target_sum=2020, expense_count=2)
expense_2020_by_3 = calculator.get_target_expenses(target_sum=2020, expense_count=3)

print(f"PART ONE: {math.prod(expense_2020_by_2)}")
print(f"PART TWO: {math.prod(expense_2020_by_3)}")
