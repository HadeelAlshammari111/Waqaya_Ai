import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from waqaya_engine import WaqayaEngine
# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Waqaya AI",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================
# GLOBAL STYLE
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #f4f7fb;
}
.block-container {
    max-width: 1450px;
    padding: 2rem 3rem 4rem 3rem;
}
/* Remove default Streamlit spacing */
div[data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #081525;
    border-right: 1px solid #14263b;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.2rem;
}
section[data-testid="stSidebar"] * {
    color: #e8eef6 !important;
}
section[data-testid="stSidebar"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] input {
    color: #0f172a !important;
}
/* Buttons */
.stButton > button {
    border-radius: 11px;
    border: none;
    min-height: 44px;
    font-weight: 700;
    transition: 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
}
/* Header */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}
.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}
.brand-mark {
    width: 46px;
    height: 46px;
    border-radius: 13px;
    background: linear-gradient(135deg, #0f766e, #164e63);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
    box-shadow: 0 8px 20px rgba(15,118,110,0.22);
}
.brand-name {
    font-size: 21px;
    font-weight: 800;
    color: #0f172a;
}
.brand-sub {
    font-size: 11px;
    color: #64748b;
    margin-top: 2px;
}
/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 85% 20%, rgba(45,212,191,0.18), transparent 28%),
        linear-gradient(135deg, #071525 0%, #0d2940 55%, #0e4350 100%);
    border-radius: 25px;
    padding: 40px 42px;
    color: white;
    min-height: 220px;
    box-shadow: 0 20px 45px rgba(8,21,37,0.14);
}
.hero:after {
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 50%;
    right: -90px;
    top: -100px;
}
.hero-kicker {
    color: #5eead4;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
}
.hero-title {
    font-size: 40px;
    line-height: 1.1;
    font-weight: 800;
    margin-top: 10px;
    letter-spacing: -1.2px;
}
.hero-description {
    max-width: 720px;
    color: #c8d5e3;
    font-size: 15px;
    line-height: 1.75;
    margin-top: 12px;
}
.hero-pill {
    display: inline-block;
    margin-top: 19px;
    padding: 7px 13px;
    border: 1px solid rgba(255,255,255,0.13);
    background: rgba(255,255,255,0.07);
    border-radius: 50px;
    font-size: 11px;
    color: #dbeafe;
}
/* Section */
.section-head {
    margin-top: 32px;
    margin-bottom: 15px;
}
.section-title {
    color: #0f172a;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.4px;
}
.section-description {
    color: #64748b;
    font-size: 13px;
    margin-top: 4px;
}
/* Cards */
.card {
    background: white;
    border: 1px solid #e5eaf0;
    border-radius: 19px;
    padding: 21px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.045);
}
.card-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}
.card-title {
    color: #0f172a;
    font-size: 17px;
    font-weight: 750;
    margin-top: 5px;
}
.card-value {
    color: #0f172a;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}
.card-muted {
    color: #94a3b8;
    font-size: 11px;
    margin-top: 3px;
}
/* Risk cards */
.risk-card {
    background: white;
    border: 1px solid #e5eaf0;
    border-radius: 19px;
    padding: 20px;
    min-height: 152px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.045);
}
.risk-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.risk-title {
    color: #334155;
    font-size: 13px;
    font-weight: 750;
}
.risk-percent {
    color: #0f172a;
    font-size: 25px;
    font-weight: 800;
    margin-top: 12px;
}
.progress {
    height: 7px;
    background: #edf1f5;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 11px;
}
.progress-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #0f766e, #14b8a6);
}
.risk-status {
    color: #64748b;
    font-size: 11px;
    margin-top: 9px;
}
/* Score */
.score-card {
    background: white;
    border: 1px solid #e5eaf0;
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.045);
}
.score-title {
    color: #334155;
    font-size: 13px;
    font-weight: 750;
}
.score-caption {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: -8px;
}
/* Alert */
.alert-card {
    border-radius: 18px;
    padding: 20px 22px;
    margin-top: 5px;
}
.alert-title {
    font-size: 17px;
    font-weight: 800;
}
.alert-text {
    font-size: 13px;
    line-height: 1.75;
    margin-top: 5px;
}
/* Insight */
.insight-card {
    background: #f8fafc;
    border: 1px solid #e5eaf0;
    border-radius: 15px;
    padding: 16px 18px;
    margin-bottom: 9px;
}
.insight-title {
    color: #0f172a;
    font-size: 13px;
    font-weight: 750;
}
.insight-text {
    color: #64748b;
    font-size: 12px;
    line-height: 1.65;
    margin-top: 4px;
}
/* Feature */
.feature-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #eef2f6;
}
.feature-name {
    color: #334155;
    font-size: 13px;
    font-weight: 600;
}
.feature-value {
    color: #0f766e;
    font-size: 13px;
    font-weight: 800;
}
/* Footer */
.footer {
    margin-top: 50px;
    padding: 25px 0 10px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
    color: #94a3b8;
    font-size: 11px;
    line-height: 1.7;
}
/* RTL */
.rtl {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)
# ============================================================
# SESSION STATE
# ============================================================
if "language" not in st.session_state:
    st.session_state.language = "English"
