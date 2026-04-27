# Edgebot Internship Assessment Project

# Introduction

This is a brief (human-written!) README file to explain the architecture of the project and how to run the code.

# Setting up and Running the Project

## Setting up the environment

To set up the environment, you will need to:

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Set up the `.env` file. You will need to define the following variables:

  - `SERIES_DATA_PATH`: This will hold the path to the provided data CSV.
  - `OUTPUT_ROOT_DIR`: This will hold the path to the directory where you wish to save the output generated from user scripts (this is further explained later on).

## Running the Project

After setting up, you are ready to run the interfaces:

- To run the CLI interface, run:

  ```
  python -m user.cli [args]
  ```

- For example:
  - To the run the execute command:

    ```
    python -m user.cli execute
    ```

    Then write your script and end it with the EOF character (`CTRL-Z` on windows and `CTRL+D` on Unix-like systems).

  - To run the view command:

    ```
    python -m user.cli view f2de9b89-9502-4879-be08-26f4b2c80cdb btc eth
    ```

- To run the RESTAPI interface, run:

  ```
  python -m user.rest_api [args]
  ```

You can query the endpoints of the API as demonstrated in the instructions pdf.

# Organization of the Modules

This project follows a [three-tier](https://www.ibm.com/think/topics/three-tier-architecture) architecture. `data/` represents the data tier, `engine/` represents the application tier, and `user/` represents the presentation tier.

## Data Tier (`/data`)

This module consists of:

- `SeriesDataLoader`: The class responsible for handling data interactions with the provided time series CSV.
- `UserSeriesStorage`: The class responsible for handling data interactions with the `output` directory. The series generated during every script run are saved as a JSON file in the `output` directory.

_Note that I could have saved the user-generated series as a `.csv`. This has the benefit of staying consistent with the given data format and it also allows me to use the same class to access and manipulate both types of data: fixed series and user-generated series. However, since this is an assessment about system organization, I decided I would organize the data in the way I would usually opt for._

## Application Tier (`engine/`)

This module consists of:

- `parser.py`: A file consisting of helper functions designed to parse the user script to a more manageable format.
- `Transformation`: The class responsible for taking transformation inputs and actually running the appropriate transformations.
- `Engine`: The application tier class that faces the presentation tier. This class orchestrates the invocation of the parser functions and the transformations. It exposes functions such as `execute` and `view`.
  - `execute` takes a user script as a string and returns an `id` as specified by the requirements.
  - `view` takes an `id` and a list of `items` and returns the user's series as specified by the requirements.

## Presentation Tier (`/user`)

This module consists of `cli.py` and `rest_api.py` which can both be used as demonstrated in the requirements pdf.
