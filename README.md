# Persian–English Tool-Calling Probe

**Author:** Matin Khosravi  
**Experiment date:** 2026-10-23  
**Model:** `gemini-3.1-flash-lite`

Supporting materials for the article **“One Click in English. Lost in Arabic.”** submitted to Towards Data Science. This is a **small exploratory experiment**, not proof of equivalent general multilingual agent performance.

## Design

Five customer-support scenarios, each tested three times in Persian and three times in English: 30 total trials. The available tools were `lookup_order`, `update_shipping_address`, `cancel_order`, and `create_support_ticket`. Function calling was forced with `ANY`, so the experiment did not measure whether the model would choose not to call a tool. No real-world actions were executed.

## Results

| Metric | Persian | English |
|---|---:|---:|
| Completed | 15 | 15 |
| Initial automatic score | 15/15 | 12/15 |
| After documented semantic review | 15/15 | 15/15 |

All three original English failures were the same support-ticket task. The model selected the correct function and order ID, but generated `package is damaged` instead of the expected `damaged package`. This is a semantically valid paraphrase, so the three classifications were corrected in a **separate audit**; the raw observations must remain unchanged.

## Materials

- `data/gemini_observations_raw.jsonl`: original observations
- `data/semantic_audit.json`: separate reviewed classifications
- `experiment/trial_manifest.csv`: prompts and expected calls
- `experiment/tool_schemas.json`: tool definitions
- `experiment/run_gemini.py`: original execution script
- `experiment/run_gemini_reproducible.py`: adapted rerun script, where provided

## Limitations

Only five simple tasks, repeated three times per language; one model; English tool names; forced tool calls; no real tool execution, GUI testing, or Arabic trials. The manual scoring correction was conducted after observing outputs, not under a blinded annotation protocol. A larger preregistered experiment is needed before claiming language parity.

## Reproducibility

Never commit an API key. Set `GEMINI_API_KEY` through an environment variable or Colab Secrets. Model outputs may vary even with temperature zero. Retain raw data independently of semantic annotations.

**Suggested citation:** Khosravi, M. (2026). *Persian–English Tool-Calling Probe: A 30-Trial Exploratory Evaluation of Gemini 3.1 Flash Lite*. Research data and code.
