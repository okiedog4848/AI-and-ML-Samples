# TGO Resort AI Properties Tracker

An **AI-augmented ETL pipeline** that automatically scrapes property listings from [The Great Outdoors Resort](https://www.tgoresort.com/properties/), parses messy plain-text data using LLMs, detects weekly changes (new listings, removed listings, price changes), tracks historical metrics, and displays everything in a live dashboard.

This project demonstrates real-world **AI ETL / Data Engineering skills** — exactly the kind of work needed for modern data migration and AI-powered platforms.

## Project Goals
- Scrape weekly property listings from a static, inconsistently formatted real-estate page.
- Use AI agents to reliably parse unstructured text into clean structured data (address, price, beds, baths).
- Automatically detect **new**, **removed**, and **price-changed** properties each week.
- Calculate business metrics over time (total active listings, average price, inferred "sales" via removals).
- Store historical snapshots and enable natural-language querying via RAG.
- Deploy a fully automated, production-like system using only free tools.

## Tech Stack
- **Core**: Python, Requests + BeautifulSoup (scraping)
- **AI Layer**: LangChain / LangGraph, CrewAI (multi-agent workflows)
- **Parsing & Transformation**: Prompt engineering + LLM (Grok / OpenAI / etc.)
- **Storage**: SQLite (weekly snapshots)
- **Orchestration**: GitHub Actions (weekly cron job)
- **Frontend**: Streamlit (interactive dashboard with charts and RAG chat)
- **Vector DB** (later): Chroma (for RAG over historical data)
- **Modern Data Tools** (Phase 4+): dbt + LLM integration

## How It Demonstrates AI ETL Skills
- **Traditional ETL** → replaced/enhanced with **Agentic AI pipelines**
- Handles messy, real-world data (inconsistent bed/bath formatting, plain text)
- Change detection logic + historical tracking (similar to data migration validation)
- Human-in-the-loop ready architecture
- Production deployment with scheduling, logging, and a public dashboard

This project shows I can move from manual Python scripts (my current PRISM work) to designing reliable **AI-powered data pipelines** that reduce manual effort while improving accuracy.

## Live Dashboard
(Will be added once deployed on Streamlit Community Cloud)

## Project Status
- **Phase 1–2**: In progress (scraping + prompt-based parsing)
- Next: Multi-agent change detection + Streamlit UI

## Folder Structure
