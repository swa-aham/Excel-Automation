# LNC Implementation Dashboard

An interactive dashboard for visualizing LNC implementation metrics and performance across different cycles and districts.

## Features

- **Implementation Overview**: View key metrics and a comprehensive bar chart of all implementation data
- **District Performance**: Compare district-level performance with interactive visualizations
- **Cycle Comparison**: Analyze trends across implementation cycles with line charts and radar diagrams

## Getting Started

### Prerequisites

- Python 3.7+
- Required packages: streamlit, pandas, plotly, openpyxl, matplotlib

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```
   streamlit run lnc_dashboard.py
   ```

### Data Files

The dashboard works with two Excel files:
- `Cycle 1 LNC Implementation Analysis January 25.xlsx`
- `LNC Implementation Comparison Graph January 25.xlsx`

You can either place these files in the same directory as the app or upload them through the app's interface.

## Deployment

This dashboard is ready to deploy on Streamlit Cloud. Follow these steps:

1. Push this repository to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud) and connect your GitHub repository
3. Configure the deployment to use the `lnc_dashboard.py` file as the main app

## License

This project is open source and available under the [MIT License](LICENSE).
