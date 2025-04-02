## **NLP Approach for Rule-Based Clustering in Random Forest Interpretability**  

We leveraged **Natural Language Processing (NLP)** techniques to extract, encode, and cluster decision rules from a **Random Forest (RF) classifier**, transforming them into a structured **feature interaction graph**. This approach ensures a global understanding of the model’s decision-making process by capturing feature interactions across multiple decision trees.

---

## **1. Rule Extraction: Converting Decision Trees into Textual Representations**  
Each decision tree in the **Random Forest** follows a **set of conditions** in the form of:  
\[
\text{IF (Feature} \, X \leq T_1) \, \text{AND (Feature} \, Y > T_2) \, \text{THEN Class C}
\]
- These conditions are extracted **directly from each decision tree** using traversal methods.
- The extracted rules **preserve logical structures** with comparison operators (`<=`, `>`) and Boolean operators (`AND`, `OR`).

Example extracted rule:  
```
(FEAT_8_LTE_0.09) AND (FEAT_26_LTE_18.64) AND (FEAT_20_GT_957.45)
```

---

## **2. Label Encoding: Standardizing Feature Representation**  
### **Why Label Encoding?**  
- In real-world datasets, features are named semantically (e.g., `Blood_Pressure`, `Glucose_Level`), which adds complexity when comparing rules.
- To ensure consistency, we **convert all feature names into numerical labels** (`FEAT_x`) while **preserving structure**.

### **Encoding Process:**  
- Assign each unique feature a label using **LabelEncoder**.
- Transform feature names to **standardized tokens**:  
  - `Blood_Pressure` → `FEAT_3`
  - `Glucose_Level` → `FEAT_7`

Encoded rule:  
```
(FEAT_3_LTE_120) AND (FEAT_7_GT_5.6)
```

---

## **3. Tokenization: Structuring Rules for NLP Processing**  
Tokenization is a crucial step to separate **features, operators, and threshold values** for further processing.  

For the rule:  
```
(FEAT_8_LTE_0.09) AND (FEAT_26_LTE_18.64) AND (FEAT_20_GT_957.45)
```
### **Tokenized output:**
```
[ 'FEAT_8', 'LTE', '0.09', 'AND', 'FEAT_26', 'LTE', '18.64', 'AND', 'FEAT_20', 'GT', '957.45']
```
- **Operators (`LTE`, `GT`)** are preserved as tokens.
- **Threshold values (`0.09`, `18.64`)** are treated as part of the rule structure.
- **Boolean connectors (`AND`, `OR`)** maintain logical dependencies.

---

## **4. Rule Representation via TF-IDF Encoding**  
### **Why TF-IDF?**
Once tokenized, rules are treated as **textual documents**, where each rule represents a "sentence" in a corpus.  
To numerically represent these rules for clustering, we use **Term Frequency - Inverse Document Frequency (TF-IDF)**.

\[
\text{TF-IDF} = \text{TF} \times \text{IDF}
\]

- **TF (Term Frequency):** Measures how often a token appears in a rule.
- **IDF (Inverse Document Frequency):** Weighs tokens based on how common or rare they are across all rules.

### **Example TF-IDF Matrix (Simplified)**  
| Rule ID | FEAT_8 | LTE | 0.09 | AND | FEAT_26 | LTE | 18.64 | FEAT_20 | GT | 957.45 |
|---------|--------|-----|------|-----|---------|-----|------|---------|----|--------|
| Rule 1  | 0.5    | 0.3 | 0.2  | 0.1 | 0.5     | 0.3 | 0.2  | 0.5     | 0.3 | 0.2    |
| Rule 2  | 0.2    | 0.3 | 0.1  | 0.1 | 0.7     | 0.3 | 0.2  | 0.6     | 0.3 | 0.1    |

- Features with **higher TF-IDF values** contribute more **strongly to decision-making**.
- **Frequent patterns** are captured, while rare ones get downweighted.

---

## **5. Rule Clustering Using Hierarchical Clustering**  
Once encoded, rules are **vectorized** and **clustered** using **Agglomerative Clustering** based on their cosine similarity.

### **Clustering Strategy**
- **Cosine Similarity**: Measures **angular distance** between rule vectors (more robust than Euclidean distance for high-dimensional data).
- **Linkage Strategy**: `average` linkage merges clusters based on mean pairwise distances.
- **Number of Clusters (`n_clusters`)**: Empirically set to balance **overfitting (too many clusters)** vs **underfitting (too few clusters)**.

\[
\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}
\]

Example clustering result:  
**Cluster 1:**
- `(FEAT_8_LTE_0.09) AND (FEAT_26_LTE_18.64)`
- `(FEAT_8_LTE_0.09) AND (FEAT_26_GT_18.64)`

**Cluster 2:**
- `(FEAT_8_GT_0.09) AND (FEAT_25_LTE_102.25)`
- `(FEAT_8_GT_0.09) AND (FEAT_25_GT_102.25)`

Clustering ensures:
- **Rules with similar conditions group together**.
- **Overlapping decision paths are merged**, improving interpretability.

---

## **6. Converting Clustered Rules into a Surrogate Interpretable Graph**  
After clustering, we transform **feature interactions** into a **directed weighted graph**:

### **Graph Construction Steps**
1. **Extract feature transitions** from rules:
   ```
   (FEAT_8 → FEAT_26) → FEAT_20
   ```
2. **Edge weight** = Frequency of co-occurrence in clustered rules.
3. **Use MILP (Mixed-Integer Linear Programming) to optimize graph sparsity**:
   - **Constraint:** Maximum `k` edges to avoid clutter.
   - **Objective:** Preserve most informative connections.

**Final Graph:**
- **Nodes = Features**
- **Edges = Conditional transitions (weighted by frequency)**
- **Graph interpretation:** Features central to predictions have high connectivity.

---

## **7. Final Outcome: A Scalable Interpretability Framework**  
🔹 **Extracts transparent, interpretable rules from RF models**  
🔹 **Clusters similar rules to prevent redundancy**  
🔹 **Uses NLP (TF-IDF + Cosine Similarity) to structure rule space**  
🔹 **Builds a directed graph that preserves global feature interactions**  
🔹 **MILP-based graph sparsification ensures clarity**  
