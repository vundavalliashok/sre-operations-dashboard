import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="SRE Operations Dashboard",
    page_icon=":material/monitoring:",
    layout="wide",
)

data = pd.DataFrame(
    {
        "Server": ["AZRMDELPRDWEB1", "AZRMDELPRDWEB2", "AZRMDELPRDAPP", "AZRMDELPRDSDB"],
        "CPU Usage": [45, 67, 82, 35],
        "Memory Usage": [60, 75, 89, 42],
    }
)

incidents = pd.DataFrame(
    {
        "Incident ID": ["INC001", "INC002", "INC003"],
        "Service": ["Payment API", "Authentication", "Database"],
        "Severity": ["Critical", "High", "Medium"],
        "Status": ["Open", "Investigating", "Resolved"],
    }
)

slo = pd.DataFrame(
    {
        "Service": ["Payment API", "Authentication", "Customer API"],
        "SLO Target": [99.9, 99.95, 99.5],
        "Actual Availability": [99.95, 99.97, 99.3],
    }
)

active_incidents = incidents["Status"].isin(["Open", "Investigating"]).sum()
services_meeting_slo = (
    slo["Actual Availability"] >= slo["SLO Target"]
).sum()

st.title("SRE operations center", icon=":material/monitoring:")
st.caption(
    "Reliability health, infrastructure utilization, and incident response at a glance."
)
st.badge("Demo telemetry", icon=":material/info:", color="blue")

with st.container(horizontal=True):
    st.metric(
        "Service availability",
        "99.95%",
        "+0.05%",
        delta_color="normal",
        border=True,
    )
    st.metric(
        "Active incidents",
        str(active_incidents),
        "-2",
        delta_color="inverse",
        border=True,
    )
    st.metric(
        "Deployment success",
        "96.5%",
        "+1.5%",
        delta_color="normal",
        border=True,
    )
    st.metric(
        "Average response time",
        "145 ms",
        "-12 ms",
        delta_color="inverse",
        border=True,
    )

st.header("Infrastructure health", icon=":material/dns:")
st.caption("Resource utilization across the monitored server fleet.")


def utilization_chart(metric: str, color: str):
    figure = px.bar(data, x="Server", y=metric)
    figure.update_traces(
        marker_color=color,
        texttemplate="%{y:.0f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>%{y:.0f}%<extra></extra>",
    )
    figure.update_layout(
        height=320,
        margin={"l": 12, "r": 12, "t": 16, "b": 8},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F4F7FB"},
        showlegend=False,
        bargap=0.48,
    )
    figure.update_xaxes(
        showgrid=False,
        title=None,
        linecolor="rgba(148,163,184,0.35)",
        tickfont={"color": "#CBD5E1"},
    )
    figure.update_yaxes(
        range=[0, 105],
        ticksuffix="%",
        title=None,
        showgrid=True,
        gridcolor="rgba(148,163,184,0.2)",
        zeroline=False,
        tickfont={"color": "#CBD5E1"},
    )
    return figure


cpu_peak = data["CPU Usage"].max()
memory_peak = data["Memory Usage"].max()
cpu_column, memory_column = st.columns(2, gap="large")

with cpu_column:
    with st.container(border=True):
        st.subheader("CPU utilization")
        st.caption(f"Fleet peak: {cpu_peak}%")
        st.plotly_chart(
            utilization_chart("CPU Usage", "#6366F1"),
            theme="streamlit",
            width="stretch",
            alt="CPU utilization by server, peaking at 82 percent",
        )

with memory_column:
    with st.container(border=True):
        st.subheader("Memory utilization")
        st.caption(f"Fleet peak: {memory_peak}%")
        st.plotly_chart(
            utilization_chart("Memory Usage", "#14B8A6"),
            theme="streamlit",
            width="stretch",
            alt="Memory utilization by server, peaking at 89 percent",
        )

st.header("Incident response", icon=":material/notification_important:")
st.caption(f"{active_incidents} active incidents · {len(incidents)} tracked")

severity_colors = {"Critical": "red", "High": "orange", "Medium": "blue"}
status_colors = {"Open": "red", "Investigating": "orange", "Resolved": "green"}
incident_columns = st.columns(len(incidents), gap="medium")

for column, incident in zip(incident_columns, incidents.to_dict("records")):
    with column:
        with st.container(border=True):
            st.markdown(f"**{incident['Incident ID']}**")
            st.markdown(f"### {incident['Service']}")
            st.badge(
                incident["Severity"],
                icon=":material/priority_high:",
                color=severity_colors[incident["Severity"]],
            )
            st.badge(
                incident["Status"],
                icon=":material/schedule:",
                color=status_colors[incident["Status"]],
            )

st.header("Service level objectives", icon=":material/track_changes:")
st.caption(f"{services_meeting_slo} of {len(slo)} services currently meet their SLO.")

slo_columns = st.columns(len(slo), gap="medium")
for column, service in zip(slo_columns, slo.to_dict("records")):
    availability = service["Actual Availability"]
    target = service["SLO Target"]
    meets_slo = availability >= target

    with column:
        with st.container(border=True):
            st.markdown(f"**{service['Service']}**")
            st.metric(
                "Availability",
                f"{availability:.2f}%",
                f"{availability - target:+.2f} pp vs target",
                delta_color="normal",
            )
            st.badge(
                "Meeting SLO" if meets_slo else "Below SLO",
                icon=(
                    ":material/check_circle:"
                    if meets_slo
                    else ":material/warning:"
                ),
                color="green" if meets_slo else "red",
            )

st.caption("Demo environment · Metrics and incidents are sample data.")