# ============================================================
# TRANSLATIONS
# ============================================================
TEXT = {
    "English": {
        "dashboard": "Health Intelligence Dashboard",
        "kicker": "PREVENTIVE HEALTH INTELLIGENCE",
        "hero_title": "Understand your health pattern before it becomes a warning.",
        "hero_desc":
            "Waqaya AI combines machine learning, personal baseline analysis "
            "and anomaly detection to transform health measurements into "
            "an early preventive signal.",
        "prototype": "DATA SCIENCE PROTOTYPE",
        "assessment": "Health Assessment",
        "personal": "Personal Profile",
        "vitals": "Vital Signs",
        "lifestyle": "Lifestyle",
        "analyze": "Analyze Health Profile",
        "overview": "Health Intelligence",
        "overview_desc":
            "A unified view of your current preventive health signals.",
        "early_score": "Early Risk Score",
        "anomaly": "Anomaly Signal",
        "status": "Current Status",
        "stable": "Stable",
        "monitor": "Monitor",
        "attention": "Attention",
        "risk": "Risk Intelligence",
        "risk_desc":
            "Prototype risk estimates generated by trained machine-learning models.",
        "diabetes": "Diabetes",
        "cardio": "Cardiovascular",
        "respiratory": "Respiratory",
        "dehydration": "Dehydration",
        "low": "Low",
        "moderate": "Moderate",
        "elevated": "Elevated",
        "pattern": "Personal Health Pattern",
        "pattern_desc":
            "Monitor how your measurements move over time instead of looking at one reading.",
        "baseline": "Personal Baseline",
        "baseline_desc":
            "Waqaya compares today's measurements with your recent personal pattern.",
        "warning": "AI Early Warning",
        "warning_desc":
            "Signals are generated from the combination of machine-learning risk, "
            "anomaly detection and baseline deviation.",
        "detected": "Preventive attention detected",
        "no_warning": "No elevated preventive warning detected",
        "changed": "What changed today?",
        "explain": "Explainable AI",
        "explain_desc":
            "The features that contribute most to the trained model's predictions.",
        "insights": "Preventive Insights",
        "insights_desc":
            "Simple actions suggested from the current prototype measurements.",
        "footer":
            "Waqaya AI is a Data Science prototype for preventive health monitoring "
            "and early risk estimation. It is not a medical diagnostic system.",
        "language": "Language",
        "today": "Today",
        "current": "Current",
        "baseline_value": "Baseline",
        "deviation": "Deviation",
        "select_metric": "Select health indicator",
        "heart_rate": "Heart Rate",
        "spo2": "SpO2",
        "sleep": "Sleep Hours",
        "steps": "Daily Steps",
        "water": "Water Intake",
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "systolic": "Systolic BP",
        "diastolic": "Diastolic BP",
        "heart": "Heart Rate",
        "water_input": "Water Intake (L)",
        "urination": "Urination Frequency",
        "bmi": "BMI",
        "sleep_input": "Sleep Hours",
        "steps_input": "Daily Steps"
    },
    "العربية": {
        "dashboard": "لوحة المعلومات الصحية الذكية",
        "kicker": "الذكاء الوقائي للصحة",
        "hero_title": "افهم نمطك الصحي قبل أن يتحول إلى إشارة تحذيرية.",
        "hero_desc":
            "تجمع وقاية بين تعلم الآلة وتحليل خط الأساس الشخصي واكتشاف الأنماط غير الطبيعية "
            "لتحويل المؤشرات الصحية إلى إشارات وقائية مبكرة.",
        "prototype": "نموذج أولي لعلوم البيانات",
        "assessment": "التقييم الصحي",
        "personal": "البيانات الشخصية",
        "vitals": "المؤشرات الحيوية",
        "lifestyle": "نمط الحياة",
        "analyze": "تحليل الملف الصحي",
        "overview": "الذكاء الصحي",
        "overview_desc":
            "نظرة موحدة على الإشارات الوقائية الحالية.",
        "early_score": "مؤشر الخطر المبكر",
        "anomaly": "إشارة التغير",
        "status": "الحالة الحالية",
        "stable": "مستقرة",
        "monitor": "تحتاج متابعة",
        "attention": "تحتاج انتباه",
        "risk": "تحليل المخاطر",
        "risk_desc":
            "تقديرات أولية مولدة بواسطة نماذج تعلم آلي مدربة.",
        "diabetes": "السكري",
        "cardio": "القلب والأوعية",
        "respiratory": "الجهاز التنفسي",
        "dehydration": "الجفاف",
        "low": "منخفض",
        "moderate": "متوسط",
        "elevated": "مرتفع",
        "pattern": "النمط الصحي الشخصي",
        "pattern_desc":
            "تابع تغير المؤشرات مع الوقت بدل الاعتماد على قراءة واحدة.",
        "baseline": "خط الأساس الشخصي",
        "baseline_desc":
            "تقارن وقاية قراءات اليوم بالنمط الشخصي الأخير.",
        "warning": "الإنذار الوقائي الذكي",
        "warning_desc":
            "تُبنى الإشارة على دمج تقدير تعلم الآلة واكتشاف التغير والانحراف عن خط الأساس.",
        "detected": "تم اكتشاف إشارة تستحق المتابعة",
        "no_warning": "لم يتم اكتشاف إشارة وقائية مرتفعة",
        "changed": "ماذا تغير اليوم؟",
        "explain": "الذكاء الاصطناعي القابل للتفسير",
        "explain_desc":
            "العوامل الأكثر تأثيرًا في تنبؤات النموذج المدرب.",
        "insights": "الرؤى الوقائية",
        "insights_desc":
            "ملاحظات مبسطة مستخرجة من المؤشرات الحالية في النموذج الأولي.",
        "footer":
            "وقاية AI نموذج أولي لعلوم البيانات للمراقبة الصحية الوقائية وتقدير المخاطر المبكرة. "
            "لا يُعد نظامًا للتشخيص الطبي.",
        "language": "اللغة",
        "today": "اليوم",
        "current": "الحالي",
        "baseline_value": "خط الأساس",
        "deviation": "الانحراف",
        "select_metric": "اختر المؤشر الصحي",
        "heart_rate": "نبض القلب",
        "spo2": "الأكسجين",
        "sleep": "ساعات النوم",
        "steps": "الخطوات اليومية",
        "water": "استهلاك الماء",
        "age": "العمر",
        "gender": "الجنس",
        "male": "ذكر",
        "female": "أنثى",
        "systolic": "الضغط الانقباضي",
        "diastolic": "الضغط الانبساطي",
        "heart": "نبض القلب",
        "water_input": "استهلاك الماء (لتر)",
        "urination": "عدد مرات التبول",
        "bmi": "مؤشر كتلة الجسم",
        "sleep_input": "ساعات النوم",
        "steps_input": "الخطوات اليومية"
    }
}
# ============================================================
# LANGUAGE SELECTOR
# ============================================================
language_col1, language_col2 = st.columns([7, 1])
with language_col2:
    selected_language = st.selectbox(
        "Language",
        ["English", "العربية"],
        index=0 if st.session_state.language == "English" else 1,
        label_visibility="collapsed"
    )
    st.session_state.language = selected_language
