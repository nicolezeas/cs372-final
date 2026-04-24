from __future__ import annotations

from dataclasses import dataclass, field


def parse_issue_tags(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    return [tag.strip().lower() for tag in str(raw_value).split("|") if tag.strip()]


@dataclass
class SourceDocument:
    doc_id: str
    title: str
    source_url: str
    source_type: str
    jurisdiction: str
    county: str
    issue_category: str
    file_name: str
    text: str
    issue_tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        parsed_tags = self.issue_tags or parse_issue_tags(self.issue_category)
        self.issue_tags = list(dict.fromkeys(parsed_tags))
        if self.issue_tags:
            self.issue_category = self.issue_tags[0]
