from typing import List

import pandas as pd

from molgenis.eucan_connect.model import Catalogue
from molgenis.eucan_connect.printer import Printer
from molgenis.eucan_connect.table_info import TableType


class Transformer:
    """
    This class is responsible for converting the raw source data to data compatible with
    the EUCAN-Connect Catalogue data model
    """

    def __init__(self, printer: Printer, catalogue: Catalogue):
        self.catalogue = catalogue
        self.printer = printer

    def transform(self, source_data: List):
        self.printer.print(f"Transform {self.catalogue.description} source data")
        df_eucan_data = pd.DataFrame()
        df_eucan_studies = pd.DataFrame()

        for study in source_data:
            df_study = self._eucan_studies(study)

            df_eucan_studies = pd.concat([df_eucan_studies, df_study])

        # Rename, and select columns and add prefix
        df_eucan_studies = TableType.STUDIES.to_eucan_columns(df_eucan_studies)

        return pd.concat([df_eucan_data, df_eucan_studies], ignore_index=True)

    def _eucan_studies(self, json_data) -> pd.DataFrame:
        # Convert the json list to a pandas dataframe
        table_type = TableType.STUDIES
        df = pd.json_normalize(json_data)
        # Add id and source_data
        df["id"] = df["id"].str.replace(" ", "_", regex=False)
        source_url_part = (
            "/catalogue/catalogue/#/networks-catalogue/"
            + self.catalogue.networks
            + "/cohorts/"
        )
        df["source_data"] = self.catalogue.catalogue_url + source_url_part + df["id"]
        df["id"] = self.catalogue.get_id_prefix(table_type) + df["id"]

        # Convert values to the right format
        # Get a list with countries
        try:
            df["countries"] = df["countries"].apply(
                lambda x: [d["name"].split("(")[0].strip() for d in x] if x == x else x
            )
        except KeyError:
            df["countries"] = [[] for _ in range(len(df))]

        return df
