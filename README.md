# Algebraic Structure of Chain-of-Thought Prompt Composition

## Overview

This project develops a rigorous algebraic framework for chain-of-thought (CoT) prompt composition as a **semigroup of operators on a metric space of reasoning trajectories**. We prove that CoT operators form a monoid with explicit composition formulas, establish sharp convergence criteria via spectral analysis, and classify all possible convergence behaviors into four mutually exclusive cases.

## Key Results

- **Theorem 1 (Semigroup Structure):** CoT operators form a monoid under composition with formula T(A₂,B₂) ∘ T(A₁,B₁) = T(A₂+B₂A₁, B₂B₁).
- **Theorem 2 (Convergence Criterion):** Iteration converges iff the spectral radius ρ(B) < 1, with convergence rate O(ρ(B)^n).
- **Theorem 3 (Idempotent Characterization):** Idempotent CoT operators satisfy B² = B and BA = 0, corresponding to projections onto reasoning subspaces.
- **Theorem 4 (Classification):** Four exhaustive cases — contractive convergence, projective convergence, oscillation, and divergence.
- **Theorem 5 (JdLG Decomposition):** Reasoning trajectories decompose into stable reasoning patterns and transient noise.

## File Structure

```
├── REPORT.md              # Full research report with proofs
├── definitions.md         # Formal definitions and notation
├── planning.md            # Research plan
├── literature_review.md   # Literature review (pre-gathered)
├── resources.md           # Resource catalog (pre-gathered)
├── src/
│   ├── semigroup_verification.py   # Main computational verification
│   ├── symbolic_proofs.py          # Symbolic proof verification (SymPy)
│   └── visualizations.py           # Figure generation
├── results/
│   ├── verification_results.json   # Numerical experiment results
│   └── symbolic_verification.json  # Symbolic verification results
├── figures/
│   ├── convergence_analysis.png    # Convergence behavior comparison
│   ├── spectral_analysis.png       # Eigenvalue and spectral analysis
│   ├── composition_convergence.png # Commuting vs non-commuting composition
│   └── greens_structure.png        # Green's relations structure
└── papers/                         # Reference papers (PDFs)
```

## Reproducing Results

```bash
# Set up environment
uv venv && source .venv/bin/activate
uv add sympy numpy scipy matplotlib networkx

# Run computational verification
python src/semigroup_verification.py

# Run symbolic proof verification
python src/symbolic_proofs.py

# Generate figures
python src/visualizations.py
```

## Dependencies

- Python ≥ 3.10
- NumPy, SciPy, SymPy, Matplotlib, NetworkX
