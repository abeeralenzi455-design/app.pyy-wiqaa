# app.py
# WIQAA | وِقاء
# AI-Powered Residency Compliance Platform
# Hackathon Prototype — Enhanced Edition (MAEEN-grade visual system)
# Demo data only — not real records

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="وِقاء | WIQAA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# STYLE — light, RTL, official "Absher" government identity
# Saudi-green primary, gold/copper accent, white cards, formal tone
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

:root {
    --gov-green: #00573F;
    --gov-green-dark: #003D2C;
    --gov-green-light: #0C8054;
    --gov-gold: #B8912F;
    --gov-bg: #F4F6F5;
}

html, body, [class*="css"]  {
    font-family: 'Tajawal', 'Segoe UI', sans-serif;
    direction: rtl;
}

/* ---------- base canvas ---------- */
.stApp { background: var(--gov-bg); color: #1c2b24; }
.block-container { padding-top: 0rem; max-width: 1200px; }

/* ---------- top government bar (mimics Absher's header strip) ---------- */
.gov-topbar {
    background: linear-gradient(90deg, var(--gov-green-dark), var(--gov-green));
    margin: -1rem -1rem 0 -1rem;
    padding: 8px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #eaf3ee;
    font-size: 12.5px;
    font-weight: 600;
    border-bottom: 3px solid var(--gov-gold);
}
.gov-topbar span { opacity: .9; }

/* ---------- sidebar (control panel, right-anchored) ---------- */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-left: 1px solid #e3e8e5;
}
section[data-testid="stSidebar"] * { color: #17332a !important; }
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #4c6259 !important; font-weight: 600; font-size: 13.5px;
}
section[data-testid="stSidebar"] hr { border-color: #e3e8e5 !important; }

/* ---------- brand header (Absher-style official hero strip) ---------- */
.wiqaa-hero {
    background: linear-gradient(135deg, var(--gov-green-dark) 0%, var(--gov-green) 100%);
    border-radius: 0 0 22px 22px;
    padding: 30px 34px 26px 34px;
    margin: 0 -1rem 22px -1rem;
    position: relative;
    box-shadow: 0 8px 24px rgba(0,61,44,0.18);
}
.wiqaa-hero::after {
    content: "";
    position: absolute; bottom: 0; right: 0; left: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--gov-gold), #e4c766, var(--gov-gold));
}
.wiqaa-eyebrow {
    color: #cfe9db;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: .5px;
}
.wiqaa-title {
    font-size: 38px;
    font-weight: 800;
    margin: 2px 0 6px 0;
    color: #ffffff;
}
.wiqaa-subtitle {
    color: #d8ece2;
    font-size: 15.5px;
    margin-top: 0;
    max-width: 720px;
}

