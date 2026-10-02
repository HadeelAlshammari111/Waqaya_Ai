# ============================================================
# WAQAYA AI — FINAL COMPETITION EDITION
# Preventive Health Intelligence Platform
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from waqaya_engine import WaqayaEngine


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Waqaya AI | وقاية",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "language": "العربية",
    "splash_done": False,
    "profile_completed": False,
    "user_profile": {},
    "glucose_log": [],
    "analysis": None,
    "current_data": None,
    "history": None,
    "analysis_completed": False,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LANGUAGE
# ============================================================

AR = st.session_state.language == "العربية"


TEXT = {

    "ar": {

        "language": "اللغة / Language",

        "start": "ابدأ مع وقاية",

        "profile_title": "لنبدأ ببناء ملفك الصحي",
        "profile_desc":
            "أدخل معلوماتك الأساسية لبناء تجربة صحية أكثر تخصيصًا.",

        "name": "الاسم",
        "age": "العمر",
        "gender": "الجنس",
        "female": "أنثى",
        "male": "ذكر",

        "weight": "الوزن (كجم)",
        "height": "الطول (سم)",

        "yes": "نعم",
        "no": "لا",

        "diabetes":
            "هل تعاني من مرض السكري؟",

        "wearable":
            "هل تستخدم جهازًا ذكيًا لمتابعة صحتك؟",

        "wearable_type":
            "نوع الجهاز الذكي",

        "watch":
            "ساعة أو سوار ذكي",

        "ring":
            "خاتم ذكي",

        "both":
            "كلاهما",

        "create":
            "إنشاء الملف الصحي",

        "bmi":
            "مؤشر كتلة الجسم",

        "personal":
            "الملف الشخصي",

        "vitals":
            "المؤشرات الحيوية",

        "lifestyle":
            "نمط الحياة",

        "systolic":
            "الضغط الانقباضي (mmHg)",

        "diastolic":
            "الضغط الانبساطي (mmHg)",

        "heart":
            "نبض القلب (نبضة/دقيقة)",

        "spo2":
            "تشبع الأكسجين SpO₂ (%)",

        "sleep":
            "ساعات النوم",

        "steps":
            "الخطوات اليومية",

        "water":
            "استهلاك الماء (لتر)",

        "urination":
            "عدد مرات التبول",

        "analyze":
            "تشغيل تحليل وقاية",

        "hero_tag":
            "ذكاء وقائي للصحة",

        "hero_title":
            "افهم نمطك الصحي قبل أن يتحول إلى إشارة تحذيرية.",

        "hero_desc":
            "تجمع وقاية بين تعلم الآلة، خط الأساس الشخصي "
            "واكتشاف الأنماط غير الطبيعية لتحويل المؤشرات "
            "الصحية اليومية إلى رؤى وقائية مبكرة.",

        "ready":
            "وقاية جاهز لتحليل بياناتك",

        "ready_desc":
            "أدخل مؤشراتك من القائمة الجانبية ثم اضغط "
            "تشغيل تحليل وقاية لبدء التحليل.",

        "intelligence":
            "مركز ذكاء وقاية",

        "intelligence_desc":
            "ملخص ذكي للإشارات التي تم اكتشافها من "
            "بياناتك الحالية مقارنة بنمطك المرجعي.",

        "risk_score":
            "مؤشر وقاية المبكر",

        "anomaly":
            "إشارة التغير",

        "status":
            "الحالة الحالية",

        "indicators":
            "المؤشرات المحللة",

        "stable":
            "مستقرة",

        "detected":
            "تم رصد تغير",

        "low":
            "منخفض",

        "moderate":
            "متوسط",

        "high":
            "مرتفع",

        "risk_analysis":
            "تقديرات نماذج تعلم الآلة",

        "risk_desc":
            "تعرض وقاية تقديرات النماذج المحملة داخل النظام. "
            "هذه النتائج ليست تشخيصًا طبيًا.",

        "diabetes_risk":
            "السكري",

        "cardio":
            "القلب والأوعية",

        "respiratory":
            "الجهاز التنفسي",

        "dehydration":
            "الجفاف",

        "baseline":
            "خط الأساس الشخصي",

        "baseline_desc":
            "يقارن وقاية القراءة الحالية بالنمط المرجعي "
            "بدل الاعتماد على الحدود العامة فقط.",

        "why":
            "لماذا تغيّر مؤشر وقاية؟",

        "why_desc":
            "أبرز المؤشرات التي تغيرت مقارنة بخط الأساس المرجعي.",

        "performance":
            "أداء نماذج تعلم الآلة",

        "performance_desc":
            "يتم عرض مقاييس الأداء المحفوظة فعليًا داخل "
            "حزمة النموذج فقط.",

        "explain":
            "الذكاء الاصطناعي القابل للتفسير",

        "explain_desc":
            "اكتشف العوامل الأكثر تأثيرًا في قرارات نماذج وقاية.",

        "demo":
            "مختبر الإنذار المبكر",

        "demo_desc":
            "محاكاة توضيحية تبين كيف يمكن لوقاية اكتشاف "
            "التغير التدريجي في عدة مؤشرات صحية عبر الزمن.",

        "run_demo":
            "تشغيل محاكاة الإنذار المبكر",

        "insights":
            "الرؤى الوقائية",

        "nutrition":
            "حاسبة السعرات والماكروز",

        "activity":
            "مستوى النشاط",

        "goal":
            "الهدف",

        "sedentary":
            "قليل الحركة",

        "light":
            "نشاط خفيف",

        "moderate_activity":
            "نشاط متوسط",

        "active":
            "نشاط مرتفع",

        "maintain":
            "المحافظة على الوزن",

        "lose":
            "خسارة الوزن",

        "gain":
            "زيادة الوزن",

        "protein":
            "البروتين",

        "carbs":
            "الكربوهيدرات",

        "fat":
            "الدهون",

        "diabetes_center":
            "مركز متابعة الجلوكوز",

        "glucose":
            "قراءة الجلوكوز (mg/dL)",

        "measurement":
            "وقت / حالة القياس",

        "fasting":
            "صائم",

        "before_meal":
            "قبل الأكل",

        "after_1h":
            "بعد الأكل بساعة",

        "after_2h":
            "بعد الأكل بساعتين",

        "bedtime":
            "قبل النوم",

        "meal":
            "الوجبة أو ملاحظة",

        "save_glucose":
            "حفظ قراءة السكر",

        "health_search":
            "البحث الصحي",

        "search_type":
            "نوع البحث",

        "disease":
            "البحث عن مرض",

        "symptoms":
            "البحث عن أعراض",

        "search":
            "بحث",

        "how":
            "كيف تعمل وقاية؟",
    },


    "en": {

        "language":
            "Language / اللغة",

        "start":
            "Start with Waqaya",

        "profile_title":
            "Build Your Health Profile",

        "profile_desc":
            "Enter your basic information to build a more "
            "personalized health experience.",

        "name":
            "Name",

        "age":
            "Age",

        "gender":
            "Gender",

        "female":
            "Female",

        "male":
            "Male",

        "weight":
            "Weight (kg)",

        "height":
            "Height (cm)",

        "yes":
            "Yes",

        "no":
            "No",

        "diabetes":
            "Do you have diabetes?",

        "wearable":
            "Do you use a smart health wearable?",

        "wearable_type":
            "Wearable Type",

        "watch":
            "Smartwatch / Band",

        "ring":
            "Smart Ring",

        "both":
            "Both",

        "create":
            "Create Health Profile",

        "bmi":
            "Body Mass Index",

        "personal":
            "Personal Profile",

        "vitals":
            "Vital Signs",

        "lifestyle":
            "Lifestyle",

        "systolic":
            "Systolic BP (mmHg)",

        "diastolic":
            "Diastolic BP (mmHg)",

        "heart":
            "Heart Rate (bpm)",

        "spo2":
            "SpO₂ (%)",

        "sleep":
            "Sleep Hours",

        "steps":
            "Daily Steps",

        "water":
            "Water Intake (L)",

        "urination":
            "Urination Frequency",

        "analyze":
            "Run Waqaya Analysis",

        "hero_tag":
            "PREVENTIVE HEALTH INTELLIGENCE",

        "hero_title":
            "Understand your health pattern before it becomes a warning signal.",

        "hero_desc":
            "Waqaya combines machine learning, personal baselines "
            "and anomaly detection to transform everyday health "
            "indicators into early preventive insights.",

        "ready":
            "Waqaya is ready to analyze your data",

        "ready_desc":
            "Enter your indicators in the sidebar and run "
            "Waqaya Analysis to begin.",

        "intelligence":
            "Waqaya Intelligence Center",

        "intelligence_desc":
            "A unified summary of signals detected from your "
            "current data and reference pattern.",

        "risk_score":
            "Waqaya Early Score",

        "anomaly":
            "Pattern Signal",

        "status":
            "Current Status",

        "indicators":
            "Analyzed Indicators",

        "stable":
            "Stable",

        "detected":
            "Change Detected",

        "low":
            "Low",

        "moderate":
            "Moderate",

        "high":
            "High",

        "risk_analysis":
            "Machine-Learning Risk Estimates",

        "risk_desc":
            "Waqaya displays estimates from the models loaded "
            "into the system. These are not medical diagnoses.",

        "diabetes_risk":
            "Diabetes",

        "cardio":
            "Cardiovascular",

        "respiratory":
            "Respiratory",

        "dehydration":
            "Dehydration",

        "baseline":
            "Personal Health Baseline",

        "baseline_desc":
            "Waqaya compares current readings with a reference "
            "pattern instead of relying only on general thresholds.",

        "why":
            "Why Did Waqaya Change?",

        "why_desc":
            "The indicators showing the largest changes from "
            "the reference baseline.",

        "performance":
            "Machine-Learning Model Performance",

        "performance_desc":
            "Only evaluation metrics actually stored in the "
            "model package are displayed.",

        "explain":
            "Explainable AI",

        "explain_desc":
            "Explore the factors with the greatest influence "
            "on Waqaya's machine-learning models.",

        "demo":
            "Early-Warning Lab",

        "demo_desc":
            "An illustrative simulation showing how Waqaya can "
            "detect gradual multi-indicator changes over time.",

        "run_demo":
            "Run Early-Warning Simulation",

        "insights":
            "Preventive Insights",

        "nutrition":
            "Calories & Macros Calculator",

        "activity":
            "Activity Level",

        "goal":
            "Goal",

        "sedentary":
            "Sedentary",

        "light":
            "Light Activity",

        "moderate_activity":
            "Moderate Activity",

        "active":
            "Very Active",

        "maintain":
            "Maintain Weight",

        "lose":
            "Lose Weight",

        "gain":
            "Gain Weight",

        "protein":
            "Protein",

        "carbs":
            "Carbohydrates",

        "fat":
            "Fat",

        "diabetes_center":
            "Glucose Monitoring Center",

        "glucose":
            "Glucose (mg/dL)",

        "measurement":
            "Measurement Context",

        "fasting":
            "Fasting",

        "before_meal":
            "Before Meal",

        "after_1h":
            "1 Hour After Meal",

        "after_2h":
            "2 Hours After Meal",

        "bedtime":
            "Bedtime",

        "meal":
            "Meal / Note",

        "save_glucose":
            "Save Glucose Reading",

        "health_search":
            "Health Search",

        "search_type":
            "Search Type",

        "disease":
            "Search by Disease",

        "symptoms":
            "Search by Symptoms",

        "search":
            "Search",

        "how":
            "How Waqaya Works",
    },
}


