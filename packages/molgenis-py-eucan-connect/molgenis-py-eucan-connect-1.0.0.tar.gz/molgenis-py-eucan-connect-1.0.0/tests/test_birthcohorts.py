from unittest import mock
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from molgenis.eucan_connect.birthcohorts.birthcohorts_assembler import Assembler
from molgenis.eucan_connect.model import Catalogue


@pytest.fixture
def source_collector_init():
    with patch(
        "molgenis.eucan_connect.birthcohorts.birthcohorts_assembler." "SourceCollector"
    ) as source_collector_mock:
        yield source_collector_mock


def test_birthcohort_assembler(
    eucan, birthcohorts_data, birthcohorts_transformed, source_collector_init
):
    catalogue = Catalogue("BC", "BirthCohorts", "birthcohorts_url", "BirthCohorts")
    assembler = Assembler(eucan.printer)
    assembler._get_source_data = MagicMock(side_effect=assembler._get_source_data)
    assembler._transform_data = MagicMock(side_effect=assembler._transform_data)

    source_collector_init.return_value.get_birthcohorts_data.side_effect = [
        birthcohorts_data
    ]

    data = assembler.assemble(catalogue)
    assembler._get_source_data.assert_called_once()
    assert eucan.printer.print.mock_calls[0] == mock.call("📦 Collecting Source Data")

    assert source_collector_init.mock_calls == [
        mock.call(catalogue),
        mock.call().get_birthcohorts_data(),
    ]

    assembler._transform_data.assert_called_once()
    assert eucan.printer.print.mock_calls[1] == mock.call(
        "✏️ Preparing Source Data for Import"
    )
    assert eucan.printer.print.mock_calls[2] == mock.call(
        "Transform BirthCohorts source data"
    )

    pd.testing.assert_frame_equal(
        data.sort_index(axis=1), birthcohorts_transformed.sort_index(axis=1)
    )
