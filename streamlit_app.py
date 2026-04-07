import streamlit as st
import streamlit.components.v1 as components
import requests
from pathlib import Path

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroScan AI",
    page_icon="🧠",
    layout="centered"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060912 !important;
    color: #E8EAF0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,180,216,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(72,52,212,0.10) 0%, transparent 60%),
        #060912 !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

.block-container {
    max-width: 720px !important;
    padding: 3rem 2rem 4rem !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Section ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 2rem;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #00B4D8;
    background: rgba(0,180,216,0.08);
    border: 1px solid rgba(0,180,216,0.22);
    border-radius: 100px;
    padding: 5px 14px;
    margin-bottom: 1.4rem;
}

.hero-eyebrow span.dot {
    width: 6px; height: 6px;
    background: #00B4D8;
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(32px, 6vw, 52px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #FFFFFF 0%, #A8D8EA 60%, #00B4D8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem; 
}

.hero-sub {
    font-size: 15px;
    font-weight: 300;
    color: rgba(232,234,240,0.55);
    max-width: 500px;
    margin: 0.5rem auto 0; 
    text-align: center;     
}

/* ── Divider ── */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,180,216,0.25), transparent);
    margin: 2rem 0;
}

/* ── Upload Card ── */
.upload-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.45);
    margin-bottom: 0.6rem;
    display: block;
}

/* Streamlit uploader override */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(0,180,216,0.30) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    transition: border-color 0.25s ease, background 0.25s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,180,216,0.65) !important;
    background: rgba(0,180,216,0.04) !important;
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploader"] label {
    color: rgba(232,234,240,0.5) !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Image preview ── */
[data-testid="stImage"] img {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── Analyze Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #0096C7 0%, #0077B6 100%) !important;
    color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    height: auto !important;
    cursor: pointer;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(0,150,199,0.30) !important;
    margin-top: 1rem;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00B4D8 0%, #0096C7 100%) !important;
    box-shadow: 0 6px 32px rgba(0,180,216,0.45) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 3px 16px rgba(0,150,199,0.30) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #00B4D8 !important;
}

/* ── Result Cards ── */
.result-section {
    margin-top: 2rem;
    animation: fadeUp 0.45s ease forwards;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-header {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.35);
    margin-bottom: 1rem;
}

.result-card {
    border-radius: 18px;
    padding: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.2rem;
    border: 1px solid transparent;
    transition: all 0.3s ease;
}

.result-card.safe {
    background: linear-gradient(135deg, rgba(0,200,120,0.10), rgba(0,200,120,0.04));
    border-color: rgba(0,200,120,0.20);
}

.result-card.danger {
    background: linear-gradient(135deg, rgba(255,75,75,0.12), rgba(255,75,75,0.04));
    border-color: rgba(255,75,75,0.22);
}

.result-icon {
    font-size: 40px;
    flex-shrink: 0;
    filter: drop-shadow(0 0 12px currentColor);
}

.result-body {}

.result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 0.25rem;
}

.result-verdict.safe  { color: #00C878; }
.result-verdict.danger { color: #FF6B6B; }

.result-desc {
    font-size: 13px;
    font-weight: 400;
    color: rgba(232,234,240,0.45);
    line-height: 1.5;
}

/* ── Confidence Row ── */
.conf-row {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.25rem 1.6rem;
}

.conf-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.75rem;
}

.conf-label {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.4);
}

.conf-value {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
}

.conf-bar-bg {
    background: rgba(255,255,255,0.07);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
}

.conf-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.8s cubic-bezier(0.16,1,0.3,1);
}

