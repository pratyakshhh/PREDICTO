# ⚽ World Cup 2026 Match Predictor

> Predict match outcomes for all 48 FIFA World Cup 2026 nations using historical international football data and machine learning — deployed as an interactive web app.

**[🚀 Live Demo](YOUR_STREAMLIT_URL_HERE)**

---

## 📸 What it does

- Select any two of the **48 World Cup 2026 teams** from a dropdown
- Adjust each team's recent form using a slider
- Hit **Predict** and get:
  - Win / Draw / Loss prediction with confidence level
  - Probability breakdown across all three outcomes
  - Full **head-to-head historical record** between the two teams
  - Model performance metrics (Accuracy, F1 Score, ROC AUC)

---

## 🧠 How it works

### Data
- **~32,000 international football matches** from 1990–2024
- Source: [Kaggle — International football results from 1872](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017) by martj42

### Features engineered
| Feature | Description |
|---|---|
| `home_team_enc` | Home team encoded as integer |
| `away_team_enc` | Away team encoded as integer |
| `home_form` | Home team win rate over last 10 matches |
| `away_form` | Away team win rate over last 10 matches |
| `form_diff` | Difference in form between the two teams |
| `home_h2h_rate` | Home team's historical win rate vs this specific opponent |
| `is_neutral` | Whether the match is at a neutral venue (0 or 1) |

### Models compared
| Model | Test Accuracy |
|---|---|
| Gradient Boosting | ~54.5% |
| Random Forest | ~54.1% |
| Logistic Regression | ~53.8% |
| KNN | ~47.4% |

Best model selected automatically and saved for the app.

> 📊 ~54% accuracy is realistic for football — even professional bookmakers rarely exceed 65% on 3-outcome prediction. Random guessing gives 33%.

---

## 🗂️ Project structure

```
match-predictor/
├── app/
│   └── app.py                  ← Streamlit web app
├── data/
│   ├── raw/
│   │   └── results.csv         ← Raw Kaggle dataset
│   └── processed/
│       ├── clean_matches.csv   ← Cleaned data (Day 6)
│       └── features.csv        ← Feature engineered data (Day 7)
├── models/
│   ├── match_model.pkl         ← Trained best model
│   ├── team_encoder.pkl        ← LabelEncoder for team names
│   └── metrics.json            ← Accuracy, F1, ROC AUC scores
├── notebooks/
│   ├── 04_explore.ipynb        ← Day 5: data exploration
│   ├── 05_clean.ipynb          ← Day 6: data cleaning
│   ├── 06_features.ipynb       ← Day 7: feature engineering
│   └── 07_model.ipynb          ← Day 8: model training + comparison
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | ML models + evaluation |
| Matplotlib | Charts and visualizations |
| Streamlit | Web app framework |

---

## 🚀 Run locally

```bash
# Clone the repo
git clone https://github.com/YOURNAME/worldcup-2026-predictor.git
cd worldcup-2026-predictor

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/app.py
```

---

## 🌍 World Cup 2026 — 48 Teams

| Confederation | Teams |
|---|---|
| UEFA (16) | France, Spain, Germany, England, Portugal, Netherlands, Belgium, Croatia, Switzerland, Austria, Sweden, Norway, Scotland, Czechia, Bosnia & Herzegovina, Türkiye |
| CAF (10) | Morocco, Senegal, Egypt, Ghana, Tunisia, Algeria, South Africa, Côte d'Ivoire, DR Congo, Cabo Verde |
| AFC (9) | Japan, South Korea, Australia, Saudi Arabia, Iran, Qatar, Iraq, Jordan, Uzbekistan |
| CONMEBOL (6) | Argentina, Brazil, Colombia, Uruguay, Ecuador, Paraguay |
| CONCACAF (6) | USA, Mexico, Canada, Panama, Haiti, Curaçao |
| OFC (1) | New Zealand |

---

## 📚 What I learned

- Building a full **end-to-end ML pipeline** from raw data to deployed web app
- **Feature engineering** on time-series sports data without data leakage
- Comparing multiple classifiers and selecting the best performer programmatically
- Building an **interactive Streamlit dashboard** with custom dark theme
- Deploying a Python ML app on **Streamlit Cloud**

---

## 👤 About

Built as a **20-day data science learning project** starting from Python basics.

**Day 1–4**: Python, Pandas, visualization, ML fundamentals  
**Day 5–8**: Data exploration, cleaning, feature engineering, model training  
**Day 9–10**: Streamlit app, deployment, documentation  

---

*Data source: martj42 on Kaggle | Tournament: FIFA World Cup 2026, USA/Canada/Mexico*
