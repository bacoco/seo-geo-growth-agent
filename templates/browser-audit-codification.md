# Browser Audit Codification

Use this template after a browser-driven audit flow has been performed successfully at least twice for the same class of site.

## Candidate Flow

| Field | Value |
|---|---|
| Site class |  |
| Repeated task |  |
| Browser steps |  |
| Stable selectors or URLs |  |
| Required auth/cookies | none / owner-provided / private |
| Outputs | screenshots / JSON / CSV / report |
| Failure modes |  |

## Codification Decision

| Criterion | Pass? | Evidence |
|---|---:|---|
| Same flow repeated at least twice |  |  |
| Does not transmit sensitive data |  |  |
| Can run in report-only mode |  |  |
| Has deterministic output schema |  |  |
| Has a fixture or saved screenshot |  |  |

## Result

- Keep manual
- Add project-local browser note
- Add reusable script
- Add full browser-skill

## Safety Notes

Do not codify flows that bypass access controls, solve CAPTCHAs, evade WAFs, submit forms, or mutate owner data unless the user explicitly owns the site and authorizes that exact action.
