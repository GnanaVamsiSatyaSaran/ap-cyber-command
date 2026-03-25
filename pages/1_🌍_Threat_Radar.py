import streamlit as st
import plotly.express as px
from core_systems import inject_enterprise_css, run_query, render_live_ticker

st.set_page_config(page_title="Threat Radar", layout="wide")
inject_enterprise_css()
render_live_ticker()

if not st.session_state.get('authenticated', False): st.stop()

st.markdown("<h2 style='color:#00E5FF;'>🌍 STATEWIDE CRIME HOTSPOTS</h2>", unsafe_allow_html=True)
st.markdown("""
<div style='background: rgba(15,23,42,0.6); padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 20px; border: 1px solid rgba(16,185,129,0.3);'>
    <p style='color:#E2E8F0; margin:0;'><strong>How to read this map:</strong> The <b>size</b> of the circle shows the financial money lost. The <b>color</b> indicates danger: <span style='color:#10B981;'>Green (Low)</span> ➔ <span style='color:#F59E0B;'>Yellow</span> ➔ <span style='color:#EF4444;'>Red (High Danger)</span>.</p>
</div>
""", unsafe_allow_html=True)

df = run_query("SELECT Jurisdiction, Lat, Lon, SUM(Financial_Loss_Lakhs) as Total_Loss FROM intel_records GROUP BY Jurisdiction")

if not df.empty:
    fig = px.scatter_mapbox(
        df, lat="Lat", lon="Lon", size="Total_Loss", color="Total_Loss",       
        hover_name="Jurisdiction", hover_data={"Lat": False, "Lon": False, "Total_Loss": True}, 
        color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"], size_max=45, zoom=5.8,                 
        center=dict(lat=16.5, lon=80.6), mapbox_style="carto-darkmatter"
    )
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        height=650, 
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available to display on the map.")
