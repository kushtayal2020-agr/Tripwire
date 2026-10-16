# Threat model

## What we protect
An AI agent that reads external content (web pages, emails, documents) **and** can take actions (send email, delete files, make payments, run commands), together with the private data it can access.

## The attack: indirect prompt injection
The attacker does not talk to the agent directly. They plant instructions inside content the agent will read, for example hidden text on a web page. If the model treats that text as a command, the attacker can steal data or trigger actions with the user's authority.

## Attacker assumptions
- Controls some external content the agent may read.
- Cannot change the agent's code, system prompt or model weights.
- May know that Tripwire exists and try to evade it.

## Defences (layers)
| Layer | File | Stops | Does not stop |
|---|---|---|---|
| 1. Heuristics | `tripwire/heuristics.py` | Known phrases in English/Hindi/Hinglish, hidden Unicode and HTML, base64 blobs | Paraphrases, leetspeak, new languages |
| 2. Open-weight classifier | `tripwire/classifier.py` | Attacks similar to its training data | Novel attacks; Hinglish coverage is limited |
| 3. Policy | `tripwire/policy.py`, `tripwire/agent_loop.py` | Risky tool calls (email, delete, payment, shell) once untrusted content is in context, even if detection missed the attack | Attacks that only change the text answer (for example a misleading summary) |

## Design choices
- **Taint tracking:** once the agent has read external content, risky tools are blocked or need user confirmation for the rest of the run. This is deliberately conservative.
- **Local only:** scanning runs on-device, so private content is never sent to a third-party service.
- **Fail visible:** blocked actions and quarantined pages are logged (`tripwire_blocked.log`).

## Known gaps (see `eval/RESULTS.md` for current numbers)
- Paraphrased, obfuscated or multi-step attacks can evade the rules.
- Some harmless text is flagged (for example "New task:" or "Do not tell the user's password...").
- Taint tracking is coarse: it blocks risky tools even when the user's own request, not the page, caused them.
- Data-only attacks (biased or false summaries) are out of scope.

## Out of scope
Jailbreaks typed directly by the user, model backdoors, malware in downloaded files, and network-level attacks.
