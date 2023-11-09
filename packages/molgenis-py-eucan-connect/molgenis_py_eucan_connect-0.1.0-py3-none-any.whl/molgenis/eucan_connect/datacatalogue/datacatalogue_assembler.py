from typing import List

from molgenis.eucan_connect.datacatalogue.datacatalogue_transformer import Transformer
from molgenis.eucan_connect.errors import requests_error_handler
from molgenis.eucan_connect.model import Catalogue
from molgenis.eucan_connect.printer import Printer
from molgenis.eucan_connect.source_collector import SourceCollector


class Assembler:
    """Prepares catalogue data for importing."""

    def __init__(
        self,
        printer: Printer,
    ):
        self.printer = printer

    @requests_error_handler
    def assemble(self, catalogue: Catalogue):
        source_data = self._get_source_data(catalogue)
        return self._transform_data(catalogue, source_data)

    def _get_source_data(self, catalogue: Catalogue) -> List:
        self.printer.print("📦 Collecting Source Data")
        return SourceCollector(catalogue).get_datacatalogue_data()

    def _transform_data(self, catalogue: Catalogue, source_data: List):
        self.printer.print("✏️ Preparing Source Data for Import")
        with self.printer.indentation():
            return Transformer(
                catalogue=catalogue,
                printer=self.printer,
            ).transform(source_data)
