import uuid
from .transformations import Transformation
from . import parser

from data import UserSeriesStorage

class Engine:
    def __init__(self, series_data_path, output_data_path):
        self.transformer = Transformation(series_data_path)
        self.data_accessor = UserSeriesStorage(output_data_path)

    def view(self, output_id, series):
        output = self.data_accessor.get_output(output_id)
        res = {series_name: output[series_name] for series_name in series}
        return res

    def run_engine(self, script):
        parsed_script = parser.parse_script(script)
        context = {}
        for command in parsed_script:
            self.update_context(context, command)
        return self.save_context(context)

    def update_context(self, context, command):
        input_config = command["config"]
        input_series = [context[series_name] for series_name in command["series_names"]]
        res = self.transformer.apply_transformation(command["transformation_id"], *input_config, *input_series)
        context[command["main_id"]] = res

    def save_context(self, output):
        output_id = str(uuid.uuid4())
        self.data_accessor.save_output(output_id, output)
        return output_id
