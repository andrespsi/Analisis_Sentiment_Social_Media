# Advanced Social Media Sentiment Analysis Pipeline

**[!] PORTFOLIO & ARCHITECTURE DEMONSTRATION**

**Please Note: This is a portfolio repository demonstrating the architecture and capabilities of the project. The Python source code (`*.py`) containing the core logic is private and excluded via `.gitignore`. Trained models and sensitive data are also excluded.**

---

## 1. Project Overview

This project implements a comprehensive, end-to-end pipeline for **advanced sentiment analysis of social media comments**. It goes beyond simple API calls by incorporating custom data scraping, sophisticated text preprocessing, fine-tuning of modern language models, and results visualization.

The system is designed to:
1.  **Scrape comments** from multiple major platforms (Instagram, Facebook, TikTok, Twitter, YouTube), using both API and assisted methods.
2.  **Preprocess** the collected text data for optimal analysis.
3.  Perform **accurate sentiment classification** using a fine-tuned Transformer-based language model, specifically adapted for the nuances of social media language (likely Spanish).
4.  **Store** the results efficiently in a database.
5.  Provide **programmatic access** via an API and visualize insights through an interactive **dashboard**.

## 2. Technical Architecture & Key Features

The project follows a modular structure, demonstrating best practices in software engineering and data science:

* **Multi-Platform Scraping (`src/connectors/`, `scraper_*.py`):** Robust modules for data acquisition from diverse social media sources, handling different authentication methods (including cookie extraction) and scraping techniques.
* **Custom NLP Preprocessing (`src/utils/preprocesamiento.py`):** Tailored text cleaning and preparation pipeline designed for social media slang, emojis, and noise.
* **Fine-Tuned Sentiment Model (`fine_tune.py`, `src/analysis/analizador.py`):** Leverages a base Transformer model (details inferred from dependencies) fine-tuned on a custom dataset (`dataset_sentimiento.csv`) for superior performance on domain-specific text compared to off-the-shelf models.
* **Data Management (`src/core/database.py`):** Structured storage of scraped comments and analysis results.
* **API & Visualization (`src/api/endpoints.py`, `dashboard.py`):** Provides both an API for integration and an interactive dashboard (likely Streamlit/Dash) for exploring sentiment trends and results.
* **Modular Codebase (`src/`):** Well-organized source directory separating concerns (analysis, connectors, core, utils, api).

## 3. What is Public in This Repository

This repository showcases the project's structure and dependencies:

* `requirements.txt`: Lists the necessary Python libraries, highlighting the use of modern ML/NLP frameworks (like Transformers, PyTorch/TensorFlow, Scikit-learn, etc.).
* `Estructura de carpetas.txt`: Provides an overview of the project's organization.
* `.gitignore`: Demonstrates which components (source code, models, sensitive data) are intentionally kept private.
* `README.md`: This file, describing the project.
* *(Optionally, if you choose not to ignore them):* `dataset_sentimiento.csv`, `comentarios_*.txt` (Examples of the data used/collected).

## 4. Author

**Andrés Eduardo Gonzales Palacios**

https://www.linkedin.com/in/andr%C3%A9s-gonzales-palacios-57344156/
https://bit.ly/3LCM6UT
andresgp.psi@gmail.com
