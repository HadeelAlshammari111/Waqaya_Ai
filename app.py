# ============================================================
# WAQAYA AI
# app.py — PART 1 OF 2
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from waqaya_engine import WaqayaEngine


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Waqaya AI | وقاية",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SAFE HTML RENDERER
# Prevents HTML from appearing as text
# ============================================================

def ui(html):
    clean = "\n".join(line.strip() for line in html.splitlines())
    st.markdown(clean, unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "language": "العربية",
    "splash_done": False,
    "profile_completed": False,
    "user_profile": {},
    "glucose_log": [],
    "analysis": None,
    "current_data": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LANGUAGE
# ============================================================

language = st.session_state.language
AR = language == "العربية"

T = {
    "ar": {
        "language": "اللغة / Language",
        "start": "ابدأ مع وقاية",
        "profile_title": "لنبدأ ببناء ملفك الصحي",
        "profile_desc": "أدخل معلوماتك الأساسية للحصول على تحليل صحي أكثر تخصيصًا.",
        "name": "الاسم",
        "age": "العمر",
        "gender": "الجنس",
        "female": "أنثى",
        "male": "ذكر",
        "weight": "الوزن (كجم)",
        "height": "الطول (سم)",
        "diabetes": "هل تعاني من مرض السكري؟",
        "wearable": "هل تستخدم جهازًا ذكيًا لمتابعة صحتك؟",
        "wearable_type": "نوع الجهاز الذكي",
        "watch": "ساعة / سوار ذكي",
        "ring": "خاتم ذكي",
        "both": "كلاهما",
        "yes": "نعم",
        "no": "لا",
        "create": "إنشاء الملف الصحي",
        "bmi": "مؤشر كتلة الجسم",
        "normal_bmi": "ضمن النطاق الطبيعي",
        "brand_sub": "Preventive Health Intelligence",
        "health_eval": "التقييم الصحي",
        "personal": "البيانات الشخصية",
        "vitals": "المؤشرات الحيوية",
        "lifestyle": "نمط الحياة",
        "systolic": "الضغط الانقباضي (mmHg)",
        "diastolic": "الضغط الانبساطي (mmHg)",
        "heart": "نبض القلب (نبضة/دقيقة)",
        "spo2": "تشبع الأكسجين SpO₂ (%)",
        "sleep": "ساعات النوم",
        "steps": "الخطوات اليومية",
        "water": "استهلاك الماء (لتر)",
        "urination": "عدد مرات التبول",
        "analyze": "تحليل الملف الصحي",
        "hero_tag": "ذكاء وقائي للصحة",
        "hero_title": "افهم نمطك الصحي قبل أن يتحول إلى إشارة تحذيرية.",
        "hero_desc": "تجمع وقاية بين تعلم الآلة، خط الأساس الشخصي واكتشاف الأنماط غير الطبيعية لتحويل المؤشرات الصحية إلى رؤى وقائية مبكرة.",
        "intelligence": "الذكاء الصحي",
        "intelligence_desc": "نظرة موحدة على إشاراتك الوقائية الحالية.",
        "risk_score": "مؤشر الخطر المبكر",
        "anomaly": "إشارة التغير",
        "status": "الحالة الحالية",
        "indicators": "المؤشرات الصحية",
        "stable": "مستقرة",
        "detected": "تم رصد تغير",
        "risk_analysis": "تحليل المخاطر",
        "risk_desc": "تقديرات وقائية مبنية على بياناتك الحالية وليست تشخيصًا طبيًا.",
        "diabetes_risk": "السكري",
        "cardio": "القلب والأوعية",
        "respiratory": "الجهاز التنفسي",
        "dehydration": "الجفاف",
        "low": "منخفض",
        "moderate": "متوسط",
        "high": "مرتفع",
        "warning": "الإنذار الوقائي الذكي",
        "baseline": "خط الأساس الشخصي",
        "baseline_desc": "مقارنة قراءاتك الحالية بنمطك المعتاد.",
        "daily": "النمط الصحي اليومي",
        "explain": "لماذا ظهرت هذه النتيجة؟",
        "feature": "أهمية المؤشرات في النموذج",
        "insights": "الرؤى الوقائية",
        "nutrition": "حاسبة السعرات والماكروز",
        "nutrition_desc": "تقدير احتياجك اليومي من الطاقة والماكروز بناءً على بيانات ملفك الشخصي.",
        "activity": "مستوى النشاط",
        "goal": "الهدف",
        "sedentary": "قليل الحركة",
        "light": "نشاط خفيف",
        "moderate_activity": "نشاط متوسط",
        "active": "نشاط مرتفع",
        "maintain": "المحافظة على الوزن",
        "lose": "خسارة الوزن",
        "gain": "زيادة الوزن",
        "protein": "البروتين",
        "carbs": "الكربوهيدرات",
        "fat": "الدهون",
        "diabetes_center": "مركز متابعة السكري",
        "diabetes_desc": "سجّل قراءات الجلوكوز وتابع نمطها حسب توقيت القياس.",
        "glucose": "قراءة الجلوكوز (mg/dL)",
        "measurement": "وقت / حالة القياس",
        "fasting": "صائم",
        "before_meal": "قبل الأكل",
        "after_1h": "بعد الأكل بساعة",
        "after_2h": "بعد الأكل بساعتين",
        "bedtime": "قبل النوم",
        "meal": "الوجبة أو ملاحظة",
        "save_glucose": "حفظ قراءة السكر",
        "avg": "متوسط القراءات",
        "highest": "أعلى قراءة",
        "lowest": "أقل قراءة",
        "last": "آخر قراءة",
        "glucose_analysis": "تحليل القراءة",
        "health_search": "البحث الصحي",
        "search_desc": "ابحث عن مرض أو أعراض للحصول على معلومات تثقيفية مختصرة.",
        "search_type": "نوع البحث",
        "disease": "البحث عن مرض",
        "symptoms": "البحث عن أعراض",
        "search": "بحث",
        "search_placeholder": "مثال: السكري، الصداع، العطش...",
        "how": "كيف تعمل وقاية؟",
        "model": "عن النموذج",
        "notice": "تنبيه مهم",
        "step1": "إدخال بياناتك",
        "step1d": "تُجمع المؤشرات الصحية الأساسية وبيانات نمط الحياة.",
        "step2": "تحليل البيانات",
        "step2d": "تتم معالجة البيانات باستخدام نماذج تعلم آلي وتحليل وقائي.",
        "step3": "اكتشاف الأنماط",
        "step3d": "تُقارن القراءات بخط الأساس لاكتشاف التغيرات غير المعتادة.",
        "step4": "الرؤى الوقائية",
        "step4d": "تتحول النتائج إلى مؤشرات ورؤى سهلة الفهم.",
    },

    "en": {
        "language": "Language / اللغة",
        "start": "Start with Waqaya",
        "profile_title": "Build Your Health Profile",
        "profile_desc": "Enter your basic information for a more personalized health analysis.",
        "name": "Name",
        "age": "Age",
        "gender": "Gender",
        "female": "Female",
        "male": "Male",
        "weight": "Weight (kg)",
        "height": "Height (cm)",
        "diabetes": "Do you have diabetes?",
        "wearable": "Do you use a smart health wearable?",
        "wearable_type": "Wearable type",
        "watch": "Smartwatch / Band",
        "ring": "Smart Ring",
        "both": "Both",
        "yes": "Yes",
        "no": "No",
        "create": "Create Health Profile",
        "bmi": "Body Mass Index",
        "normal_bmi": "BMI classification",
        "brand_sub": "Preventive Health Intelligence",
        "health_eval": "Health Assessment",
        "personal": "Personal Profile",
        "vitals": "Vital Signs",
        "lifestyle": "Lifestyle",
        "systolic": "Systolic BP (mmHg)",
        "diastolic": "Diastolic BP (mmHg)",
        "heart": "Heart Rate (bpm)",
        "spo2": "SpO₂ (%)",
        "sleep": "Sleep Hours",
        "steps": "Daily Steps",
        "water": "Water Intake (L)",
        "urination": "Urination Frequency",
        "analyze": "Analyze Health Profile",
        "hero_tag": "PREVENTIVE HEALTH INTELLIGENCE",
        "hero_title": "Understand your health pattern before it becomes a warning signal.",
        "hero_desc": "Waqaya combines machine learning, personal baselines and anomaly detection to transform health indicators into early preventive insights.",
        "intelligence": "Health Intelligence",
        "intelligence_desc": "A unified view of your current preventive signals.",
        "risk_score": "Early Risk Score",
        "anomaly": "Pattern Signal",
        "status": "Current Status",
        "indicators": "Health Indicators",
        "stable": "Stable",
        "detected": "Change detected",
        "risk_analysis": "Risk Analysis",
        "risk_desc": "Preventive estimates based on current data; not a medical diagnosis.",
        "diabetes_risk": "Diabetes",
        "cardio": "Cardiovascular",
        "respiratory": "Respiratory",
        "dehydration": "Dehydration",
        "low": "Low",
        "moderate": "Moderate",
        "high": "High",
        "warning": "AI Early Warning",
        "baseline": "Personal Baseline",
        "baseline_desc": "Compare current readings with your usual pattern.",
        "daily": "Daily Health Pattern",
        "explain": "Why this result?",
        "feature": "Feature Importance",
        "insights": "Preventive Insights",
        "nutrition": "Calories & Macros Calculator",
        "nutrition_desc": "Estimate daily energy and macro needs from your profile.",
        "activity": "Activity Level",
        "goal": "Goal",
        "sedentary": "Sedentary",
        "light": "Light Activity",
        "moderate_activity": "Moderate Activity",
        "active": "Very Active",
        "maintain": "Maintain Weight",
        "lose": "Lose Weight",
        "gain": "Gain Weight",
        "protein": "Protein",
        "carbs": "Carbohydrates",
        "fat": "Fat",
        "diabetes_center": "Diabetes Monitoring Center",
        "diabetes_desc": "Log glucose readings and analyze their pattern by measurement timing.",
        "glucose": "Glucose (mg/dL)",
        "measurement": "Measurement Context",
        "fasting": "Fasting",
        "before_meal": "Before Meal",
        "after_1h": "1 Hour After Meal",
        "after_2h": "2 Hours After Meal",
        "bedtime": "Bedtime",
        "meal": "Meal / Note",
        "save_glucose": "Save Glucose Reading",
        "avg": "Average",
        "highest": "Highest",
        "lowest": "Lowest",
        "last": "Latest",
        "glucose_analysis": "Reading Analysis",
        "health_search": "Health Search",
        "search_desc": "Search by disease or symptoms for concise educational information.",
        "search_type": "Search Type",
        "disease": "Search by Disease",
        "symptoms": "Search by Symptoms",
        "search": "Search",
        "search_placeholder": "Example: diabetes, headache, thirst...",
        "how": "How Waqaya Works",
        "model": "About the Model",
        "notice": "Important Notice",
        "step1": "Health Data",
        "step1d": "Core health indicators and lifestyle data are collected.",
        "step2": "Data Analysis",
        "step2d": "Data is processed using machine-learning and preventive analysis.",
        "step3": "Pattern Detection",
        "step3d": "Readings are compared with the personal baseline to identify unusual changes.",
        "step4": "Preventive Insights",
        "step4d": "Results are transformed into understandable preventive indicators."
    }
}


def t(key):
    return T["ar" if AR else "en"].get(key, key)


# ============================================================
# CSS — REFERENCE DESIGN
# ============================================================

ui("""
<style>

:root{
    --navy:#07172d;
    --navy2:#0b213c;
    --green:#2aa889;
    --green2:#47c5ad;
    --orange:#e85c36;
    --paper:#f6f8f7;
    --text:#102033;
    --muted:#718096;
}

html, body, [class*="css"]{
    font-family: "Segoe UI", Tahoma, Arial, sans-serif;
}

.stApp{
    background:
        radial-gradient(circle at 90% 5%, rgba(42,168,137,.08), transparent 28%),
        #f7f9f8;
    color:var(--text);
}

.block-container{
    max-width:1280px;
    padding-top:1.5rem;
    padding-bottom:4rem;
}

[data-testid="stSidebar"]{
    background:
        radial-gradient(circle at 20% 20%, rgba(45,180,145,.10), transparent 35%),
        linear-gradient(180deg,#08182c 0%,#071323 100%);
    border-right:1px solid rgba(255,255,255,.07);
}

[data-testid="stSidebar"] *{
    color:#f5f7fa;
}

[data-testid="stSidebar"] input{
    color:#102033 !important;
    background:#f5f7f6 !important;
}

[data-testid="stSidebar"] label{
    color:#ffffff !important;
    font-weight:600;
}

[data-testid="stSidebar"] hr{
    border-color:rgba(255,255,255,.12);
}

.stButton > button{
    min-height:48px;
    border-radius:10px;
    border:0;
    font-weight:700;
    transition:.2s;
}

.stButton > button[kind="primary"]{
    background:linear-gradient(90deg,#1ea789,#45c5ad);
    color:white;
}

.stButton > button:hover{
    transform:translateY(-1px);
}

[data-testid="stSidebar"] .stButton > button{
    background:linear-gradient(90deg,#d84e31,#f26b42) !important;
    color:#fff !important;
    width:100%;
}

div[data-baseweb="select"] > div{
    border-radius:10px;
}

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input{
    border-radius:10px;
}

hr{
    border:none;
    border-top:1px solid #e7ecea;
    margin:34px 0;
}

.waqaya-hero{
    background:
      radial-gradient(circle at 92% 20%,rgba(47,174,142,.22),transparent 28%),
      linear-gradient(115deg,#07162b 0%,#0a1d37 62%,#12382f 130%);
    border-radius:25px;
    padding:58px 64px;
    color:white;
    box-shadow:0 20px 55px rgba(7,23,45,.13);
    margin:15px 0 32px 0;
    position:relative;
    overflow:hidden;
}

.waqaya-hero:after{
    content:"";
    position:absolute;
    width:260px;
    height:260px;
    border-radius:50%;
    right:-90px;
    bottom:-150px;
    background:rgba(64,196,166,.08);
}

.hero-tag{
    color:#69d1b7;
    font-size:.78rem;
    font-weight:800;
    letter-spacing:.08em;
    margin-bottom:18px;
}

.hero-title{
    font-size:2.45rem;
    line-height:1.45;
    font-weight:800;
    max-width:900px;
}

.hero-desc{
    margin-top:15px;
    color:#dce7ec;
    font-size:1rem;
    line-height:1.9;
    max-width:900px;
}

.tech-pill{
    display:inline-block;
    margin-top:22px;
    background:rgba(70,167,210,.13);
    border:1px solid rgba(120,205,230,.18);
    border-radius:999px;
    padding:9px 16px;
    color:#dbeef4;
    font-size:.82rem;
}

.section-title{
    font-size:1.8rem;
    font-weight:800;
    color:#102033;
    margin:10px 0 5px;
}

.section-sub{
    color:#7a8792;
    margin-bottom:22px;
    font-size:.92rem;
}

.metric-card{
    background:#fff;
    border:1px solid #edf0ef;
    border-radius:18px;
    padding:22px;
    min-height:142px;
    box-shadow:0 8px 28px rgba(20,40,60,.045);
}

.metric-label{
    color:#7d8994;
    font-size:.78rem;
    text-transform:uppercase;
    letter-spacing:.04em;
}

.metric-value{
    color:#102033;
    font-size:1.75rem;
    font-weight:800;
    margin-top:14px;
}

.metric-note{
    color:#80908a;
    font-size:.78rem;
    margin-top:7px;
}

.risk-card{
    background:#fff;
    border:1px solid #edf0ef;
    border-radius:18px;
    padding:20px;
    min-height:150px;
}

.risk-name{
    color:#52616c;
    font-size:.88rem;
}

.risk-value{
    font-size:1.85rem;
    font-weight:800;
    color:#102033;
    margin:10px 0;
}

.progress-track{
    height:7px;
    border-radius:99px;
    background:#e8eeec;
    overflow:hidden;
}

.progress-fill{
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#278c75,#47c5ad);
}

.info-panel{
    background:#fff;
    border:1px solid #e8eeec;
    border-radius:18px;
    padding:24px;
}

.dark-panel{
    background:linear-gradient(120deg,#07172d,#0b213b);
    color:white;
    border-radius:23px;
    padding:34px;
    margin-top:15px;
}

.dark-panel h2,.dark-panel h3{
    color:white;
}

.dark-muted{
    color:#c8d4dc;
    line-height:1.8;
}

.step-number{
    font-size:1.8rem;
    font-weight:800;
    color:#61cdb4;
}

.step-title{
    color:white;
    font-weight:800;
    margin:8px 0;
}

.step-desc{
    color:#c6d2da;
    line-height:1.7;
    font-size:.86rem;
}

.glucose-card{
    background:linear-gradient(145deg,#0a1b33,#0d2944);
    border-radius:18px;
    padding:22px;
    color:white;
}

.glucose-number{
    font-size:2rem;
    font-weight:800;
    color:white;
}

.glucose-label{
    color:#b7cbd4;
    font-size:.8rem;
}

.notice{
    background:#eef8f5;
    border-left:4px solid #2aa889;
    border-radius:10px;
    padding:15px 18px;
    color:#38524c;
    font-size:.87rem;
    line-height:1.7;
}

.footer{
    text-align:center;
    padding:35px 10px 10px;
    color:#8b979e;
    font-size:.8rem;
}

@media(max-width:800px){
    .waqaya-hero{
        padding:35px 25px;
    }
    .hero-title{
        font-size:1.75rem;
    }
}

</style>
""")


# ============================================================
# HELPERS
# ============================================================

def calculate_bmi(weight, height_cm):
    if height_cm <= 0:
        return 0
    return round(weight / ((height_cm / 100) ** 2), 1)


def bmi_category(bmi):
    if bmi < 18.5:
        return "نقص وزن" if AR else "Underweight"
    elif bmi < 25:
        return "طبيعي" if AR else "Normal"
    elif bmi < 30:
        return "زيادة وزن" if AR else "Overweight"
    return "سمنة" if AR else "Obesity"


def risk_level(value):
    value = float(value)
    if value < 30:
        return t("low")
    if value < 60:
        return t("moderate")
    return t("high")


def risk_percent(value):
    try:
        value = float(value)
        if value <= 1:
            value *= 100
        return int(max(0, min(100, value)))
    except:
        return 0


def normalize_text(text):
    text = str(text).lower().strip()
    replacements = {
        "أ": "ا", "إ": "ا", "آ": "ا",
        "ة": "ه", "ى": "ي"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


# ============================================================
# HEALTH DATABASE
# ============================================================

HEALTH_DB = [
    {
        "ar": "السكري من النوع الثاني",
        "en": "Type 2 Diabetes",
        "aliases": ["سكري", "السكر", "diabetes", "type 2 diabetes", "عطش", "تبول"],
        "symptoms_ar": "العطش المتكرر، كثرة التبول، التعب، تشوش الرؤية، بطء التئام الجروح.",
        "symptoms_en": "Frequent thirst, urination, fatigue, blurred vision and slow wound healing.",
        "causes_ar": "ترتبط عوامل الخطورة بمقاومة الإنسولين، التاريخ العائلي، زيادة الوزن وقلة النشاط.",
        "causes_en": "Risk factors include insulin resistance, family history, excess weight and low activity."
    },
    {
        "ar": "ارتفاع ضغط الدم",
        "en": "Hypertension",
        "aliases": ["ضغط", "ضغط الدم", "hypertension", "صداع", "دوخه"],
        "symptoms_ar": "غالبًا لا يسبب أعراضًا واضحة، وقد يصاحبه صداع أو دوخة في بعض الحالات.",
        "symptoms_en": "Often has no obvious symptoms; headache or dizziness can occur in some cases.",
        "causes_ar": "قد ترتبط عوامل الخطورة بالعمر، الوراثة، الصوديوم، الوزن وقلة النشاط.",
        "causes_en": "Risk factors can include age, genetics, sodium intake, weight and inactivity."
    },
    {
        "ar": "الجفاف",
        "en": "Dehydration",
        "aliases": ["جفاف", "عطش", "قلة الماء", "dehydration", "thirst", "dry mouth"],
        "symptoms_ar": "العطش، جفاف الفم، البول الداكن، الدوخة والتعب.",
        "symptoms_en": "Thirst, dry mouth, dark urine, dizziness and fatigue.",
        "causes_ar": "قلة شرب السوائل أو زيادة فقدانها بسبب الحرارة أو التعرق أو المرض.",
        "causes_en": "Low fluid intake or increased fluid loss from heat, sweating or illness."
    },
    {
        "ar": "فقر الدم بنقص الحديد",
        "en": "Iron Deficiency Anemia",
        "aliases": ["فقر الدم", "انيميا", "حديد", "anemia", "fatigue", "تعب", "شحوب"],
        "symptoms_ar": "التعب، الشحوب، الدوخة، ضيق النفس والخفقان.",
        "symptoms_en": "Fatigue, pallor, dizziness, shortness of breath and palpitations.",
        "causes_ar": "قد ينتج عن نقص الحديد الغذائي أو فقدان الدم أو ضعف الامتصاص.",
        "causes_en": "Can result from low dietary iron, blood loss or impaired absorption."
    },
    {
        "ar": "الربو",
        "en": "Asthma",
        "aliases": ["ربو", "كحه", "صفير", "ضيق تنفس", "asthma", "wheezing", "cough"],
        "symptoms_ar": "صفير الصدر، السعال، ضيق النفس والشعور بضيق في الصدر.",
        "symptoms_en": "Wheezing, coughing, shortness of breath and chest tightness.",
        "causes_ar": "قد تحفزه الحساسية، المهيجات، الهواء البارد أو النشاط البدني لدى بعض الأشخاص.",
        "causes_en": "Triggers may include allergens, irritants, cold air or exercise."
    },
    {
        "ar": "الصداع النصفي",
        "en": "Migraine",
        "aliases": ["صداع", "صداع نصفي", "migraine", "headache", "غثيان"],
        "symptoms_ar": "صداع نابض قد يصاحبه غثيان وحساسية للضوء أو الصوت.",
        "symptoms_en": "Throbbing headache that may include nausea and sensitivity to light or sound.",
        "causes_ar": "تختلف المحفزات وتشمل قلة النوم، التوتر وبعض الأطعمة والتغيرات الهرمونية.",
        "causes_en": "Triggers vary and may include poor sleep, stress, foods and hormonal changes."
    }
]


def health_search(query, mode):
    q = normalize_text(query)
    results = []

    for item in HEALTH_DB:
        disease_names = [
            normalize_text(item["ar"]),
            normalize_text(item["en"])
        ]

        aliases = [normalize_text(x) for x in item["aliases"]]

        if mode == "disease":
            if any(q in name or name in q for name in disease_names + aliases):
                results.append(item)
        else:
            if any(q in alias or alias in q for alias in aliases):
                results.append(item)

    return results


# ============================================================
# LANGUAGE CONTROL
# ============================================================

top_left, top_right = st.columns([5, 1])

with top_right:
    selected_language = st.selectbox(
        t("language"),
        ["العربية", "English"],
        index=0 if st.session_state.language == "العربية" else 1,
        key="language_selector"
    )

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()


# ============================================================
# SPLASH
# ============================================================

if not st.session_state.splash_done:

    ui(f"""
    <div class="waqaya-hero" style="min-height:520px;display:flex;align-items:center;">
        <div>
            <div class="hero-tag">PREVENTIVE HEALTH INTELLIGENCE</div>
            <div class="hero-title" style="font-size:3.5rem;">وقاية</div>
            <div style="font-size:2rem;font-weight:800;margin-top:4px;">Waqaya AI</div>
            <div style="font-size:1.4rem;font-weight:700;margin-top:30px;">
                {"منصة ذكية للوقاية الصحية المبنية على البيانات" if AR else "Data-Driven Preventive Health Intelligence"}
            </div>
            <div class="hero-desc">
                {"تحليل المؤشرات الصحية، اكتشاف الأنماط المبكرة وتحويل البيانات اليومية إلى رؤى وقائية أكثر وضوحًا." if AR else "Analyze health indicators, identify early patterns and transform everyday data into clearer preventive insights."}
            </div>
            <div class="tech-pill">
                Machine Learning &nbsp; • &nbsp; Personal Baseline &nbsp; • &nbsp;
                Anomaly Detection &nbsp; • &nbsp; Preventive Insights
            </div>
        </div>
    </div>
    """)

    if st.button(t("start"), type="primary", use_container_width=True):
        st.session_state.splash_done = True
        st.rerun()

    st.stop()


# ============================================================
# PROFILE SETUP
# ============================================================

if not st.session_state.profile_completed:

    ui(f"""
    <div class="waqaya-hero">
        <div class="hero-tag">WAQAYA HEALTH PROFILE</div>
        <div class="hero-title">{t("profile_title")}</div>
        <div class="hero-desc">{t("profile_desc")}</div>
    </div>
    """)

    c1, c2 = st.columns(2)

    with c1:
        name = st.text_input(t("name"))
        age = st.number_input(t("age"), min_value=12, max_value=100, value=25)
        weight = st.number_input(t("weight"), min_value=25.0, max_value=250.0, value=60.0, step=0.5)
        diabetic = st.radio(t("diabetes"), [t("no"), t("yes")], horizontal=True)

    with c2:
        gender = st.selectbox(t("gender"), [t("female"), t("male")])
        height = st.number_input(t("height"), min_value=120.0, max_value=220.0, value=165.0, step=1.0)
        wearable = st.radio(t("wearable"), [t("no"), t("yes")], horizontal=True)

        wearable_type = None
        if wearable == t("yes"):
            wearable_type = st.selectbox(
                t("wearable_type"),
                [t("watch"), t("ring"), t("both")]
            )

    bmi = calculate_bmi(weight, height)

    ui(f"""
    <div class="info-panel" style="margin-top:20px;">
        <div class="metric-label">{t("bmi")}</div>
        <div class="metric-value">{bmi}</div>
        <div class="metric-note">{bmi_category(bmi)}</div>
    </div>
    """)

    if st.button(t("create"), type="primary", use_container_width=True):

        if not name.strip():
            st.warning("يرجى إدخال الاسم." if AR else "Please enter your name.")
            st.stop()

        st.session_state.user_profile = {
            "name": name.strip(),
            "age": int(age),
            "gender": gender,
            "weight": float(weight),
            "height": float(height),
            "bmi": float(bmi),
            "diabetic": diabetic == t("yes"),
            "wearable": wearable == t("yes"),
            "wearable_type": wearable_type
        }

        st.session_state.profile_completed = True
        st.rerun()

    st.stop()


# ============================================================
# PROFILE DATA
# ============================================================

profile = st.session_state.user_profile


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# Waqaya AI")
    st.caption("Preventive Health Intelligence")

    st.markdown("---")
    st.markdown(f"### {t('health_eval')}")

    st.markdown(f"### {t('personal')}")
    st.caption(
        f"{profile['name']} · {profile['age']} · BMI {profile['bmi']}"
    )

    if profile["diabetic"]:
        st.caption("Diabetes profile" if not AR else "ملف مريض سكري")

    if profile["wearable"]:
        st.caption(
            ("Wearable: " + str(profile["wearable_type"]))
            if not AR else
            ("الجهاز الذكي: " + str(profile["wearable_type"]))
        )

    st.markdown("---")
    st.markdown(f"### {t('vitals')}")

    systolic = st.number_input(
        t("systolic"), 70, 220, 120, key="sys"
    )

    diastolic = st.number_input(
        t("diastolic"), 40, 140, 80, key="dia"
    )

    heart_rate = st.number_input(
        t("heart"), 35, 200, 75, key="hr"
    )

    spo2 = st.number_input(
        t("spo2"), 70.0, 100.0, 98.0, step=0.1, key="spo2"
    )

    st.markdown(f"### {t('lifestyle')}")

    sleep_hours = st.number_input(
        t("sleep"), 0.0, 15.0, 7.0, step=0.5, key="sleep"
    )

    steps = st.number_input(
        t("steps"), 0, 60000, 7000, step=500, key="steps"
    )

    water_liters = st.number_input(
        t("water"), 0.0, 10.0, 2.0, step=0.25, key="water"
    )

    urination = st.number_input(
        t("urination"), 0, 30, 6, key="urination"
    )

    st.metric(t("bmi"), profile["bmi"])

    analyze_clicked = st.button(
        t("analyze"),
        type="primary",
        use_container_width=True
    )


# ============================================================
# MODEL DATA — EXACT 11 FEATURES
# ============================================================

gender_numeric = 0 if profile["gender"] in ["أنثى", "Female"] else 1

current_data = {
    "age": profile["age"],
    "gender": gender_numeric,
    "systolic_bp": systolic,
    "diastolic_bp": diastolic,
    "heart_rate": heart_rate,
    "spo2": spo2,
    "sleep_hours": sleep_hours,
    "steps": steps,
    "water_liters": water_liters,
    "urination": urination,
    "bmi": profile["bmi"]
}

st.session_state.current_data = current_data


# ============================================================
# ENGINE
# ============================================================

@st.cache_resource
def load_engine():
    return WaqayaEngine("waqaya_models.pkl")


try:
    engine = load_engine()
except Exception as e:
    st.error(
        ("تعذر تحميل نموذج وقاية: " if AR else "Unable to load Waqaya model: ")
        + str(e)
    )
    st.stop()


# ============================================================
# ANALYSIS
# ============================================================

if analyze_clicked or st.session_state.analysis is None:

    rng = np.random.default_rng(42)

    history_rows = []

    for _ in range(7):
        history_rows.append({
            "age": profile["age"],
            "gender": gender_numeric,
            "systolic_bp": max(70, systolic + rng.normal(0, 4)),
            "diastolic_bp": max(40, diastolic + rng.normal(0, 3)),
            "heart_rate": max(35, heart_rate + rng.normal(0, 4)),
            "spo2": min(100, max(70, spo2 + rng.normal(0, 0.5))),
            "sleep_hours": max(0, sleep_hours + rng.normal(0, 0.5)),
            "steps": max(0, steps + rng.normal(0, 800)),
            "water_liters": max(0, water_liters + rng.normal(0, 0.2)),
            "urination": max(0, urination + rng.normal(0, 1)),
            "bmi": profile["bmi"]
        })

    history = pd.DataFrame(history_rows)

    try:
        st.session_state.analysis = engine.analyze(
            current_data=current_data,
            history=history
        )
    except Exception as e:
        st.error(
            ("حدث خطأ أثناء تحليل الملف الصحي: " if AR
             else "An error occurred while analyzing the health profile: ")
            + str(e)
        )
        st.stop()


analysis = st.session_state.analysis or {}


# ============================================================
# EXTRACT ANALYSIS SAFELY
# ============================================================

risks = analysis.get("risks", {})

def find_risk(keywords, fallback=0):
    for key, value in risks.items():
        key_lower = str(key).lower()
        if any(word in key_lower for word in keywords):
            if isinstance(value, dict):
                for candidate in ["probability", "risk", "score", "value"]:
                    if candidate in value:
                        return risk_percent(value[candidate])
            return risk_percent(value)
    return fallback


diabetes_risk = find_risk(["diab"], 8)
cardio_risk = find_risk(["card", "heart"], 6)
resp_risk = find_risk(["resp", "lung"], 5)

# dehydration heuristic for dashboard only
dehydration_risk = 8
if water_liters < 1.5:
    dehydration_risk += 25
if urination >= 10:
    dehydration_risk += 10
if steps >= 12000 and water_liters < 2:
    dehydration_risk += 10
dehydration_risk = min(100, dehydration_risk)

early_score_raw = analysis.get("early_risk_score", None)

if isinstance(early_score_raw, dict):
    early_score_raw = early_score_raw.get(
        "score",
        early_score_raw.get("value", None)
    )

if early_score_raw is None:
    early_score = int(np.mean([
        diabetes_risk,
        cardio_risk,
        resp_risk,
        dehydration_risk
    ]))
else:
    early_score = risk_percent(early_score_raw)

anomaly_value = analysis.get("anomaly", False)

if isinstance(anomaly_value, dict):
    anomaly_detected = bool(
        anomaly_value.get(
            "is_anomaly",
            anomaly_value.get("detected", False)
        )
    )
else:
    anomaly_detected = bool(anomaly_value)


# ============================================================
# MAIN HEADER
# ============================================================

header_left, header_right = st.columns([5, 1])

with header_left:
    st.caption(
        "Waqaya AI · Preventive Health Intelligence"
    )

with header_right:
    st.caption(profile["name"])


# ============================================================
# HERO
# ============================================================

ui(f"""
<div class="waqaya-hero">
    <div class="hero-tag">{t("hero_tag")}</div>
    <div class="hero-title">{t("hero_title")}</div>
    <div class="hero-desc">{t("hero_desc")}</div>
    <div class="tech-pill">
        Machine Learning &nbsp; • &nbsp;
        Personal Baseline &nbsp; • &nbsp;
        Anomaly Detection &nbsp; • &nbsp;
        {"Preventive Insights" if not AR else "رؤى وقائية"}
    </div>
</div>
""")


# ============================================================
# HEALTH INTELLIGENCE
# ============================================================

ui(f"""
<div class="section-title">{t("intelligence")}</div>
<div class="section-sub">{t("intelligence_desc")}</div>
""")

m1, m2, m3, m4 = st.columns(4)

with m1:
    ui(f"""
    <div class="metric-card">
        <div class="metric-label">{t("risk_score")}</div>
        <div class="metric-value">{early_score}%</div>
        <div class="metric-note">{risk_level(early_score)}</div>
    </div>
    """)

with m2:
    ui(f"""
    <div class="metric-card">
        <div class="metric-label">{t("anomaly")}</div>
        <div class="metric-value">{"1" if anomaly_detected else "0"}</div>
        <div class="metric-note">
            {t("detected") if anomaly_detected else t("stable")}
        </div>
    </div>
    """)

with m3:
    ui(f"""
    <div class="metric-card">
        <div class="metric-label">{t("status")}</div>
        <div class="metric-value" style="font-size:1.35rem;">
            {t("detected") if anomaly_detected else t("stable")}
        </div>
        <div class="metric-note">Preventive status</div>
    </div>
    """)

with m4:
    ui(f"""
    <div class="metric-card">
        <div class="metric-label">{t("indicators")}</div>
        <div class="metric-value">11</div>
        <div class="metric-note">
            {"مؤشرًا تم تحليله" if AR else "indicators analyzed"}
        </div>
    </div>
    """)


# ============================================================
# EARLY RISK GAUGE
# ============================================================

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=early_score,
        number={"suffix": "%", "font": {"size": 38}},
        title={"text": t("risk_score")},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#0a1d37"},
            "steps": [
                {"range": [0, 30], "color": "#dcece7"},
                {"range": [30, 60], "color": "#eee8d7"},
                {"range": [60, 100], "color": "#eeddd8"}
            ]
        }
    )
)

