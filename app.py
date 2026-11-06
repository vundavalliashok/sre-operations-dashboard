import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(
    page_title="SRE Operations Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 SRE Operations Dashboard")
st.caption("Site Reliability Engineering | DevOps Operations")

# Simulated operational metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Service Availability", "99.95%", "+0.05%")
col2.metric("Active Incidents", "3", "-2")
col3.metric("Deployment Success", "96.5%", "+1.5%")
col4.metric("Avg Response Time", "145 ms", "-12 ms")

st.divider()

st.subheader("Infrastructure Monitoring")

data = pd.DataFrame({
    "Server": ["Server 1", "Server 2", "Server 3", "Server 4"],
    "CPU Usage": [45, 67, 82, 35],
    "Memory Usage": [60, 75, 89, 42]
})

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        px.bar(data, x="Server", y="CPU Usage",
               title="CPU Utilization (%)"),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        px.bar(data, x="Server", y="Memory Usage",
               title="Memory Utilization (%)"),
        use_container_width=True
    )

st.subheader("Incident Management")

incidents = pd.DataFrame({
    "Incident ID": ["INC001", "INC002", "INC003"],
    "Service": ["Payment API", "Authentication", "Database"],
    "Severity": ["Critical", "High", "Medium"],
    "Status": ["Open", "Investigating", "Resolved"]
})

st.dataframe(incidents, use_container_width=True)

st.subheader("SLO Monitoring")

slo = pd.DataFrame({
    "Service": ["Payment API", "Authentication", "Customer API"],
    "SLO Target": [99.9, 99.95, 99.5],
    "Actual Availability": [99.95, 99.97, 99.3]
})

st.dataframe(slo, use_container_width=True)

st.success("SRE Operations Dashboard is running!")