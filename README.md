# CityFlow Backend

FastAPI backend for the Delhi NCR mobility platform.

## What is already scaffolded

- FastAPI API layer under `/api/v1`
- Pydantic request/response schemas
- SQLAlchemy async persistence
- Alembic migration support
- Configurable CORS for local + deployed frontend origins
- Delhi NCR-only region validation
- Provider abstraction for traffic, incidents, routing, weather, transit, safety and prediction
- TomTom adapters for traffic, incident and vehicle routing integrations
- Open-Meteo weather + air-quality integration
- Deterministic transit/safety/prediction adapters until real GTFS/ML components are installed
- Vehicle CRUD, saved routes, preferences and user profile endpoints

## Provider modes

`PROVIDER_MODE=mock` uses deterministic local data.

`PROVIDER_MODE=hybrid` uses TomTom/Open-Meteo for traffic, incidents, routing and weather while keeping transit, safety and prediction on the local adapters.

`PROVIDER_MODE=live` uses the same real-provider integrations and is intended for deployment once all required integrations are configured.

## Local run

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

alembic upgrade head
uvicorn app.main:app --reload
```



## Frontend CORS

Set `FRONTEND_ORIGIN` to the exact frontend origin. Multiple origins can be comma-separated, for example:

```env
FRONTEND_ORIGIN=http://localhost:3000,https://cityflow.example.com
```

For Vercel + EC2, put the Vercel production URL in the EC2 environment.

## Real providers

TomTom traffic flow, incidents and routing are called server-side; the TomTom API key never belongs in the frontend.

Open-Meteo supplies weather and air-quality values. Open-Meteo documents `/v1/forecast` for weather and `/v1/air-quality` for AQI/pollutants. See their current documentation for request parameters and attribution requirements. 

## Next integrations

1. Replace mock transit with a Delhi NCR GTFS/journey-planner provider.
2. Add the traffic prediction model and persistence of model inputs/outputs.
3. Add the accident-risk model and hotspot persistence.
4. Enable Supabase Auth/JWT verification when the frontend auth flow is connected.
5. Move the production `DATABASE_URL` to Supabase PostgreSQL.
