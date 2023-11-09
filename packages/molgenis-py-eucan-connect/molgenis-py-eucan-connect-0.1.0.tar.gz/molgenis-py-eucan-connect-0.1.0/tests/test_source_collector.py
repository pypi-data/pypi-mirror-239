import json
from importlib import resources
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from molgenis.eucan_connect.errors import EucanError
from molgenis.eucan_connect.model import Catalogue
from molgenis.eucan_connect.source_collector import SourceCollector


def birthcohorts():
    """
    Reads the data (json-format) from birthcohorts.json to test with.
    """
    file = open(str(resources.files("tests.resources") / "birthcohorts.json"), "r")
    birthcohorts_data = json.load(file)
    file.close()
    return birthcohorts_data


def datacatalogue():
    """
    Reads the data (json-format) from datacatalogue.json to test with.
    """
    file = open(str(resources.files("tests.resources") / "datacatalogue.json"), "r")
    datacatalogue_data = json.load(file)
    file.close()
    return datacatalogue_data


def mica():
    """
    Reads the data (json-format) from mica.json to test with.
    """
    file = open(str(resources.files("tests.resources") / "mica.json"), "r")
    mica_data = json.load(file)
    file.close()
    return mica_data


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (
        args[0] == "http://www.birthcohorts.net/wp-content/themes/x-child/"
        "rss.cohorts.php?limit=10&page=1&json"
    ):
        return MockResponse({"cohort": birthcohorts()}, 200)
    elif (
        args[0] == "http://www.birthcohorts.net/wp-content/themes/x-child/"
        "rss.cohorts.php?limit=10&page=11&json"
    ):
        return MockResponse({}, 200)
    elif args[0] == "https://mica_url/ws/study/mc1":
        return MockResponse(mica()[0], 200)
    elif args[0] == "https://mica_url/ws/study/mcTwo":
        return MockResponse(mica()[1], 200)
    elif args[0] == "https://mica_url/ws/study/noC":
        return MockResponse(mica()[2], 200)
    elif args[0] == "https://mica_url/ws/network/micanetwork":
        return MockResponse(
            {
                "studySummaries": [
                    {"design": "cohort_study", "id": "mc1"},
                    {"design": "cohort_study", "id": "mcTwo"},
                    {"design": "cohort_study", "id": "noC"},
                ]
            },
            200,
        )

    return MockResponse(None, 404)


# This method will be used by the mock to replace requests.post
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "https://dc_url/catalogue/graphql":
        return MockResponse({"data": {"Cohorts": datacatalogue()}}, 200)
    elif args[0] == "https://mica_url/ws/studies/_rql":
        return MockResponse(
            {
                "studyResultDto": {
                    "obiba.mica.StudyResultDto.result": {
                        "summaries": [{"id": "mc1"}, {"id": "mcTwo"}, {"id": "noC"}]
                    },
                    "totalHits": 3,
                }
            },
            200,
        )

    return MockResponse(None, 404)


# patch 'requests.get' with the mock method.
@patch("requests.get", side_effect=mocked_requests_get)
def test_birthcohorts(mock_get, birthcohorts_data):
    catalogue = Catalogue("BC", "BirthCohorts", "birthcohorts_url", "BirthCohorts")
    source_collector = SourceCollector(catalogue)
    source_collector._check_source_data = MagicMock(
        side_effect=source_collector._check_source_data
    )
    source_collector.printer = MagicMock()

    data = source_collector.get_birthcohorts_data()

    source_collector._check_source_data.assert_called_once()
    assert source_collector.printer.print.mock_calls[0] == mock.call(
        "Number of BirthCohorts studies is 3"
    )
    assert data == birthcohorts_data


# patch 'requests.post' with the mock method.
@patch("requests.Session.post", side_effect=mocked_requests_post)
def test_datacatalogue(mock_post, datacatalogue_data):
    catalogue = Catalogue("TN", "DataCatalogue", "https://dc_url", "TestNetwork")
    source_collector = SourceCollector(catalogue)
    source_collector._check_source_data = MagicMock(
        side_effect=source_collector._check_source_data
    )
    source_collector.printer = MagicMock()
    source_collector._mica_study_ids = MagicMock(
        side_effect=source_collector._mica_study_ids
    )

    source_collector._mica_study_data = MagicMock(
        side_effect=source_collector._mica_study_data
    )

    data = source_collector.get_datacatalogue_data()

    source_collector._check_source_data.assert_called_once()
    assert source_collector.printer.print.mock_calls[0] == mock.call(
        "Number of TestNetwork studies is 3"
    )
    assert data == datacatalogue_data


@patch("requests.Session.get", side_effect=mocked_requests_get)
@patch("requests.Session.post", side_effect=mocked_requests_post)
def test_mica(mock_post, mock_get, mica_data):
    catalogue = Catalogue("MS", "Mica", "https://mica_url", "Mica")
    source_collector = SourceCollector(catalogue)
    source_collector._check_source_data = MagicMock(
        side_effect=source_collector._check_source_data
    )
    source_collector.printer = MagicMock()

    data = source_collector.get_mica_data()

    source_collector._check_source_data.assert_called_once()
    assert source_collector.printer.print.mock_calls[0] == mock.call(
        "Number of Mica studies is 3"
    )

    assert sorted(data, key=lambda d: d["id"]) == sorted(
        mica_data, key=lambda d: d["id"]
    )


@patch("requests.Session.get", side_effect=mocked_requests_get)
@patch("requests.Session.post", side_effect=mocked_requests_post)
def test_mica_networks(mock_post, mock_get, mica_data):
    catalogue = Catalogue("MS", "Mica", "https://mica_url", "Mica", None, "MicaNetwork")
    source_collector = SourceCollector(catalogue)
    source_collector._check_source_data = MagicMock(
        side_effect=source_collector._check_source_data
    )
    source_collector.printer = MagicMock()

    data = source_collector.get_mica_data()

    source_collector._check_source_data.assert_called_once()
    assert source_collector.printer.print.mock_calls[0] == mock.call(
        "Number of Mica studies is 3"
    )
    assert sorted(data, key=lambda d: d["id"]) == sorted(
        mica_data, key=lambda d: d["id"]
    )


def test_no_source_data():
    catalogue = Catalogue("MS", "Mica", "https://mica_url", "Mica")
    source_collector = SourceCollector(catalogue)

    with pytest.raises(EucanError) as e:
        source_collector._check_source_data([])

    assert str(e.value) == "No Mica source data found!"