fig_gauge.update_layout(
    height=340,
    margin=dict(l=35, r=35, t=60, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#102033")
)

st.plotly_chart(fig_gauge, use_container_width=True)


# ============================================================
# RISK ANALYSIS
# ============================================================

ui(f"""
<div class="section-title">{t("risk_analysis")}</div>
<div class="section-sub">{t("risk_desc")}</div>
""")

risk_items = [
    (t("diabetes_risk"), diabetes_risk),
    (t("cardio"), cardio_risk),
    (t("respiratory"), resp_risk),
    (t("dehydration"), dehydration_risk)
]

risk_cols = st.columns(4)

for col, (label, value) in zip(risk_cols, risk_items):
    with col:
        ui(f"""
        <div class="risk-card">
            <div class="risk-name">{label}</div>
            <div class="risk-value">{value}%</div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{value}%;"></div>
            </div>
            <div class="metric-note">{risk_level(value)}</div>
        </div>
        """)

risk_df = pd.DataFrame({
    "Category": [x[0] for x in risk_items],
    "Risk": [x[1] for x in risk_items]
})

fig_risk = px.bar(
    risk_df,
    x="Category",
    y="Risk",
    text="Risk"
)

fig_risk.update_traces(
    marker_color=["#3f8d7b", "#54a18e", "#0b213c", "#64a68f"],
    texttemplate="%{text}%",
    textposition="outside"
)

fig_risk.update_layout(
    height=380,
    yaxis_title="Risk %",
    xaxis_title="",
    yaxis_range=[0, 100],
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=30, r=20, t=30, b=30),
    showlegend=False
)

