# Tripwire: a prompt-injection guard for open-weight agents

Tripwire protects AI agents from hidden instructions in web pages, emails and documents. It runs fully locally on open-weight models, and supports English, Hindi and Hinglish attacks.

## Compliance with the challenge guidelines
| Guideline | Where |
|---|---|
| Open-source / open-weight AI is important | `tripwire/classifier.py` (open-weight DeBERTa classifier), `tripwire/agent_loop.py` (local open-weight LLM via Ollama) |
| Public GitHub repo + open-source license | `LICENSE` (MIT) |
| Agent skill follows the Agent Skill Open Standard | `skill/tripwire-guard/SKILL.md` |
| Model harness: original implementation | `tripwire/agent_loop.py`, `tripwire/policy.py` |

## How it works
1. **Heuristics** (`heuristics.py`): rules for English/Hinglish/Hindi phrases, hidden Unicode, hidden HTML, base64 blobs.
2. **Classifier** (`classifier.py`): open-weight model scores anything the rules miss.
3. **Policy** (`policy.py`): tags untrusted content and blocks risky tool calls (email, delete, payment) when it is in context.

## Quick start
```bash
pip install -r requirements.txt
python -m pytest                 # tests
python -m eval.run_eval          # results table
python -m demo.agent_demo        # attack demo (offline mock model)
python -m demo.agent_demo --ollama   # with a real local model: ollama pull qwen2.5:3b
```

## Results
_Paste the output of `python -m eval.run_eval` here._

## Limitations
Small hand-written test set (rules were tuned while looking at it, so real-world numbers will be lower); adaptive or heavily obfuscated attacks can evade the rules; the classifier is mostly English-trained. The policy layer is the safety net for what detection misses.

## Team
Detection: @member-a | Harness: @member-b | Skill, eval, docs: @member-c
