from typing import List
from .comment import Comment


class Batch:
    def __init__(self) -> None:
        self.batch_token_count: int = 0
        self.batch_size: int = 0
        self.batch: List[Comment] = []

    def add_comment(self, comment: Comment, token_count: int) -> None:
        self.batch.append(comment)
        self.batch_token_count += token_count
        self.batch_size += 1

    def reset_batch(self) -> None:
        self.batch = []
        self.batch_token_count = 0
        self.batch_size = 0

    def get_comments(self) -> str:
        comments = ""
        for comment in self.batch:
            comments += comment.prompt
            if comment != self.batch[-1]:
                comments += " "
        return comments

    def print_batch(self) -> None:
        for comment in self.batch:
            print(comment.prompt)
