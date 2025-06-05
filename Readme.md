## **1. Overcoming the Limitations of Decision Path Analysis in Random Forest**
### **Existing Decision Path Methods Are Limited**
While we can extract decision paths from the Random Forest, these methods **only tell us how a specific instance is classified** but fail to provide a **global understanding** of how the model behaves as a whole.

- **Instance-Specific Insights Only**: Decision paths typically focus on **one data point at a time**, which means we do not get a clear picture of the **general decision-making patterns** across all trees.
- **High Variability**: Each tree in the Random Forest may have different paths, leading to inconsistencies in interpretation.
- **No Feature Interaction Visualization**: We cannot see how different features interact across multiple trees to contribute to a final decision.

Thus, **decision path analysis alone does not provide a holistic or human-friendly understanding of how features work together** in an ensemble model.

---

## **2. Why Study Rule Extraction from Sub-Trees?**
### **A More Transparent Understanding of Decision Making**
Extracting **decision rules from sub-trees** allows us to:
- **Capture Local Decisions**: Rules extracted from individual decision trees show the conditions under which a sample is classified. 
- **Analyze Feature Importance Locally**: Instead of just a feature importance score from the whole model, we see **why a feature is important at specific decision points**.
- **Provide Explainability at a Granular Level**: Instead of relying on a single surrogate model, we analyze the raw logic used within the ensemble.

### **Why Not Just Extract Rules from the Whole Random Forest?**
Extracting rules directly from the **entire** Random Forest classifier does not give us meaningful insights because:
1. **Rules Become Too Complex**: With hundreds of trees, the rule set becomes too large and unmanageable.
2. **Contradictory Rules**: Different trees may have conflicting rules, making direct interpretation harder.
3. **Feature Interactions Are Hard to See**: Individual trees do not always show how features interact across the whole forest.

Instead, extracting **rules from sub-trees**, then **clustering them**, helps us find **patterns and common decision-making structures** within the model.

---

## **3. Why Build the Interpretable Surrogate Graph?**
### **The Random Forest Is Not Naturally Interpretable**
- Random Forest **consists of multiple decision trees** that collectively make a prediction.
- We cannot visualize all trees at once, making it hard to understand feature **interactions** globally.
- The ensemble nature **hides how individual trees contribute** to the final decision.

### **Graph Representation Helps Us Understand Global Structure**
The **interpretable surrogate graph** serves as a **structural blueprint** of how features interact across the entire Random Forest.

#### **What We Gain from the Surrogate Graph**
✅ **Capturing Global Feature Interactions**:  
- Unlike single decision paths, a graph **aggregates** how features interact across all trees.  
- **Nodes** represent features, and **edges** represent decision relationships learned by the model.

✅ **Identifying the Most Important Relationships**:  
- We can **quantify feature interactions** based on how often two features appear together in decision rules.
- This helps identify **dominant decision patterns** rather than just relying on feature importance scores.

✅ **Optimizing and Simplifying Interpretability**:  
- By applying **Mixed Integer Linear Programming (MILP) optimization**, we can **prune unnecessary connections** and highlight only the **most crucial feature relationships**.  
- This allows us to remove noise and present a **concise yet powerful** explanation of the model.

✅ **A More Trustworthy, Human-Friendly Model Representation**:  
- Instead of just a long list of extracted rules, a graph-based approach provides a **visual and structured** way to communicate how decisions are made.
- This is useful for **regulatory applications, medical AI, finance, and critical decision-making models** where trust is important.

---

## **4. Why Cluster Extracted Rules?**
Extracting rules from every tree in the Random Forest leads to a **large number of overlapping and redundant rules**. **Clustering them helps to**:

- **Group Similar Decision Rules**: Instead of analyzing thousands of rules, we **summarize them into a few clusters** that represent key decision patterns.
- **Understand the Most Common Decision Strategies**: Some trees may follow a similar decision logic. Clustering helps **reveal these common strategies**.
- **Reduce Complexity for Interpretation**: Instead of a list of hundreds of rules, we **summarize them into just a few representative ones**.

### **How Is This Better Than Direct Rule Extraction?**
Without clustering, we would end up with **hundreds or thousands of rules** that are:
- Redundant
- Hard to navigate
- Difficult to summarize

Clustering **condenses** these rules, **preserving essential information** while making them easier to analyze.

---

## **5. Why Conduct So Much Experimentation and Research?**
You are essentially asking: **"Why not just use existing methods? Why innovate?"**  
Here’s why Our work is valuable:

### **A. Improving Trust in AI & Random Forest Models**
- AI models, especially ensemble methods, **are often seen as black boxes**.
- Making Random Forest models more interpretable **helps build trust**, especially in fields like healthcare, law, and finance.

### **B. Existing Methods Are Not Enough**
- Traditional decision trees and feature importance methods **oversimplify** model behavior.
- Our approach provides **more detailed, structured, and interactive explanations**.

