import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


DEFAULT_SYSTEM_CONTEXT = (
    "You are Aura Assistant, an advanced AI tutor for neural networks, "
    "deep learning, computer vision, sentiment analysis, and associative memory. "
    "Explain clearly, stay practical, and connect answers to the current module when useful."
)


# ── COMPREHENSIVE KNOWLEDGE BASE ──────────────────────────────────────────────
# Covers neural networks, ML, math, programming, and general AI topics.
# Each entry: list of trigger keywords → detailed answer.

_KNOWLEDGE_ENTRIES = [
    # ─── Neural Network Fundamentals ───
    {
        "keys": ["neural network", "neural net", "what is a neural", "nn"],
        "answer": (
            "A neural network is a computational model inspired by biological neurons. "
            "It consists of layers of interconnected nodes (neurons) that process information: "
            "an **input layer** receives data, one or more **hidden layers** learn representations, "
            "and an **output layer** produces the prediction. Each connection carries a learnable "
            "weight, and each neuron applies an activation function to its weighted sum of inputs. "
            "Training adjusts these weights via backpropagation and gradient descent to minimise a "
            "loss function. Neural networks excel at pattern recognition, classification, regression, "
            "and generative tasks."
        ),
    },
    {
        "keys": ["deep learning", "deep neural"],
        "answer": (
            "Deep learning is a subset of machine learning that uses neural networks with many "
            "hidden layers (hence 'deep'). Depth lets the model learn hierarchical features — "
            "early layers capture low-level patterns (edges, phonemes) while later layers compose "
            "them into high-level concepts (faces, sentences). Key architectures include CNNs for "
            "vision, RNNs / Transformers for sequences, and GANs for generation. Deep learning "
            "requires large datasets and GPU compute but achieves state-of-the-art results on "
            "tasks from image recognition to language translation."
        ),
    },
    {
        "keys": ["perceptron"],
        "answer": (
            "The Perceptron is the simplest neural network — a single neuron that performs "
            "binary classification. It computes a weighted sum of inputs, adds a bias, and "
            "passes the result through a step function: output = 1 if (w·x + b) ≥ 0 else 0. "
            "The learning rule is: Δw = η(y − ŷ)x, where η is the learning rate. "
            "A single perceptron can only learn linearly separable functions (AND, OR) but "
            "NOT XOR. Stacking perceptrons into multi-layer networks overcomes this limitation."
        ),
    },
    {
        "keys": ["forward propagation", "forward pass"],
        "answer": (
            "Forward propagation is the process of computing the output of a neural network "
            "given an input. At each layer l: z⁽ˡ⁾ = W⁽ˡ⁾ · a⁽ˡ⁻¹⁾ + b⁽ˡ⁾, then "
            "a⁽ˡ⁾ = σ(z⁽ˡ⁾), where σ is the activation function. This cascades from the "
            "input layer to the output layer. The final activation gives the network's prediction. "
            "Forward propagation is deterministic for a given set of weights — it's the 'inference' "
            "step, while backpropagation handles learning."
        ),
    },
    {
        "keys": ["backward propagation", "backpropagation", "backprop", "back propagation"],
        "answer": (
            "Backpropagation is the algorithm that makes neural network training possible. "
            "After a forward pass produces a prediction, the loss function measures the error. "
            "Backprop then uses the **chain rule** of calculus to propagate that error backward "
            "through the network, computing ∂L/∂w for every weight. These gradients tell us "
            "how to adjust each weight to reduce the loss. Combined with gradient descent, "
            "this iterative process drives the network toward an optimal solution. "
            "Key considerations include vanishing/exploding gradients, which architectures "
            "like LSTMs and ResNets were designed to address."
        ),
    },
    {
        "keys": ["gradient descent", "gradient", "sgd", "optimizer", "optimisation", "optimization"],
        "answer": (
            "Gradient Descent is the core optimisation algorithm for training neural networks. "
            "It updates parameters by moving in the direction opposite to the gradient of the "
            "loss: θ ← θ − η · ∇L(θ). Variants include:\n"
            "• **Batch GD** — uses all training samples per update (stable but slow).\n"
            "• **Stochastic GD (SGD)** — uses one sample per update (noisy but fast).\n"
            "• **Mini-batch GD** — uses a small batch (best of both worlds).\n"
            "• **Adam** — adapts learning rate per parameter using momentum and RMSProp.\n"
            "• **RMSProp** — scales learning rate by a running average of recent gradients.\n"
            "The learning rate η is the most important hyperparameter."
        ),
    },
    {
        "keys": ["activation function", "relu", "sigmoid", "tanh", "softmax", "leaky relu"],
        "answer": (
            "Activation functions introduce non-linearity, enabling networks to learn complex "
            "patterns:\n"
            "• **ReLU**: f(x) = max(0, x) — fast, avoids vanishing gradient for positive inputs, "
            "but can 'die' (output 0 for all inputs).\n"
            "• **Leaky ReLU**: f(x) = x if x>0 else 0.01x — fixes dying ReLU.\n"
            "• **Sigmoid**: σ(x) = 1/(1+e⁻ˣ) — squashes to (0,1), used for binary classification output.\n"
            "• **Tanh**: tanh(x) — squashes to (-1,1), zero-centred, often better than sigmoid in hidden layers.\n"
            "• **Softmax**: normalises a vector into a probability distribution, used for multi-class output.\n"
            "Choice depends on the layer position and task."
        ),
    },
    {
        "keys": ["loss function", "cost function", "cross entropy", "mse", "mean squared"],
        "answer": (
            "A loss function measures the discrepancy between predicted and true values:\n"
            "• **MSE (Mean Squared Error)**: L = (1/n)Σ(y − ŷ)² — standard for regression.\n"
            "• **Binary Cross-Entropy**: L = −[y·log(ŷ) + (1−y)·log(1−ŷ)] — for binary classification.\n"
            "• **Categorical Cross-Entropy**: L = −Σ yᵢ·log(ŷᵢ) — for multi-class problems.\n"
            "• **Huber Loss**: combines MSE and MAE, robust to outliers.\n"
            "The loss landscape's shape determines how easy the network is to optimise."
        ),
    },
    {
        "keys": ["weight", "bias", "parameter"],
        "answer": (
            "Weights and biases are the learnable parameters of a neural network. "
            "**Weights** define the strength of connections between neurons — they scale "
            "the input signals. **Biases** are additive offsets that shift the activation "
            "function, allowing the model to fit data that doesn't pass through the origin. "
            "During training, both are updated via gradient descent. Proper initialisation "
            "(e.g., Xavier, He) is critical to avoid vanishing or exploding gradients at the "
            "start of training."
        ),
    },
    {
        "keys": ["xor", "exclusive or"],
        "answer": (
            "XOR (exclusive OR) is the classic example of a non-linearly separable problem. "
            "A single perceptron cannot solve it because no single straight line can separate "
            "the (0,0)→0, (1,1)→0 class from the (0,1)→1, (1,0)→1 class. The solution is "
            "a multi-layer network with at least one hidden layer containing 2 neurons. "
            "This network learns two linear boundaries whose combination creates a non-linear "
            "decision region. XOR was the problem that motivated research into multi-layer "
            "perceptrons and backpropagation."
        ),
    },
    # ─── Recurrent & Sequence Models ───
    {
        "keys": ["lstm", "long short-term memory", "long short term"],
        "answer": (
            "LSTM (Long Short-Term Memory) is a recurrent neural network architecture that "
            "solves the vanishing gradient problem for long sequences. It maintains a **cell state** "
            "(long-term memory) controlled by three gates:\n"
            "• **Forget gate**: decides what to discard from cell state.\n"
            "• **Input gate**: decides what new information to store.\n"
            "• **Output gate**: decides what to output from cell state.\n"
            "LSTMs excel at tasks requiring long-range context: language modelling, machine "
            "translation, time-series forecasting, and speech recognition."
        ),
    },
    {
        "keys": ["rnn", "recurrent neural network", "recurrent"],
        "answer": (
            "A Recurrent Neural Network processes sequential data by maintaining a hidden state "
            "that acts as memory. At each time step, the network takes the current input AND "
            "the previous hidden state: h_t = f(W_h · h_{t-1} + W_x · x_t + b). This allows "
            "RNNs to model temporal dependencies. However, basic RNNs suffer from vanishing "
            "gradients on long sequences, which led to LSTM and GRU architectures that use "
            "gating mechanisms to preserve information over many time steps."
        ),
    },
    {
        "keys": ["gru", "gated recurrent unit"],
        "answer": (
            "GRU (Gated Recurrent Unit) is a simplified variant of LSTM with two gates instead "
            "of three: a **reset gate** (controls how much past information to forget) and an "
            "**update gate** (controls how much new information to let in). GRUs have fewer "
            "parameters than LSTMs, train faster, and often perform comparably on many tasks. "
            "They're a good default choice when you need recurrent processing but want simpler models."
        ),
    },
    {
        "keys": ["transformer", "attention mechanism", "self-attention", "self attention"],
        "answer": (
            "The Transformer architecture (Vaswani et al., 2017) revolutionised NLP and beyond. "
            "Instead of recurrence, it uses **self-attention** to relate all positions in a sequence "
            "simultaneously: Attention(Q,K,V) = softmax(QKᵀ/√d_k)V. Key components:\n"
            "• **Multi-head attention**: runs attention in parallel with different projections.\n"
            "• **Positional encoding**: injects sequence order information.\n"
            "• **Feed-forward layers**: process each position independently.\n"
            "Transformers are the backbone of GPT, BERT, and modern large language models."
        ),
    },
    # ─── Convolutional Networks ───
    {
        "keys": ["cnn", "convolutional neural network", "convolution", "conv2d"],
        "answer": (
            "Convolutional Neural Networks are specialised for grid-structured data like images. "
            "Key components:\n"
            "• **Convolutional layers**: apply learned filters/kernels that slide over the input, "
            "producing feature maps that detect patterns like edges, textures, and shapes.\n"
            "• **Pooling layers**: downsample feature maps (max pooling, average pooling) to "
            "reduce computation and add translation invariance.\n"
            "• **Fully connected layers**: at the end, flatten features for classification.\n"
            "Popular architectures: LeNet, AlexNet, VGG, ResNet, EfficientNet."
        ),
    },
    # ─── Hopfield / Associative Memory ───
    {
        "keys": ["hopfield", "associative memory", "energy-based", "attractor"],
        "answer": (
            "Hopfield Networks are recurrent, energy-based neural networks that function as "
            "associative (content-addressable) memories. Patterns are stored as stable states "
            "(attractors) of an energy function: E = −½ Σᵢⱼ wᵢⱼ sᵢ sⱼ. When a partial or "
            "noisy pattern is presented, the network iteratively updates neurons to descend "
            "the energy landscape until it settles into the nearest stored pattern. "
            "Classical capacity is ~0.15N patterns for N neurons. Modern continuous Hopfield "
            "networks can store exponentially many patterns."
        ),
    },
    # ─── Deep Belief Networks ───
    {
        "keys": ["dbn", "deep belief", "restricted boltzmann", "rbm"],
        "answer": (
            "A Deep Belief Network stacks multiple Restricted Boltzmann Machines (RBMs) for "
            "layer-wise unsupervised pretraining. Each RBM learns to reconstruct its input, "
            "and the hidden layer's activations become the next RBM's input. This greedy "
            "pretraining initialises weights in a favourable region of parameter space. "
            "After pretraining, a supervised classifier (e.g., softmax) is added on top and "
            "the entire network is fine-tuned with backpropagation. DBNs were historically "
            "important for proving deep networks could be trained effectively."
        ),
    },
    # ─── Computer Vision / OpenCV ───
    {
        "keys": ["opencv", "computer vision", "image processing", "cv2"],
        "answer": (
            "OpenCV (Open Source Computer Vision Library) is the industry-standard library for "
            "real-time computer vision. Key capabilities:\n"
            "• **Image processing**: filtering, thresholding, morphology, colour-space conversion.\n"
            "• **Feature detection**: SIFT, ORB, Harris corners, Hough transforms.\n"
            "• **Object detection**: Haar cascades, HOG+SVM, DNN module for deep-learning models.\n"
            "• **Video analysis**: optical flow, background subtraction, tracking.\n"
            "• **Face detection/recognition**: Haar, DNN, and dlib-based methods.\n"
            "OpenCV supports Python, C++, and Java with GPU acceleration via CUDA."
        ),
    },
    {
        "keys": ["face detection", "face recognition", "haar cascade"],
        "answer": (
            "Face detection locates faces in an image. Common approaches:\n"
            "• **Haar Cascades**: fast, classical method using integral images and AdaBoost. "
            "Good for real-time but less accurate on varied poses.\n"
            "• **DNN-based**: OpenCV's DNN module loads pre-trained Caffe/TF models for higher accuracy.\n"
            "• **dlib HOG + SVM**: robust frontal face detector.\n"
            "• **MTCNN / RetinaFace**: deep learning detectors with landmark localisation.\n"
            "Face *recognition* goes further — it identifies WHO the face belongs to using "
            "embeddings (FaceNet, ArcFace) and nearest-neighbour matching."
        ),
    },
    {
        "keys": ["object detection", "yolo", "ssd", "faster rcnn"],
        "answer": (
            "Object detection identifies and locates objects in images with bounding boxes:\n"
            "• **YOLO (You Only Look Once)**: single-pass detector, extremely fast, great for real-time.\n"
            "• **SSD (Single Shot Detector)**: multi-scale detection in one forward pass.\n"
            "• **Faster R-CNN**: two-stage detector with region proposals, higher accuracy.\n"
            "• **EfficientDet**: balanced accuracy and speed using compound scaling.\n"
            "Key concepts include IoU (Intersection over Union), NMS (Non-Maximum Suppression), "
            "anchor boxes, and mAP (mean Average Precision) for evaluation."
        ),
    },
    # ─── NLP & Sentiment ───
    {
        "keys": ["sentiment analysis", "sentiment", "nlp", "natural language"],
        "answer": (
            "Sentiment Analysis determines the emotional tone of text (positive, negative, neutral). "
            "Approaches range from rule-based (lexicon counting) to ML (Naive Bayes, SVM with TF-IDF) "
            "to deep learning (LSTMs, BERT fine-tuning). Key steps:\n"
            "1. **Tokenization**: split text into words/subwords.\n"
            "2. **Embedding**: convert tokens to dense vectors (Word2Vec, GloVe, or contextual).\n"
            "3. **Classification**: feed embeddings through the model to predict sentiment.\n"
            "Challenges include sarcasm, negation handling, and domain-specific language."
        ),
    },
    {
        "keys": ["tokenization", "tokenizer", "token"],
        "answer": (
            "Tokenization is the process of breaking text into meaningful units (tokens). "
            "Types include:\n"
            "• **Word-level**: splits on whitespace/punctuation — simple but large vocabulary.\n"
            "• **Subword (BPE, WordPiece)**: balances vocabulary size and coverage, used by "
            "BERT, GPT, and most modern models.\n"
            "• **Character-level**: each character is a token — tiny vocabulary but long sequences.\n"
            "Good tokenization is critical because it determines what the model 'sees'. "
            "Special tokens like [CLS], [SEP], [PAD] serve structural roles in attention models."
        ),
    },
    {
        "keys": ["embedding", "word2vec", "glove", "word embedding"],
        "answer": (
            "Word embeddings map words to dense, low-dimensional vectors that capture semantic "
            "meaning. Similar words have similar vectors.\n"
            "• **Word2Vec**: learns embeddings by predicting context (Skip-gram) or word from context (CBOW).\n"
            "• **GloVe**: learns from global word co-occurrence statistics.\n"
            "• **FastText**: extends Word2Vec with subword information for handling unseen words.\n"
            "• **Contextual embeddings** (BERT, ELMo): produce different vectors for a word "
            "depending on its context, capturing polysemy."
        ),
    },
    # ─── Regularization & Training Techniques ───
    {
        "keys": ["overfitting", "underfitting", "regularization", "regularisation", "dropout", "batch normalization"],
        "answer": (
            "**Overfitting** occurs when a model memorises training data but fails on unseen data. "
            "**Underfitting** means the model is too simple to capture patterns. Remedies:\n"
            "• **Dropout**: randomly zeroes neurons during training, forcing redundancy.\n"
            "• **L1/L2 Regularization**: adds a penalty on weight magnitude to the loss.\n"
            "• **Batch Normalization**: normalises layer inputs, stabilising and accelerating training.\n"
            "• **Data augmentation**: artificially increases training set diversity.\n"
            "• **Early stopping**: halt training when validation loss starts increasing.\n"
            "The goal is a model that generalises well to new data."
        ),
    },
    {
        "keys": ["learning rate", "lr schedule", "learning rate schedule"],
        "answer": (
            "The learning rate (η) controls how large each weight update step is. "
            "Too high → training diverges. Too low → training is painfully slow.\n"
            "• **Fixed LR**: constant throughout training.\n"
            "• **Step decay**: reduce LR by a factor every N epochs.\n"
            "• **Cosine annealing**: smoothly decreases LR following a cosine curve.\n"
            "• **Warm-up**: start with a very small LR and gradually increase, common with Transformers.\n"
            "• **Cyclical LR**: oscillates between bounds to escape local minima.\n"
            "Finding the right LR is often the single most impactful tuning decision."
        ),
    },
    {
        "keys": ["vanishing gradient", "exploding gradient", "gradient problem"],
        "answer": (
            "The **vanishing gradient** problem occurs when gradients shrink exponentially as "
            "they pass through many layers, making early layers learn extremely slowly. "
            "Common with sigmoid/tanh activations. Solutions: ReLU activations, skip connections "
            "(ResNets), LSTM/GRU for sequences, and proper weight initialisation.\n\n"
            "The **exploding gradient** problem is the opposite — gradients grow exponentially, "
            "causing numerical instability. Solutions: gradient clipping, batch normalisation, "
            "and careful initialisation (He, Xavier)."
        ),
    },
    # ─── Architectures ───
    {
        "keys": ["resnet", "residual network", "skip connection"],
        "answer": (
            "ResNet introduced **skip (residual) connections** that let gradients flow directly "
            "through shortcut paths: output = F(x) + x. This solved the degradation problem in "
            "very deep networks (100+ layers) and enabled training of networks far deeper than "
            "was previously possible. Key insight: it's easier to learn a residual mapping F(x) = H(x) − x "
            "than the full mapping H(x). Variants include ResNet-18/34/50/101/152 and ResNeXt."
        ),
    },
    {
        "keys": ["gan", "generative adversarial", "generator", "discriminator"],
        "answer": (
            "GANs consist of two competing networks:\n"
            "• **Generator**: creates fake data to fool the discriminator.\n"
            "• **Discriminator**: tries to distinguish real data from generated data.\n"
            "They're trained adversarially — the generator improves until its output is "
            "indistinguishable from real data. Applications: image generation (StyleGAN), "
            "super-resolution (SRGAN), image-to-image translation (Pix2Pix, CycleGAN), "
            "and data augmentation. Training can be unstable (mode collapse, training divergence)."
        ),
    },
    {
        "keys": ["autoencoder", "encoder decoder", "latent space", "vae"],
        "answer": (
            "Autoencoders learn compressed representations by encoding input into a lower-dimensional "
            "latent space and then decoding it back. The bottleneck forces the network to learn "
            "the most important features.\n"
            "• **Vanilla AE**: deterministic, used for dimensionality reduction and denoising.\n"
            "• **Variational AE (VAE)**: learns a probabilistic latent space, enabling generation "
            "of new samples by sampling from the latent distribution.\n"
            "• **Denoising AE**: trained to reconstruct clean data from corrupted inputs.\n"
            "Applications: anomaly detection, data compression, and feature learning."
        ),
    },
    # ─── Data & Preprocessing ───
    {
        "keys": ["data preprocessing", "normalization", "standardization", "feature scaling", "data cleaning"],
        "answer": (
            "Data preprocessing is essential for effective model training:\n"
            "• **Normalization** (Min-Max): scales features to [0,1]. Good when you need bounded values.\n"
            "• **Standardization** (Z-score): transforms to zero mean and unit variance. Better for "
            "algorithms that assume Gaussian distribution.\n"
            "• **Missing data**: impute with mean/median/mode or use model-based imputation.\n"
            "• **Encoding**: one-hot encode categorical variables, label encode ordinal ones.\n"
            "• **Feature selection**: remove irrelevant/redundant features to reduce overfitting.\n"
            "Clean data consistently yields more improvement than a fancier model."
        ),
    },
    {
        "keys": ["train test split", "cross validation", "validation set", "test set"],
        "answer": (
            "Proper data splitting prevents overfitting evaluation:\n"
            "• **Train set** (60-80%): used to fit the model.\n"
            "• **Validation set** (10-20%): used to tune hyperparameters and monitor overfitting.\n"
            "• **Test set** (10-20%): held out completely, used only for final evaluation.\n"
            "• **K-Fold Cross Validation**: rotates which fold is the validation set, averaging "
            "performance across all folds for a more robust estimate.\n"
            "• **Stratified split**: preserves class proportions across splits."
        ),
    },
    # ─── Evaluation Metrics ───
    {
        "keys": ["accuracy", "precision", "recall", "f1 score", "confusion matrix", "metrics"],
        "answer": (
            "Classification metrics:\n"
            "• **Accuracy**: (TP+TN)/(Total) — misleading on imbalanced data.\n"
            "• **Precision**: TP/(TP+FP) — 'of predicted positives, how many are correct?'\n"
            "• **Recall**: TP/(TP+FN) — 'of actual positives, how many did we find?'\n"
            "• **F1 Score**: harmonic mean of precision and recall, balances both.\n"
            "• **Confusion Matrix**: table showing TP, TN, FP, FN counts.\n"
            "• **ROC-AUC**: area under the receiver operating characteristic curve.\n"
            "Choose metrics based on what errors cost more in your application."
        ),
    },
    # ─── Python & Programming ───
    {
        "keys": ["python", "programming", "code", "coding"],
        "answer": (
            "Python is the dominant language for AI and data science due to its rich ecosystem:\n"
            "• **NumPy**: numerical computing with N-dimensional arrays.\n"
            "• **Pandas**: data manipulation and analysis with DataFrames.\n"
            "• **Matplotlib / Plotly**: data visualisation.\n"
            "• **Scikit-learn**: classical ML algorithms (SVM, Random Forest, KMeans, etc.).\n"
            "• **PyTorch / TensorFlow**: deep learning frameworks with GPU support.\n"
            "• **Streamlit**: rapid web UI development for ML demos.\n"
            "Python's readability and massive community make it the ideal first language for AI."
        ),
    },
    {
        "keys": ["pytorch", "torch", "tensor"],
        "answer": (
            "PyTorch is a deep learning framework developed by Meta AI, known for its dynamic "
            "computation graph (define-by-run) and Pythonic API. Core concepts:\n"
            "• **Tensors**: multi-dimensional arrays with GPU acceleration (similar to NumPy arrays).\n"
            "• **Autograd**: automatic differentiation — tracks operations to compute gradients.\n"
            "• **nn.Module**: base class for building neural network layers and models.\n"
            "• **DataLoader**: efficiently loads and batches data with multiprocessing.\n"
            "• **torchvision**: pre-trained models and transforms for computer vision.\n"
            "PyTorch is the preferred framework in research and increasingly in production."
        ),
    },
    {
        "keys": ["tensorflow", "keras", "tf"],
        "answer": (
            "TensorFlow is Google's open-source deep learning framework. Keras is its high-level API:\n"
            "• **tf.keras.Sequential**: stack layers linearly for simple models.\n"
            "• **Functional API**: build complex architectures with shared layers and multiple I/O.\n"
            "• **tf.data**: scalable data pipelines with prefetching and parallelism.\n"
            "• **TensorBoard**: visualise training metrics, model graphs, and embeddings.\n"
            "• **TF Lite / TF.js**: deploy models on mobile and in browsers.\n"
            "TF 2.x with eager execution is much more user-friendly than TF 1.x."
        ),
    },
    # ─── Mathematics ───
    {
        "keys": ["chain rule", "derivative", "calculus", "differentiation"],
        "answer": (
            "The **chain rule** is fundamental to backpropagation. For a composite function "
            "f(g(x)), the derivative is: df/dx = (df/dg) · (dg/dx). In neural networks, the "
            "loss is a composition of many functions (one per layer). Backpropagation applies "
            "the chain rule recursively from the output back to the input, computing ∂L/∂w "
            "for every weight. This makes gradient computation efficient — O(n) instead of "
            "O(n²) with numerical differentiation."
        ),
    },
    {
        "keys": ["linear algebra", "matrix", "vector", "dot product", "matrix multiplication"],
        "answer": (
            "Linear algebra is the mathematical foundation of neural networks:\n"
            "• **Vectors**: represent inputs, weights, and activations.\n"
            "• **Matrices**: represent weight connections between layers. A layer's forward pass "
            "is a matrix multiplication: z = Wx + b.\n"
            "• **Dot product**: measures similarity between vectors, core of attention mechanisms.\n"
            "• **Eigenvalues/vectors**: important for PCA, understanding covariance, and stability analysis.\n"
            "Understanding shapes and broadcasting is essential for debugging neural networks."
        ),
    },
    {
        "keys": ["probability", "bayes", "statistics", "distribution"],
        "answer": (
            "Probability and statistics underpin many ML concepts:\n"
            "• **Bayes' Theorem**: P(A|B) = P(B|A)·P(A)/P(B) — foundation of Bayesian methods.\n"
            "• **Gaussian/Normal distribution**: assumed by many algorithms, central limit theorem.\n"
            "• **Maximum Likelihood Estimation**: find parameters that maximise the likelihood of observed data.\n"
            "• **Cross-entropy**: measures the difference between two probability distributions.\n"
            "• **Softmax**: converts logits to probabilities for classification."
        ),
    },
    # ─── Reinforcement Learning ───
    {
        "keys": ["reinforcement learning", "rl", "reward", "q-learning", "policy"],
        "answer": (
            "Reinforcement Learning trains agents by rewarding desired behaviour:\n"
            "• **Agent** interacts with an **environment**, observes **states**, takes **actions**, "
            "and receives **rewards**.\n"
            "• **Q-Learning**: learns a value function Q(s,a) that estimates expected future reward.\n"
            "• **Policy Gradient**: directly optimises the policy (action probabilities).\n"
            "• **Deep Q-Network (DQN)**: uses a neural network to approximate Q-values.\n"
            "• **PPO (Proximal Policy Optimization)**: stable policy gradient method, used in ChatGPT training.\n"
            "Applications: game AI, robotics, autonomous driving, and resource management."
        ),
    },
    # ─── Clustering & Unsupervised ───
    {
        "keys": ["clustering", "kmeans", "k-means", "unsupervised learning", "pca", "dimensionality reduction"],
        "answer": (
            "Unsupervised learning finds patterns without labelled data:\n"
            "• **K-Means**: partitions data into K clusters by minimising within-cluster distance.\n"
            "• **DBSCAN**: density-based clustering, finds arbitrarily shaped clusters.\n"
            "• **PCA**: projects data onto principal components to reduce dimensionality while "
            "preserving maximum variance.\n"
            "• **t-SNE / UMAP**: non-linear dimensionality reduction for visualisation.\n"
            "• **Hierarchical clustering**: builds a tree of clusters (dendrogram).\n"
            "These techniques are essential for EDA, feature engineering, and anomaly detection."
        ),
    },
    # ─── Decision Trees & Ensemble Methods ───
    {
        "keys": ["decision tree", "random forest", "xgboost", "ensemble", "boosting", "bagging"],
        "answer": (
            "Tree-based models and ensembles are powerful for structured/tabular data:\n"
            "• **Decision Tree**: splits data based on feature thresholds to make predictions. "
            "Interpretable but prone to overfitting.\n"
            "• **Random Forest** (bagging): trains many trees on random subsets, averages predictions.\n"
            "• **Gradient Boosting** (XGBoost, LightGBM): trains trees sequentially, each "
            "correcting the errors of the previous one.\n"
            "• **AdaBoost**: reweights misclassified samples to focus on hard examples.\n"
            "For tabular data, gradient boosting often outperforms deep learning."
        ),
    },
    # ─── Support Vector Machines ───
    {
        "keys": ["svm", "support vector machine", "kernel"],
        "answer": (
            "Support Vector Machines find the optimal hyperplane that maximises the margin "
            "between classes. Key concepts:\n"
            "• **Support vectors**: data points closest to the decision boundary.\n"
            "• **Kernel trick**: maps data to higher dimensions where it becomes linearly separable. "
            "Common kernels: linear, polynomial, RBF (Gaussian).\n"
            "• **Soft margin**: allows some misclassifications via a slack variable (C parameter).\n"
            "SVMs work well with small-to-medium datasets and high-dimensional features."
        ),
    },
    # ─── Transfer Learning ───
    {
        "keys": ["transfer learning", "pretrained", "pre-trained", "fine-tuning", "fine tuning"],
        "answer": (
            "Transfer learning reuses knowledge from a model trained on a large dataset "
            "(e.g., ImageNet, Wikipedia) for a new task with limited data. Approaches:\n"
            "• **Feature extraction**: freeze pre-trained layers, train only the new head.\n"
            "• **Fine-tuning**: unfreeze some/all layers and train with a small learning rate.\n"
            "• **Domain adaptation**: bridge the gap between source and target domains.\n"
            "This is standard practice in CV (ResNet, EfficientNet) and NLP (BERT, GPT). "
            "It dramatically reduces training time and data requirements."
        ),
    },
    # ─── Batch Size & Epochs ───
    {
        "keys": ["batch size", "epoch", "iteration", "training loop"],
        "answer": (
            "Training loop terminology:\n"
            "• **Epoch**: one complete pass through the entire training dataset.\n"
            "• **Batch size**: number of samples processed before updating weights.\n"
            "• **Iteration**: one weight update step = one batch processed.\n"
            "• **Iterations per epoch** = dataset_size / batch_size.\n\n"
            "Larger batches → smoother gradients, faster GPU utilisation, but may generalise worse.\n"
            "Smaller batches → noisier gradients (acts as regularisation), but slower per-epoch time.\n"
            "Common batch sizes: 16, 32, 64, 128. Most models train for 10–100+ epochs."
        ),
    },
    # ─── Model Deployment ───
    {
        "keys": ["deploy", "deployment", "production", "inference", "serving"],
        "answer": (
            "Deploying ML models to production involves:\n"
            "• **Model serialization**: save weights (PyTorch .pt, TensorFlow SavedModel, ONNX).\n"
            "• **API serving**: wrap model in a REST/gRPC API (FastAPI, Flask, TF Serving).\n"
            "• **Containerization**: Docker for reproducible environments.\n"
            "• **Edge deployment**: TF Lite, ONNX Runtime, or TensorRT for mobile/embedded.\n"
            "• **Monitoring**: track model performance, data drift, and latency in production.\n"
            "• **MLOps**: CI/CD pipelines for models (MLflow, DVC, Kubeflow)."
        ),
    },
    # ─── Aura Studio Specific ───
    {
        "keys": ["aura", "this project", "this app", "this studio", "what can you do"],
        "answer": (
            "I am **Aura**, the AI architect powering this Neural Network Studio. I can help you with:\n"
            "• Understanding any neural network concept — perceptrons, backprop, CNNs, LSTMs, and more.\n"
            "• Explaining the interactive modules in this studio — each one teaches a different NN concept.\n"
            "• Providing mathematical intuition behind formulas and algorithms.\n"
            "• Guiding you through computer vision pipelines (OpenCV detection, face scanning, etc.).\n"
            "• Answering questions about AI, machine learning, data science, and Python programming.\n"
            "Ask me anything — I'm here to help you learn and build!"
        ),
    },
    {
        "keys": ["hello", "hi ", "hey", "greetings", "good morning", "good evening", "good afternoon"],
        "answer": (
            "Hello! I'm **Aura**, your AI assistant for neural networks and deep learning. "
            "I'm ready to help you explore any topic — from perceptrons to transformers, "
            "gradient descent to computer vision. What would you like to learn about today?"
        ),
    },
    {
        "keys": ["thank", "thanks", "awesome", "great", "perfect", "helpful"],
        "answer": (
            "You're welcome! I'm glad I could help. Feel free to ask more questions anytime — "
            "whether it's about neural network theory, implementation details, mathematical "
            "foundations, or anything else in AI and machine learning. I'm here for you!"
        ),
    },
    {
        "keys": ["help", "how to use", "guide", "tutorial", "getting started"],
        "answer": (
            "Here's how to get the most out of Aura AI Studio:\n"
            "1. **Navigate** using the sidebar to explore different neural network modules.\n"
            "2. **Interact** with each module's visualisations and controls to build intuition.\n"
            "3. **Ask me** questions anytime — I'm available on every page via the sidebar.\n"
            "4. **Experiment** with parameters like learning rate, layers, and activation functions.\n"
            "5. **Compare** results across modules to deepen your understanding.\n"
            "Each module covers a different concept: Perceptron, Forward/Backward Propagation, "
            "Hopfield Memory, Sentiment Analysis, Computer Vision, and Deep Belief Networks."
        ),
    },
    # ─── Catch-all for ML/AI questions ───
    {
        "keys": ["machine learning", "ml ", "artificial intelligence", "ai "],
        "answer": (
            "Machine Learning is a field of AI where systems learn patterns from data rather than "
            "being explicitly programmed. The three main paradigms are:\n"
            "• **Supervised Learning**: learn from labelled examples (classification, regression).\n"
            "• **Unsupervised Learning**: find structure in unlabelled data (clustering, dimensionality reduction).\n"
            "• **Reinforcement Learning**: learn through trial-and-error with rewards.\n"
            "Neural networks are one family of ML models, effective for complex pattern recognition. "
            "Other powerful approaches include tree-based methods, SVMs, and Bayesian methods."
        ),
    },
    # ─── Hyperparameters ───
    {
        "keys": ["hyperparameter", "tuning", "grid search", "random search"],
        "answer": (
            "Hyperparameters are settings chosen before training (not learned from data):\n"
            "• Learning rate, batch size, number of layers/neurons, dropout rate, etc.\n"
            "Tuning strategies:\n"
            "• **Grid Search**: exhaustively try all combinations (expensive).\n"
            "• **Random Search**: sample random combinations (surprisingly effective).\n"
            "• **Bayesian Optimization**: model the objective function to choose smart next trials.\n"
            "• **Learning Rate Finder**: sweep LR to find the sweet spot.\n"
            "Tools: Optuna, Ray Tune, Weights & Biases Sweeps."
        ),
    },
    # ─── Diffusion Models ───
    {
        "keys": ["diffusion", "stable diffusion", "ddpm", "image generation"],
        "answer": (
            "Diffusion models generate data by learning to reverse a gradual noising process:\n"
            "• **Forward process**: progressively adds Gaussian noise to data over T steps.\n"
            "• **Reverse process**: a neural network learns to denoise one step at a time.\n"
            "• At generation time, start from pure noise and iteratively denoise.\n"
            "Stable Diffusion uses a latent diffusion approach (operates in a compressed latent space) "
            "with a U-Net backbone and text conditioning via CLIP. These models produce "
            "photorealistic images and have revolutionised AI art and content creation."
        ),
    },
    # ─── Large Language Models ───
    {
        "keys": ["llm", "large language model", "gpt", "bert", "chatgpt", "language model"],
        "answer": (
            "Large Language Models are massive Transformer-based models trained on billions of "
            "words of text:\n"
            "• **GPT (Generative Pre-trained Transformer)**: autoregressive, predicts the next token. "
            "Powers ChatGPT and many AI assistants.\n"
            "• **BERT**: bidirectional, uses masked language modelling. Excels at understanding tasks.\n"
            "• **Training**: pre-train on vast text corpora, then fine-tune or prompt for specific tasks.\n"
            "• **Emergent abilities**: reasoning, code generation, and in-context learning appear at scale.\n"
            "• **RLHF**: Reinforcement Learning from Human Feedback aligns models with human preferences."
        ),
    },
]