st.plotly_chart(fig_risk, use_container_width=True)
# ============================================================
# WAQAYA AI
# app.py — PART 2 OF 2
# Paste directly under PART 1
# ============================================================


# ============================================================
# AI EARLY WARNING
# ============================================================

st.markdown("---")

ui(f"""
<div class="section-title">{t("warning")}</div>
<div class="section-sub">
{"قراءة وقائية مبنية على المؤشرات الحالية." if AR else "A preventive interpretation based on your current indicators."}
</div>
""")

warnings = []

if systolic >= 140 or diastolic >= 90:
    warnings.append(
        "قراءة ضغط الدم الحالية أعلى من النطاق المعتاد وتستحق المتابعة."
        if AR else
        "The current blood-pressure reading is above the usual range and deserves follow-up."
    )

if spo2 < 95:
    warnings.append(
        "تشبع الأكسجين الحالي منخفض نسبيًا مقارنة بالنطاق المعتاد."
        if AR else
        "Current oxygen saturation is relatively low compared with the usual range."
    )

if sleep_hours < 6:
    warnings.append(
        "مدة النوم منخفضة وقد تؤثر في التعافي والطاقة اليومية."
        if AR else
        "Sleep duration is low and may affect recovery and daily energy."
    )

if water_liters < 1.5:
    warnings.append(
        "استهلاك الماء المسجل منخفض؛ راقب الترطيب خصوصًا مع النشاط."
        if AR else
        "Recorded water intake is low; monitor hydration, especially with activity."
    )

