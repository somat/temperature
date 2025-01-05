# Temperature

A very simple FastAPI-based REST API app for IoT applications to send and process temperature and humidity data.

* APIKeyHeader is used to validate requests with a header named `X-API-KEY`.
* POST `/api/data`: Receives JSON payload from the IoT device and saves it to the database.
* Run the server with `uvicorn main:app --reload`.
