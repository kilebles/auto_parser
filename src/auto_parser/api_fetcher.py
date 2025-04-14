import httpx
import pprint

BASE_URL = "https://localrent.com/api/cars/"


async def fetch_cars_from_api(from_date: str, to_date: str) -> list[str]:
    params = {
        "key": "localrent",
        "signature": "b7805902da22c24ce9d3eaa69d35ca5c",
        "locale": "ru",
        "limit": "100",
        "pickup_date": from_date,
        "dropoff_date": to_date,
        "pickup_city_id": "106531",   # Тбилиси
        "dropoff_city_id": "106531",

        "age": 30,
        "driving_license_age": 5,
        "cost_min": 1,
        "cost_max": 100000,
        "engine_min": 0.0,
        "engine_max": 6.2,
        "consumption_min": 0.0,
        "consumption_max": 25.0,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # pprint.pprint(data.get("cars", [])[0], width=120)
        print(f"✅ Найдено машин: {len(data.get('cars', []))}")

        return [car.get("full_name", "unknown") for car in data.get("cars", [])]

