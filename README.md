# 🏠 Propeak — Gurgaon Real Estate Analytics & Price Prediction

A full end-to-end data science project that scrapes, cleans, analyzes, and models residential property data from Gurgaon, India. Culminates in an interactive **Streamlit web app** with analytics dashboards and an ML-powered price predictor.

---

## 📌 Project Overview

Propeak ingests raw property listings (flats and houses) from Gurgaon, runs them through a multi-stage preprocessing and feature engineering pipeline, evaluates 11 regression models, and deploys the best-performing model as a user-facing web application.

**Core capabilities:**
- Interactive geospatial analytics by sector
- Price prediction with confidence range (±0.22 Cr)
- BHK composition, area-vs-price, and furnishing breakdowns
- Feature word cloud from property descriptions

---

## 🗂️ Project Structure

```
Propeak-Real-Estate/
│
├── Real_Estate_App/                  # Streamlit application
│   ├── Home.py                       # App entry point
│   └── pages/
│       ├── Analysis_App.py           # Analytics dashboard
│       └── Price_predictor.py        # Price prediction page
│
├── Data & Notebooks (Pipeline Order)
│   ├── gurgaon_properties.csv                        # Raw dataset
│   ├── flats.csv / houses.csv                        # Property-type splits
│   ├── flats.ipynb / houses.ipynb                    # Type-specific cleaning
│   ├── data_preprocessing.ipynb                      # Core preprocessing
│   ├── eda-univariate-analysis.ipynb                 # Univariate EDA
│   ├── eda-multivariate-analysis.ipynb               # Multivariate EDA
│   ├── eda-pandas-profiling.ipynb                    # Profiling report
│   ├── missing-value-imputation.ipynb                # Imputation
│   ├── outlier-removal.ipynb                         # Outlier treatment
│   ├── feature-engineering.ipynb                     # Feature creation
│   ├── feature-selection.ipynb                       # Feature selection
│   ├── Baseline_model.ipynb                          # Baseline modelling
│   ├── model-selection.ipynb                         # Model comparison
│   └── output_report.html                            # Pandas profiling HTML report
│
└── Cleaned Data Versions
    ├── gurgaon_properties_cleaned_v1.csv
    ├── gurgaon_properties_cleaned_v2.csv
    ├── gurgaon_properties_missing_value_imputation.csv
    ├── gurgaon_properties_outlier_treated.csv
    └── gurgaon_properties_post_feature_selection.csv
```

---

## 🔬 ML Pipeline

### Data
- **Source:** `gurgaon_properties.csv` — raw property listings for Gurgaon, Haryana
- **Property types:** Flats and houses (processed separately then merged)
- **Key features:** `property_type`, `sector`, `bedRoom`, `bathroom`, `balcony`, `agePossession`, `built_up_area`, `servant room`, `store room`, `furnishing_type`, `luxury_category`, `floor_category`

### Preprocessing Steps
1. Type-specific cleaning (flats & houses notebooks)
2. Missing value imputation
3. Outlier removal
4. Feature engineering (luxury category, floor category, furnishing type, etc.)
5. Feature selection

### Model Selection
11 regression models were evaluated using **10-fold cross-validation** (R² + MAE):

| Model | Notes |
|---|---|
| Linear Regression | Baseline |
| Ridge | L2 regularization |
| Lasso | L1 regularization |
| SVR | Support Vector Regression |
| Decision Tree | |
| Random Forest | |
| Extra Trees | |
| Gradient Boosting | |
| AdaBoost | |
| MLP (Neural Net) | |
| **XGBoost** | Final deployed model |

The final `pipeline.pkl` wraps the best model with a `ColumnTransformer` (OneHotEncoder + OrdinalEncoder + StandardScaler) for clean end-to-end inference.

---

## 📊 App Features

### Analytics Page
- **Sector Geomap** — Plotly scatter map showing price per sqft by sector with built-up area as bubble size
- **Feature Word Cloud** — Most common amenities/features across all listings
- **Area vs Price** — Scatter plot by property type and bedroom count
- **BHK Pie Chart** — Bedroom distribution, filterable by sector
- **BHK Price Range** — Box plot comparing price ranges across 1–4 BHK units
- **Property Type Distribution** — KDE/distplot for house vs flat prices

### Price Predictor Page
Input parameters:
- Property type, sector, bedrooms, bathrooms, balconies
- Property age, built-up area, servant/store room
- Furnishing type, luxury category, floor category

Output: `"The price of the flat is between X Cr and Y Cr"` (±0.22 Cr range)

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| EDA | Plotly, Seaborn, Matplotlib, ydata-profiling |
| ML | Scikit-learn, XGBoost |
| NLP / Viz | WordCloud |
| Web App | Streamlit |
| Geospatial | Plotly Express (scatter_mapbox, OpenStreetMap) |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install streamlit pandas numpy scikit-learn xgboost plotly matplotlib seaborn wordcloud ydata-profiling
```

### Run the App
```bash
cd Real_Estate_App
streamlit run Home.py
```

The app will open at https://anubhavspeaks01-propeak-real-estate--real-estate-apphome-rfjubq.streamlit.app/. Use the sidebar to navigate between **Analytics** and **Price Predictor** pages.

> **Note:** The app expects `df.pkl`, `pipeline.pkl`, `datasets/data_viz1.csv`, and `datasets/feature_text.pkl` to be present in the working directory. Generate these by running the notebooks in order.

### Run Notebooks (in order)
```
1. flats.ipynb / houses.ipynb
2. data_preprocessing.ipynb
3. eda-*.ipynb  (optional, for analysis)
4. missing-value-imputation.ipynb
5. outlier-removal.ipynb
6. feature-engineering.ipynb
7. feature-selection.ipynb
8. model-selection.ipynb  → exports pipeline.pkl
```

---

## 🔮 Roadmap

- [ ] Expand to other Indian cities (Mumbai, Bangalore, Pune)
- [ ] Add independent floors and residential plots
- [ ] Add commercial property support
- [ ] Recommender system (suggest similar properties)
- [ ] Improve prediction accuracy with hyperparameter tuning
- [ ] Add a data refresh pipeline for live listings

---

## 👥 Contributors

- Anubhav
- Amit
- Nisa
- Binal
