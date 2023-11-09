import re

import pandas as pd
from unidecode import unidecode

from molgenis.eucan_connect.errors import EucanWarning
from molgenis.eucan_connect.importer import ImportingState
from molgenis.eucan_connect.printer import Printer


class Transformer:
    """
    The published tables have a few extra attributes that the staging tables don't have.
    This class is responsible for adding those attributes so the staging tables can be
    published correctly.
    """

    def __init__(
        self, printer: Printer, source_data: pd.DataFrame, state: ImportingState
    ):
        self.printer = printer
        self.source_data = source_data
        self.state = state

        self.warnings = []

    def transform(self):
        """
        Transforms the data of a catalogue:
        1. Replaces, if necessary, the country codes in the country columns
        by the right IDs
        2. Removes html tags from descriptions etc
        3. Adds the label column (study name without accents on the first letter)
        """

        self._set_country_codes()
        self._remove_html_tags()
        self._add_name_label()

        return self.warnings

    def _set_country_codes(self):
        """
        Replaces if necessary the country codes in the country columns by the right IDs
        """
        for column in ["studies_countries"]:
            self.printer.print("Set Country Codes")
            self.source_data[column] = self.source_data[column].apply(
                lambda x: self._get_country_code(x) if len(x) > 0 else x
            )

    def _get_country_code(self, countries):
        country_ids = []
        for country in countries:
            country_id = self.state.country_info.get_country_id(country)
            if not country_id:
                warning = EucanWarning(f"Country {country} not found in CountryInfo")
                self.printer.print_warning(warning)
                self.warnings.append(warning)
            else:
                country_ids.append(country_id)

        return country_ids

    def _remove_html_tags(self):
        """
        Removes if necessary any html tags from a text string
        """
        for column in ["studies_objectives"]:
            self.printer.print("Remove HTML tags")
            self.source_data[column] = self.source_data[column].apply(
                lambda x: re.sub("<[^<]+?>", "", x) if x == x else x
            )

    def _add_name_label(self):
        """
        Add label column (study name without accents on the first letter)
        """
        self.printer.print("Add label column")
        self.source_data["studies_label"] = self.source_data[
            "studies_study_name"
        ].apply(lambda x: unidecode(x[0]) + x[1:])