def t(key):
    language = "ar" if AR else "en"
    return TEXT[language].get(key, key)


# ============================================================
# HTML HELPER
# Prevents Streamlit from displaying card HTML as plain text
# ============================================================

def ui(html):
    clean_html = "\n".join(
        line.strip()
        for line in html.splitlines()
    )

    st.markdown(
        clean_html,
        unsafe_allow_html=True
    )


# ============================================================
# GLOBAL DESIGN SYSTEM
# ============================================================

ui("""
<style>

:root {
    --navy: #07182d;
    --navy-soft: #0c2743;
    --navy-light: #123653;

    --green: #22a889;
    --green-light: #58cbb3;

    --orange: #df603d;

    --paper: #f5f8f7;
    --white: #ffffff;

    --text: #112235;
    --muted: #73828c;
    --line: #e6ece9;
}


/* ----------------------------------------------------------
   GLOBAL
---------------------------------------------------------- */

html,
body,
[class*="css"] {
    font-family:
        "Segoe UI",
        Tahoma,
        Arial,
        sans-serif;
}


.stApp {

    background:

        radial-gradient(
            circle at 92% 4%,
            rgba(34, 168, 137, 0.07),
            transparent 26%
        ),

        #f5f8f7;

    color: var(--text);
}


.block-container {

    max-width: 1280px;

    padding-top: 1.5rem;

    padding-bottom: 4rem;
}


/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

[data-testid="stSidebar"] {

    background:

        radial-gradient(
            circle at 15% 15%,
            rgba(45, 180, 145, 0.12),
            transparent 32%
        ),

        linear-gradient(
            180deg,
            #08192e 0%,
            #061321 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.06);
}


[data-testid="stSidebar"] * {
    color: #f5f7fa;
}


[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 600;
}


[data-testid="stSidebar"] input {

    color: #102033 !important;

    background:
        #f5f7f6 !important;
}


[data-testid="stSidebar"] hr {

    border-color:
        rgba(255,255,255,0.12);
}


/* ----------------------------------------------------------
   BUTTONS
---------------------------------------------------------- */

.stButton > button {

    min-height: 48px;

    border-radius: 11px;

    border: 0;

    font-weight: 700;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.stButton > button:hover {

    transform:
        translateY(-1px);

    box-shadow:
        0 8px 22px
        rgba(20,40,60,0.10);
}


.stButton > button[kind="primary"] {

    background:

        linear-gradient(
            90deg,
            #1ea789,
            #45c5ad
        );

    color: white;
}


[data-testid="stSidebar"]
.stButton > button {

    background:

        linear-gradient(
            90deg,
            #d84e31,
            #f26b42
        ) !important;

    color: #ffffff !important;

    width: 100%;
}


/* ----------------------------------------------------------
   FORM CONTROLS
---------------------------------------------------------- */

div[data-baseweb="select"] > div,

[data-testid="stNumberInput"] input,

[data-testid="stTextInput"] input {

    border-radius: 10px;
}


/* ----------------------------------------------------------
   DIVIDER
---------------------------------------------------------- */

hr {

    border: none;

    border-top:
        1px solid #e7ecea;

    margin:
        34px 0;
}


/* ----------------------------------------------------------
   HERO
---------------------------------------------------------- */

.waqaya-hero {

    background:

        radial-gradient(
            circle at 92% 20%,
            rgba(47,174,142,0.22),
            transparent 28%
        ),

        linear-gradient(
            115deg,
            #07162b 0%,
            #0a1d37 62%,
            #12382f 130%
        );

    border-radius: 25px;

    padding:
        58px 64px;

    color: white;

    box-shadow:
        0 20px 55px
        rgba(7,23,45,0.13);

    margin:
        15px 0 32px;

    position: relative;

    overflow: hidden;
}


.hero-tag {

    color:
        #69d1b7;

    font-size:
        0.78rem;

    font-weight:
        800;

    letter-spacing:
        0.08em;

    margin-bottom:
        18px;
}


.hero-title {

    font-size:
        2.45rem;

    line-height:
        1.45;

    font-weight:
        800;

    max-width:
        900px;
}


.hero-desc {

    margin-top:
        15px;

    color:
        #dce7ec;

    font-size:
        1rem;

    line-height:
        1.9;

    max-width:
        900px;
}


.tech-pill {

    display:
        inline-block;

    margin-top:
        22px;

    background:
        rgba(70,167,210,0.13);

    border:
        1px solid
        rgba(120,205,230,0.18);

    border-radius:
        999px;

    padding:
        9px 16px;

    color:
        #dbeef4;

    font-size:
        0.82rem;
}


/* ----------------------------------------------------------
   SECTIONS
---------------------------------------------------------- */

.section-title {

    font-size:
        1.8rem;

    font-weight:
        800;

    color:
        #102033;

    margin:
        10px 0 5px;
}


.section-sub {

    color:
        #7a8792;

    margin-bottom:
        22px;

    font-size:
        0.92rem;

    line-height:
        1.7;
}


/* ----------------------------------------------------------
   CARDS
---------------------------------------------------------- */

.metric-card,
.risk-card,
.info-panel {

    background:
        #ffffff;

    border:
        1px solid #edf0ef;

    border-radius:
        18px;

    padding:
        22px;

    box-shadow:
        0 8px 28px
        rgba(20,40,60,0.045);
}


.metric-card {
    min-height:
        142px;
}


.risk-card {
    min-height:
        150px;
}


.metric-label {

    color:
        #7d8994;

    font-size:
        0.78rem;

    text-transform:
        uppercase;

    letter-spacing:
        0.04em;
}


.metric-value {

    color:
        #102033;

    font-size:
        1.75rem;

    font-weight:
        800;

    margin-top:
        14px;
}


.metric-note {

    color:
        #80908a;

    font-size:
        0.78rem;

    margin-top:
        7px;
}


.risk-name {

    color:
        #52616c;

    font-size:
        0.88rem;
}


.risk-value {

    font-size:
        1.85rem;

    font-weight:
        800;

    color:
        #102033;

    margin:
        10px 0;
}


/* ----------------------------------------------------------
   PROGRESS
---------------------------------------------------------- */

.progress-track {

    height:
        7px;

    border-radius:
        99px;

    background:
        #e8eeec;

    overflow:
        hidden;
}


.progress-fill {

    height:
        100%;

    border-radius:
        99px;

    background:

        linear-gradient(
            90deg,
            #278c75,
            #47c5ad
        );
}


/* ----------------------------------------------------------
   DARK INTELLIGENCE PANEL
---------------------------------------------------------- */

.dark-panel {

    background:

        linear-gradient(
            120deg,
            #07172d,
            #0b213b
        );

    color:
        white;

    border-radius:
        23px;

    padding:
        34px;

    margin-top:
        15px;
}


.dark-panel h2,
.dark-panel h3 {

    color:
        white;
}


.dark-muted {

    color:
        #c8d4dc;

    line-height:
        1.8;
}


/* ----------------------------------------------------------
   NOTICE
---------------------------------------------------------- */

.notice {

    background:
        #eef8f5;

    border-left:
        4px solid #2aa889;

    border-radius:
        10px;

    padding:
        15px 18px;

    color:
        #38524c;

    font-size:
        0.87rem;

    line-height:
        1.7;
}


/* ----------------------------------------------------------
   WAQAYA INTELLIGENCE SIGNAL
---------------------------------------------------------- */

.signal {

    background:

        linear-gradient(
            135deg,
            #07172d,
            #12382f
        );

    border-radius:
        20px;

    padding:
        26px;

    color:
        white;

    min-height:
        170px;
}


.signal .big {

    font-size:
        2.2rem;

    font-weight:
        800;

    margin:
        12px 0;
}


.signal .small {

    color:
        #c8d9d4;

    font-size:
        0.85rem;

    line-height:
        1.7;
}


/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.footer {

    text-align:
        center;

    padding:
        35px 10px 10px;

    color:
        #8b979e;

    font-size:
        0.8rem;
}


/* ----------------------------------------------------------
   MOBILE
---------------------------------------------------------- */

@media(max-width:800px) {

    .waqaya-hero {

        padding:
            35px 25px;
    }

    .hero-title {

        font-size:
            1.75rem;
    }

}

</style>
""")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_bmi(weight, height_cm):

    if height_cm <= 0:
        return 0

    height_m = height_cm / 100

    return round(
        weight / (height_m ** 2),
        1
    )


