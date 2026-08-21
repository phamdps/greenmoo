# 🌿 GreenMOO

**Green Multi-Objective Optimization Framework for Automated Deep Learning**

---

## 📌 Reference & Attribution

> **Notice:** **GreenMOO** is built upon an embedded, heavily customized evolutionary engine derived from the original **Platypus** framework (developed by David Hadka).
> Rather than relying on external pre-built optimization binaries, the core evolutionary computing algorithms have been fully integrated, restructured, and extended locally within this repository. We have repurposed these foundations to pioneer a specialized **Green Multi-Objective Optimization** engine designed for sustainable, resource-aware machine learning pipelines.

---

## 💡 What is GreenMOO?

**GreenMOO** bridges classical evolutionary computing with the critical demands of **Green AI**. Traditional machine learning optimization focuses solely on predictive accuracy, often at a catastrophic cost to energy consumption and carbon emissions.

GreenMOO automates neural architecture design and hyperparameter tuning while explicitly co-optimizing performance against sustainability metrics—such as total energy expenditure ($kWh$), estimated carbon footprints ($gCO_2eq$), inference latency, and hardware memory footprints.

---

## ✨ Key Features

* **Embedded Evolutionary Engine:** Native, self-contained implementation of advanced Multi-Objective Evolutionary Algorithms (MOEAs like NSGA-II, NSGA-III, and MOEA/D) adapted seamlessly without external optimization library overhead.
* **Green AI & Sustainability Metrics:** Built-in tracking for energy profiling and environmental impact alongside traditional model validation metrics.
* **Algorithmic Extensibility:** A dedicated `algorithms` module structured for rapid prototyping and custom search strategy deployment.
* **Hardware-Aware Constraints:** Enforce rigorous caps on parameter counts, active hardware power draw, and memory consumption during optimization loops.

---

## 📦 Installation

Because **GreenMOO** bundles its own embedded and enhanced optimization backend, it operates entirely as an independent package.

Clone the repository and install it locally in editable mode for development:

```bash
git clone https://github.com/phamdps/greenmoo.git
cd greenmoo
pip install -r requirements.txt
python -m pip install --editable .

```

---

## 📂 Repository Structure

```text
greenmoo/
├── core/               # Embedded evolutionary computing & MOEA engines (derived from Platypus)
├── algorithms/         # Advanced multi-objective optimization algorithms and search strategies
├── metrics/            # Energy profiling, carbon tracking, and performance evaluation
├── examples/           # Sample benchmarks and pipelines (Coming Soon)
├── tests/              # Comprehensive unit and integration test suites
├── setup.py            # Package installation configuration
└── README.md

```

---

## 🚀 Roadmap & Status

* [x] Core evolutionary engine integration & restructuring
* [x] Base multiobjective optimization modules setup
* [ ] Finalizing the `algorithms` search backend and green metric hooks *(In Progress)*
* [ ] Public benchmark scripts and usage documentation

---

## 📜 Citation

If you use GreenMOO or its optimization components in your academic research, please cite both our framework and the foundational Platypus project:

> **GreenMOO Framework:**
> ```bibtex
> @software{greenmoo2026,
>   author = {phamdps},
>   title = {GreenMOO: A Green Multi-Objective Optimization Framework for Automated Deep Learning},
>   year = {2026},
>   url = {https://github.com/phamdps/greenmoo}
> }
> 
> ```
> 
> 

> **Foundational Optimization Engine (Platypus):**
> > Hadka, D. (2024). Platypus: A Framework for Evolutionary Computing in Python (Version 1.4.1) [Computer software]. Retrieved from [https://github.com/Project-Platypus/Platypus](https://www.google.com/search?q=https://github.com/Project-Platypus/Platypus)
> 
> 

---

## ⚖️ License

GreenMOO is open-source software released under the **GNU General Public License (GPL-3.0)**, preserving full compliance with the licensing terms of the original Platypus project.