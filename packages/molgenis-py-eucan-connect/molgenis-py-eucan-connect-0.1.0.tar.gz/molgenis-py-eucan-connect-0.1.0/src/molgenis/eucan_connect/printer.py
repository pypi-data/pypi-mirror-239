from contextlib import contextmanager

from molgenis.eucan_connect.errors import ErrorReport, EucanError, EucanWarning
from molgenis.eucan_connect.model import Catalogue


class Printer:
    """
    Simple printer that keeps track of indentation levels. Also has utility methods
    for printing some EUCAN-Connect objects.
    """

    def __init__(self):
        self.indents = 0

    def indent(self):
        self.indents += 1

    def dedent(self):
        self.indents = max(0, self.indents - 1)

    def reset_indent(self):
        self.indents = 0

    def print(self, value: str = None, indent: int = 0):
        self.indents += indent
        if value:
            print(f"{'    ' * self.indents}{value}")
        else:
            print()
        self.indents -= indent

    def print_catalogue_title(self, catalogue: Catalogue):
        self.print_header(f"🌍 Catalogue {catalogue.code} ({catalogue.description})")

    def print_header(self, text: str):
        title = f"{text}"
        border = "=" * (len(title) + 1)
        self.reset_indent()
        self.print()
        self.print(border)
        self.print(title)
        self.print(border)

    def print_error(self, error: EucanError):
        message = str(error)
        if error.__cause__:
            message += f" - Cause: {str(error.__cause__)}"
        self.print(f"❌ {message}")

    def print_warning(self, warning: EucanWarning, indent: int = 0):
        self.print(f"⚠️ {warning.message}", indent)

    def print_summary(self, report: ErrorReport):
        self.reset_indent()
        self.print()
        self.print("==========")
        self.print("📋 Summary")
        self.print("==========")

        for catalogue in report.catalogues:
            if catalogue in report.catalogue_errors or report.error:
                message = f"❌ Catalogue {catalogue.code} failed"
                if catalogue in report.catalogue_warnings:
                    message += (
                        f" with {len(report.catalogue_warnings[catalogue])} warning(s)"
                    )
            elif catalogue in report.catalogue_warnings:
                message = (
                    f"⚠️ Catalogue {catalogue.code} finished successfully with "
                    f"{len(report.catalogue_warnings[catalogue])} warning(s)"
                )
            else:
                message = f"✅ Catalogue {catalogue.code} finished successfully"
            self.print(message)

    @contextmanager
    def indentation(self):
        self.indent()
        yield
        self.dedent()
