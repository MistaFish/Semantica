class Comment:
    def __init__(self, reading_id: str, comment_text: str) -> None:
        self.id: str = reading_id
        self.comment: str = comment_text
        self.prompt: str = f"<avis>{self.id}: {self.comment}</avis>"