def bmi_category(bmi):

    if bmi < 18.5:

        return (
            "نقص وزن"
            if AR
            else "Underweight"
        )

    if bmi < 25:

        return (
            "طبيعي"
            if AR
            else "Normal"
        )

    if bmi < 30:

        return (
            "زيادة وزن"
            if AR
            else "Overweight"
        )

    return (
        "سمنة"
        if AR
        else "Obesity"
    )


def risk_percent(value):

    try:

        value = float(value)

        if value <= 1:
            value *= 100

        return int(
            max(
                0,
                min(
                    100,
                    round(value)
                )
            )
        )

    except Exception:

        return 0


def risk_level(value):

    if value < 30:
        return t("low")

    if value < 60:
        return t("moderate")

    return t("high")


FEATURE_LABELS_AR = {

    "heart_rate":
        "نبض القلب",

    "spo2":
        "تشبع الأكسجين",

    "sleep_hours":
        "النوم",

    "steps":
        "الخطوات",

    "water_liters":
        "استهلاك الماء",

    "systolic_bp":
        "الضغط الانقباضي",

    "diastolic_bp":
        "الضغط الانبساطي",

    "age":
        "العمر",

    "gender":
        "الجنس",

    "bmi":
        "مؤشر كتلة الجسم",

    "urination":
        "عدد مرات التبول",
}


def feature_label(feature):

    if AR:

        return FEATURE_LABELS_AR.get(
            feature,
            feature.replace("_", " ")
        )

    return feature.replace(
        "_",
        " "
    ).title()


# ============================================================
# LANGUAGE SWITCH
# ============================================================

language_space, language_column = st.columns(
    [5, 1]
)

with language_column:

    selected_language = st.selectbox(

        t("language"),

        [
            "العربية",
            "English"
        ],

        index=(
            0
            if st.session_state.language == "العربية"
            else 1
        ),

        key="language_selector"
    )


if selected_language != st.session_state.language:

    st.session_state.language = selected_language

    st.rerun()
    # ============================================================
# SPLASH SCREEN
# ============================================================

if not st.session_state.splash_done:

    ui(f"""
    <div class="waqaya-hero"
         style="min-height:520px;display:flex;align-items:center;">

        <div>

            <div class="hero-tag">
                PREVENTIVE HEALTH INTELLIGENCE
            </div>

            <div class="hero-title"
                 style="font-size:3.5rem;">
                وقاية
            </div>

            <div style="
                font-size:2rem;
                font-weight:800;
                margin-top:4px;
            ">
                Waqaya AI
            </div>

            <div style="
                font-size:1.4rem;
                font-weight:700;
                margin-top:30px;
            ">
                {
                    "منصة ذكية للوقاية الصحية المبنية على البيانات"
                    if AR
                    else
                    "Data-Driven Preventive Health Intelligence"
                }
            </div>

            <div class="hero-desc">
                {
                    "تحليل المؤشرات الصحية، اكتشاف الأنماط المبكرة "
                    "وتحويل البيانات اليومية إلى رؤى وقائية أكثر وضوحًا."
                    if AR
                    else
                    "Analyze health indicators, identify early patterns "
                    "and transform everyday data into preventive insights."
                }
            </div>

            <div class="tech-pill">
                Machine Learning • Personal Baseline •
                Anomaly Detection • Explainable AI
            </div>

        </div>

    </div>
    """)

    if st.button(
        t("start"),
        type="primary",
        use_container_width=True
    ):

        st.session_state.splash_done = True
        st.rerun()

    st.stop()


# ============================================================
# HEALTH PROFILE
# ============================================================

if not st.session_state.profile_completed:

    ui(f"""
    <div class="waqaya-hero">

        <div class="hero-tag">
            WAQAYA HEALTH PROFILE
        </div>

        <div class="hero-title">
            {t("profile_title")}
        </div>

        <div class="hero-desc">
            {t("profile_desc")}
        </div>

    </div>
    """)

    left, right = st.columns(2)

    with left:

        name = st.text_input(
            t("name")
        )

        age = st.number_input(
            t("age"),
            min_value=12,
            max_value=100,
            value=25
        )

        weight = st.number_input(
            t("weight"),
            min_value=25.0,
            max_value=250.0,
            value=60.0,
            step=0.5
        )

        diabetic = st.radio(
            t("diabetes"),
            [
                t("no"),
                t("yes")
            ],
            horizontal=True
        )

    with right:

        gender = st.selectbox(
            t("gender"),
            [
                t("female"),
                t("male")
            ]
        )

        height = st.number_input(
            t("height"),
            min_value=120.0,
            max_value=220.0,
            value=165.0,
            step=1.0
        )

        wearable = st.radio(
            t("wearable"),
            [
                t("no"),
                t("yes")
            ],
            horizontal=True
        )

        wearable_type = None

        if wearable == t("yes"):

            wearable_type = st.selectbox(
                t("wearable_type"),
                [
                    t("watch"),
                    t("ring"),
                    t("both")
                ]
            )

    bmi = calculate_bmi(
        weight,
        height
    )

    ui(f"""
    <div class="info-panel"
         style="margin-top:20px;">

        <div class="metric-label">
            {t("bmi")}
        </div>

        <div class="metric-value">
            {bmi}
        </div>

        <div class="metric-note">
            {bmi_category(bmi)}
        </div>

    </div>
    """)

    if st.button(
        t("create"),
        type="primary",
        use_container_width=True
    ):

        if not name.strip():

            st.warning(
                "يرجى إدخال الاسم."
                if AR
                else
                "Please enter your name."
            )

            st.stop()

        st.session_state.user_profile = {

            "name":
                name.strip(),

            "age":
                int(age),

            "gender":
                gender,

            "weight":
                float(weight),

            "height":
                float(height),

            "bmi":
                float(bmi),

            "diabetic":
                diabetic == t("yes"),

            "wearable":
                wearable == t("yes"),

            "wearable_type":
                wearable_type
        }

        st.session_state.profile_completed = True

        st.rerun()

    st.stop()


# ============================================================
# LOAD PROFILE
# ============================================================

