import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="ESG Risk Analysis Dashboard",
    layout="wide",
    page_icon="📊"
)

sns.set_style("whitegrid")
plt.rcParams["figure.facecolor"] = "white"

# -----------------------------
# Load and clean data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("SP 500 ESG Risk Ratings.csv")

    numeric_cols = [
        "Total ESG Risk score",
        "Environment Risk Score",
        "Social Risk Score",
        "Governance Risk Score",
        "Full Time Employees",
        "Controversy Level"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Total ESG Risk score", "Sector", "Name"])
    df = df.drop_duplicates(subset=["Name"])

    def classify_esg(score):
        if score < 10:
            return "Negligible"
        elif score < 20:
            return "Low"
        elif score < 30:
            return "Medium"
        elif score < 40:
            return "High"
        else:
            return "Severe"

    df["ESG Risk Category"] = df["Total ESG Risk score"].apply(classify_esg)

    return df


df = load_data()

# -----------------------------
# Title and introduction
# -----------------------------
st.title("📊 ESG Risk Analysis Dashboard")
st.markdown(
    """
    This dashboard provides an interactive analysis of **S&P 500 ESG Risk Ratings**.  
    Users can filter companies by **sector**, **risk score**, **employee size**, and **risk category**,  
    then explore company details, compare firms, review sector-level trends, and examine ESG patterns through visualization.
    """
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("🔎 Filter Panel")
st.sidebar.markdown("Use the controls below to refine the dataset.")

sector_options = sorted(df["Sector"].dropna().unique())
selected_sectors = st.sidebar.multiselect(
    "Select Sector(s)",
    options=sector_options,
    default=sector_options
)

score_min = float(df["Total ESG Risk score"].min())
score_max = float(df["Total ESG Risk score"].max())
score_range = st.sidebar.slider(
    "ESG Risk Score Range",
    min_value=float(score_min),
    max_value=float(score_max),
    value=(float(score_min), float(score_max))
)

employee_non_na = df["Full Time Employees"].dropna()
if not employee_non_na.empty:
    emp_min = int(employee_non_na.min())
    emp_max = int(employee_non_na.max())
else:
    emp_min = 0
    emp_max = 100000

employee_range = st.sidebar.slider(
    "Employee Range",
    min_value=emp_min,
    max_value=emp_max,
    value=(emp_min, emp_max)
)

risk_options = sorted(df["ESG Risk Category"].dropna().unique())
risk_category = st.sidebar.multiselect(
    "ESG Risk Category",
    options=risk_options,
    default=risk_options
)

# -----------------------------
# Apply filters
# -----------------------------
filtered = df.copy()

filtered = filtered[filtered["Sector"].isin(selected_sectors)]

filtered = filtered[
    (filtered["Total ESG Risk score"] >= score_range[0]) &
    (filtered["Total ESG Risk score"] <= score_range[1])
]

filtered = filtered[
    (filtered["Full Time Employees"].isna()) |
    (
        (filtered["Full Time Employees"] >= employee_range[0]) &
        (filtered["Full Time Employees"] <= employee_range[1])
    )
]

filtered = filtered[filtered["ESG Risk Category"].isin(risk_category)]

if filtered.empty:
    st.warning("⚠️ No companies match the current filters. Please adjust your selection.")
    st.stop()

# -----------------------------
# Dataset snapshot
# -----------------------------
with st.expander("View filtered dataset preview"):
    st.dataframe(filtered.head(20))

# -----------------------------
# KPI Overview
# -----------------------------
st.subheader("📌 Overview")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", len(filtered))
c2.metric("Average ESG Risk", round(filtered["Total ESG Risk score"].mean(), 2))
c3.metric("Lowest Risk", round(filtered["Total ESG Risk score"].min(), 2))
c4.metric("Highest Risk", round(filtered["Total ESG Risk score"].max(), 2))

# -----------------------------
# Summary Insights
# -----------------------------
st.subheader("🧠 Summary Insights")

avg_risk = round(filtered["Total ESG Risk score"].mean(), 2)
sector_group = filtered.groupby("Sector")["Total ESG Risk score"].mean()

lowest_sector = sector_group.idxmin()
highest_sector = sector_group.idxmax()
lowest_sector_score = round(sector_group.min(), 2)
highest_sector_score = round(sector_group.max(), 2)

lowest_company_row = filtered.loc[filtered["Total ESG Risk score"].idxmin()]
highest_company_row = filtered.loc[filtered["Total ESG Risk score"].idxmax()]

st.markdown(
    f"""
    - The **average ESG risk score** in the current filtered dataset is **{avg_risk}**.  
    - The sector with the **lowest average ESG risk** is **{lowest_sector}** (**{lowest_sector_score}**).  
    - The sector with the **highest average ESG risk** is **{highest_sector}** (**{highest_sector_score}**).  
    - The **lowest-risk company** currently displayed is **{lowest_company_row['Name']}** with a score of **{round(lowest_company_row['Total ESG Risk score'], 2)}**.  
    - The **highest-risk company** currently displayed is **{highest_company_row['Name']}** with a score of **{round(highest_company_row['Total ESG Risk score'], 2)}**.  
    """
)

# -----------------------------
# Download filtered data
# -----------------------------
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_esg_data.csv",
    mime="text/csv"
)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Single Company",
    "Comparison",
    "Sector Analysis",
    "ESG Relationships",
    "Ranking"
])

