from typing import List

from molgenis.eucan_connect.data_assembler import DataAssembler
from molgenis.eucan_connect.errors import (
    ErrorReport,
    EucanError,
    EucanWarning,
    requests_error_handler,
)
from molgenis.eucan_connect.eucan_client import AttributesRequest, EucanSession
from molgenis.eucan_connect.importer import Importer, ImportingState
from molgenis.eucan_connect.model import Catalogue
from molgenis.eucan_connect.printer import Printer


class Eucan:
    """
    Main class for importing data from source catalogues
    into the EUCAN-Connect Catalogue.
    """

    def __init__(self, session: EucanSession):
        """
        :param EucanSession session: an authenticated session with
                                     an EUCAN-Connect Catalogue
        """
        self.session = session
        self.printer = Printer()
        self.importer = Importer(self.session, self.printer)
        self.warnings: List[EucanWarning] = []

    def import_catalogues(self, catalogues: List[Catalogue]) -> ErrorReport:
        """
        Imports data from the provided source catalogue(s) into the tables
        in the EUCAN-Connect catalogue.

        Parameters:
            catalogues (List[Catalogue]): The list of catalogues to import data from
        """

        report = ErrorReport(catalogues)
        try:
            state = self._init_state(catalogues, report)
        except EucanError as e:
            self.printer.print_error(e)
            report.set_global_error(e)
        else:
            self._assemble_catalogue_data(catalogues, state)
            self._import_catalogue_data(state)

        self.printer.print_summary(report)
        return report

    @requests_error_handler
    def _init_state(
        self, catalogues: List[Catalogue], report: ErrorReport
    ) -> ImportingState:
        self.printer.print_header("⚙️ Preparation")

        self.printer.print("📦 Retrieving existing EUCAN-Connect Catalogue data")
        eucan_data = self.session.get_eucan_data(
            catalogues,
            AttributesRequest(
                persons=["id", "source_catalogue"],
                events=["id", "source_catalogue"],
                populations=["id", "source_catalogue"],
                studies=["id", "study_name", "source_catalogue"],
            ),
        )

        self.printer.print("📦 Retrieving Country Information")
        country_info = self.session.get_country_info()

        self.printer.print("📦 Retrieving Study Linkage Information")
        linkage_info = self.session.get_linked_studies()

        return ImportingState(
            existing_data=eucan_data,
            country_info=country_info,
            linkage_info=linkage_info,
            catalogues=catalogues,
            report=report,
        )

    def _assemble_catalogue_data(self, catalogues, state):
        for catalogue in catalogues:
            self.printer.print_catalogue_title(catalogue)
            try:
                catalogue_data = DataAssembler(
                    self.printer, self.session, catalogue, state
                ).assemble()
                state.data_to_import.merge(catalogue_data)
            except EucanError as e:
                self.printer.print_error(e)
                state.existing_data.remove_catalogue_rows(catalogue)
                state.report.add_catalogue_error(catalogue, e)

    def _import_catalogue_data(self, state: ImportingState):
        self.printer.print_header(
            f"🎁 Import catalogue{'s' if len(state.catalogues) > 1 else ''}"
        )
        try:
            self.importer.import_data(state)
        except EucanError as e:
            self.printer.print_error(e)
            state.report.set_global_error(e)
