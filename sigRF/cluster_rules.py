from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering

# Step 1: Vectorize the encoded rules using CountVectorizer or TfidfVectorizer
# You can also try TfidfVectorizer


def rulesCluster(encoded_rules, vectorizer="CountVectorizer", showEx = True): 
    
    if vectorizer=="CountVectorizer":
        vectorizer = CountVectorizer()

    elif vectorizer=="TfidfVectorizer":
        vectorizer = TfidfVectorizer()

    encoded_rule_vectors = vectorizer.fit_transform(encoded_rules)

    # Step 2: Perform hierarchical clustering on the vectorized encoded rules
    n_clusters = 5
    clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='cosine', linkage='average')
    labels = clustering.fit_predict(encoded_rule_vectors.toarray())

    # Step 3: Group the rules by their clusters
    clustered_rules = {i: [] for i in range(n_clusters)}
    for encoded_rule, label in zip(encoded_rules, labels):
        clustered_rules[label].append(encoded_rule)

    # Example: Print some clustered rules

    if showEx:
        for cluster_id, rules in clustered_rules.items():
            print(f"Cluster {cluster_id}:")
            for rule in rules[:5]:  # Show first 5 rules in each cluster
                print(f"  {rule}")
            print("\n")

    return labels, clustered_rules
