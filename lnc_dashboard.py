import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

# Set page configuration
st.set_page_config(
    page_title="LNC Implementation Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and introduction
st.title("LNC Implementation Dashboard")
st.markdown("### Analysis and Visualization of LNC Implementation Data")

# Define default files (for local development)
DEFAULT_CYCLE1_FILE = "Cycle 1 LNC Implementation  Analysis January 25.xlsx"
DEFAULT_COMPARISON_FILE = "LNC Implementation Comparison Graph January 25.xlsx"

# Add file upload option
st.sidebar.header("Upload Data Files")
st.sidebar.markdown("Upload your Excel files or use the default files if available:")

uploaded_cycle1 = st.sidebar.file_uploader("Upload Cycle 1 Analysis File", type=["xlsx"])
uploaded_comparison = st.sidebar.file_uploader("Upload Comparison Graph File", type=["xlsx"])

# Function to load data
@st.cache_data
def load_data(cycle1_file, comparison_file):
    try:
        # Load Cycle 1 data
        if isinstance(cycle1_file, io.BytesIO):  # Uploaded file
            cycle1_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1")
            cycle1_state_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1 State DPM wise status")
        else:  # Local file path
            cycle1_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1")
            cycle1_state_df = pd.read_excel(cycle1_file, sheet_name="Cycle 1 State DPM wise status")
        
        # Load comparison data
        if isinstance(comparison_file, io.BytesIO):  # Uploaded file
            comparison_df = pd.read_excel(comparison_file, sheet_name="Comparison Graph")
        else:  # Local file path
            comparison_df = pd.read_excel(comparison_file, sheet_name="Comparison Graph")
        
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
        comparison_cleaned = comparison_cleaned.iloc[1:].reset_index(drop=True)  # Remove first row (dates)
        comparison_cleaned.fillna(0, inplace=True)  # Replace NaN with 0

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Implementation Overview", "District Performance", "Comparison Across Cycles"])

        # Tab 1: Implementation Overview
        with tab1:
            st.header("Implementation Overview")
            
            # Display key metrics from the State DPM wise status sheet
            st.subheader("Key Implementation Metrics")
            
            # Filter out rows with sensible data (remove headers)
            state_data = cycle1_state_df[cycle1_state_df['CG State wide Implementation table'].notna() & 
                                         cycle1_state_df['CG State wide Implementation table'] != 'NaN']
            
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
                        ls_row = comparison_cleaned[comparison_cleaned['Questions'].str.contains('LS', na=False)]
                        if not ls_row.empty:
                            ls_value = ls_row.iloc[0]['Cycle 1']
                            st.metric("LS Training Attendance", f"{ls_value}%")
                        else:
                            st.metric("LS Training Attendance", "N/A")
                    except:
                        st.metric("LS Training Attendance", "N/A")
                        
                with metrics_col4:
                    try:
                        # Find AWW attendance in comparison data
                        aww_row = comparison_cleaned[comparison_cleaned['Questions'].str.contains('AWW', na=False)]
                        if not aww_row.empty:
                            aww_value = aww_row.iloc[0]['Cycle 1']
                            st.metric("AWW Training Attendance", f"{aww_value}%")
                        else:
                            st.metric("AWW Training Attendance", "N/A")
                    except:
                        st.metric("AWW Training Attendance", "N/A")
            
            # Create a bar chart for key metrics from comparison data
            st.subheader("Implementation Metrics - Cycle 1")
            
            # Clean questions for better display
            comparison_cleaned['Questions'] = comparison_cleaned['Questions'].str.replace('%', '')
            comparison_cleaned['Questions'] = comparison_cleaned['Questions'].str.replace('/', '-')
            
            # Create bar chart
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

        # Tab 2: District Performance
        with tab2:
            st.header("District Performance Analysis")
            
            # Filter state data to get district-level data
            district_data = None
            
            try:
                # Find district column and filter out headers
                district_data = cycle1_state_df[cycle1_state_df['Unnamed: 3'].notna() & 
                                              (cycle1_state_df['Unnamed: 3'] != 'District')]
                district_data = district_data[['Unnamed: 3', 'Unnamed: 10', 'Unnamed: 15', 'Unnamed: 22', 'Unnamed: 27']]
                district_data.columns = ['District', 'CDPO Training', 'CDPO Lab Practice', 'LS AWW Workshop', 'AWW Training']
            except:
                st.error("Could not extract district data from the Excel file. The format may be different than expected.")
            
            if district_data is not None and not district_data.empty:
                # Display district data table
                st.subheader("District Performance Table")
                st.dataframe(district_data, use_container_width=True)
                
                # Create district comparison chart
                st.subheader("District Performance Comparison")
                
                # Allow user to select metrics to compare
                selected_metrics = st.multiselect(
                    "Select metrics to compare across districts",
                    options=district_data.columns[1:].tolist(),
                    default=district_data.columns[1:3].tolist()
                )
                
                if selected_metrics:
                    # Prepare data for visualization
                    plot_data = district_data.melt(
                        id_vars=['District'],
                        value_vars=selected_metrics,
                        var_name='Metric',
                        value_name='Percentage'
                    )
                    
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
                    
                    # Create heatmap for comprehensive view
                    st.subheader("District Performance Heatmap")
                    
                    # Prepare data for heatmap
                    heatmap_data = district_data.set_index('District')
                    heatmap_data = heatmap_data[selected_metrics]
                    
                    # Create heatmap
                    fig = px.imshow(
                        heatmap_data.values,
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        color_continuous_scale=px.colors.sequential.Blues,
                        labels=dict(x="Metric", y="District", color="Percentage"),
                        title="Performance Heatmap by District"
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

        # Tab 3: Comparison Across Cycles
        with tab3:
            st.header("Comparison Across Implementation Cycles")
            
            # Display comparison data
            st.subheader("Cycle Comparison Data")
            st.dataframe(comparison_cleaned, use_container_width=True)
            
            # Create line chart to compare metrics across cycles
            st.subheader("Trends Across Implementation Cycles")
            
            # Allow user to select metrics to compare
            selected_questions = st.multiselect(
                "Select metrics to compare across cycles",
                options=comparison_cleaned['Questions'].tolist(),
                default=comparison_cleaned['Questions'].tolist()[:3]
            )
            
            if selected_questions:
                # Filter data based on selection
                filtered_data = comparison_cleaned[comparison_cleaned['Questions'].isin(selected_questions)]
                
                # Prepare data for line chart
                plot_data = filtered_data.melt(
                    id_vars=['Questions'],
                    value_vars=['Cycle 1', 'Cycle 2', 'Cycle 2.1', 'Cycle 3'],
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
                
                # Create radar chart for comprehensive comparison
                st.subheader("Radar Chart: Metrics Across Cycles")
                
                # Create radar chart
                fig = go.Figure()
                
                # Add traces for each cycle
                for cycle in ['Cycle 1', 'Cycle 2', 'Cycle 2.1', 'Cycle 3']:
                    cycle_data = filtered_data.copy()
                    fig.add_trace(go.Scatterpolar(
                        r=cycle_data[cycle].values,
                        theta=cycle_data['Questions'].values,
                        fill='toself',
                        name=cycle
                    ))
                
                # Update layout
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**LNC Implementation Dashboard** | Created on: April 2025")
