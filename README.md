Sniper-Bot – Automated Trading System (Olymp Trade)

A production-ready automated trading bot featuring real-time candlestick analysis, ZigZag indicator integration, 
Wick Rejection filters, and a scalable modular architecture. Built with Python 3.10+ and Selenium.

🚀 Features

Real-time market interaction via Selenium

ZigZag-based pivot detection

Wick Rejection (price action) filtering for high-precision entries

Dynamic Stop Loss and daily trade limit management

Modular, production-ready codebase suitable for portfolio projects

⚙️ Core Functionality

Real-time OHLC candlestick fetching

Pivot point detection using configurable ZigZag deviation

Wick-to-body ratio filtering (WICK_FACTOR = 0.35)

Automatic trade execution simulation

Consecutive loss monitoring and trade limits

Risk management with configurable Stop Loss

🧑‍💻 Developer Experience

Modular architecture (core / logic / config)

PEP8-compliant code

Centralized configuration management (config.py)

Real-time logging and debugging support

Easily extensible for multi-platform trading

🛠️ Tech Stack

Backend

Python 3.10+

Selenium WebDriver

WebDriver Manager (Chrome)

DevOps

Git & GitHub

.env configuration for sensitive credentials

pip / requirements.txt dependency management

📦 Installation
Prerequisites

Python 3.10+

Chrome Browser

Selenium WebDriver

🛠️ Installation & Usage
For Users (Standalone EXE)
Go to the Releases section in this repository.

Download the SniperBot_v1_Build.zip.

Extract the folder and run SniperBot_Olymp.exe.

🚀 Quick Start

# Clone the repository
git clone https://github.com/TakeshiDaiki/OlymTrade_bot

# Install dependencies
pip install -r requirements.txt

# Run the Application
python gui.py



## 🔧 Configuration

Adjust behavior in `config.py`:

| Parameter          | Description                                     |
|--------------------|-------------------------------------------------|
| ZIGZAG_DEVIATION   | Sensitivity of ZigZag pivot detection           |
| WICK_FACTOR        | Minimum wick rejection ratio (0.35 recommended) |
| ZZ_TOLERANCE       | Tolerance when touching historical pivots       |
| MAX_LOSSES         | Max allowed consecutive losses                  |
| MAX_TRADES_PER_DAY | Daily trade limit                               |




## 📚 Strategy Documentation

### 🧠 Strategy Logic

| Indicator         | Condition               | Description               |
|-------------------|-------------------------|---------------------------|
| ZigZag            | Pivot detected          | Identify high/low pivots  |
| Wick Rejection    | Wick/Body > WICK_FACTOR | Confirms price rejection  |
| Stop Loss         | Configured              | Limits losses             |
| Daily Trade Limit | Configured              | Risk management control   |



📁 Project Structure

OlymTrade_bot/
├── core/                        # ENGINE LAYER: Browser & DOM interaction
│   ├── browser.py               # Selenium encapsulation & automation methods
├── logic/                       # INTELLIGENCE LAYER: Strategy & Indicators
│   ├── indicators.py            # Technical analysis (ZigZag & Wick math)
│   └── strategy.py              # Decision logic (Signal generation)
├── dist/                        # DEPLOYMENT: Standalone binary (Git-ignored)
│   └── SniperBot_Olymp/         # Compiled portable application folder
│       ├── _internal/           # Binary dependencies & Python runtime
│       ├── core/ & logic/       # Local copies for the executable
│       └── SniperBot_Olymp.exe  # Main entry point for Windows users
├── config.py                    # SINGLE SOURCE OF TRUTH: Constants & Selectors
├── gui.py                       # INTERFACE: Modern UI & Process Management
├── main.py                      # CONTROLLER: Orchestrates the trading loop
├── requirements.txt             # DEPENDENCIES: Manifest for environment setup
└── .gitignore                   # VERSION CONTROL: Exclusion rules (build, dist, pycache)

## Scripts Reference

| Command                         | Description             |
|---------------------------------|-------------------------|
| python main.py                  | Start the trading bot   |
| pip install -r requirements.txt | Install dependencies    |


👤 Author

José Salazar
Software Developer focused on automation, algorithmic trading and AI
LinkedIn: https://www.linkedin.com/in/jose-salazar-60ab21283/
GitHub: https://github.com/TakeshiDaiki

⚠️ Important Note

This bot is a demonstration and portfolio project only.
It is not recommended for live trading without extensive testing and validation.
The author is not responsible for any financial losses.
