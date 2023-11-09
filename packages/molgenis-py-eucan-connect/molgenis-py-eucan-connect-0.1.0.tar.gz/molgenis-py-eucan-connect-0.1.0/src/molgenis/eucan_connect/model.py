import typing
from abc import ABC
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

from molgenis.eucan_connect.table_info import TableType
from molgenis.eucan_connect.utils import to_ordered_dict


@dataclass(frozen=True)
class TableMeta:
    """Convenient wrapper for the output of the metadata API."""

    meta: dict
    id_attribute: str = field(init=False)

    def __post_init__(self):
        for attribute in self.meta["attributes"]["items"]:
            if attribute["data"]["idAttribute"] is True:
                object.__setattr__(self, "id_attribute", attribute["data"]["name"])

    @property
    def id(self):
        return self.meta["id"]


@dataclass(frozen=True)
class BaseTable(ABC):
    """
    Simple representation of a MOLGENIS table. The rows should be in the uploadable
    format.
    """

    rows_by_id: "typing.OrderedDict[str, dict]"
    meta: TableMeta

    @property
    def rows(self) -> List[dict]:
        return list(self.rows_by_id.values())

    @property
    def full_name(self) -> str:
        return self.meta.id


@dataclass(frozen=True)
class Table(BaseTable):
    """
    Simple representation of a EUCAN-Connect Catalogue table.
    """

    type: TableType

    @staticmethod
    def of(table_type: TableType, meta: TableMeta, rows: List[dict]) -> "Table":
        """Factory method that takes a list of rows instead of an OrderedDict of
        ids/rows."""
        return Table(rows_by_id=to_ordered_dict(rows), meta=meta, type=table_type)

    @staticmethod
    def of_empty(table_type: TableType, meta: TableMeta):
        return Table(rows_by_id=OrderedDict(), meta=meta, type=table_type)


@dataclass(frozen=True)
class Catalogue:
    """Represents a single source catalogue in the EUCAN-Connect catalogue."""

    code: str
    catalogue_type: str
    catalogue_url: str
    description: str
    catalogue_query: str | None = None
    networks: str | None = None

    _classifiers = {
        TableType.PERSONS: "contactID",
        TableType.EVENTS: "eventID",
        TableType.POPULATIONS: "populationID",
        TableType.STUDIES: "studyID",
    }

    def get_id_prefix(self, table_type: TableType) -> str:
        """
        Each table has a specific prefix for the identifiers of its rows. This prefix is
        based on the source catalogue's description and the classifier of the table.

        :param TableType table_type: the table to get the id prefix for
        :return: the id prefix
        """
        classifier = self._classifiers[table_type]
        source = self.description.lower().replace(" ", "-")
        return f"{source}:{classifier}:"

    @staticmethod
    def of(code: str):
        return Catalogue(code, "url", "type", "description")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Catalogue):
            return self.code == other.code
        return False

    def __hash__(self):
        return hash(self.code)


class Source(Enum):
    SOURCE_CATALOGUE = "source_catalogue"
    EUCAN = "eucan_catalogue"
    TRANSFORMED = "transformed"


@dataclass
class EucanData(ABC):
    """Abstract base class for containers storing rows from the four EUCAN tables:
    persons, events, populations, studies."""

    source: Source
    persons: Table
    events: Table
    populations: Table
    studies: Table
    table_by_type: Dict[TableType, Table] = field(init=False)

    def __post_init__(self):
        self.table_by_type = {
            TableType.PERSONS: self.persons,
            TableType.EVENTS: self.events,
            TableType.POPULATIONS: self.populations,
            TableType.STUDIES: self.studies,
        }

    @property
    def import_order(self) -> List[Table]:
        return [self.persons, self.events, self.populations, self.studies]


@dataclass()
class CatalogueData(EucanData):
    """Container object storing the four tables of a single catalogue."""

    catalogue: Catalogue

    @staticmethod
    def from_dict(
        catalogue: Catalogue, source: Source, tables: Dict[str, Table]
    ) -> "CatalogueData":
        return CatalogueData(catalogue=catalogue, source=source, **tables)


class MixedData(EucanData):
    """Container object storing the four tables with mixed origins, for example from
    the combined tables or from multiple source catalogues."""

    @staticmethod
    def from_mixed_dict(source: Source, tables: Dict[str, Table]) -> "MixedData":
        return MixedData(source=source, **tables)

    def merge(self, other_data: EucanData):
        self.persons.rows_by_id.update(other_data.persons.rows_by_id)
        self.events.rows_by_id.update(other_data.events.rows_by_id)
        self.populations.rows_by_id.update(other_data.populations.rows_by_id)
        self.studies.rows_by_id.update(other_data.studies.rows_by_id)

    def remove_catalogue_rows(self, catalogue: Catalogue):
        for table in self.import_order:
            ids_to_remove = [
                row["id"]
                for row in table.rows
                if row["source_catalogue"] == catalogue.code
            ]
            all(table.rows_by_id.pop(id_) for id_ in ids_to_remove)

    def copy_empty(self) -> "MixedData":
        return MixedData(
            source=self.source,
            persons=Table.of_empty(TableType.PERSONS, self.persons.meta),
            events=Table.of_empty(TableType.EVENTS, self.events.meta),
            populations=Table.of_empty(TableType.POPULATIONS, self.populations.meta),
            studies=Table.of_empty(TableType.STUDIES, self.studies.meta),
        )


@dataclass(frozen=True)
class CountryInfo:
    """
    Stores all available ISO (two and three letter) country codes
    and the country names available in the EUCAN-Connect Catalogue
    """

    countries: List[dict]
    """List with a dictionary per country"""

    def get_country_id(self, country_description: str) -> str:
        iso_country = None
        for iso_type in self.countries[0].keys():
            iso_country = next(
                (
                    country
                    for country in self.countries
                    if country[iso_type].split("(")[0].strip() == country_description
                ),
                False,
            )
            if iso_country:
                break
        if iso_country:
            return iso_country["iso2_code"]
        else:
            return ""
