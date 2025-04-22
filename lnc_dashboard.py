import streamlit as st
import pandas as pd
import os
import io

# Set page configuration
st.set_page_config(
    page_title="LNC Implementation Dashboard",
    page_icon="📊",
    layout="wide"
)

# Import visualization libraries only when needed
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    st.warning("Plotly not found. Installing...")
    # Auto-install if missing
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly==5.14.1"])
    import plotly.express as px
    import plotly.graph_objects as go

# Title and introduction
st.title("LNC Implementation Dashboard")
st.markdown("### Analysis and Visualization of LNC Implementation Data")

# Function to safely convert columns to appropriate types
def safe_convert_types(df):
    try:
        for col in df.columns:
            # Try to convert numeric columns
            try:
                if df[col].dtype == 'object':
                    # Try to convert to numeric, but keep as string if it fails
                    df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
        return df
    except Exception as e:
        st.error(f"Error converting data types: {e}")
        return df

# Define default files (for local development)
DEFAULT_CYCLE1_FILE = "Cycle 1 LNC Implementation  Analysis January 25.xlsx"
DEFAULT_COMPARISON_FILE = "LNC Implementation Comparison Graph January 25.xlsx"

# Add file upload option
st.sidebar.header("Upload Data Files")
st.sidebar.markdown("Upload your Excel files or use the default files if available:")

uploaded_cycle1 = st.sidebar.file_uploader("Upload Cycle 1 Analysis File", type=["xlsx"])
uploaded_comparison = st.sidebar.file_uploader("Upload Comparison Graph File", type=["xlsx"])

# Function to load data with enhanced error handling
@st.cache_data
def load_data(cycle1_file, comparison_file):
    try:
        # Load Cycle 1 data
        if isinstance(cycle1_file, io.BytesIO):  # Uploaded file
            cycle1_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1", dtype=str)
            cycle1_state_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1 State DPM wise status", dtype=str)
        else:  # Local file path
            cycle1_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1", dtype=str)
            cycle1_state_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1 State DPM wise status", dtype=str)
        
        # Load comparison data
        if isinstance(comparison_file, io.BytesIO):  # Uploaded file
            comparison_df = pd.read_excel(comparison_file, sheet_name="Comparison Graph", dtype=str)
        else:  # Local file path
            comparison_df = pd.read_excel(comparison_file, sheet_name="Comparison Graph", dtype=str)
        
        # Convert types safely
        cycle1_df = safe_convert_types(cycle1_df)
        cycle1_state_df = safe_convert_types(cycle1_state_df)
        comparison_df = safe_convert_types(comparison_df)
        
        return cycle1_df, cycle1_state_df, comparison_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Determine which files to use
if uploaded_cycle1 is not None:
    cycle1_file = uploaded_cycle1
else:
    # Try to use the default file if it exists
    if os.path.exists(DEFAULT_CYCLE1_FILE):
        cycle1_file = DEFAULT_CYCLE1_FILE
    else:
        st.warning(f"Default file {DEFAULT_CYCLE1_FILE} not found. Please upload a file.")
        cycle1_file = None

if uploaded_comparison is not None:
    comparison_file = uploaded_comparison
else:
    # Try to use the default file if it exists
    if os.path.exists(DEFAULT_COMPARISON_FILE):
        comparison_file = DEFAULT_COMPARISON_FILE
    else:
        st.warning(f"Default file {DEFAULT_COMPARISON_FILE} not found. Please upload a file.")
        comparison_file = None

