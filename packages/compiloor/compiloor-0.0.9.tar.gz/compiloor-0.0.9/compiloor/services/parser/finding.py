from mistune import create_markdown, escape, HTMLRenderer

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.token import Error
from pygments.styles.default import DefaultStyle

from compiloor.constants.environment import FINDING_RESOLUTION_STATUS_HEADING
from compiloor.services.logger.logger import Logger
from compiloor.services.typings.finding import Severity, SeverityFolderIndex, FindingStatusAnnotation


# This class if here to avoid circular imports:
class DefaultStyleExtended(DefaultStyle):
    """
        A class that extends the default Pygments style.
        Removes the red color from the Error token.
    """
    
    styles = DefaultStyle.styles.copy()
    styles.update({ Error: '#000' })

class Finding:
    """
        A class that represents a serialized finding.
    """
    
    id: str # The ID of the finding. Example: "[H-01]".
    id_num: int # The number of the finding in the severity it belongs to.
    
    title: str
    severity: Severity
    status: FindingStatusAnnotation
    
    fragment: str
    
    # The to-be-rendered HTML fragment of the finding. It includes rendered code blocks. 
    # This is the fragment that will be inserted into the report.
    render_fragment: str 
    
    def __init__(self, fragment: str) -> None:
        self.fragment = fragment
        first_row = fragment.split("\n")[0]
        
        if not "[" in first_row or not "]" in first_row:
            Logger.error(f"Invalid finding fragment: {first_row}")
            exit(1)
        
        fragments: list[str] = first_row.split("]")
        
        if fragments[1] == "": fragments[1] = "-"
        
        self.id = fragments[0].split("[")[1].strip()
        self.id_num = int(self.id.split("-")[1].strip())
        
        self.title = fragments[1].strip()
        self.severity = SeverityFolderIndex.cast_to_severity(SeverityFolderIndex(self.id.split("-")[0].strip().upper()))
        self.status = None
        
        if FINDING_RESOLUTION_STATUS_HEADING in self.fragment:
            
            _resolution_status_fragment = self.fragment.split(FINDING_RESOLUTION_STATUS_HEADING)[1].strip()
            if _resolution_status_fragment == "{{resolution_status}}": 
                self.fragment = self.fragment.replace(_resolution_status_fragment, FindingStatusAnnotation.RESOLVED.value)
                _resolution_status_fragment = FindingStatusAnnotation.RESOLVED
                
            self.status = FindingStatusAnnotation(_resolution_status_fragment)

            self.fragment = self.fragment.replace(FINDING_RESOLUTION_STATUS_HEADING + self.status.value, "")

        if not self.status: self.status = FindingStatusAnnotation.RESOLVED

        # TODO: Abstract away the CSS classes into a modular system.
        self.render_fragment = f'''
            <div id="section-8-[[{self.severity.value}_severity_index]]-{self.id_num}" class="finding">
                {MarkdownRenderer.create_markdown(self.fragment)}
            </div>
        '''
                    
    def __str__(self) -> str:
        """
        Returns the finding's raw string fragment.
        """
        
        return self.fragment
    
class HighlightRenderer(HTMLRenderer):
    """
        A custom renderer that highlights code blocks.
    """
    
    def block_code(self, code, info=None):
        """
            Renders a code block with syntax highlighting.
        """
        
        if not info:
            # Wrapping it in a code block:
            return '<pre><code>' + escape(code) + '</code></pre>'
        
        lexer = get_lexer_by_name(info, stripall=True)
        formatter = HtmlFormatter(style=DefaultStyleExtended, full=True)
        
        highlighted_code: str = highlight(code, lexer, formatter)
        
        # TODO: Abstract away the CSS classes into a modular system.
        return f'<div class="code-border no-underline-heading">{highlighted_code}</div>'
    
class MarkdownRenderer():
    """
        A custom renderer that renders Markdown.
    """
    
    @staticmethod
    def create_markdown(fragment: str, remove_newlines: bool = False) -> str:
        """
            Creates a Markdown parser with syntax highlighting.
        """
        
        markdown: str = create_markdown(renderer=HighlightRenderer())(fragment)
        
        return markdown.replace("\n", "") if remove_newlines else markdown