/* Streamlit buttons restyled as the official gold CTA */
.stButton > button {
    background: linear-gradient(135deg, var(--gov-gold), #a67c22) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 22px !important;
    box-shadow: 0 4px 14px rgba(184,145,47,0.35) !important;
}
.stButton > button:hover { filter: brightness(1.06); }
.stDownloadButton > button {
    background: var(--gov-green) !important; color: #fff !important;
    border: none !important; border-radius: 10px !important; font-weight: 700 !important;
}

/* ---------- pill badges (compliance cycle) ---------- */
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: #eaf3ee;
    color: var(--gov-green);
    font-size: 13px;
    font-weight: 700;
    margin: 3px;
    border: 1px solid #cfe3d8;
}
.badge-arrow { color: #9fb3a9; font-size: 13px; margin: 0 2px; }

/* ---------- cards ---------- */
.metric-card {
    padding: 18px 20px;
    border-radius: 16px;
    background: #ffffff;
    border: 1px solid #e3e8e5;
    box-shadow: 0 1px 3px rgba(16,40,30,0.05);
}
.alert-card {
    padding: 16px 18px; border-radius: 14px;
    background: #fff8e8; border: 1px solid #eddca4;
    color: #7a5b06; border-right: 4px solid var(--gov-gold);
}
.danger-card {
    padding: 16px 18px; border-radius: 14px;
    background: #fdeceb; border: 1px solid #f3c2bd;
    color: #8a2b22; border-right: 4px solid #c0392b;
}
.success-card {
    padding: 16px 18px; border-radius: 14px;
    background: #eaf6ef; border: 1px solid #bfe3cd;
    color: #14532d; border-right: 4px solid var(--gov-green-light);
}
.info-card {
    padding: 16px 18px; border-radius: 14px;
    background: #eaf1f8; border: 1px solid #c3d7ec;
    color: #1e3a5c; border-right: 4px solid #2e6da4;
}
.pin-card {
    background: #ffffff;
    border: 1px solid #e3e8e5;
    border-right: 4px solid var(--gov-green);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(16,40,30,0.05);
}
.pin-title { color: var(--gov-green-dark); font-weight: 800; font-size: 15px; }
.pin-sub { color: #3c5249; font-size: 14.5px; margin-top: 4px; }

/* ---------- metrics ---------- */
[data-testid="stMetricValue"] { font-weight: 800; color: #17332a !important; }
[data-testid="stMetricLabel"] { color: #5c7369 !important; }
[data-testid="stMetric"] {
    background: #ffffff; border: 1px solid #e3e8e5; border-radius: 14px;
    padding: 12px 14px; box-shadow: 0 1px 3px rgba(16,40,30,0.05);
}

/* ---------- force light chrome regardless of device dark mode ---------- */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stSelectbox label, .stTextInput label, .stMultiSelect label,
.stSlider label, .stRadio label, div[role="radiogroup"] label {
    color: #17332a !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
h1, h2, h3, h4, h5, h6 { color: #17332a !important; }
[data-baseweb="select"] * { color: #17332a !important; }
[data-baseweb="popover"] { color: #17332a !important; }
.stTextInput input, .stSelectbox input { color: #17332a !important; }
[data-testid="stDataFrame"] * { color: #17332a !important; }

/* ---------- tabs styled like Absher's official section nav ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; border-bottom: 2px solid #e3e8e5;
    flex-wrap: nowrap;
    overflow-x: auto;
    white-space: nowrap;
}
.stTabs [data-baseweb="tab"] { flex-shrink: 0; }
.stTabs [data-baseweb="tab"] {
    color: #5c7369; font-weight: 700; font-size: 14.5px;
    padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
    color: var(--gov-green-dark) !important;
    border-bottom: 3px solid var(--gov-gold) !important;
}

/* ---------- dataframe polish ---------- */
[data-testid="stDataFrame"] {
    border-radius: 14px; overflow: hidden;
    border: 1px solid #e3e8e5;
}

hr { border-color: #e3e8e5 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="gov-topbar">
  <span>🇸🇦 المملكة العربية السعودية — منصة حكومية إلكترونية</span>
  <span>وِقاء | خدمة إلكترونية آمنة وموثوقة 🔒</span>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "notifications" not in st.session_state:
    st.session_state.notifications = []

# --------------------------------------------------
# DEMO DATA
# --------------------------------------------------
@st.cache_data
def build_demo_data():
    today = date.today()
    np.random.seed(42)

    n = 14
    names = [f"وافد {str(i+1).zfill(3)}" for i in range(n)]
    case_ids = [f"WQ-{1001 + i}" for i in range(n)]
    residency_types = np.random.choice(
        ["عمل", "زيارة", "إقامة مميزة", "عمل منزلي"],
        size=n, p=[0.55, 0.2, 0.1, 0.15]
    )
    sectors = np.random.choice(
        ["قطاع خاص", "قطاع حكومي", "أعمال منزلية", "غير مصنف"],
        size=n, p=[0.5, 0.15, 0.15, 0.2]
    )
    offsets = [5, 12, 25, 45, 75, -3, 8, -10, 2, 18, 60, -1, 33, 90]
    expiry_dates = [today + timedelta(days=o) for o in offsets]
    processing_time = [1.2, 0.8, 0.5, 0.2, 0.1, 4.8, 1.7, 6.1,
                        0.9, 1.1, 0.3, 5.4, 0.6, 0.2]
    channels = np.random.choice(
        ["رسالة نصية", "بريد إلكتروني", "تطبيق الجوال"], size=n
    )

    df = pd.DataFrame({
        "رقم الحالة": case_ids,
        "الاسم": names,
        "الجهة/القطاع": sectors,
        "نوع الإقامة": residency_types,
        "تاريخ الانتهاء": expiry_dates,
        "زمن المعالجة": processing_time,
        "قناة التواصل": channels,
    })
    df["الأيام المتبقية"] = (
        pd.to_datetime(df["تاريخ الانتهاء"]) - pd.Timestamp(today)
    ).dt.days

    def status_from_days(d):
        if d < 0:
            return "منتهية"
        elif d <= 7:
            return "تنبيه عاجل"
        elif d <= 14:
            return "متابعة"
        elif d <= 30:
            return "تنبيه مبكر"
        else:
            return "مستقرة"

    df["حالة الإجراء"] = df["الأيام المتبقية"].apply(status_from_days)
    return df

base_data = build_demo_data()

# --------------------------------------------------
# RISK ENGINE
# --------------------------------------------------
def calculate_risk(days):
    if days < 0:
        return 100
    elif days <= 7:
        return 90
    elif days <= 14:
        return 75
    elif days <= 30:
        return 50
    elif days <= 60:
        return 25
    else:
        return 10

STATUS_COLORS = {
    "منتهية": "#d92d20",
    "تنبيه عاجل": "#f79009",
    "متابعة": "#fac515",
    "تنبيه مبكر": "#2e90fa",
    "مستقرة": "#12b76a",
}

# --------------------------------------------------
# SIDEBAR — simulation / control panel (MAEEN-style)
# --------------------------------------------------
st.sidebar.markdown("## 🛡️ وِقاء")
st.sidebar.caption("WIQAA | Immigration Compliance Intelligence")
st.sidebar.divider()

st.sidebar.markdown("### ⚙️ محاكاة مدخلات النظام")
st.sidebar.caption("اختر السيناريو (Preset):")

SCENARIO_OPTIONS = ["مخصص (Custom)", "يوم طبيعي (Normal Day)",
                     "ذروة التجديدات (Renewal Peak)", "أزمة امتثال (Compliance Crisis)"]
st.session_state.setdefault("scenario_radio", SCENARIO_OPTIONS[0])

scenario = st.sidebar.radio(
    "السيناريو",
    SCENARIO_OPTIONS,
    key="scenario_radio",
    label_visibility="collapsed",
)

# Scenario presets drive the two core simulation sliders
scenario_defaults = {
    "مخصص (Custom)": (30, 6),
    "يوم طبيعي (Normal Day)": (15, 3),
    "ذروة التجديدات (Renewal Peak)": (55, 10),
    "أزمة امتثال (Compliance Crisis)": (80, 14),
}
default_load, default_intake = scenario_defaults[scenario]

# When the scenario preset changes (via the radio OR the CTA button),
# push its defaults into the slider widgets before they're created.
if st.session_state.get("_last_scenario") != scenario:
    st.session_state["case_load_slider"] = default_load
    st.session_state["daily_intake_slider"] = default_intake
    st.session_state["_last_scenario"] = scenario

case_load_pct = st.sidebar.slider(
    "نسبة الحالات شبه الحرجة (%)", 0, 100, step=5,
    key="case_load_slider",
    help="نسبة الحالات المفترضة أنها قريبة من الانتهاء في هذا السيناريو"
)
daily_intake = st.sidebar.slider(
    "معدل الحالات الجديدة يوميًا", 0, 30, step=1,
    key="daily_intake_slider",
)
automation_pct = st.sidebar.slider(
    "نسبة الأتمتة المقترحة (%)", 0, 90, 30, step=10
)

st.sidebar.divider()
type_filter = st.sidebar.multiselect(
    "🔍 تصفية حسب نوع الإقامة",
    options=sorted(base_data["نوع الإقامة"].unique().tolist()),
    default=sorted(base_data["نوع الإقامة"].unique().tolist()),
)

st.sidebar.divider()
st.sidebar.info(
    "نسخة تجريبية للهاكاثون\n\nجميع البيانات المعروضة افتراضية "
    "ولا تمثل بيانات حقيقية لأي جهة."
)

# Apply scenario stress factor to a working copy of the data (demo simulation only)
data = base_data.copy()
data = data[data["نوع الإقامة"].isin(type_filter)] if type_filter else data
stress_factor = case_load_pct / 30.0  # 30% treated as baseline
data["الأيام المتبقية"] = (data["الأيام المتبقية"] / max(stress_factor, 0.3)).round().astype(int)
data["درجة الأولوية"] = data["الأيام المتبقية"].apply(calculate_risk)
data["حالة الإجراء"] = data["الأيام المتبقية"].apply(
    lambda d: "منتهية" if d < 0 else "تنبيه عاجل" if d <= 7 else "متابعة"
    if d <= 14 else "تنبيه مبكر" if d <= 30 else "مستقرة"
)
data["زمن المعالجة"] = (data["زمن المعالجة"] * (1 - automation_pct / 100)).round(2)

# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------
st.markdown(f"""
<div class="wiqaa-hero">
  <div class="wiqaa-eyebrow">WIQAA | وِقاء</div>
  <div class="wiqaa-title">وِقاء 🛡️</div>
  <div class="wiqaa-subtitle">من الوقاية من المخالفة إلى تسريع معالجتها — منصة استباقية لإدارة امتثال الإقامة، مدعومة بالذكاء الاصطناعي.</div>
</div>
""", unsafe_allow_html=True)


def _run_interactive_scenario():
    """CTA action: loads the most demanding preset (crisis) so every panel
    (gauges, decision map, recommendations) lights up for the demo."""
    st.session_state["scenario_radio"] = "أزمة امتثال (Compliance Crisis)"
    st.session_state["case_load_slider"] = 80
    st.session_state["daily_intake_slider"] = 14
    st.session_state["scenario_just_ran"] = True


st.button("▶ تشغيل السيناريو التفاعلي", key="run_scenario_btn",
          on_click=_run_interactive_scenario)

if st.session_state.get("scenario_just_ran"):
    st.success("تم تشغيل سيناريو «أزمة امتثال» — تحقق من الشريط الجانبي ولوحة النظرة العامة.")
    st.session_state["scenario_just_ran"] = False

st.write("")

stages = ["تسجيل", "حساب", "تنبؤ", "إشعار", "كشف",
          "ترتيب أولوية", "توجيه", "معالجة", "إغلاق", "تعلّم"]
st.markdown(
    " ".join(
        f'<span class="badge">{s}</span>'
        + ('<span class="badge-arrow">←</span>' if i < len(stages) - 1 else "")
        for i, s in enumerate(stages)
    ),
    unsafe_allow_html=True,
)
st.write("")

# --------------------------------------------------
# TABS — MAEEN-style top navigation
# --------------------------------------------------
tab_overview, tab_registry, tab_predict, tab_violations, tab_process, tab_recs = st.tabs(
    ["📊 نظرة عامة", "👤 سجل الوافدين", "🔮 التنبؤ الذكي",
     "🚨 الحالات المخالفة", "⚙️ المحاكاة والتحسين", "🧠 التوصيات"]
)

# ==================================================
# TAB 1 — OVERVIEW
# ==================================================
with tab_overview:
    total = len(data)
    expiring_30 = len(data[(data["الأيام المتبقية"] >= 0) & (data["الأيام المتبقية"] <= 30)])
    expired = len(data[data["الأيام المتبقية"] < 0])
    urgent = len(data[data["درجة الأولوية"] >= 75])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي الحالات", total)
    c2.metric("تنتهي خلال 30 يوم", expiring_30)
    c3.metric("إقامات منتهية", expired)
    c4.metric("تحتاج تدخل عاجل", urgent)

    st.divider()

    # Decision-map style section, mirroring MAEEN's layout
    col_map, col_gauge = st.columns([1.3, 1])

    with col_map:
        st.markdown("#### 🗺️ خريطة قرار وِقاء (Decision Map)")
        top_sector = (
            data.groupby("الجهة/القطاع")["درجة الأولوية"].mean()
            .sort_values(ascending=False)
        )
        if len(top_sector) > 0:
            worst_sector = top_sector.index[0]
            worst_score = top_sector.iloc[0]
            st.markdown(f"""
            <div class="pin-card">
              <div class="pin-title">📍 القطاع الأكثر تأثرًا</div>
              <div class="pin-sub">{worst_sector} — متوسط درجة الأولوية {worst_score:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        near_expiry = data[data["الأيام المتبقية"].between(0, 7)]
        st.markdown(f"""
        <div class="pin-card">
          <div class="pin-title">📍 حالات في نافذة الخطر (٧ أيام)</div>
          <div class="pin-sub">{len(near_expiry)} حالة تحتاج تدخلًا فوريًا خلال الأسبوع القادم</div>
        </div>
        """, unsafe_allow_html=True)
        expired_channel = data[data["الأيام المتبقية"] < 0]["قناة التواصل"].mode()
        ch = expired_channel.iloc[0] if len(expired_channel) else "—"
        st.markdown(f"""
        <div class="pin-card">
          <div class="pin-title">📍 القناة الأنسب للتصعيد</div>
          <div class="pin-sub">{ch} — الأكثر استخدامًا لدى الحالات شديدة الخطورة</div>
        </div>
        """, unsafe_allow_html=True)

    with col_gauge:
        st.markdown("#### مؤشر الخطر اللحظي (Risk Gauge)")
        overall_risk = data["درجة الأولوية"].mean() if total else 0
        g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_risk,
            number={"suffix": ""},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#5c7369"},
                "bar": {"color": "#B8912F"},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(18,183,106,0.35)"},
                    {"range": [40, 70], "color": "rgba(247,144,9,0.35)"},
                    {"range": [70, 100], "color": "rgba(217,45,32,0.35)"},
                ],
            },
        ))
        g.update_layout(
            height=300, margin=dict(t=20, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)", font={"color": "#1c2b24"}
        )
        st.plotly_chart(g, use_container_width=True)

    st.divider()

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("توزيع الحالات حسب قرب انتهاء الإقامة")

        def expiry_group(d):
            if d < 0:
                return "منتهية"
            elif d <= 7:
                return "خلال 7 أيام"
            elif d <= 30:
                return "خلال 30 يوم"
            elif d <= 60:
                return "خلال 60 يوم"
            else:
                return "أكثر من 60 يوم"

        order = ["منتهية", "خلال 7 أيام", "خلال 30 يوم", "خلال 60 يوم", "أكثر من 60 يوم"]
        chart_data = data["الأيام المتبقية"].apply(expiry_group).value_counts().reindex(order).fillna(0).reset_index()
        chart_data.columns = ["الفترة", "عدد الحالات"]
        fig = px.bar(chart_data, x="الفترة", y="عدد الحالات",
                     color="الفترة",
                     color_discrete_map={
                         "منتهية": "#d92d20", "خلال 7 أيام": "#f79009",
                         "خلال 30 يوم": "#2e90fa", "خلال 60 يوم": "#7a5af8",
                         "أكثر من 60 يوم": "#12b76a"
                     })
        fig.update_layout(
            showlegend=False, height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#1c2b24"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("مؤشر الصحة العامة")
        compliance_score = max(0, 100 - (urgent / max(total, 1)) * 100)
        gauge2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=compliance_score,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#5c7369"},
                "bar": {"color": "#12b76a" if compliance_score >= 70 else "#f79009"},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(217,45,32,0.25)"},
                    {"range": [40, 70], "color": "rgba(247,144,9,0.25)"},
                    {"range": [70, 100], "color": "rgba(18,183,106,0.25)"},
                ],
            },
        ))
        gauge2.update_layout(
            height=280, margin=dict(t=30, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)", font={"color": "#1c2b24"}
        )
        st.plotly_chart(gauge2, use_container_width=True)

    st.subheader("🚨 الحالات ذات الأولوية")
    priority = data.sort_values("درجة الأولوية", ascending=False).head(6)
    st.dataframe(
        priority[["رقم الحالة", "تاريخ الانتهاء", "الأيام المتبقية",
                  "درجة الأولوية", "حالة الإجراء"]],
        use_container_width=True, hide_index=True,
    )

# ==================================================
# TAB 2 — REGISTRY
# ==================================================
with tab_registry:
    st.write("قاعدة بيانات تجريبية لمتابعة صلاحية الإقامات.")
    search = st.text_input("🔎 البحث برقم الحالة أو الاسم")
    filtered = data.copy()
    if search:
        filtered = filtered[
            filtered["رقم الحالة"].str.contains(search, case=False, na=False)
            | filtered["الاسم"].str.contains(search, case=False, na=False)
        ]

    st.dataframe(
        filtered[["رقم الحالة", "الاسم", "الجهة/القطاع", "نوع الإقامة",
                  "تاريخ الانتهاء", "الأيام المتبقية", "حالة الإجراء"]],
        use_container_width=True, hide_index=True,
    )

    csv = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ تنزيل كملف CSV", data=csv,
                        file_name="wiqaa_residents.csv", mime="text/csv")

# ==================================================
# TAB 3 — PREDICTION
# ==================================================
with tab_predict:
    st.write("يحدد النظام الحالات التي تحتاج إلى تدخل قبل انتهاء صلاحية الإقامة.")

    if data.empty:
        st.warning("لا توجد حالات مطابقة للفلترة الحالية.")
    else:
        selected = st.selectbox("اختر حالة", data["رقم الحالة"])
        row = data[data["رقم الحالة"] == selected].iloc[0]
        days = int(row["الأيام المتبقية"])
        risk = row["درجة الأولوية"]

        c1, c2, c3 = st.columns(3)
        c1.metric("تاريخ الانتهاء", pd.to_datetime(row["تاريخ الانتهاء"]).strftime("%Y-%m-%d"))
        c2.metric("الأيام المتبقية", days)
        c3.metric("درجة الأولوية", f"{risk}%")

        st.divider()

        col_gauge, col_timeline = st.columns([1, 2])
        with col_gauge:
            g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk,
                title={"text": "درجة الخطورة"},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#5c7369"},
                    "bar": {"color": STATUS_COLORS.get(row["حالة الإجراء"], "#667085")},
                    "bgcolor": "rgba(0,0,0,0)",
                }
            ))
            g.update_layout(
                height=260, margin=dict(t=40, b=10, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)", font={"color": "#1c2b24"}
            )
            st.plotly_chart(g, use_container_width=True)

        with col_timeline:
            st.markdown("**الخط الزمني للحالة**")
            today = date.today()
            expiry = pd.to_datetime(row["تاريخ الانتهاء"]).date()
            timeline_df = pd.DataFrame({
                "الحدث": ["اليوم", "تاريخ الانتهاء"],
                "التاريخ": [today, expiry],
            })
            tfig = px.scatter(timeline_df, x="التاريخ", y=["الحدث"] * 2,
                               text="الحدث", color="الحدث")
            tfig.update_traces(marker=dict(size=16), textposition="top center")
            tfig.update_yaxes(visible=False)
            tfig.update_layout(
                height=260, showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#1c2b24"}
            )
            st.plotly_chart(tfig, use_container_width=True)

        if days < 0:
            st.markdown('<div class="danger-card">🔴 الإقامة منتهية — الحالة تحتاج مراجعة وفق الإجراءات النظامية.</div>', unsafe_allow_html=True)
        elif days <= 7:
            st.markdown('<div class="alert-card">⚠️ تنبيه عاجل: الإقامة تقترب من الانتهاء.</div>', unsafe_allow_html=True)
        elif days <= 30:
            st.markdown('<div class="info-card">🟠 تنبيه مبكر: يوصى باتخاذ الإجراء قبل اقتراب موعد الانتهاء.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-card">🟢 الحالة مستقرة حاليًا.</div>', unsafe_allow_html=True)

        st.subheader("📲 محاكاة إشعار الوافد")
        if st.button("إرسال تنبيه تجريبي"):
            note = {
                "رقم الحالة": selected,
                "القناة": row["قناة التواصل"],
                "التاريخ": date.today().strftime("%Y-%m-%d %H:%M"),
                "الرسالة": f"ستنتهي إقامتك بتاريخ {expiry}. يرجى اتخاذ الإجراء النظامي.",
            }
            st.session_state.notifications.insert(0, note)
            st.success(f"تم إرسال تنبيه تجريبي للحالة {selected} عبر {row['قناة التواصل']}.")

        st.divider()
        st.subheader("📲 مركز الإشعارات")
        notes = st.session_state.notifications
        nc1, nc2 = st.columns(2)
        nc1.metric("إجمالي الإشعارات المُرسلة", len(notes))
        if notes:
            by_channel = pd.DataFrame(notes)["القناة"].value_counts().idxmax()
            nc2.metric("القناة الأكثر استخدامًا", by_channel)
            st.dataframe(pd.DataFrame(notes), use_container_width=True, hide_index=True)
        else:
            nc2.metric("القناة الأكثر استخدامًا", "—")
            st.info("لم يتم إرسال أي إشعارات بعد.")

# ==================================================
# TAB 4 — VIOLATIONS
# ==================================================
with tab_violations:
    violations = data[data["الأيام المتبقية"] < 0].copy()
    st.metric("إجمالي الحالات المنتهية", len(violations))
    st.divider()

    if len(violations) > 0:
        violations["أولوية المعالجة"] = violations["درجة الأولوية"]
        violations = violations.sort_values("أولوية المعالجة", ascending=False)
        st.dataframe(
            violations[["رقم الحالة", "تاريخ الانتهاء", "الأيام المتبقية",
                        "أولوية المعالجة", "زمن المعالجة"]],
            use_container_width=True, hide_index=True,
        )
        st.subheader("🧠 توصية النظام")
        st.markdown(
            '<div class="info-card">يتم ترتيب الحالات حسب الأولوية وزمن التأخر، '
            'ثم توجيهها للمسار الإجرائي المختص وفق الصلاحيات المعتمدة.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="success-card">لا توجد حالات منتهية في البيانات التجريبية المفلترة حاليًا.</div>', unsafe_allow_html=True)

# ==================================================
# TAB 5 — PROCESS SIMULATION
# ==================================================
with tab_process:
    st.write("تحليل الاختناقات في معالجة الحالات ومحاكاة أثر تحسين الطاقة التشغيلية.")

    avg_time = data["زمن المعالجة"].mean() if len(data) else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("متوسط زمن المعالجة", f"{avg_time:.1f} يوم")
    c2.metric("أعلى زمن معالجة", f"{data['زمن المعالجة'].max():.1f} يوم" if len(data) else "—")
    c3.metric("حالات تحتاج تدخل", len(data[data["زمن المعالجة"] > 3]))

    st.divider()

    process_data = data[["رقم الحالة", "زمن المعالجة"]].sort_values(
        "زمن المعالجة", ascending=False
    )
    fig = px.bar(process_data, x="رقم الحالة", y="زمن المعالجة",
                 title="زمن معالجة الحالات (بعد تطبيق نسبة الأتمتة من لوحة المحاكاة)")
    fig.update_layout(
        height=340, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#1c2b24"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔎 الاختناقات المحتملة")
    bottlenecks = data[data["زمن المعالجة"] > 3]
    if len(bottlenecks) > 0:
        st.markdown(
            f'<div class="alert-card">تم رصد {len(bottlenecks)} حالات تتجاوز 3 أيام '
            'في البيانات التجريبية. التوصية: مراجعة سبب التأخير وإعادة توزيع الحالات '
            'وفق الطاقة التشغيلية والصلاحيات المعتمدة.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="success-card">لا توجد اختناقات واضحة في البيانات التجريبية.</div>', unsafe_allow_html=True)

    st.caption(f"تُطبَّق حاليًا نسبة أتمتة {automation_pct}% ومعدّل حالات جديدة {daily_intake}/يوم — يمكن تعديلهما من لوحة المحاكاة في الشريط الجانبي.")

# ==================================================
# TAB 6 — RECOMMENDATIONS
# ==================================================
with tab_recs:
    st.write("توصيات مولّدة من نمط الحالات الحالية ومخرجات المحاكاة.")

    recs = []
    if expired > 0:
        recs.append(("🔴", f"يوجد {expired} حالة منتهية — يوصى بفتح مسار تصعيد فوري ومراجعة الاستثناءات النظامية."))
    if urgent > 0:
        recs.append(("🟠", f"{urgent} حالة بدرجة أولوية ≥75% — إرسال تنبيه عبر القناة الأكثر استجابة قبل نهاية اليوم."))
    if len(data[data["زمن المعالجة"] > 3]) > 0:
        recs.append(("🔵", "رُصدت اختناقات في زمن المعالجة — رفع نسبة الأتمتة في لوحة المحاكاة يقلّص متوسط الزمن بشكل مباشر."))
    if daily_intake >= 10:
        recs.append(("🟣", f"معدل التدفق اليومي مرتفع ({daily_intake} حالة/يوم) — يوصى بزيادة الطاقة التشغيلية أو التصعيد التلقائي للحالات الحرجة."))
    if not recs:
        recs.append(("🟢", "لا توجد مؤشرات خطر حرجة حاليًا وفق بيانات السيناريو المختار."))

    for icon, text in recs:
        st.markdown(f'<div class="pin-card"><div class="pin-title">{icon} توصية</div><div class="pin-sub">{text}</div></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🧪 محاكاة قبل / بعد التحسين")
    improved = process_data.copy()
    improved["زمن المعالجة"] = improved["زمن المعالجة"]  # already automation-adjusted above
    baseline = data.copy()
    baseline_avg = (baseline["زمن المعالجة"] / max(1 - automation_pct / 100, 0.1)).mean() if len(baseline) else 0
    compare = pd.concat([
        process_data.assign(الحالة="بعد التحسين"),
    ])
    cfig = px.bar(compare, x="رقم الحالة", y="زمن المعالجة", color="الحالة",
                  barmode="group", title="أثر الأتمتة على زمن المعالجة")
    cfig.update_layout(
        height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#1c2b24"}
    )
    st.plotly_chart(cfig, use_container_width=True)

    saved = baseline_avg - avg_time
    st.markdown(
        f'<div class="success-card">بتطبيق {automation_pct}% أتمتة، ينخفض متوسط '
        f'زمن المعالجة من {baseline_avg:.1f} يوم إلى {avg_time:.1f} يوم '
        f'(توفير {max(saved,0):.1f} يوم لكل حالة تقريبًا).</div>',
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption("WIQAA | Hackathon Prototype | Demo Data Only — REGISTER → CALCULATE → PREDICT → NOTIFY → DETECT → PRIORITIZE → ROUTE → PROCESS → CLOSE → LEARN")
