from typing import List
from unittest import mock
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from molgenis.eucan_connect.errors import ErrorReport, EucanWarning
from molgenis.eucan_connect.importer import ImportingState
from molgenis.eucan_connect.model import Catalogue, CountryInfo
from molgenis.eucan_connect.transformer import Transformer


@pytest.fixture
def transformer():
    return Transformer(
        printer=MagicMock(),
        source_data=MagicMock(),
        state=MagicMock(),
    )


def test_country_codes(eucan, mica_transformed, transformer):
    catalogue = Catalogue("MS", "Mica", "mica_url", "Mica")
    transformer.printer = eucan.printer
    transformer.source_data = mica_transformed
    transformer.state = _setup_state([catalogue], eucan)

    transformer._set_country_codes()

    countries = pd.DataFrame({"studies_countries": [["FI"], ["NL"], []]})

    assert eucan.printer.print.mock_calls[0] == mock.call("Set Country Codes")

    pd.testing.assert_series_equal(
        mica_transformed["studies_countries"], countries["studies_countries"]
    )

    assert transformer.warnings == [
        EucanWarning("Country GER not found in CountryInfo")
    ]


def test_html_tags(eucan, mica_transformed, transformer):
    catalogue = Catalogue("MS", "Mica", "mica_url", "Mica")
    transformer.printer = eucan.printer
    transformer.source_data = mica_transformed
    transformer.state = _setup_state([catalogue], eucan)

    transformer._remove_html_tags()

    objectives = pd.DataFrame(
        {
            "studies_objectives": [
                "The first Mica Study",
                np.nan,
                "Mica Study without country.",
            ]
        }
    )

    assert eucan.printer.print.mock_calls[0] == mock.call("Remove HTML tags")

    pd.testing.assert_series_equal(
        mica_transformed["studies_objectives"], objectives["studies_objectives"]
    )


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