L = TEXT[st.session_state.language]
is_arabic = st.session_state.language == "العربية"
# ============================================================
# TOP BRAND
# ============================================================
direction_class = "rtl" if is_arabic else ""
st.markdown(
    f"""
    <div class="top-header {direction_class}">
        <div class="brand">
            <div class="brand-mark">
                W
            </div>
            <div>
                <div class="brand-name">
                    Waqaya AI
                </div>
                <div class="brand-sub">
                    {L["dashboard"]}
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# HERO
# ============================================================
st.markdown(
    f"""
    <div class="hero {direction_class}">
        <div class="hero-kicker">
            {L["kicker"]}
        </div>
        <div class="hero-title">
            {L["hero_title"]}
        </div>
        <div class="hero-description">
            {L["hero_desc"]}
        </div>
        <div class="hero-pill">
            {L["prototype"]}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            Machine Learning
            &nbsp;&nbsp;•&nbsp;&nbsp;
            Personal Baseline
            &nbsp;&nbsp;•&nbsp;&nbsp;
            Anomaly Detection
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:800;
            margin-bottom:4px;">
            Waqaya AI
        </div>
        <div style="
            color:#94a3b8;
            font-size:12px;
            margin-bottom:22px;">
            Preventive Health Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"### {L['assessment']}"
    )
    st.markdown("---")
    st.markdown(
        f"**{L['personal']}**"
    )
    age = st.slider(
        L["age"],
        18,
        90,
        25
    )
    gender_text = st.selectbox(
        L["gender"],
        [L["female"], L["male"]]
    )
    gender = 0 if gender_text == L["female"] else 1
    st.markdown(
        f"**{L['vitals']}**"
    )
    systolic_bp = st.number_input(
        L["systolic"],
        min_value=80,
        max_value=220,
        value=120
    )
    diastolic_bp = st.number_input(
        L["diastolic"],
        min_value=40,
        max_value=140,
        value=80
    )
    heart_rate = st.number_input(
        L["heart"],
        min_value=40,
        max_value=180,
        value=75
    )
    spo2 = st.number_input(
        "SpO2 (%)",
        min_value=70.0,
        max_value=100.0,
        value=98.0,
        step=0.1
    )
    st.markdown(
        f"**{L['lifestyle']}**"
    )
    sleep_hours = st.number_input(
        L["sleep_input"],
        min_value=0.0,
        max_value=16.0,
        value=7.0,
        step=0.5
    )
    steps = st.number_input(
        L["steps_input"],
        min_value=0,
        max_value=50000,
        value=7000,
        step=500
    )
    water_liters = st.number_input(
        L["water_input"],
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1
    )
    urination = st.number_input(
        L["urination"],
        min_value=0,
        max_value=20,
        value=6
    )
    bmi = st.number_input(
        L["bmi"],
        min_value=10.0,
        max_value=60.0,
        value=23.0,
        step=0.1
    )
    st.markdown("---")
    analyze = st.button(
        L["analyze"],
        use_container_width=True,
        type="primary"
    )
