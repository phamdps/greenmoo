"""
Modular visualization utilities for Greenmoo using Plotly, Matplotlib, and Seaborn.
"""
import math
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Apply clean aesthetic styling for seaborn/matplotlib
sns.set_theme(style="whitegrid", palette="deep")

def plot_pareto(solutions, problem=None, objective_names=None, algorithm_name=None):
    """
    Renders an interactive 2D or 3D Pareto front visualization using Plotly.
    Includes the algorithm name in the legend and title if provided.
    """
    if not solutions:
        raise ValueError("The solution population is empty.")

    n_objectives = len(solutions[0].objectives)
    if n_objectives < 2:
        raise ValueError("Unsupported number of objectives for plotting. Must have at least 2 objectives.")
    
    if objective_names is None:
        if n_objectives == 2:
            objective_names = ("Objective f1", "Objective f2")
        elif n_objectives == 3:
            objective_names = ("Validation Error", "Energy (J)", "Carbon (gCO2eq)")
        else:
            objective_names = [f"Objective {i+1}" for i in range(n_objectives)]

    x_vals, y_vals, hover_texts = [], [], []

    # --- Build Hover Metadata ---
    for idx, sol in enumerate(solutions):
        x_vals.append(sol.objectives[0])
        y_vals.append(sol.objectives[1])
        
        var_strs = []
        for v_idx, raw_var in enumerate(sol.variables):
            if problem and v_idx < len(problem.types):
                var_type = problem.types[v_idx]
                if hasattr(var_type, "decode") and isinstance(raw_var, (list, tuple)):
                    try:
                        decoded_val = var_type.decode(raw_var)
                        var_strs.append(f"Var {v_idx}: {decoded_val}")
                        continue
                    except Exception:
                        pass
                elif not isinstance(raw_var, (list, tuple)) and hasattr(var_type, "decode"):
                    try:
                        decoded_val = var_type.decode(raw_var)
                        var_strs.append(f"Var {v_idx}: {decoded_val}")
                        continue
                    except Exception:
                        pass
            var_strs.append(f"Var {v_idx}: {raw_var}")
            
        vars_display = "<br>".join(var_strs)
        objs_display = "<br>".join([f"<b>{objective_names[i]}:</b> {sol.objectives[i]:.4f}" for i in range(n_objectives)])

        hover_text = (
            f"<b>Solution {idx + 1}</b><br>"
            f"----------------------------------<br>"
            f"{vars_display}<br>"
            f"----------------------------------<br>"
            f"{objs_display}"
        )
        hover_texts.append(hover_text)

    # Dynamic label and title formatting based on algorithm name
    algo_label = f"{algorithm_name} Front" if algorithm_name else "Pareto Optimal Solutions"
    title_suffix = f" — {algorithm_name}" if algorithm_name else ""

    # --- 2D Plotly Visualization ---
    if n_objectives == 2:
        fig = go.Figure(data=go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers',
            name=algo_label,  # Displays algorithm name in the legend
            marker=dict(
                size=11,
                color=y_vals,
                colorscale='Viridis',
                showscale=True,
                line=dict(width=1, color='rgba(0,0,0,0.6)'),
                colorbar=dict(title=objective_names[1])
            ),
            hovertext=hover_texts,
            hoverinfo='text'
        ))
        
        fig.update_layout(
            title=f"<b>Greenmoo Pareto Front (2D Trade-off){title_suffix}</b>",
            xaxis_title=objective_names[0],
            yaxis_title=objective_names[1],
            template="plotly_white",
            font=dict(family="Arial, sans-serif", size=12),
            legend=dict(title="Optimizer", x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor="lightgray", borderwidth=1)
        )

    # --- 3D Plotly Visualization ---
    else:
        z_vals = [sol.objectives[2] for sol in solutions]
        
        fig = go.Figure(data=go.Scatter3d(
            x=x_vals,
            y=y_vals,
            z=z_vals,
            mode='markers',
            name=algo_label,  # Displays algorithm name in the legend
            marker=dict(
                size=7,
                color=z_vals,
                colorscale='Viridis',
                showscale=True,
                line=dict(width=0.5, color='rgba(0,0,0,0.5)'),
                colorbar=dict(title=objective_names[2])
            ),
            hovertext=hover_texts,
            hoverinfo='text'
        ))
        
        fig.update_layout(
            title=f"<b>Greenmoo Pareto Front (3D Sustainable Trade-off){title_suffix}</b>",
            scene=dict(
                xaxis_title=objective_names[0],
                yaxis_title=objective_names[1],
                zaxis_title=objective_names[2]
            ),
            template="plotly_white",
            font=dict(family="Arial, sans-serif", size=12),
            legend=dict(title="Optimizer", x=0.02, y=0.98)
        )

    fig.show()
    return fig


