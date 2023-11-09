from molgenis.eucan_connect.errors import EucanWarning
from molgenis.eucan_connect.printer import Printer
from molgenis.eucan_connect.validator import Validator


def test_validate(mica_catalogue_data):
    validator = Validator(mica_catalogue_data, Printer())

    warnings = validator.validate()

    assert warnings == [
        EucanWarning(message="Study mica_url/study/mcTwo has no objectives"),
        EucanWarning(message="Study mica_url/study/noC has no start_year"),
        EucanWarning(message="Study mica_url/study/noC has no countries"),
    ]
