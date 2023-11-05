from os.path import abspath


FINDING_TEMPLATE_NAME = "finding-template.md"
CONFIG_NAME = "config.json"

INITIALIZED = True
NOT_INITIALIZED = False

MAIN_DIRECTORY = "compiloor-report"
MAIN_DIRECTORY_ABS_PATH = abspath(MAIN_DIRECTORY)

FINDINGS_DIRECTORY = "findings"
REPORTS_DIRECTORY = MAIN_DIRECTORY + "/reports"
TEMPLATE_DIRECTORY = "templates"

CONFIG_DIRECTORY = MAIN_DIRECTORY + "/" + CONFIG_NAME

FINDING_LIST_TABLE_COLUMNS = ["ID", "Title", "Severity", "Status"]

BASE_CONFIG_SCHEMA: dict[str, str] = {
    "title": "SECURITY RESEARCHER NAME",
    "author": "SECURITY RESEARCER",
    "date": "DATE",
    "company_name": "COMPANY NAME",
    "protocol_name": "PROTOCOL NAME",
    "repository": "GITHUB/GITLAB REPOSITORY",
    "type": "SOME PROTOCOL TYPE",
    "commit": "COMMIT HASH",
    "sloc": "SLOC",
    "about_author_content": "ABOUT SECTION",
    "disclaimer_content": "DISCLAIMER CONTENT",
    "introduction_content": "INTRODUCTION CONTENT",
    "about_protocol_content": "ABOUT PROTOCOL CONTENT",
    "template_url": "REPORT URL",
    "stylesheet_url": "REPORT CONTENT",
    "cover_img_url": "COVER IMAGE URL",
}

FINDING_RESOLUTION_STATUS_HEADING: str = "## _STATUS_="

FINDING_RESOLUTION_STATUS_SECTION: str = FINDING_RESOLUTION_STATUS_HEADING + "{{resolution_status}}"


BASE_FINDING_MD_TEMPLATE: str = f"""# [{{{{finding_severity}}}}-{{{{finding_index}}}}]

## Severity

**Impact:**

**Likelihood:**

## Description

## Recommendations

{FINDING_RESOLUTION_STATUS_SECTION}
""" 