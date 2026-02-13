# Attention Is All You Need

**Paper**: *Attention Is All You Need*  
**Authors**: Ashish Vaswani; Noam Shazeer; Niki Parmar; Jakob Uszkoreit; Llion Jones; Aidan N. Gomez; Łukasz Kaiser; Illia Polosukhin  
**Year**: 2017  
**One line summary**: Introduced the **Transformer**, a sequence to sequence architecture that replaces recurrence and convolution with attention mechanisms for faster, highly parallelizable training.

---

## Overview

**What it proposes**  
A sequence to sequence model built entirely on **self attention** and **multi head attention** layers, organized into encoder and decoder stacks. By removing recurrent and convolutional components, the model enables greater parallelism and shorter training times while achieving state of the art translation performance.

**Why it matters**  
The Transformer became the foundation for many subsequent advances in natural language processing and beyond, powering language models, translation systems, summarizers, and multimodal architectures.

---

## Architecture

| **Component** | **Purpose** | **Key detail** |
|---|---:|---|
| **Self Attention** | Contextualize tokens | Each token attends to all tokens in the sequence |
| **Multi Head Attention** | Capture diverse relations | Multiple attention heads run in parallel |
| **Scaled Dot Product Attention** | Compute attention weights | Dot products scaled by \(\sqrt{d_k}\) then softmax |
| **Positionwise Feedforward** | Nonlinear per position transform | Same feedforward network applied to each position |
| **Positional Encoding** | Inject order information | Sinusoidal position vectors added to inputs |
| **Encoder Decoder Stacks** | Encode source and generate target | Stacked layers of attention and feedforward |

**Attention formula**  

\[
\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]

---

## Key Innovations

- **Attention only sequence modeling** — removes recurrence and convolution, enabling full parallelization.  
- **Multi head attention** — lets the model attend to different representation subspaces simultaneously.  
- **Scaled dot product attention** — stabilizes gradients for large key dimensions by dividing by \(\sqrt{d_k}\).  
- **Sinusoidal positional encodings** — provide a continuous way to inject order information and generalize to unseen sequence lengths.

---

## Impact and Applications

**Broader impact**  
The Transformer reshaped research and engineering practices by prioritizing attention and parallelism. It underlies many modern large language models and has been adapted for vision, audio, and multimodal tasks.

**Common applications**  
- Machine translation  
- Language modeling and generation  
- Text summarization  
- Question answering  
- Multimodal tasks when combined with vision or audio encoders

---

## Fun Facts

- **Name origin**: The term Transformer hints at transforming sequences via attention rather than via recurrence.  
- **Sinusoidal trick**: The original paper used sinusoidal positional encodings so the model could generalize to sequence lengths not seen during training.  
- **Collaborative paper**: Eight authors from Google Brain and Google Research contributed to the work.  
- **Speed surprise**: Because attention can be computed in parallel across positions, Transformers trained far faster than comparable RNNs on the same hardware.  
- **Rapid takeover**: Within a few years the Transformer architecture became the dominant paradigm in NLP research and industry.

---

## Quick Cheat Sheet

- **Core idea**: Replace recurrence with attention.  
- **Key formula**: \(\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V\).  
- **Where to read**: arXiv preprint Attention Is All You Need 1706.03762