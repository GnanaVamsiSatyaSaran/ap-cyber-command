import streamlit as st
import plotly.graph_objects as go
from core_systems import inject_enterprise_css, run_query, render_live_ticker

st.set_page_config(page_title="Analytics Dashboard", layout="wide")
inject_enterprise_css()
render_live_ticker()
if not st.session_state.get('authenticated', False): st.stop()

st.markdown("<h2>📊 State Analytics Command</h2>", unsafe_allow_html=True)
df = run_query("SELECT * FROM intel_records")

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Incidents</div><div class="kpi-val">{df["Incident_Count"].sum():,}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Capital Drain</div><div class="kpi-val" style="color:#EF4444;">₹{df["Financial_Loss_Lakhs"].sum():,.1f}L</div></div>', unsafe_allow_html=True)
with c3: 
    avg = df["Financial_Loss_Lakhs"].sum()/df["Incident_Count"].sum() if df["Incident_Count"].sum() > 0 else 0
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Average Loss Per Case</div><div class="kpi-val">₹{avg:.2f}L</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    stats = df.groupby('Crime_Category').agg({'Incident_Count': 'sum'}).sort_values('Incident_Count')
    fig1 = go.Figure(go.Bar(x=stats['Incident_Count'], y=stats.index, orientation='h', marker=dict(color='#00E5FF')))
    fig1.update_layout(title="Attack Volume by Vector", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#94A3B8"), height=400)
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    stats2 = df.groupby('Jurisdiction').agg({'Financial_Loss_Lakhs': 'sum'}).sort_values('Financial_Loss_Lakhs').tail(8)
    fig2 = go.Figure(go.Bar(x=stats2['Financial_Loss_Lakhs'], y=stats2.index, orientation='h', marker=dict(color='#E11D48')))
    fig2.update_layout(title="Top Jurisdictions by Financial Impact", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#94A3B8"), height=400)
    st.plotly_chart(fig2, use_container_width=True)