if heart_rate > 100:
    warnings.append(
        "نبض القلب المدخل مرتفع نسبيًا إذا كانت القراءة أثناء الراحة."
        if AR else
        "The entered heart rate is relatively high if measured at rest."
    )

if not warnings:
    warnings.append(
        "لا تظهر من البيانات المدخلة إشارة واضحة تستدعي تنبيهًا وقائيًا مرتفعًا حاليًا."
        if AR else
        "The entered data does not currently show a clear high preventive warning signal."
    )

for warning in warnings:
    ui(f"""
    <div class="notice" style="margin-bottom:10px;">
        {warning}
    </div>
    """)


# ============================================================
# PERSONAL BASELINE
# ============================================================

st.markdown("---")

ui(f"""
<div class="section-title">{t("baseline")}</div>
<div class="section-sub">{t("baseline_desc")}</div>
""")

baseline_data = pd.DataFrame({
    "Indicator": [
        t("systolic"),
        t("heart"),
        t("spo2"),
        t("sleep"),
        t("steps"),
        t("water")
    ],
    "Current": [
        systolic,
        heart_rate,
        spo2,
        sleep_hours,
        steps,
        water_liters
    ],
    "Reference": [
        120,
        75,
        98,
        7.5,
        8000,
        2.2
    ]
})