def plot_pareto_static(solutions, problem=None, objective_names=None, save_path=None, color=None, cmap='viridis'):
    """
    Renders a static, publication-ready 2D or 3D Pareto front visualization 
    using Matplotlib and Seaborn. Added 'color' and 'cmap' customization.
    """
    if not solutions:
        raise ValueError("The solution population is empty.")

    n_objectives = len(solutions[0].objectives)
    if n_objectives < 2:
        raise ValueError("Unsupported number of objectives for static plotting. Must have at least 2 objectives.")
    
    if objective_names is None:
        if n_objectives == 2:
            objective_names = ("Objective f1", "Objective f2")
        elif n_objectives == 3:
            objective_names = ("Validation Error", "Energy (J)", "Carbon (gCO2eq)")
        else:
            objective_names = [f"Objective {i+1}" for i in range(n_objectives)]

    x_vals = [sol.objectives[0] for sol in solutions]
    y_vals = [sol.objectives[1] for sol in solutions]

    # --- 2D Static Plot ---
    if n_objectives == 2:
        plt.figure(figsize=(8, 6))
        
        # Check if a custom solid color was passed, otherwise use a colormap
        if color:
            sc = plt.scatter(
                x_vals, y_vals, 
                c=color, 
                s=90, edgecolor='k', linewidth=1.0, alpha=0.85
            )
        else:
            sc = plt.scatter(
                x_vals, y_vals, 
                c=y_vals, cmap=cmap, 
                s=90, edgecolor='k', linewidth=0.8, alpha=0.9
            )
            cbar = plt.colorbar(sc)
            cbar.set_label(objective_names[1], fontsize=11)
        
        plt.title("Greenmoo Pareto Front (2D)", fontsize=14, fontweight='bold', pad=12)
        plt.xlabel(objective_names[0], fontsize=12)
        plt.ylabel(objective_names[1], fontsize=12)
        plt.tight_layout()

    # --- 3D Static Plot ---
    else:
        z_vals = [sol.objectives[2] for sol in solutions]
        
        fig = plt.figure(figsize=(9, 7))
        ax = fig.add_subplot(projection='3d')
        
        if color:
            sc = ax.scatter(
                x_vals, y_vals, z_vals, 
                c=color, 
                s=70, edgecolor='k', linewidth=0.5, depthshade=True
            )
        else:
            sc = ax.scatter(
                x_vals, y_vals, z_vals, 
                c=z_vals, cmap=cmap, 
                s=70, edgecolor='k', linewidth=0.5, depthshade=True
            )
            cbar = fig.colorbar(sc, shrink=0.6, aspect=12)
            cbar.set_label(objective_names[2], fontsize=11)
        
        ax.set_title("Greenmoo Pareto Front (3D Sustainable AutoDL)", fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel(objective_names[0], fontsize=10, labelpad=8)
        ax.set_ylabel(objective_names[1], fontsize=10, labelpad=8)
        ax.set_zlabel(objective_names[2], fontsize=10, labelpad=8)
        plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved static Pareto plot successfully to: {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_experiment_grid(results, problem_name=None, seed_idx=0):
    """
    Abstracted utility to automatically render a multi-panel grid 
    comparing all algorithms from an experiment with proper vertical spacing.
    """
    if not results:
        raise ValueError("Results dictionary is empty.")
    
    # Auto-detect problem name if not specified
    if problem_name is None:
        first_alg = list(results.keys())[0]
        problem_name = list(results[first_alg].keys())[0]
        
    n_algs = len(results)
    cols = min(5, n_algs)
    rows = math.ceil(n_algs / cols)
    
    # Increased height per row to prevent 3D subplots from overlapping
    fig = plt.figure(figsize=(cols * 3.8, rows * 4.5))
    
    plot_idx = 1  # Dedicated counter to prevent gaps when items are skipped
    
    for algorithm_key, prob_dict in results.items():
        if problem_name not in prob_dict:
            continue
            
        runs = prob_dict[problem_name]
        if seed_idx >= len(runs) or not runs[seed_idx]:
            continue
            
        population = runs[seed_idx]
        n_objs = len(population[0].objectives)
        is_3d = (n_objs >= 3)
        
        ax = fig.add_subplot(rows, cols, plot_idx, projection='3d' if is_3d else None)
        plot_idx += 1
        
        x = [s.objectives[0] for s in population]
        y = [s.objectives[1] for s in population]
        
        if is_3d:
            z = [s.objectives[2] for s in population]
            ax.scatter(x, y, z, s=15, c=z, cmap='viridis', edgecolors='k', linewidths=0.2, alpha=0.85)
            ax.set_zlim([0.0, 1.05])
            ax.view_init(elev=25.0, azim=35.0)
            ax.locator_params(nbins=3)
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
        else:
            ax.scatter(x, y, s=20, c=y, cmap='viridis', edgecolors='k', linewidths=0.5, alpha=0.85)
        
        # Robust title extraction (handles both classes and configuration tuples)
        if isinstance(algorithm_key, tuple):
            alg_cls = algorithm_key[0]
        else:
            alg_cls = algorithm_key
            
        raw_name = getattr(alg_cls, "__name__", str(alg_cls))
        title_str = raw_name.split('.')[-1].replace(">", "").replace("'", "").strip()
        
        ax.set_title(title_str, fontsize=11, fontweight='bold', pad=6)
        ax.set_xlim([0.0, 1.05])
        ax.set_ylim([0.0, 1.05])
        
    plt.suptitle(f"Multi-Algorithm Benchmark Comparison: {problem_name}", fontsize=16, fontweight='bold', y=0.96)
    
    # Explicitly add vertical spacing (hspace) between rows to stop overlapping
    plt.subplots_adjust(hspace=0.35, wspace=0.25, top=0.90, bottom=0.08, left=0.05, right=0.95)
    plt.show()

# Overlay functions
def plot_pareto_overlay(results_dict, problem_name="Pareto Comparison", objective_names=None, ref_set=None):
    """
    Renders an interactive multi-algorithm Pareto front overlay using Plotly.
    
    Parameters
    ----------
    results_dict : dict
        Dictionary mapping algorithm name (str) to list of solution objects.
    problem_name : str, optional
        Name of the benchmark problem for the plot title.
    objective_names : tuple of str, optional
        Human-readable labels for the objectives.
    ref_set : list, optional
        True reference Pareto set for comparison.
    """
    if not results_dict:
        raise ValueError("The results dictionary is empty.")

    # Determine dimensions from the first available solution
    first_solutions = next(iter(results_dict.values()))
    if not first_solutions:
        raise ValueError("One or more algorithm result lists are empty.")
        
    n_objectives = len(first_solutions[0].objectives)
    if n_objectives < 2:
        raise ValueError("Unsupported number of objectives for overlay plotting. Must have at least 2.")

    if objective_names is None:
        if n_objectives == 2:
            objective_names = ("Objective f1", "Objective f2")
        elif n_objectives == 3:
            objective_names = ("Objective 1", "Objective 2", "Objective 3")
        else:
            objective_names = [f"Objective {i+1}" for i in range(n_objectives)]

    fig = go.Figure()

    # --- 1. Plot Reference Set if Available ---
    if ref_set is not None and len(ref_set) > 0:
        ref_x = [obj[0] if isinstance(obj, (list, tuple)) else obj.objectives[0] for obj in ref_set]
        ref_y = [obj[1] if isinstance(obj, (list, tuple)) else obj.objectives[1] for obj in ref_set]
        
        if n_objectives >= 3:
            ref_z = [obj[2] if isinstance(obj, (list, tuple)) else obj.objectives[2] for obj in ref_set]
            fig.add_trace(go.Scatter3d(
                x=ref_x, y=ref_y, z=ref_z,
                mode='markers',
                name='Reference Front (True)',
                marker=dict(color='black', size=4, symbol='x'),
                opacity=0.6
            ))
        else:
            fig.add_trace(go.Scatter(
                x=ref_x, y=ref_y,
                mode='markers',
                name='Reference Front (True)',
                marker=dict(color='black', size=6, symbol='x'),
                opacity=0.6
            ))

    # --- 2. Plot Each Algorithm's Pareto Front ---
    for algo_name, solutions in results_dict.items():
        x_vals = [s.objectives[0] for s in solutions]
        y_vals = [s.objectives[1] for s in solutions]

        if n_objectives >= 3:
            z_vals = [s.objectives[2] for s in solutions]
            fig.add_trace(go.Scatter3d(
                x=x_vals, y=y_vals, z=z_vals,
                mode='markers',
                name=algo_name,
                marker=dict(size=5)
            ))
        else:
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_vals,
                mode='markers+text',
                name=algo_name,
                text=[f"{algo_name[0]}{i+1}" for i in range(len(solutions))],
                textposition="top center",
                marker=dict(size=8)
            ))

    # --- 3. Layout Configuration ---
    if n_objectives >= 3:
        fig.update_layout(
            title=f"<b>Multi-Algorithm Pareto Front Comparison ({problem_name})</b>",
            scene=dict(
                xaxis_title=objective_names[0],
                yaxis_title=objective_names[1],
                zaxis_title=objective_names[2]
            ),
            template="plotly_white",
            legend=dict(title="Algorithms", x=0.8, y=0.9)
        )
    else:
        fig.update_layout(
            title=f"<b>Multi-Algorithm Pareto Front Comparison ({problem_name})</b>",
            xaxis_title=objective_names[0],
            yaxis_title=objective_names[1],
            template="plotly_white",
            hovermode='closest',
            legend=dict(title="Algorithms", x=0.80, y=0.95)
        )

    fig.show()
    return fig


