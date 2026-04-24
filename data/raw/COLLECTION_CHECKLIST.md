# NC Housing Source Collection Checklist

Use this file to track the sources you manually collect for LexAI-NC.

## Goal

Collect at least 8 to 10 North Carolina housing-related documents with useful legal or procedural information.

## Best First Sources

- [ ] `nc_courts_landlord_tenant_issues.txt`
- [ ] `legal_aid_nc_housing_overview.txt`
- [ ] `nc_courts_small_claims_landlord_tenant.txt`
- [ ] `legal_aid_nc_security_deposit.txt`
- [ ] `legal_aid_nc_repairs_habitability.txt`
- [ ] `legal_aid_nc_eviction_help.txt`
- [ ] `legal_aid_nc_lockout_rights.txt`
- [ ] `legal_aid_nc_lease_termination.txt`
- [ ] `legal_aid_nc_utility_shutoff.txt`
- [ ] `nc_county_housing_court_help.txt`
- [ ] `nc_tenant_landlord_rental_laws_2026.txt`
- [ ] `nc_chapter_42_landlord_tenant.txt`

## For Each Source

1. Open the webpage.
2. Copy the main content only.
3. Paste it into the matching `.txt` file in this folder.
4. Replace `FILL_URL_HERE` in the text file and in `source_index.csv`.
5. If relevant, replace `FILL_COUNTY_HERE`.

## Cleanup Rules

Keep:

- title
- headings
- legal explanations
- court steps
- filing rules
- timelines
- rights and next-step guidance

Remove:

- navigation menus
- headers and footers
- donation prompts
- repeated page chrome
- unrelated links

## Done Check

When 3 or more files contain real text instead of placeholders, run:

```bash
python3 -m src.data.pipeline
python3 -m src.main
```
