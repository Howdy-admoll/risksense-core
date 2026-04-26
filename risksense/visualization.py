"""
RiskSense Visualization — Plot fuzzy sets and model decisions

Provides:
- Fuzzy membership function plots
- Risk score distribution across borrower profiles
- 2D parameter heatmaps
- Decision surface visualization
- Sensitivity plots

Requirements:
    matplotlib, numpy (already have these)

Usage:
    from risksense.visualization import plot_membership_functions
    plot_membership_functions('income', save_path='income_fuzzy.png')
"""

import numpy as np
from pathlib import Path
from typing import Optional

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def plot_membership_functions(
    variable: str,
    save_path: Optional[str] = None,
    dpi: int = 100,
) -> Optional[str]:
    """
    Plot fuzzy membership functions for an input variable.

    Args:
        variable (str): "income", "dti", "credit", or "stability"
        save_path (str, optional): Save to file if provided
        dpi (int): Resolution for saved figure

    Returns:
        str: Path to saved file, or None if not saved

    Example:
        >>> plot_membership_functions('income', 'fuzzy_income.png')
    """
    if not HAS_MATPLOTLIB:
        raise ImportError(
            'matplotlib required for visualization. '
            'Install: pip install matplotlib'
        )

    fig, ax = plt.subplots(figsize=(10, 6))

    if variable == 'income':
        # Annual income (₦M)
        x = np.arange(0, 10.1, 0.1)
        # Triangular membership functions
        low = np.maximum(1 - np.abs(x - 0) / 2.5, 0)
        medium = np.maximum(1 - np.abs(x - 4) / 2.5, 0)
        high = np.maximum(1 - np.abs(x - 10) / 2.5, 0)

        ax.plot(x, low, 'b-', linewidth=2, label='Low')
        ax.plot(x, medium, 'orange', linewidth=2, label='Medium')
        ax.plot(x, high, 'r-', linewidth=2, label='High')
        ax.set_xlabel('Annual Income (₦ Millions)', fontsize=12)
        ax.set_title('Income Fuzzy Membership Functions', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 10)

    elif variable == 'dti':
        # Debt-to-Income ratio
        x = np.arange(0, 1.01, 0.01)
        low = np.maximum(1 - np.abs(x - 0) / 0.35, 0)
        medium = np.maximum(1 - np.abs(x - 0.55) / 0.3, 0)
        high = np.maximum(1 - np.abs(x - 1.0) / 0.35, 0)

        ax.plot(x, low, 'b-', linewidth=2, label='Low')
        ax.plot(x, medium, 'orange', linewidth=2, label='Medium')
        ax.plot(x, high, 'r-', linewidth=2, label='High')
        ax.set_xlabel('Debt-to-Income Ratio', fontsize=12)
        ax.set_title('DTI Fuzzy Membership Functions', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1.0)

    elif variable == 'credit':
        # Credit score
        x = np.arange(0, 101, 1)
        poor = np.maximum(1 - np.abs(x - 0) / 40, 0)
        fair = np.maximum(1 - np.abs(x - 60) / 30, 0)
        good = np.maximum(1 - np.abs(x - 100) / 30, 0)

        ax.plot(x, poor, 'r-', linewidth=2, label='Poor')
        ax.plot(x, fair, 'orange', linewidth=2, label='Fair')
        ax.plot(x, good, 'g-', linewidth=2, label='Good')
        ax.set_xlabel('Credit History Score', fontsize=12)
        ax.set_title('Credit Score Fuzzy Membership Functions', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)

    elif variable == 'stability':
        # Employment stability
        x = np.arange(0, 10.1, 0.1)
        low = np.maximum(1 - np.abs(x - 0) / 3, 0)
        medium = np.maximum(1 - np.abs(x - 5) / 3, 0)
        high = np.maximum(1 - np.abs(x - 10) / 3, 0)

        ax.plot(x, low, 'b-', linewidth=2, label='Low')
        ax.plot(x, medium, 'orange', linewidth=2, label='Medium')
        ax.plot(x, high, 'g-', linewidth=2, label='High')
        ax.set_xlabel('Employment Stability Index', fontsize=12)
        ax.set_title('Employment Stability Fuzzy Membership Functions', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 10)

    else:
        raise ValueError(f'Unknown variable: {variable}')

    ax.set_ylabel('Membership Degree', fontsize=12)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_axisbelow(True)

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return save_path
    else:
        plt.show()
        return None


