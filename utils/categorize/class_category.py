from typing import Dict
from utils.categorize.class_sub_category import Sub_category

class Category():
    def __init__(self, num_category: str, name: str):
        self.num_category: str = num_category
        self.name: str = name
        self.sub_categories: Dict[str, Sub_category] = {}

    def add_sub_category(self, num_sub_category: str, sub_category: Sub_category):
        self.sub_categories[num_sub_category] = sub_category

    def get_prompt(self):
        prompt = f"{self.num_category} : {self.name}\n"
        for num_sub_category, sub_category in self.sub_categories.items():
            prompt += f"{num_sub_category} : {sub_category.name}\n"
        prompt += "\n"
        return prompt