# ESG Risk Analysis Dashboard

## Project Overview

This project is an interactive ESG Risk Analysis Dashboard developed with Python and Streamlit. It is based on ESG risk rating data for S&P 500 companies and is designed to help users explore ESG performance from multiple perspectives, including company-level detail, sector-level comparison, ESG component structure, and ranking analysis.

The project was created as a small Python-based data product for a business-related analytical task. Instead of presenting only raw code or static graphs, it transforms the analysis into an interactive dashboard that users can explore directly.

## Analytical Problem

The analytical problem addressed in this project is how to use Python to analyse and communicate ESG risk patterns among S&P 500 companies in a clear and user-friendly way. The project focuses on identifying:

- how ESG risk varies across sectors;
- how individual companies differ in their ESG profiles;
- how the environment, social, and governance dimensions compare on average;
- how company size may relate to ESG risk;
- which companies appear to have the lowest and highest ESG risk scores.

## Intended Users

This dashboard is designed for:

- business, finance, and accounting students;
- users interested in ESG and sustainability analysis;
- beginner-level investors or analysts who want to compare firms based on ESG-related indicators;
- general users who want to explore corporate ESG risk data through an interactive interface.

## Dataset

The project uses the **S&P 500 ESG Risk Ratings** dataset obtained from Kaggle.

### Dataset link
https://www.kaggle.com/datasets/pritish509/s-and-p-500-esg-risk-ratings

### Access date
14 April 2026

### Why this dataset was selected

This dataset was selected because it is directly relevant to a business and sustainability context and contains multiple variables that support descriptive analysis and dashboard design. It includes firm-level ESG risk information as well as sector, industry, and company characteristics, making it suitable for comparison, filtering, and visual exploration.

### Main variables used in the project

- Name
- Symbol
- Sector
- Industry
- Total ESG Risk score
- Environment Risk Score
- Social Risk Score
- Governance Risk Score
- Full Time Employees

## Product Features

The dashboard includes the following functions:

- **Interactive filter panel** for sector, ESG score range, employee range, and ESG risk category;
- **Single company analysis** with company details and ESG composition;
- **Keyword-based company search** in the single company tab;
- **Company comparison** across total ESG score and ESG component scores;
- **Sector analysis** showing average ESG risk by sector and ESG score distribution;
- **ESG relationships analysis** including average ESG component scores, employee size vs ESG risk, and a correlation matrix;
- **Ranking analysis** showing the companies with the lowest and highest ESG risk scores;
- **Download button** for exporting the filtered dataset.

## Python Workflow

The project follows a coherent Python-based analytical workflow:

1. define the analytical problem and target users;
2. load the ESG dataset into Python;
3. inspect the data structure and identify relevant variables;
4. clean and prepare the data by converting numeric fields, removing missing key records, and dropping duplicates;
5. create an ESG risk category variable for easier interpretation;
6. conduct descriptive analysis and visualisation;
7. translate the analysis into an interactive Streamlit dashboard.

## Files in This Project

- `app.py` – the Streamlit dashboard application
- `ESG_Risk_Analysis_Notebook.ipynb` – the Python notebook showing the analytical workflow
- `SP 500 ESG Risk Ratings.csv` – the dataset used in the project
- `README.md` – project documentation

## Tools and Libraries

This project was developed using:

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook

## How to Run the Dashboard

1. Make sure the following files are stored in the same folder:
   - `app.py`
   - `SP 500 ESG Risk Ratings.csv`

2. Install the required Python libraries if they are not already installed:

```bash
pip install streamlit pandas matplotlib seaborn