# Only proceed if we have data
if cycle1_file is not None and comparison_file is not None:
    # Load data
    cycle1_df, cycle1_state_df, comparison_df = load_data(cycle1_file, comparison_file)
    
    if cycle1_df is not None and cycle1_state_df is not None and comparison_df is not None:
        # Clean comparison data
        comparison_cleaned = comparison_df.copy()
        # First row might contain dates - identify and skip
        if pd.to_datetime(comparison_cleaned.iloc[0, 1:], errors='coerce').notna().any():
            comparison_cleaned = comparison_cleaned.iloc[1:].reset_index(drop=True)
        comparison_cleaned.fillna(0, inplace=True)  # Replace NaN with 0
        
        # Convert percentage columns to numeric
        for col in comparison_cleaned.columns:
            if col != 'Questions':
                comparison_cleaned[col] = pd.to_numeric(comparison_cleaned[col], errors='coerce')

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Implementation Overview", "District Performance", "Comparison Across Cycles"])

        # Tab 1: Implementation Overview
        with tab1:
            st.header("Implementation Overview")
            
            # Display key metrics from the State DPM wise status sheet
            st.subheader("Key Implementation Metrics")
            
            # Filter out rows with sensible data (remove headers)
            state_data = cycle1_state_df[cycle1_state_df['CG State wide Implementation table'].notna() & 
                                         (cycle1_state_df['CG State wide Implementation table'] != 'NaN')]
            
            # Calculate overall metrics
            if not state_data.empty:
                metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
                
                # Find columns with percentages (may need adjustment based on your actual data)
                dpo_attendance_col = '% DPOs/ DWCDOs attended central workshop'
                cdpo_attendance_col = '% of CDPOs Attended workshop'
                ls_attendance_col = '% of LS attended workshop'
                aww_attendance_col = '% of AWWs received training'
                
                # Try to find columns - if they don't exist exactly, use closest match
                if dpo_attendance_col not in state_data.columns:
                    dpo_attendance_col = [col for col in state_data.columns if '% DPO' in col and 'attend' in col.lower()]
                    dpo_attendance_col = dpo_attendance_col[0] if dpo_attendance_col else None
                
                if cdpo_attendance_col not in state_data.columns:
                    cdpo_attendance_col = [col for col in state_data.columns if '% CDPO' in col and 'attend' in col.lower()]
                    cdpo_attendance_col = cdpo_attendance_col[0] if cdpo_attendance_col else None
                    
                if ls_attendance_col not in state_data.columns:
                    ls_attendance_col = [col for col in state_data.columns if '% LS' in col and 'attend' in col.lower()]
                    ls_attendance_col = ls_attendance_col[0] if ls_attendance_col else None
                    
                if aww_attendance_col not in state_data.columns:
                    aww_attendance_col = [col for col in state_data.columns if '% AWW' in col and 'train' in col.lower()]
                    aww_attendance_col = aww_attendance_col[0] if aww_attendance_col else None
                
                # Extract the values from comparison_df for Cycle 1 since they're cleaner
                with metrics_col1:
                    try:
                        dpo_value = comparison_cleaned.loc[0, 'Cycle 1']
                        st.metric("DPO/DWCDO Workshop Attendance", f"{dpo_value}%")
                    except:
                        st.metric("DPO/DWCDO Workshop Attendance", "N/A")
                        
                with metrics_col2:
                    try:
                        cdpo_value = comparison_cleaned.loc[3, 'Cycle 1']
                        st.metric("CDPO Training Attendance", f"{cdpo_value}%")
                    except:
                        st.metric("CDPO Training Attendance", "N/A")
                        
                with metrics_col3:
                    try:
                        # Find LS attendance in comparison data
                        ls_rows = comparison_cleaned[comparison_cleaned['Questions'].str.contains('LS', na=False, case=False)]
                        if not ls_rows.empty:
                            ls_value = ls_rows.iloc[0]['Cycle 1']
                            st.metric("LS Training Attendance", f"{ls_value}%")
                        else:
                            st.metric("LS Training Attendance", "N/A")
                    except:
                        st.metric("LS Training Attendance", "N/A")
                        
                with metrics_col4:
                    try:
                        # Find AWW attendance in comparison data
                        aww_rows = comparison_cleaned[comparison_cleaned['Questions'].str.contains('AWW', na=False, case=False)]
                        if not aww_rows.empty:
                            aww_value = aww_rows.iloc[0]['Cycle 1']
                            st.metric("AWW Training Attendance", f"{aww_value}%")
                        else:
                            st.metric("AWW Training Attendance", "N/A")
                    except:
                        st.metric("AWW Training Attendance", "N/A")
            
            # Create a bar chart for key metrics from comparison data
            st.subheader("Implementation Metrics - Cycle 1")
            
            # Clean questions for better display
            comparison_cleaned['Questions'] = comparison_cleaned['Questions'].astype(str)
            comparison_cleaned['Questions'] = comparison_cleaned['Questions'].str.replace('%', '')
            comparison_cleaned['Questions'] = comparison_cleaned['Questions'].str.replace('/', '-')
            
            # Create bar chart
            try:
                fig = px.bar(
                    comparison_cleaned, 
                    x='Questions', 
                    y='Cycle 1',
                    labels={'Questions': 'Metric', 'Cycle 1': 'Percentage (%)'},
                    title='Cycle 1 Implementation Metrics',
                    color='Cycle 1',
                    color_continuous_scale=px.colors.sequential.Blues
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating bar chart: {e}")
                st.write("Raw data:")
                st.dataframe(comparison_cleaned)

        # Tab 2: District Performance
        with tab2:
            st.header("District Performance Analysis")
            
            # Filter state data to get district-level data
            district_data = None
            
            try:
                # Find district column and filter out headers
                district_col = "Unnamed: 3"  # This is the column name from the original analysis
                if district_col in cycle1_state_df.columns:
                    district_data = cycle1_state_df[cycle1_state_df[district_col].notna() & 
                                                  (cycle1_state_df[district_col] != 'District')]
                    target_cols = [district_col, 'Unnamed: 10', 'Unnamed: 15', 'Unnamed: 22', 'Unnamed: 27']
                    available_cols = [col for col in target_cols if col in cycle1_state_df.columns]
                    
                    if len(available_cols) > 1:  # At least district column + one metric
                        district_data = district_data[available_cols]
                        district_data.columns = ['District'] + [f'Metric {i}' for i in range(len(available_cols)-1)]
                    else:
                        st.error("Could not find enough metric columns in the data")
                        district_data = None
                else:
                    st.error(f"District column '{district_col}' not found")
                    # Show available columns
                    st.write("Available columns:")
                    st.write(cycle1_state_df.columns.tolist())
            except Exception as e:
                st.error(f"Could not extract district data from the Excel file: {e}")
            
            if district_data is not None and not district_data.empty:
                # Display district data table
                st.subheader("District Performance Table")
                st.dataframe(district_data, use_container_width=True)
                
                # Create district comparison chart
                st.subheader("District Performance Comparison")
                
                # Allow user to select metrics to compare
                metric_cols = district_data.columns[1:].tolist()
                if metric_cols:
                    selected_metrics = st.multiselect(
                        "Select metrics to compare across districts",
                        options=metric_cols,
                        default=metric_cols[:min(2, len(metric_cols))]
                    )
                    
                    if selected_metrics:
                        try:
                            # Prepare data for visualization
                            plot_data = district_data.melt(
                                id_vars=['District'],
                                value_vars=selected_metrics,
                                var_name='Metric',
                                value_name='Percentage'
                            )
                            
                            # Convert percentage to numeric
                            plot_data['Percentage'] = pd.to_numeric(plot_data['Percentage'], errors='coerce')
                            
                            # Create grouped bar chart
                            fig = px.bar(
                                plot_data,
                                x='District',
                                y='Percentage',
                                color='Metric',
                                barmode='group',
                                title='District Performance by Key Metrics',
                                labels={'Percentage': 'Percentage (%)', 'District': 'District Name'}
                            )
                            fig.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error creating district comparison chart: {e}")
                            st.write("Raw data:")
                            st.dataframe(plot_data)

        # Tab 3: Comparison Across Cycles
        with tab3:
            st.header("Comparison Across Implementation Cycles")
            
            # Display comparison data
            st.subheader("Cycle Comparison Data")
            st.dataframe(comparison_cleaned, use_container_width=True)
            
            # Create line chart to compare metrics across cycles
            st.subheader("Trends Across Implementation Cycles")
            
            # Allow user to select metrics to compare
            if 'Questions' in comparison_cleaned.columns:
                question_options = comparison_cleaned['Questions'].dropna().astype(str).tolist()
                
                if question_options:
                    selected_questions = st.multiselect(
                        "Select metrics to compare across cycles",
                        options=question_options,
                        default=question_options[:min(3, len(question_options))]
                    )
                    
                    if selected_questions:
                        try:
                            # Filter data based on selection
                            filtered_data = comparison_cleaned[comparison_cleaned['Questions'].isin(selected_questions)]
                            
                            # Identify cycle columns
                            cycle_cols = [col for col in comparison_cleaned.columns 
                                          if col.startswith('Cycle') and col != 'Questions']
                            
                            if cycle_cols:
                                # Prepare data for line chart
                                plot_data = filtered_data.melt(
                                    id_vars=['Questions'],
                                    value_vars=cycle_cols,
                                    var_name='Cycle',
                                    value_name='Percentage'
                                )
                                
                                # Create line chart
                                fig = px.line(
                                    plot_data,
                                    x='Cycle',
                                    y='Percentage',
                                    color='Questions',
                                    markers=True,
                                    labels={'Percentage': 'Percentage (%)', 'Cycle': 'Implementation Cycle'},
                                    title='Implementation Metrics Across Cycles'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.error("No cycle columns found in the data")
                        except Exception as e:
                            st.error(f"Error creating cycle comparison chart: {e}")
                            st.write("Raw data for debugging:")
                            st.dataframe(filtered_data)
                else:
                    st.error("No question options found in the data")
            else:
                st.error("'Questions' column not found in comparison data")
    else:
        st.error("Error loading the data files. Please check the format and try again.")
else:
    st.info("Please upload both files to view the dashboard.")

# Footer
st.markdown("---")
st.markdown("**LNC Implementation Dashboard** | Created on: April 2025")
