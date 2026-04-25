import csv

class SeriesDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_data(self):
        self.data = {}
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            
            for row in reader:
                name = row[0]
                self.data[name] = list(map(float, row[1:]))

    def get_series(self, series_name):
        if self.data is None:
            self.read_data()
        return self.data[series_name]
