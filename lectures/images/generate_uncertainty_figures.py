#!/usr/bin/env python3
"""
Generate figures for the Uncertainty lecture using actual simulations.
Run this script to regenerate all SVG figures from real data.

Requirements: pip install numpy matplotlib scipy
"""

import os
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

OUTPUT_DIR = 'lectures/images'
os.makedirs(OUTPUT_DIR, exist_ok=True)


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
    ax.text(expected + 0.5, ax.get_ylim()[1] * 0.97, f'Expected: {expected:.1f}',
            color=MAROON, fontsize=10)

    ax.set_xlabel('Number of 1s out of 100 rolls')
    ax.set_ylabel('Probability')
    ax.set_title('Distribution of 1s in 100 Rolls of a Fair Die', fontweight='bold')
    ax.set_xlim(0, 35)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/dice-distribution.svg', format='svg', bbox_inches='tight')
    plt.savefig(f'{OUTPUT_DIR}/dice-distribution.png', format='png', dpi=150, bbox_inches='tight')
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
    plt.savefig(f'{OUTPUT_DIR}/sample-size-comparison.svg', format='svg', bbox_inches='tight')
    plt.savefig(f'{OUTPUT_DIR}/sample-size-comparison.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: sample-size-comparison.svg")


def fig3_confidence_interval():
    """
    Illustrates confidence interval construction via test inversion.
    Three panels showing: if truth were X, would we likely see 48%?
    """
    n_voters = 100
    our_estimate = 0.48

    fig, axes = plt.subplots(1, 3, figsize=(13, 5))

    test_values = [0.35, 0.48, 0.61]
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
        ax.set_title(f'If true value = {true_p:.0%}', fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Possible poll results')
        if ax == axes[0]:
            ax.set_ylabel('Probability density')

        # Explanation text below x-axis using xlabel area
        if result == 'REJECT':
            if true_p < our_estimate:
                expl = f'48% too high to come from {true_p:.0%}'
            else:
                expl = f'48% too low to come from {true_p:.0%}'
        else:
            expl = f'48% is plausible if truth is {true_p:.0%}'

        ax.set_ylim(bottom=0)

        # Add result badge below the plot
        ax.text(0.5, -0.22, result, transform=ax.transAxes, fontsize=13,
                fontweight='bold', color='white', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=result_color, edgecolor='none'))
        ax.text(0.5, -0.35, expl, transform=ax.transAxes, fontsize=9,
                ha='center', va='center', color='#555')

    # Add annotation for "our estimate"
    fig.text(0.5, -0.04, 'Red line & dot = our poll estimate (48%)', ha='center',
             fontsize=11, color=MAROON, fontweight='bold')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.savefig(f'{OUTPUT_DIR}/confidence-interval.svg', format='svg', bbox_inches='tight')
    plt.savefig(f'{OUTPUT_DIR}/confidence-interval.png', format='png', dpi=150, bbox_inches='tight')
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
    arrow_target_x = 5
    arrow_target_y = counts[5] if len(counts) > 5 else 5
    ax.annotate(f'{n_suspicious} dice "look suspicious"',
                xy=(arrow_target_x, arrow_target_y),
                xytext=(5, max(counts) * 0.3),
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
    plt.savefig(f'{OUTPUT_DIR}/multiple-testing.svg', format='svg', bbox_inches='tight')
    plt.savefig(f'{OUTPUT_DIR}/multiple-testing.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: multiple-testing.svg")

    # Print some stats
    print(f"  - Dice with 5+ ones: {n_suspicious} ({n_suspicious/n_dice:.1%})")
    print(f"  - Expected under null: {n_dice * (1 - stats.binom.cdf(4, n_rolls, p_one)):.1f}")


def fig5_ci_construction():
    """
    Visualizes confidence interval construction via test inversion.
    Three panels show sampling distributions for candidate true values,
    with a CI bar underneath showing the accepted region.
    """
    n_voters = 100
    our_estimate = 0.48
    confidence_level = 0.95
    alpha = 1 - confidence_level

    # Compute the CI via simulation sweep
    candidate_truths = np.linspace(0.30, 0.66, 200)
    accepted = []
    for p0 in candidate_truths:
        # Step 1: Assume this candidate is the true vote share
        # Step 2: Simulate N_SIMS polls of n_voters, compute sample proportions
        sim_estimates = np.random.binomial(n_voters, p0, N_SIMS) / n_voters

        # Step 3: Find the critical region — the most extreme 5% of outcomes
        lower_critical = np.percentile(sim_estimates, 2.5)
        upper_critical = np.percentile(sim_estimates, 97.5)

        # Step 4: Does our estimate fall in the plausible range?
        is_plausible = lower_critical <= our_estimate <= upper_critical
        accepted.append(is_plausible)

    accepted = np.array(accepted)
    ci_low = candidate_truths[accepted].min()
    ci_high = candidate_truths[accepted].max()

    # --- Three-panel figure with CI bar ---
    fig = plt.figure(figsize=(13, 6.5))
    gs = fig.add_gridspec(2, 3, height_ratios=[4, 1], hspace=0.35)

    # Top row: three distributions
    test_values = [0.35, 0.48, 0.61]
    results = ['REJECT', 'ACCEPT', 'REJECT']
    result_colors = ['#cc0000', '#008800', '#cc0000']
    fill_colors = ['#ffcccc', '#ccffcc', '#ffcccc']

    for col, (true_p, result, result_color, fill_color) in enumerate(
            zip(test_values, results, result_colors, fill_colors)):

        ax = fig.add_subplot(gs[0, col])

        std = np.sqrt(true_p * (1 - true_p) / n_voters)
        x = np.linspace(true_p - 4 * std, true_p + 4 * std, 200)
        y = stats.norm.pdf(x, true_p, std)

        ax.fill_between(x, y, alpha=0.4, color=fill_color)
        ax.plot(x, y, color=result_color, linewidth=2)

        ax.axvline(true_p, color=result_color, linestyle='--', linewidth=1.5, alpha=0.7)

        y_at_est = stats.norm.pdf(our_estimate, true_p, std)
        ax.plot(our_estimate, y_at_est, 'o', color=MAROON, markersize=10, zorder=5)
        ax.axvline(our_estimate, color=MAROON, linewidth=2, alpha=0.8)

        ax.set_title(f'If true value = {true_p:.0%}', fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Possible poll results')
        if col == 0:
            ax.set_ylabel('Probability density')
        ax.set_ylim(bottom=0)


    # Bottom row: CI bar spanning all three columns
    ax_ci = fig.add_subplot(gs[1, :])

    # Draw reject/accept regions
    ax_ci.axhspan(0, 1, xmin=0, xmax=1, color='#ffcccc', alpha=0.3)
    ax_ci.axvspan(ci_low, ci_high, color='#ccffcc', alpha=0.5)

    # CI boundary lines
    ax_ci.axvline(ci_low, color='#008800', linewidth=2, linestyle='--')
    ax_ci.axvline(ci_high, color='#008800', linewidth=2, linestyle='--')

    # Our estimate
    ax_ci.axvline(our_estimate, color=MAROON, linewidth=1.5, zorder=5, linestyle='--', alpha=0.6)

    # Labels
    ax_ci.text(ci_low, -0.35, f'{ci_low:.1%}', ha='center', fontsize=11,
               fontweight='bold', color='#008800', transform=ax_ci.get_xaxis_transform())
    ax_ci.text(ci_high, -0.35, f'{ci_high:.1%}', ha='center', fontsize=11,
               fontweight='bold', color='#008800', transform=ax_ci.get_xaxis_transform())
    ax_ci.text(our_estimate, -0.35, f'{our_estimate:.0%}', ha='center', fontsize=11,
               fontweight='bold', color=MAROON, transform=ax_ci.get_xaxis_transform())

    # Region labels
    ax_ci.text((0.30 + ci_low) / 2, 0.5, 'REJECT', ha='center', va='center',
               fontsize=12, fontweight='bold', color='#cc0000')
    ax_ci.text((ci_low + ci_high) / 2, 0.5, '95% CONFIDENCE INTERVAL', ha='center',
               va='center', fontsize=12, fontweight='bold', color='#008800')
    ax_ci.text((ci_high + 0.66) / 2, 0.5, 'REJECT', ha='center', va='center',
               fontsize=12, fontweight='bold', color='#cc0000')

    # Connect panels to CI bar with arrows for the three test values
    for true_p, result_color in zip(test_values, result_colors):
        ax_ci.annotate('', xy=(true_p, 1.0), xytext=(true_p, 1.3),
                       xycoords=('data', 'axes fraction'),
                       textcoords=('data', 'axes fraction'),
                       arrowprops=dict(arrowstyle='->', color=result_color, lw=1.5))

    ax_ci.set_xlim(0.30, 0.66)
    ax_ci.set_yticks([])
    ax_ci.set_xlabel('Candidate true vote share', fontsize=11)

    fig.suptitle('Constructing a 95% Confidence Interval via Test Inversion\n'
                 f'Poll of {n_voters} voters, observed estimate = {our_estimate:.0%}',
                 fontweight='bold', fontsize=14, y=1.02)

    plt.savefig(f'{OUTPUT_DIR}/ci-construction.svg', format='svg', bbox_inches='tight')
    plt.savefig(f'{OUTPUT_DIR}/ci-construction.png', format='png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: ci-construction.svg")
    print(f"  - 95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

if __name__ == '__main__':
    print(f"Generating Uncertainty lecture figures from {N_SIMS:,} simulations...\n")

    fig1_dice_distribution()
    fig2_sample_size_comparison()
    fig3_confidence_interval()
    fig4_multiple_testing()
    fig5_ci_construction()

    print("\nDone! All figures regenerated from actual simulation data.")