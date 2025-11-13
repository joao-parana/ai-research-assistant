# Partial Discharge Analysis with Machine Learning

> Advanced analysis system for detecting and predicting equipment failures using ML/DL techniques

## Research Focus

- Machine Learning for Partial Discharge Detection
- Time Series Analysis of Electrical Systems
- Predictive Maintenance using Deep Learning
- Anomaly Detection in Power Transformers

## Research Questions

- How can we improve early detection of partial discharge events?
- Which ML models perform best for time series anomaly detection?
- Can transfer learning reduce the need for large labeled datasets?
- What features are most predictive of equipment failures?
- How to reduce false positives while maintaining high sensitivity?

## Technologies

- Python 3.13
- NumPy & Pandas for data processing
- Matplotlib for visualization
- SciPy for signal processing
- Pydantic for data validation
- Random Forest for baseline models
- LSTM Networks for temporal patterns
- Transformer models for complex relationships
- 1D-CNN for feature extraction

## Keywords

- partial discharge
- time series analysis
- anomaly detection
- predictive maintenance
- machine learning
- deep learning
- LSTM
- transformers
- random forest
- 1D-CNN
- power systems
- equipment monitoring

## Goals

- Develop real-time partial discharge detection system
- Achieve >86% accuracy in fault classification
- Reduce false positive rate by 50%
- Process streaming data with <1s latency
- Deploy model in production environment

## Methodology

1. Data preprocessing and cleaning
2. Feature engineering from time series
3. Exploratory data analysis
4. Baseline model comparison (RF, XGBoost)
5. Deep learning model development (LSTM, 1D-CNN, Transformers)
6. Hyperparameter optimization
7. Cross-validation and testing
8. Model deployment and monitoring

## Datasets

- SOMA internal sensor data (2020-2025)
- Public partial discharge benchmarks
- Simulated fault scenarios
- Real-world equipment failure cases

## Related Papers

- "Benchmarking ML and DL for Fault Detection in Power Transformers" (2025)
- "Enhancing Power Quality Event Classification with AI Transformers" (2024)
- "Deep Learning for Time Series Classification" (2024)

## Project Structure

```
gamma-pd-analytics/
├── src/
│   └── gamma_pd_analytics/
│       ├── partial_discharge_analysis.py
│       ├── read_soma_data.py
│       ├── time_recover.py
│       └── linear_fit.py
├── data/
│   └── *.csv files
└── tests/
```

## Installation

```bash
pip install -e .
```

## Usage

```bash
python src/gamma_pd_analytics/partial_discharge_analysis.py
```

---

**Note:** This README structure is optimized for the MCP Server AI Research Assistant.
The tool will automatically extract research metadata to find relevant papers and suggest improvements.