profile = st.session_state.user_profile


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# Waqaya AI")

    st.caption(
        "Preventive Health Intelligence"
    )

    st.markdown("---")

    st.markdown(
        f"### {t('personal')}"
    )

    st.caption(
        f"{profile['name']} · "
        f"{profile['age']} · "
        f"BMI {profile['bmi']}"
    )

    st.markdown("---")

    st.markdown(
        f"### {t('vitals')}"
    )

    systolic = st.number_input(
        t("systolic"),
        min_value=70,
        max_value=220,
        value=120,
        key="sys"
    )

    diastolic = st.number_input(
        t("diastolic"),
        min_value=40,
        max_value=140,
        value=80,
        key="dia"
    )

    heart_rate = st.number_input(
        t("heart"),
        min_value=35,
        max_value=200,
        value=75,
        key="hr"
    )

    spo2 = st.number_input(
        t("spo2"),
        min_value=70.0,
        max_value=100.0,
        value=98.0,
        step=0.1,
        key="spo2"
    )

    st.markdown(
        f"### {t('lifestyle')}"
    )

    sleep_hours = st.number_input(
        t("sleep"),
        min_value=0.0,
        max_value=15.0,
        value=7.0,
        step=0.5,
        key="sleep"
    )

    steps = st.number_input(
        t("steps"),
        min_value=0,
        max_value=60000,
        value=7000,
        step=500,
        key="steps"
    )

    water_liters = st.number_input(
        t("water"),
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.25,
        key="water"
    )

    urination = st.number_input(
        t("urination"),
        min_value=0,
        max_value=30,
        value=6,
        key="urination"
    )

    st.metric(
        t("bmi"),
        profile["bmi"]
    )

    analyze_clicked = st.button(
        t("analyze"),
        type="primary",
        use_container_width=True
    )


# ============================================================
# BUILD MODEL INPUT
# ============================================================

gender_numeric = (
    0
    if profile["gender"] in [
        "أنثى",
        "Female"
    ]
    else 1
)


current_data = {

    "age":
        profile["age"],

    "gender":
        gender_numeric,

    "systolic_bp":
        systolic,

    "diastolic_bp":
        diastolic,

    "heart_rate":
        heart_rate,

    "spo2":
        spo2,

    "sleep_hours":
        sleep_hours,

    "steps":
        steps,

    "water_liters":
        water_liters,

    "urination":
        urination,

    "bmi":
        profile["bmi"]
}


st.session_state.current_data = current_data


# ============================================================
# LOAD WAQAYA ENGINE
# ============================================================

@st.cache_resource
def load_engine():

    return WaqayaEngine(
        "waqaya_models.pkl"
    )


try:

    engine = load_engine()

except Exception as error:

    st.error(
        (
            "تعذر تحميل نموذج وقاية: "
            if AR
            else
            "Unable to load Waqaya model: "
        )
        + str(error)
    )

    st.stop()


# ============================================================
# PROTOTYPE REFERENCE HISTORY
#
# Important:
# This is simulated reference history used to demonstrate
# the Personal Baseline mechanism.
#
# It must NOT be presented as real wearable/user history.
# ============================================================

def build_reference_history(current):

    rng = np.random.default_rng(42)

    rows = []

    for day in range(14):

        rows.append({

            "age":
                current["age"],

            "gender":
                current["gender"],

            "systolic_bp":
                current["systolic_bp"]
                + rng.normal(0, 4),

            "diastolic_bp":
                current["diastolic_bp"]
                + rng.normal(0, 3),

            "heart_rate":
                current["heart_rate"]
                + rng.normal(0, 4),

            "spo2":
                np.clip(
                    current["spo2"]
                    + rng.normal(0, 0.45),
                    70,
                    100
                ),

            "sleep_hours":
                max(
                    0,
                    current["sleep_hours"]
                    + rng.normal(0, 0.45)
                ),

            "steps":
                max(
                    0,
                    current["steps"]
                    + rng.normal(0, 700)
                ),

            "water_liters":
                max(
                    0,
                    current["water_liters"]
                    + rng.normal(0, 0.18)
                ),

            "urination":
                max(
                    0,
                    current["urination"]
                    + rng.normal(0, 0.7)
                ),

            "bmi":
                current["bmi"]
        })

    return pd.DataFrame(rows)


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_clicked:

    history = build_reference_history(
        current_data
    )

    try:

        st.session_state.analysis = engine.analyze(

            current_data=current_data,

            history=history
        )

        st.session_state.history = history

        st.session_state.analysis_completed = True

    except Exception as error:

        st.error(
            (
                "حدث خطأ أثناء تحليل الملف الصحي: "
                if AR
                else
                "An error occurred during analysis: "
            )
            + str(error)
        )

        st.stop()


# ============================================================
# MAIN HERO
# ============================================================

st.caption(
    "Waqaya AI · Preventive Health Intelligence"
)


ui(f"""
<div class="waqaya-hero">

    <div class="hero-tag">
        {t("hero_tag")}
    </div>

    <div class="hero-title">
        {t("hero_title")}
    </div>

    <div class="hero-desc">
        {t("hero_desc")}
    </div>

    <div class="tech-pill">
        Machine Learning •
        Personal Baseline •
        Anomaly Detection •
        Explainable AI
    </div>

</div>
""")


# ============================================================
# WAIT FOR FIRST ANALYSIS
# ============================================================

if not st.session_state.analysis_completed:

    ui(f"""
    <div class="dark-panel">

        <div style="
            color:#62cdb5;
            font-size:0.78rem;
            font-weight:800;
        ">
            WAQAYA AI
        </div>

        <h2>
            {t("ready")}
        </h2>

        <div class="dark-muted">
            {t("ready_desc")}
        </div>

    </div>
    """)

    st.stop()


analysis = (
    st.session_state.analysis
    or {}
)

history = (
    st.session_state.history
)


# ============================================================
# IMPORTANT MODEL CONNECTION
#
# waqaya_engine.py returns:
#     risk_predictions
#
# not:
#     risks
#
# This connects the dashboard to actual model output.
# ============================================================

risks = analysis.get(
    "risk_predictions",
    analysis.get(
        "risks",
        {}
    )
)


def model_risk(name):

    return risk_percent(
        risks.get(
            name,
            0
        )
    )


diabetes_risk = model_risk(
    "diabetes_risk"
)

cardio_risk = model_risk(
    "cardio_risk"
)

resp_risk = model_risk(
    "respiratory_risk"
)

dehydration_risk = model_risk(
    "dehydration_risk"
)


early_score = risk_percent(
    analysis.get(
        "early_risk_score",
        0
    )
)


anomaly = (
    analysis.get(
        "anomaly",
        {}
    )
    or {}
)


if isinstance(
    anomaly,
    dict
):

    anomaly_detected = bool(
        anomaly.get(
            "is_anomaly",
            False
        )
    )

    anomaly_score = risk_percent(
        anomaly.get(
            "score",
            0
        )
    )

else:

    anomaly_detected = bool(
        anomaly
    )

    anomaly_score = 0


baseline = (
    analysis.get(
        "baseline",
        {}
    )
    or {}
)


deviations = (
    analysis.get(
        "baseline_deviation",
        {}
    )
    or {}
)


trends = (
    analysis.get(
        "trends",
        {}
    )
    or {}
)
# ============================================================
# WAQAYA INTELLIGENCE CENTER
# ============================================================

ui(f"""
<div class="section-title">
    {t("intelligence")}
</div>

<div class="section-sub">
    {t("intelligence_desc")}
</div>
""")


metric_columns = st.columns(4)


intelligence_cards = [

    (
        t("risk_score"),
        f"{early_score}%",
        risk_level(early_score)
    ),

    (
        t("anomaly"),
        f"{anomaly_score}%",
        (
            t("detected")
            if anomaly_detected
            else t("stable")
        )
    ),

    (
        t("status"),
        (
            t("detected")
            if anomaly_detected
            else t("stable")
        ),
        (
            "Preventive Intelligence"
        )
    ),

    (
        t("indicators"),
        "11",
        (
            "Health Data Features"
        )
    )
]


for column, card in zip(
    metric_columns,
    intelligence_cards
):

    label, value, note = card

    with column:

        ui(f"""
        <div class="metric-card">

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-note">
                {note}
            </div>

        </div>
        """)


# ============================================================
# INTELLIGENCE SUMMARY
# ============================================================

if deviations:

    largest_deviation = max(

        deviations.items(),

        key=lambda item:
            abs(
                float(
                    item[1]
                )
            )
    )

else:

    largest_deviation = (
        None,
        0
    )


largest_feature = (
    feature_label(
        largest_deviation[0]
    )
    if largest_deviation[0]
    else (
        "لا يوجد"
        if AR
        else "None"
    )
)


largest_change = float(
    largest_deviation[1]
)


if anomaly_detected:

    anomaly_sentence = (
        "تم رصد نمط غير اعتيادي "
        "يستحق المتابعة."
        if AR
        else
        "An unusual pattern was detected "
        "and may deserve monitoring."
    )

else:

    anomaly_sentence = (
        "لا توجد إشارة شذوذ واضحة حاليًا."
        if AR
        else
        "No clear anomaly signal is "
        "currently detected."
    )


