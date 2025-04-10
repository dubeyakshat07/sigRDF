
1. **Rule Extraction**
2. **Rule Structure Encoding**
3. **Surrogate Graph Construction**
4. **MILP Optimization of Surrogate Graph**

---

## 🧮 **Time Complexity Analysis**

| Step                          | Description                                                                 | Time Complexity                                      |
|-------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------|
| **1. Rule Extraction**        | Extract all decision paths (rules) from all subtrees in the Random Forest  | \( O(n_{\text{trees}} \cdot 2^d) \)                   |
| **2. Rule Structure Encoding**| Convert rule strings into structured, encoded format using LabelEncoder     | \( O(R \cdot C) \), where \( R \) is rule count       |
| **3. Surrogate Graph Creation**| Construct graph with features as nodes, edges from co-occurring rule pairs | \( O(R \cdot f^2) \), where \( f \) is number of features |
| **4. MILP Optimization**      | Optimize node/edge selection to prune/simplify the graph                    | \( O(2^R) \) (worst-case; practically heuristic-based) |

---

## 📘 **Symbol & Abbreviation Explanations**

| Symbol / Abbreviation | Meaning                                                                 |
|------------------------|------------------------------------------------------------------------|
| \( n_{\text{trees}} \) | Number of estimators in the Random Forest                              |
| \( d \)                | Maximum depth of each decision tree                                    |
| \( R \)                | Total number of rules extracted from all trees                         |
| \( C \)                | Cost of parsing and encoding a single rule                             |
| \( f \)                | Number of unique features in the dataset                               |
| **MILP**               | Mixed Integer Linear Programming — an optimization method              |
| **Surrogate Graph**    | Graph where nodes are features, and edges represent co-occurrence in rules |

---

## 🔁 **Detailed Step Complexity**

### 1. **Rule Extraction**
- Each tree in the forest has up to \( 2^d \) nodes for depth \( d \)
- Total rules = sum of paths to leaf nodes across all trees  
**⏱ Complexity: \( O(n_{\text{trees}} \cdot 2^d) \)**

---

### 2. **Rule Structure Encoding**
- Each rule is tokenized and features are encoded (e.g., `mean radius <= 12.3` → `FEAT_0_LTE_12.3`)  
**⏱ Complexity: \( O(R \cdot C) \)**

---

### 3. **Surrogate Graph Construction**
- For each rule, determine pairs of features used and add edges to the graph  
- For \( R \) rules and up to \( f \) features per rule  
**⏱ Complexity: \( O(R \cdot f^2) \)** in worst-case

---

### 4. **MILP Optimization**
- The surrogate graph can be pruned using MILP to select a minimal set of nodes/edges covering key rule paths
- MILP is **NP-hard**, but practical solvers use branch-and-bound and heuristics  
**⏱ Worst-case: \( O(2^R) \)**

---

## ⚖️ **Final Time Complexity Summary**

| Step                    | Time Complexity                    |
|-------------------------|-------------------------------------|
| Rule Extraction         | \( O(n_{\text{trees}} \cdot 2^d) \) |
| Rule Encoding           | \( O(R \cdot C) \)                  |
| Graph Construction      | \( O(R \cdot f^2) \)                |
| MILP Optimization       | \( O(2^R) \)                        |

---