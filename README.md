# ARTHA — Financial Clarity Engine

**Portfolio Project by Aditya Bayar | April 2026**

A working MVP of the financial clarity product described in the ARTHA PRD. Built as a Streamlit web application.

## What it does

ARTHA analyses a young Indian professional's financial inputs across salary, credit card debt, investments, savings, insurance, and goals — and delivers a personalised Financial Health Report with:

- A scored 5-pillar health assessment (0 to 100)
- One specific priority action with rupee calculations
- Freshness alerts for financial blind spots
- Competitive signal vs peers at the same income level
- A 6-month financial clarity roadmap

## The problem it solves

No existing Indian fintech product tells you whether the sum of your financial decisions is moving you toward your goals or away from them. Groww shows your portfolio. ICICI shows your credit card. No product connects these two numbers and tells you that your credit card interest is silently destroying your SIP gains.

ARTHA does.

## Run locally

```bash
pip install streamlit
streamlit run app.py
```

## Deploy

Deploy instantly on [Streamlit Community Cloud](https://streamlit.io/cloud) — free, no server required.

## Technology

Pure Python with Streamlit. No API keys. No database. All analysis runs locally in the browser session using a financial logic engine built from scratch.
