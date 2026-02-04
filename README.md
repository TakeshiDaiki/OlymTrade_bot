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

🚀 Quick Start

git clone https://github.com/TakeshiDaiki/OlymTrade_bot
cd sniper-bot
pip install -r requirements.txt
python main.py

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
│
├── core/
│ ├── browser.py # Main Selenium automation (browser control)
│ └── risk.py # Risk management logic
│
├── logic/
│ ├── init.py
│ ├── indicators.py # Technical indicators
│ └── strategy.py # Trading strategy implementation
│
├── config.py # Global configuration settings
├── gui.py # Optional GUI / user interface logic
├── main.py # Main entry point of the bot
│
├── requirements.txt # Python dependencies
├── .gitignore # Ignored files for Git
└── README.md # Project documentation

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
