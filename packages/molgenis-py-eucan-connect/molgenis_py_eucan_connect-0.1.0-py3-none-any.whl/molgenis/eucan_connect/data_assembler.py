import pandas as pd

from molgenis.eucan_connect.birthcohorts.birthcohorts_assembler import (
    Assembler as BirthCohorts,
)
from molgenis.eucan_connect.datacatalogue.datacatalogue_assembler import (
    Assembler as DataCatalogue,
)
from molgenis.eucan_connect.errors import EucanError, requests_error_handler
from molgenis.eucan_connect.eucan_client import EucanSession
from molgenis.eucan_connect.importer import ImportingState
from molgenis.eucan_connect.mica.mica_assembler import Assembler as Mica
from molgenis.eucan_connect.model import Catalogue, CatalogueData
from molgenis.eucan_connect.printer import Printer
from molgenis.eucan_connect.transformer import Transformer
from molgenis.eucan_connect.validator import Validator


class DataAssembler:
    """Prepares catalogues for importing."""

    def __init__(
        self,
        printer: Printer,
        session: EucanSession,
        catalogue: Catalogue,
        state: ImportingState,
    ):
        self.catalogue = catalogue
        self.printer = printer
        self.session = session
        self.state = state

    @requests_error_handler
    def assemble(self):
        if self.catalogue.catalogue_type == "BirthCohorts":
            source_data = BirthCohorts(
                self.printer,
            ).assemble(self.catalogue)
        elif self.catalogue.catalogue_type == "DataCatalogue":
            source_data = DataCatalogue(
                self.printer,
            ).assemble(self.catalogue)
        elif self.catalogue.catalogue_type == "Mica":
            source_data = Mica(
                self.printer,
            ).assemble(self.catalogue)
        else:
            raise EucanError(f"Unknown catalogue type {self.catalogue.catalogue_type}")

        self._transform_data(source_data)
        catalogue_data = self.session.create_catalogue_data(self.catalogue, source_data)
        self._validate_data(catalogue_data)

        return catalogue_data

    def _transform_data(self, source_data: pd.DataFrame):
        with self.printer.indentation():
            warnings = Transformer(self.printer, source_data, self.state).transform()
            if warnings:
                self.state.report.add_catalogue_warnings(self.catalogue, warnings)

    def _validate_data(self, catalogue_data: CatalogueData):
        self.printer.print(f"🔎 Validating {catalogue_data.catalogue.description} data")
        with self.printer.indentation():
            warnings = Validator(catalogue_data, self.printer).validate()
            if warnings:
                self.state.report.add_catalogue_warnings(
                    catalogue_data.catalogue, warnings
                )
