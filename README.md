# ESG Risk Analysis Dashboard

## 1. Problem & User
This project explores how ESG risk varies across S&P 500 companies and sectors using Python and Streamlit. It is designed for business, finance, and accounting students, as well as general users who want to understand and compare corporate ESG risk in an interactive way.

## 2. Data
**Source:** S&P 500 ESG Risk Ratings dataset from Kaggle  
**Dataset link:** https://www.kaggle.com/datasets/pritish509/s-and-p-500-esg-risk-ratings  
**Access date:** 14 April 2026  

**Key fields used:**
- Name
- Symbol
- Sector
- Industry
- Total ESG Risk score
- Environment Risk Score
- Social Risk Score
- Governance Risk Score
- Full Time Employees

## 3. Methods
The main Python workflow for this project included:
1. Loading the dataset into Python using pandas  
2. Inspecting the dataset structure and selecting relevant variables  
3. Cleaning the data by converting numeric fields, handling missing values, and removing duplicates  
4. Creating an ESG risk category variable for easier interpretation  
5. Producing descriptive analysis and visualisations using matplotlib and seaborn  
6. Building an interactive dashboard in Streamlit with filters, comparison tools, and ranking views  

## 4. Key Findings
- ESG risk varies across sectors, with some sectors showing higher average risk scores than others.  
- Companies within the same sector can still have noticeably different ESG risk profiles.  
- Total ESG risk is influenced by a combination of environmental, social, and governance factors rather than one single component.  
- Company comparison and ranking views help identify firms with relatively lower or higher ESG risk scores.  
- The dashboard makes ESG analysis easier to explore through interactive filtering and visualisation.  

## 5. How to run
1. Clone or download this repository.  
2. Make sure the following files are in the same folder:
   - `app.py`
   - `SP 500 ESG Risk Ratings.csv`
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
4. Open a terminal in the project folder and run:
    streamlit run app.py

## 6. Product link / Demo
GitHub repository:
https://github.com/jasmine23425/ESG-Risk-Analysis-Dashboard/tree/main
Demo video:
Submitted through Mediasite for ACC102 Track 4.

## 7. Limitations & next steps
This project is based on one secondary dataset, so the quality of the results depends on the completeness and reliability of that source. Some variables, especially employee data, contain missing values, and the analysis is descriptive rather than predictive or causal. In future, the project could be improved by adding more data sources, including historical ESG data for time-series analysis, and providing clearer explanations for non-technical users.
