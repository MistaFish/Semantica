import csv
from tiktoken import Encoding, get_encoding

from ..comment import Comment
from ..batch import Batch
from ..constants.params import TOKEN_LIMIT

class CSVExtractor:
    def __init__(self, filename: str, total_line_count: int) -> None:
        self.filename: str = filename
        self.encoder: Encoding = get_encoding("cl100k_base")
        self.Batch: Batch = Batch()
        self.total_line_count: int = total_line_count
        self.last_read_position: int = 0
        self.total_comments: int = 0
        self.total_tokens: int = 0
        self.total_batches: int = 0
        self.eof: bool = False


    def _count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))


    def extract_comments_in_batches(
        self, max_tokens: int = TOKEN_LIMIT
    ) -> Batch | None:
        total_token_count: int = 0


        with open(self.filename, "r") as file:
            self.Batch.reset_batch()
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i < self.last_read_position:
                    continue


                reading_id = f"P{reader.line_num}"
                comment_text = row["f600_comment"]
                comment = Comment(reading_id, comment_text)
                token_count = len(self.encoder.encode(comment.comment))


                if total_token_count + token_count >= max_tokens:
#                     self.Batch.print_batch()
#                     print(
#                         f"Stopped at line {reader.line_num} with \
# {total_token_count} tokens and in batch {self.Batch.batch_size} reviews."
#                     )
                    self.last_read_position = i
                    break
                total_token_count += token_count
                self.total_comments += 1
                self.Batch.add_comment(comment, token_count)
                if reader.line_num == self.total_line_count:
#                     self.Batch.print_batch()
#                     print(
#                         f"Stopped at line {reader.line_num} with \
# {total_token_count} tokens and in batch {self.Batch.batch_size} reviews."
#                     )
#                     print("Reached EOF.")
                    self.eof = True
                    break


        self.total_batches += 1
        self.total_tokens += total_token_count
        # print(f"Total Tokens Processed: {self.Batch.batch_token_count}")
        return self.Batch