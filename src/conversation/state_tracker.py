from __future__ import annotations

from dataclasses import dataclass, field
import re


KNOWN_COUNTIES = [
    "durham",
    "wake",
    "mecklenburg",
    "orange",
    "guilford",
    "buncombe",
    "forsyth",
]

ISSUE_KEYWORDS = {
    "lockout": ["lockout", "changed the locks", "changed my locks", "changed locks", "padlock", "locked me out"],
    "utility_shutoff": ["utilities", "utility", "water", "power", "electric", "gas", "shut off"],
    "security_deposit": ["security deposit", "deposit", "itemized bill"],
    "habitability": ["repair", "repairs", "mold", "heat", "plumbing", "habitable"],
    "eviction": ["eviction", "evict", "summary ejectment", "writ of possession"],
    "lease_termination": ["month-to-month", "month to month", "notice", "terminate lease", "lease ended"],
}


@dataclass
class UserCaseState:
    county: str | None = None
    issue_category: str | None = None
    has_written_lease: bool | None = None
    hearing_date: str | None = None
    urgency_level: str | None = None
    facts: dict[str, str] = field(default_factory=dict)

    def update_fact(self, key: str, value: str) -> None:
        self.facts[key] = value

    def infer_from_text(self, text: str) -> None:
        lowered = text.lower()

        for county in KNOWN_COUNTIES:
            if county in lowered:
                self.county = county.title()
                break

        matched_issues: list[str] = []
        for issue, keywords in ISSUE_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                matched_issues.append(issue)

        if matched_issues:
            self.issue_category = matched_issues[-1]
            self.facts["matched_issues"] = ", ".join(matched_issues)

        if any(word in lowered for word in ["today", "tomorrow", "soon", "urgent", "asap", "court date", "hearing is soon"]):
            self.urgency_level = "high"

        if "written lease" in lowered:
            self.has_written_lease = True
        elif "no lease" in lowered or "oral lease" in lowered:
            self.has_written_lease = False

        hearing_match = re.search(r"hearing (?:is )?(?:on )?([a-z]+\s+\d{1,2})", lowered)
        if hearing_match:
            self.hearing_date = hearing_match.group(1)

        if any(phrase in lowered for phrase in ["changed the locks", "changed my locks", "changed locks", "locked me out"]):
            self.facts["possible_lockout"] = "yes"
        if any(phrase in lowered for phrase in ["repair", "repairs", "mold", "heat", "plumbing"]):
            self.facts["repair_or_habitability_issue"] = "yes"

    def summary(self) -> str:
        return (
            f"county={self.county}, "
            f"issue_category={self.issue_category}, "
            f"urgency={self.urgency_level}, "
            f"written_lease={self.has_written_lease}"
        )
