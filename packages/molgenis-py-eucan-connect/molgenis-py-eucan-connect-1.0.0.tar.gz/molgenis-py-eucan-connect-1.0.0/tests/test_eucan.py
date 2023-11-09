from typing import List
from unittest.mock import MagicMock, call, patch

import pytest

from molgenis.eucan_connect.errors import ErrorReport, EucanError
from molgenis.eucan_connect.eucan import Eucan
from molgenis.eucan_connect.importer import ImportingState
from molgenis.eucan_connect.model import Catalogue


@pytest.fixture
def eucan(session, printer) -> Eucan:
    eucan = Eucan(session)
    eucan.printer = printer
    eucan.importer = MagicMock()
    return eucan


@pytest.fixture
def report_init():
    with patch("molgenis.eucan_connect.eucan.ErrorReport") as report_mock:
        yield report_mock


@pytest.fixture()
def assembler_init():
    with patch("molgenis.eucan_connect.eucan.DataAssembler") as assembler_mock:
        yield assembler_mock


def test_import_catalogue_assemble_fails(eucan, report_init):
    ms = Catalogue("Nw", "new_type", "url", "New Catalogue")
    state = _setup_state([ms], eucan, report_init)
    eucan._assemble_catalogue_data = MagicMock(
        side_effect=eucan._assemble_catalogue_data
    )
    eucan._import_catalogue_data = MagicMock()

    error = str(EucanError("Unknown catalogue type new_type"))

    state.report = eucan.import_catalogues([ms])

    eucan.printer.print_catalogue_title.assert_called_once_with(ms)
    assert eucan._assemble_catalogue_data.called_with([ms], state)

    assert eucan.printer.print_error.called_once()

    assert str(state.report.catalogue_errors[ms]) == error
    eucan.printer.print_summary.assert_called_once_with(state.report)


def test_import_catalogues(eucan, assembler_init, report_init):
    bc = Catalogue("BC", "fails during importing", "url", "BirthCohorts")
    ms = Catalogue("MS", "succeeds", "url", "Mica")
    state = _setup_state([bc, ms], eucan, report_init)
    assembler = MagicMock()
    assembler_init.return_value = assembler
    error = EucanError("error")
    eucan.importer.import_data.side_effect = error

    error = EucanError("error")

    report = eucan.import_catalogues([bc, ms])

    assert eucan._init_state.called_once()

    assert eucan.printer.print_catalogue_title.mock_calls == [call(bc), call(ms)]
    assert assembler.assemble.call_count == 2

    eucan.importer.import_data.assert_called_with(state)
    assert len(report.catalogue_errors) == 0
    assert str(report.error) == str(error)
    assert len(report.catalogue_warnings[bc]) == 0
    eucan.printer.print_summary.assert_called_once_with(report)


def test_init_state(eucan):
    bc = Catalogue("BC", "BirthCohorts", "url", "BirthCohorts")
    ms = Catalogue("MS", "Maelstrom", "url", "Mica")
    catalogues = [bc, ms]
    report = ErrorReport(catalogues)
    eucan._init_state(catalogues, report)

    eucan.session.get_eucan_data.assert_called_once()
    eucan.session.get_country_info.assert_called_once()
    eucan.session.get_linked_studies.assert_called_once()


def test_init_state_fails(eucan):
    bc = Catalogue("BC", "fails during importing", "url", "BirthCohorts")
    ms = Catalogue("MS", "succeeds", "url", "Mica")
    error = EucanError("Init state fails")
    eucan._init_state = MagicMock()
    eucan._init_state.side_effect = error
    eucan._assemble_catalogue_data = MagicMock(
        side_effect=eucan._assemble_catalogue_data
    )
    eucan._import_catalogue_data = MagicMock()

    report = eucan.import_catalogues([bc, ms])
    assert eucan._init_state.called
    assert not eucan._assemble_catalogue_data.called
    assert not eucan._import_catalogue_data.called

    assert report.error == error


# noinspection PyProtectedMember
def _setup_state(catalogues: List[Catalogue], eucan: Eucan, report_init):
    report = ErrorReport(catalogues)
    report_init.return_value = report

    state = ImportingState(
        existing_data=MagicMock(),
        country_info=MagicMock(),
        linkage_info=MagicMock(),
        catalogues=catalogues,
        report=report,
    )
    eucan._init_state = MagicMock()
    eucan._init_state.return_value = state
    return state
