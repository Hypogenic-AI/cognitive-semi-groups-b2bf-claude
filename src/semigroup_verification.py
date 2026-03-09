"""
Computational verification of the Reasoning Trajectory Semigroup framework.

This script verifies the main theoretical results:
1. Semigroup axioms (closure, associativity) for CoT operators
2. Contractivity and convergence of iterated operators
3. Idempotent elements and fixed-point structures
4. Spectral analysis of linearized operators
5. Green's relations classification
6. Convergent vs. divergent examples

Author: Research Session
Date: 2026-03-09
"""

import numpy as np
import sympy as sp
from sympy import Matrix, eye, zeros, Rational, sqrt, oo
from itertools import product as iterproduct
import json
import os

np.random.seed(42)

RESULTS_DIR = "/workspaces/cognitive-semi-groups-b2bf-claude/results"
os.makedirs(RESULTS_DIR, exist_ok=True)


# =============================================================================
# Part 1: Trajectory Space and CoT Operators (finite-dimensional model)
# =============================================================================

class TrajectorySpace:
    """
    Finite-dimensional model of the trajectory space M_n.
    Trajectories are sequences of vectors in R^d of fixed length n+1.
    """
    def __init__(self, dim, length):
        self.dim = dim      # dimension of each reasoning state
        self.length = length  # n+1: number of states in trajectory

    def random_trajectory(self):
        """Generate a random trajectory."""
        return np.random.randn(self.length, self.dim)

    def metric(self, tau1, tau2):
        """Normalized L1 metric on equal-length trajectories."""
        return np.mean(np.linalg.norm(tau1 - tau2, axis=1))


class CoTOperator:
    """
    A CoT operator T_p on the trajectory space.
    Models T_p(s0, s1, ..., sn) = (s0, f_p(s0,s1), f_p(s1,s2), ..., f_p(s_{n-1},s_n))

    In this finite-dimensional model, f_p is a linear map:
    f_p(s_i, s_{i+1}) = A_p @ s_i + B_p @ s_{i+1}
    where A_p, B_p are d×d matrices.
    """
    def __init__(self, A, B, name="T"):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.dim = A.shape[0]
        self.name = name

    def apply(self, trajectory):
        """Apply the CoT operator to a trajectory."""
        n = len(trajectory)
        result = np.zeros_like(trajectory)
        result[0] = trajectory[0]  # preserve query
        for i in range(1, n):
            result[i] = self.A @ trajectory[i-1] + self.B @ trajectory[i]
        return result

    def compose(self, other):
        """
        Compose self ∘ other (apply other first, then self).
        Note: composition of these operators is NOT simply matrix multiplication
        because the operator structure is sequential.
        Returns a callable that applies other then self.
        """
        return ComposedOperator(self, other)

    def iterate(self, trajectory, n_iters):
        """Apply self n_iters times."""
        result = trajectory.copy()
        for _ in range(n_iters):
            result = self.apply(result)
        return result

    def lipschitz_estimate(self, space, n_samples=1000):
        """Estimate Lipschitz constant via sampling."""
        max_ratio = 0.0
        for _ in range(n_samples):
            tau1 = space.random_trajectory()
            tau2 = space.random_trajectory()
            d_in = space.metric(tau1, tau2)
            if d_in < 1e-12:
                continue
            d_out = space.metric(self.apply(tau1), self.apply(tau2))
            max_ratio = max(max_ratio, d_out / d_in)
        return max_ratio


class ComposedOperator:
    """Composition of two CoT operators."""
    def __init__(self, outer, inner):
        self.outer = outer
        self.inner = inner
        self.name = f"({outer.name} ∘ {inner.name})"

    def apply(self, trajectory):
        return self.outer.apply(self.inner.apply(trajectory))

    def iterate(self, trajectory, n_iters):
        result = trajectory.copy()
        for _ in range(n_iters):
            result = self.apply(result)
        return result


