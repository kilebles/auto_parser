import httpx
import asyncio
import json

async def fetch_filters():
    url = "https://localrent.com/api/filters"
    params = {
        "country_id": "124",  # Грузия
        "pickup_city_id": "106531",
        "dropoff_city_id": "106531",
        "locale": "ru",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        with open("filters.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

asyncio.run(fetch_filters())
