import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
 
st.set_page_config(
    page_title="Smart Irrigation MCDA — Egypt",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
# ── DATA ─────────────────────────────────────────────────────────────────────
GOVS = [
    {"rank":1,  "name":"El Beheira",       "m":[4.5,4.5,4.0,4.5,5.0,4.0], "system":"New Land Corporate Reclamation",        "status":"selected",  "water":"Mixed/Canal"},
    {"rank":2,  "name":"El Qalyoubeya",    "m":[3.5,5.0,2.0,5.0,5.0,5.0], "system":"Old Delta Fragmented Smallholder",      "status":"selected",  "water":"Surface Canal"},
    {"rank":3,  "name":"Alexandria",       "m":[4.5,3.5,3.5,4.0,5.0,3.0], "system":"Mediterranean Coastal New Land",        "status":"selected",  "water":"Mixed/Canal"},
    {"rank":4,  "name":"El Dakahlia",      "m":[4.5,3.0,2.5,4.5,4.0,4.5], "system":"Mid-Delta Tail-End Salinity Zone",      "status":"selected",  "water":"Mixed/Canal"},
    {"rank":5,  "name":"Sohag",            "m":[3.5,2.5,4.5,3.5,4.5,4.5], "system":"Upper Egypt Narrow Valley (High-ET)",   "status":"selected",  "water":"Surface Nile"},
    {"rank":6,  "name":"El Wadi El Gedid", "m":[3.0,4.0,5.0,2.5,4.0,1.0], "system":"Hyper-Arid Fossil Aquifer Reclamation", "status":"boundary",  "water":"Groundwater"},
    {"rank":7,  "name":"Matrouh",          "m":[3.5,3.5,4.5,2.5,2.5,1.5], "system":"NW Coastal Desert / Bedouin Rainfed",   "status":"other",     "water":"Rainfed"},
    {"rank":8,  "name":"El Sharqia",       "m":[3.0,2.5,2.5,4.0,2.0,4.5], "system":"Eastern Delta Smallholder",             "status":"other",     "water":"Mixed/Canal"},
    {"rank":9,  "name":"South Sinai",      "m":[3.0,3.5,5.0,2.0,2.5,1.0], "system":"Sinai Mountain / Coastal",              "status":"other",     "water":"Groundwater"},
    {"rank":10, "name":"North Sinai",      "m":[3.5,3.0,4.0,2.5,2.0,2.0], "system":"Sinai Canal Zone",                      "status":"other",     "water":"Mixed/Canal"},
    {"rank":11, "name":"El Minia",         "m":[2.5,1.5,4.0,3.5,2.5,4.0], "system":"Middle Upper Egypt",                    "status":"other",     "water":"Surface Nile"},
    {"rank":12, "name":"El Fayoum",        "m":[3.0,1.5,3.0,3.5,2.5,3.5], "system":"Fayoum Depression",                     "status":"other",     "water":"Surface Canal"},
    {"rank":12, "name":"Asyut",            "m":[2.5,1.5,4.0,3.5,2.0,4.0], "system":"Central Upper Egypt",                   "status":"other",     "water":"Surface Nile"},
    {"rank":14, "name":"Kafr El Sheikh",   "m":[3.0,2.0,2.5,3.5,2.0,4.0], "system":"Northern Coastal Delta",                "status":"other",     "water":"Mixed/Canal"},
    {"rank":15, "name":"Qena",             "m":[2.5,1.5,4.5,3.0,2.0,3.5], "system":"Upper Egypt — Luxor Region",            "status":"other",     "water":"Surface Nile"},
    {"rank":16, "name":"Aswan",            "m":[2.5,2.0,5.0,3.0,1.5,2.0], "system":"Extreme Upper Egypt",                   "status":"other",     "water":"Surface Nile"},
    {"rank":17, "name":"El Gharbia",       "m":[2.5,2.0,2.0,4.0,1.5,4.5], "system":"Core Delta Smallholder",                "status":"other",     "water":"Surface Canal"},
    {"rank":18, "name":"Ismailia",         "m":[2.5,2.5,3.0,3.5,2.0,2.0], "system":"Canal Zone Reclamation",                "status":"other",     "water":"Mixed/Canal"},
    {"rank":19, "name":"Beni Suef",        "m":[2.5,1.5,3.5,3.0,2.0,3.5], "system":"Upper Egypt Transition Zone",           "status":"other",     "water":"Surface Nile"},
    {"rank":20, "name":"El Menoufia",      "m":[2.5,1.5,2.0,4.0,1.5,4.5], "system":"Central Delta",                         "status":"other",     "water":"Surface Canal"},
    {"rank":21, "name":"Luxor",            "m":[2.0,1.5,4.5,3.0,1.5,2.5], "system":"Tourism / Upper Egypt",                 "status":"other",     "water":"Surface Nile"},
    {"rank":22, "name":"Giza",             "m":[2.0,1.5,2.5,4.0,1.5,3.5], "system":"Peri-Urban / Old Land",                 "status":"other",     "water":"Surface Canal"},
    {"rank":23, "name":"Red Sea",          "m":[2.0,3.0,4.5,2.0,1.5,1.0], "system":"Sparse Coastal Desert",                 "status":"other",     "water":"Groundwater"},
    {"rank":24, "name":"Damietta",         "m":[2.5,2.0,2.0,3.0,1.5,3.0], "system":"Northern Delta Coastal",                "status":"other",     "water":"Mixed/Canal"},
    {"rank":25, "name":"Suez",             "m":[1.5,2.0,3.5,2.5,1.0,1.5], "system":"Industrial / Coastal",                  "status":"other",     "water":"Mixed"},
    {"rank":26, "name":"Cairo",            "m":[1.5,1.0,2.0,4.0,1.0,2.0], "system":"Urban Peri-Agriculture",                "status":"other",     "water":"Surface Canal"},
    {"rank":27, "name":"Port Said",        "m":[1.5,1.5,2.0,2.5,1.0,1.5], "system":"Canal Zone Urban",                      "status":"other",     "water":"Mixed"},
]
WEIGHTS = [0.22, 0.18, 0.15, 0.17, 0.18, 0.10]
M_SHORT = ["M₁ Hydrology","M₂ Land Tenure","M₃ Climate","M₄ Institutional","M₅ Representativeness","M₆ Farm Density"]
M_FULL  = ["M₁ — Hydrological Source Diversity","M₂ — Land Tenure & Farm Structure","M₃ — Climatic & Arid Stress","M₄ — Logistical & Institutional Readiness","M₅ — Agricultural System Representativeness","M₆ — Farmer Population Density & Generalizability"]
M_ICONS = ["💧","🏡","☀️","🏛️","🌾","👥"]
STATUS_LABEL = {"selected":"✓ Selected","boundary":"◎ Boundary Case","other":"Other"}
COLOR_SELECTED="#c8a96e"; COLOR_BOUNDARY="#ff7043"; COLOR_OTHER="#37474f"; COLOR_ACTIVE="#2196F3"; COLOR_GRID="rgba(255,255,255,0.05)"
 
def calc_wlc(m, w=None):
    w = w or WEIGHTS
    return round(sum(wi*mi for wi,mi in zip(w,m)), 3)
 
def build_df(custom=None, weights=None):
    w = weights or WEIGHTS
    rows = []
    for g in GOVS:
        m = custom.get(g["name"], g["m"]) if custom else g["m"]
        rows.append({"Governorate":g["name"],"M₁":m[0],"M₂":m[1],"M₃":m[2],"M₄":m[3],"M₅":m[4],"M₆":m[5],
                     "WLC Score":calc_wlc(m,w),"Farming System":g["system"],"Water Source":g["water"],
                     "Status":STATUS_LABEL[g["status"]],"_status":g["status"]})
    df = pd.DataFrame(rows).sort_values("WLC Score",ascending=False).reset_index(drop=True)
    df.index += 1
    return df
 
PLOTLY_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(15,32,53,0.5)",
    font={"family":"Inter","color":"rgba(255,255,255,0.7)"},legend={"bgcolor":"rgba(0,0,0,0)"},margin={"r":80,"t":40})
 
# ── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:linear-gradient(135deg,#0a0f1e 0%,#0d1b2a 40%,#0a1628 100%);}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:rgba(255,255,255,0.04);border-radius:14px;padding:6px;border:1px solid rgba(255,255,255,0.08);}
.stTabs [data-baseweb="tab"]{border-radius:10px;color:rgba(255,255,255,0.5);font-family:'Inter',sans-serif;font-weight:500;font-size:13px;padding:8px 18px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#1e3a5f,#2d6a9f)!important;color:white!important;box-shadow:0 4px 15px rgba(45,106,159,0.4);}
[data-testid="metric-container"]{background:linear-gradient(135deg,rgba(30,58,95,0.6),rgba(13,27,42,0.8));border:1px solid rgba(100,180,255,0.15);border-radius:16px;padding:20px;transition:transform 0.2s;}
[data-testid="metric-container"]:hover{transform:translateY(-2px);border-color:rgba(100,180,255,0.3);}
[data-testid="stMetricLabel"]{color:rgba(180,210,255,0.7)!important;font-size:12px!important;font-weight:500!important;text-transform:uppercase;letter-spacing:0.5px;}
[data-testid="stMetricValue"]{color:#64b4ff!important;font-family:'Space Grotesk',sans-serif!important;font-weight:700!important;font-size:28px!important;}
.stButton>button{background:linear-gradient(135deg,#1e3a5f,#2d6a9f);color:white;border:1px solid rgba(100,180,255,0.3);border-radius:10px;font-family:'Inter',sans-serif;font-weight:500;transition:all 0.2s;}
.stButton>button:hover{background:linear-gradient(135deg,#2d6a9f,#3d8fd4);transform:translateY(-1px);box-shadow:0 6px 20px rgba(45,106,159,0.4);}
.stDownloadButton>button{background:linear-gradient(135deg,#1a4a2e,#2d7a4a)!important;border-color:rgba(100,220,150,0.3)!important;color:#90eeb4!important;}
.stInfo{background:rgba(30,58,95,0.4)!important;border:1px solid rgba(100,180,255,0.2)!important;border-radius:12px!important;}
.stSuccess{background:rgba(20,60,35,0.4)!important;border:1px solid rgba(100,220,150,0.2)!important;border-radius:12px!important;}
.stError{background:rgba(80,20,20,0.4)!important;border:1px solid rgba(255,100,100,0.2)!important;border-radius:12px!important;}
hr{border-color:rgba(255,255,255,0.07)!important;}
.stCaption{color:rgba(255,255,255,0.35)!important;font-size:11px!important;}
[data-testid="stDataFrame"]{border:1px solid rgba(100,180,255,0.1);border-radius:12px;overflow:hidden;}
</style>""", unsafe_allow_html=True)
 
# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,rgba(30,58,95,0.8) 0%,rgba(13,27,42,0.9) 100%);
    border:1px solid rgba(100,180,255,0.15);border-radius:20px;padding:28px 32px;margin-bottom:20px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
        background:radial-gradient(circle,rgba(45,106,159,0.15),transparent);border-radius:50%;"></div>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
        <div style="background:linear-gradient(135deg,#1e3a5f,#2d6a9f);width:52px;height:52px;border-radius:14px;
            display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 8px 24px rgba(45,106,159,0.4);">🌊</div>
        <div>
            <h1 style="margin:0;font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:700;color:white;letter-spacing:-0.5px;">
                Smart Irrigation MCDA — Egypt</h1>
            <p style="margin:4px 0 0;color:rgba(180,210,255,0.5);font-size:12px;">
                WLC Model · 27 Governorates · Six-Criterion Framework · Stage 1</p>
        </div>
        <div style="margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;">
            <span style="background:rgba(100,180,255,0.1);border:1px solid rgba(100,180,255,0.2);color:#64b4ff;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;">27 Governorates</span>
            <span style="background:rgba(200,169,110,0.1);border:1px solid rgba(200,169,110,0.2);color:#c8a96e;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;">5 Selected</span>
        </div>
    </div>
</div>""", unsafe_allow_html=True)
 
# ── KPIs ─────────────────────────────────────────────────────────────────────
df_all = build_df()
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("📍 Governorates", "27")
k2.metric("✓ Selected Sites", "5")
k3.metric("◎ Boundary Case", "1")
k4.metric("📊 Avg WLC Score", round(df_all["WLC Score"].mean(),3))
k5.metric("🏆 Highest Score", df_all["WLC Score"].max())
st.markdown("---")
 
tab1,tab2,tab3,tab4,tab5_t = st.tabs(["📊  WLC Results","🧮  Interactive Calculator","🔬  Sensitivity Analysis","✏️  Edit Scores","📥  Download Data"])
 
# ═══ TAB 1 ═══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🏆 Top 5 Selected Governorates")
    top5 = [g for g in GOVS if g["status"]=="selected"]
    cols = st.columns(5)
    for i,g in enumerate(top5):
        with cols[i]:
            st.metric(label=g["name"], value=calc_wlc(g["m"]))
            st.caption(g["system"])
 
    st.markdown("""<div style="background:rgba(30,58,95,0.3);border:1px solid rgba(100,180,255,0.15);
        border-radius:14px;padding:14px 20px;margin:16px 0;">
        <p style="color:rgba(180,210,255,0.5);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">WLC Formula</p>
        <p style="color:rgba(255,255,255,0.9);font-family:'Space Grotesk',sans-serif;font-size:14px;margin:0;">
        S = (0.22×M₁) + (0.18×M₂) + (0.15×M₃) + (0.17×M₄) + (0.18×M₅) + (0.10×M₆)</p></div>""", unsafe_allow_html=True)
 
    st.markdown("### 📋 Full Ranking — All 27 Governorates")
    disp = df_all[["Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","Status","Farming System","Water Source"]].copy()
    def hl(val):
        if "Selected" in str(val): return "background-color:#1a2e0a;color:#90eeb4;font-weight:600"
        if "Boundary" in str(val): return "background-color:#2a1a0a;color:#ffab70"
        return ""
    st.dataframe(disp.style.map(hl,subset=["Status"]), use_container_width=True, height=600)
 
    cl,cr = st.columns(2)
    with cl:
        st.markdown("### 📊 Visual Ranking — Top 15")
        fig = px.bar(df_all.head(15),x="WLC Score",y="Governorate",orientation="h",color="Status",
            color_discrete_map={"✓ Selected":COLOR_SELECTED,"◎ Boundary Case":COLOR_BOUNDARY,"Other":COLOR_OTHER},
            text="WLC Score",template="plotly_dark")
        fig.update_layout(**PLOTLY_LAYOUT,yaxis={"categoryorder":"total ascending"},height=480)
        fig.update_traces(textposition="outside",textfont_size=10)
        fig.update_xaxes(gridcolor=COLOR_GRID); fig.update_yaxes(gridcolor=COLOR_GRID)
        st.plotly_chart(fig,use_container_width=True)
    with cr:
        st.markdown("### 🕸️ Criteria Radar — Top 5")
        fig_r = go.Figure()
        cats  = [s.split(" — ")[0] for s in M_FULL]+[M_FULL[0].split(" — ")[0]]
        clrs  = ["#64b4ff","#c8a96e","#4caf90","#ff7043","#ab6cf5"]
        for i,g in enumerate(top5):
            vals = g["m"]+[g["m"][0]]
            r,gg,b = int(clrs[i][1:3],16),int(clrs[i][3:5],16),int(clrs[i][5:],16)
            fig_r.add_trace(go.Scatterpolar(r=vals,theta=cats,fill="toself",name=g["name"],
                line_color=clrs[i],fillcolor=f"rgba({r},{gg},{b},0.1)"))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],gridcolor="rgba(255,255,255,0.1)"),
            bgcolor="rgba(15,32,53,0.5)",angularaxis=dict(gridcolor="rgba(255,255,255,0.08)")),
            paper_bgcolor="rgba(0,0,0,0)",font={"family":"Inter","color":"rgba(255,255,255,0.7)"},
            legend={"bgcolor":"rgba(0,0,0,0)"},height=480)
        st.plotly_chart(fig_r,use_container_width=True)
 
# ═══ TAB 2 ═══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🧮 Interactive Score Calculator")
    st.info("Adjust any governorate's scores — the full ranking updates instantly.")
    if "custom_scores" not in st.session_state:
        st.session_state.custom_scores = {g["name"]:list(g["m"]) for g in GOVS}
    gov_names = [g["name"] for g in GOVS]
    csel,crst = st.columns([4,1])
    with csel: selected = st.selectbox("Select a Governorate",gov_names,key="calc_gov")
    with crst:
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("↺ Reset All"):
            st.session_state.custom_scores={g["name"]:list(g["m"]) for g in GOVS}; st.rerun()
    gov_obj   = next(g for g in GOVS if g["name"]==selected)
    current_m = st.session_state.custom_scores[selected]
    st.markdown(f"""<div style="background:rgba(30,58,95,0.3);border:1px solid rgba(100,180,255,0.12);
        border-radius:12px;padding:12px 18px;margin:8px 0 16px;">
        <span style="color:rgba(180,210,255,0.5);font-size:11px;font-weight:600;text-transform:uppercase;">Farming System</span><br>
        <span style="color:white;font-size:14px;">{gov_obj['system']}</span> &nbsp;
        <span style="background:rgba(100,180,255,0.1);border:1px solid rgba(100,180,255,0.2);color:#64b4ff;padding:2px 10px;border-radius:10px;font-size:11px;">{gov_obj['water']}</span>
        </div>""", unsafe_allow_html=True)
    new_m=[]; sc1,sc2,sc3=st.columns(3); scols=[sc1,sc2,sc3,sc1,sc2,sc3]
    for i,(name,icon) in enumerate(zip(M_FULL,M_ICONS)):
        with scols[i]:
            v=st.slider(f"{icon} {name}",1.0,5.0,float(current_m[i]),0.5,key=f"calc_{i}"); new_m.append(v)
    st.session_state.custom_scores[selected]=new_m
    df_custom=build_df(custom=st.session_state.custom_scores); df_base=build_df()
    new_score=calc_wlc(new_m); orig_score=calc_wlc(gov_obj["m"])
    new_rank=int(df_custom[df_custom["Governorate"]==selected].index[0])
    orig_rank=int(df_base[df_base["Governorate"]==selected].index[0])
    rank_delta=orig_rank-new_rank; score_delta=round(new_score-orig_score,3)
    pct_above=round((27-new_rank)/27*100)
    st.markdown("---"); st.markdown("### 📍 Result")
    m1,m2,m3,m4=st.columns(4)
    m1.metric("New WLC Score",new_score,delta=score_delta)
    m2.metric("Original Score",orig_score)
    m3.metric("New Rank",f"#{new_rank}",delta=f"{rank_delta:+d} positions" if rank_delta else "Unchanged")
    m4.metric("Beats",f"{pct_above}%",delta="of all governorates")
    st.markdown("---"); st.markdown("### 🔼🔽 Neighbours in Ranking")
    above=df_custom[df_custom.index==new_rank-1] if new_rank>1 else None
    below=df_custom[df_custom.index==new_rank+1] if new_rank<27 else None
    cs="background:rgba(30,58,95,0.4);border:1px solid rgba(100,180,255,0.15);border-radius:14px;padding:18px;text-align:center;"
    sc=COLOR_SELECTED if gov_obj["status"]=="selected" else COLOR_BOUNDARY if gov_obj["status"]=="boundary" else "#64b4ff"
    nb1,nb2,nb3=st.columns(3)
    with nb1:
        if above is not None and not above.empty:
            ab=above.iloc[0]; diff=round(ab["WLC Score"]-new_score,3)
            st.markdown(f'<div style="{cs}"><b>🔼 One Rank Above</b><h3 style="color:white">{ab["Governorate"]}</h3><p>Score: <b>{ab["WLC Score"]}</b></p><p style="color:#ef9a9a">Gap: +{diff}</p><small style="color:rgba(255,255,255,0.4)">{ab["Farming System"]}</small></div>',unsafe_allow_html=True)
        else: st.markdown(f'<div style="{cs}"><h3>🥇 #1 Ranked!</h3></div>',unsafe_allow_html=True)
    with nb2:
        st.markdown(f"""<div style="background:rgba(30,58,95,0.6);border:2px solid {sc};border-radius:14px;padding:18px;text-align:center;">
            <p style="color:{sc};font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Selected</p>
            <h3 style="color:white;margin:4px 0">{selected}</h3>
            <p style="font-size:28px;font-weight:700;color:{sc};margin:4px 0">{new_score}</p>
            <p style="color:rgba(255,255,255,0.5);font-size:13px">Rank #{new_rank} of 27</p>
            <p style="color:rgba(255,255,255,0.35);font-size:12px">Top {100-pct_above}% of governorates</p></div>""",unsafe_allow_html=True)
    with nb3:
        if below is not None and not below.empty:
            bl=below.iloc[0]; diff=round(new_score-bl["WLC Score"],3)
            st.markdown(f'<div style="{cs}"><b>🔽 One Rank Below</b><h3 style="color:white">{bl["Governorate"]}</h3><p>Score: <b>{bl["WLC Score"]}</b></p><p style="color:#a5d6a7">Lead: +{diff}</p><small style="color:rgba(255,255,255,0.4)">{bl["Farming System"]}</small></div>',unsafe_allow_html=True)
        else: st.markdown(f'<div style="{cs}"><h3>Last position</h3></div>',unsafe_allow_html=True)
    st.markdown("---"); st.markdown("### 📊 Full Ranking Visualization")
    colors_bar=[]
    for _,row in df_custom.iterrows():
        if row["Governorate"]==selected: colors_bar.append(COLOR_ACTIVE)
        elif "Selected" in row["Status"]: colors_bar.append(COLOR_SELECTED)
        elif "Boundary" in row["Status"]: colors_bar.append(COLOR_BOUNDARY)
        else: colors_bar.append(COLOR_OTHER)
    fig3=go.Figure(go.Bar(x=df_custom["WLC Score"],y=df_custom["Governorate"],orientation="h",
        marker_color=colors_bar,text=df_custom["WLC Score"],textposition="outside",textfont={"size":10}))
    fig3.update_layout(**PLOTLY_LAYOUT,yaxis={"categoryorder":"total ascending"},height=820,
        title={"text":f"Full Ranking — {selected} in blue","font":{"size":13}})
    fig3.update_xaxes(gridcolor=COLOR_GRID,range=[0,5.3]); fig3.update_yaxes(gridcolor=COLOR_GRID)
    st.plotly_chart(fig3,use_container_width=True)
    changed=[g["name"] for g in GOVS if abs(calc_wlc(st.session_state.custom_scores[g["name"]])-calc_wlc(g["m"]))>0.001]
    if changed: st.info(f"✏️ Modified: {' · '.join(changed)}")
    st.dataframe(df_custom[["Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","Status","Farming System"]],use_container_width=True,height=620)
 
# ═══ TAB 3 ═══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔬 Sensitivity Analysis — OAT Weight Perturbation")
    st.info("Adjust criterion weights to test model stability. Weights must sum to **1.00**.")
    sa1,sa2,sa3=st.columns(3); wcols=[sa1,sa2,sa3,sa1,sa2,sa3]; new_w=[]
    for i,(name,icon) in enumerate(zip(M_SHORT,M_ICONS)):
        with wcols[i]:
            w=st.slider(f"{icon} {name}",0.01,0.50,WEIGHTS[i],0.01,key=f"sw{i}"); new_w.append(w)
    total_w=round(sum(new_w),3)
    if abs(total_w-1.0)>0.005: st.error(f"⚠️ Weights sum = {total_w} — must equal 1.00")
    else:
        st.success(f"✓ Weights sum = {total_w}")
        df_sens=build_df(weights=new_w); df_base2=build_df()
        merged=df_sens[["Governorate","WLC Score","Status"]].copy()
        merged.columns=["Governorate","New Score","Status"]
        merged["Original Score"]=merged["Governorate"].map(df_base2.set_index("Governorate")["WLC Score"])
        merged["Δ Change"]=(merged["New Score"]-merged["Original Score"]).round(3)
        merged=merged.sort_values("New Score",ascending=False).reset_index(drop=True); merged.index+=1
        st.dataframe(merged[["Governorate","Original Score","New Score","Δ Change","Status"]],use_container_width=True,height=500)
        fig4=go.Figure()
        t10=merged.head(10)
        fig4.add_trace(go.Bar(name="Original",x=t10["Governorate"],y=t10["Original Score"],marker_color=COLOR_OTHER))
        fig4.add_trace(go.Bar(name="New",x=t10["Governorate"],y=t10["New Score"],marker_color=COLOR_SELECTED))
        fig4.update_layout(**PLOTLY_LAYOUT,barmode="group",height=360,title={"text":"Original vs New — Top 10","font":{"size":13}})
        fig4.update_xaxes(gridcolor=COLOR_GRID); fig4.update_yaxes(gridcolor=COLOR_GRID)
        st.plotly_chart(fig4,use_container_width=True)
 
# ═══ TAB 4 ═══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### ✏️ Edit Individual Governorate Scores")
    sel2=st.selectbox("Select Governorate",[g["name"] for g in GOVS],key="edit_gov2")
    g2=next(g for g in GOVS if g["name"]==sel2)
    st.markdown(f"**System:** {g2['system']} &nbsp;|&nbsp; **Water:** {g2['water']}")
    st.markdown("---")
    sc2=[]; e1,e2,e3=st.columns(3); ecols=[e1,e2,e3,e1,e2,e3]
    for i,(name,icon) in enumerate(zip(M_FULL,M_ICONS)):
        with ecols[i]:
            v=st.slider(f"{icon} {name}",1.0,5.0,float(g2["m"][i]),0.5,key=f"ed_{i}"); sc2.append(v)
    nw2=calc_wlc(sc2); ow2=calc_wlc(g2["m"]); d2=round(nw2-ow2,3)
    x1,x2,x3=st.columns(3)
    x1.metric("Original WLC Score",ow2); x2.metric("New WLC Score",nw2,delta=d2); x3.metric("Change",f"{'+' if d2>=0 else ''}{d2}")
 
# ═══ TAB 5 ═══════════════════════════════════════════════════════════════════
with tab5_t:
    st.markdown("### 📥 Download Results & Reference Data")
    df_dl=build_df()
    st.dataframe(df_dl[["Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","Status","Farming System","Water Source"]],use_container_width=True)
    csv=df_dl.to_csv(index=True,encoding="utf-8-sig")
    st.download_button("⬇️ Download Full Results CSV",csv,"egypt_irrigation_mcda.csv","text/csv")
    st.markdown("---"); st.markdown("### 📐 Weights Reference")
    wdf=pd.DataFrame({"Criterion":M_FULL,"Code":["M₁","M₂","M₃","M₄","M₅","M₆"],"Weight":WEIGHTS,"Percentage":[f"{w*100:.0f}%" for w in WEIGHTS]})
    st.dataframe(wdf,use_container_width=True,hide_index=True)
 
st.divider()
st.markdown("""<div style="text-align:center;padding:10px;">
    <span style="color:rgba(255,255,255,0.2);font-size:11px;">
    Smart Irrigation MCDA Tool — Egypt · Stage 1 WLC Model · MALR 2017 · WMRI 2018 · Built with Streamlit 🌊
    </span></div>""", unsafe_allow_html=True)
 