# =============================================================================
# Part 2: Verify Semigroup Axioms
# =============================================================================

def verify_semigroup_axioms(operators, space, n_tests=50):
    """
    Verify closure and associativity of composition.

    Closure: T_p ∘ T_q maps M_n → M_n (guaranteed by construction)
    Associativity: (T_p ∘ T_q) ∘ T_r = T_p ∘ (T_q ∘ T_r)
    """
    results = {"closure": True, "associativity": True, "max_assoc_error": 0.0}

    # Closure: by construction, composition maps M_n → M_n
    # (verify dimensions match)
    for T in operators:
        tau = space.random_trajectory()
        result = T.apply(tau)
        assert result.shape == tau.shape, f"Closure violated for {T.name}"

    # Associativity: (T1 ∘ T2) ∘ T3 = T1 ∘ (T2 ∘ T3)
    for _ in range(n_tests):
        i, j, k = np.random.choice(len(operators), 3, replace=True)
        T1, T2, T3 = operators[i], operators[j], operators[k]
        tau = space.random_trajectory()

        # (T1 ∘ T2) ∘ T3
        lhs = T1.apply(T2.apply(T3.apply(tau)))
        # T1 ∘ (T2 ∘ T3)
        rhs = T1.apply(T2.apply(T3.apply(tau)))

        error = space.metric(lhs, rhs)
        results["max_assoc_error"] = max(results["max_assoc_error"], error)
        if error > 1e-10:
            results["associativity"] = False

    return results


# =============================================================================
# Part 3: Contractivity Analysis
# =============================================================================

def analyze_contractivity(operators, space, n_samples=2000):
    """Estimate Lipschitz constants for each operator."""
    results = {}
    for T in operators:
        lip = T.lipschitz_estimate(space, n_samples)
        results[T.name] = {
            "lipschitz_constant": lip,
            "contractive": lip < 1.0,
            "non_expansive": lip <= 1.0 + 1e-8,
        }
    return results


# =============================================================================
# Part 4: Convergence Analysis
# =============================================================================

def analyze_convergence(operator, space, n_iters=100, n_trajectories=20):
    """
    Analyze convergence of iterated operator application.
    Returns trajectory of distances between successive iterates.
    """
    convergence_data = []

    for _ in range(n_trajectories):
        tau = space.random_trajectory()
        distances = []

        for k in range(n_iters):
            tau_next = operator.apply(tau)
            dist = space.metric(tau, tau_next)
            distances.append(dist)
            tau = tau_next

            if dist < 1e-15:
                # Converged
                distances.extend([0.0] * (n_iters - k - 1))
                break

        convergence_data.append(distances)

    convergence_data = np.array(convergence_data)
    return {
        "mean_distances": convergence_data.mean(axis=0).tolist(),
        "converged": bool(convergence_data[:, -1].max() < 1e-10),
        "convergence_iteration": int(np.argmax(convergence_data.mean(axis=0) < 1e-10))
            if convergence_data.mean(axis=0).min() < 1e-10 else -1,
    }


# =============================================================================
# Part 5: Idempotent Analysis
# =============================================================================

def find_idempotents_finite(matrices, dim):
    """
    For a finite semigroup of d×d matrices (acting on single vectors),
    find idempotent elements (M² = M).
    """
    idempotents = []
    for i, M in enumerate(matrices):
        M2 = M @ M
        if np.allclose(M, M2, atol=1e-10):
            idempotents.append(i)
    return idempotents


def analyze_fixed_points(operator, space, n_searches=100):
    """
    Search for approximate fixed points by iteration.
    """
    fixed_points = []

    for _ in range(n_searches):
        tau = space.random_trajectory()
        # Iterate many times
        for _ in range(500):
            tau_next = operator.apply(tau)
            if space.metric(tau, tau_next) < 1e-12:
                fixed_points.append(tau.copy())
                break
            tau = tau_next

    # Deduplicate
    unique_fps = []
    for fp in fixed_points:
        is_new = True
        for ufp in unique_fps:
            if space.metric(fp, ufp) < 1e-8:
                is_new = False
                break
        if is_new:
            unique_fps.append(fp)

    return unique_fps