ui(f"""
<div class="signal"
     style="margin-top:22px;">

    <div style="
        color:#62cdb5;
        font-weight:800;
        font-size:0.78rem;
    ">
        WAQAYA INTELLIGENCE SUMMARY
    </div>

    <div class="big">
        {risk_level(early_score)}
        ·
        {early_score}/100
    </div>

    <div class="small">

        {
            "أكبر تغير عن خط الأساس:"
            if AR
            else
            "Largest baseline change:"
        }

        <strong>
            {largest_feature}
        </strong>

        ({largest_change:+.1f}%)

        <br><br>

        {anomaly_sentence}

    </div>

</div>
""")


# ============================================================
# WAQAYA EARLY SCORE GAUGE
# ============================================================

gauge = go.Figure(

    go.Indicator(

        mode=
            "gauge+number",

        value=
            early_score,

        number={
            "suffix": "%",
            "font": {
                "size": 38
            }
        },

        title={
            "text":
                t("risk_score")
        },

        gauge={

            "axis": {
                "range": [
                    0,
                    100
                ]
            },

            "bar": {
                "color":
                    "#0a1d37"
            },

            "steps": [

                {
                    "range": [
                        0,
                        30
                    ],

                    "color":
                        "#dcece7"
                },

                {
                    "range": [
                        30,
                        60
                    ],

                    "color":
                        "#eee8d7"
                },

                {
                    "range": [
                        60,
                        100
                    ],

                    "color":
                        "#eeddd8"
                }
            ]
        }
    )
)


gauge.update_layout(

    height=330,

    margin=dict(
        l=35,
        r=35,
        t=60,
        b=20
    ),

    paper_bgcolor=
        "rgba(0,0,0,0)"
)


st.plotly_chart(
    gauge,
    use_container_width=True
)


# ============================================================
# MACHINE LEARNING RISK ESTIMATES
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("risk_analysis")}
</div>

<div class="section-sub">
    {t("risk_desc")}
</div>
""")


risk_items = [

    (
        t("diabetes_risk"),
        diabetes_risk
    ),

    (
        t("cardio"),
        cardio_risk
    ),

    (
        t("respiratory"),
        resp_risk
    ),

    (
        t("dehydration"),
        dehydration_risk
    )
]


risk_columns = st.columns(4)


for column, item in zip(
    risk_columns,
    risk_items
):

    label, value = item

    with column:

        ui(f"""
        <div class="risk-card">

            <div class="risk-name">
                {label}
            </div>

            <div class="risk-value">
                {value}%
            </div>

            <div class="progress-track">

                <div
                    class="progress-fill"
                    style="width:{value}%">
                </div>

            </div>

            <div class="metric-note">
                {risk_level(value)}
            </div>

        </div>
        """)


risk_dataframe = pd.DataFrame({

    "Category":
        [
            item[0]
            for item
            in risk_items
        ],

    "Risk":
        [
            item[1]
            for item
            in risk_items
        ]
})


risk_chart = px.bar(

    risk_dataframe,

    x="Category",

    y="Risk",

    text="Risk"
)


risk_chart.update_traces(

    marker_color=
        "#278c75",

    texttemplate=
        "%{text}%",

    textposition=
        "outside"
)


risk_chart.update_layout(

    height=360,

    yaxis_range=[
        0,
        100
    ],

    xaxis_title="",

    yaxis_title=
        "Risk %",

    paper_bgcolor=
        "rgba(0,0,0,0)",

    plot_bgcolor=
        "rgba(0,0,0,0)",

    showlegend=False
)


st.plotly_chart(

    risk_chart,

    use_container_width=True
)


# ============================================================
# PERSONAL HEALTH BASELINE
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("baseline")}
</div>

<div class="section-sub">
    {t("baseline_desc")}
</div>
""")


baseline_features = [

    "systolic_bp",

    "diastolic_bp",

    "heart_rate",

    "spo2",

    "sleep_hours",

    "steps",

    "water_liters"
]


baseline_rows = []


for feature in baseline_features:

    current_value = float(
        current_data[feature]
    )

    baseline_value = float(
        baseline.get(
            feature,
            current_value
        )
    )

    deviation_value = float(
        deviations.get(
            feature,
            0
        )
    )

    baseline_rows.append({

        (
            "المؤشر"
            if AR
            else
            "Indicator"
        ):
            feature_label(feature),

        (
            "خط الأساس"
            if AR
            else
            "Baseline"
        ):
            round(
                baseline_value,
                2
            ),

        (
            "الحالي"
            if AR
            else
            "Current"
        ):
            round(
                current_value,
                2
            ),

        (
            "التغير %"
            if AR
            else
            "Deviation %"
        ):
            round(
                deviation_value,
                2
            )
    })


baseline_dataframe = pd.DataFrame(
    baseline_rows
)


st.dataframe(

    baseline_dataframe,

    use_container_width=True,

    hide_index=True
)


# ============================================================
# BASELINE COMPARISON CHART
# ============================================================

baseline_chart_features = [

    "systolic_bp",

    "diastolic_bp",

    "heart_rate",

    "spo2",

    "sleep_hours",

    "water_liters"
]


comparison_rows = []


for feature in baseline_chart_features:

    comparison_rows.append({

        "Indicator":
            feature_label(feature),

        "Baseline":
            float(
                baseline.get(
                    feature,
                    current_data[feature]
                )
            ),

        "Current":
            float(
                current_data[feature]
            )
    })


comparison_dataframe = pd.DataFrame(
    comparison_rows
)


comparison_chart = go.Figure()


comparison_chart.add_trace(

    go.Bar(

        name=
            (
                "خط الأساس"
                if AR
                else
                "Baseline"
            ),

        x=
            comparison_dataframe[
                "Indicator"
            ],

        y=
            comparison_dataframe[
                "Baseline"
            ]
    )
)


comparison_chart.add_trace(

    go.Bar(

        name=
            (
                "الحالي"
                if AR
                else
                "Current"
            ),

        x=
            comparison_dataframe[
                "Indicator"
            ],

        y=
            comparison_dataframe[
                "Current"
            ]
    )
)


comparison_chart.update_layout(

    barmode=
        "group",

    height=
        390,

    paper_bgcolor=
        "rgba(0,0,0,0)",

    plot_bgcolor=
        "rgba(0,0,0,0)",

    legend_title_text=""
)


st.plotly_chart(

    comparison_chart,

    use_container_width=True
)


# ============================================================
# SCIENTIFIC TRANSPARENCY
# ============================================================

if AR:

    ui("""
    <div class="notice">

        خط الأساس في النموذج الأولي الحالي مبني على
        سجل مرجعي محاكى لشرح آلية Personal Baseline.

        في النسخة التشغيلية المستقبلية يمكن بناء
        خط الأساس من السجل الحقيقي للمستخدم أو
        بيانات الأجهزة القابلة للارتداء.

    </div>
    """)

else:

    ui("""
    <div class="notice">

        The current prototype baseline uses simulated
        reference history to demonstrate the Personal
        Baseline mechanism.

        A production version can learn the baseline from
        real longitudinal user or wearable data.

    </div>
    """)


# ============================================================
# WHY DID WAQAYA CHANGE?
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("why")}
</div>

<div class="section-sub">
    {t("why_desc")}
</div>
""")


sorted_deviations = sorted(

    deviations.items(),

    key=lambda item:
        abs(
            float(
                item[1]
            )
        ),

    reverse=True
)


if sorted_deviations:

    why_columns = st.columns(3)

    for index, item in enumerate(
        sorted_deviations[:3]
    ):

        feature, deviation = item

        deviation = float(
            deviation
        )

        if AR:

            direction = (
                "أعلى من خط الأساس"
                if deviation > 0
                else
                "أقل من خط الأساس"
            )

        else:

            direction = (
                "Above baseline"
                if deviation > 0
                else
                "Below baseline"
            )

        with why_columns[index]:

            ui(f"""
            <div class="info-panel"
                 style="min-height:155px;">

                <div class="metric-label">
                    {feature_label(feature)}
                </div>

                <div class="metric-value">
                    {abs(deviation):.1f}%
                </div>

                <div class="metric-note">
                    {direction}
                </div>

            </div>
            """)

else:

    st.info(
        "لا توجد انحرافات كافية لعرضها."
        if AR
        else
        "No baseline deviations are available."
    )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("performance")}
</div>

<div class="section-sub">
    {t("performance_desc")}
</div>
""")


metrics = (
    getattr(
        engine,
        "metrics",
        {}
    )
    or {}
)


metric_rows = []


if isinstance(
    metrics,
    dict
):

    for model_name, model_metrics in metrics.items():

        if isinstance(
            model_metrics,
            dict
        ):

            row = {
                "Model":
                    str(
                        model_name
                    )
            }

            for metric_name, metric_value in model_metrics.items():

                if isinstance(
                    metric_value,
                    (
                        int,
                        float,
                        np.integer,
                        np.floating
                    )
                ):

                    row[
                        str(metric_name)
                    ] = float(
                        metric_value
                    )

            if len(row) > 1:

                metric_rows.append(
                    row
                )

        elif isinstance(
            model_metrics,
            (
                int,
                float,
                np.integer,
                np.floating
            )
        ):

            metric_rows.append({

                "Metric":
                    str(
                        model_name
                    ),

                "Value":
                    float(
                        model_metrics
                    )
            })


