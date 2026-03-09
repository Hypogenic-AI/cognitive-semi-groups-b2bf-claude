# Downloaded Papers

## Prompt/Transformer Theory

1. **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (wei2022_chain_of_thought_prompting.pdf)
   - Authors: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, et al.
   - Year: 2022
   - arXiv: 2201.11903
   - Why relevant: Foundational CoT paper; defines the reasoning paradigm we formalize

2. **Theoretical Foundations of Prompt Engineering: From Heuristics to Expressivity** (chen2025_theoretical_foundations_prompt_engineering.pdf)
   - Authors: Kim et al.
   - Year: 2025
   - arXiv: 2512.12688
   - Why relevant: Prompt-UAT theorem, Composition Lemma with Lipschitz error bounds, prompt-as-operator framework

3. **A Theoretical Framework for Prompt Engineering: Approximating Smooth Functions with Transformer Prompts** (wang2025_theoretical_framework_prompt_approximation.pdf)
   - Authors: Wang et al.
   - Year: 2025
   - arXiv: 2503.20561
   - Why relevant: Shows transformers can configure as "virtual" neural networks via prompts; EUAF activation function theory

4. **A Mathematical Perspective on Transformers** (castin2023_mathematical_perspective_transformers.pdf)
   - Authors: Geshkovski, Letrouit, Polyanskiy, Rigollet
   - Year: 2023 (updated 2025)
   - arXiv: 2312.10794
   - Why relevant: Transformer layers as one-parameter semigroup on P(S^{d-1}), clustering/convergence results, gradient flow structure

5. **Characterizing the Expressivity of Fixed-Precision Transformer Language Models** (barcelo2025_expressivity_fixed_precision_transformers.pdf)
   - Authors: Barcelo et al.
   - Year: 2025
   - arXiv: 2505.23623
   - Why relevant: Fixed-precision transformers = fragment of linear temporal logic; expressivity characterization

## Operator Semigroup Theory

6. **Asymptotics of Operator Semigroups via the Semigroup at Infinity** (gluck2018_asymptotics_operator_semigroups.pdf)
   - Authors: Jochen Gluck, Markus Haase
   - Year: 2018
   - arXiv: 1811.07955
   - Why relevant: Core framework — JdLG decomposition, minimal idempotent P_∞, convergence characterization

7. **Convergence of Positive Operator Semigroups** (gerlach2017_convergence_positive_operator_semigroups.pdf)
   - Authors: Moritz Gerlach, Jochen Gluck
   - Year: 2017
   - arXiv: 1705.01587
   - Why relevant: AM-compact + quasi-interior fixed point ⟹ strong convergence; three-layer proof architecture

8. **Transfinite Iteration of Operator Transforms and Spectral Projections** (badea2025_transfinite_iteration_operator_transforms.pdf)
   - Authors: Catalin Badea et al.
   - Year: 2025
   - arXiv: 2508.06025
   - Why relevant: Iterated Schur transforms → idempotent projections; commutativity essential; Denjoy-Wolff convergence

9. **On the Contraction Properties of Sinkhorn Semigroups** (delMoral2025_contraction_sinkhorn_semigroups.pdf)
   - Authors: Akyildiz, Del Moral, Miguez
   - Year: 2025
   - arXiv: 2503.09887
   - Why relevant: Lyapunov contraction principles, drift-minorization, exponential stability on weighted Banach spaces

## LLM Reasoning Dynamics

10. **Rethinking Thinking Tokens: LLMs as Improvement Operators** (yang2025_rethinking_thinking_tokens_improvement_operators.pdf)
    - Authors: Yang et al.
    - Year: 2025
    - arXiv: 2510.01123
    - Why relevant: LLM as operator s_{t+1} = M_θ(x, s_t, C_t); SR and PDR dynamics; empirical convergence/failure modes

11. **The Evolution of Thought: Tracking LLM Overthinking via Reasoning Dynamics Analysis** (liu2025_evolution_of_thought_reasoning_dynamics.pdf)
    - Authors: Liu et al.
    - Year: 2025
    - arXiv: 2508.17627
    - Why relevant: Semantic path convergence in reasoning; overthinking as post-convergence token generation

12. **Landscape of Thoughts: Visualizing the Reasoning Process of Large Language Models** (wu2025_landscape_of_thoughts.pdf)
    - Authors: Wu et al.
    - Year: 2025
    - arXiv: 2503.22165
    - Why relevant: Convergence visualization; relationship between model scale and convergence speed

13. **Syzygy of Thoughts: Improving LLM CoT with the Minimal Free Resolution** (li2025_syzygy_of_thoughts.pdf)
    - Authors: Li et al.
    - Year: 2025
    - arXiv: (SoT paper)
    - Why relevant: Uses algebraic geometry (minimal free resolutions, Betti numbers) to structure CoT decomposition

14. **Dual Filter: A Mathematical Framework for Inference using Transformer-like Architectures** (chen2025_dual_filter_transformer_inference.pdf)
    - Authors: Chen et al.
    - Year: 2025
    - arXiv: 2505.00818
    - Why relevant: Fixed-point equation for transformer inference; mean-field ODE perspective