# ============================================================
# CURRENT DATA
# ============================================================
current_data = pd.DataFrame([{
    "age": age,
    "gender": gender,
    "systolic_bp": systolic_bp,
    "diastolic_bp": diastolic_bp,
    "heart_rate": heart_rate,
    "spo2": spo2,
    "sleep_hours": sleep_hours,
    "steps": steps,
    "water_liters": water_liters,
    "urination": urination,
    "bmi": bmi
}])
# ============================================================
# ENGINE
# ============================================================
@st.cache_resource
def get_engine():
    return WaqayaEngine(
        model_path="waqaya_models.pkl"
    )
try:
    engine = get_engine()
except Exception as error:
    st.error(
        "Waqaya AI model package could not be loaded."
    )
    st.code(str(error))
    st.stop()
# ============================================================
# DEMONSTRATION HISTORY
# ============================================================
np.random.seed(42)
history = pd.DataFrame({
    "day": [
        "Day 1",
        "Day 2",
        "Day 3",
        "Day 4",
        "Day 5",
        "Day 6",
        "Today"
    ],
    "age": [age] * 7,
    "gender": [gender] * 7,
    "systolic_bp": np.clip(
        systolic_bp + np.random.normal(0, 4, 7),
        80,
        220
    ),
    "diastolic_bp": np.clip(
        diastolic_bp + np.random.normal(0, 3, 7),
        40,
        140
    ),
    "heart_rate": np.clip(
        heart_rate + np.random.normal(0, 5, 7),
        40,
        180
    ),
    "spo2": np.clip(
        spo2 + np.random.normal(0, 0.6, 7),
        70,
        100
    ),
    "sleep_hours": np.clip(
        sleep_hours + np.random.normal(0, 0.5, 7),
        0,
        16
    ),
    "steps": np.clip(
        steps + np.random.normal(0, 900, 7),
        0,
        50000
    ),
    "water_liters": np.clip(
        water_liters + np.random.normal(0, 0.2, 7),
        0,
        10
    ),
    "urination": np.clip(
        urination + np.random.normal(0, 0.7, 7),
        0,
        20
    ),
    "bmi": np.clip(
        bmi + np.random.normal(0, 0.2, 7),
        10,
        60
    )
})
# ============================================================
# ANALYZE
# ============================================================
try:
    analysis = engine.analyze(
        current_data=current_data,
        history=history
    )
