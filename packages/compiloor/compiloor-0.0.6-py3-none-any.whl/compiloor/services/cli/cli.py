from typer import Typer

from typing_extensions import Annotated

from compiloor.services.environment.utils import FileUtils, FindingUtils
from compiloor.services.logger import Logger
from compiloor.services.parser.chromium import ChromiumUtils
from compiloor.services.parser.page_numbering import PageNumberingUtils
from compiloor.services.parser.utils import ReportCustomizer
from compiloor.services.typings.finding import FindingIdentifier, FindingStatusAnnotation, SeverityAnnotation
from compiloor.services.environment import (
    current_directory_initialized, initialize_directory,
    add_finding_template
)
from compiloor.services.environment.constants import INITIALIZED, NOT_INITIALIZED
from compiloor.services.utils.config import ConfigUtils

cli = Typer()

@cli.command("init")
def init(force: Annotated[bool, "force"] = False):
    current_directory_initialized(NOT_INITIALIZED, force)
    initialize_directory(force)
    
@cli.command("add-finding")
def add_finding(severity: Annotated[SeverityAnnotation, "severity"] = SeverityAnnotation.MEDIUM):
    current_directory_initialized(INITIALIZED)
    add_finding_template(severity.cast_to_severity())


@cli.command("mark")
def change_finding_status(finding: Annotated[str, "finding"], status: Annotated[FindingStatusAnnotation, "status"]):
    current_directory_initialized(INITIALIZED)
    finding_identifier = FindingIdentifier(finding) # Will throw if the finding id is invalid.

    if finding_identifier.index > FindingUtils.get_current_finding_amount(finding_identifier.severity):
        Logger.error(f"There is no \"{finding}\" finding.")
        exit(1)
    
    finding_path = FileUtils.get_finding_path(finding_identifier.severity, finding_identifier.index)
    # TODO: For the change in status to work we need to have a parser that checks for either the variable from the markdown or one of the other statuses.
    
@cli.command("compile")
def compile_report():
    current_directory_initialized(INITIALIZED)
    ConfigUtils.validate_config_template_urls(FileUtils.read_config(json=True))
    
    # The customizer creates the base report and handles almost all serialization:
    customizer = ReportCustomizer()
    
    # Save the initial report to a PDF file:
    (_, report_path) = ChromiumUtils.create_chromium_document(customizer.report)
    
    # Finalize the report by adding page numbers and a legend:
    PageNumberingUtils.create_report_with_page_numbers_and_legend(report_path, customizer.report_section_headings)


