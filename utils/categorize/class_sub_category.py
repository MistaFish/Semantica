class Sub_category():
    def __init__(self, num_sub_category: str, name: str):
        self.num_sub_category: str = num_sub_category
        self.name: str = name
        self.satisfied: list[str] = []  # List to hold identifiers of satisfied reviews
        self.not_satisfied: list[str] = []  # List to hold identifiers of not satisfied reviews

    def add_review(self, review_id: str, satisfaction: str):
        if satisfaction == 'S':
            self.satisfied.append(review_id)
        elif satisfaction == 'NS':
            self.not_satisfied.append(review_id)
