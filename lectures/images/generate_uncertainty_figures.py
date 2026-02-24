#!/usr/bin/env python3
"""
Generate figures for the Uncertainty lecture using actual simulations.
Run this script to regenerate all SVG figures from real data.

Requirements: pip install numpy matplotlib scipy
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gaussian_kde

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# UChicago colors
MAROON = '#800000'
ORANGE = '#ff8243'
DARK_MAROON = '#4a0000'

np.random.seed(42)  # For reproducibility

N_SIMS = 10000  # Number of simulated experiments


def fig1_dice_distribution():
    """
    Distribution of number of 1s in 100 rolls of a fair die.
    Shows the binomial distribution B(100, 1/6).
    """
    n_rolls = 100
    p_one = 1/6

    # Simulate N_SIMS experiments
    results = np.random.binomial(n_rolls, p_one, N_SIMS)

    fig, ax = plt.subplots(figsize=(8, 5))

    # Histogram of simulation results
    bins = np.arange(0, 40) - 0.5
    ax.hist(results, bins=bins, density=True, color=MAROON, alpha=0.7,
            edgecolor='white', linewidth=0.5)

    # Overlay theoretical distribution
    x = np.arange(0, 40)
    theoretical = stats.binom.pmf(x, n_rolls, p_one)
    ax.plot(x, theoretical, color=DARK_MAROON, linewidth=2, label='Theoretical')

    # Expected value line
    expected = n_rolls * p_one
    ax.axvline(expected, color=MAROON, linestyle='--', linewidth=2)
    ax.text(expected + 0.5, ax.get_ylim()[1] * 0.9, f'Expected: {expected:.1f}',
            color=MAROON, fontsize=10)

    ax.set_xlabel('Number of 1s out of 100 rolls')
    ax.set_ylabel('Probability')
    ax.set_title('Distribution of 1s in 100 Rolls of a Fair Die', fontweight='bold')
    ax.set_xlim(0, 35)

    plt.tight_layout()
    plt.savefig('dice-distribution.svg', format='svg', bbox_inches='tight')
    plt.savefig('dice-distribution.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: dice-distribution.svg")


def fig2_sample_size_comparison():
    """
    Shows how uncertainty shrinks as sample size increases.
    For each sample size, we simulate N_SIMS experiments.
    Each experiment: roll die N times, compute proportion of 1s.
    """
    p_true = 1/6

    sample_sizes = [10, 100, 1000]
    colors = [ORANGE, MAROON, DARK_MAROON]
    alphas = [0.4, 0.5, 0.6]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    for n, color, alpha in zip(sample_sizes, colors, alphas):
        # Simulate N_SIMS experiments, each rolling the die n times
        ones_count = np.random.binomial(n, p_true, N_SIMS)
        proportions = ones_count / n

        # Plot kernel density estimate for smooth curve
        kde = gaussian_kde(proportions, bw_method=0.12)
        x = np.linspace(0, 0.5, 500)
        ax.fill_between(x, kde(x), alpha=alpha, color=color,
                        label=f'N = {n:,} rolls per experiment')
        ax.plot(x, kde(x), color=color, linewidth=1.5)

    # True value line
    ax.axvline(p_true, color='#333', linestyle='--', linewidth=2, label='True value: 1/6')

    ax.set_xlabel('Estimated probability of rolling a 1')
    ax.set_ylabel('Density')
    ax.set_title(f'More Data = Less Uncertainty\n({N_SIMS:,} simulated experiments for each sample size)',
                 fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig('sample-size-comparison.svg', format='svg', bbox_inches='tight')
    plt.savefig('sample-size-comparison.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: sample-size-comparison.svg")


def fig3_confidence_interval():
    """
    Illustrates confidence interval construction via test inversion.
    Three panels showing: if truth were X, would we likely see 48%?
    """
    n_voters = 100
    our_estimate = 0.48

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    test_values = [0.40, 0.48, 0.58]
    results = ['REJECT', 'ACCEPT', 'REJECT']
    result_colors = ['#cc0000', '#008800', '#cc0000']
    fill_colors = ['#ffcccc', '#ccffcc', '#ffcccc']

    for ax, true_p, result, result_color, fill_color in zip(
            axes, test_values, results, result_colors, fill_colors):

        # Distribution of estimates if true value were true_p
        std = np.sqrt(true_p * (1 - true_p) / n_voters)
        x = np.linspace(true_p - 4*std, true_p + 4*std, 200)
        y = stats.norm.pdf(x, true_p, std)

        # Fill the distribution
        ax.fill_between(x, y, alpha=0.4, color=fill_color)
        ax.plot(x, y, color=result_color, linewidth=2)

        # Mark the true value
        ax.axvline(true_p, color=result_color, linestyle='--', linewidth=1.5, alpha=0.7)

        # Mark our estimate
        y_at_est = stats.norm.pdf(our_estimate, true_p, std)
        ax.plot(our_estimate, y_at_est, 'o', color=MAROON, markersize=10, zorder=5)
        ax.axvline(our_estimate, color=MAROON, linewidth=2, alpha=0.8)

        # Labels
        ax.set_title(f'If true value = {true_p:.0%}', fontweight='bold', fontsize=12)
        ax.set_xlabel('Possible poll results')
        if ax == axes[0]:
            ax.set_ylabel('Probability density')

        # Result text
        ax.text(0.5, 0.95, result, transform=ax.transAxes, fontsize=14,
                fontweight='bold', color=result_color, ha='center', va='top')

        # Explanation
        if result == 'REJECT':
            if true_p < our_estimate:
                expl = f'48% is too high\nto come from {true_p:.0%}'
            else:
                expl = f'48% is too low\nto come from {true_p:.0%}'
        else:
            expl = f'48% is plausible\nif truth is {true_p:.0%}'
        ax.text(0.5, 0.82, expl, transform=ax.transAxes, fontsize=9,
                ha='center', va='top', color='#666')

        ax.set_ylim(bottom=0)

    # Add annotation for "our estimate"
    fig.text(0.5, 0.02, 'Red dot = our poll estimate (48%)', ha='center',
             fontsize=10, color=MAROON)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('confidence-interval.svg', format='svg', bbox_inches='tight')
    plt.savefig('confidence-interval.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: confidence-interval.svg")


def fig4_multiple_testing():
    """
    Multiple testing problem: 1000 fair dice, each rolled 10 times.
    Shows histogram of number of 1s, highlighting "suspicious" dice.
    """
    n_dice = 1000
    n_rolls = 10
    p_one = 1/6

    # Simulate: each die rolled 10 times, count 1s
    ones_per_die = np.random.binomial(n_rolls, p_one, n_dice)

    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Count dice in each bin
    bins = np.arange(0, n_rolls + 2) - 0.5
    counts, edges, patches = ax.hist(ones_per_die, bins=bins, color=MAROON,
                                      edgecolor='white', linewidth=1)

    # Highlight "suspicious" dice (5+ ones)
    suspicious_threshold = 5
    for i, (count, patch) in enumerate(zip(counts, patches)):
        if i >= suspicious_threshold:
            patch.set_facecolor(ORANGE)

    # Count suspicious dice
    n_suspicious = np.sum(ones_per_die >= suspicious_threshold)

    # Theoretical expectation line
    expected_counts = n_dice * stats.binom.pmf(np.arange(n_rolls + 1), n_rolls, p_one)
    ax.plot(np.arange(n_rolls + 1), expected_counts, 'o-', color=DARK_MAROON,
            linewidth=2, markersize=6, label='Expected (theory)')

    # Annotation arrow to suspicious dice
    arrow_target_x = 5.5
    arrow_target_y = counts[5] if len(counts) > 5 else 10
    ax.annotate(f'{n_suspicious} dice "look suspicious"',
                xy=(arrow_target_x, arrow_target_y),
                xytext=(7, max(counts) * 0.85),
                fontsize=11, color=ORANGE, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2),
                ha='left')

    # Text box - positioned to not overlap with legend
    textstr = f'But all {n_dice:,} dice are fair!\nThese are false positives.'
    props = dict(boxstyle='round', facecolor='#fff3e6', edgecolor=ORANGE, linewidth=2)
    ax.text(0.98, 0.65, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    ax.set_xlabel('Number of 1s (out of 10 rolls per die)')
    ax.set_ylabel('Number of dice')
    ax.set_title(f'{n_dice:,} Fair Dice, Each Rolled {n_rolls} Times', fontweight='bold')
    ax.legend(loc='upper left')
    ax.set_xlim(-0.5, 10.5)

    plt.tight_layout()
    plt.savefig('multiple-testing.svg', format='svg', bbox_inches='tight')
    plt.savefig('multiple-testing.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: multiple-testing.svg")

    # Print some stats
    print(f"  - Dice with 5+ ones: {n_suspicious} ({n_suspicious/n_dice:.1%})")
    print(f"  - Expected under null: {n_dice * (1 - stats.binom.cdf(4, n_rolls, p_one)):.1f}")


if __name__ == '__main__':
    print(f"Generating Uncertainty lecture figures from {N_SIMS:,} simulations...\n")

    fig1_dice_distribution()
    fig2_sample_size_comparison()
    fig3_confidence_interval()
    fig4_multiple_testing()

    print("\nDone! All figures regenerated from actual simulation data.")
