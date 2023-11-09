import numpy as np
import pytest

from molgenis.eucan_connect import utils


@pytest.fixture
def rows():
    return [
        {
            "id": "studyA",
            "study_name": "Study A",
            "countries": [],
        },
        {
            "id": "studyB",
            "countries": ["C1"],
        },
    ]


def test_to_ordered_dict(rows):
    rows_by_id = utils.to_ordered_dict(rows)
    assert rows_by_id["studyA"]["study_name"] == "Study A"
    assert rows_by_id["studyB"]["countries"] == ["C1"]


def test_isnan():
    x1 = np.nan
    x2 = "test"
    x3 = ["test1", "test2"]
    x4 = np.NaN

    assert utils.isnan(x1) is True
    assert utils.isnan(x2) is False
    assert utils.isnan(x3) is False
    assert utils.isnan(x4) is True
