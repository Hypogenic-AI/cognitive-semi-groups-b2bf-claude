# Literature Review: Algebraic Structure of Chain-of-Thought Prompt Composition and Convergence in Reasoning Trajectory Semigroups

## Research Area Overview

This research sits at the intersection of three mathematical areas: (1) **operator semigroup theory** on Banach/metric spaces, (2) **formal frameworks for transformer/prompt computation**, and (3) **fixed-point theory and contraction mappings**. The central hypothesis is that CoT prompt transformations form a semigroup under composition, and that algebraic properties (idempotency, commutativity, contractivity) characterize convergence to fixed-point reasoning patterns.

No prior work has explicitly constructed a semigroup-theoretic framework for CoT prompt composition. However, substantial mathematical infrastructure exists across these three areas that can be synthesized to build such a framework.

---

## Key Definitions

**Definition 1 (Semigroup).** A non-empty set S with an associative binary operation is a semigroup. If there exists e ∈ S with es = se = s for all s, it is a monoid. [Gluck & Haase, 2018]

**Definition 2 (Operator Semigroup).** A family T = (T_s)_{s ∈ S} of bounded linear operators on a Banach space E, where T_{s+t} = T_s ∘ T_t, forming a semigroup homomorphism S → L(E). [Gerlach & Gluck, 2017]

**Definition 3 (Semigroup at Infinity).** For a bounded operator semigroup T on E, T_∞ := ∩_{s ∈ S} cl_SOT{T_t : t ≥ s}, the set of SOT-cluster points of the net (T_s). [Gluck & Haase, 2018]

**Definition 4 (Prompt-Induced Hypothesis Class).** For a fixed backbone θ*, H_{θ*} := {F_{θ*}(p, ·) : p ∈ P} ⊂ C(X), the family of all functions realizable by varying the prompt alone. [Kim et al., 2025]

**Definition 5 (Prompt-UAT Property).** A fixed backbone θ* satisfies Prompt-UAT if cl(H_{θ*}) = C(X) in the sup-norm, i.e., prompts can approximate any continuous function. [Kim et al., 2025]

**Definition 6 (Improvement Operator).** An LLM M_θ viewed as an operator: s_{t+1} ← M_θ(x, s_t, C_t), mapping task x, current artifact s_t, and workspace C_t to a refined artifact. [Yang et al., 2025]

**Definition 7 (Schur Holomorphic Function on a Spectrum).** A function p on σ(A) satisfying: sup|p(λ)| ≤ 1, p(1) = 1, and for |λ| = 1, |p(λ)| = 1 ⟹ p(λ) = λ (peripheral fixed-point property). [Badea et al., 2025]

**Definition 8 (AM-Compact Operator).** T: E → F on a Banach lattice is AM-compact if T maps order intervals to relatively compact sets. [Gerlach & Gluck, 2017]

**Definition 9 (Ritt Operator).** A power-bounded operator A on a Banach space with σ(A) ⊆ D̄ and sup_{|z|>1}(|z|-1)‖(zI-A)^{-1}‖ < ∞. Admits a bounded H^∞ functional calculus. [Badea et al., 2025]

---

## Key Papers

### Paper 1: Theoretical Foundations of Prompt Engineering (Kim et al., arXiv 2512.12688, 2025)
- **Main Results:** Prompt-UAT theorem showing that a fixed transformer backbone, with sufficiently large architecture, can approximate any continuous function by varying only the prompt. Proved via a two-stage strategy: (1) approximate target by ReLU MLP, (2) construct executor that emulates MLP from prompt parameters.
- **Proof Techniques:** Routing Lemma (softmax concentration), Arithmetic Lemma (FFN approximation), Composition Lemma (error accumulation under Lipschitz maps: ‖G̃_{1:T}(z) - G_{1:T}(z)‖ ≤ Σ_t ε_t ∏_{s>t} L_s).
- **Relevance:** Provides the formal foundation for defining prompt operators. The Composition Lemma directly governs convergence of iterated prompt operators. When Lipschitz constants K_t ≤ 1, errors accumulate additively (boundary of contraction). The macro-step structure s_{t+1} = Ψ_t(s_t, λ_t(p)) is a controlled dynamical system amenable to semigroup analysis.
- **Gap:** No algebraic structure (composition, identity) explicitly defined on prompts. No semigroup axioms verified.

