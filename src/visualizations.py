"""
Visualization of convergence dynamics for the Reasoning Trajectory Semigroup.
Generates figures for the research report.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json

np.random.seed(42)

FIGURES_DIR = "/workspaces/cognitive-semi-groups-b2bf-claude/figures"
RESULTS_DIR = "/workspaces/cognitive-semi-groups-b2bf-claude/results"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Import from verification module
import sys
sys.path.insert(0, "/workspaces/cognitive-semi-groups-b2bf-claude/src")
from semigroup_verification import (
    TrajectorySpace, CoTOperator, construct_examples,
    analyze_convergence, spectral_analysis_linear
)


def plot_convergence_comparison():
    """Plot convergence behavior of different operator types."""
    dim, traj_length = 3, 5
    space, operators = construct_examples(dim, traj_length)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Convergent operators
    convergent_ops = [op for op in operators if op.name in
                      ["T_contract", "T_nc1", "T_nc2", "T_nilpotent"]]
    ax = axes[0, 0]
    for T in convergent_ops:
        conv = analyze_convergence(T, space, n_iters=60, n_trajectories=10)
        dists = conv["mean_distances"]
        ax.semilogy(range(len(dists)), [max(d, 1e-20) for d in dists], label=T.name, linewidth=2)
    ax.set_xlabel("Iteration k")
    ax.set_ylabel("d(T^k(τ), T^{k+1}(τ))")
    ax.set_title("Convergent Operators")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Divergent/bounded operators
    ax = axes[0, 1]
    for T in operators:
        if T.name in ["T_expand", "T_rotate"]:
            conv = analyze_convergence(T, space, n_iters=30, n_trajectories=5)
            dists = conv["mean_distances"]
            ax.plot(range(len(dists)), dists, label=T.name, linewidth=2)
    ax.set_xlabel("Iteration k")
    ax.set_ylabel("d(T^k(τ), T^{k+1}(τ))")
    ax.set_title("Divergent/Non-convergent Operators")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Idempotent behavior
    ax = axes[1, 0]
    for T in operators:
        if T.name in ["T_idempotent", "T_nonexp"]:
            conv = analyze_convergence(T, space, n_iters=10, n_trajectories=10)
            dists = conv["mean_distances"]
            ax.plot(range(len(dists)), dists, 'o-', label=T.name, linewidth=2)
    ax.set_xlabel("Iteration k")
    ax.set_ylabel("d(T^k(τ), T^{k+1}(τ))")
    ax.set_title("Idempotent Operators (T² = T)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Lipschitz constant vs convergence
    ax = axes[1, 1]
    lips = []
    conv_iters = []
    names = []
    for T in operators:
        lip = T.lipschitz_estimate(space, 500) if isinstance(T, CoTOperator) else None
        if lip is not None:
            conv = analyze_convergence(T, space, n_iters=100, n_trajectories=10)
            ci = conv["convergence_iteration"] if conv["converged"] else 100
            lips.append(lip)
            conv_iters.append(ci)
            names.append(T.name)

    colors = ['green' if c < 100 else 'red' for c in conv_iters]
    ax.scatter(lips, conv_iters, c=colors, s=100, zorder=5)
    for i, name in enumerate(names):
        ax.annotate(name, (lips[i], conv_iters[i]), textcoords="offset points",
                   xytext=(5, 5), fontsize=8)
    ax.axvline(x=1.0, color='black', linestyle='--', alpha=0.5, label='Lip=1 boundary')
    ax.set_xlabel("Lipschitz Constant")
    ax.set_ylabel("Convergence Iteration (100 = not converged)")
    ax.set_title("Lipschitz Constant vs. Convergence Speed")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "convergence_analysis.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: convergence_analysis.png")


def plot_spectral_analysis():
    """Plot eigenvalue distributions and convergence prediction."""
    dim, traj_length = 3, 5
    space, operators = construct_examples(dim, traj_length)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Eigenvalue plot (unit circle)
    ax = axes[0]
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Unit circle')

    colors = plt.cm.tab10(np.linspace(0, 1, len(operators)))
    for T, color in zip(operators, colors):
        if isinstance(T, CoTOperator):
            # Get eigenvalues of the sub-operator (excluding preserved s₀)
            n = traj_length - 1
            d = T.A.shape[0]
            total_dim = d * n
            M_sub = np.zeros((total_dim, total_dim))
            for i in range(n):
                row_start = i * d
                if i > 0:
                    col_start_prev = (i - 1) * d
                    M_sub[row_start:row_start+d, col_start_prev:col_start_prev+d] = T.A
                col_start_curr = i * d
                M_sub[row_start:row_start+d, col_start_curr:col_start_curr+d] = T.B

            eigs = np.linalg.eigvals(M_sub)
            ax.scatter(eigs.real, eigs.imag, c=[color], s=40, label=T.name, alpha=0.7)

    ax.set_xlabel("Re(λ)")
    ax.set_ylabel("Im(λ)")
    ax.set_title("Eigenvalues of Sub-operators (excl. query preservation)")
    ax.legend(fontsize=8, loc='upper left')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Spectral radius of sub-operator vs convergence
    ax = axes[1]
    for T in operators:
        if isinstance(T, CoTOperator):
            n = traj_length - 1
            d = T.A.shape[0]
            total_dim = d * n
            M_sub = np.zeros((total_dim, total_dim))
            for i in range(n):
                row_start = i * d
                if i > 0:
                    col_start_prev = (i - 1) * d
                    M_sub[row_start:row_start+d, col_start_prev:col_start_prev+d] = T.A
                col_start_curr = i * d
                M_sub[row_start:row_start+d, col_start_curr:col_start_curr+d] = T.B

            rho = max(abs(np.linalg.eigvals(M_sub)))

            conv = analyze_convergence(T, space, n_iters=80, n_trajectories=10)
            dists = conv["mean_distances"]
            # Plot convergence curve
            valid_dists = [max(d, 1e-20) for d in dists]
            ax.semilogy(range(len(valid_dists)), valid_dists,
                       label=f"{T.name} (ρ={rho:.3f})", linewidth=1.5)

    ax.set_xlabel("Iteration k")
    ax.set_ylabel("Mean distance d(T^k, T^{k+1})")
    ax.set_title("Convergence Curves with Sub-operator Spectral Radii")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "spectral_analysis.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: spectral_analysis.png")


def plot_composition_convergence():
    """Plot convergence of composed operators (commuting vs non-commuting)."""
    dim, traj_length = 3, 5
    space = TrajectorySpace(dim, traj_length)

    # Commuting contractive operators (diagonal)
    A1 = 0.1 * np.diag([1, 0, 0])
    B1 = np.diag([0.3, 0.4, 0.5])
    T1 = CoTOperator(A1, B1, "T_diag1")

    A2 = 0.1 * np.diag([0, 1, 0])
    B2 = np.diag([0.4, 0.3, 0.5])
    T2 = CoTOperator(A2, B2, "T_diag2")

    # Non-commuting contractive operators
    A3 = 0.1 * np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)
    B3 = 0.4 * np.array([[1, 0.5, 0], [0.5, 1, 0], [0, 0, 0.5]])
    T3 = CoTOperator(A3, B3, "T_noncomm1")

    A4 = 0.1 * np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float)
    B4 = 0.4 * np.array([[0.5, 0, 0.5], [0, 1, 0], [0.5, 0, 1]])
    T4 = CoTOperator(A4, B4, "T_noncomm2")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Alternating composition: T1 T2 T1 T2 ...
    ax = axes[0]
    ax.set_title("Commuting Operators: Alternating Composition")
    for _ in range(5):
        tau = space.random_trajectory()
        dists = []
        for k in range(60):
            op = T1 if k % 2 == 0 else T2
            tau_next = op.apply(tau)
            dists.append(space.metric(tau, tau_next))
            tau = tau_next
        ax.semilogy(range(len(dists)), [max(d, 1e-20) for d in dists], alpha=0.5, linewidth=1)
    ax.set_xlabel("Iteration k")
    ax.set_ylabel("d(S_k(τ), S_{k+1}(τ))")
    ax.grid(True, alpha=0.3)

    # Non-commuting composition
    ax = axes[1]
    ax.set_title("Non-commuting Operators: Alternating Composition")
    for _ in range(5):
        tau = space.random_trajectory()
        dists = []
        for k in range(60):
            op = T3 if k % 2 == 0 else T4
            tau_next = op.apply(tau)
            dists.append(space.metric(tau, tau_next))
            tau = tau_next
        ax.semilogy(range(len(dists)), [max(d, 1e-20) for d in dists], alpha=0.5, linewidth=1)
    ax.set_xlabel("Iteration k")
    ax.set_ylabel("d(S_k(τ), S_{k+1}(τ))")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "composition_convergence.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: composition_convergence.png")


def plot_greens_lattice():
    """Visualize the J-class lattice structure of a finite semigroup."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    # Use results from verification
    results_path = os.path.join(RESULTS_DIR, "verification_results.json")
    with open(results_path) as f:
        results = json.load(f)

    greens = results.get("greens_relations", {})

    # Create a summary visualization
    categories = ["Elements", "Idempotents", "L-classes", "R-classes", "J-classes"]
    values = [
        greens.get("n_elements", 0),
        greens.get("n_idempotents", 0),
        greens.get("n_L_classes", 0),
        greens.get("n_R_classes", 0),
        greens.get("n_J_classes", 0),
    ]

    bars = ax.bar(categories, values, color=['#2196F3', '#FF9800', '#4CAF50', '#9C27B0', '#F44336'])
    ax.set_ylabel("Count")
    ax.set_title("Algebraic Structure of Finite Matrix Semigroup (2×2)")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
               str(val), ha='center', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "greens_structure.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: greens_structure.png")


if __name__ == "__main__":
    plot_convergence_comparison()
    plot_spectral_analysis()
    plot_composition_convergence()
    plot_greens_lattice()
    print("\nAll figures generated successfully.")
