from tqdm import tqdm

class LoadingBar:
    def __init__(self, total_batches):
        self.pbar = tqdm(
            total=total_batches,
            ncols=50,  # Adjust ncols to your desired width
            colour='#37B6BD',
        )

    def update(self):
        self.pbar.update(1)

    def close(self):
        self.pbar.close()