if metric_rows:

    metrics_dataframe = pd.DataFrame(
        metric_rows
    )

    st.dataframe(

        metrics_dataframe,

        use_container_width=True,

        hide_index=True
    )

else:

    st.info(

        (
            "لا توجد مقاييس تقييم محفوظة داخل "
            "حزمة النموذج الحالية، لذلك لن تعرض "
            "وقاية أرقام أداء غير موثقة."
        )

        if AR

        else

        (
            "No evaluation metrics are stored in "
            "the current model package, so Waqaya "
            "will not display undocumented scores."
        )
    )


# ============================================================
# EXPLAINABLE AI
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("explain")}
</div>

<div class="section-sub">
    {t("explain_desc")}
</div>
""")


feature_importance = analysis.get(
    "feature_importance",
    None
)


if feature_importance is None:

    try:

        feature_importance = (
            engine.get_feature_importance()
        )

    except Exception:

        feature_importance = None


feature_dataframe = None


if isinstance(
    feature_importance,
    pd.DataFrame
):

    feature_dataframe = (
        feature_importance.copy()
    )


elif isinstance(
    feature_importance,
    dict
) and feature_importance:

    if all(
        isinstance(
            value,
            dict
        )
        for value
        in feature_importance.values()
    ):

        aggregate = {}

        for inner_dictionary in feature_importance.values():

            for feature, importance in inner_dictionary.items():

                if isinstance(
                    importance,
                    (
                        int,
                        float,
                        np.integer,
                        np.floating
                    )
                ):

                    aggregate[feature] = (
                        aggregate.get(
                            feature,
                            0
                        )
                        +
                        float(
                            importance
                        )
                    )

        feature_importance = aggregate


    if isinstance(
        feature_importance,
        dict
    ):

        feature_dataframe = pd.DataFrame(

            list(
                feature_importance.items()
            ),

            columns=[
                "Feature",
                "Importance"
            ]
        )


if (
    feature_dataframe is not None
    and
    not feature_dataframe.empty
):

    feature_dataframe = (
        feature_dataframe.iloc[
            :,
            :2
        ].copy()
    )

    feature_dataframe.columns = [
        "Feature",
        "Importance"
    ]

    feature_dataframe[
        "Importance"
    ] = pd.to_numeric(

        feature_dataframe[
            "Importance"
        ],

        errors="coerce"
    )


    feature_dataframe = (
        feature_dataframe.dropna()
    )


    feature_dataframe[
        "Feature"
    ] = feature_dataframe[
        "Feature"
    ].map(
        feature_label
    )


    feature_dataframe = (

        feature_dataframe

        .sort_values(
            "Importance"
        )

        .tail(10)
    )


    explain_chart = px.bar(

        feature_dataframe,

        x=
            "Importance",

        y=
            "Feature",

        orientation=
            "h"
    )


    explain_chart.update_traces(

        marker_color=
            "#0b213c"
    )


    explain_chart.update_layout(

        height=
            430,

        paper_bgcolor=
            "rgba(0,0,0,0)",

        plot_bgcolor=
            "rgba(0,0,0,0)"
    )


    st.plotly_chart(

        explain_chart,

        use_container_width=True
    )


else:

    st.info(

        (
            "أهمية الخصائص غير متاحة "
            "للنماذج الحالية."
        )

        if AR

        else

        (
            "Feature importance is not "
            "available for the current models."
        )
    )
    # ============================================================
# EARLY-WARNING COMPETITION DEMO
# ============================================================

st.markdown("---")


ui(f"""
<div class="dark-panel">

    <div style="
        color:#62cdb5;
        font-size:0.78rem;
        font-weight:800;
    ">
        COMPETITION DEMO
    </div>

    <h2>
        {t("demo")}
    </h2>

    <div class="dark-muted">
        {t("demo_desc")}
    </div>

</div>
""")


if st.button(
    t("run_demo"),
    type="primary",
    use_container_width=True
):

    demo_dataframe = pd.DataFrame({

        "Day": [
            "D1",
            "D2",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
            "D8",
            "D9",
            "D10"
        ],

        "Sleep": [
            7.7,
            7.5,
            7.6,
            7.4,
            7.3,
            6.8,
            6.2,
            5.7,
            5.2,
            4.9
        ],

        "Heart Rate": [
            72,
            73,
            72,
            74,
            73,
            77,
            80,
            84,
            88,
            91
        ],

        "Steps": [
            8200,
            8500,
            7900,
            8300,
            8100,
            7200,
            6400,
            5500,
            4300,
            3600
        ],

        "Waqaya Score": [
            12,
            13,
            12,
            15,
            14,
            22,
            31,
            43,
            59,
            71
        ]
    })


    demo_chart = px.line(

        demo_dataframe,

        x="Day",

        y="Waqaya Score",

        markers=True
    )


    demo_chart.add_hline(

        y=30,

        line_dash="dash",

        annotation_text=
            (
                "بداية التغير"
                if AR
                else
                "Change Signal"
            )
    )


    demo_chart.add_hline(

        y=60,

        line_dash="dash",

        annotation_text=
            (
                "إشارة مرتفعة"
                if AR
                else
                "High Signal"
            )
    )


    demo_chart.update_traces(

        line_color=
            "#14866d",

        marker_color=
            "#0b213c"
    )


    demo_chart.update_layout(

        height=
            390,

        yaxis_range=[
            0,
            100
        ],

        paper_bgcolor=
            "rgba(0,0,0,0)",

        plot_bgcolor=
            "rgba(0,0,0,0)"
    )


    st.plotly_chart(

        demo_chart,

        use_container_width=True
    )


    demo_column_1, \
    demo_column_2, \
    demo_column_3 = st.columns(3)


    demo_column_1.metric(

        t("sleep"),

        "4.9 h",

        "-2.8 h"
    )


    demo_column_2.metric(

        t("heart"),

        "91 bpm",

        "+19 bpm"
    )


    demo_column_3.metric(

        t("steps"),

        "3,600",

        "-4,600"
    )


    if AR:

        st.info(
            "هذه محاكاة توضيحية لشرح فكرة "
            "الإنذار المبكر، وليست نتيجة سريرية "
            "أو بيانات مستخدم حقيقية."
        )

    else:

        st.info(
            "This is an illustrative simulation "
            "of the early-warning concept, not a "
            "clinical result or real user data."
        )


# ============================================================
# PREVENTIVE INSIGHTS
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("insights")}
</div>
""")


preventive_insights = []


if steps < 6000:

    preventive_insights.append(

        (
            "نشاطك اليومي منخفض نسبيًا. "
            "الزيادة التدريجية في الحركة قد "
            "تدعم الصحة العامة."
        )

        if AR

        else

        (
            "Daily activity is relatively low. "
            "Gradually increasing movement may "
            "support general health."
        )
    )


if sleep_hours < 7:

    preventive_insights.append(

        (
            "مدة النوم المسجلة منخفضة نسبيًا. "
            "راقب انتظام النوم والتعافي."
        )

        if AR

        else

        (
            "Recorded sleep duration is relatively "
            "low. Monitor sleep consistency and recovery."
        )
    )


if water_liters < 2:

    preventive_insights.append(

        (
            "استهلاك السوائل المسجل منخفض نسبيًا، "
            "خصوصًا إذا كان مستوى النشاط مرتفعًا."
        )

        if AR

        else

        (
            "Recorded fluid intake is relatively low, "
            "especially if activity is high."
        )
    )


if (
    systolic >= 130
    or
    diastolic >= 85
):

    preventive_insights.append(

        (
            "قراءة ضغط الدم تستحق المتابعة عبر "
            "عدة قياسات بدل الاعتماد على قراءة واحدة."
        )

        if AR

        else

        (
            "The recorded blood-pressure value may "
            "deserve monitoring across multiple readings "
            "rather than relying on one measurement."
        )
    )


if spo2 < 95:

    preventive_insights.append(

        (
            "تشبع الأكسجين المسجل أقل من المعتاد. "
            "أعد القياس بطريقة صحيحة، وإذا كانت "
            "القراءة منخفضة باستمرار أو لديك أعراض "
            "فاطلب تقييمًا طبيًا."
        )

        if AR

        else

        (
            "Recorded oxygen saturation is lower than "
            "usual. Recheck the measurement correctly; "
            "persistent low readings or symptoms warrant "
            "medical assessment."
        )
    )


if not preventive_insights:

    preventive_insights.append(

        (
            "المؤشرات المدخلة تبدو متوازنة نسبيًا. "
            "الاستمرار في تسجيل البيانات يحسن جودة "
            "خط الأساس الشخصي بمرور الوقت."
        )

        if AR

        else

        (
            "Entered indicators appear relatively balanced. "
            "Consistent tracking can improve the quality "
            "of the personal baseline over time."
        )
    )


