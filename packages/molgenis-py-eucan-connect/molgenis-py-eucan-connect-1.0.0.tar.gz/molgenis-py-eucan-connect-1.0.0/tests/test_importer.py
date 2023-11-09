from unittest import mock
from unittest.mock import MagicMock

import pytest

from molgenis.client import MolgenisRequestError
from molgenis.eucan_connect.errors import ErrorReport, EucanError, EucanWarning
from molgenis.eucan_connect.importer import ImportingState
from molgenis.eucan_connect.model import (
    Catalogue,
    CatalogueData,
    MixedData,
    Source,
    Table,
)
from molgenis.eucan_connect.table_info import TableType


def test_import_data(importer, session):
    importer._upsert_data = MagicMock(side_effect=importer._upsert_data)
    importer._delete_rows = MagicMock(side_effect=importer._delete_rows)
    state = _setup_state()

    importer.import_data(state)

    importer._upsert_data.assert_called_once()
    session.upload_data.assert_called_with(state.data_to_import)

    assert importer._delete_rows.mock_calls == [
        mock.call(state.data_to_import.studies, state.existing_data.studies, state),
        mock.call(
            state.data_to_import.populations, state.existing_data.populations, state
        ),
        mock.call(state.data_to_import.events, state.existing_data.events, state),
        mock.call(state.data_to_import.persons, state.existing_data.persons, state),
    ]


def test_upsert_fails(importer, session):
    session.upload_data.side_effect = MolgenisRequestError("")
    state = _setup_state()
    with pytest.raises(EucanError) as e:
        importer.import_data(state)

    assert str(e.value) == "Error importing data in the EUCAN-Connect Catalogue"


def test_delete_rows_fails(importer, mica_catalogue_data, session):
    session.delete_list.side_effect = MolgenisRequestError("")
    with pytest.raises(EucanError) as e:
        importer._delete_data(_setup_state())

    assert str(e.value) == "Error deleting row(s) from eucan_studies"


def test_delete_rows(eucan, importer, mica_catalogue_data: CatalogueData, session):
    existing_studies_table = Table.of(
        table_type=TableType.STUDIES,
        meta=MagicMock(),
        rows=[
            {
                "id": "mica:studyID:noC",
                "name": "Mica Study no Country",
                "source_catalogue": "Mica",
            },
            {"id": "delete_this_row", "source_catalogue": "Mica"},
            {"id": "undeletable_id", "source_catalogue": "Mica"},
        ],
    )

    state: ImportingState = MagicMock()
    state.linkage_info = ["undeletable_id"]

    state.report = ErrorReport([mica_catalogue_data.catalogue])

    warning1 = EucanWarning("ID delete_this_row is deleted")

    warning2 = EucanWarning("Prevented the deletion of a linked study: undeletable_id")

    importer._delete_rows(mica_catalogue_data.studies, existing_studies_table, state)

    assert eucan.printer.print.mock_calls[0] == mock.call(
        "Deleting 1 row(s) from eucan_studies"
    )
    session.delete_list.assert_called_with("eucan_studies", ["delete_this_row"])

    assert state.report.catalogue_warnings[Catalogue.of("Mica")] == [warning1, warning2]


def _setup_state():
    state = ImportingState(
        catalogues=[Catalogue.of("BC"), Catalogue.of("MS")],
        existing_data=MixedData(
            source=Source.TRANSFORMED,
            persons=Table.of_empty(TableType.PERSONS, MagicMock()),
            events=Table.of_empty(TableType.EVENTS, MagicMock()),
            populations=Table.of_empty(TableType.POPULATIONS, MagicMock()),
            studies=Table.of(
                table_type=TableType.STUDIES,
                meta=MagicMock(),
                rows=[
                    {
                        "id": "mica:studyID:noC",
                        "name": "Mica Study no Country",
                        "source_catalogue": "Mica",
                    },
                    {"id": "delete_this_row", "source_catalogue": "Mica"},
                    {"id": "undeletable_id", "source_catalogue": "Mica"},
                ],
            ),
        ),
        country_info=MagicMock(),
        linkage_info=MagicMock(),
        report=MagicMock(),
    )
    return state