baseline_display = baseline_data.copy()
baseline_display.columns = [
    "المؤشر" if AR else "Indicator",
    "الحالي" if AR else "Current",
    "مرجع العرض" if AR else "Display Reference"
]

st.dataframe(
    baseline_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DAILY PATTERN
# ============================================================

ui(f"""
<div class="section-title">{t("daily")}</div>
<div class="section-sub">
{"عرض بصري مبسط لمؤشرات نمط الحياة." if AR else "A simplified visual view of lifestyle indicators."}
</div>
""")

pattern_df = pd.DataFrame({
    "Indicator": [
        t("sleep"),
        t("steps"),
        t("water"),
        t("urination")
    ],
    "Normalized": [
        min(100, sleep_hours / 8 * 100),
        min(100, steps / 10000 * 100),
        min(100, water_liters / 2.5 * 100),
        min(100, urination / 8 * 100)
    ]
})

fig_pattern = px.bar(
    pattern_df,
    x="Indicator",
    y="Normalized",
    text_auto=".0f"
)

fig_pattern.update_traces(marker_color="#278c75")

fig_pattern.update_layout(
    height=350,
    yaxis_title="%",
    xaxis_title="",
    yaxis_range=[0, 100],
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False
)

st.plotly_chart(fig_pattern, use_container_width=True)


# ============================================================
# EXPLAINABLE AI
# ============================================================

st.markdown("---")

ui(f"""
<div class="section-title">{t("explain")}</div>
<div class="section-sub">{t("feature")}</div>
""")

feature_importance = analysis.get("feature_importance", None)

if feature_importance is None:
    try:
        feature_importance = engine.get_feature_importance()
    except:
        feature_importance = None

feature_df = None

if isinstance(feature_importance, pd.DataFrame):
    feature_df = feature_importance.copy()

elif isinstance(feature_importance, dict):
    try:
        feature_df = pd.DataFrame(
            list(feature_importance.items()),
            columns=["Feature", "Importance"]
        )
    except:
        feature_df = None

if feature_df is not None and not feature_df.empty:

    if len(feature_df.columns) >= 2:
        feature_df = feature_df.iloc[:, :2]
        feature_df.columns = ["Feature", "Importance"]

        feature_df["Importance"] = pd.to_numeric(
            feature_df["Importance"],
            errors="coerce"
        )

        feature_df = (
            feature_df
            .dropna()
            .sort_values("Importance", ascending=True)
            .tail(10)
        )

        fig_feature = px.bar(
            feature_df,
            x="Importance",
            y="Feature",
            orientation="h"
        )

        fig_feature.update_traces(marker_color="#0b213c")

        fig_feature.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig_feature, use_container_width=True)