insight_columns = st.columns(
    min(
        3,
        len(
            preventive_insights
        )
    )
)


for index, insight in enumerate(
    preventive_insights
):

    column = insight_columns[
        index
        %
        len(
            insight_columns
        )
    ]

    with column:

        ui(f"""
        <div class="info-panel"
             style="min-height:155px;">

            <strong>
                {
                    "رؤية وقائية"
                    if AR
                    else
                    "Preventive Insight"
                }
            </strong>

            <div style="
                margin-top:10px;
                color:#697a76;
                line-height:1.8;
            ">
                {insight}
            </div>

        </div>
        """)


# ============================================================
# CALORIES & MACROS
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("nutrition")}
</div>
""")


nutrition_left, \
nutrition_right = st.columns(2)


with nutrition_left:

    activity = st.selectbox(

        t("activity"),

        [
            t("sedentary"),
            t("light"),
            t("moderate_activity"),
            t("active")
        ]
    )


with nutrition_right:

    goal = st.selectbox(

        t("goal"),

        [
            t("maintain"),
            t("lose"),
            t("gain")
        ]
    )


# Mifflin-St Jeor equation

bmr = (

    10
    * profile["weight"]

    +

    6.25
    * profile["height"]

    -

    5
    * profile["age"]

    +

    (
        5
        if gender_numeric == 1
        else -161
    )
)


activity_factors = {

    t("sedentary"):
        1.2,

    t("light"):
        1.375,

    t("moderate_activity"):
        1.55,

    t("active"):
        1.725
}


tdee = (
    bmr
    *
    activity_factors[
        activity
    ]
)


if goal == t("lose"):

    calorie_target = (
        tdee - 350
    )

elif goal == t("gain"):

    calorie_target = (
        tdee + 300
    )

else:

    calorie_target = tdee


calorie_target = max(
    1000,
    calorie_target
)


protein = (
    profile["weight"]
    * 1.6
)


fat = (
    profile["weight"]
    * 0.8
)


carbohydrates = max(

    0,

    (
        calorie_target

        -

        protein * 4

        -

        fat * 9
    )

    / 4
)


nutrition_columns = st.columns(5)


nutrition_cards = [

    (
        "BMR",
        f"{bmr:.0f} kcal"
    ),

    (
        "TDEE",
        f"{tdee:.0f} kcal"
    ),

    (
        t("protein"),
        f"{protein:.0f} g"
    ),

    (
        t("carbs"),
        f"{carbohydrates:.0f} g"
    ),

    (
        t("fat"),
        f"{fat:.0f} g"
    )
]


for column, item in zip(
    nutrition_columns,
    nutrition_cards
):

    label, value = item

    with column:

        ui(f"""
        <div class="metric-card">

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value"
                 style="font-size:1.35rem;">
                {value}
            </div>

        </div>
        """)


if AR:

    ui("""
    <div class="notice"
         style="margin-top:16px;">

        حاسبة السعرات والماكروز تقدم تقديرًا عامًا
        وليست خطة غذائية علاجية فردية.

    </div>
    """)

else:

    ui("""
    <div class="notice"
         style="margin-top:16px;">

        The calorie and macro calculator provides
        a general estimate and is not an individualized
        therapeutic nutrition plan.

    </div>
    """)


# ============================================================
# GLUCOSE MONITORING
# ============================================================

st.markdown("---")


if profile["diabetic"]:

    glucose_section = st.container()

else:

    glucose_section = st.expander(
        t("diabetes_center")
    )


with glucose_section:

    ui(f"""
    <div class="section-title">
        {t("diabetes_center")}
    </div>
    """)


    glucose_left, \
    glucose_right = st.columns(2)


    with glucose_left:

        glucose = st.number_input(

            t("glucose"),

            min_value=20,

            max_value=600,

            value=100,

            step=1,

            key="glucose_value"
        )


    with glucose_right:

        glucose_context = st.selectbox(

            t("measurement"),

            [
                t("fasting"),
                t("before_meal"),
                t("after_1h"),
                t("after_2h"),
                t("bedtime")
            ],

            key="glucose_context"
        )


    meal_note = st.text_input(

        t("meal"),

        key="meal_note"
    )


    if st.button(

        t("save_glucose"),

        type="primary",

        use_container_width=True,

        key="save_glucose"
    ):

        st.session_state.glucose_log.append({

            "time":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),

            "glucose":
                glucose,

            "context":
                glucose_context,

            "meal":
                meal_note
        })


        st.success(

            "تم حفظ القراءة."
            if AR
            else
            "Reading saved."
        )


    if st.session_state.glucose_log:

        glucose_dataframe = pd.DataFrame(
            st.session_state.glucose_log
        )


        glucose_chart = px.line(

            glucose_dataframe,

            x="time",

            y="glucose",

            markers=True,

            hover_data=[
                "context",
                "meal"
            ]
        )


        glucose_chart.add_hline(

            y=70,

            line_dash="dash"
        )


        glucose_chart.add_hline(

            y=180,

            line_dash="dash"
        )


        glucose_chart.update_traces(

            line_color=
                "#14866d",

            marker_color=
                "#0b213c"
        )


        glucose_chart.update_layout(

            height=360,

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)"
        )


        st.plotly_chart(

            glucose_chart,

            use_container_width=True
        )


        st.dataframe(

            glucose_dataframe,

            use_container_width=True,

            hide_index=True
        )


    if AR:

        ui("""
        <div class="notice">

            قراءات الجلوكوز هنا مخصصة للتثقيف
            والمتابعة العامة فقط، ولا تستخدمها
            وقاية لتشخيص السكري أو تعديل العلاج.

        </div>
        """)

    else:

        ui("""
        <div class="notice">

            Glucose readings here are intended for
            general education and tracking only.
            Waqaya does not use them to diagnose
            diabetes or modify treatment.

        </div>
        """)


# ============================================================
# HEALTH SEARCH DATABASE
# ============================================================

st.markdown("---")


ui(f"""
<div class="section-title">
    {t("health_search")}
</div>

<div class="section-sub">
    {
        "بحث تثقيفي مبسط عن الحالات الصحية والأعراض الشائعة."
        if AR
        else
        "A simplified educational search for common health conditions and symptoms."
    }
