# House Price Prediction

An end-to-end Machine Learning project for predicting house prices featuring a FastAPI backend, modern React frontend, and exploratory Jupyter notebooks.

## Project Structure

```text
house-price-project/
├── .gitignore
├── README.md
├── notebooks/
│   ├── data/
│   │   └── house_prices.csv
│   ├── house_price_model.ipynb
│   ├── house_price.pkl
│   └── locations.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── prediction.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── prediction.py
│   │   ├── services/
│   │   │   ├── preprocessing.py
│   │   │   └── inference.py
│   │   ├── utils/
│   │   │   └── logging_config.py
│   │   └── main.py
│   ├── models/
│   │   └── house_price.pkl
│   ├── tests/
│   │   └── test_prediction.py
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── predictionClient.ts
    │   ├── components/
    │   │   └── PredictionForm.tsx
    │   ├── pages/
    │   │   ├── HomePage.tsx
    │   │   ├── ResultPage.tsx
    │   │   └── NotFoundPage.tsx
    │   ├── types/
    │   │   └── prediction.ts
    │   └── App.tsx
    ├── .env
    └── .env.example
```

## Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