### Paper 2: A Mathematical Perspective on Transformers (Geshkovski et al., arXiv 2312.10794, 2023/2025)
- **Main Results:** Transformer layers modeled as a nonlinear one-parameter semigroup of flow maps Φ_t: P(S^{d-1}) → P(S^{d-1}). As depth t → ∞, tokens cluster to a single point (Theorem 4.1: consensus for β = 0). The interaction energy E_β is a Lyapunov function monotonically increasing along the flow.
- **Proof Techniques:** Gradient flow structure on (S^{d-1})^n with modified Wasserstein metric. Łojasiewicz theorem for convergence to critical points. Dobrushin-type stability estimates: W_1(μ_n(t), μ(t)) ≤ exp(O(1)|t|) W_1(μ_n(0), μ(0)).
- **Relevance:** Provides rigorous treatment of transformer computation as a semigroup. The clustering result (convergence to Dirac masses) is an idempotent-like fixed point. The gradient flow structure with Wasserstein metric is directly applicable to reasoning trajectory analysis. Exponential convergence rate when d ≥ n (Theorem 6.3).
- **Gap:** Focuses on self-attention dynamics, not on prompt composition or CoT-specific structures.

### Paper 3: Asymptotics of Operator Semigroups via the Semigroup at Infinity (Gluck & Haase, arXiv 1811.07955, 2018)
- **Main Results:** Fundamental theorem (Thm 2.2): When T_∞ is strongly compact and non-empty, JdLG theory yields a unique minimal idempotent P_∞, decomposing E = E_∞ ⊕ ker(P_∞). Strong convergence iff T_∞ is a singleton (Cor 2.3). Quasi-compactness ensures T_∞ is non-empty and compact (Thm 3.1).
- **Proof Techniques:** Jacobs-de Leeuw-Glicksberg decomposition, universal subnets, spectral theory of compact semitopological semigroups.
- **Relevance:** Core mathematical framework for our research. The characterization of convergence via idempotent elements in T_∞ directly maps to our hypothesis about CoT convergence to fixed-point reasoning patterns. The JdLG decomposition (reversible part + stable part) could correspond to (stable reasoning patterns + transient reasoning noise).

### Paper 4: Convergence of Positive Operator Semigroups (Gerlach & Gluck, arXiv 1705.01587, 2017)
- **Main Results:** Strong convergence for positive bounded semigroups containing an AM-compact operator with quasi-interior fixed point (Thm 3.5). Extension to semigroups dominating AM-compact operators (Thm 3.9). Spectral characterization: convergence iff no non-constant torsion eigenvalue (Thm 6.1).
- **Proof Techniques:** Three-layer architecture: (1) Algebraic: divisible groups have only trivial positive representations on atomic lattices (Thm 2.2). (2) Splitting: JdLG decomposition. (3) Compactness: AM-compactness forces atomicity of the reversible part.
- **Relevance:** Provides sufficient conditions for semigroup convergence that could be verified for reasoning operators. The requirement of a "quasi-interior fixed point" may correspond to a baseline coherent reasoning pattern.

