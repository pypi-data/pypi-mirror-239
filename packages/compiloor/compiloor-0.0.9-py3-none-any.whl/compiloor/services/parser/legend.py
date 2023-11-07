from compiloor.services.parser.finding import Finding


class ReportLegendUtils:
    """
        A class that contains utility methods for creating the report legend.
    """
    
    @staticmethod
    def create_finding_severities_legend_html(findings_section_index: str, findings: list[Finding]) -> str:
        # The bellow code can only work with strings so we are casting the findings_section_index to a string here:
        if not isinstance(findings_section_index, str):
            findings_section_index = str(findings_section_index) 

        fragments = []
        current_severity, current_severity_index, current_severity_finding_index = None, 0, 0

        for finding in findings:
            if finding.severity != current_severity:
                
                current_severity = finding.severity
                current_severity_index += 1
                current_severity_finding_index = 0
                section_index = f'[{findings_section_index}.{current_severity_index}]_page'

                if current_severity_index != 1: fragments.append("<div>")

                fragments.extend([
                    f'''
                        <div class="sub-paragraph">
                            <a href="#section-{findings_section_index}-{current_severity_index}">
                                <div class="section-wrapper">
                                    <p>
                                        {findings_section_index}.{current_severity_index}. {current_severity.cast_to_display_case()} Findings
                                    </p>
                                    {{{{{section_index}}}}}
                                </div>
                            </a>
                        </div>
                    '''
                    # '</div>'
                ])

            current_severity_finding_index += 1
            section_index = f'[{finding.id}]_page'

            fragments.append(
                f'''
                <div class="sub-sub-paragraph">
                    <a href="#section-{findings_section_index}-{current_severity_index}-{current_severity_finding_index}">
                        <div class="section-wrapper">
                            <p class="legend-section-heading">[{finding.id}] {finding.title.replace("`", "")}</p>
                            <p class="page-number">{{{{{section_index}}}}}</p>
                        </div>
                    </a>
                </div>
                '''
            )

        return "".join(fragments)