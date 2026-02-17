# Cursor Performance Optimization Mode

Purpose:
Identify and fix performance bottlenecks safely.

Rules:
- Measure before changing (profiling, metrics, benchmarks).
- Avoid premature optimization.
- Make targeted changes and validate improvements.
- Ensure no regression in correctness or resource leaks.
- Include measurements in PR to justify changes.

Workflow:
1. Reproduce the performance issue and collect baseline metrics.
2. Identify hotspots with profiling tools.
3. Propose minimal focused optimizations.
4. Implement and measure improvement.
5. Add regression tests or benchmarks if relevant.