### Paper 5: Transfinite Iteration of Operator Transforms (Badea et al., arXiv 2508.06025, 2025)
- **Main Results:** Iterative application of holomorphic operator transforms converges in SOT to an idempotent (projection) that commutes with the operator (Thm 2.1). Convergence via Denjoy-Wolff theorem for holomorphic self-maps of D. Stabilization at ordinal stage ω (Prop .10). Banach-space extension via mean ergodic theorem and Katznelson-Tzafriri theorem (Thm 3.1).
- **Proof Techniques:** Normal functional calculus, Denjoy-Wolff theorem, Julia-Wolff-Carathéodory theorem, Schwarz-Pick contraction, H^∞ calculus for Ritt operators.
- **Relevance:** Most directly relevant to our algebraic hypothesis. Shows that iterated composition of contractive transforms converges to idempotent projections — exactly the mechanism we hypothesize for CoT convergence. The requirement that layers commute (via functional calculus of a common operator) is essential; non-commuting layers can destroy convergence (Example 4.5). The peripheral fixed-point property ensures the limit is a genuine projection.

### Paper 6: Rethinking Thinking Tokens: LLMs as Improvement Operators (Yang et al., arXiv 2510.01123, 2025)
- **Main Results:** LLMs modeled as improvement operators with iterative refinement dynamics. Sequential Refinement (SR) and Parallel-Distill-Refine (PDR) as operator instantiations. Empirical monotone improvement with saturation. Connection to space-bounded computation.
- **Relevance:** Provides the concrete LLM operator framework that our algebraic theory aims to formalize. Shows empirical convergence (accuracy saturation) and failure modes (anchoring bias, summary drift = non-convergence). The bounded workspace constraint |C_t| ≤ κ is a finite-dimensional projection that could be modeled as a contractive operation.

### Paper 7: On the Contraction Properties of Sinkhorn Semigroups (Akyildiz et al., arXiv 2503.09887, 2025)
- **Main Results:** Lyapunov-based stability theory for Sinkhorn semigroups with exponential convergence on weighted Banach spaces. Contraction inequalities for φ-divergences and Kantorovich/Wasserstein distances. Drift-minorization conditions for quantitative convergence rates.
- **Relevance:** Provides proof technique templates for establishing contraction properties of reasoning operator semigroups. The Lyapunov approach (drift condition + local minorization) is directly applicable. The weighted Banach space framework handles unbounded state spaces relevant to token embedding spaces.

---

## Known Results (Prerequisite Theorems)

| Result | Source | Used For |
|--------|--------|----------|
| Banach Fixed-Point Theorem | Classical | Contraction maps on complete metric spaces have unique fixed points |
| JdLG Decomposition | Jacobs/de Leeuw/Glicksberg | Splitting semigroup orbits into reversible and stable parts |
| Denjoy-Wolff Theorem | Classical complex analysis | Iteration of holomorphic self-maps of D converges to boundary/interior fixed point |
| Prompt-UAT | Kim et al. 2025 | Fixed transformer can approximate any continuous function via prompts |
| Composition Lemma | Kim et al. 2025 | Error bound: ‖G̃_{1:T} - G_{1:T}‖ ≤ Σ_t ε_t ∏_{s>t} L_s |
| Convergence to idempotent | Badea et al. 2025 | Iterated Schur transforms converge to spectral projections |
| Positive semigroup convergence | Gerlach & Gluck 2017 | AM-compact + quasi-interior fixed point ⟹ strong convergence |
| Transformer clustering | Geshkovski et al. 2023 | Deep transformers converge to consensus (single cluster) |
| Mean Ergodic Theorem | Von Neumann/Yosida | Cesaro averages converge for power-bounded operators on reflexive spaces |
| Katznelson-Tzafriri Theorem | 1986 | ‖T^n(I-T)‖ → 0 for power-bounded T with σ(T) ∩ T ⊆ {1} |

---

## Proof Techniques in the Literature

1. **JdLG + Algebraic Triviality:** Decompose via JdLG, then show group action on reversible part is trivial (using divisibility). Used in [Gerlach & Gluck 2017, Gluck & Haase 2018].

2. **Denjoy-Wolff + Functional Calculus:** Iterate holomorphic maps on the disk, lift to operator level via functional calculus. Convergence to {0,1}-valued functions yields idempotent projections. Used in [Badea et al. 2025].

