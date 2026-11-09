# Changelog

## Unreleased

- `n8n/`: failure 1 rebuilt in n8n Agents and run on a real model, 60 runs on
  `openai/gpt-4.1` across three setups and two rounds. Ships the guard
  workflow, the three agent configs, the data table rows, the protocol and the
  raw run log, so it can be reproduced. `harness.py` is unchanged.

## 0.1.0

First release, published alongside the article.

- `boundary(rules, max_repeats=3)` — refuse calls before they execute. Works on
  sync and async `execute`; an async loop used to receive an un-awaited
  coroutine, which is a guard that silently does nothing.
- `Denied` — refusals are a `str` subclass carrying `.rule`, so existing loops
  keep working while `isinstance(r, Denied)` replaces matching on text.
- `.denials` on the wrapped function — refusal counts per rule, for your metrics.
- `allowlist(roots)` — normalise the path, then check it.
- `host_allowlist(hosts)` — the network half. Compares the parsed hostname, so
  `api.openai.com.evil.com` and `evil.com/?x=api.openai.com` are both refused.
- `Store` — three destinations, named at write time; `reset()` clears only chat.
- `read_only`, `dry_run` — the reviewer gets a copy, irreversible tools describe
  themselves unless the flag is turned off on purpose.
- `Distiller` — counts what the subagent read against what the main thread paid for.
- Type hints throughout, `py.typed`, Python 3.8+.
