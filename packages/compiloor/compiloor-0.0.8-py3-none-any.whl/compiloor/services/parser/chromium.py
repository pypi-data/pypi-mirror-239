from bs4 import BeautifulSoup

from typing import Tuple

from os.path import abspath

from playwright.sync_api import sync_playwright

from compiloor.services.environment.utils import FileUtils, ReportUtils
from compiloor.constants.environment import REPORTS_DIRECTORY
from compiloor.constants.utils import REPORT_EXTENSION


class ChromiumUtils:
    """
        A class containing utilities for creating PDF documents from HTML fragments using the playwright chromium driver.
    """
    
    @staticmethod
    def create_chromium_document(fragment: str, dir: str = abspath(REPORTS_DIRECTORY)) -> Tuple[int, str]:
        """
            Creates a PDF document from the given HTML fragment and saves it in the given directory.
        """
        
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul"]: fragment = fragment.replace(f"<{tag}></{tag}>", "")
        fragment = BeautifulSoup(fragment, "html.parser")

        # Using a context manager just because the documentation says so:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            document = browser.new_page()
            document.set_content(str(fragment), wait_until="networkidle")
            report_index = ReportUtils.get_current_report_count() + 1 
            
            dir = f'{dir}/report-{FileUtils.get_fs_sig_index(report_index)}{REPORT_EXTENSION}'
            
            document.pdf(path=dir, print_background=True, format="A4")
            # Keeping the html digest for debugging purposes:
            # open("report.html", "w").write(document.content())
            browser.close()
        return report_index, dir