# ================= SINGLE COMPANY =================
with tab1:
    st.subheader("Single Company Detail")

    company_list = sorted(filtered["Name"].dropna().unique())

    search_keyword = st.text_input("Search company by keyword")
    if search_keyword:
        matched_companies = [c for c in company_list if search_keyword.lower() in c.lower()]
    else:
        matched_companies = company_list

    if not matched_companies:
        st.warning("No company matches your search keyword.")
    else:
        company = st.selectbox("Select a Company", matched_companies)
        data = filtered[filtered["Name"] == company].iloc[0]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Company Information")
            st.write("**Symbol:**", data.get("Symbol", "N/A"))
            st.write("**Sector:**", data.get("Sector", "N/A"))
            st.write("**Industry:**", data.get("Industry", "N/A"))
            st.write("**Employees:**", data.get("Full Time Employees", "N/A"))
            st.write("**Controversy Level:**", data.get("Controversy Level", "N/A"))
            st.write("**Risk Category:**", data.get("ESG Risk Category", "N/A"))

            st.markdown("### Description")
            st.write(data.get("Description", "No description available."))

        with col2:
            st.markdown("### ESG Metrics")
            st.metric("Total ESG", round(data["Total ESG Risk score"], 2))
            st.metric("Environment", round(data["Environment Risk Score"], 2))
            st.metric("Social", round(data["Social Risk Score"], 2))
            st.metric("Governance", round(data["Governance Risk Score"], 2))

        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.pie(
            [
                data["Environment Risk Score"],
                data["Social Risk Score"],
                data["Governance Risk Score"]
            ],
            labels=["Environment", "Social", "Governance"],
            autopct="%1.1f%%",
            colors=["#2a9d8f", "#f4a261", "#457b9d"],
            startangle=90
        )
        ax.set_title(f"ESG Risk Composition: {company}")
        st.pyplot(fig)

# ================= COMPARISON =================
with tab2:
    st.subheader("Company Comparison")

    company_list = sorted(filtered["Name"].dropna().unique())
    col1, col2 = st.columns(2)

    company1 = col1.selectbox("Company 1", company_list, key="company_1")
    company2 = col2.selectbox("Company 2", company_list, key="company_2")

    d1 = filtered[filtered["Name"] == company1].iloc[0]
    d2 = filtered[filtered["Name"] == company2].iloc[0]

    compare = pd.DataFrame({
        "Total ESG": [d1["Total ESG Risk score"], d2["Total ESG Risk score"]],
        "Environment": [d1["Environment Risk Score"], d2["Environment Risk Score"]],
        "Social": [d1["Social Risk Score"], d2["Social Risk Score"]],
        "Governance": [d1["Governance Risk Score"], d2["Governance Risk Score"]],
        "Employees": [d1["Full Time Employees"], d2["Full Time Employees"]],
        "Controversy": [d1["Controversy Level"], d2["Controversy Level"]],
    }, index=[company1, company2])

    st.markdown("### Comparison Table")
    st.dataframe(compare)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    compare[["Total ESG", "Environment", "Social", "Governance"]].T.plot(
        kind="bar",
        ax=ax,
        color=["#e76f51", "#264653"]
    )
    ax.set_ylabel("Score")
    ax.set_title("ESG Score Comparison")
    plt.xticks(rotation=0)
    st.pyplot(fig)

# ================= SECTOR ANALYSIS =================
with tab3:
    st.subheader("Sector Analysis")

    sector_avg = filtered.groupby("Sector")["Total ESG Risk score"].mean().sort_values()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    sector_avg.plot(
        kind="bar",
        ax=ax,
        color=sns.color_palette("viridis", len(sector_avg))
    )
    ax.set_ylabel("Average ESG Risk Score")
    ax.set_title("Average ESG Risk by Sector")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    st.markdown("### ESG Risk Distribution")
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    ax2.hist(filtered["Total ESG Risk score"], bins=20, color="#6a4c93", alpha=0.8, edgecolor="black")
    ax2.set_xlabel("Total ESG Risk Score")
    ax2.set_ylabel("Number of Companies")
    ax2.set_title("Distribution of ESG Risk Scores")
    st.pyplot(fig2)

    st.markdown("### Lowest and Highest Risk Sectors")
    col1, col2 = st.columns(2)

    col1.write("**Lowest Average Risk Sectors**")
    col1.dataframe(
        sector_avg.head(5).reset_index().rename(
            columns={"Total ESG Risk score": "Avg ESG"}
        )
    )

    col2.write("**Highest Average Risk Sectors**")
    col2.dataframe(
        sector_avg.tail(5).sort_values(ascending=False).reset_index().rename(
            columns={"Total ESG Risk score": "Avg ESG"}
        )
    )