</div>
""")


HEALTH_DATABASE = [

    {
        "name_ar":
            "السكري من النوع الثاني",

        "name_en":
            "Type 2 Diabetes",

        "aliases":
            [
                "سكري",
                "السكري",
                "diabetes",
                "type 2 diabetes"
            ],

        "symptoms_ar":
            "زيادة العطش، كثرة التبول، التعب، تشوش الرؤية.",

        "symptoms_en":
            "Increased thirst, frequent urination, fatigue and blurred vision.",

        "causes_ar":
            "ترتبط عوامل الخطورة بمقاومة الإنسولين، التاريخ العائلي، الوزن ونمط الحياة.",

        "causes_en":
            "Risk factors can include insulin resistance, family history, weight and lifestyle."
    },

    {
        "name_ar":
            "ارتفاع ضغط الدم",

        "name_en":
            "Hypertension",

        "aliases":
            [
                "ضغط",
                "ارتفاع الضغط",
                "hypertension",
                "high blood pressure"
            ],

        "symptoms_ar":
            "قد لا يسبب أعراضًا واضحة، وقد تظهر أعراض غير نوعية لدى بعض الأشخاص.",

        "symptoms_en":
            "It often causes no obvious symptoms; some people may experience nonspecific symptoms.",

        "causes_ar":
            "تشمل عوامل الخطورة العمر، التاريخ العائلي، زيادة الوزن، قلة النشاط وبعض الأنماط الغذائية.",

        "causes_en":
            "Risk factors include age, family history, excess weight, inactivity and some dietary patterns."
    },

    {
        "name_ar":
            "الجفاف",

        "name_en":
            "Dehydration",

        "aliases":
            [
                "جفاف",
                "dehydration"
            ],

        "symptoms_ar":
            "العطش، جفاف الفم، الدوخة، قلة البول والتعب.",

        "symptoms_en":
            "Thirst, dry mouth, dizziness, reduced urination and fatigue.",

        "causes_ar":
            "قد يحدث بسبب قلة السوائل أو فقدانها مع الحرارة أو النشاط أو المرض.",

        "causes_en":
            "It may occur from inadequate fluid intake or fluid loss due to heat, activity or illness."
    },

    {
        "name_ar":
            "فقر الدم بنقص الحديد",

        "name_en":
            "Iron Deficiency Anemia",

        "aliases":
            [
                "فقر الدم",
                "نقص الحديد",
                "anemia",
                "iron deficiency"
            ],

        "symptoms_ar":
            "التعب، الضعف، الشحوب، الدوخة أو ضيق النفس لدى بعض الأشخاص.",

        "symptoms_en":
            "Fatigue, weakness, pallor, dizziness or shortness of breath in some people.",

        "causes_ar":
            "قد يرتبط بنقص الحديد الغذائي أو فقدان الدم أو زيادة الاحتياج للحديد.",

        "causes_en":
            "It may be related to low dietary iron, blood loss or increased iron requirements."
    },

    {
        "name_ar":
            "الربو",

        "name_en":
            "Asthma",

        "aliases":
            [
                "ربو",
                "asthma"
            ],

        "symptoms_ar":
            "صفير التنفس، ضيق النفس، السعال وشعور بضيق الصدر.",

        "symptoms_en":
            "Wheezing, shortness of breath, coughing and chest tightness.",

        "causes_ar":
            "قد تتأثر الأعراض بالحساسية، المهيجات، العدوى التنفسية أو النشاط لدى بعض الأشخاص.",

        "causes_en":
            "Symptoms can be affected by allergies, irritants, respiratory infections or activity."
    },

    {
        "name_ar":
            "الصداع النصفي",

        "name_en":
            "Migraine",

        "aliases":
            [
                "صداع نصفي",
                "شقيقة",
                "migraine"
            ],

        "symptoms_ar":
            "صداع نابض، غثيان وحساسية للضوء أو الصوت لدى بعض الأشخاص.",

        "symptoms_en":
            "Throbbing headache, nausea and sensitivity to light or sound in some people.",

        "causes_ar":
            "تختلف المحفزات وقد تشمل اضطراب النوم، التوتر وبعض العوامل الفردية.",

        "causes_en":
            "Triggers vary and can include sleep disruption, stress and individual factors."
    }
]


search_mode = st.selectbox(

    t("search_type"),

    [
        t("disease"),
        t("symptoms")
    ]
)


health_query = st.text_input(

    (
        "اكتب اسم المرض أو العرض"
        if AR
        else
        "Enter a disease or symptom"
    ),

    key="health_search_query"
)


if st.button(

    t("search"),

    use_container_width=True,

    key="health_search_button"
):

    normalized_query = (
        health_query
        .strip()
        .lower()
    )


    search_results = []


    if normalized_query:

        for condition in HEALTH_DATABASE:

            searchable_text = " ".join([

                condition["name_ar"],

                condition["name_en"],

                " ".join(
                    condition["aliases"]
                ),

                condition["symptoms_ar"],

                condition["symptoms_en"]

            ]).lower()


            if normalized_query in searchable_text:

                search_results.append(
                    condition
                )


    if search_results:

        for condition in search_results:

            ui(f"""
            <div class="info-panel"
                 style="margin-bottom:15px;">

                <div style="
                    font-size:1.15rem;
                    font-weight:800;
                    color:#102033;
                ">
                    {
                        condition["name_ar"]
                        if AR
                        else
                        condition["name_en"]
                    }
                </div>

                <div style="
                    margin-top:14px;
                    line-height:1.8;
                    color:#66757f;
                ">

                    <strong>
                        {
                            "الأعراض الشائعة:"
                            if AR
                            else
                            "Common symptoms:"
                        }
                    </strong>

                    <br>

                    {
                        condition["symptoms_ar"]
                        if AR
                        else
                        condition["symptoms_en"]
                    }

                    <br><br>

                    <strong>
                        {
                            "الأسباب / عوامل الخطورة:"
                            if AR
                            else
                            "Causes / risk factors:"
                        }
                    </strong>

                    <br>

                    {
                        condition["causes_ar"]
                        if AR
                        else
                        condition["causes_en"]
                    }

                </div>

            </div>
            """)

    else:

        st.info(

            (
                "لم يتم العثور على نتيجة في قاعدة "
                "المعلومات التعليمية الحالية."
            )

            if AR

            else

            (
                "No result was found in the current "
                "educational knowledge base."
            )
        )


if AR:

    ui("""
    <div class="notice">

        البحث الصحي في وقاية أداة تثقيفية عامة
        ولا يقدم تشخيصًا طبيًا أو بديلًا عن
        الاستشارة الطبية.

    </div>
    """)

else:

    ui("""
    <div class="notice">

        Waqaya Health Search is a general educational
        feature and does not provide medical diagnosis
        or replace professional medical care.

    </div>
    """)


# ============================================================
# HOW WAQAYA WORKS
# ============================================================

st.markdown("---")


if AR:

    how_waqaya_works = """

    <div class="dark-panel">

        <div style="
            color:#62cdb5;
            font-size:0.78rem;
            font-weight:800;
        ">
            WAQAYA AI ARCHITECTURE
        </div>

        <h2>
            كيف تعمل وقاية؟
        </h2>

        <div class="dark-muted">

            <strong>01 — جمع البيانات</strong><br>
            يستقبل النظام المؤشرات الحيوية وبيانات نمط الحياة.

            <br><br>

            <strong>02 — نماذج تعلم الآلة</strong><br>
            تمر الخصائص المدخلة إلى نماذج وقاية المدربة
            لتقدير إشارات الخطورة.

            <br><br>

            <strong>03 — خط الأساس الشخصي</strong><br>
            يقارن النظام القراءة الحالية بالنمط المرجعي
            لاكتشاف التغير النسبي للفرد.

            <br><br>

            <strong>04 — اكتشاف الشذوذ</strong><br>
            يبحث النظام عن أنماط غير معتادة داخل مجموعة
            المؤشرات الصحية.

            <br><br>

            <strong>05 — Waqaya Early Score</strong><br>
            تدمج وقاية إشارات النماذج والانحرافات
            لاستخراج مؤشر وقائي مبكر.

            <br><br>

            <strong>06 — Explainable AI</strong><br>
            يعرض النظام أهم الخصائص والعوامل المرتبطة
            بنتائج التحليل لتكون النتيجة أكثر وضوحًا.

        </div>

    </div>

    """

else:

    how_waqaya_works = """

    <div class="dark-panel">

        <div style="
            color:#62cdb5;
            font-size:0.78rem;
            font-weight:800;
        ">
            WAQAYA AI ARCHITECTURE
        </div>

        <h2>
            How Waqaya Works
        </h2>

        <div class="dark-muted">

            <strong>01 — Data Collection</strong><br>
            The system receives vital signs and lifestyle indicators.

            <br><br>

            <strong>02 — Machine Learning</strong><br>
            Input features are processed by Waqaya's trained
            machine-learning models to estimate risk signals.

            <br><br>

            <strong>03 — Personal Baseline</strong><br>
            Current readings are compared with a reference
            pattern to identify individual-level changes.

            <br><br>

            <strong>04 — Anomaly Detection</strong><br>
            The system searches for unusual patterns across
            the health indicators.

            <br><br>

            <strong>05 — Waqaya Early Score</strong><br>
            Model signals and deviations are combined into
            an early preventive intelligence score.

            <br><br>

            <strong>06 — Explainable AI</strong><br>
            Important features are presented to make the
            analytical result more transparent.

        </div>

    </div>

    """


ui(
    how_waqaya_works
)


# ============================================================
# WEARABLE PROTOTYPE NOTE
# ============================================================

if profile["wearable"]:

    st.info(

        (
            "تم تسجيل استخدام جهاز ذكي. "
            "الربط المباشر بالساعات والخواتم الذكية "
            "ليس مفعّلًا في النموذج الأولي الحالي، "
            "ولذلك يتم إدخال المؤشرات يدويًا."
        )

        if AR

        else

        (
            "Wearable use is recorded. Direct integration "
            "with smartwatches and smart rings is not enabled "
            "in the current prototype, so indicators are "
            "entered manually."
        )
    )


# ============================================================
# MEDICAL / RESEARCH DISCLAIMER
# ============================================================

st.markdown("---")


if AR:

    ui("""
    <div class="notice">

        <strong>تنبيه مهم:</strong>

        وقاية مشروع تقني في علوم البيانات والذكاء
        الاصطناعي الوقائي، وهو نموذج أولي بحثي/تعليمي.

        لا يُعد جهازًا طبيًا، ولا يقدم تشخيصًا أو
        وصفة علاجية، ولا ينبغي استخدام نتائجه بدل
        التقييم الطبي المتخصص.

    </div>
    """)

else:

    ui("""
    <div class="notice">

        <strong>Important notice:</strong>

        Waqaya is a preventive AI and data-science
        technology project and a research/educational
        prototype.

        It is not a medical device, does not provide
        diagnosis or treatment, and its outputs should
        not replace professional medical assessment.

    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

ui(f"""
<div class="footer">

    <strong>
        Waqaya AI
    </strong>

    <br>

    Preventive Health Intelligence

    <br><br>

    {
        "نموذج أولي للابتكار في علوم البيانات الصحية والذكاء الاصطناعي"
        if AR
        else
        "Prototype for innovation in health data science and artificial intelligence"
    }

    <br>

    Machine Learning ·
    Personal Baseline ·
    Anomaly Detection ·
    Explainable AI

</div>
""")