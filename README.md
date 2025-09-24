# Cross-Sectional Equity Momentum Reversal Factor

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-black.svg)](https://www.python.org/dev/peps/pep-0008/)

## 🎯 Project Overview

A comprehensive quantitative research project implementing and analyzing a **cross-sectional equity momentum reversal strategy**. This project demonstrates advanced factor research methodologies, statistical testing frameworks, and systematic backtesting techniques commonly used in institutional quantitative finance.

**Research Hypothesis**: Stocks with high short-term momentum tend to reverse, creating opportunities for contrarian strategies that go long low-momentum stocks and short high-momentum stocks.

### 🏆 Key Achievements
- **Statistical Significance**: Fama-MacBeth regression with p-value of 0.034 demonstrates factor predictive power
- **Cross-Sectional Analysis**: 6,610 observations across 661 trading days and 15 large-cap equities
- **Professional Implementation**: Production-ready backtesting engine with comprehensive risk metrics
- **Institutional-Grade Analysis**: Full attribution analysis, drawdown management, and statistical significance testing

---

## 📊 Research Results Summary

| **Metric** | **Value** | **Benchmark (SPY)** |
|------------|-----------|---------------------|
| **Total Return** | -29.49% | +23.49% |
| **Annual Return** | -10.51% | +10.18% |
| **Sharpe Ratio** | -0.83 | +0.33 |
| **Maximum Drawdown** | -39.22% | -23.93% |
| **Win Rate** | 44.11% | N/A |
| **Annual Volatility** | 15.11% | 18.52% |

**Alpha vs Benchmark**: -20.70% (Strategy underperformed during 2020-2023 bull market)

---

## 🔬 Technical Implementation

### Factor Construction & Analysis
- **Momentum Calculation**: 90-day price momentum with proper handling of corporate actions
- **Cross-Sectional Ranking**: Daily decile-based ranking system across equity universe
- **Signal Generation**: Contrarian signals based on momentum reversal hypothesis
- **Risk Controls**: Position sizing and turnover management

### Statistical Methodology
- **Fama-MacBeth Regressions**: Time-series of cross-sectional regressions controlling for size and beta
- **Bootstrap Testing**: Robustness testing with statistical significance validation
- **Performance Attribution**: Decomposition of returns into systematic and idiosyncratic components
- **Risk Analytics**: VaR, Sortino ratio, Calmar ratio, and drawdown analysis

### Backtesting Framework
- **Long/Short Portfolio**: Systematic rebalancing with transaction cost considerations
- **Universe**: 15 large-cap US equities (expandable framework)
- **Rebalancing**: Monthly rebalancing (21-trading-day frequency)
- **Position Management**: Equal-weighted decile construction with risk budgeting

---

## 📁 Project Structure

```
├── notebooks/                          # Research & Analysis
│   ├── 01_data_exploration.ipynb      # EDA and data quality checks
│   ├── 02_factor_analysis.ipynb       # Factor construction & Fama-MacBeth
│   └── 03_backtest_visualization.ipynb # Strategy implementation & results
├── src/                                # Production Code
│   ├── backtester/
│   │   ├── __init__.py
│   │   └── engine.py                   # Backtesting framework
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── cleaners.py                 # Data preprocessing pipeline
│   └── factor_lib/
│       ├── __init__.py
│       └── momentum.py                 # Factor calculation library
├── data/                              # Data Storage
│   ├── raw/                          # Original market data
│   └── processed/                    # Cleaned datasets
├── reports/                          # Generated Analysis
│   └── figures/                     # Visualization outputs
├── config.yaml                      # Configuration management
├── requirements.txt                 # Dependencies
└── README.md                       # This file
```

---

## 🔧 Technologies & Libraries

### Core Quantitative Stack
- **pandas** & **numpy**: High-performance data manipulation and numerical computing
- **scipy** & **statsmodels**: Advanced statistical analysis and hypothesis testing
- **yfinance**: Real-time and historical market data acquisition
- **scikit-learn**: Machine learning preprocessing and validation

### Visualization & Analysis
- **matplotlib** & **seaborn**: Statistical visualization and publication-quality charts
- **plotly**: Interactive dashboards and risk analytics
- **jupyterlab**: Research environment with reproducible analysis

### Production & Testing
- **pytest**: Unit testing framework for code reliability
- **mlflow**: Experiment tracking and model versioning
- **pyarrow** & **fastparquet**: High-performance data serialization

---

## 🚀 Quick Start

### Environment Setup
```bash
# Clone repository
git clone https://github.com/DataHiveMind/Cross-Sectional-Equity-Momentum-Reversal-Factor.git
cd Cross-Sectional-Equity-Momentum-Reversal-Factor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Analysis
```bash
# Launch Jupyter environment
jupyter lab

# Execute notebooks in order:
# 1. 01_data_exploration.ipynb
# 2. 02_factor_analysis.ipynb  
# 3. 03_backtest_visualization.ipynb
```

### Standalone Factor Testing
```bash
# Test momentum factor implementation
python src/factor_lib/momentum.py

# Run backtesting engine
python src/backtester/engine.py
```

---

## 📈 Research Methodology

### 1. Factor Analysis Framework
Our implementation follows academic best practices for factor research:

- **Cross-Sectional Ranking**: Daily ranking of securities by momentum metric
- **Forward Return Calculation**: 1-week ahead returns for signal validation
- **Decile Portfolio Construction**: Systematic grouping for performance analysis
- **Statistical Testing**: Fama-MacBeth methodology for robust inference

### 2. Backtesting Best Practices
- **Point-in-Time Data**: Elimination of look-ahead bias
- **Transaction Costs**: Implicit cost modeling through turnover analysis  
- **Survivorship Bias**: Robust universe construction
- **Risk Management**: Systematic position sizing and exposure limits

### 3. Performance Evaluation
- **Risk-Adjusted Metrics**: Sharpe, Sortino, and Calmar ratios
- **Benchmark Comparison**: Relative performance vs market index
- **Statistical Significance**: Hypothesis testing for strategy viability
- **Regime Analysis**: Performance across different market conditions

---

## 🔍 Key Findings & Insights

### Factor Validation Results
✅ **Statistical Significance**: Momentum coefficient statistically significant (p=0.034)  
✅ **Cross-Sectional Power**: Strong explanatory power (R² = 44.12%)  
✅ **Temporal Stability**: Consistent factor loadings across 661 trading days  
❌ **Strategy Performance**: Reversal hypothesis didn't hold during bull market period

### Market Regime Analysis
The momentum reversal strategy underperformed during the 2020-2023 period, suggesting:
- **Momentum Continuation**: Strong trend-following behavior dominated reversal patterns
- **Market Regime Dependency**: Strategy may perform better in sideways/bear markets
- **Parameter Sensitivity**: Alternative lookback periods and rebalancing frequencies merit investigation

### Risk Characteristics
- **Moderate Volatility**: 15.11% annualized (lower than market)
- **Significant Drawdowns**: -39.22% maximum drawdown indicates strategy risk
- **Low Win Rate**: 44.11% suggests strategy requires larger average wins

---

## 💼 Recruitment Relevance

This project demonstrates proficiency in:

### Quantitative Research Skills
- **Factor Research**: End-to-end factor development and validation
- **Statistical Methods**: Advanced econometric techniques (Fama-MacBeth, significance testing)
- **Signal Processing**: Cross-sectional ranking and portfolio construction
- **Performance Attribution**: Comprehensive risk and return decomposition

### Technical Competencies  
- **Python Proficiency**: Production-quality code with proper documentation
- **Data Engineering**: Efficient data pipeline construction and management  
- **Visualization**: Professional-grade charts and interactive dashboards
- **Research Workflow**: Reproducible analysis with version control

### Institutional Knowledge
- **Academic Literature**: Implementation of peer-reviewed methodologies
- **Risk Management**: Systematic approach to drawdown control and position sizing
- **Backtesting Rigor**: Industry-standard practices for strategy validation
- **Documentation Standards**: Clear communication of complex quantitative concepts

---

## 🔮 Future Enhancements

### Short-term Improvements
- [ ] **Alternative Universes**: Extend to mid-cap and international equities
- [ ] **Transaction Costs**: Explicit modeling of bid-ask spreads and market impact
- [ ] **Risk Models**: Integration of multi-factor risk model for better attribution
- [ ] **Parameter Optimization**: Systematic hyperparameter tuning framework

### Advanced Features
- [ ] **Machine Learning**: Ensemble methods for signal combination
- [ ] **Alternative Data**: Integration of sentiment and fundamental factors  
- [ ] **Real-time Deployment**: Production system with live data feeds
- [ ] **Portfolio Optimization**: Mean-variance optimization with constraints

---

## 📞 Contact & Portfolio

**Author**: [Kenneth LeGare]  
**Email**: [kennethlegare5@gmail.com]  



*This project represents a comprehensive demonstration of quantitative research capabilities suitable for roles in asset management, hedge funds, and proprietary trading firms.*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Factor research methodology based on academic literature from Jegadeesh & Titman (1993)
- Backtesting framework inspired by industry best practices from AQR and Two Sigma
- Statistical testing approaches follow Campbell, Lo, and MacKinlay (1997) guidelines