# ================= ESG RELATIONSHIPS =================
with tab4:
    st.subheader("ESG Relationships")

    # ---------- Average ESG component scores ----------
    st.markdown("### Average ESG Component Scores")

    component_means = filtered[
        ["Environment Risk Score", "Social Risk Score", "Governance Risk Score"]
    ].mean()

    fig3, ax3 = plt.subplots(figsize=(7, 4.5))
    component_means.plot(
        kind="bar",
        ax=ax3,
        color=["#2a9d8f", "#f4a261", "#457b9d"],
        edgecolor="black"
    )
    ax3.set_ylabel("Average Score")
    ax3.set_title("Average Environment, Social, and Governance Risk Scores")
    ax3.set_xticklabels(["Environment", "Social", "Governance"], rotation=0)
    ax3.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig3)

    # ---------- Employees vs ESG ----------
    st.markdown("### Employees vs ESG Risk")

    filtered_scatter = filtered.dropna(subset=["Full Time Employees", "Total ESG Risk score"])
    full_scatter = df.dropna(subset=["Full Time Employees", "Total ESG Risk score"])

    if not filtered_scatter.empty:
        scatter_source = filtered_scatter
        st.caption("Data source: current filtered dataset")
    elif not full_scatter.empty:
        scatter_source = full_scatter
        st.caption("Data source: full dataset (fallback because filtered data has no valid employee records)")
    else:
        scatter_source = pd.DataFrame()

    fig4, ax4 = plt.subplots(figsize=(7, 4.5))

    if not scatter_source.empty:
        ax4.scatter(
            scatter_source["Full Time Employees"],
            scatter_source["Total ESG Risk score"],
            alpha=0.65,
            color="#2a9d8f",
            edgecolors="black",
            linewidths=0.3
        )
        ax4.set_xlabel("Full Time Employees")
        ax4.set_ylabel("Total ESG Risk Score")
        ax4.set_title("Company Size and ESG Risk")
        ax4.grid(True, linestyle="--", alpha=0.4)
    else:
        ax4.text(
            0.5, 0.5,
            "No employee data available in dataset",
            ha="center", va="center", fontsize=12
        )
        ax4.set_xticks([])
        ax4.set_yticks([])
        ax4.set_title("Company Size and ESG Risk")

    st.pyplot(fig4)

    # ---------- Correlation Matrix ----------
    st.markdown("### Correlation Matrix")

    corr_cols = [
        "Total ESG Risk score",
        "Environment Risk Score",
        "Social Risk Score",
        "Governance Risk Score",
        "Full Time Employees"
    ]

    corr_data = filtered[corr_cols].copy()
    fig5, ax5 = plt.subplots(figsize=(8, 5.5))

    if corr_data.dropna(how="all").empty:
        ax5.text(
            0.5, 0.5,
            "No sufficient data for correlation matrix",
            ha="center", va="center", fontsize=12
        )
        ax5.set_xticks([])
        ax5.set_yticks([])
        ax5.set_title("Correlation Matrix")
    else:
        corr = corr_data.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax5)
        ax5.set_title("Correlation Matrix")

    st.pyplot(fig5)

# ================= RANKING =================
with tab5:
    st.subheader("Company Ranking")

    top_n = st.slider("Select Top / Bottom N", 5, 20, 10)

    best = filtered.sort_values("Total ESG Risk score").head(top_n)
    worst = filtered.sort_values("Total ESG Risk score", ascending=False).head(top_n)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Lowest ESG Risk Companies")
        st.dataframe(best[["Name", "Sector", "Total ESG Risk score", "ESG Risk Category"]])

    with col2:
        st.markdown("### Highest ESG Risk Companies")
        st.dataframe(worst[["Name", "Sector", "Total ESG Risk score", "ESG Risk Category"]])

    fig6, ax6 = plt.subplots(figsize=(8, 4.5))
    ax6.barh(best["Name"], best["Total ESG Risk score"], color="#457b9d")
    ax6.set_xlabel("Total ESG Risk Score")
    ax6.set_title("Lowest ESG Risk Companies")
    ax6.invert_yaxis()
    st.pyplot(fig6)

    fig7, ax7 = plt.subplots(figsize=(8, 4.5))
    ax7.barh(worst["Name"], worst["Total ESG Risk score"], color="#e63946")
    ax7.set_xlabel("Total ESG Risk Score")
    ax7.set_title("Highest ESG Risk Companies")
    ax7.invert_yaxis()
    st.pyplot(fig7)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Dashboard created for ESG risk analysis of S&P 500 companies using Streamlit, Pandas, Matplotlib, and Seaborn.")