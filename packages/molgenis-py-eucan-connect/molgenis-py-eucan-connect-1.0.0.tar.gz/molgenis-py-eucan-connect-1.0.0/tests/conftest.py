"""
    conftest.py

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
import json
from importlib import resources
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from molgenis.eucan_connect.eucan import Eucan
from molgenis.eucan_connect.eucan_client import EucanSession
from molgenis.eucan_connect.importer import Importer
from molgenis.eucan_connect.model import (
    Catalogue,
    CatalogueData,
    Source,
    Table,
    TableMeta,
)
from molgenis.eucan_connect.table_info import TableType


@pytest.fixture
def session() -> MagicMock:
    session = MagicMock()
    session.url = "url"

    def entity_type(table_name):
        return meta_data(table_name)

    session.get_meta = MagicMock(side_effect=entity_type)

    def existing_data(table_name, q: str = None):
        if table_name == "eucan_persons":
            return [
                {"id": "person_id", "source_catalogue": {"id": "Test"}},
                {"id": "person_deleted_id", "source_catalogue": {"id": "Test"}},
            ]
        if table_name == "eucan_source_catalogues" and q == "id=in=(TC)":
            return [
                {
                    "_href": "/api/v2/eucan_source_catalogues/TC",
                    "id": "TC",
                    "description": "Test Catalogue",
                    "catalogue_url": "https://test.nl",
                    "catalogue_type": {"id": "Test"},
                }
            ]
        else:
            return [
                {
                    "_href": "/api/v2/eucan_source_catalogues/TC",
                    "id": "TC",
                    "description": "Test Catalogue",
                    "catalogue_url": "https://test.nl",
                    "catalogue_type": {"id": "BirthCohorts"},
                },
                {
                    "_href": "/api/v2/eucan_source_catalogues/C2",
                    "id": "C2",
                    "description": "Test Catalogue2",
                    "catalogue_url": "https://test2.nl",
                    "catalogue_type": {"id": "Mica"},
                },
                {
                    "_href": "/api/v2/eucan_source_catalogues/C3",
                    "id": "C3",
                    "description": "Test Catalogue3",
                    "catalogue_url": "https://test3.nl",
                    "catalogue_type": {"id": "DNA_catalogue"},
                },
            ]

    session.get = MagicMock(side_effect=existing_data)

    return session


@pytest.fixture
def printer() -> MagicMock:
    return MagicMock()


@pytest.fixture
def importer(session, printer) -> Importer:
    return Importer(session, printer)


@pytest.fixture
def eucan(session, printer) -> Eucan:
    eucan = Eucan(session)
    eucan.printer = printer
    eucan.importer = importer
    return eucan


@pytest.fixture
def birthcohorts_data():
    """
    Reads the data (json-format) from birthcohorts.json to test with.
    """
    file = open(str(resources.files("tests.resources") / "birthcohorts.json"), "r")
    birthcohorts_data = json.load(file)
    file.close()
    return birthcohorts_data


@pytest.fixture
def birthcohorts_transformed():
    """
    Reads the data (csv) from birthcohorts_transformed.csv to test with.
    """
    file = str(resources.files("tests.resources") / "birthcohorts_transformed.csv")
    data = pd.read_csv(file, sep=";")

    data["studies_countries"] = data["studies_countries"].apply(
        lambda x: x[1:-1].split(",") if x == x else []
    )

    str_columns = ["studies_start_year"]
    for column in str_columns:
        data[column] = (
            data[column].fillna(-1).astype(int).astype(str).replace("-1", np.nan)
        )

    return data


@pytest.fixture
def birthcohorts_catalogue_data(session, birthcohorts_transformed):
    eucan_session = EucanSession("url")
    eucan_session.get_meta = session.get_meta
    catalogue = Catalogue("BC", "BirthCohorts", "birthcohort_url", "BirthCohorts")
    data = eucan_session.create_catalogue_data(catalogue, birthcohorts_transformed)

    return data


@pytest.fixture
def datacatalogue_data():
    """
    Reads the data (json-format) from datacatalogue.json to test with.
    """
    file = open(str(resources.files("tests.resources") / "datacatalogue.json"), "r")
    datacatalogue_data = json.load(file)
    file.close()
    return datacatalogue_data


@pytest.fixture
def datacatalogue_transformed():
    """
    Reads the data (csv) from datacatalogue_transformed.csv to test with.
    """
    file = str(resources.files("tests.resources") / "datacatalogue_transformed.csv")
    data = pd.read_csv(file, sep=";")

    data["studies_countries"] = data["studies_countries"].apply(
        lambda x: x[1:-1].split(",") if x == x else []
    )

    return data


@pytest.fixture
def datacatalogue_catalogue_data(session, datacatalogue_transformed):
    eucan_session = EucanSession("url")
    eucan_session.get_meta = session.get_meta
    catalogue = Catalogue("ECN", "EUChildNetwork", "ecn_url", "DataCatalogue")
    data = eucan_session.create_catalogue_data(catalogue, datacatalogue_transformed)

    return data


@pytest.fixture
def mica_data():
    """
    Reads the data (json-format) from mica.json to test with.
    """
    file = open(str(resources.files("tests.resources") / "mica.json"), "r")
    mica_data = json.load(file)
    file.close()
    return mica_data


@pytest.fixture
def mica_transformed():
    """
    Reads the data (csv) from mica_transformed.csv to test with.
    """
    file = str(resources.files("tests.resources") / "mica_transformed.csv")
    data = pd.read_csv(file, sep=";")

    data["studies_countries"] = data["studies_countries"].apply(
        lambda x: x[1:-1].split(",") if x == x else []
    )

    return data


@pytest.fixture
def mica_catalogue_data(session, mica_transformed):
    eucan_session = EucanSession("url")
    eucan_session.get_meta = session.get_meta
    catalogue = Catalogue("MS", "Mica", "mica_url", "Mica")
    data = eucan_session.create_catalogue_data(catalogue, mica_transformed)

    return data


@pytest.fixture
def fake_catalogue_data(eucan):
    catalogue = Catalogue("Test", "succeeds", "test_url", "CatalogueType")
    persons_meta = TableMeta(eucan.session.get_meta("eucan_persons"))
    persons = Table.of_empty(
        TableType.PERSONS,
        persons_meta,
    )

    events_meta = TableMeta(eucan.session.get_meta("eucan_events"))
    events = Table.of_empty(
        TableType.EVENTS,
        events_meta,
    )

    populations_meta = TableMeta(eucan.session.get_meta("eucan_populations"))
    populations = Table.of_empty(
        TableType.POPULATIONS,
        populations_meta,
    )

    study_meta = TableMeta(eucan.session.get_meta("eucan_studies"))
    studies = Table.of(
        TableType.STUDIES,
        study_meta,
        [
            {
                "id": "id",
                "study_name": "name",
                "acronym": "acronym",
                "objectives": "objectives",
                "start_year": 2021,
                "countries": ["NL", "AT"],
                "source_data": "source_url.com/id",
                "source_catalogue": "Test",
            },
        ],
    )

    return CatalogueData.from_dict(
        catalogue=catalogue,
        source=Source.SOURCE_CATALOGUE,
        tables={
            TableType.PERSONS.value: persons,
            TableType.EVENTS.value: events,
            TableType.POPULATIONS.value: populations,
            TableType.STUDIES.value: studies,
        },
    )


@pytest.fixture()
def fake_converted_source_data():
    df = pd.DataFrame(
        [
            {
                "studies_id": "id",
                "studies_study_name": "name",
                "studies_acronym": "acronym",
                "studies_objectives": "objectives",
                "studies_start_year": 2021,
                "studies_countries": ["NL", "AT"],
                "studies_source_data": "source_url.com/id",
            }
        ]
    )
    return df


def meta_data(table_name):
    meta = {
        "id": table_name,
        "label": "Test",
        "attributes": {
            "items": [
                {
                    "data": {
                        "id": "aaaac",
                        "label": "ID",
                        "name": "id",
                        "type": "string",
                        "idAttribute": True,
                    }
                }
            ]
        },
    }
    return meta
