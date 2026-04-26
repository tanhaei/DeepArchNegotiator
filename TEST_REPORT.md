# Test report

Generated before packaging.

## Commands run

```bash
PYTHONPATH=src python -S -m unittest discover -s tests -v
PYTHONPATH=src python -S scripts/smoke_test.py
PYTHONPATH=src python -S experiments/run_all.py --out artifacts
```

## Results

- Unit tests: 3 tests passed.
- Smoke test: passed.
- Smoke-selected proposal: `gateway_event`.
- Accepted coupling delta: `0.08`.
- Direct DB coupling delta checked: `0.42`.
- Accepted latency: `12 ms`.
- Final hard violations: `0`.
- Adoption rate: `0.85`.
- Generated artifacts: ADR, traceability matrix, migration plan, test obligations, CSV tables, and SVG figures.
