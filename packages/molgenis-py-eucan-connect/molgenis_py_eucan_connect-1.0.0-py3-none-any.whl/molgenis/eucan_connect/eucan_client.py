from dataclasses import asdict, dataclass
from enum import Enum
from typing import List

import numpy as np
import pandas as pd

from molgenis.client import Session
from molgenis.eucan_connect import utils
from molgenis.eucan_connect.model import (
    Catalogue,
    CatalogueData,
    CountryInfo,
    EucanData,
    MixedData,
    Source,
    Table,
    TableMeta,
)
from molgenis.eucan_connect.table_info import TableType


@dataclass
class AttributesRequest:
    persons: List[str]
    events: List[str]
    populations: List[str]
    studies: List[str]


class ImportDataAction(Enum):
    """Enum of MOLGENIS import actions"""

    ADD = "add"
    ADD_UPDATE_EXISTING = "add_update_existing"
    UPDATE = "update"
    ADD_IGNORE_EXISTING = "add_ignore_existing"


class ImportMetadataAction(Enum):
    """Enum of MOLGENIS import metadata actions"""

    ADD = "add"
    UPDATE = "update"
    UPSERT = "upsert"
    IGNORE = "ignore"


class EucanSession(Session):
    """
    A session with a EUCAN-Connect Catalogue. Contains methods to get source catalogues,
    their data and EUCAN-Connect data.
    """

    def __init__(self, *args, **kwargs):
        super(EucanSession, self).__init__(*args, **kwargs)

    CATALOGUES_TABLE = "eucan_source_catalogues"

    def get_catalogues(self, codes: List[str] = None) -> List[Catalogue]:
        """
        Retrieves a list of Source catalogues objects from the source catalogues table.
        Returns all source catalogues or some source catalogues if 'codes' is specified.
        :param codes: source catalogues to get by code
        :return: list of Catalogue objects
        """
        if codes:
            catalogues = self.get(self.CATALOGUES_TABLE, q=f"id=in=({','.join(codes)})")
        else:
            catalogues = self.get(self.CATALOGUES_TABLE)

        if codes:
            self._validate_codes(codes, catalogues)
        return self._to_catalogues(catalogues)

    def get_country_info(self) -> CountryInfo:
        """
        Retrieves all ISO two and three letter country codes and the country names
        stored in the EUCAN-Connect Catalogue
        :return: an IsoCountryData object
        """
        eucan_countries = self.get(
            "eucan_countries",
            batch_size=10000,
            attributes="iso2_code,iso3_code,country_name,country_code",
            uploadable=True,
        )

        return CountryInfo(countries=eucan_countries)

    def get_linked_studies(self) -> List:
        """
        Retrieves a list with study IDs from the study_linkage table
        :return: a List
        """
        eucan_linkage = self.get(
            "eucan_linkage", batch_size=10000, attributes="studies", uploadable=True
        )
        linked_studies = []
        for row in eucan_linkage:
            linked_studies.extend(row["studies"])

        return linked_studies

    def create_catalogue_data(
        self, catalogue: Catalogue, df_in: pd.DataFrame
    ) -> CatalogueData:
        """
        Converts processed source catalogue data to the EUCAN-Catalogue format
        Fills the four EUCAN-Connect tables for the specific source catalogue

        :param catalogue: the source catalogue
        :param df_in: the source catalogue data in pandas DataFrame
        :return: a CatalogueData object
        """

        tables = dict()
        for table_type in TableType.get_import_order():
            id_ = table_type.base_id
            meta = TableMeta(meta=self.get_meta(id_))

            tables[table_type.value] = Table.of(
                table_type=table_type,
                meta=meta,
                rows=self._get_uploadable_data(catalogue, df_in, table_type),
            )

        return CatalogueData.from_dict(
            catalogue=catalogue, source=Source.SOURCE_CATALOGUE, tables=tables
        )

    @staticmethod
    def _get_uploadable_data(
        catalogue: Catalogue, df_data: pd.DataFrame, table_type: TableType
    ) -> List[dict]:
        """
        Returns all the rows of an entity type in the dataFrame, transformed to
        the uploadable format.
        """
        table_columns = [x for x in df_data.columns if table_type.table in x[:10]]
        table_data = df_data[table_columns].to_dict("records")
        # Remove the "table" name from the columns and remove missing values
        for row in table_data:
            for tab_column in table_columns:
                column = tab_column.replace(table_type.table + "_", "", 1)
                row[column] = row[tab_column]
                del row[tab_column]

                if type(row[column]) is np.ndarray:
                    row[column] = list(row[column])

                if utils.isnan(row[column]):
                    del row[column]

                # Convert floats to int
                if column in table_type.int_columns and column in row:
                    row[column] = int(row[column])

                # Replace invalid characters in the id
                if column == "id":
                    row[column] = row[column].replace(".", "-")

        # Remove duplicate records
        unique_data = [
            i for n, i in enumerate(table_data) if i not in table_data[n + 1 :]
        ]

        # Remove empty records
        while {} in unique_data:
            unique_data.remove({})

        # Add the source catalogue
        unique_data = [
            dict(item, source_catalogue=catalogue.code) for item in unique_data
        ]

        return unique_data

    @staticmethod
    def _to_catalogues(catalogues: List[dict]):
        """Maps rows to the Catalogue object."""
        result = list()
        for catalogue in catalogues:
            result.append(
                Catalogue(
                    code=catalogue["id"],
                    description=catalogue.get("description"),
                    catalogue_url=catalogue["catalogue_url"],
                    catalogue_type=catalogue["catalogue_type"]["id"],
                    catalogue_query=catalogue.get("catalogue_query"),
                    networks=catalogue.get("networks"),
                )
            )
        return result

    @staticmethod
    def _validate_codes(codes: List[str], catalogues: List[dict]):
        """Raises a KeyError if a requested source catalogue code was not found."""
        retrieved_codes = {catalogue["id"] for catalogue in catalogues}
        for code in codes:
            if code not in retrieved_codes:
                raise KeyError(f"Unknown code: {code}")

    def get_eucan_data(
        self, catalogues: List[Catalogue], attributes: AttributesRequest
    ) -> MixedData:
        """
        Gets the four tables that belong to one or more catalogues from the
        EUCAN-Connect Catalogue.
        Filters the rows based on the source catalogue field.

        :param List[Catalogue] catalogues: the catalogue(s) to get the
        EUCAN-Connect Catalogue data for
        :param AttributesRequest attributes: the attributes to get for each table
        :return: an EucanData object
        """

        if len(catalogues) == 0:
            raise ValueError("No catalogues provided")

        attributes = asdict(attributes)
        codes = [catalogue.code for catalogue in catalogues]
        tables = dict()
        for table_type in TableType.get_import_order():
            id_ = table_type.base_id
            meta = TableMeta(self.get_meta(id_))
            attrs = attributes[table_type.value]

            tables[table_type.value] = Table.of(
                table_type=table_type,
                meta=meta,
                rows=self.get(
                    id_,
                    batch_size=10000,
                    q=f"source_catalogue=in=({','.join(codes)})",
                    attributes=",".join(attrs),
                    uploadable=True,
                ),
            )

        return MixedData.from_mixed_dict(source=Source.EUCAN, tables=tables)

    def upload_data(self, data: EucanData):
        """
        Converts the four tables of an EucanData object to CSV, bundles them in
        a ZIP archive and imports them through the import API.
        :param data: an EucanData object
        """

        importable_data = dict()
        for table in data.import_order:
            importable_data[table.full_name] = table.rows

        self.import_data(
            importable_data,
            data_action=ImportDataAction.ADD_UPDATE_EXISTING,
            metadata_action=ImportMetadataAction.IGNORE,
        )
