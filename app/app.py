import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Page config


st.set_page_config(
    page_title="PREDICTO",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Custom CSS — dark football theme


st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600&display=swap');

  html, body, [class*="css"] {
    background-color: #0a0e1a;
    color: #f0f0f0;
    font-family: 'Inter', sans-serif;
  }

  .hero {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a2744 50%, #0d1f3c 100%);
    border: 1px solid #2a3a5c;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: "⚽";
    position: absolute;
    font-size: 180px;
    opacity: 0.04;
    top: -20px;
    left: -30px;
  }
  .hero::after {
    content: "🏆";
    position: absolute;
    font-size: 180px;
    opacity: 0.04;
    bottom: -20px;
    right: -30px;
  }
  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1;
  }
  .hero-sub {
    color: #8899bb;
    font-size: 1rem;
    margin-top: 0.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  .team-card {
    background: linear-gradient(135deg, #111827, #1e2d45);
    border: 1px solid #2a3a5c;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
  }
  .team-card:hover { border-color: #FFD700; }

  .team-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 3px;
    color: #FFD700;
    margin-bottom: 0.5rem;
  }

  .vs-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding-top: 2rem;
  }
  .vs-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: #FFD700;
    line-height: 1;
  }

  .prediction-banner {
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
    border: 2px solid #FFD700;
    background: linear-gradient(135deg, #1a2400, #2d3d00);
  }
  .prediction-result {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 3px;
    color: #FFD700;
  }
  .prediction-conf {
    color: #aabbcc;
    font-size: 1rem;
    margin-top: 0.25rem;
  }

  .stat-card {
    background: #111827;
    border: 1px solid #2a3a5c;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
  }
  .stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #FFD700;
    line-height: 1;
  }
  .stat-label {
    color: #8899bb;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.25rem;
  }

  .conf-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }

  .predict-btn > button {
    background: linear-gradient(90deg, #FFD700, #FFA500) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: opacity 0.2s !important;
  }
  .predict-btn > button:hover { opacity: 0.85 !important; }

  div[data-testid="stSelectbox"] > div {
    background: #111827 !important;
    border: 1px solid #2a3a5c !important;
    border-radius: 8px !important;
    color: #f0f0f0 !important;
  }

  .flag-row {
    font-size: 2.5rem;
    margin-bottom: 0.25rem;
  }

  .h2h-row {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
  }

  .stSlider > div > div > div { background: #FFD700 !important; }

  hr { border-color: #2a3a5c !important; }

  .footer {
    text-align: center;
    color: #3a4a6c;
    font-size: 0.75rem;
    padding-top: 2rem;
    letter-spacing: 1px;
  }
</style>
""", unsafe_allow_html=True)


# All 48 World Cup 2026 teams with flags and confederation


WC2026_TEAMS = {
    # CONMEBOL
    "Argentina":      {"flag": "🇦🇷", "conf": "CONMEBOL", "conf_color": "#1a6b3a"},
    "Brazil":         {"flag": "🇧🇷", "conf": "CONMEBOL", "conf_color": "#1a6b3a"},
    "Colombia":       {"flag": "🇨🇴", "conf": "CONMEBOL", "conf_color": "#1a6b3a"},
    "Ecuador":        {"flag": "🇪🇨", "conf": "CONMEBOL", "conf_color": "#1a6b3a"},
    "Paraguay":       {"flag": "🇵🇾", "conf": "CONMEBOL", "conf_color": "#1a6b3a"},
    "Uruguay":        {"flag": "🇺🇾", "conf": "CONMEBOL", "conf_color": "#1a6b3a"},
    # UEFA
    "Austria":        {"flag": "🇦🇹", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Belgium":        {"flag": "🇧🇪", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Bosnia and Herzegovina": {"flag": "🇧🇦", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Croatia":        {"flag": "🇭🇷", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Czechia":        {"flag": "🇨🇿", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "England":        {"flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "France":         {"flag": "🇫🇷", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Germany":        {"flag": "🇩🇪", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Netherlands":    {"flag": "🇳🇱", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Norway":         {"flag": "🇳🇴", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Portugal":       {"flag": "🇵🇹", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Scotland":       {"flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Spain":          {"flag": "🇪🇸", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Sweden":         {"flag": "🇸🇪", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Switzerland":    {"flag": "🇨🇭", "conf": "UEFA", "conf_color": "#1a3a6b"},
    "Turkey":         {"flag": "🇹🇷", "conf": "UEFA", "conf_color": "#1a3a6b"},
    # CAF
    "Algeria":        {"flag": "🇩🇿", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Cabo Verde":     {"flag": "🇨🇻", "conf": "CAF", "conf_color": "#6b3a1a"},
    "DR Congo":       {"flag": "🇨🇩", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Côte d'Ivoire":  {"flag": "🇨🇮", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Egypt":          {"flag": "🇪🇬", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Ghana":          {"flag": "🇬🇭", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Morocco":        {"flag": "🇲🇦", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Senegal":        {"flag": "🇸🇳", "conf": "CAF", "conf_color": "#6b3a1a"},
    "South Africa":   {"flag": "🇿🇦", "conf": "CAF", "conf_color": "#6b3a1a"},
    "Tunisia":        {"flag": "🇹🇳", "conf": "CAF", "conf_color": "#6b3a1a"},
    # AFC
    "Australia":      {"flag": "🇦🇺", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Iraq":           {"flag": "🇮🇶", "conf": "AFC", "conf_color": "#4a1a6b"},
    "IR Iran":        {"flag": "🇮🇷", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Japan":          {"flag": "🇯🇵", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Jordan":         {"flag": "🇯🇴", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Korea Republic": {"flag": "🇰🇷", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Qatar":          {"flag": "🇶🇦", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Saudi Arabia":   {"flag": "🇸🇦", "conf": "AFC", "conf_color": "#4a1a6b"},
    "Uzbekistan":     {"flag": "🇺🇿", "conf": "AFC", "conf_color": "#4a1a6b"},
    # CONCACAF
    "Canada":         {"flag": "🇨🇦", "conf": "CONCACAF", "conf_color": "#6b1a1a"},
    "Curaçao":        {"flag": "🇨🇼", "conf": "CONCACAF", "conf_color": "#6b1a1a"},
    "Haiti":          {"flag": "🇭🇹", "conf": "CONCACAF", "conf_color": "#6b1a1a"},
    "Mexico":         {"flag": "🇲🇽", "conf": "CONCACAF", "conf_color": "#6b1a1a"},
    "Panama":         {"flag": "🇵🇦", "conf": "CONCACAF", "conf_color": "#6b1a1a"},
    "United States":  {"flag": "🇺🇸", "conf": "CONCACAF", "conf_color": "#6b1a1a"},
    # OFC
    "New Zealand":    {"flag": "🇳🇿", "conf": "OFC", "conf_color": "#1a5a5a"},
}

TEAM_NAMES = sorted(WC2026_TEAMS.keys())



# Map WC2026 names to names in results.csv
# (some names differ between datasets)


NAME_MAP = {
    "Turkey":                 "Turkey",
    "IR Iran":                "Iran",
    "Korea Republic":         "South Korea",
    "Cabo Verde":             "Cape Verde",
    "DR Congo":               "DR Congo",
    "Côte d'Ivoire":         "Ivory Coast",
    "Bosnia and Herzegovina": "Bosnia-Herzegovina",
    "United States":          "United States",
}

def to_dataset_name(team):
    return NAME_MAP.get(team, team)


# Load model and data


@st.cache_resource
def load_model():
    model = pickle.load(open("models/match_model.pkl", "rb"))
    le    = pickle.load(open("models/team_encoder.pkl", "rb"))
    return model, le

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/clean_matches.csv",
                       parse_dates=["date"])

model, le = load_model()
df        = load_data()


# Hero banner


st.markdown("""
<div class="hero">
  <p class="hero-title">PREDICTO</p>
  <p class="hero-sub">Predict Every World Cup 2026 Match &nbsp;·&nbsp; 48 Nations &nbsp;·&nbsp; 1 Prediction Engine</p>
</div>
""", unsafe_allow_html=True)



# Team selection


col_home, col_vs, col_away = st.columns([5, 2, 5])

with col_home:
    st.markdown('<div class="team-label">🏠 Home Team</div>', unsafe_allow_html=True)
    home_team = st.selectbox(
        "Home", TEAM_NAMES,
        index=TEAM_NAMES.index("Brazil"),
        label_visibility="collapsed",
        key="home_select"
    )
    home_info = WC2026_TEAMS[home_team]
    st.markdown(f"""
    <div style="text-align:center; margin: 8px 0">
      <div class="flag-row">{home_info['flag']}</div>
      <span class="conf-badge" style="background:{home_info['conf_color']}22;
            color:{home_info['conf_color'].replace('1a','88').replace('3a','bb').replace('6b','ee')}44;
            border:1px solid {home_info['conf_color']}44">
        {home_info['conf']}
      </span>
    </div>
    """, unsafe_allow_html=True)
    home_form = st.slider(
    "Recent form", 0, 100, 60, 5,
    format="%d%%",
    help="Win rate over last 10 matches. 0% = lost all. 100% = won all.",
    key="home_form"
    ) / 100
    

with col_vs:
    st.markdown("""
    <div class="vs-box">
      <div class="vs-text">VS</div>
    </div>
    """, unsafe_allow_html=True)
    is_neutral = st.checkbox("Neutral\nvenue", value=False, key="neutral")

with col_away:
    st.markdown('<div class="team-label">✈️ Away Team</div>', unsafe_allow_html=True)
    away_team = st.selectbox(
        "Away", TEAM_NAMES,
        index=TEAM_NAMES.index("France"),
        label_visibility="collapsed",
        key="away_select"
    )
    away_info = WC2026_TEAMS[away_team]
    st.markdown(f"""
    <div style="text-align:center; margin: 8px 0">
      <div class="flag-row">{away_info['flag']}</div>
      <span class="conf-badge" style="background:{away_info['conf_color']}22;
            color:{away_info['conf_color']}44;
            border:1px solid {away_info['conf_color']}44">
        {away_info['conf']}
      </span>
    </div>
    """, unsafe_allow_html=True)
    away_form = st.slider(
    "Recent form", 0, 100, 50, 5,
    format="%d%%",
    key="away_form"
    ) / 100



# Head-to-head stats


st.divider()

home_ds = to_dataset_name(home_team)
away_ds = to_dataset_name(away_team)

h2h = df[
    ((df["home_team"] == home_ds) & (df["away_team"] == away_ds)) |
    ((df["home_team"] == away_ds) & (df["away_team"] == home_ds))
].copy()

home_wins_h2h = len(h2h[
    ((h2h["home_team"] == home_ds) & (h2h["result"] == "Home Win")) |
    ((h2h["away_team"] == home_ds) & (h2h["result"] == "Away Win"))
])
away_wins_h2h = len(h2h[
    ((h2h["home_team"] == away_ds) & (h2h["result"] == "Home Win")) |
    ((h2h["away_team"] == away_ds) & (h2h["result"] == "Away Win"))
])
draws_h2h = len(h2h[h2h["result"] == "Draw"])

if len(h2h) > 0:
    st.markdown(f"### {WC2026_TEAMS[home_team]['flag']} {home_team} vs {away_team} {WC2026_TEAMS[away_team]['flag']} — Head to Head")

    s1, s2, s3, s4 = st.columns(4)
    s1.markdown(f'<div class="stat-card"><div class="stat-num">{len(h2h)}</div><div class="stat-label">Total Meetings</div></div>', unsafe_allow_html=True)
    s2.markdown(f'<div class="stat-card"><div class="stat-num">{home_wins_h2h}</div><div class="stat-label">{home_team} Wins</div></div>', unsafe_allow_html=True)
    s3.markdown(f'<div class="stat-card"><div class="stat-num">{draws_h2h}</div><div class="stat-label">Draws</div></div>', unsafe_allow_html=True)
    s4.markdown(f'<div class="stat-card"><div class="stat-num">{away_wins_h2h}</div><div class="stat-label">{away_team} Wins</div></div>', unsafe_allow_html=True)

    with st.expander("📋 Full match history"):
        display = h2h[["date","home_team","home_score","away_score",
                        "away_team","tournament"]].sort_values("date", ascending=False)
        display.columns = ["Date","Home","H","A","Away","Tournament"]
        st.dataframe(display.head(20).reset_index(drop=True),
                     use_container_width=True, hide_index=True)
else:
    st.info(f"No recorded matches between {home_team} and {away_team} in the dataset.")


# Predict button


st.divider()

st.markdown('<div class="predict-btn">', unsafe_allow_html=True)
predict = st.button("⚡ Predict Match Outcome", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if predict:
    if home_team == away_team:
        st.error("Please select two different teams.")
        st.stop()

    # Check if teams exist in encoder
    known_teams = set(le.classes_)
    home_ds_name = to_dataset_name(home_team)
    away_ds_name = to_dataset_name(away_team)

    home_known = home_ds_name in known_teams
    away_known = away_ds_name in known_teams

    if not home_known or not away_known:
        unknown = []
        if not home_known: unknown.append(home_team)
        if not away_known: unknown.append(away_team)
        st.warning(
            f"{', '.join(unknown)} not found in historical data "
            f"(debut nation or name mismatch). Using average encoding."
        )

    home_enc  = le.transform([home_ds_name])[0] if home_known else int(len(le.classes_)/2)
    away_enc  = le.transform([away_ds_name])[0] if away_known else int(len(le.classes_)/2)
    form_diff = home_form - away_form
    h2h_rate  = home_wins_h2h / len(h2h) if len(h2h) > 0 else 0.5

    X_pred = pd.DataFrame([[
        home_enc, away_enc,
        home_form, away_form, form_diff,
        h2h_rate, int(is_neutral)
    ]], columns=[
        "home_team_enc", "away_team_enc",
        "home_form", "away_form", "form_diff",
        "home_h2h_rate", "is_neutral"
    ])

    prediction = model.predict(X_pred)[0]
    probas     = model.predict_proba(X_pred)[0]
    classes    = list(model.classes_)
    prob_dict  = dict(zip(classes, probas))

    ordered      = ["Home Win", "Draw", "Away Win"]
    winner_label = {
        "Home Win": f"{WC2026_TEAMS[home_team]['flag']} {home_team} wins",
        "Away Win": f"{WC2026_TEAMS[away_team]['flag']} {away_team} wins",
        "Draw":     "⚖️ Draw"
    }

    confidence   = prob_dict.get(prediction, 0)
    conf_level   = "HIGH" if confidence > 0.55 else "MEDIUM" if confidence > 0.42 else "LOW"
    conf_color   = "#4CAF50" if conf_level == "HIGH" else "#FFA500" if conf_level == "MEDIUM" else "#F44336"

    st.markdown(f"""
    <div class="prediction-banner">
      <div style="color:#8899bb;font-size:0.85rem;letter-spacing:2px;
                  text-transform:uppercase;margin-bottom:0.5rem">
        Prediction
      </div>
      <div class="prediction-result">{winner_label[prediction]}</div>
      <div class="prediction-conf">
        Confidence: <span style="color:{conf_color};font-weight:600">{conf_level}</span>
        &nbsp;·&nbsp; {confidence:.1%} probability
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Probability bars
    fig, ax = plt.subplots(figsize=(9, 3))
    fig.patch.set_facecolor("#0a0e1a")
    ax.set_facecolor("#0a0e1a")

    probs    = [prob_dict.get(o, 0) for o in ordered]
    labels   = [
        f"{WC2026_TEAMS[home_team]['flag']} Home Win",
        "Draw ⚖️",
        f"Away Win {WC2026_TEAMS[away_team]['flag']}"
    ]
    bar_cols = [
        "#FFD700" if ordered[i] == prediction else "#1e3a5f"
        for i in range(3)
    ]

    bars = ax.barh(labels, probs, color=bar_cols,
                   height=0.5, edgecolor="#2a3a5c")

    for bar, prob in zip(bars, probs):
        ax.text(prob + 0.01, bar.get_y() + bar.get_height()/2,
                f"{prob:.1%}", va="center", color="white", fontsize=12)

    ax.axvline(0.333, color="#3a4a6c", linestyle="--", alpha=0.7, linewidth=1)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Probability", color="#8899bb")
    ax.tick_params(colors="#8899bb")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a3a5c")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Probability metrics
    m1, m2, m3 = st.columns(3)
    for col, label, outcome in zip(
        [m1, m2, m3],
        [f"{home_team} Win", "Draw", f"{away_team} Win"],
        ordered
    ):
        prob = prob_dict.get(outcome, 0)
        is_pred = outcome == prediction
        col.metric(
            label=f"{'✅ ' if is_pred else ''}{label}",
            value=f"{prob:.1%}"
        )

    # Form comparison bar
    st.divider()
    st.markdown("#### 📊 Form comparison")
    fc1, fc2 = st.columns(2)
    fc1.progress(home_form,
                 text=f"{WC2026_TEAMS[home_team]['flag']} {home_team} — {home_form:.0%} form")
    fc2.progress(away_form,
                 text=f"{WC2026_TEAMS[away_team]['flag']} {away_team} — {away_form:.0%} form")

# ============================================
# Model metrics cards
# ============================================

import json
import os

st.divider()
st.markdown("#### 🤖 Model Performance")

metrics_path = "models/metrics.json"
if os.path.exists(metrics_path):
    with open(metrics_path) as f:
        metrics = json.load(f)

    m1, m2, m3, m4 = st.columns(4)

    m1.markdown(f"""
    <div class="stat-card">
      <div class="stat-num">{metrics['accuracy']:.0%}</div>
      <div class="stat-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

    m2.markdown(f"""
    <div class="stat-card">
      <div class="stat-num">{metrics['f1_score']:.0%}</div>
      <div class="stat-label">F1 Score</div>
    </div>
    """, unsafe_allow_html=True)

    m3.markdown(f"""
    <div class="stat-card">
      <div class="stat-num">{metrics['roc_auc']:.0%}</div>
      <div class="stat-label">ROC AUC</div>
    </div>
    """, unsafe_allow_html=True)

    m4.markdown(f"""
    <div class="stat-card">
      <div class="stat-num" style="font-size:1rem;line-height:1.3">
        {metrics['model_name']}
      </div>
      <div class="stat-label">Model Used</div>
    </div>
    """, unsafe_allow_html=True)

# Tournament info strip

st.divider()
st.markdown("#### 🌎 World Cup 2026 — Quick Facts")

f1, f2, f3, f4 = st.columns(4)
f1.markdown('<div class="stat-card"><div class="stat-num">48</div><div class="stat-label">Teams</div></div>', unsafe_allow_html=True)
f2.markdown('<div class="stat-card"><div class="stat-num">104</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
f3.markdown('<div class="stat-card"><div class="stat-num">16</div><div class="stat-label">Host Cities</div></div>', unsafe_allow_html=True)
f4.markdown('<div class="stat-card"><div class="stat-num">3</div><div class="stat-label">Host Nations</div></div>', unsafe_allow_html=True)

# How it works


with st.expander("🔬 How does this predictor work?"):
    st.markdown("""
    **Data**: ~32,000 international matches from 1990–2024 (Kaggle / martj42 dataset).

    **Features the model uses:**
    - Home and away team identity (from historical records)
    - Each team's rolling win rate over their last 10 matches
    - Difference in form between the two teams
    - Head-to-head win rate between these specific opponents
    - Whether the match is at a neutral venue

    **Models tested**: Logistic Regression, KNN, Random Forest, Gradient Boosting.
    Best performer selected automatically.

    **Accuracy**: ~54–55% on held-out test data.
    This is realistic — football is inherently unpredictable.
    A 33% baseline (random guess between 3 outcomes) is the floor.

    **Debut nations** (Cabo Verde, Curaçao, Jordan, Uzbekistan) may have limited
    historical data — predictions for them use available records where possible.
    """)

st.markdown('<div class="footer">Built with Python · scikit-learn · Streamlit &nbsp;|&nbsp; World Cup 2026 Data Science Project</div>', unsafe_allow_html=True)