.conf-bar-fill.safe   { background: linear-gradient(90deg, #00C878, #00E5A0); }
.conf-bar-fill.danger { background: linear-gradient(90deg, #FF4B4B, #FF8080); }

/* ── Error ── */
[data-testid="stAlert"] {
    background: rgba(255,75,75,0.08) !important;
    border: 1px solid rgba(255,75,75,0.20) !important;
    border-radius: 12px !important;
    color: #FF9090 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3.5rem;
    font-size: 12px;
    color: rgba(232,234,240,0.18);
    line-height: 1.8;
}

.footer a { color: rgba(0,180,216,0.5); text-decoration: none; }

/* ── Metrics Row ── */
.metrics-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.metric-pill {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-pill-val {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #00B4D8;
}

.metric-pill-key {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.30);
    margin-top: 2px;
}

</style>
""", unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow"><span class="dot"></span> AI-Powered Diagnostics</div>
    <h1 class="hero-title">NeuroScan AI</h1>
    <p class="hero-sub">Upload an MRI scan and get instant, AI-assisted brain tumor classification.</p>
</div>
""", unsafe_allow_html=True)

# ─── Stats Row ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="metrics-row">
    <div class="metric-pill">
        <div class="metric-pill-val">4</div>
        <div class="metric-pill-key">Tumor Types</div>
    </div>
    <div class="metric-pill">
        <div class="metric-pill-val">82%</div>
        <div class="metric-pill-key">Accuracy</div>
    </div>
    <div class="metric-pill">
        <div class="metric-pill-val">&lt;2s</div>
        <div class="metric-pill-key">Inference</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── Upload ──────────────────────────────────────────────────────────────────
st.markdown('<span class="upload-label">MRI Scan — JPG / PNG / JPEG</span>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    st.image(uploaded_file, caption="", use_container_width=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    analyze = st.button("🔬  Analyze Scan", use_container_width=True)

    if analyze:
        API_URL = "http://127.0.0.1:8000/predict/"
        with st.spinner("Running inference…"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(API_URL, files=files, timeout=15)

                if response.status_code == 200:
                    result = response.json()
                    prediction = result["prediction"]
                    confidence = result["confidence"]

                    is_safe   = prediction.lower() == "no_tumor"
                    css_cls   = "safe" if is_safe else "danger"
                    icon      = "✅" if is_safe else "⚠️"
                    verdict   = "No Tumor Detected" if is_safe else prediction.replace("_", " ").title()
                    desc      = (
                        "The MRI scan shows no signs of a brain tumor. "
                        "Regular follow-up is still recommended."
                        if is_safe else
                        "A potential tumor has been identified. "
                        "Please consult a specialist for further evaluation."
                    )
                    conf_pct  = f"{confidence:.1%}"
                    bar_w     = int(confidence * 100)

                    card_color     = "rgba(0,200,120,0.10)"  if is_safe else "rgba(255,75,75,0.12)"
                    card_border    = "rgba(0,200,120,0.25)"  if is_safe else "rgba(255,75,75,0.28)"
                    verdict_color  = "#00C878"               if is_safe else "#FF6B6B"
                    bar_color      = "linear-gradient(90deg,#00C878,#00E5A0)" if is_safe else "linear-gradient(90deg,#FF4B4B,#FF8080)"

                    components.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: transparent;
    font-family: 'DM Sans', sans-serif;
    color: #E8EAF0;
    padding: 4px 2px 8px;
  }}

  .result-header {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.35);
    margin-bottom: 12px;
  }}

  .result-card {{
    border-radius: 18px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 14px;
    background: {card_color};
    border: 1px solid {card_border};
    animation: fadeUp 0.4s ease forwards;
  }}

  .result-icon {{ font-size: 38px; flex-shrink: 0; }}

  .result-verdict {{
    font-family: 'Syne', sans-serif;
    font-size: 21px;
    font-weight: 700;
    color: {verdict_color};
    margin-bottom: 4px;
  }}

  .result-desc {{
    font-size: 13px;
    color: rgba(232,234,240,0.50);
    line-height: 1.55;
  }}

  .conf-row {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    animation: fadeUp 0.5s ease forwards;
  }}

  .conf-top {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }}

  .conf-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.38);
  }}

  .conf-value {{
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
  }}

  .conf-bar-bg {{
    background: rgba(255,255,255,0.08);
    border-radius: 100px;
    height: 7px;
    overflow: hidden;
  }}

  .conf-bar-fill {{
    height: 100%;
    border-radius: 100px;
    background: {bar_color};
    width: 0%;
    transition: width 1s cubic-bezier(0.16,1,0.3,1);
  }}

  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
</style>
</head>
<body>
  <div class="result-header">Analysis Result</div>

  <div class="result-card">
    <div class="result-icon">{icon}</div>
    <div>
      <div class="result-verdict">{verdict}</div>
      <div class="result-desc">{desc}</div>
    </div>
  </div>

  <div class="conf-row">
    <div class="conf-top">
      <span class="conf-label">Confidence Score</span>
      <span class="conf-value">{conf_pct}</span>
    </div>
    <div class="conf-bar-bg">
      <div class="conf-bar-fill" id="bar"></div>
    </div>
  </div>

  <script>
    // Animate bar after paint
    requestAnimationFrame(() => {{
      setTimeout(() => {{
        document.getElementById('bar').style.width = '{bar_w}%';
      }}, 80);
    }});
  </script>
</body>
</html>
""", height=230, scrolling=False)

                else:
                    st.error(f"API returned status {response.status_code}. Check that the backend is running.")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the API at `http://127.0.0.1:8000`. Make sure your FastAPI backend is running.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

else:
    # Placeholder hint
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem; color:rgba(232,234,240,0.22); font-size:13px;">
        Drag & drop or click above to upload your MRI image
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    NeuroScan AI &nbsp;·&nbsp; For research & educational use only<br>
    Not a substitute for professional medical diagnosis
</div>
""", unsafe_allow_html=True)