import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from data.governorates import GOVS, WEIGHTS, M_SHORT, M_FULL, M_ICONS, STATUS_LABEL, calc_wlc, build_df
from styles import DARK_CSS, HEADER_HTML, PLOTLY_LAYOUT, COLOR_SELECTED, COLOR_BOUNDARY, COLOR_OTHER, COLOR_ACTIVE, COLOR_GRID

st.set_page_config(
    page_title="Smart Irrigation MCDA — Egypt",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(DARK_CSS, unsafe_allow_html=True)
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# ── KPI Cards ────────────────────────────────────────────────────────────────
df_all = build_df()
top5   = [g for g in GOVS if g["status"] == "selected"]
avg_score  = round(df_all["WLC Score"].mean(), 3)
max_score  = df_all["WLC Score"].max()
min_score  = df_all["WLC Score"].min()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📍 Governorates Analysed", "27")
k2.metric("✓ Selected Sites",         "5")
k3.metric("◎ Boundary Case",          "1")
k4.metric("📊 Average WLC Score",     avg_score)
k5.metric("🏆 Highest Score",         max_score)

st.markdown("---")

tab1, tab2, tab3, tab4, tab5_t = st.tabs([
    "📊  WLC Results",
    "🧮  Interactive Calculator",
    "🔬  Sensitivity Analysis",
    "✏️  Edit Scores",
    "📥  Download Data",
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — WLC Results
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🏆 Top 5 Selected Governorates")
    cols = st.columns(5)
    for i, g in enumerate(top5):
        with cols[i]:
            st.metric(label=g["name"], value=calc_wlc(g["m"]))
            st.caption(g["system"])

    st.markdown("""
    <div style="background:rgba(30,58,95,0.3);border:1px solid rgba(100,180,255,0.15);
        border-radius:14px;padding:14px 20px;margin:16px 0;">
        <p style="color:rgba(180,210,255,0.5);font-size:11px;font-weight:600;
            text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">WLC Formula</p>
        <p style="color:rgba(255,255,255,0.9);font-family:'Space Grotesk',sans-serif;font-size:14px;margin:0;">
            S = (0.22×M₁) + (0.18×M₂) + (0.15×M₃) + (0.17×M₄) + (0.18×M₅) + (0.10×M₆)
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Full Ranking — All 27 Governorates")
    display = df_all[["Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","Status","Farming System","Water Source"]].copy()
    def hl(val):
        if "Selected" in str(val): return "background-color:#1a2e0a;color:#90eeb4;font-weight:600"
        if "Boundary" in str(val): return "background-color:#2a1a0a;color:#ffab70"
        return ""
    st.dataframe(display.style.map(hl, subset=["Status"]), use_container_width=True, height=600)

    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("### 📊 Visual Ranking — Top 15")
        fig = px.bar(df_all.head(15), x="WLC Score", y="Governorate", orientation="h",
                     color="Status",
                     color_discrete_map={"✓ Selected": COLOR_SELECTED, "◎ Boundary Case": COLOR_BOUNDARY, "Other": COLOR_OTHER},
                     text="WLC Score", template="plotly_dark")
        fig.update_layout(**PLOTLY_LAYOUT, yaxis={"categoryorder":"total ascending"}, height=480)
        fig.update_traces(textposition="outside", textfont_size=10)
        fig.update_xaxes(gridcolor=COLOR_GRID)
        fig.update_yaxes(gridcolor=COLOR_GRID)
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.markdown("### 🕸️ Criteria Radar — Top 5")
        fig_r = go.Figure()
        cats   = [s.split(" — ")[0] for s in M_FULL] + [M_FULL[0].split(" — ")[0]]
        clrs   = ["#64b4ff","#c8a96e","#4caf90","#ff7043","#ab6cf5"]
        for i, g in enumerate(top5):
            vals = g["m"] + [g["m"][0]]
            fig_r.add_trace(go.Scatterpolar(
                r=vals, theta=cats, fill="toself", name=g["name"],
                line_color=clrs[i],
                fillcolor=f"rgba({int(clrs[i][1:3],16)},{int(clrs[i][3:5],16)},{int(clrs[i][5:],16)},0.1)"
            ))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,5], gridcolor="rgba(255,255,255,0.1)"),
                bgcolor="rgba(15,32,53,0.5)",
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)")
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"family":"Inter","color":"rgba(255,255,255,0.7)"},
            legend={"bgcolor":"rgba(0,0,0,0)"},
            height=480
        )
        st.plotly_chart(fig_r, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2 — Interactive Calculator
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🧮 Interactive Score Calculator")
    st.info("Adjust any governorate's scores using the sliders — the full ranking updates instantly.")

    if "custom_scores" not in st.session_state:
        st.session_state.custom_scores = {g["name"]: list(g["m"]) for g in GOVS}

    gov_names = [g["name"] for g in GOVS]
    col_sel, col_rst = st.columns([4, 1])
    with col_sel:
        selected = st.selectbox("Select a Governorate", gov_names, key="calc_gov")
    with col_rst:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↺ Reset All"):
            st.session_state.custom_scores = {g["name"]: list(g["m"]) for g in GOVS}
            st.rerun()

    gov_obj   = next(g for g in GOVS if g["name"] == selected)
    current_m = st.session_state.custom_scores[selected]

    st.markdown(f"""
    <div style="background:rgba(30,58,95,0.3);border:1px solid rgba(100,180,255,0.12);
        border-radius:12px;padding:12px 18px;margin:8px 0 16px;">
        <span style="color:rgba(180,210,255,0.5);font-size:11px;font-weight:600;
            text-transform:uppercase;">Farming System</span><br>
        <span style="color:white;font-size:14px;">{gov_obj['system']}</span>
        &nbsp;
        <span style="background:rgba(100,180,255,0.1);border:1px solid rgba(100,180,255,0.2);
            color:#64b4ff;padding:2px 10px;border-radius:10px;font-size:11px;">
            {gov_obj['water']}
        </span>
    </div>
    """, unsafe_allow_html=True)

    new_m = []
    sc1, sc2, sc3 = st.columns(3)
    slider_cols = [sc1, sc2, sc3, sc1, sc2, sc3]
    for i, (name, icon) in enumerate(zip(M_FULL, M_ICONS)):
        with slider_cols[i]:
            v = st.slider(f"{icon} {name}", 1.0, 5.0, float(current_m[i]), 0.5, key=f"calc_{i}")
            new_m.append(v)
    st.session_state.custom_scores[selected] = new_m

    df_custom = build_df(custom=st.session_state.custom_scores)
    df_base   = build_df()

    new_score  = calc_wlc(new_m)
    orig_score = calc_wlc(gov_obj["m"])
    new_rank   = int(df_custom[df_custom["Governorate"] == selected].index[0])
    orig_rank  = int(df_base[df_base["Governorate"] == selected].index[0])
    rank_delta = orig_rank - new_rank
    score_delta= round(new_score - orig_score, 3)
    pct_above  = round((27 - new_rank) / 27 * 100)

    st.markdown("---")
    st.markdown("### 📍 Result")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("New WLC Score",   new_score,   delta=score_delta)
    m2.metric("Original Score",  orig_score)
    m3.metric("New Rank",        f"#{new_rank}",  delta=f"{rank_delta:+d} positions" if rank_delta else "Unchanged")
    m4.metric("Beats",           f"{pct_above}%", delta="of all governorates")

    st.markdown("---")
    st.markdown("### 🔼🔽 Neighbours in Ranking")
    above = df_custom[df_custom.index == new_rank - 1] if new_rank > 1  else None
    below = df_custom[df_custom.index == new_rank + 1] if new_rank < 27 else None

    nb1, nb2, nb3 = st.columns(3)
    card_style = "background:rgba(30,58,95,0.4);border:1px solid rgba(100,180,255,0.15);border-radius:14px;padding:18px;text-align:center;"
    status_col = COLOR_SELECTED if gov_obj["status"]=="selected" else COLOR_BOUNDARY if gov_obj["status"]=="boundary" else "#64b4ff"

    with nb1:
        if above is not None and not above.empty:
            ab   = above.iloc[0]
            diff = round(ab["WLC Score"] - new_score, 3)
            st.markdown(f'<div style="{card_style}"><b>🔼 One Rank Above</b><h3 style="color:white">{ab["Governorate"]}</h3><p>Score: <b>{ab["WLC Score"]}</b></p><p style="color:#ef9a9a">Gap above: +{diff}</p><small style="color:rgba(255,255,255,0.4)">{ab["Farming System"]}</small></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="{card_style}"><h3>🥇 #1 Ranked!</h3></div>', unsafe_allow_html=True)

    with nb2:
        st.markdown(f"""<div style="background:rgba(30,58,95,0.6);border:2px solid {status_col};
            border-radius:14px;padding:18px;text-align:center;">
            <p style="color:{status_col};font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Selected</p>
            <h3 style="color:white;margin:4px 0">{selected}</h3>
            <p style="font-size:28px;font-weight:700;color:{status_col};margin:4px 0">{new_score}</p>
            <p style="color:rgba(255,255,255,0.5);font-size:13px">Rank #{new_rank} of 27</p>
            <p style="color:rgba(255,255,255,0.35);font-size:12px">Top {100-pct_above}% of governorates</p>
        </div>""", unsafe_allow_html=True)

    with nb3:
        if below is not None and not below.empty:
            bl   = below.iloc[0]
            diff = round(new_score - bl["WLC Score"], 3)
            st.markdown(f'<div style="{card_style}"><b>🔽 One Rank Below</b><h3 style="color:white">{bl["Governorate"]}</h3><p>Score: <b>{bl["WLC Score"]}</b></p><p style="color:#a5d6a7">Your lead: +{diff}</p><small style="color:rgba(255,255,255,0.4)">{bl["Farming System"]}</small></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="{card_style}"><h3>Last position</h3></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Full Ranking Visualization")
    colors_bar = []
    for _, row in df_custom.iterrows():
        if row["Governorate"] == selected:        colors_bar.append(COLOR_ACTIVE)
        elif "Selected" in row["Status"]:         colors_bar.append(COLOR_SELECTED)
        elif "Boundary" in row["Status"]:         colors_bar.append(COLOR_BOUNDARY)
        else:                                     colors_bar.append(COLOR_OTHER)

    fig3 = go.Figure(go.Bar(
        x=df_custom["WLC Score"], y=df_custom["Governorate"],
        orientation="h", marker_color=colors_bar,
        text=df_custom["WLC Score"], textposition="outside", textfont={"size":10}
    ))
    fig3.update_layout(**PLOTLY_LAYOUT,
        yaxis={"categoryorder":"total ascending"},
        height=820,
        title={"text":f"Full Ranking — {selected} in blue","font":{"size":13}}
    )
    fig3.update_xaxes(gridcolor=COLOR_GRID, range=[0, 5.3])
    fig3.update_yaxes(gridcolor=COLOR_GRID)
    st.plotly_chart(fig3, use_container_width=True)

    changed = [g["name"] for g in GOVS if abs(calc_wlc(st.session_state.custom_scores[g["name"]]) - calc_wlc(g["m"])) > 0.001]
    if changed:
        st.info(f"✏️ Modified: {' · '.join(changed)}")
    st.dataframe(df_custom[["Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","Status","Farming System"]], use_container_width=True, height=620)

# ═══════════════════════════════════════════════════════════════
# TAB 3 — Sensitivity Analysis
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔬 Sensitivity Analysis — OAT Weight Perturbation")
    st.info("Adjust criterion weights to test model stability. Weights must sum to exactly **1.00**.")

    sa1, sa2, sa3 = st.columns(3)
    wcols = [sa1, sa2, sa3, sa1, sa2, sa3]
    new_w = []
    for i, (name, icon) in enumerate(zip(M_SHORT, M_ICONS)):
        with wcols[i]:
            w = st.slider(f"{icon} {name}", 0.01, 0.50, WEIGHTS[i], 0.01, key=f"sw{i}")
            new_w.append(w)

    total_w = round(sum(new_w), 3)
    if abs(total_w - 1.0) > 0.005:
        st.error(f"⚠️ Weights sum = {total_w} — must equal 1.00")
    else:
        st.success(f"✓ Weights sum = {total_w}")
        df_sens   = build_df(weights=new_w)
        df_base2  = build_df()
        merged    = df_sens[["Governorate","WLC Score","Status"]].copy()
        merged.columns = ["Governorate","New Score","Status"]
        merged["Original Score"] = merged["Governorate"].map(df_base2.set_index("Governorate")["WLC Score"])
        merged["Δ Change"]       = (merged["New Score"] - merged["Original Score"]).round(3)
        merged = merged.sort_values("New Score", ascending=False).reset_index(drop=True)
        merged.index += 1
        st.dataframe(merged[["Governorate","Original Score","New Score","Δ Change","Status"]], use_container_width=True, height=500)

        fig4 = go.Figure()
        t10  = merged.head(10)
        fig4.add_trace(go.Bar(name="Original", x=t10["Governorate"], y=t10["Original Score"], marker_color=COLOR_OTHER))
        fig4.add_trace(go.Bar(name="New",      x=t10["Governorate"], y=t10["New Score"],      marker_color=COLOR_SELECTED))
        fig4.update_layout(**PLOTLY_LAYOUT, barmode="group", height=360, title={"text":"Original vs New — Top 10","font":{"size":13}})
        fig4.update_xaxes(gridcolor=COLOR_GRID)
        fig4.update_yaxes(gridcolor=COLOR_GRID)
        st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4 — Edit Scores
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### ✏️ Edit Individual Governorate Scores")
    gov_names2 = [g["name"] for g in GOVS]
    sel2 = st.selectbox("Select Governorate", gov_names2, key="edit_gov2")
    g2   = next(g for g in GOVS if g["name"] == sel2)
    st.markdown(f"**System:** {g2['system']} &nbsp;|&nbsp; **Water:** {g2['water']}")
    st.markdown("---")
    sc2  = []
    e1, e2, e3 = st.columns(3)
    ecols = [e1, e2, e3, e1, e2, e3]
    for i, (name, icon) in enumerate(zip(M_FULL, M_ICONS)):
        with ecols[i]:
            v = st.slider(f"{icon} {name}", 1.0, 5.0, float(g2["m"][i]), 0.5, key=f"ed_{i}")
            sc2.append(v)
    nw2 = calc_wlc(sc2); ow2 = calc_wlc(g2["m"]); d2 = round(nw2-ow2,3)
    x1, x2, x3 = st.columns(3)
    x1.metric("Original WLC Score", ow2)
    x2.metric("New WLC Score",       nw2, delta=d2)
    x3.metric("Change",              f"{'+' if d2>=0 else ''}{d2}")

# ═══════════════════════════════════════════════════════════════
# TAB 5 — Download
# ═══════════════════════════════════════════════════════════════
with tab5_t:
    st.markdown("### 📥 Download Results & Reference Data")
    df_dl = build_df()
    st.dataframe(df_dl[["Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","Status","Farming System","Water Source"]], use_container_width=True)
    csv = df_dl.to_csv(index=True, encoding="utf-8-sig")
    st.download_button("⬇️ Download Full Results CSV", csv, "egypt_irrigation_mcda.csv", "text/csv")

    st.markdown("---")
    st.markdown("### 📐 Weights Reference")
    wdf = pd.DataFrame({"Criterion": M_FULL, "Code":["M₁","M₂","M₃","M₄","M₅","M₆"],
                        "Weight": WEIGHTS, "Percentage": [f"{w*100:.0f}%" for w in WEIGHTS]})
    st.dataframe(wdf, use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align:center;padding:10px;">
    <span style="color:rgba(255,255,255,0.2);font-size:11px;">
        Smart Irrigation MCDA Tool — Egypt &nbsp;·&nbsp;
        Stage 1 WLC Model &nbsp;·&nbsp;
        MALR 2017 · WMRI 2018 &nbsp;·&nbsp;
        Built with Streamlit 🌊
    </span>
</div>
""", unsafe_allow_html=True)