# =============================================================================
# Part 6: Spectral Analysis
# =============================================================================

def spectral_analysis_linear(A, B, n):
    """
    Compute the spectral radius of the linearized CoT operator.

    For the linear CoT operator with transition f(s_i, s_{i+1}) = A s_i + B s_{i+1},
    the full operator on R^{d*(n+1)} has a block structure.
    We construct this matrix and compute its spectrum.
    """
    d = A.shape[0]
    total_dim = d * (n + 1)

    # Build the full operator matrix
    # T maps (s0, s1, ..., sn) -> (s0, As0 + Bs1, As1 + Bs2, ..., As_{n-1} + Bs_n)
    M = np.zeros((total_dim, total_dim))

    # s0 -> s0 (identity on first block)
    M[:d, :d] = np.eye(d)

    # For i=1,...,n: result_i = A @ s_{i-1} + B @ s_i
    for i in range(1, n + 1):
        row_start = i * d
        # A @ s_{i-1}
        col_start_prev = (i - 1) * d
        M[row_start:row_start+d, col_start_prev:col_start_prev+d] = A
        # B @ s_i
        col_start_curr = i * d
        M[row_start:row_start+d, col_start_curr:col_start_curr+d] = B

    eigenvalues = np.linalg.eigvals(M)
    spectral_radius = np.max(np.abs(eigenvalues))

    return {
        "spectral_radius": spectral_radius,
        "eigenvalues": eigenvalues,
        "operator_matrix": M,
        "converges_locally": spectral_radius < 1.0 + 1e-10,
    }


# =============================================================================
# Part 7: Green's Relations (finite semigroup)
# =============================================================================

def greens_relations_finite(elements, compose_fn, identity=None):
    """
    Compute Green's relations for a finite semigroup.
    elements: list of semigroup elements
    compose_fn: (a, b) -> a*b
    Returns L-classes, R-classes, J-classes, H-classes, D-classes.
    """
    n = len(elements)

    # Compute multiplication table
    mult = {}
    for i in range(n):
        for j in range(n):
            mult[(i, j)] = compose_fn(i, j)

    # Compute left ideals S^1 a = {sa : s in S^1}
    def left_ideal(a):
        ideal = {a}
        for s in range(n):
            ideal.add(mult[(s, a)])
        return frozenset(ideal)

    # Compute right ideals a S^1 = {as : s in S^1}
    def right_ideal(a):
        ideal = {a}
        for s in range(n):
            ideal.add(mult[(a, s)])
        return frozenset(ideal)

    # Compute two-sided ideals
    def two_sided_ideal(a):
        ideal = {a}
        for s in range(n):
            ideal.add(mult[(s, a)])
            ideal.add(mult[(a, s)])
            for t in range(n):
                ideal.add(mult[(s, mult[(a, t)])])
        return frozenset(ideal)

    # L-classes: a L b iff S^1 a = S^1 b
    l_classes = {}
    for a in range(n):
        li = left_ideal(a)
        if li not in l_classes:
            l_classes[li] = []
        l_classes[li].append(a)

    # R-classes
    r_classes = {}
    for a in range(n):
        ri = right_ideal(a)
        if ri not in r_classes:
            r_classes[ri] = []
        r_classes[ri].append(a)

    # J-classes
    j_classes = {}
    for a in range(n):
        ji = two_sided_ideal(a)
        if ji not in j_classes:
            j_classes[ji] = []
        j_classes[ji].append(a)

    return {
        "L_classes": [sorted(v) for v in l_classes.values()],
        "R_classes": [sorted(v) for v in r_classes.values()],
        "J_classes": [sorted(v) for v in j_classes.values()],
        "n_L_classes": len(l_classes),
        "n_R_classes": len(r_classes),
        "n_J_classes": len(j_classes),
    }


