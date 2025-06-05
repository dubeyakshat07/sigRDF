import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import _tree
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus, value
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder


def get_decision_paths(model, X):
    decision_paths = []
    
    # Iterate over each tree in the forest
    for tree in model.estimators_:
        tree_paths = extract_tree_paths(tree, X)
        decision_paths.append(tree_paths)
    
    return decision_paths

def extract_tree_paths(tree, X):
    # Get the decision tree structure
    children_left = tree.tree_.children_left
    children_right = tree.tree_.children_right
    feature = tree.tree_.feature
    threshold = tree.tree_.threshold
    value = tree.tree_.value
    
    paths = []
    
    # For each sample in X, trace the path from root to leaf
    for _, sample in X.iterrows():
        path = []
        node = 0  # Start from the root node
        
        while children_left[node] != children_right[node]:  # Not a leaf node
            feature_index = feature[node]
            threshold_value = threshold[node]
            feature_name = X.columns[feature_index]
            
            # Record the decision (feature, threshold, direction)
            if sample[feature_name] <= threshold_value:
                path.append((feature_name, threshold_value, "left"))
                node = children_left[node]
            else:
                path.append((feature_name, threshold_value, "right"))
                node = children_right[node]
        
        # At the leaf node, record the leaf prediction
        leaf_prediction = np.argmax(value[node])
        paths.append((path, leaf_prediction))
    
    return paths


# Function to extract decision paths/rules
def extract_rule_paths(tree, feature_names):
    tree_ = tree.tree_
    feature = tree_.feature
    threshold = tree_.threshold
    rules = []

    def recurse(node, current_rule):
        if tree_.children_left[node] == _tree.TREE_LEAF:
            rule_str = " AND ".join(current_rule)
            rules.append(rule_str)
        else:
            rule_left = f"({feature_names[feature[node]]} <= {threshold[node]:.2f})"
            current_rule.append(rule_left)
            recurse(tree_.children_left[node], current_rule)
            current_rule.pop()

            rule_right = f"({feature_names[feature[node]]} > {threshold[node]:.2f})"
            current_rule.append(rule_right)
            recurse(tree_.children_right[node], current_rule)
            current_rule.pop()

    recurse(0, [])
    return rules

