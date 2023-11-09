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
            if type(study) != dict:  # for some reason the last rows contain plain text
                continue

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
        df["source_data"] = (
            "https://"
            + self.catalogue.catalogue_url
            + "/birthcohorts/birthcohort/?id="
            + df["identification.id_user"]
        )
        df["id"] = (
            self.catalogue.get_id_prefix(table_type) + df["identification.id_user"]
        )
        # Convert values to the right format
        try:
            df["start_year"] = df["description.enrollment.period.start"].apply(
                lambda x: x[0:4]
            )
        except KeyError:
            pass

        try:
            df["countries"] = df["identification.country"].apply(
                lambda x: self._rename_countries(x) if x == x else x
            )
        except KeyError:
            df["countries"] = [[] for _ in range(len(df))]

        return df

    @staticmethod
    def _rename_countries(countries):
        country_list = []
        right_names = {
            "Czech Republic": "Czechia",
            "Russia": "Russian Federation",
            "United States": "United States of America",
            "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
        }
        for country in countries.split(","):
            country = country.split("(")[0].strip()
            try:
                country_list.append(right_names[country])
            except KeyError:
                country_list.append(country)

        return country_list
