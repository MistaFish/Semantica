from typing import Dict

class Reviewer:
    def __init__(self, reviewer_id: str):
        self.reviewer_id: str = reviewer_id
        self.satisfaction: Dict[str, str] = {}  # Dictionary to hold satisfaction levels for each sub-category

    def add_satisfaction(self, num_sub_category: str, satisfaction: str):
        self.satisfaction[num_sub_category] = satisfaction

    def get_promt(self):
        return f"{self.reviewer_id} : {self.satisfaction}"