def plot_pareto_overlay_static(results_dict, problem_name="Pareto Comparison", objective_names=None, ref_set=None, save_path=None):
    """
    Renders a static, publication-ready multi-algorithm Pareto front overlay 
    using Matplotlib and Seaborn.
    """
    if not results_dict:
        raise ValueError("The results dictionary is empty.")

    first_solutions = next(iter(results_dict.values()))
    n_objectives = len(first_solutions[0].objectives)
    if n_objectives < 2:
        raise ValueError("Unsupported number of objectives for static overlay. Must have at least 2.")

    if objective_names is None:
        if n_objectives == 2:
            objective_names = ("Objective f1", "Objective f2")
        elif n_objectives == 3:
            objective_names = ("Objective 1", "Objective 2", "Objective 3")
        else:
            objective_names = [f"Objective {i+1}" for i in range(n_objectives)]

    if n_objectives >= 3:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='3d')
    else:
        fig, ax = plt.subplots(figsize=(9, 6))

    # --- 1. Plot Reference Set ---
    if ref_set is not None and len(ref_set) > 0:
        ref_x = [obj[0] if isinstance(obj, (list, tuple)) else obj.objectives[0] for obj in ref_set]
        ref_y = [obj[1] if isinstance(obj, (list, tuple)) else obj.objectives[1] for obj in ref_set]
        
        if n_objectives >= 3:
            ref_z = [obj[2] if isinstance(obj, (list, tuple)) else obj.objectives[2] for obj in ref_set]
            ax.scatter(ref_x, ref_y, ref_z, c='black', marker='x', s=50, label='Reference Front (True)', alpha=0.5)
        else:
            ax.scatter(ref_x, ref_y, c='black', marker='x', s=50, label='Reference Front (True)', alpha=0.5)

    # --- 2. Plot Algorithm Fronts ---
    markers = ['o', 's', '^', 'D', 'v', '<', '>']
    for idx, (algo_name, solutions) in enumerate(results_dict.items()):
        x = [s.objectives[0] for s in solutions]
        y = [s.objectives[1] for s in solutions]
        marker_style = markers[idx % len(markers)]

        if n_objectives >= 3:
            z = [s.objectives[2] for s in solutions]
            ax.scatter(x, y, z, marker=marker_style, s=50, label=algo_name, alpha=0.85, edgecolors='k', linewidths=0.5)
            ax.set_zlabel(objective_names[2], fontsize=11, labelpad=8)
        else:
            ax.scatter(x, y, marker=marker_style, s=70, label=algo_name, alpha=0.85, edgecolors='k', linewidths=0.6)

    # --- 3. Formatting ---
    ax.set_title(f"Multi-Algorithm Pareto Front Comparison ({problem_name})", fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel(objective_names[0], fontsize=11)
    ax.set_ylabel(objective_names[1], fontsize=11)
    ax.legend(title="Algorithms", loc='best', frameon=True, facecolor='white', edgecolor='lightgray')
    
    if n_objectives < 3:
        ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved static overlay plot successfully to: {save_path}")
    else:
        plt.show()
    
    plt.close()