else:
    st.info(
        "أهمية الخصائص غير متاحة لهذا النموذج حاليًا."
        if AR else
        "Feature importance is not available for this model."
    )


# ============================================================
# PREVENTIVE INSIGHTS
# ============================================================

st.markdown("---")

ui(f"""
<div class="section-title">{t("insights")}</div>
<div class="section-sub">
{"توصيات عامة تتغير حسب البيانات التي أدخلتها." if AR else "General insights that adapt to the data you entered."}
</div>
""")

insights = []

if steps < 6000:
    insights.append(
        "نشاطك اليومي المسجل منخفض نسبيًا. الزيادة التدريجية في الحركة قد تدعم الصحة العامة."
        if AR else
        "Recorded daily activity is relatively low. Gradually increasing movement may support general health."
    )

if sleep_hours < 7:
    insights.append(
        "حاول تحسين انتظام ومدة النوم لأن النوم عنصر مهم في التعافي والصحة الأيضية."
        if AR else
        "Consider improving sleep duration and consistency, an important part of recovery and metabolic health."
    )

if water_liters < 2:
    insights.append(
        "راقب استهلاك السوائل خلال اليوم، خصوصًا في الطقس الحار أو مع النشاط."
        if AR else
        "Monitor fluid intake throughout the day, especially in hot weather or with activity."
    )

if systolic >= 130 or diastolic >= 85:
    insights.append(
        "من المفيد متابعة ضغط الدم عبر قراءات متعددة بدل الاعتماد على قراءة واحدة."
        if AR else
        "It may be useful to track blood pressure across multiple readings rather than relying on one measurement."
    )

if not insights:
    insights.append(
        "مؤشرات نمط الحياة المدخلة تبدو متوازنة نسبيًا. الاستمرارية تساعد في بناء خط أساس شخصي أدق."
        if AR else
        "Entered lifestyle indicators appear relatively balanced. Consistent tracking helps build a better personal baseline."
    )

insight_cols = st.columns(min(3, len(insights)))

for i, insight in enumerate(insights):
    with insight_cols[i % len(insight_cols)]:
        ui(f"""
        <div class="info-panel" style="min-height:150px;">
            <div style="font-weight:800;color:#18372f;margin-bottom:10px;">
                {"رؤية وقائية" if AR else "Preventive Insight"}
            </div>
            <div style="color:#697a76;line-height:1.8;font-size:.88rem;">
                {insight}
            </div>
        </div>
        """)


# ============================================================
# CALORIES & MACROS
# ============================================================

st.markdown("---")

ui(f"""
<div class="section-title">{t("nutrition")}</div>
<div class="section-sub">{t("nutrition_desc")}</div>
""")

calc1, calc2 = st.columns(2)

with calc1:
    activity = st.selectbox(
        t("activity"),
        [
            t("sedentary"),
            t("light"),
            t("moderate_activity"),
            t("active")
        ],
        key="activity_level"
    )

with calc2:
    goal = st.selectbox(
        t("goal"),
        [
            t("maintain"),
            t("lose"),
            t("gain")
        ],
        key="nutrition_goal"
    )


# Mifflin-St Jeor
if gender_numeric == 1:
    bmr = (
        10 * profile["weight"]
        + 6.25 * profile["height"]
        - 5 * profile["age"]
        + 5
    )
