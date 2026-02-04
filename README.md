# Sniper-Bot — Market Automation & Technical Analysis System (Olymp Trade)

Sniper-Bot is a modular **technical analysis and market automation framework** built with **Python 3.10+** 
and **Selenium**.

It features real-time candlestick monitoring, ZigZag pivot detection, wick rejection filtering, and configurable 
risk-management rules.  
This project was designed as a **portfolio-grade automation system** with clean architecture and extensibility in mind.

---

## 🚀 Features

- Real-time market interaction via Selenium WebDriver  
- ZigZag-based pivot point detection  
- Wick Rejection (price action) filtering for higher-quality signals  
- Dynamic Stop Loss and daily trade limit controls  
- Modular and scalable project structure  
- Standalone Windows executable build (optional)

---

## ⚙️ How It Works

1. The bot launches Olymp Trade using Selenium.  
2. The user has **3 minutes** to log in manually and configure the platform.  
3. After login, the engine starts collecting OHLC candlestick data.  
4. Trading signals are generated using:

   - ZigZag pivot detection  
   - Wick rejection confirmation  

5. Risk rules prevent overtrading by enforcing:

   - Maximum consecutive losses  
   - Daily trade execution limits  

---

## 📦 Portable Version (Windows EXE)

If you downloaded the standalone `.zip` release, no Python installation is required:

1. Extract the ZIP file anywhere on your PC  
2. Open `config.py` to adjust trading parameters  
3. Run:

   - `SniperBot_Olymp.exe`

---

## 🚀 Quick Start (Developers)

### Clone the Repository

```bash
git clone https://github.com/TakeshiDaiki/OlymTrade_bot
cd OlymTrade_bot
```

### Install Dependencies

pip install -r requirements.txt

### Run the Application

python gui.py

### 🔧 Configuration

All strategy parameters are centralized in:

config.py

You can modify behavior without recompiling the project.

## 🔧 Configuration Parameters

| Parameter          |  Description                                    |
|--------------------|-------------------------------------------------|
| ZIGZAG_DEVIATION   | ZigZag pivot sensitivity                        |
| WICK_FACTOR        | Minimum wick rejection ratio (0.35 recommended) |
| ZZ_TOLERANCE       | Pivot touch tolerance                           |
| MAX_LOSSES         | Max consecutive losses allowed                  |
| MAX_TRADES_PER_DAY | Daily trade execution limit                     |



## 📚 Strategy Logic

| Indicator         |  Condition              | Description                    |
|-------------------|-------------------------|--------------------------------|
| ZigZag            | Pivot detected          | Identifies high/low pivots     |
| Wick Rejection    | Wick/Body > WICK_FACTOR | Confirms price rejection       |
| Stop Loss         | Configured              | Limits consecutive losses      |
| Daily Trade Limit | Configured              | Prevents excessive executions  |



### 📁 Project Structure
``` text 
OlymTrade_bot/
├── core/                        # ENGINE LAYER: Browser & DOM interaction
│   └── browser.py               # Selenium encapsulation & automation methods
│
├── logic/                       # INTELLIGENCE LAYER: Strategy & Indicators
│   ├── indicators.py            # Technical analysis (ZigZag & Wick math)
│   └── strategy.py              # Decision logic (signal generation)
│
├── dist/                        # DEPLOYMENT: Standalone binary (Git-ignored)
│   └── SniperBot_Olymp/         # Compiled portable application folder
│       ├── _internal/           # Binary dependencies & Python runtime
│       └── SniperBot_Olymp.exe  # Main Windows executable
│
├── config.py                    # SINGLE SOURCE OF TRUTH: Constants & Selectors
├── gui.py                       # INTERFACE: Modern UI & process management
├── main.py                      # CONTROLLER: Orchestrates the execution loop
├── requirements.txt             # Python dependencies manifest
└── .gitignore                   # Version control exclusions
```

### 🛠️ Tech Stack

Python 3.10+

Selenium WebDriver

WebDriver Manager (Chrome)

Git + GitHub

Modular architecture (core / logic separation)

## 📌 Scripts Reference

| Command                            | Description                  |
|------------------------------------|------------------------------|
| python gui.py                      | Launch the full application  |
| python main.py                     | Start the automation engine  |
| pip install -r requirements.txt    | Install required libraries   |



### 👤 Author

José Salazar
Software Developer focused on automation, algorithmic systems, and AI.

LinkedIn: https://www.linkedin.com/in/jose-salazar-60ab21283/

GitHub: https://github.com/TakeshiDaiki

### ⚠️ Disclaimer

This project is provided for educational and portfolio purposes only.
It is not intended for live trading without extensive testing and validation.

The author is not responsible for any financial losses or misuse of this software.