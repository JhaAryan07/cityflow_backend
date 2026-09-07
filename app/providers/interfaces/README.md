# Provider integration boundary

These protocols are the only place where future external data-source implementations need to conform to CityFlow.

Replace the active mock implementation later for traffic, routing, transit, weather, incidents, or safety data. Do not place vendor SDK calls in FastAPI routes.

The prediction interface is a contract boundary for the future ML service. The current implementation is `MockPredictionProvider`; it performs no model inference and does not load `.joblib` files.