### **C. Advancing the State of Explainable AI (XAI)**
- Explainable AI is an evolving field.
- Our research **expands existing methodologies** by combining multiple interpretability techniques (rule extraction, clustering, MILP optimization, and graph-based visualizations).
- This can lead to **new breakthroughs** in model transparency.
---

## Conclusion:
✅ **Going beyond decision paths**: Individual decision paths are limited; global interpretability requires deeper insights.  
✅ **Graph representation is powerful**: It enables visualization of complex feature interactions across all trees.  
✅ **Clustering rules helps**: It summarizes thousands of rules into **clear decision strategies**.  
✅ **Optimization via MILP makes things cleaner**: Reducing complexity ensures interpretability without losing essential insights.  
✅ **Our approach advances interpretability research**: By combining multiple interpretability techniques, Our work is making AI **more trustworthy, structured, and practical**.  

In summary: Existing methods are too simple, while our research enhances how we understand complex models.

### 🔍 **What our Surrogate Graph Approach Does**
our method:
1. **Extracts actual paths (rules)** from each tree in the Random Forest.
2. **Creates a global feature interaction graph**, where:
   - Nodes = Features.
   - Edges = Interactions (based on average usage and co-occurrence across subtrees).
   - Prunes edges based on `max_edges_per_node` for clarity.
3. **Clusters and summarizes rules** for interpretability.
4. **Builds a surrogate decision tree** from these summarized rules for global reasoning.

---

## 🔄 Comparison: **sigRDF** vs. **TreeSHAP**

| **Aspect**                  | **sigRDF (Surrogate Interpretable Graph)**                                            | **TreeSHAP**                                                             |
| --------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| **Transparency**            | ✅ High – Extracts and visualizes actual decision rules and feature paths.            | ⚠️ Medium – Provides additive attributions without exposing rule logic.  |
| **Structure Awareness**     | ✅ Preserves the full path, split logic, and feature hierarchy from decision trees.   | ⚠️ Ignores underlying tree paths; based on feature marginalization.      |
| **Global Interpretability** | ✅ Excellent – Shows how features co-occur, dominate, and interact across the forest. | ⚠️ Moderate – Pairwise interactions only; lacks full structural context. |
| **Rule-Based**              | ✅ Yes – Clusters and summarizes real, interpretable rules from trees.                | ❌ No – Does not provide rule logic or extract decision paths.            |
| **Visual Simplicity**       | ✅ High – Graphs are pruned, layout-optimized, and modular.                           | ⚠️ Limited – Force and dependence plots can be hard to read at scale.    |
| **Faithfulness to Trees**   | ✅ Directly reflects true logic used by trees.                                        | ⚠️ Approximate – Based on game-theoretic surrogates.                     |
| **Customizability**         | ✅ High – Flexible rule depth, clustering, interaction metrics, and layout.           | ❌ Low – Fixed algorithm with minimal parameter tuning.                   |
| **Scalability**             | ✅ Handles high-dimensional data with pruning and abstraction.                        | ⚠️ Can become noisy or intractable on high-dimensional data.             |
| **Interaction Mapping**     | ✅ Builds full feature interaction **DAG** with co-occurrence weights.                | ⚠️ Only shows pairwise interaction heatmaps.                             |

---

### ✅ **Advantages of sigRDF Over TreeSHAP**

1. **Structural Fidelity** – Maintains the original tree structure, making interpretations faithful and auditable.
2. **Human-Centered Design** – Visuals are optimized for interpretability: interaction DAGs, rule clusters, and surrogate simplifications.
3. **Rule Compression** – Transforms a forest into a few summarized, human-readable logic chains.
4. **Flexibility** – Allows domain-specific adjustments: clustering, pruning depth, visual abstraction, etc.

---

### ⚠️ **TreeSHAP Limitations Addressed by sigRDF**

* **TreeSHAP abstracts rules** – It gives numerical attributions but no visibility into decision paths.
* **Limited global view** – TreeSHAP’s interactions are pairwise and don’t scale well globally.
* **Poor auditability** – Attribution values are hard to trace back to specific training logic.
* **Low visual and structural context** – TreeSHAP lacks a structured, topological explanation of feature interactions.

---
If you found this work useful, please consider citing the following research work:

### 📄 Citation

Dubey, A., Anžel, A., & Hattab, G. (2025).
**Surrogate Interpretable Graph for Random Decision Forests**.
*arXiv:2506.01988*.
[https://arxiv.org/abs/2506.01988](https://arxiv.org/abs/2506.01988)

```bibtex
@misc{dubey2025surrogateinterpretablegraphrandom,
  title={Surrogate Interpretable Graph for Random Decision Forests}, 
  author={Akshat Dubey and Aleksandar Anžel and Georges Hattab},
  year={2025},
  eprint={2506.01988},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
  url={https://arxiv.org/abs/2506.01988}
}
```

---