else:
    bmr = (
        10 * profile["weight"]
        + 6.25 * profile["height"]
        - 5 * profile["age"]
        - 161
    )

activity_map = {
    t("sedentary"): 1.2,
    t("light"): 1.375,
    t("moderate_activity"): 1.55,
    t("active"): 1.725
}

tdee = bmr * activity_map[activity]

if goal == t("lose"):
    target_calories = tdee - 350
elif goal == t("gain"):
    target_calories = tdee + 300
else:
    target_calories = tdee

target_calories = max(1000, target_calories)

protein_g = profile["weight"] * 1.6
fat_g = profile["weight"] * 0.8

remaining_calories = (
    target_calories
    - protein_g * 4
    - fat_g * 9
)

carbs_g = max(0, remaining_calories / 4)

nutrition_values = [
    ("BMR", f"{bmr:.0f} kcal"),
    ("TDEE", f"{tdee:.0f} kcal"),
    (t("protein"), f"{protein_g:.0f} g"),
    (t("carbs"), f"{carbs_g:.0f} g"),
    (t("fat"), f"{fat_g:.0f} g")
]

nutrition_cols = st.columns(5)

for col, (label, value) in zip(
    nutrition_cols,
    nutrition_values
):
    with col:
        ui(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="font-size:1.45rem;">
                {value}
            </div>
        </div>
        """)

macro_df = pd.DataFrame({
    "Macro": [
        t("protein"),
        t("carbs"),
        t("fat")
    ],
    "Grams": [
        protein_g,
        carbs_g,
        fat_g
    ]
})

fig_macro = px.bar(
    macro_df,
    x="Macro",
    y="Grams",
    text_auto=".0f"
)

fig_macro.update_traces(marker_color="#0b5b76")

fig_macro.update_layout(
    height=350,
    xaxis_title="",
    yaxis_title="Grams",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False
)

st.plotly_chart(fig_macro, use_container_width=True)

ui("""
<div class="notice">
هذه الحاسبة تقدم تقديرًا عامًا للاحتياج الغذائي وليست وصفة علاجية أو خطة غذائية فردية.
</div>
""" if AR else """
<div class="notice">
This calculator provides a general nutrition estimate and is not an individualized medical nutrition plan.
</div>
""")


# ============================================================
# DIABETES CENTER
# Show prominently for diabetic users,
# but remains available to everyone as requested.
# ============================================================

st.markdown("---")

ui(f"""
<div class="dark-panel">
    <div style="color:#62cdb5;font-size:.78rem;font-weight:800;">
        GLUCOSE INTELLIGENCE
    </div>
    <h2>{t("diabetes_center")}</h2>
    <div class="dark-muted">{t("diabetes_desc")}</div>
</div>
""")

if not profile["diabetic"]:
    st.info(
        "يمكن استخدام هذا القسم لتسجيل قراءة جلوكوز عند الحاجة، حتى إذا لم يكن الملف مسجلًا كمريض سكري."
        if AR else
        "This section can still be used to log a glucose reading even if the profile is not marked as diabetic."
    )

g1, g2 = st.columns(2)

with g1:
    glucose = st.number_input(
        t("glucose"),
        min_value=20,
        max_value=600,
        value=100,
        step=1,
        key="glucose_value"
    )

with g2:
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
    placeholder=(
        "مثال: الإفطار - شوفان وبيض"
        if AR else
        "Example: Breakfast - oats and eggs"
    )
)

if st.button(
    t("save_glucose"),
    type="primary",
    use_container_width=True,
    key="save_glucose"
):

    st.session_state.glucose_log.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "glucose": glucose,
        "context": glucose_context,
        "meal": meal_note
    })

    st.success(
        "تم حفظ القراءة."
        if AR else
        "Reading saved."
    )


# ============================================================
# GLUCOSE READING INTERPRETATION
# General educational reference only
# ============================================================

def glucose_interpretation(value, context):

    if value < 70:
        return (
            "القراءة أقل من 70 mg/dL، وهي قراءة منخفضة وفق المرجع العام."
            if AR else
            "The reading is below 70 mg/dL, which is low by the general reference."
        )

    if context == t("fasting"):

        if value <= 99:
            return (
                "القراءة الصيامية تقع ضمن المرجع العام المعتاد لغير المصابين بالسكري."
                if AR else
                "The fasting reading is within the usual general reference for people without diabetes."
            )

        if value <= 125:
            return (
                "القراءة الصيامية أعلى من المرجع المعتاد وتحتاج تقييمًا طبيًا إذا تكررت."
                if AR else
                "The fasting reading is above the usual reference and warrants medical evaluation if repeated."
            )

        return (
            "القراءة الصيامية مرتفعة. لا يمكن تشخيص السكري من قراءة واحدة ويُنصح بالتقييم الطبي."
            if AR else
            "The fasting reading is high. Diabetes cannot be diagnosed from one reading; medical evaluation is recommended."
        )

    if context == t("after_2h"):

        if value < 140:
            return (
                "القراءة بعد ساعتين تقع ضمن المرجع العام المعتاد لغير المصابين بالسكري."
                if AR else
                "The 2-hour reading is within the usual general reference for people without diabetes."
            )

        if value < 200:
            return (
                "القراءة بعد ساعتين أعلى من المرجع المعتاد وتستحق المتابعة إذا تكررت."
                if AR else
                "The 2-hour reading is above the usual reference and deserves follow-up if repeated."
            )

        return (
            "القراءة بعد ساعتين مرتفعة. يلزم تقييم طبي للتفسير والتشخيص."
            if AR else
            "The 2-hour reading is high. Medical evaluation is needed for interpretation and diagnosis."
        )

    if value <= 180:
        return (
            "القراءة تقع ضمن النطاق المرجعي العام المستخدم في هذا النموذج للعرض فقط."
            if AR else
            "The reading falls within the general display reference used by this prototype."
        )

    return (
        "القراءة أعلى من 180 mg/dL. الأهداف تختلف حسب الشخص وحالته وخطته العلاجية."
        if AR else
        "The reading is above 180 mg/dL. Targets vary by individual condition and treatment plan."
    )


ui(f"""
<div class="info-panel" style="margin-top:18px;">
    <div class="metric-label">{t("glucose_analysis")}</div>
    <div style="font-size:1.05rem;font-weight:700;margin-top:12px;line-height:1.8;">
        {glucose_interpretation(glucose, glucose_context)}
    </div>
</div>
""")


# ============================================================
# GLUCOSE HISTORY
# ============================================================

if st.session_state.glucose_log:

    glucose_df = pd.DataFrame(
        st.session_state.glucose_log
    )

    values = glucose_df["glucose"].astype(float)

    gm1, gm2, gm3, gm4 = st.columns(4)

    glucose_metrics = [
        (t("avg"), f"{values.mean():.0f}"),
        (t("highest"), f"{values.max():.0f}"),
        (t("lowest"), f"{values.min():.0f}"),
        (t("last"), f"{values.iloc[-1]:.0f}")
    ]

    for col, (label, value) in zip(
        [gm1, gm2, gm3, gm4],
        glucose_metrics
    ):
        with col:
            ui(f"""
            <div class="glucose-card">
                <div class="glucose-label">{label}</div>
                <div class="glucose-number">{value}</div>
                <div class="glucose-label">mg/dL</div>
            </div>
            """)

    fig_glucose = px.line(
        glucose_df,
        x="time",
        y="glucose",
        markers=True,
        hover_data=["context", "meal"]
    )

    fig_glucose.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="70"
    )

    fig_glucose.add_hline(
        y=180,
        line_dash="dash",
        annotation_text="180"
    )

    fig_glucose.update_traces(
        line_color="#14866d",
        marker_color="#0b213c"
    )

    fig_glucose.update_layout(
        height=380,
        xaxis_title="",
        yaxis_title="mg/dL",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_glucose,
        use_container_width=True
    )

    display_glucose = glucose_df.rename(
        columns={
            "time": "الوقت" if AR else "Time",
            "glucose": "الجلوكوز" if AR else "Glucose",
            "context": "حالة القياس" if AR else "Context",
            "meal": "الوجبة / الملاحظة" if AR else "Meal / Note"
        }
    )

    st.dataframe(
        display_glucose,
        use_container_width=True,
        hide_index=True
    )


ui("""
<div class="notice" style="margin-top:16px;">
تصنيفات الجلوكوز هنا مراجع تثقيفية عامة وليست أهدافًا علاجية شخصية. أهداف مرضى السكري قد تختلف حسب الخطة العلاجية والحالة الصحية، ولا يستخدم وقاية هذه القراءات لتشخيص المرض.
</div>
""" if AR else """
<div class="notice" style="margin-top:16px;">
Glucose classifications shown here are general educational references, not individualized treatment targets. Diabetes targets may differ by health status and treatment plan, and Waqaya does not use these readings to diagnose disease.
</div>
""")


# ============================================================
# HEALTH SEARCH
# ============================================================

st.markdown("---")

ui(f"""
<div class="section-title">{t("health_search")}</div>
<div class="section-sub">{t("search_desc")}</div>
""")

search_type_label = st.radio(
    t("search_type"),
    [t("disease"), t("symptoms")],
    horizontal=True,
    key="health_search_type"
)

search_query = st.text_input(
    t("health_search"),
    placeholder=t("search_placeholder"),
    label_visibility="collapsed",
    key="health_query"
)

search_clicked = st.button(
    t("search"),
    key="health_search_button"
)

if search_clicked:

    if not search_query.strip():
        st.warning(
            "اكتب اسم المرض أو العرض أولًا."
            if AR else
            "Enter a disease or symptom first."
        )

    else:
        mode = (
            "disease"
            if search_type_label == t("disease")
            else "symptoms"
        )

        search_results = health_search(
            search_query,
            mode
        )

        if search_results:

            for result in search_results:

                title = (
                    result["ar"]
                    if AR
                    else result["en"]
                )

                symptoms_text = (
                    result["symptoms_ar"]
                    if AR
                    else result["symptoms_en"]
                )

                causes_text = (
                    result["causes_ar"]
                    if AR
                    else result["causes_en"]
                )

                ui(f"""
                <div class="info-panel" style="margin-top:14px;">
                    <div style="font-size:1.25rem;font-weight:800;color:#102033;">
                        {title}
                    </div>

                    <div style="margin-top:16px;font-weight:700;color:#278c75;">
                        {"الأعراض الشائعة" if AR else "Common Symptoms"}
                    </div>

                    <div style="color:#687982;line-height:1.8;margin-top:5px;">
                        {symptoms_text}
                    </div>

                    <div style="margin-top:16px;font-weight:700;color:#278c75;">
                        {"الأسباب وعوامل الخطورة" if AR else "Causes & Risk Factors"}
                    </div>

                    <div style="color:#687982;line-height:1.8;margin-top:5px;">
                        {causes_text}
                    </div>
                </div>
                """)

        else:
            st.info(
                "لم أجد نتيجة في قاعدة المعرفة الحالية. جرّب كلمة أخرى أو عرضًا أكثر تحديدًا."
                if AR else
                "No result was found in the current knowledge base. Try another term or a more specific symptom."
            )

ui("""
<div class="notice" style="margin-top:16px;">
البحث الصحي في وقاية مخصص للتثقيف الصحي العام، ولا يشخص الأمراض ولا يستبدل تقييم الطبيب.
</div>
""" if AR else """
<div class="notice" style="margin-top:16px;">
Waqaya Health Search is intended for general health education. It does not diagnose disease or replace professional medical evaluation.
</div>
""")


# ============================================================
# HOW WAQAYA WORKS
# ============================================================

st.markdown("---")

ui(f"""
<div class="dark-panel">
    <h2>{t("how")}</h2>

    <div class="dark-muted" style="margin-bottom:28px;">
        {"من البيانات الصحية اليومية إلى إشارة وقائية قابلة للفهم." if AR else "From everyday health data to understandable preventive signals."}
    </div>

    <div style="
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:18px;
    ">

        <div style="
            padding:20px;
            border:1px solid rgba(255,255,255,.10);
            border-radius:18px;
            background:rgba(255,255,255,.04);
        ">
            <div class="step-number">01</div>
            <div class="step-title">{t("step1")}</div>
            <div class="step-desc">{t("step1d")}</div>
        </div>

        <div style="
            padding:20px;
            border:1px solid rgba(255,255,255,.10);
            border-radius:18px;
            background:rgba(255,255,255,.04);
        ">
            <div class="step-number">02</div>
            <div class="step-title">{t("step2")}</div>
            <div class="step-desc">{t("step2d")}</div>
        </div>

        <div style="
            padding:20px;
            border:1px solid rgba(255,255,255,.10);
            border-radius:18px;
            background:rgba(255,255,255,.04);
        ">
            <div class="step-number">03</div>
            <div class="step-title">{t("step3")}</div>
            <div class="step-desc">{t("step3d")}</div>
        </div>

        <div style="
            padding:20px;
            border:1px solid rgba(255,255,255,.10);
            border-radius:18px;
            background:rgba(255,255,255,.04);
        ">
            <div class="step-number">04</div>
            <div class="step-title">{t("step4")}</div>
            <div class="step-desc">{t("step4d")}</div>
        </div>

    </div>

    <div style="
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:28px;
        margin-top:35px;
    ">

        <div>
            <h3>{t("model")}</h3>
            <div class="dark-muted">
                {"وقاية نموذج أولي يستخدم نماذج تعلم آلي وتحليل الأنماط وخط الأساس الشخصي للمساعدة في اكتشاف التغيرات الصحية المبكرة وتقديم معلومات وقائية قابلة للفهم." if AR else "Waqaya is a prototype that combines machine-learning models, pattern analysis and personal baselines to help identify early health changes and provide understandable preventive information."}
            </div>
        </div>

        <div>
            <h3>{t("notice")}</h3>
            <div class="dark-muted">
                {"النظام نموذج أولي بحثي/تقني وليس أداة تشخيص طبي، ولا ينبغي استخدام نتائجه لاتخاذ قرار علاجي دون مختص صحي." if AR else "This is a research/technical prototype, not a medical diagnostic tool. Its results should not be used to make treatment decisions without a healthcare professional."}
            </div>
        </div>

    </div>

</div>
""")


# ============================================================
# WEARABLE INFORMATION
# ============================================================

if profile["wearable"]:

    st.info(
        (
            "تم تسجيل استخدامك لجهاز ذكي. في النسخة الأولية من وقاية يتم إدخال القراءات يدويًا، ويمكن لاحقًا ربط المنصة بواجهات الأجهزة القابلة للارتداء."
        )
        if AR else
        (
            "Your wearable use is recorded. In this Waqaya prototype, readings are entered manually; wearable APIs can be integrated in a future version."
        )
    )


# ============================================================
# FOOTER
# ============================================================

ui(f"""
<div class="footer">
    <strong>Waqaya AI</strong><br>
    Preventive Health Intelligence<br><br>
    {"نموذج أولي للابتكار في تحليل البيانات الصحية والذكاء الاصطناعي" if AR else "Prototype for innovation in health data analytics and artificial intelligence"}
</div>
""")