# Temperature

A very simple FastAPI-based REST API app for IoT applications to send and process temperature and humidity data.

* APIKeyHeader is used to validate requests with a header named `X-API-KEY`.
* POST `/api/data`: Receives JSON payload from the IoT device and saves it to the database.

## Database Setup
This application requires a MariaDB database with the following configuration:

- **Database Name**: `temperature`
- **Table Name**: `monitor`
- **Table Structure**:
  - `id` (Integer, Primary Key, Auto Increment)
  - `created_at` (Datetime, Default: Current Timestamp)
  - `temperature` (Float, Not Null)
  - `humidity` (Float, Not Null)

- **Example SQL to Create the Database and Table**:
```sql
CREATE DATABASE temperature;

USE temperature;

CREATE TABLE monitor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL
);
```

## Environment Variables
The application reads configuration details from environment variables. These are stored in a `.env` file:

```plaintext
# Database configuration
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=temperature

# API Key for authentication
API_KEY=your_api_key
```

## Usage
The API includes endpoints for IoT devices to send data securely, which is stored in a database for further analysis and monitoring.

### Installation and Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up the database using the SQL script above.
3. Create a `.env` file with your configuration.
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Example Request
Use tools like Postman or an ESP32 device to send data:

```bash
curl -X POST "http://localhost:8000/api/data" \
-H "X-API-KEY: your_api_key" \
-H "Content-Type: application/json" \
-d '{"temperature": 25.5, "humidity": 60.2}'
```
