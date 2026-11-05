import json
import os
from datetime import datetime

import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(page_title="BuildWise AI | Construction Intelligence", page_icon="🏗️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {padding-top:1.5rem;padding-bottom:2rem}
.hero {padding:1.4rem 1.6rem;border-radius:16px;background:linear-gradient(120deg,#10243a,#1e4964);color:white;margin-bottom:1rem}
.hero h1 {color:white;margin-bottom:.25rem}
.hero p {color:#d8e8f2;margin-bottom:0}
div[data-testid="stMetric"] {background:#f4f7fa;border:1px solid #e3eaf0;padding:12px;border-radius:12px}
.small-note {color:#64748b;font-size:.88rem}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🏗️ BuildWise AI</h1>
<p>Multimodal Construction Intelligence Platform · Skill Wallet Capstone</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API key", value=os.getenv("GEMINI_API_KEY", ""), type="password", help="Optional. Add a Gemini API key to enable live image analysis and AI chat.")
    st.caption("No key? Demo mode remains available.")
    st.divider()
    st.markdown("**Platform modules**")
    st.markdown("1. Site safety & PPE audit\n2. Concrete crack diagnostics\n3. Project cost estimator\n4. Site assistant & weather advisory")
    st.caption("Prototype decision-support tool. Have qualified site engineers verify findings.")

def ask_gemini(prompt, image=None):
    key = api_key.strip()
    if not key:
        return None
    try:
        client = genai.Client(api_key=key)
        contents = [prompt]
        if image is not None:
            contents.append(types.Part.from_bytes(data=image.getvalue(), mime_type=image.type or "image/jpeg"))
        response = client.models.generate_content(model="gemini-2.5-flash", contents=contents)
        return response.text or "The model returned an empty response."
    except Exception as exc:
        st.error(f"Gemini request failed: {exc}")
        return None

def show_result(raw_text, fallback_obj, filename):
    if raw_text:
        st.markdown(raw_text)
        st.download_button("⬇️ Download AI analysis", data=raw_text, file_name=filename, mime="text/markdown")
    else:
        st.info("Demo mode: illustrative output only. No real image detection is performed without a Gemini API key.")
        st.json(fallback_obj)
        st.download_button("⬇️ Download demo JSON", data=json.dumps(fallback_obj, indent=2), file_name=filename.replace(".md", ".json"), mime="application/json")

tab_safety, tab_cracks, tab_cost, tab_assistant = st.tabs(["🦺 Site Safety & PPE", "🧱 Crack Diagnostics", "📐 Cost & Valuation", "🤖 Site Assistant"])

with tab_safety:
    st.subheader("Site Safety & PPE Audit")
    st.write("Upload a construction-site photo to review visible PPE and potential hazards.")
    safety_file = st.file_uploader("Upload site photo", type=["jpg", "jpeg", "png"], key="safety")
    if safety_file:
        image = Image.open(safety_file).convert("RGB")
        st.image(image, caption="Uploaded construction-site image", use_container_width=True)
        if st.button("Run PPE safety audit", type="primary", key="run_safety"):
            prompt = """Act as a cautious construction-site safety assistant. Inspect only visible evidence.
Return: (1) indicative safety score 0-100 and concern level; (2) PPE checklist for hard hats, high-visibility vests, footwear, eye protection and harnesses where relevant, using Present / Not visible / Unclear; (3) hazards with severity, visual evidence and corrective action; (4) limitations and human verification needed. Do not claim legal or code compliance from a photo. Do not infer hidden items."""
            result = ask_gemini(prompt, safety_file)
            fallback = {"mode":"DEMO_ONLY","safety_score":None,"overall_status":"Requires human inspection","ppe_detection":{"hard_hat":"Not evaluated","high_visibility_vest":"Not evaluated","safety_footwear":"Not evaluated","harness":"Not evaluated"},"hazards":[],"notice":"Connect Gemini to analyze an uploaded image. This demo does not perform image detection."}
            show_result(result, fallback, "ppe-safety-analysis.md")
    else:
        st.info("Upload a JPG or PNG site photo to begin.")

with tab_cracks:
    st.subheader("Concrete Crack Diagnostics")
    st.write("Upload a wall or concrete-surface photo for an indicative visual assessment.")
    crack_file = st.file_uploader("Upload concrete / wall photo", type=["jpg", "jpeg", "png"], key="crack")
    if crack_file:
        st.image(Image.open(crack_file), caption="Uploaded surface image", use_container_width=True)
        if st.button("Analyze visible cracks", type="primary", key="run_crack"):
            prompt = """Review this concrete/wall image as preliminary visual screening, not as a structural engineer. Describe visible defect type only where supportable, apparent pattern, possible causes as hypotheses, urgency (Low/Medium/High/Urgent), and next inspection steps. Do not estimate crack width without a visible scale. Do not certify structural safety. State uncertainty and advise qualified engineer review for load-bearing or widening cracks."""
            result = ask_gemini(prompt, crack_file)
            fallback = {"mode":"DEMO_ONLY","defect_type":"Not evaluated","estimated_width_mm":None,"urgency":"Requires qualified inspection","notice":"No image analysis is performed without a Gemini API key."}
            show_result(result, fallback, "crack-diagnostics.md")
    else:
        st.info("Upload a JPG or PNG surface photo to begin.")

with tab_cost:
    st.subheader("Project Planning & Cost Estimator")
    st.caption("Planning estimate only. Replace rates with local BOQ, supplier quotes and engineer-approved quantities.")
    c1, c2, c3 = st.columns(3)
    with c1:
        structure = st.selectbox("Structure type", ["Residential", "Commercial", "Industrial"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, max_value=1000000, value=1500, step=100)
    with c2:
        city_tier = st.selectbox("Location tier", ["Tier 1", "Tier 2", "Tier 3"])
        completion = st.slider("Construction completed (%)", 0, 100, 35)
    with c3:
        quality = st.selectbox("Finish quality", ["Economy", "Standard", "Premium"])
        contingency = st.slider("Contingency (%)", 0, 25, 10)
    base_rate = {"Tier 1":2400,"Tier 2":2050,"Tier 3":1800}[city_tier]
    quality_factor = {"Economy":0.85,"Standard":1.0,"Premium":1.3}[quality]
    structure_factor = {"Residential":1.0,"Commercial":1.15,"Industrial":1.1}[structure]
    rate = base_rate * quality_factor * structure_factor
    total_budget = area * rate * (1 + contingency / 100)
    incurred = total_budget * completion / 100
    remaining = total_budget - incurred
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated total budget", f"₹{total_budget/100000:.2f} lakh")
    m2.metric("Estimated incurred", f"₹{incurred/100000:.2f} lakh")
    m3.metric("Estimated remaining", f"₹{remaining/100000:.2f} lakh")
    st.progress(completion / 100, text=f"Project completion: {completion}%")
    st.caption(f"Illustrative blended rate: ₹{rate:,.0f}/sq ft. Not a market quote or valuation.")
    estimate = {"structure_type":structure,"built_up_area_sqft":area,"location_tier":city_tier,"finish_quality":quality,"completion_percent":completion,"estimated_rate_inr_per_sqft":round(rate,2),"estimated_total_budget_inr":round(total_budget,2),"estimated_incurred_inr":round(incurred,2),"estimated_remaining_inr":round(remaining,2),"contingency_percent":contingency,"disclaimer":"Illustrative planning estimate; not a professional valuation or BOQ."}
    st.download_button("⬇️ Download cost estimate (JSON)", json.dumps(estimate, indent=2), "construction-cost-estimate.json", "application/json")

with tab_assistant:
    st.subheader("Daily Site Assistant")
    weather = st.selectbox("Current site weather", ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"])
    advisories = {
        "Normal":["Continue routine inspections and housekeeping.","Check PPE, access routes and equipment before each shift."],
        "High Wind":["Pause lifting operations when wind exceeds equipment/site limits.","Secure loose materials, formwork and temporary structures."],
        "Heavy Rain":["Inspect drainage, excavation stability and water ingress.","Isolate electrical hazards and avoid work in flooded areas."],
        "Extreme Heat":["Provide drinking water, shaded rest and heat-stress monitoring.","Schedule strenuous work in cooler periods and follow local heat-safety rules."]
    }
    st.warning(f"Weather advisory: {weather}")
    for item in advisories[weather]:
        st.write("• " + item)
    st.divider()
    question = st.text_area("Ask a construction planning or safety question", placeholder="Example: What should I inspect before a concrete pour?")
    if st.button("Ask site assistant", type="primary"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            prompt = f"You are a cautious construction project assistant. Answer in practical steps. Current weather: {weather}. Question: {question}. Mention when a qualified engineer, safety officer, local code or manufacturer instruction must be consulted. Do not certify structural safety."
            answer = ask_gemini(prompt)
            if answer:
                st.markdown(answer)
            else:
                st.info("Demo response: define the work activity, inspect site conditions, verify approved drawings and method statements, check PPE and equipment, document findings, and escalate structural or high-risk issues to a qualified professional. Add a Gemini API key for live AI responses.")

st.divider()
st.markdown('<p class="small-note">BuildWise AI is an educational capstone prototype. Image outputs may be incomplete or incorrect. Never use this tool as the sole basis for safety, engineering, cost, legal, or real-estate decisions.</p>', unsafe_allow_html=True)
st.caption(f"BuildWise AI · Generated {datetime.now().strftime('%d %b %Y')}")
