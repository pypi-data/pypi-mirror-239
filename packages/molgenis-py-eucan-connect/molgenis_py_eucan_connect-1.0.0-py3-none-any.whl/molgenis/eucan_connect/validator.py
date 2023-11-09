from typing import List

from molgenis.eucan_connect.errors import EucanWarning
from molgenis.eucan_connect.model import CatalogueData, Table
from molgenis.eucan_connect.printer import Printer


class Validator:
    """
    This class is responsible for validating the transformed data. Validation
    consists of:
    1. Checking if there is missing data in the variables of the minimal dataset
    """

    def __init__(self, catalogue_data: CatalogueData, printer: Printer):
        self.catalogue_data = catalogue_data
        self.printer = printer
        self.warnings: List[EucanWarning] = list()

    def validate(self) -> List[EucanWarning]:
        for table in self.catalogue_data.import_order:
            self._validate_minimal_dataset(table)

        return self.warnings

    def _validate_minimal_dataset(self, table: Table):
        for row in table.rows:
            for column in table.type.minimal_dataset:
                if column not in row or (
                    type(row[column]) not in (bool, int) and len(row[column]) == 0
                ):
                    warning = EucanWarning(
                        f"Study {row['source_data']} has no {column}"
                    )
                    self.printer.print_warning(warning)
                    self.warnings.append(warning)
