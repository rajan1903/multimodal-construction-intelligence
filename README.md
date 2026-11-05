# BuildWise AI — Multimodal Construction Intelligence Platform

A Streamlit capstone prototype for construction-site visual review, concrete defect screening, project cost planning, and a weather-aware site assistant.

## Features
- **Site Safety & PPE Audit:** Upload a JPG/PNG and request a Gemini multimodal review of visible PPE and hazards.
- **Crack Diagnostics:** Preliminary visual screening of concrete/wall defects with uncertainty and engineer-review warnings.
- **Cost & Valuation Planner:** Illustrative budget estimate using area, location tier, finish quality, project type, completion and contingency.
- **Daily Site Assistant:** Weather-aware safety reminders and Gemini-powered Q&A when an API key is configured.
- **Downloads:** Export analysis notes and cost-estimate JSON.

## Tech stack
Python 3.9+, Streamlit, Google Gemini API (google-genai), Pillow, JSON.

## Run locally
```bash
git clone https://github.com/rajan1903/multimodal-construction-intelligence.git
cd multimodal-construction-intelligence
python -m venv .venv
```
Activate the environment (Windows: `.venv\\Scripts\\Activate.ps1`; macOS/Linux: `source .venv/bin/activate`), then:
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown in the terminal, usually http://localhost:8501.

## Enable Gemini
1. Create an API key in Google AI Studio.
2. Paste it into the app sidebar, or set `GEMINI_API_KEY` as an environment variable.
3. The app uses `gemini-2.5-flash` for image analysis and assistant responses.
4. Never commit API keys to GitHub.
Without a key, the app remains usable in clearly labelled demo mode. Demo mode does not perform real image detection.

## Deploy on Streamlit Community Cloud
1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Select **New app**.
3. Choose repository `rajan1903/multimodal-construction-intelligence`, branch `main`, and main file `app.py`.
4. Click **Deploy**.
5. For live Gemini responses, open **App settings → Secrets** and add:
```toml
GEMINI_API_KEY = "your_actual_key_here"
```
6. Save, wait for restart, and test all four modules.

## Skill Wallet submission
- GitHub repository: https://github.com/rajan1903/multimodal-construction-intelligence
- Live demo: copy the actual public URL shown by Streamlit after deployment. Do not submit a guessed demo URL.

## Important limitations
- PPE and crack outputs are AI-assisted visual observations, not certified inspections.
- Crack width is not estimated unless a reliable scale reference is visible.
- Cost rates are illustrative placeholders; replace them with local BOQ and supplier data.
- Weather advisories are general reminders, not a substitute for official forecasts or site safety plans.
- A qualified engineer / safety officer must verify critical decisions.

## Project structure
```text
multimodal-construction-intelligence/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

Educational capstone prototype.
