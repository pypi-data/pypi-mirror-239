import json
from typing import List

import pandas as pd

from molgenis.eucan_connect.errors import EucanError
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
            df_study["countries"] = ""
            try:
                df_populations = self._eucan_populations(df_study)

                # Add countries to df_study
                countries = df_populations["selectionCriteria.countriesIso"].tolist()
                countries = [
                    country for country_list in countries for country in country_list
                ]
                if len(countries) == 0:
                    countries = [df_populations["selectionCriteria.territory.en"][0]]

                df_study.at[0, "countries"] = list(set(countries))
            except (KeyError, TypeError):
                pass

            df_eucan_studies = pd.concat(
                [df_eucan_studies, df_study], ignore_index=True
            )

        # Rename, and select columns and add prefix
        df_eucan_studies = TableType.STUDIES.to_eucan_columns(df_eucan_studies)

        return pd.concat([df_eucan_data, df_eucan_studies])

    def _eucan_studies(self, json_data) -> pd.DataFrame:
        # Convert the json list to a pandas dataframe
        table_type = TableType.STUDIES
        df = pd.json_normalize(json_data)
        study_content = pd.json_normalize(df["content"].apply(json.loads))
        df = pd.concat([df, study_content], axis=1)

        # Add id and source_data
        df["source_data"] = self.catalogue.catalogue_url + "/study/" + df["id"]
        df["id"] = self.catalogue.get_id_prefix(table_type) + df["id"]

        # Convert values to the right format
        # Set the English descriptions for names, acronym, and objectives

        for column in {"name", "acronym", "objectives"}.intersection(df.columns):
            df[column] = df[column].apply(
                lambda x: next(y for y in x if y["lang"] == "en")["value"]
                if x == x
                else x
            )

        return df

    @staticmethod
    def _eucan_populations(df_study) -> pd.DataFrame:
        if len(df_study["populations"]) != 1:
            raise EucanError(
                f"Length of populations "
                f"{len(df_study['populations'])} greater than 1"
            )
        df = pd.json_normalize(df_study["populations"][0])
        try:
            population_content = pd.json_normalize(df["content"].apply(json.loads))
            df = pd.concat([df.drop(["content"], axis=1), population_content], axis=1)
        except KeyError:
            df["selectionCriteria.countriesIso"] = [[] for _ in range(len(df))]

        return df