except Exception as error:
    st.error(
        "An error occurred while analyzing the health profile."
    )
    st.code(str(error))
    st.stop()
# ============================================================
# RESULTS
# ============================================================
risk_predictions = analysis.get(
    "risk_predictions",
    {}
)
early_risk = analysis.get(
    "early_risk_score",
    0
)
anomaly = analysis.get(
    "anomaly",
    {}
)
baseline = analysis.get(
    "baseline",
    {}
)
baseline_deviation = analysis.get(
    "baseline_deviation",
    {}
)
feature_importance = analysis.get(
    "feature_importance",
    {}
)
# ============================================================
# SAFE NUMBER
# ============================================================
def percent(value):
    try:
        if isinstance(value, dict):
            value = value.get(
                "probability",
                value.get(
                    "score",
                    value.get(
                        "value",
                        0
                    )
                )
            )
        value = float(value)
        if value <= 1:
            value *= 100
        return float(
            np.clip(
                value,
                0,
                100
            )
        )
    except Exception:
        return 0.0
# ============================================================
# STATUS
# ============================================================
early_score = percent(
    early_risk
)
if early_score < 30:
    status = L["stable"]
elif early_score < 60:
    status = L["monitor"]
else:
    status = L["attention"]
# ============================================================
# SECTION: OVERVIEW
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            {L["overview"]}
        </div>
        <div class="section-description">
            {L["overview_desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(
    [1.2, 1, 1, 1]
)
# ------------------------------------------------------------
# SCORE GAUGE
# ------------------------------------------------------------
with overview_col1:
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=early_score,
            number={
                "suffix": "%",
                "font": {
                    "size": 34,
                    "color": "#0f172a"
                }
            },
            title={
                "text": L["early_score"],
                "font": {
                    "size": 13,
                    "color": "#475569"
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 0,
                    "tickcolor": "rgba(0,0,0,0)"
                },
                "bar": {
                    "color": "#0f766e"
                },
                "bgcolor": "#edf2f5",
                "borderwidth": 0,
                "steps": [
                    {
                        "range": [0, 30],
                        "color": "#ecfdf5"
                    },
                    {
                        "range": [30, 60],
                        "color": "#fefce8"
                    },
                    {
                        "range": [60, 100],
                        "color": "#fff7ed"
                    }
                ]
            }
        )
    )
    gauge.update_layout(
        height=190,
        margin=dict(
            l=15,
            r=15,
            t=30,
            b=0
        ),
        paper_bgcolor="white",
        font={
            "family": "Inter"
        }
    )
    st.plotly_chart(
        gauge,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )
# ------------------------------------------------------------
# ANOMALY
# ------------------------------------------------------------
with overview_col2:
    anomaly_score = percent(
        anomaly.get(
            "score",
            anomaly.get(
                "anomaly_score",
                0
            )
        )
    )
    st.markdown(
        f"""
        <div class="card">
            <div class="card-label">
                {L["anomaly"]}
            </div>
            <div class="card-value">
                {anomaly_score:.0f}%
            </div>
            <div class="card-muted">
                Pattern deviation signal
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ------------------------------------------------------------
# STATUS
# ------------------------------------------------------------
with overview_col3:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-label">
                {L["status"]}
            </div>
            <div class="card-value"
                 style="font-size:24px;">
                {status}
            </div>
            <div class="card-muted">
                Preventive monitoring state
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ------------------------------------------------------------
# DATA POINTS
# ------------------------------------------------------------
with overview_col4:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-label">
                Health Indicators
            </div>
            <div class="card-value">
                {len(current_data.columns)}
            </div>
            <div class="card-muted">
                Input features analyzed
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# SECTION: RISK
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            {L["risk"]}
        </div>
        <div class="section-description">
            {L["risk_desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
risk_items = [
    (
        L["diabetes"],
        "diabetes_risk"
    ),
    (
        L["cardio"],
        "cardio_risk"
    ),
    (
        L["respiratory"],
        "respiratory_risk"
    ),
    (
        L["dehydration"],
        "dehydration_risk"
    )
]
risk_columns = st.columns(4)
for column, (label, key) in zip(
    risk_columns,
    risk_items
):
    value = percent(
        risk_predictions.get(
            key,
            0
        )
    )
    if value < 30:
        level = L["low"]
    elif value < 60:
        level = L["moderate"]
    else:
        level = L["elevated"]
    with column:
        st.markdown(
            f"""
            <div class="risk-card {direction_class}">
                <div class="risk-top">
                    <div class="risk-title">
                        {label}
                    </div>
                    <div style="
                        font-size:10px;
                        color:#94a3b8;">
                        AI
                    </div>
                </div>
                <div class="risk-percent">
                    {value:.0f}%
                </div>
                <div class="progress">
                    <div class="progress-fill"
                         style="width:{value}%;">
                    </div>
                </div>
                <div class="risk-status">
                    {level} risk signal
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ============================================================
# RISK VISUALIZATION
# ============================================================
risk_chart = pd.DataFrame({
    "Risk": [
        L["diabetes"],
        L["cardio"],
        L["respiratory"],
        L["dehydration"]
    ],
    "Probability": [
        percent(
            risk_predictions.get(
                "diabetes_risk",
                0
            )
        ),
        percent(
            risk_predictions.get(
                "cardio_risk",
                0
            )
        ),
        percent(
            risk_predictions.get(
                "respiratory_risk",
                0
            )
        ),
        percent(
            risk_predictions.get(
                "dehydration_risk",
                0
            )
        )
    ]
})
risk_fig = px.bar(
    risk_chart,
    x="Risk",
    y="Probability",
    text="Probability",
    template="plotly_white"
)
risk_fig.update_traces(
    texttemplate="%{text:.0f}%",
    textposition="outside"
)
risk_fig.update_layout(
    height=360,
    yaxis={
        "range": [0, 100],
        "title": "Risk %",
        "gridcolor": "#edf2f7"
    },
    xaxis={
        "title": ""
    },
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(
        l=20,
        r=20,
        t=25,
        b=20
    ),
    showlegend=False
)
st.plotly_chart(
    risk_fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)
# ============================================================
# SECTION: EARLY WARNING
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            {L["warning"]}
        </div>
        <div class="section-description">
            {L["warning_desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
if early_score >= 60:
    st.markdown(
        f"""
        <div class="alert-card"
             style="
             background:#fff7ed;
             border:1px solid #fed7aa;">
            <div class="alert-title"
                 style="color:#9a3412;">
                {L["detected"]}
            </div>
            <div class="alert-text"
                 style="color:#7c2d12;">
                Waqaya detected an elevated preventive signal.
                The result combines machine-learning risk estimation,
                anomaly detection and personal baseline deviation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div class="alert-card"
             style="
             background:#ecfdf5;
             border:1px solid #a7f3d0;">
            <div class="alert-title"
                 style="color:#065f46;">
                {L["no_warning"]}
            </div>
            <div class="alert-text"
                 style="color:#047857;">
                The current prototype analysis did not identify
                an elevated preventive warning signal.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# SECTION: PERSONAL BASELINE + CHANGES
# ============================================================
baseline_col, changes_col = st.columns(
    [1.35, 1]
)
# ------------------------------------------------------------
# BASELINE
# ------------------------------------------------------------
with baseline_col:
    st.markdown(
        f"""
        <div class="section-head {direction_class}">
            <div class="section-title">
                {L["baseline"]}
            </div>
            <div class="section-description">
                {L["baseline_desc"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    baseline_features = [
        (
            "heart_rate",
            L["heart_rate"]
        ),
        (
            "spo2",
            L["spo2"]
        ),
        (
            "sleep_hours",
            L["sleep"]
        ),
        (
            "steps",
            L["steps"]
        ),
        (
            "water_liters",
            L["water"]
        )
    ]
    baseline_rows = []
    for feature, label in baseline_features:
        current_value = float(
            current_data.iloc[0][feature]
        )
        baseline_value = float(
            baseline.get(
                feature,
                history[feature].mean()
            )
        )
        deviation = float(
            baseline_deviation.get(
                feature,
                0
            )
        )
        baseline_rows.append({
            "Indicator": label,
            L["current"]: round(
                current_value,
                2
            ),
            L["baseline_value"]: round(
                baseline_value,
                2
            ),
            L["deviation"]:
                f"{deviation:+.1f}%"
        })
    baseline_df = pd.DataFrame(
        baseline_rows
    )
    st.dataframe(
        baseline_df,
        use_container_width=True,
        hide_index=True
    )
# ------------------------------------------------------------
# WHAT CHANGED
# ------------------------------------------------------------
with changes_col:
    st.markdown(
        f"""
        <div class="section-head {direction_class}">
            <div class="section-title">
                {L["changed"]}
            </div>
            <div class="section-description">
                Personal deviation signals
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    for feature, label in baseline_features:
        deviation = float(
            baseline_deviation.get(
                feature,
                0
            )
        )
        if abs(deviation) < 5:
            symbol = "Stable"
        elif deviation > 0:
            symbol = f"+{deviation:.1f}%"
        else:
            symbol = f"{deviation:.1f}%"
        st.markdown(
            f"""
            <div class="feature-row">
                <div class="feature-name">
                    {label}
                </div>
                <div class="feature-value">
                    {symbol}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ============================================================
# SECTION: DAILY PATTERN
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            {L["pattern"]}
        </div>
        <div class="section-description">
            {L["pattern_desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
metric_options = {
    L["heart_rate"]:
        "heart_rate",
    L["spo2"]:
        "spo2",
    L["sleep"]:
        "sleep_hours",
    L["steps"]:
        "steps",
    L["water"]:
        "water_liters"
}
selected_metric_label = st.selectbox(
    L["select_metric"],
    list(metric_options.keys())
)
selected_metric = metric_options[
    selected_metric_label
]
pattern_fig = go.Figure()
pattern_fig.add_trace(
    go.Scatter(
        x=history["day"],
        y=history[selected_metric],
        mode="lines+markers",
        line={
            "width": 3,
            "color": "#0f766e"
        },
        marker={
            "size": 8,
            "color": "#0f766e"
        },
        fill="tozeroy",
        fillcolor="rgba(15,118,110,0.08)"
    )
)
pattern_fig.update_layout(
    height=390,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(
        l=20,
        r=20,
        t=25,
        b=20
    ),
    xaxis={
        "title": "",
        "gridcolor": "#f1f5f9"
    },
    yaxis={
        "title": selected_metric_label,
        "gridcolor": "#f1f5f9"
    }
)
st.plotly_chart(
    pattern_fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)
# ============================================================
# EXPLAINABLE AI
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            {L["explain"]}
        </div>
        <div class="section-description">
            {L["explain_desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
importance_rows = []
if isinstance(
    feature_importance,
    dict
):
    for feature, value in feature_importance.items():
        try:
            importance_rows.append({
                "Feature":
                    str(feature)
                    .replace("_", " ")
                    .title(),
                "Importance":
                    float(value)
            })
        except Exception:
            pass
if importance_rows:
    importance_df = pd.DataFrame(
        importance_rows
    ).sort_values(
        "Importance",
        ascending=False
    ).head(8)
    importance_fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        template="plotly_white"
    )
    importance_fig.update_traces(
        marker_color="#0f766e"
    )
    importance_fig.update_layout(
        height=370,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        xaxis={
            "gridcolor": "#f1f5f9"
        },
        yaxis={
            "categoryorder":
                "total ascending"
        }
    )
    st.plotly_chart(
        importance_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )
else:
    st.info(
        "Feature importance is not available."
    )
# ============================================================
# PREVENTIVE INSIGHTS
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            {L["insights"]}
        </div>
        <div class="section-description">
            {L["insights_desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
insights = []
if sleep_hours < 6:
    insights.append(
        (
            "Sleep Pattern",
            "Sleep duration is relatively low in the current input."
        )
    )
if water_liters < 1.5:
    insights.append(
        (
            "Hydration",
            "Water intake is relatively low in the current input."
        )
    )
if steps < 4000:
    insights.append(
        (
            "Activity",
            "Daily activity is relatively low in the current input."
        )
    )
if spo2 < 94:
    insights.append(
        (
            "Oxygen Pattern",
            "SpO2 is below the monitoring range used by this prototype."
        )
    )
if heart_rate > 100:
    insights.append(
        (
            "Heart Rate",
            "Heart rate is elevated relative to this prototype's monitoring range."
        )
    )
if not insights:
    insights.append(
        (
            "Pattern Status",
            "No major preventive insight was triggered by the current prototype rules."
        )
    )
insight_columns = st.columns(
    min(
        len(insights),
        3
    )
)
for index, (title, message) in enumerate(
    insights
):
    with insight_columns[
        index % len(insight_columns)
    ]:
        st.markdown(
            f"""
            <div class="insight-card {direction_class}">
                <div class="insight-title">
                    {title}
                </div>
                <div class="insight-text">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ============================================================
# HOW WAQAYA WORKS
# ============================================================
st.markdown(
    f"""
    <div class="section-head {direction_class}">
        <div class="section-title">
            How Waqaya Works
        </div>
        <div class="section-description">
            From raw health measurements to a preventive intelligence signal.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
process1, process2, process3, process4 = st.columns(4)
process_cards = [
    (
        "01",
        "Health Data",
        "Collect key vital signs and lifestyle indicators."
    ),
    (
        "02",
        "Personal Baseline",
        "Understand the individual's normal pattern."
    ),
    (
        "03",
        "AI Analysis",
        "Estimate risk and detect unusual changes."
    ),
    (
        "04",
        "Early Warning",
        "Transform multiple signals into one preventive view."
    )
]
for column, (
    number,
    title,
    description
) in zip(
    [
        process1,
        process2,
        process3,
        process4
    ],
    process_cards
):
    with column:
        st.markdown(
            f"""
            <div class="card">
                <div style="
                    color:#0f766e;
                    font-size:12px;
                    font-weight:800;">
                    {number}
                </div>
                <div class="card-title">
                    {title}
                </div>
                <div style="
                    color:#64748b;
                    font-size:12px;
                    line-height:1.65;
                    margin-top:7px;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ============================================================
# FOOTER
# ============================================================
st.markdown(
    f"""
    <div class="footer">
        <strong>WAQAYA AI</strong>
        <br>
        {L["footer"]}
        <br><br>
        Preventive Health Intelligence • Data Science • Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)