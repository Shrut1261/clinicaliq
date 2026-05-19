# Deployment Plan

## Local

```powershell
python -m pip install -e ".[dev,app]"
docker compose up -d
python -m pytest
uvicorn clinicaliq.apps.api.main:app --reload
streamlit run src/clinicaliq/apps/dashboard/streamlit_app.py
```

## Public Portfolio Deployment

- Database: Neon Postgres or Railway Postgres
- API: Railway or Fly.io
- Dashboard: Streamlit Community Cloud
- Synthetic data only: never upload real patient data

