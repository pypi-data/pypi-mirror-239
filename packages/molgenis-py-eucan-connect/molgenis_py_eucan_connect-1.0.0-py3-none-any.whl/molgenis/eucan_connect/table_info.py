from enum import Enum
from typing import List

import pandas as pd


class TableType(Enum):
    """
    Enum representing the tables the core EUCAN-Connect Catalogue has.
    Including the columns in the minimal dataset

        1. Stores the columns that are in the minimal dataset
    2. Stores all source catalogue column names together with the corresponding
    EUCAN-Connect Catalogue column names of the minimal dataset
    3. Stores a list with integer columns
    """

    PERSONS = "persons"
    EVENTS = "events"
    POPULATIONS = "populations"
    STUDIES = "studies"

    _mapping = {
        "studies": {
            "name": "study_name",
            "identification.name": "study_name",
            "identification.abbreviation": "acronym",
            "description": "objectives",
            "description.aim": "objectives",
            "startYear": "start_year",
        },
        "populations": {"selectionCriteria.countriesIso": "countries"},
    }

    _eucan_columns = {
        "studies": {
            "id": "Y",
            "study_name": "Y",
            "acronym": "Y",
            "objectives": "Y",
            "start_year": "Y",
            "countries": "Y",
            "source_data": "Y",
        },
    }

    _int_columns = {
        "studies": ["start_year"],
    }

    @classmethod
    def get_import_order(cls) -> List["TableType"]:
        return [
            type_
            for type_ in cls
            if type_ in [cls.PERSONS, cls.EVENTS, cls.POPULATIONS, cls.STUDIES]
        ]

    @property
    def table(self) -> str:
        return f"{self.value}"

    @property
    def base_id(self) -> str:
        return f"eucan_{self.value}"

    @property
    def columns(self):
        return self._eucan_columns.value[self.value]

    @property
    def mapping(self):
        return self._mapping.value[self.value]

    @property
    def int_columns(self):
        return self._int_columns.value[self.value]

    @property
    def minimal_dataset(self):
        columns = []
        for column in self._eucan_columns.value[self.value].keys():
            if self._eucan_columns.value[self.value][column] == "Y":
                columns.append(column)

        return columns

    @property
    def df_column_prefix(self) -> dict:
        return self.value + "_"

    def to_eucan_columns(self, df: pd.DataFrame):
        """
        Only select the columns that are in the EUCAN-Connect tables and add a prefix.
        """
        df.rename(columns=self.mapping, inplace=True)
        eucan_columns = list(set(self.columns).intersection(df.columns))
        df = df[eucan_columns].add_prefix(self.df_column_prefix)

        return df
