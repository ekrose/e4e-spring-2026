#!/usr/bin/env python3
"""
Generate figures for the Uncertainty lecture using actual simulations.
Run this script to regenerate all SVG figures from real data.

Requirements: pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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


def fig1_dice_distribution():
    """
    Distribution of number of 1s in 100 rolls of a fair die.
    Shows the binomial distribution B(100, 1/6).
    """
    n_rolls = 100
    p_one = 1/6

    # Simulate 10,000 experiments
    n_sims = 10000
    results = np.random.binomial(n_rolls, p_one, n_sims)

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
    Distributions of estimated P(1) for N = 10, 100, 1000 rolls.
    """
    p_true = 1/6
    n_sims = 10000

    sample_sizes = [10, 100, 1000]
    colors = [ORANGE, MAROON, DARK_MAROON]
    alphas = [0.5, 0.6, 0.7]

    fig, ax = plt.subplots(figsize=(9, 5))

    for n, color, alpha in zip(sample_sizes, colors, alphas):
        # Simulate: for each experiment, roll n times, compute proportion of 1s
        ones_count = np.random.binomial(n, p_true, n_sims)
        proportions = ones_count / n

        # Plot kernel density estimate for smooth curve
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(proportions, bw_method=0.15)
        x = np.linspace(0, 0.5, 500)
        ax.fill_between(x, kde(x), alpha=alpha, color=color, label=f'N = {n:,} rolls')
        ax.plot(x, kde(x), color=color, linewidth=1.5)

    # True value line
    ax.axvline(p_true, color='#333', linestyle='--', linewidth=2)
    ax.text(p_true + 0.01, ax.get_ylim()[1] * 0.95, f'True: 1/6', fontsize=10)

    ax.set_xlabel('Estimated probability of rolling a 1')
    ax.set_ylabel('Probability Density')
    ax.set_title('More Data = Less Uncertainty', fontweight='bold')
    ax.legend(loc='upper right')
    ax.set_xlim(0, 0.5)

    plt.tight_layout()
    plt.savefig('sample-size-comparison.svg', format='svg', bbox_inches='tight')
    plt.savefig('sample-size-comparison.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: sample-size-comparison.svg")


def fig3_confidence_interval():
    """
    Illustrates confidence interval construction via test inversion.
    For each hypothetical true value, shows whether our estimate of 48% is plausible.
    """
    n_voters = 100
    our_estimate = 0.48
    n_sims = 10000

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), height_ratios=[1, 0.4])

    # Top panel: Show distributions for different hypothetical true values
    ax1 = axes[0]

    test_values = [0.40, 0.48, 0.60]
    colors = ['#cc0000', '#008800', '#cc0000']
    fills = ['#ffcccc', '#ccffcc', '#ffcccc']
    labels = ['Reject (40%)', 'Accept (48%)', 'Reject (60%)']

    x = np.linspace(0.25, 0.75, 500)

    for i, (true_p, color, fill, label) in enumerate(zip(test_values, colors, fills, labels)):
        # Distribution of estimates if true value were true_p
        std = np.sqrt(true_p * (1 - true_p) / n_voters)
        y = stats.norm.pdf(x, true_p, std)

        # Offset for visibility
        offset = i * 0.15
        ax1.fill_between(x, y + offset, offset, alpha=0.5, color=fill)
        ax1.plot(x, y + offset, color=color, linewidth=2)
        ax1.axvline(true_p, ymin=offset/1.5, ymax=(max(y)+offset)/1.5,
                   color=color, linestyle='--', linewidth=1.5)

        # Mark our estimate
        y_at_estimate = stats.norm.pdf(our_estimate, true_p, std)
        ax1.plot(our_estimate, y_at_estimate + offset, 'o', color=MAROON, markersize=8)

        # Label
        ax1.text(0.72, offset + 0.3, label, color=color, fontsize=10, fontweight='bold')

    ax1.axvline(our_estimate, color=MAROON, linewidth=2, label=f'Our estimate: {our_estimate:.0%}')
    ax1.set_xlim(0.25, 0.75)
    ax1.set_ylim(0, 1.5)
    ax1.set_xlabel('Possible poll results')
    ax1.set_ylabel('Probability density')
    ax1.set_title('Testing Different Hypothetical True Values', fontweight='bold')
    ax1.legend(loc='upper left')

    # Bottom panel: The resulting confidence interval
    ax2 = axes[1]

    # Compute actual 95% CI
    std_est = np.sqrt(our_estimate * (1 - our_estimate) / n_voters)
    ci_low = our_estimate - 1.96 * std_est
    ci_high = our_estimate + 1.96 * std_est

    # Draw CI
    ax2.barh(0, ci_high - ci_low, left=ci_low, height=0.3, color='#ccffcc',
             edgecolor='#008800', linewidth=2)
    ax2.barh(0, ci_low - 0.25, left=0.25, height=0.3, color='#ffcccc', alpha=0.5)
    ax2.barh(0, 0.75 - ci_high, left=ci_high, height=0.3, color='#ffcccc', alpha=0.5)

    ax2.plot(our_estimate, 0, 'o', color=MAROON, markersize=12, zorder=5)
    ax2.text(our_estimate, 0.25, f'{our_estimate:.0%}', ha='center', fontsize=10, color=MAROON)

    ax2.text(ci_low, -0.35, f'{ci_low:.0%}', ha='center', fontsize=9)
    ax2.text(ci_high, -0.35, f'{ci_high:.0%}', ha='center', fontsize=9)

    ax2.set_xlim(0.25, 0.75)
    ax2.set_ylim(-0.5, 0.5)
    ax2.set_xlabel('True Republican vote share')
    ax2.set_title(f'95% Confidence Interval: {ci_low:.0%} to {ci_high:.0%}',
                  fontweight='bold', color='#008800')
    ax2.set_yticks([])
    ax2.spines['left'].set_visible(False)

    plt.tight_layout()
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

    fig, ax = plt.subplots(figsize=(9, 5))

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

    # Annotation
    ax.annotate(f'{n_suspicious} dice\n"look suspicious"',
                xy=(6, counts[6] if len(counts) > 6 else 10),
                xytext=(7.5, max(counts) * 0.7),
                fontsize=11, color=ORANGE, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))

    # Add text box
    textstr = f'All {n_dice:,} dice are fair!\nThese {n_suspicious} are false positives.'
    props = dict(boxstyle='round', facecolor='#fff3e6', edgecolor=ORANGE, linewidth=2)
    ax.text(0.98, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    # Theoretical expectation
    expected_counts = n_dice * stats.binom.pmf(np.arange(n_rolls + 1), n_rolls, p_one)
    ax.plot(np.arange(n_rolls + 1), expected_counts, 'o-', color=DARK_MAROON,
            linewidth=2, markersize=6, label='Expected (theory)')

    ax.set_xlabel('Number of 1s (out of 10 rolls)')
    ax.set_ylabel('Number of dice')
    ax.set_title(f'{n_dice:,} Fair Dice, Each Rolled {n_rolls} Times', fontweight='bold')
    ax.legend(loc='upper right')
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
    print("Generating Uncertainty lecture figures from simulations...\n")

    fig1_dice_distribution()
    fig2_sample_size_comparison()
    fig3_confidence_interval()
    fig4_multiple_testing()

    print("\nDone! All figures regenerated from actual simulation data.")
