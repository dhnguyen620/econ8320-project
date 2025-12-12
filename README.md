# \# US Labor Statistics Dashboard

# 

# An automated, interactive dashboard tracking key US labor market indicators using data from the Bureau of Labor Statistics (BLS) API.

# 

# 🔗 \*\*\[Live Dashboard](https://econ8320-project-d27imgdnynvnkogdjhs5lv.streamlit.app/)\*\*

# 

# \## 📊 Overview

# 

# This project provides real-time visualization of critical labor market metrics from January 2020 to present, including:

# 

# \- \*\*Total Nonfarm Employment\*\* - Overall employment levels across all industries

# \- \*\*Unemployment Rate\*\* - Percentage of labor force that is unemployed

# \- \*\*Labor Force Participation Rate\*\* - Percentage of population in the labor force

# \- \*\*Average Hourly Earnings\*\* - Wage growth indicator

# \- \*\*Manufacturing Employment\*\* - Employment in manufacturing sector

# \- \*\*Leisure \& Hospitality Employment\*\* - Service sector employment

# \- \*\*Professional \& Business Services Employment\*\* - White-collar job market

# 

# \## 🚀 Features

# 

# \- \*\*Automated Data Collection\*\*: GitHub Actions automatically fetches new data monthly when BLS releases updates

# \- \*\*Interactive Visualizations\*\*: Dynamic charts with filtering and date range selection

# \- \*\*Historical Analysis\*\*: 5+ years of data showing COVID-19 impact and recovery

# \- \*\*Real-time Updates\*\*: Dashboard automatically refreshes with new data

# \- \*\*Data Export\*\*: Download filtered data as CSV

# 

# \## 🛠️ Technology Stack

# 

# \- \*\*Data Collection\*\*: Python, BLS Public API

# \- \*\*Data Processing\*\*: Pandas

# \- \*\*Visualization\*\*: Streamlit, Plotly

# \- \*\*Automation\*\*: GitHub Actions

# \- \*\*Deployment\*\*: Streamlit Community Cloud

# \- \*\*Version Control\*\*: Git/GitHub

# 

# \## 📁 Project Structure

# ```

# BLS-Labor-Dashboard/

# ├── app.py                          # Streamlit dashboard application

# ├── src/

# │   └── collect\_data.py            # BLS API data collection script

# ├── data/

# │   └── processed/

# │       └── labor\_stats.csv        # Processed labor statistics data

# ├── .github/

# │   └── workflows/

# │       └── update\_data.yml        # GitHub Actions automation

# ├── requirements.txt                # Python dependencies

# └── README.md                       # Project documentation

# ```

# 

# \## 🔧 Installation \& Setup

# 

# \### Prerequisites

# \- Python 3.11+

# \- Git

# 

# \### Local Setup

# 

# 1\. \*\*Clone the repository\*\*

# ```bash

# &nbsp;  git clone https://github.com/dhnguyen620/econ8320-project.git

# &nbsp;  cd econ8320-project/BLS-Labor-Dashboard

# ```

# 

# 2\. \*\*Install dependencies\*\*

# ```bash

# &nbsp;  pip install -r requirements.txt

# ```

# 

# 3\. \*\*Run data collection\*\* (optional - data already included)

# ```bash

# &nbsp;  python src/collect\_data.py

# ```

# 

# 4\. \*\*Launch dashboard locally\*\*

# ```bash

# &nbsp;  streamlit run app.py

# ```

# 

# 5\. \*\*Open your browser\*\* to `http://localhost:8501`

# 

# \## 📈 Data Sources

# 

# All data is sourced from the \*\*U.S. Bureau of Labor Statistics (BLS)\*\* Public Data API:

# \- \*\*API Documentation\*\*: https://www.bls.gov/developers/home.htm

# \- \*\*Data Update Frequency\*\*: Monthly (typically first Friday of each month)

# \- \*\*Historical Range\*\*: January 2020 - Present

# 

# \### BLS Series IDs Used:

# \- `CES0000000001` - Total Nonfarm Employment

# \- `LNS14000000` - Unemployment Rate

# \- `LNS11300000` - Labor Force Participation Rate

# \- `CES0500000003` - Average Hourly Earnings

# \- `CES3000000001` - Manufacturing Employment

# \- `CES7000000001` - Leisure \& Hospitality Employment

# \- `CES6000000001` - Professional \& Business Services Employment

# 

# \## 🤖 Automation

# 

# The project uses \*\*GitHub Actions\*\* to automatically:

# 1\. Run data collection script monthly

# 2\. Fetch latest BLS data

# 3\. Append new records to dataset

# 4\. Commit and push updates to repository

# 5\. Trigger Streamlit dashboard redeploy

# 

# \*\*Workflow Schedule\*\*: First Friday of every month at 10:00 AM UTC

# 

# Manual workflow trigger available at: \[Actions Tab](https://github.com/dhnguyen620/econ8320-project/actions)

# 

# \## 📊 Dashboard Features

# 

# \### Overview Metrics

# \- Latest values for all tracked series

# \- Month-over-month change indicators

# \- Percentage change calculations

# 

# \### Visualizations

# \- \*\*Individual Series Charts\*\*: Detailed time series for each metric

# \- \*\*Comparison View\*\*: Multi-series overlay to identify correlations

# \- \*\*Month-over-Month Changes\*\*: Percentage change analysis

# \- \*\*Data Table\*\*: Raw data view with download capability

# 

# \### Interactive Controls

# \- Date range selector

# \- Series filter (select which metrics to display)

# \- Export data as CSV

# 

# \## 🎓 Project Context

# 

# This project was developed for \*\*ECON 8320 - Tools for Data Analysis\*\* to demonstrate:

# \- API integration and data collection

# \- Data processing and cleaning

# \- Interactive dashboard development

# \- Workflow automation

# \- Cloud deployment

# 

# \## 📝 Key Insights

# 

# The dashboard reveals significant labor market trends:

# \- \*\*COVID-19 Impact (2020)\*\*: Dramatic employment drops, especially in Leisure \& Hospitality

# \- \*\*Recovery Period (2021-2022)\*\*: Gradual employment recovery across sectors

# \- \*\*Recent Trends (2023-2025)\*\*: Stabilization and continued growth in most sectors

# 

# \## 🔮 Future Enhancements

# 

# Potential improvements for future iterations:

# \- Add year-over-year comparison visualizations

# \- Include additional BLS series (JOLTS, productivity metrics)

# \- Implement data analysis/forecasting models

# \- Add industry-specific deep dives

# \- Create email alerts for significant changes

# \- Add API key support for higher rate limits

# 

# \## 👤 Author

# 

# \*\*\DANG NGUYEN\*\*

# \- GitHub: \[@dhnguyen620](https://github.com/dhnguyen620)

# \- Project: ECON 8320 Semester Project

# \- Institution: \UNIVERSITY OF NEBRASKA AT OMAHA

# 

# \## 📄 License

# 

# This project is open source and available for educational purposes.

# 

# \## 🙏 Acknowledgments

# 

# \- U.S. Bureau of Labor Statistics for providing public data API

# \- Streamlit for free hosting platform

# \- Course: ECON 8320 - Tools for Data Analysis

# 

# ---

# 

# \*\*Last Updated\*\*: December 2025  

# \*\*Data Range\*\*: January 2020 - September 2025  

# \*\*Total Records\*\*: 483

