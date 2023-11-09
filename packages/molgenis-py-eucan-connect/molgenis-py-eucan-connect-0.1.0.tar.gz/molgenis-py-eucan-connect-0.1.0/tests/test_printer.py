import textwrap

from molgenis.eucan_connect.errors import ErrorReport, EucanError, EucanWarning
from molgenis.eucan_connect.model import Catalogue
from molgenis.eucan_connect.printer import Printer


def test_indentation(capsys):
    expected = textwrap.dedent(
        """\
        line1
            line2
                line3
                line4
            line5
        """
    )

    printer = Printer()
    printer.print("line1")
    printer.indent()
    printer.print("line2")
    printer.indent()
    printer.print("line3")
    printer.dedent()
    printer.print("line4", 1)
    printer.print("line5")

    captured = capsys.readouterr()
    assert captured.out == expected


def test_reset_indent(capsys):
    expected = textwrap.dedent(
        """\
                line1
        line2
        """
    )

    printer = Printer()
    printer.indent()
    printer.indent()
    printer.print("line1")
    printer.reset_indent()
    printer.print("line2")

    captured = capsys.readouterr()
    assert captured.out == expected


def test_print_catalogue_title(capsys):
    catalogue = Catalogue("MS", "Mica", "url", "Maelstrom")
    expected = textwrap.dedent(
        """\

        ===========================
        🌍 Catalogue MS (Maelstrom)
        ===========================
        """
    )

    printer = Printer()
    printer.print_catalogue_title(catalogue)

    captured = capsys.readouterr()
    assert captured.out == expected


def test_print_error_with_cause(capsys):
    expected = "❌ this is the message - Cause: this is the cause\n"

    try:
        raise EucanError("this is the message") from ValueError("this is the cause")
    except EucanError as e:
        Printer().print_error(e)

    captured = capsys.readouterr()
    assert captured.out == expected


def test_print_error_without_cause(capsys):
    expected = "❌ this is the message\n"

    try:
        raise EucanError("this is the message")
    except EucanError as e:
        Printer().print_error(e)

    captured = capsys.readouterr()
    assert captured.out == expected


def test_print_warning(capsys):
    expected = "⚠️ this is the message\n"
    warning = EucanWarning("this is the message")

    Printer().print_warning(warning)

    captured = capsys.readouterr()
    assert captured.out == expected


def test_print_summary(capsys):
    expected = textwrap.dedent(
        """\

        ==========
        📋 Summary
        ==========
        ✅ Catalogue A finished successfully
        ❌ Catalogue B failed
        ❌ Catalogue C failed with 1 warning(s)
        ⚠️ Catalogue D finished successfully with 2 warning(s)
        """
    )

    a = Catalogue("A", "success", "url", "typeA")
    b = Catalogue("B", "error", "url", "typeB")
    c = Catalogue("C", "error and warnings", "url", "typeC")
    d = Catalogue("D", "success with warnings", "url", "typeD")
    catalogues = [a, b, c, d]
    report = ErrorReport(catalogues)
    warning = EucanWarning("warning")
    error = EucanError("error")
    report.add_catalogue_warnings(c, [warning])
    report.add_catalogue_warnings(d, [warning, warning])
    report.add_catalogue_error(b, error)
    report.add_catalogue_error(c, error)

    Printer().print_summary(report)

    captured = capsys.readouterr()
    assert captured.out == expected


def test_with_indentation(capsys):
    expected = textwrap.dedent(
        """\
        line1
            line2
        line3
        """
    )

    printer = Printer()

    printer.print("line1")
    with printer.indentation():
        printer.print("line2")
    printer.print("line3")

    captured = capsys.readouterr()
    assert captured.out == expected
