# MyCurrency

**MyCurrency** is application for managing currencies, retrieving historical exchange rates and performing currency conversions.

This README includes instructions for both local development using virtualenv and Docker-based deployment.
- To run **locally**, use the **main branch** with virtualenv.
- To run with **Docker**, switch to the **my-currency-docker** branch.

---

## Requirements

- Python 3.11+
- pip
- virtualenv (local setup)
- Docker (containerized deployment)
- Postman (API testing)
- CurrencyBeacon API key
---

## Local Setup (virtualenv)

### 1. Create and activate virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows/PowerShell
source .venv/bin/activate # macOS/Linux
```

### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a **.env** file in the root folder:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
CURRENCYBEACON_API_KEY=your_api_key
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```

### 6. Run server
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000.

## Docker Setup 

### 1.  Build Docker image
```bash
docker build -t mycurrency-backend .
```

### 2. Run Docker container
```bash
docker run -p 8000:8000 mycurrency-backend
```
Visit http://127.0.0.1:8000.

## API Endpoints (v1)

| Endpoint                                                                                  |  Description                      |
|-------------------------------------------------------------------------------------------|--------------------------------|
| `/api/v1/currencies/`                                                                     |  List all currencies             |
| `/api/v1/rates/?source_currency=EUR&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`              |  Get historical exchange rates  |
| `/api/v1/convert/?source_currency=EUR&exchanged_currency=USD&amount=10`                   |  Convert currency amounts        |

## API Testing with Postman

1. Open Postman.
2. Import the file `postman_collection.json` from `postman` directory.
3. Set the variable `base_url` to `http://127.0.0.1:8000`.
4. Send requests to the API endpoints.

## API Endpoints with Responses
- ### List all currencies

**GET** `{{base_url}}/api/v1/currencies`

Example Response:

```json
[
    {
        "id": 1,
        "code": "EUR",
        "name": "Euro",
        "symbol": "€"
    },
    {
        "id": 2,
        "code": "USD",
        "name": "US Dollar",
        "symbol": "$"
    }
]
```

- ###  Get historical exchange rates

**GET** `{{base_url}}/api/v1/rates?source_currency=EUR&date_from=2025-01-01&date_to=2025-01-05`

Example Response:

```json
[
    {
        "date": "2025-01-01",
        "rates": {
            "USD": 1.036952
        }
    },
    {
        "date": "2025-01-02",
        "rates": {
            "USD": 1.026929
        }
    },
    {
        "date": "2025-01-03",
        "rates": {
            "USD": 1.03098
        }
    },
    {
        "date": "2025-01-04",
        "rates": {
            "USD": 1.031129
        }
    },
    {
        "date": "2025-01-05",
        "rates": {
            "USD": 1.031636
        }
    }
]
```

- ### Convert currency amount

**GET** `{{base_url}}/api/v1/convert?source_currency=EUR&exchanged_currency=USD&amount=10`

Example Response:

```json
{
    "source_currency": "EUR",
    "exchanged_currency": "USD",
    "rate": 1.134777,
    "amount": 10.0,
    "converted_amount": 11.347769999999999
}
```


## Useful  Commands

Load historical exchange rates:
```bash
python manage.py load_history --src EUR --tgt USD --from 2025-01-01 --to 2025-01-07
```

Import exchange rates from JSON file:
```bash
python manage.py import_history path/to/data.json
```

## Currency Converter Admin Page

You can perform currency conversions directly in the Django admin panel.

- **URL:** [http://127.0.0.1:8000/admin/currencies/currency/converter/](http://127.0.0.1:8000/admin/currencies/currency/converter/)
- Requires admin login.