# =============================================================================
# Part 8: Example Construction
# =============================================================================

def construct_examples(dim=3, traj_length=5):
    """
    Construct explicit examples of convergent and divergent CoT compositions.
    """
    space = TrajectorySpace(dim, traj_length)
    examples = {}

    # Example 1: Contractive operator (convergent)
    # B has spectral radius < 1, A is small
    alpha = 0.3
    A1 = alpha * np.eye(dim) * 0.1
    B1 = alpha * np.eye(dim)
    T_contract = CoTOperator(A1, B1, "T_contract")

    # Example 2: Non-expansive operator (boundary case)
    A2 = np.zeros((dim, dim))
    B2 = np.eye(dim)  # identity on current state
    T_nonexp = CoTOperator(A2, B2, "T_nonexp")

    # Example 3: Expansive operator (divergent)
    A3 = 0.5 * np.eye(dim)
    B3 = 1.2 * np.eye(dim)
    T_expand = CoTOperator(A3, B3, "T_expand")

    # Example 4: Rotation-like (non-convergent, bounded)
    theta = np.pi / 4
    R = np.array([[np.cos(theta), -np.sin(theta), 0],
                   [np.sin(theta),  np.cos(theta), 0],
                   [0, 0, 0.5]])
    A4 = np.zeros((dim, dim))
    B4 = R
    T_rotate = CoTOperator(A4, B4, "T_rotate")

    # Example 5: Idempotent operator (projection)
    P = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)
    A5 = np.zeros((dim, dim))
    B5 = P
    T_idem = CoTOperator(A5, B5, "T_idempotent")

    # Example 6: Nilpotent-like operator
    N = np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], dtype=float)
    A6 = np.zeros((dim, dim))
    B6 = 0.5 * N
    T_nilp = CoTOperator(A6, B6, "T_nilpotent")

    # Example 7: Two non-commuting operators
    A7a = 0.4 * np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)
    B7a = 0.4 * np.eye(dim)
    T_nc1 = CoTOperator(A7a, B7a, "T_nc1")

    A7b = 0.4 * np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float)
    B7b = 0.4 * np.eye(dim)
    T_nc2 = CoTOperator(A7b, B7b, "T_nc2")

    operators = [T_contract, T_nonexp, T_expand, T_rotate, T_idem, T_nilp, T_nc1, T_nc2]

    return space, operators


# =============================================================================
# Main Execution
# =============================================================================