3. **Lyapunov + Drift-Minorization:** Construct Lyapunov function satisfying drift condition, establish local minorization on sublevel sets, derive exponential contraction on weighted Banach spaces. Used in [Akyildiz et al. 2025].

4. **Gradient Flow / Energy Methods:** Model dynamics as gradient flow of energy functional on Wasserstein space. Monotonicity of energy + Łojasiewicz inequality yields convergence. Used in [Geshkovski et al. 2023].

5. **Lipschitz Composition Bounds:** Track error propagation through composed operators via Lipschitz constants. When K_t < 1 (contraction), errors decay; when K_t = 1, errors accumulate additively. Used in [Kim et al. 2025].

---

## Related Open Problems

1. **Algebraic closure of prompt operators:** Does the set {T_p : p ∈ P}, where T_p is the operator induced by prompt p, form a semigroup under composition? What is the algebraic structure of its closure?

2. **Commutativity conditions for CoT convergence:** Under what conditions do CoT prompt operators commute (or approximately commute), and how does this relate to convergence? (Non-commuting layers can destroy convergence [Badea et al. 2025, Ex. 4.5].)

3. **Characterization of idempotent reasoning patterns:** If iterated CoT application converges to an idempotent, what is the structure of the resulting "stable reasoning framework"? Does it correspond to the spectral projection onto peripheral fixed points?

4. **Rate of convergence:** Can explicit convergence rates be established for CoT iteration, analogous to the exponential rates in [Akyildiz et al. 2025] or [Geshkovski et al. 2023, Thm 6.3]?

5. **Failure mode characterization:** When does CoT iteration fail to converge (cf. anchoring bias, summary drift in [Yang et al. 2025])? Can this be characterized algebraically as absence of contractivity or violation of commutativity?

---

## Gaps and Opportunities

1. **No existing semigroup framework for prompt composition.** All prior work treats prompts either as static objects (expressivity theory) or as empirical iteration (improvement operators). Our research fills this gap.

2. **Commutativity is crucial but unexplored for prompts.** Badea et al. show non-commuting layers destroy convergence, but no one has studied commutativity of CoT prompt operators.

3. **Contraction properties of LLM operators are empirical only.** Yang et al. observe convergence empirically but provide no formal contraction bounds. Our framework can provide these.

4. **Bridge between measure-theoretic and algebraic views.** Geshkovski et al. work in P(S^{d-1}) with Wasserstein metric; Gluck & Haase work with operator semigroups on Banach spaces. Our research can unify these via the reasoning trajectory semigroup.

---

## Recommendations for Proof Strategy

1. **Define the reasoning trajectory semigroup:** Let (M, d) be a metric space of reasoning trajectories (token sequences or embedding sequences). Define T_p: M → M as the operator induced by prompt p (one step of CoT). The set S = {T_{p_n} ∘ ⋯ ∘ T_{p_1} : p_i ∈ P, n ≥ 0} forms a semigroup under composition.

2. **Establish contractivity:** Show that under appropriate conditions on prompts, T_p is a contraction (d(T_p(x), T_p(y)) ≤ α·d(x,y), α < 1) or at least non-expansive (α ≤ 1). Use the Lipschitz bounds from Kim et al.'s Composition Lemma.

3. **Apply JdLG decomposition:** If the semigroup is bounded and orbits are relatively compact, apply JdLG to decompose the trajectory space into reversible (stable reasoning patterns) and stable (transient noise) components.

4. **Characterize idempotent fixed points:** Show that the minimal idempotent P_∞ in the semigroup at infinity corresponds to a "stable logical framework" — a fixed-point reasoning pattern that is invariant under further CoT application.

5. **Use commutativity for convergence:** Identify conditions under which sub-operators commute (e.g., prompts addressing orthogonal aspects of reasoning). Show this commutativity, combined with contractivity, yields convergence via the Badea et al. framework.

6. **Computational verification:** Use SymPy for algebraic verification of semigroup properties in finite-dimensional examples. Use NetworkX for graph-based reasoning trajectory analysis.
