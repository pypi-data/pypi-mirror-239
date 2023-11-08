# table.py

from typing import Iterable
import json
from io import StringIO

import pandas as pd

__all__ = [
    "table_to_json",
    "table_from_json"
]

def table_to_json(dataset: pd.DataFrame) -> dict[str, dict[str, ...]]:
    """
    Converts the data of the dataset to json.

    :param dataset: The dataset to process.

    :return: The json representation of the data.
    """

    return json.loads(dataset.to_json(orient='index'))
# end table_to_json

def table_from_json(data: Iterable | dict[str, dict[str, ...]]) -> pd.DataFrame:
    """
    Converts the data from json format into a dataframe object.

    :param data: The json data to process.

    :return: The data frame object.
    """

    if not isinstance(data, dict):
        data = dict(enumerate(data))
    # end if

    return pd.read_json(StringIO(json.dumps(data)), orient="index")
# end table_from_json