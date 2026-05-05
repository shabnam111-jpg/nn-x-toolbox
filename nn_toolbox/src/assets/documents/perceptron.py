import streamlit as st


def perceptron_docs_page() -> None:
	st.subheader("Perceptron")

	left, center, right = st.columns([1, 2, 1])
	with center:
		st.image(
			"https://miro.medium.com/0%2Am87K4ZlVc1MR_Uvu.jpeg",
			caption="Perceptron intuition",
			width='stretch',
		)

	st.markdown(
		"""
### 1. Introduction

A **Perceptron** is the simplest form of an artificial neural network, inspired by a biological neuron.
It is mainly used for **binary classification** tasks such as Yes/No or 0/1 decisions.

At its core, a perceptron is a **linear decision model** that learns by adjusting weights from data.

---

### 2. Intuition Behind Perceptron

Imagine an air defense officer deciding whether to raise an alert based on:

- Radar signal strength
- Speed of the object
- Altitude

Each factor contributes differently to the final decision, so each gets a different **weight**.
The officer combines all factors and compares the result with a threshold.

That is exactly what a perceptron does:

- Assigns weights to inputs
- Computes a weighted sum
- Applies a decision rule

---

### 3. Components of a Perceptron

1. **Inputs:** $x_1, x_2, x_3, \dots, x_n$
2. **Weights:** $w_1, w_2, w_3, \dots, w_n$
3. **Bias:** $b$ (shifts the decision threshold)
4. **Activation function:** usually a step function for binary output

---

### 4. Mathematical Representation

**Step 1: Weighted Sum**

$$
z = \sum_{i=1}^{n} w_i x_i + b
$$

**Step 2: Activation (Step Function)**

$$
y =
\begin{cases}
1 & \text{if } z \ge 0 \\
0 & \text{if } z < 0
\end{cases}
$$

The activation converts the score $z$ into a binary class label.

---

### 5. Perceptron Learning Rule

The perceptron updates parameters **only when prediction is incorrect**.

**Weight update:**

$$
w_i^{new} = w_i^{old} + \eta (y_{true} - y_{pred})x_i
$$

**Bias update:**

$$
b^{new} = b^{old} + \eta (y_{true} - y_{pred})
$$

Where:

- $\eta$: learning rate (small positive constant)
- $y_{true}$: true label
- $y_{pred}$: predicted label

**Key idea:** learning happens from mistakes.

---

### 6. How It Works (Training Loop)

For each training sample:

1. Compute $z = w \cdot x + b$
2. Predict class using step function
3. Compare prediction with true label
4. If wrong, update $w$ and $b$
5. Repeat over multiple epochs until errors reduce

---

### 7. Decision Boundary

The boundary is defined by:

$$
w_1x_1 + w_2x_2 + \dots + w_nx_n + b = 0
$$

- In 2D: a straight line
- In higher dimensions: a hyperplane

---

### 8. Advantages

- Simple and easy to understand
- Computationally efficient
- Fast to train
- Works well on linearly separable data
- Foundation of modern neural networks

---

### 9. Disadvantages and Limitations

1. Works only for binary classification
2. Uses non-differentiable step activation
3. Cannot model complex nonlinear patterns
4. Does not produce probability outputs
5. Fails on non-linearly separable tasks (for example, XOR)

---

### 10. Why It Still Matters

The perceptron introduced core ideas used everywhere in deep learning:

- Weighted inputs
- Bias term
- Decision boundary
- Learning from error

It is the conceptual starting point for MLPs, CNNs, and RNNs.

---

### 11. One-Line Exam Summary

> A perceptron is a single-layer neural network for binary classification that learns a linear decision boundary using weighted inputs, bias, and a step activation function.
"""
	)

	st.latex(
		r"""
y =
\begin{cases}
1 & \text{if } z \ge 0 \\
0 & \text{if } z < 0
\end{cases}
"""
	)

	# st.info(
	# 	"Next topics: XOR problem (with diagram), why sigmoid replaced step function, "
	# 	"how perceptron evolved into MLP, or a code-level walkthrough."
	# )
