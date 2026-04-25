from pathlib import Path
import json

class UserSeriesStorage:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

    def get_output(self, output_id:str):
        with open(self.root_dir / (output_id + '.json'), 'r') as f:
            data = json.loads(f.read())
        return data
    
    def save_output(self, output_id:str, output):
        self.root_dir.mkdir(parents=True, exist_ok=True)
        with open(self.root_dir / (output_id + '.json'), 'w') as f:
            json.dump(output, f)