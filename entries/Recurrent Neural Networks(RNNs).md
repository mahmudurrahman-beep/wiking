
**One‑line summary**: RNNs are neural networks designed to process **sequential** data by maintaining a hidden state that carries information across time steps.

---

## Overview

RNNs process sequences \(x_1, x_2, \dots, x_T\) by updating a hidden state \(h_t\) at each time step and producing outputs \(y_t\). A simple recurrent update can be written as:

\[
h_t = \sigma(W_{hh} h_{t-1} + W_{xh} x_t + b_h)
\]
\[
y_t = f(W_{hy} h_t + b_y)
\]

where \(\sigma\) is an activation (e.g., \(\tanh\) or ReLU) and \(f\) is an output nonlinearity.

---

## Core components

- **Input sequence** — tokens, frames, or time‑series values \(x_t\).  
- **Hidden state** — \(h_t\) carries memory from previous steps.  
- **Recurrent weights** — \(W_{hh}\) ties the network across time.  
- **Output layer** — maps hidden states to predictions \(y_t\).

---

## Common RNN variants

- **Vanilla RNN** — the basic form with simple recurrent updates.  
- **LSTM (Long Short‑Term Memory)** — adds gates (input, forget, output) and a cell state to better capture long‑range dependencies.  
- **GRU (Gated Recurrent Unit)** — a simpler gated variant with update and reset gates; often faster to train than LSTM.

---

## Strengths and limitations

**Strengths**
- Naturally suited for sequential and temporal data.  
- Can model variable‑length inputs and outputs.

**Limitations**
- **Vanishing and exploding gradients** make learning long‑range dependencies difficult for vanilla RNNs.  
- Training can be slower than fully parallel architectures because of time‑step dependencies.

Gated variants (LSTM, GRU) were introduced to mitigate the vanishing gradient problem and improve learning of long‑term dependencies.

---

## Typical applications

- **Natural language processing**: language modeling, sequence tagging, machine translation (historically).  
- **Speech and audio**: speech recognition, audio generation.  
- **Time series**: forecasting, anomaly detection.  
- **Control and robotics**: sequence prediction and policy learning.

---

## Quick comparison (vanilla RNN vs LSTM vs GRU)

| **Model** | **Memory mechanism** | **Training stability** | **Typical use** |
|---|---:|---:|---|
| **Vanilla RNN** | Single hidden state | Poor for long dependencies | Simple sequence tasks |
| **LSTM** | Cell state + gates | Good for long dependencies | Language, speech |
| **GRU** | Gated hidden state | Good and simpler than LSTM | Many sequence tasks |

---

## Practical tips

- Use **layer normalization** or **dropout** between layers to regularize.  
- Prefer **LSTM/GRU** for tasks requiring long context.  
- For very long sequences or large datasets, consider **Transformer**‑style models for better parallelism.

---

## Fun facts

- **Memory metaphor**: RNN hidden states are often described as a short‑term memory that updates each time step.  
- **Gate invention**: LSTM gates were introduced in the 1990s (Hochreiter & Schmidhuber) and revived deep learning progress for sequences.  
- **From speech to translation**: RNNs powered many early breakthroughs in speech recognition and neural machine translation before attention‑only models became dominant.  
- **GRU origin**: GRU was proposed as a simpler alternative to LSTM with fewer parameters but similar performance on many tasks.

---