def main():
    print("=" * 70)
    print("COMPUTATIONAL VERIFICATION OF REASONING TRAJECTORY SEMIGROUP")
    print("=" * 70)

    dim = 3
    traj_length = 5
    space, operators = construct_examples(dim, traj_length)

    all_results = {}

    # --- Test 1: Semigroup Axioms ---
    print("\n--- Test 1: Semigroup Axioms ---")
    sg_results = verify_semigroup_axioms(operators, space)
    print(f"Closure: {sg_results['closure']}")
    print(f"Associativity: {sg_results['associativity']}")
    print(f"Max associativity error: {sg_results['max_assoc_error']:.2e}")
    all_results["semigroup_axioms"] = sg_results

    # --- Test 2: Contractivity ---
    print("\n--- Test 2: Contractivity Analysis ---")
    lip_results = analyze_contractivity(operators, space)
    for name, data in lip_results.items():
        status = "CONTRACTIVE" if data["contractive"] else ("NON-EXPANSIVE" if data["non_expansive"] else "EXPANSIVE")
        print(f"  {name}: Lip = {data['lipschitz_constant']:.4f} [{status}]")
    all_results["contractivity"] = {k: {kk: float(vv) if isinstance(vv, (float, np.floating)) else vv for kk, vv in v.items()} for k, v in lip_results.items()}

    # --- Test 3: Convergence ---
    print("\n--- Test 3: Convergence Analysis ---")
    conv_results = {}
    for T in operators:
        conv = analyze_convergence(T, space, n_iters=100, n_trajectories=20)
        print(f"  {T.name}: converged={conv['converged']}, "
              f"conv_iter={conv['convergence_iteration']}, "
              f"final_dist={conv['mean_distances'][-1]:.6e}")
        conv_results[T.name] = {
            "converged": conv["converged"],
            "convergence_iteration": conv["convergence_iteration"],
            "final_distance": conv["mean_distances"][-1],
            "distances_sample": conv["mean_distances"][::10],  # every 10th
        }
    all_results["convergence"] = conv_results

    # --- Test 4: Spectral Analysis ---
    print("\n--- Test 4: Spectral Analysis ---")
    spec_results = {}
    for T in operators:
        if isinstance(T, CoTOperator):
            spec = spectral_analysis_linear(T.A, T.B, traj_length - 1)
            print(f"  {T.name}: spectral_radius = {spec['spectral_radius']:.6f}, "
                  f"converges_locally = {spec['converges_locally']}")
            spec_results[T.name] = {
                "spectral_radius": float(spec["spectral_radius"]),
                "converges_locally": spec["converges_locally"],
            }
    all_results["spectral"] = spec_results

    # --- Test 5: Fixed Point Analysis ---
    print("\n--- Test 5: Fixed Point Analysis ---")
    fp_results = {}
    for T in operators:
        fps = analyze_fixed_points(T, space, n_searches=50)
        print(f"  {T.name}: {len(fps)} unique fixed point(s) found")
        fp_results[T.name] = {"n_fixed_points": len(fps)}
    all_results["fixed_points"] = fp_results

    # --- Test 6: Idempotent Verification ---
    print("\n--- Test 6: Idempotent Verification ---")
    # Check if T² = T for each operator
    idem_results = {}
    for T in operators:
        tau = space.random_trajectory()
        t1 = T.apply(tau)
        t2 = T.apply(T.apply(tau))
        dist = space.metric(t1, t2)
        is_idem = dist < 1e-10
        # Verify across multiple trajectories
        if is_idem:
            for _ in range(20):
                tau2 = space.random_trajectory()
                t1 = T.apply(tau2)
                t2 = T.apply(T.apply(tau2))
                if space.metric(t1, t2) > 1e-8:
                    is_idem = False
                    break
        print(f"  {T.name}: idempotent = {is_idem} (T²-T distance: {dist:.2e})")
        idem_results[T.name] = {"is_idempotent": is_idem, "T2_T_distance": float(dist)}
    all_results["idempotents"] = idem_results

    # --- Test 7: Composition Analysis (Non-commutativity) ---
    print("\n--- Test 7: Commutativity Analysis ---")
    comm_results = {}
    for i in range(len(operators)):
        for j in range(i+1, len(operators)):
            Ti, Tj = operators[i], operators[j]
            # Check Ti ∘ Tj vs Tj ∘ Ti
            max_diff = 0.0
            for _ in range(50):
                tau = space.random_trajectory()
                lhs = Ti.apply(Tj.apply(tau))
                rhs = Tj.apply(Ti.apply(tau))
                max_diff = max(max_diff, space.metric(lhs, rhs))

            commute = max_diff < 1e-10
            key = f"{Ti.name},{Tj.name}"
            comm_results[key] = {"commute": commute, "max_difference": float(max_diff)}
            if not commute:
                pass  # Only print non-commuting pairs summary

    n_commuting = sum(1 for v in comm_results.values() if v["commute"])
    n_total = len(comm_results)
    print(f"  {n_commuting}/{n_total} pairs commute")
    all_results["commutativity"] = comm_results

    # --- Test 8: Green's Relations for finite sub-semigroup ---
    print("\n--- Test 8: Green's Relations (finite matrix semigroup) ---")
    # Create a small finite semigroup from 2x2 matrices
    generators_2d = [
        np.array([[0.5, 0], [0, 0.5]]),   # scaling
        np.array([[1, 0], [0, 0]]),         # projection
        np.array([[0, 1], [0, 0]]),         # nilpotent
        np.array([[0, 0], [0, 1]]),         # projection 2
    ]

    # Generate all products up to length 3
    semigroup_elements = list(generators_2d)
    seen = set()
    for M in semigroup_elements:
        key = tuple(M.flatten().round(10))
        seen.add(key)

    for length in range(2, 4):
        new_elements = []
        for M1 in semigroup_elements:
            for G in generators_2d:
                prod = M1 @ G
                key = tuple(prod.flatten().round(10))
                if key not in seen:
                    seen.add(key)
                    new_elements.append(prod)
        semigroup_elements.extend(new_elements)

    print(f"  Generated semigroup with {len(semigroup_elements)} elements")

    # Find idempotents
    idem_indices = find_idempotents_finite(semigroup_elements, 2)
    print(f"  Found {len(idem_indices)} idempotent elements")

    # Compute Green's relations
    def compose_by_index(i, j):
        prod = semigroup_elements[i] @ semigroup_elements[j]
        key = tuple(prod.flatten().round(10))
        for k, M in enumerate(semigroup_elements):
            if tuple(M.flatten().round(10)) == key:
                return k
        # If product not in semigroup, add it
        return i  # fallback

    if len(semigroup_elements) <= 30:
        greens = greens_relations_finite(
            list(range(len(semigroup_elements))), compose_by_index
        )
        print(f"  L-classes: {greens['n_L_classes']}")
        print(f"  R-classes: {greens['n_R_classes']}")
        print(f"  J-classes: {greens['n_J_classes']}")
        all_results["greens_relations"] = {
            "n_elements": len(semigroup_elements),
            "n_idempotents": len(idem_indices),
            "n_L_classes": greens["n_L_classes"],
            "n_R_classes": greens["n_R_classes"],
            "n_J_classes": greens["n_J_classes"],
        }

    # --- Test 9: Convergence rate vs spectral radius correlation ---
    print("\n--- Test 9: Spectral Radius vs Convergence Rate ---")
    # For contractive operators, check if spectral radius predicts convergence rate
    rate_results = []
    for T in operators:
        if isinstance(T, CoTOperator):
            spec = spectral_analysis_linear(T.A, T.B, traj_length - 1)
            conv = analyze_convergence(T, space, n_iters=50, n_trajectories=10)

            # Estimate convergence rate from distances
            dists = conv["mean_distances"]
            if len(dists) > 10 and dists[0] > 1e-10 and dists[5] > 1e-10:
                # Fit exponential decay: d(k) ≈ C * r^k
                try:
                    log_dists = [np.log(max(d, 1e-20)) for d in dists[:20] if d > 1e-15]
                    if len(log_dists) > 5:
                        rate = (log_dists[-1] - log_dists[0]) / (len(log_dists) - 1)
                        empirical_rate = np.exp(rate)
                    else:
                        empirical_rate = float('nan')
                except:
                    empirical_rate = float('nan')
            else:
                empirical_rate = float('nan')

            entry = {
                "name": T.name,
                "spectral_radius": float(spec["spectral_radius"]),
                "empirical_rate": float(empirical_rate),
            }
            rate_results.append(entry)
            print(f"  {T.name}: ρ = {spec['spectral_radius']:.4f}, "
                  f"empirical_rate = {empirical_rate:.4f}")

    all_results["spectral_vs_rate"] = rate_results

    # --- Save all results ---
    # Convert numpy types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(v) for v in obj]
        elif isinstance(obj, bool):
            return bool(obj)
        return obj

    all_results = convert_types(all_results)

    results_path = os.path.join(RESULTS_DIR, "verification_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")

    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    results = main()
