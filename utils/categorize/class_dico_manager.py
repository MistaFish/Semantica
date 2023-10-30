import csv
import json
from utils.categorize.class_category import Category
from utils.categorize.class_sub_category import Sub_category
from utils.categorize.class_reviewer import Reviewer
from typing import Dict


file_path = '/Users/chsimon/Documents/SemanticaFolder/SemanRepo/outputs/dico_semantique.csv'

class Dico_manager():
    def __init__(self):
        self.categories: Dict[str, Category] = {}
        self.reviewers: Dict[str, Reviewer] = {}
        self._parse_csv(file_path)


    def get_categories_prompt(self):
        prompt = ""
        for num_category, category in self.categories.items():
            prompt += category.get_prompt()
        return prompt            
        
    def print_categories_prompt(self):
        print(self.get_categories_prompt())
    
    def get_reviewers_prompt(self):
        prompt = ""
        for reviewer_id, reviewer in self.reviewers.items():
            prompt += reviewer.get_promt()
        return prompt

    def _parse_csv(self, file_path: str):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)
            for row in csvreader:
                num_category, name_category, num_sub_category, name_sub_category = row
                if num_category not in self.categories:
                    self.categories[num_category] = Category(num_category , name_category)
                # Create Sub_category object
                sub_category = Sub_category(num_sub_category, name_sub_category)
                # Add Sub_category object to the appropriate Category object
                self.categories[num_category].add_sub_category(num_sub_category, sub_category)

    def process_reviews(self, reviews_string: str):
        reviews = json.loads(reviews_string)
        
        for review_id, categories in reviews.items():
            if review_id not in self.reviewers:
                self.reviewers[review_id] = Reviewer(review_id)
            for num_sub_category, satisfaction in categories.items():
                # Assuming num_sub_category has the format "X.Y"
                num_category = num_sub_category.split('.')[0] + '.'
                # Update the Sub_category object with this review's satisfaction level
                self.categories[num_category].sub_categories[num_sub_category].add_review(review_id, satisfaction)
                # Update the Reviewer object with this sub-category's satisfaction level
                self.reviewers[review_id].add_satisfaction(num_sub_category, satisfaction)


    def write_to_enriched_reviews(self, file_path: str):
        # Get a list of all sub_category numbers and names
        sub_category_headers = [f'{sub_cat_num} - {sub_category.name}'
                                for cat_num, category in self.categories.items()
                                for sub_cat_num, sub_category in category.sub_categories.items()]

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['reviewer_id'] + sub_category_headers
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Iterate through each reviewer and write their satisfaction levels to the CSV
            for reviewer_id, reviewer in self.reviewers.items():
                # Initialize a dictionary to hold this reviewer's satisfaction levels
                row_dict = {'reviewer_id': reviewer_id}
                # Fill in satisfaction levels for each sub-category
                for sub_cat_num in sub_category_headers:
                    # Parse the sub-category number from the header (assuming format 'X.Y - Name')
                    num_sub_category = sub_cat_num.split(' - ')[0]
                    # Get satisfaction level for this sub-category, or 'NA' if not found
                    row_dict[sub_cat_num] = reviewer.satisfaction.get(num_sub_category, 'NA')
                # Write this reviewer's satisfaction levels to the CSV
                writer.writerow(row_dict)


