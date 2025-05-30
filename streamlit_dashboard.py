import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Simple Password Gate
# ------------------------
password = st.text_input("Enter password to access dashboard", type="password")
if password != "@Pc1D$5s_2025!":
    st.warning("Access Denied. Please enter the correct password.")
    st.stop()

# Load the Excel file
df = pd.read_excel("PCI_DSS_4.0.1_Compliance_Tracker_2025.xlsx", sheet_name="PCI DSS Audit Evidences")

# Clean data
df['Status'] = df['Status'].astype(str).str.strip()
df['Category'] = df['Category'].astype(str).str.strip()
df['PCI DSS Reference'] = df['PCI DSS Reference'].astype(str).str.strip()

# Sidebar filters
st.sidebar.title("Filter")
status_filter = st.sidebar.multiselect("Select Status", options=df['Status'].unique(), default=df['Status'].unique())
pci_filter = st.sidebar.multiselect("Select PCI DSS Reference", options=df['PCI DSS Reference'].unique(), default=df['PCI DSS Reference'].unique())

# Apply filters
filtered_df = df[(df['Status'].isin(status_filter)) & (df['PCI DSS Reference'].isin(pci_filter))]

# Dashboard Title
st.title("PCI DSS 4.0.1 Compliance Dashboard")

# Completion Percentage Logic
complete_statuses = ['Done', 'Done*', 'Not Applicable']
completed_count = filtered_df['Status'].isin(complete_statuses).sum()
total_items = len(filtered_df)
completion_percentage = round((completed_count / total_items) * 100, 2) if total_items else 0

st.metric("Completion %", f"{completion_percentage}%")

# Status Summary Chart
status_summary = filtered_df['Status'].value_counts().reset_index()
status_summary.columns = ['Status', 'Count']
fig1 = px.bar(status_summary, x='Status', y='Count', title="Status Summary", text_auto=True)
st.plotly_chart(fig1)

# Category Summary Chart
category_summary = filtered_df['Category'].value_counts().reset_index()
category_summary.columns = ['Category', 'Count']
fig2 = px.pie(category_summary, names='Category', values='Count', title="Category Distribution")
st.plotly_chart(fig2)

# Show raw data
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True))