def plot_profile_risks(
    profiles: list,
    model=None,
    save_path: Optional[str] = None,
    dpi: int = 100,
) -> Optional[str]:
    """
    Bar plot showing risk scores for test profiles.

    Args:
        profiles (list): List of profile dicts
        model: RiskSenseModel instance (created if None)
        save_path (str, optional): Save to file if provided
        dpi (int): Resolution for saved figure

    Returns:
        str: Path to saved file, or None if not saved
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('matplotlib required for visualization')

    if model is None:
        from risksense import create_model
        model = create_model()

    profile_names = []
    risk_scores = []
    categories = []
    colors = []

    for p in profiles:
        score, category = model.score(
            p['annual_income'],
            p['debt_to_income'],
            p['credit_score'],
            p['employment_stability'],
        )
        profile_names.append(p['name'].replace('Profile ', 'P').split(':')[0])
        risk_scores.append(score)
        categories.append(category)

        if category == 'Low':
            colors.append('#2ecc71')  # Green
        elif category == 'Medium':
            colors.append('#f39c12')  # Orange
        else:
            colors.append('#e74c3c')  # Red

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(profile_names, risk_scores, color=colors, edgecolor='black', linewidth=1.5)

    # Add horizontal lines for risk thresholds
    ax.axhline(y=35, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Low/Medium boundary (35)')
    ax.axhline(y=65, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Medium/High boundary (65)')

    # Add value labels on bars
    for i, (bar, score, cat) in enumerate(zip(bars, risk_scores, categories)):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            score + 2,
            f'{score:.1f}\n({cat})',
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold',
        )

    ax.set_ylabel('Risk Score (0–100)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Borrower Profile', fontsize=12, fontweight='bold')
    ax.set_title('RiskSense: Profile Risk Assessment', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(fontsize=10, loc='upper left')

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return save_path
    else:
        plt.show()
        return None


def plot_sensitivity_heatmap(
    model=None,
    x_param: str = 'income',
    y_param: str = 'dti',
    save_path: Optional[str] = None,
    dpi: int = 100,
) -> Optional[str]:
    """
    2D heatmap showing risk score sensitivity to two parameters.

    Args:
        model: RiskSenseModel instance
        x_param (str): "income", "dti", "credit", or "stability"
        y_param (str): "income", "dti", "credit", or "stability"
        save_path (str, optional): Save to file if provided
        dpi (int): Resolution for saved figure

    Returns:
        str: Path to saved file, or None if not saved

    Example:
        >>> plot_sensitivity_heatmap(model, x_param='income', y_param='dti', 
        ...                          save_path='heatmap.png')
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('matplotlib required for visualization')

    if model is None:
        from risksense import create_model
        model = create_model()

    # Base case
    base = {
        'annual_income': 2.5,
        'debt_to_income': 0.5,
        'credit_score': 60,
        'employment_stability': 5.0,
    }

    # Define ranges
    ranges = {
        'income': np.linspace(0.5, 8, 15),
        'dti': np.linspace(0.1, 1.0, 15),
        'credit': np.linspace(20, 100, 15),
        'stability': np.linspace(1, 10, 15),
    }

    param_map = {
        'income': 'annual_income',
        'dti': 'debt_to_income',
        'credit': 'credit_score',
        'stability': 'employment_stability',
    }

    x_values = ranges[x_param]
    y_values = ranges[y_param]
    z = np.zeros((len(y_values), len(x_values)))

    for i, y_val in enumerate(y_values):
        for j, x_val in enumerate(x_values):
            params = base.copy()
            params[param_map[x_param]] = x_val
            params[param_map[y_param]] = y_val
            score, _ = model.score(**params)
            z[i, j] = score

    fig, ax = plt.subplots(figsize=(11, 8))
    im = ax.imshow(
        z,
        cmap='RdYlGn_r',
        aspect='auto',
        origin='lower',
        vmin=0,
        vmax=100,
    )

    # Axis labels
    x_labels = [f'{v:.1f}' for v in x_values]
    y_labels = [f'{v:.1f}' for v in y_values]

    ax.set_xticks(np.arange(len(x_values))[::2])
    ax.set_yticks(np.arange(len(y_values))[::2])
    ax.set_xticklabels(x_labels[::2])
    ax.set_yticklabels(y_labels[::2])

    ax.set_xlabel(x_param.upper(), fontsize=12, fontweight='bold')
    ax.set_ylabel(y_param.upper(), fontsize=12, fontweight='bold')
    ax.set_title(
        f'Risk Score Sensitivity: {x_param.upper()} vs {y_param.upper()}',
        fontsize=14,
        fontweight='bold',
    )

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Risk Score (0–100)', fontsize=11)

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return save_path
    else:
        plt.show()
        return None