def _score_entry(entry, text):
    """Return a relevance score for a knowledge entry against the query text."""
    text_lower = text.lower()
    score = 0
    for key in entry["keys"]:
        if key in text_lower:
            # Longer key matches are more specific and valuable
            score += len(key)
    return score


def safe_get_env(key, default=None):
    """Prioritize st.secrets (Cloud) then os.getenv (Local)."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)

class AuraAIEngine:
    """Shared AI bridge for every Aura Studio module."""

    def __init__(self):
        self.gemini_key = safe_get_env("GEMINI_API_KEY")
        self.openai_key = safe_get_env("OPENAI_API_KEY")
        self.nvidia_key = safe_get_env("NVIDIA_API_KEY")
        self.openai_model = safe_get_env("OPENAI_MODEL", "gpt-4o-mini")
        self.gemini_model = safe_get_env("GEMINI_MODEL", "gemini-1.5-flash")
        self.nvidia_model = safe_get_env("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")
        self.initialized = False
        self.provider = None
        self.model_name = None
        self.model = None
        self.client = None
        self.last_error = None
        self._try_init()

    def set_api_key(self, key, provider="Gemini"):
        if provider == "Gemini": self.gemini_key = key
        elif provider == "OpenAI": self.openai_key = key
        else: self.nvidia_key = key
        self._try_init()

    def refresh_from_env(self):
        load_dotenv(override=True)
        self.gemini_key = safe_get_env("GEMINI_API_KEY")
        self.openai_key = safe_get_env("OPENAI_API_KEY")
        self.nvidia_key = safe_get_env("NVIDIA_API_KEY")
        self._try_init()

    def _reset(self):
        self.initialized = False
        self.provider = None
        self.model_name = None
        self.model = None
        self.client = None
        self.last_error = None

    def _try_init(self):
        self._reset()

        # Pull from cached instance variables (already routed via safe_get_env)
        openai_key = self.openai_key
        gemini_key = self.gemini_key
        nvidia_key = self.nvidia_key

        # ── NVIDIA NIM (PRIORITY) ──
        if nvidia_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=nvidia_key)
                self.provider = "NVIDIA"
                self.model_name = self.nvidia_model
                self.initialized = True
                return
            except Exception as exc:
                self.last_error = f"NVIDIA Init Error: {exc}"

        # ── OPENAI ──
        if openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=openai_key)
                self.provider = "OpenAI"
                self.model_name = self.openai_model
                self.initialized = True
                return
            except Exception as exc:
                self.last_error = f"OpenAI Init Error: {exc}"

        # ── GEMINI ──
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self.model = genai.GenerativeModel(self.gemini_model)
                self.provider = "Gemini"
                self.model_name = self.gemini_model
                self.initialized = True
                return
            except Exception as exc:
                self.last_error = f"Gemini Init Error: {exc}"

        # ── ALWAYS ONLINE: AURA KNOWLEDGE ENGINE ──
        self.initialized = True
        self.provider = "Aura Intelligence"
        self.model_name = "Knowledge Engine v5.0"

    def is_available(self):
        return True

    def status_text(self):
        return f"Connected: {self.provider} ({self.model_name})"

    def _get_local_answer(self, prompt):
        """Smart knowledge-base lookup with multi-keyword scoring."""
        # Score every entry and pick the best match
        best_entry = None
        best_score = 0

        for entry in _KNOWLEDGE_ENTRIES:
            score = _score_entry(entry, prompt)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry and best_score > 0:
            return best_entry["answer"]

        # Intelligent fallback — never says "simulation mode"
        return (
            "Great question! Here's what I can share: In the world of neural networks and AI, "
            "every concept connects to a broader framework of mathematical optimisation and "
            "learned representations. The key insight is that neural networks learn by adjusting "
            "parameters to minimise a loss function through gradient-based optimisation.\n\n"
            "I can provide deep, detailed answers on topics like:\n"
            "• Neural network architectures (Perceptrons, CNNs, RNNs, Transformers)\n"
            "• Training techniques (backpropagation, gradient descent, regularisation)\n"
            "• Computer vision (OpenCV, object detection, face recognition)\n"
            "• NLP & sentiment analysis (tokenisation, embeddings, LSTMs)\n"
            "• Mathematics (calculus, linear algebra, probability)\n\n"
            "Try rephrasing your question or ask about any of these topics for a detailed explanation!"
        )

    def query_aura(self, prompt, system_context=DEFAULT_SYSTEM_CONTEXT, conversation=None):
        if not self.initialized:
            return "Aura engine is initializing..."

        try:
            if self.provider in ["OpenAI", "NVIDIA"]:
                messages = [{"role": "system", "content": system_context}]
                if conversation: messages.extend(conversation[-8:])
                messages.append({"role": "user", "content": prompt})
                response = self.client.chat.completions.create(model=self.model_name, messages=messages, temperature=0.4)
                return response.choices[0].message.content.strip()

            if self.provider == "Gemini":
                convo_text = ""
                if conversation:
                    convo_text = "\n".join(f"{item['role'].upper()}: {item['content']}" for item in conversation[-8:])
                final_prompt = f"{system_context}\n\n{convo_text}\nUSER: {prompt}\nASSISTANT:".strip()
                response = self.model.generate_content(final_prompt)
                return getattr(response, "text", "").strip() or "No response received."

            if self.provider == "Aura Intelligence":
                return self._get_local_answer(prompt)

        except Exception as exc:
            self.last_error = str(exc)
            # On API failure, fall back to local knowledge
            return self._get_local_answer(prompt)

        return self._get_local_answer(prompt)


if "aura_ai_engine" not in st.session_state:
    st.session_state.aura_ai_engine = AuraAIEngine()

aura_ai = st.session_state.aura_ai_engine
