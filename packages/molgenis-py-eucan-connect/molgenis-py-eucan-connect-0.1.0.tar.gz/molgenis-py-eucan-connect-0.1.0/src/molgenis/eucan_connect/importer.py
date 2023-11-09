from dataclasses import dataclass, field
from typing import List

from molgenis.client import MolgenisRequestError
from molgenis.eucan_connect.errors import ErrorReport, EucanError, EucanWarning
from molgenis.eucan_connect.eucan_client import EucanSession
from molgenis.eucan_connect.model import (
    Catalogue,
    CountryInfo,
    MixedData,
    Source,
    Table,
)
from molgenis.eucan_connect.printer import Printer


@dataclass
class ImportingState:
    existing_data: MixedData
    country_info: CountryInfo
    linkage_info: List
    catalogues: List[Catalogue]
    report: ErrorReport
    data_to_import: MixedData = field(init=False)

    def __post_init__(self):
        self.data_to_import = self.existing_data.copy_empty()
        self.data_to_import.source = Source.TRANSFORMED


class Importer:
    """
    This class is responsible for uploading the data into the EUCAN-Connect Catalogue
    """

    def __init__(
        self,
        session: EucanSession,
        printer: Printer,
    ):
        self.session = session
        self.printer = printer

        self.warnings: List[EucanWarning] = []

    def import_data(self, state: ImportingState):
        """
        Uploads catalogue data to the EUCAN-Connect Catalogue.
        This happens in two steps:
        1. New/existing rows are upserted in the tables
        2. Removed rows are deleted from the tables
        """
        self.printer.print("💾 Saving new and updated data into the EUCAN tables")
        with self.printer.indentation():
            self._upsert_data(state)

        self.printer.print("🧼 Cleaning up removed data from the EUCAN tables")
        with self.printer.indentation():
            self._delete_data(state)

    def _upsert_data(self, state):
        try:
            self.session.upload_data(state.data_to_import)
        except MolgenisRequestError as e:
            raise EucanError(
                "Error importing data in the EUCAN-Connect Catalogue"
            ) from e

    def _delete_data(self, state):
        for table in reversed(state.data_to_import.import_order):
            try:
                with self.printer.indentation():
                    self._delete_rows(
                        table, state.existing_data.table_by_type[table.type], state
                    )
            except MolgenisRequestError as e:
                raise EucanError(
                    f"Error deleting row(s) from {table.type.base_id}"
                ) from e

    def _delete_rows(self, table: Table, existing_table: Table, state: ImportingState):
        """
        Deletes rows from a EUCAN table that are not present in the catalogue anymore
        If a row is referenced from the study linkage table, it is not deleted
        but a warning will be raised.

        :param Table table: the EUCAN table
        :param Table existing_table: the existing rows
        """
        # Compare the ids from staging and production to see what was deleted
        source_ids = table.rows_by_id.keys()
        production_ids = set(existing_table.rows_by_id.keys())
        deleted_ids = production_ids.difference(source_ids)

        # Remove ids that we are not allowed to delete
        undeletable_ids = set(state.linkage_info).intersection(deleted_ids)
        deletable_ids = deleted_ids.difference(undeletable_ids)

        # Actually delete the rows in the EUCAN table
        if deletable_ids:
            self.printer.print(
                f"Deleting {len(deletable_ids)} row(s) from {table.type.base_id}"
            )
            self.session.delete_list(table.type.base_id, list(deletable_ids))
            for id_ in deletable_ids:
                with self.printer.indentation():
                    code = existing_table.rows_by_id[id_]["source_catalogue"]
                    warning = EucanWarning(f"ID {id_} is deleted")
                    self.printer.print_warning(warning)
                    state.report.add_catalogue_warnings(Catalogue.of(code), [warning])

        # Show a warning for every id that we prevented deletion of
        if deleted_ids != deletable_ids:
            for id_ in undeletable_ids:
                warning = EucanWarning(
                    f"Prevented the deletion of a linked study: {id_}"
                )
                self.printer.print_warning(warning)

                code = existing_table.rows_by_id[id_]["source_catalogue"]
                state.report.add_catalogue_warnings(Catalogue.of(code), [warning])
