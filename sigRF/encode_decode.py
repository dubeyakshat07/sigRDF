# Custom rule encoder that preserves the structure
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

def encode_rule_structure(rules, columns):
    encoded_rules = []

    feature_names = columns
    
    # Create a label encoder for feature names (make sure to fit it first)
    feature_encoder = LabelEncoder()
    feature_encoder.fit(feature_names)  # Fit encoder on all feature names
    
    for rule in rules:
        encoded_rule = []
        
        # Split the rule into components and encode
        components = rule.split(" AND ")
        for component in components:
            # Handle the comparison operators and extract feature names
            if "<=" in component:
                feature_name, threshold = component.split(" <= ")
                feature_name = feature_name.strip("()")  # Clean up extra characters
                encoded_rule.append(f"FEAT_{feature_encoder.transform([feature_name])[0]}_LTE_{threshold}")
            elif ">" in component:
                feature_name, threshold = component.split(" > ")
                feature_name = feature_name.strip("()")  # Clean up extra characters
                encoded_rule.append(f"FEAT_{feature_encoder.transform([feature_name])[0]}_GT_{threshold}")
        
        encoded_rules.append(" AND ".join(encoded_rule))
    
    return encoded_rules


# Function to decode an encoded rule
def decode_rule_structure(encoded_rules, columns):
    feature_names = columns
    decoded_rules = []

    # Create a label encoder for feature names (must fit the same encoder used for encoding)
    feature_encoder = LabelEncoder()
    feature_encoder.fit(feature_names)  # Fit encoder on all feature names
    
    for encoded_rule in encoded_rules:
        decoded_rule = []
        
        # Split the encoded rule into components
        components = encoded_rule.split(" AND ")
        
        for component in components:
            # Extract the feature index and threshold from the encoded part
            if "_LTE_" in component:  # Handling "<="
                feature_index, threshold = component.split("_LTE_")
                feature_index = int(feature_index.replace("FEAT_", ""))
                decoded_feature = feature_encoder.inverse_transform([feature_index])[0]  # Decode feature name
                decoded_rule.append(f"({decoded_feature} <= {threshold})")
            elif "_GT_" in component:  # Handling ">"
                feature_index, threshold = component.split("_GT_")
                feature_index = int(feature_index.replace("FEAT_", ""))
                decoded_feature = feature_encoder.inverse_transform([feature_index])[0]  # Decode feature name
                decoded_rule.append(f"({decoded_feature} > {threshold})")
        
        decoded_rules.append(" AND ".join(decoded_rule))
    
    return decoded_rules