import pytest
import requests.exceptions

from molgenis.eucan_connect.errors import (
    ErrorReport,
    EucanError,
    EucanWarning,
    requests_error_handler,
)
from molgenis.eucan_connect.model import Catalogue


def test_warning():
    warning = EucanWarning("test")
    assert warning.message == "test"


def test_error():
    error = EucanError("test")
    assert str(error) == "test"


def test_error_report():
    a = Catalogue("A", "A", "A.com", "A-type")
    b = Catalogue("B", "B", "B.com", "B-type")
    report = ErrorReport([a, b])
    warning = EucanWarning("warning")
    error = EucanError("error")

    assert not report.has_errors()
    assert not report.has_warnings()

    report.add_catalogue_error(a, error)

    assert report.catalogue_errors[a] == error
    assert b not in report.catalogue_errors
    assert report.has_errors()
    assert not report.has_warnings()

    report.add_catalogue_warnings(b, [warning, warning])

    assert report.catalogue_warnings[b] == [warning, warning]
    assert a not in report.catalogue_warnings
    assert report.has_errors()
    assert report.has_warnings()


def test_error_report_global_error():
    report = ErrorReport([])
    assert not report.has_errors()
    report.set_global_error(EucanError())
    assert report.has_errors()


def test_requests_error_handler():
    exception = requests.exceptions.ConnectionError()

    @requests_error_handler
    def raising_function():
        raise exception

    with pytest.raises(EucanError) as exception_info:
        raising_function()

    assert exception_info.value.__cause__ == exception
