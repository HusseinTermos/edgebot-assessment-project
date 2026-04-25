import os
from dotenv import load_dotenv
load_dotenv()

OUTPUT_ROOT_PATH = os.getenv("OUTPUT_ROOT_DIR")
SERIES_DATA_PATH = os.getenv("SERIES_DATA_PATH")