import numpy as np
import re
import matplotlib.pyplot as plt
import networkx as nx
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus

# Mapping from encoded feature names to actual feature names


def create_sig(columns, encoded_rules):
    feature_mapping = {f"FEAT_{i}": feature for i, feature in enumerate(columns)}

    # Initialize edge weights
    edge_weights = {}

    # Debug: Check rule extraction and feature matching
    for rule_text in encoded_rules:
        # Extract the features and thresholds
        conditions = re.findall(r'FEAT_(\d+)_\w+_([\d\.]+)', rule_text)
        
        # Debug: Print the extracted features and thresholds
        print(f"Rule: {rule_text}")
        print(f"Extracted Conditions: {conditions}")

        # Map FEAT_0, FEAT_1, ... back to actual feature names in the dataset
        features_in_rule = [feature_mapping[f"FEAT_{cond[0]}"] for cond in conditions if f"FEAT_{cond[0]}" in feature_mapping]

        # Debug: Print the features that match the dataset
        print(f"Matching Features: {features_in_rule}")

        # If features are valid, build the edges
        if len(features_in_rule) > 1:
            for i in range(len(features_in_rule) - 1):
                edge = (features_in_rule[i], features_in_rule[i+1])
                edge_weights[edge] = edge_weights.get(edge, 0) + 1

    # Create a directed graph using networkx
    G = nx.DiGraph()

    # Add edges and their weights to the graph
    for (f_from, f_to), weight in edge_weights.items():
        G.add_edge(f_from, f_to, weight=weight)


    # Create a reversed graph (H) with negated weights for minimum spanning arborescence
    H = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        H.add_edge(u, v, weight=-d['weight'])

    # Compute the Minimum Spanning Arborescence (MSA)
    if len(list(H.nodes())) > 0:
        root = list(H.nodes())[0]  # Choose an arbitrary root node
        msa = nx.minimum_spanning_arborescence(H)

        # Revert the edge weights to positive after the spanning tree computation
        for u, v, d in msa.edges(data=True):
            d['weight'] = -d['weight']
        
        # Plot the graph
        plt.figure(figsize=(20, 20))
        pos = nx.circular_layout(msa)  # Using circular layout for better visualization
        edge_labels = nx.get_edge_attributes(msa, 'weight')

        # Draw the nodes, edges, and edge labels
        nx.draw(msa, pos, with_labels=True, node_size=21000, node_color="lightcoral", arrowsize=20)
        nx.draw_networkx_edge_labels(msa, pos, edge_labels=edge_labels)

        plt.title("Surrogate Interpretable Graph (MSA) [Un-optimized]")
        plt.show()
    else:
        print("Graph H is empty. No feature transitions were detected.")

    return H

def create_sig_optimized(columns, encoded_rules, max_edges = 20):
    max_edges = max_edges
    # 1. Mapping from encoded feature names to actual feature names
    feature_mapping = {f"FEAT_{i}": feature for i, feature in enumerate(columns)}

    # 2. Define edge weights (using previous code)
    edge_weights = {}

    # Debug: Check rule extraction and feature matching
    for rule_text in encoded_rules:
        # Extract the features and thresholds
        conditions = re.findall(r'FEAT_(\d+)_\w+_([\d\.]+)', rule_text)
        
        # Map FEAT_0, FEAT_1, ... back to actual feature names in the dataset
        features_in_rule = [feature_mapping[f"FEAT_{cond[0]}"] for cond in conditions if f"FEAT_{cond[0]}" in feature_mapping]

        # If features are valid, build the edges
        if len(features_in_rule) > 1:
            for i in range(len(features_in_rule) - 1):
                edge = (features_in_rule[i], features_in_rule[i+1])
                edge_weights[edge] = edge_weights.get(edge, 0) + 1

    # 4. Create MILP problem: maximize sum of weights of selected edges subject to selecting <= max_edges.
    prob = LpProblem("Surrogate_Graph_Selection", LpMaximize)

    # 5. Create a binary variable for each edge in edge_dict
    edge_vars = {edge: LpVariable(f"edge_{edge[0]}_{edge[1]}", cat='Binary')
                for edge in edge_weights.keys()}

    # 6. Objective: maximize total weight of selected edges
    prob += lpSum([edge_weights[edge] * edge_vars[edge] for edge in edge_vars]), "Total_Weight"

    # 7. Constraint: number of selected edges <= max_edges
    prob += lpSum([edge_vars[edge] for edge in edge_vars]) <= max_edges, "EdgeCountConstraint"

    # 8. Solve the MILP problem
    prob.solve()

    print("MILP Status:", LpStatus[prob.status])

    # 9. Extract selected edges from the MILP solution
    # 9. Extract selected edges from the MILP solution
    selected_edges = [edge for edge in edge_vars if edge_vars[edge].value() == 1]
    print("Selected edges for surrogate graph:", selected_edges)


    # 10. Build surrogate graph from selected edges
    G_surrogate = nx.DiGraph()
    for edge in selected_edges:
        G_surrogate.add_edge(edge[0], edge[1], weight=edge_weights[edge])

        plt.figure(figsize=(15, 15))
    pos = nx.circular_layout(G_surrogate)
    edge_labels = nx.get_edge_attributes(G_surrogate, 'weight')
    nx.draw(G_surrogate, pos, with_labels=True, node_size=21000, node_color="lightgreen", arrowsize=20)
    nx.draw_networkx_edge_labels(G_surrogate, pos, edge_labels=edge_labels)
    plt.title("Surrogate Interpretable Graph")
    plt.show()

    return G_surrogate

def beautify(G_surrogate):
    G=G_surrogate
    # Use a perfectly circular layout: nodes equally spaced
    pos = nx.circular_layout(G, scale=1)  # scale=1 keeps radius consistent

    # Extract edge weights
    edge_weights = np.array([data['weight'] for _, _, data in G.edges(data=True)])

    # Normalize edge weights for color mapping
    min_w, max_w = edge_weights.min(), edge_weights.max()
    normalized_weights = (edge_weights - min_w) / (max_w - min_w + 1e-4)

    # Map weights to blue shades
    edge_colors = [plt.cm.Blues(w) for w in normalized_weights]
    # Draw nodes
    plt.figure(figsize=(15,10))

    nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=300, edgecolors='black')

    # Draw edges with equal length and colors mapped to weight
    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=5,  # fixed width
        arrows=True if isinstance(G, nx.DiGraph) else False,
        arrowstyle='-|>',
        min_source_margin=1,
        min_target_margin=1
    )

    # Label positioning around circle (left, right, top, bottom)
    label_pos = {}
    for node, (x, y) in pos.items():
        # Label offset distance
        dx = 0.15  # horizontal offset
        dy = 0.12  # vertical offset

        # Determine quadrant and place label accordingly
        if abs(x) > abs(y):  # More horizontal
            if x > 0:
                offset = (+dx*2.5, 0)  # Right
            else:
                offset = (-dx * 2.3, 0)  # Left with more space to prevent overlap
        else:  # More vertical
            if y > 0:
                offset = (0, dy)  # Top
            else:
                offset = (0, -dy)  # Bottom

        label_pos[node] = (x + offset[0], y + offset[1])
    nx.draw_networkx_labels(G, label_pos, font_size=12)

    # Finalize
    plt.axis('equal')  # ensures the circle looks circular
    plt.axis('off')
    plt.title("Surrogate Interpretable Graph for Alzheimers Dataset", fontsize=14)
    plt.savefig("optimized_surrogate_graph.pdf", format='pdf', bbox_inches='tight', dpi=300)
    plt.show()
