from typing import List
from unittest.mock import MagicMock, patch

import pytest

from molgenis.eucan_connect.data_assembler import DataAssembler
from molgenis.eucan_connect.errors import ErrorReport, EucanWarning
from molgenis.eucan_connect.importer import ImportingState
from molgenis.eucan_connect.model import Catalogue, CountryInfo


@pytest.fixture
def state_init():
    with patch("molgenis.eucan_connect.data_assembler.ImportingState") as state_init:
        yield state_init


@pytest.fixture
def transformer_init():
    with patch("molgenis.eucan_connect.data_assembler.Transformer") as transformer_init:
        yield transformer_init


@pytest.fixture
def validator_init():
    with patch("molgenis.eucan_connect.data_assembler.Validator") as validator_init:
        yield validator_init


@pytest.fixture
def birthcohorts_assembler_init():
    with patch(
        "molgenis.eucan_connect.data_assembler.BirthCohorts"
    ) as birthcohorts_assembler_mock:
        yield birthcohorts_assembler_mock


@pytest.fixture
def datacatalogue_assembler_init():
    with patch(
        "molgenis.eucan_connect.data_assembler.DataCatalogue"
    ) as datacatalogue_assembler_mock:
        yield datacatalogue_assembler_mock


@pytest.fixture
def mica_assembler_init():
    with patch("molgenis.eucan_connect.data_assembler.Mica") as mica_assembler_mock:
        yield mica_assembler_mock


def test_assemble(
    eucan,
    mica_assembler_init,
    birthcohorts_assembler_init,
    datacatalogue_assembler_init,
    state_init,
    mica_transformed,
    transformer_init,
    validator_init,
):
    catalogue = Catalogue("MS", "Mica", "mica_url", "Mica")
    assembler = DataAssembler(eucan.printer, eucan.session, catalogue, state_init)
    assembler.transform_data = transformer_init
    assembler.validate_data = validator_init

    mica_assembler_init.return_value = MagicMock()
    mica_assembler_init.return_value.assemble.side_effect = [mica_transformed]
    state = state_init
    report = MagicMock()
    state.report = report

    assembler.assemble()

    assert mica_assembler_init.called
    assert not birthcohorts_assembler_init.called
    assert not datacatalogue_assembler_init.called

    eucan.session.create_catalogue_data.assert_called_with(catalogue, mica_transformed)

    assembler.transform_data.assert_called_once()
    assembler.validate_data.assert_called_once()


def test_validate_warnings(eucan, validator_init, printer):
    validator = MagicMock()
    validator_init.return_value = validator
    warning = EucanWarning("warning")
    validator.validate.return_value = [warning]
    catalogue = Catalogue("MS", "Mica", "mica_url", "Mica")
    assembler = DataAssembler(eucan.printer, eucan.session, catalogue, state_init)
    catalogue_data = MagicMock()
    ms = Catalogue.of("MS")
    catalogue_data.catalogue = ms
    state_init.report = ErrorReport(ms)

    assembler._validate_data(catalogue_data)

    assert state_init.report.catalogue_warnings[ms] == [warning]


# noinspection PyProtectedMember
def _setup_state(catalogues: List[Catalogue], eucan):
    country_info = CountryInfo(
        countries=[
            {
                "iso2_code": "NL",
                "iso3_code": "NLD",
                "country_name": "Netherlands",
                "country_code": "528",
            },
            {
                "iso2_code": "DE",
                "iso3_code": "DEU",
                "country_name": "Germany",
                "country_code": "276",
            },
            {
                "iso2_code": "FI",
                "iso3_code": "FIN",
                "country_name": "Finland",
                "country_code": "246",
            },
        ]
    )

    report = ErrorReport(catalogues)

    state = ImportingState(
        existing_data=MagicMock(),
        country_info=country_info,
        linkage_info=MagicMock(),
        catalogues=catalogues,
        report=report,
    )
    eucan._init_state = MagicMock()
    eucan._init_state.return_value = state
    return state
