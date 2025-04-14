import asyncio
import pandas as pd
import logging

from datetime import datetime, timedelta
from collections import defaultdict

from auto_parser.api_fetcher import fetch_cars_from_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_car_ids_by_day(date: datetime) -> list[tuple[int, str]]:
    from_date = date.strftime("%Y-%m-%d")
    to_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    from auto_parser.api_fetcher import BASE_URL
    import httpx

    params = {
        "key": "localrent",
        "signature": "b7805902da22c24ce9d3eaa69d35ca5c",
        "locale": "ru",
        "limit": "100",
        "pickup_date": from_date,
        "dropoff_date": to_date,
        "pickup_city_id": "106531",
        "dropoff_city_id": "106531",
        "age": 30,
        "driving_license_age": 5,
        "cost_min": 1,
        "cost_max": 100000,
        "engine_min": 0.0,
        "engine_max": 6.2,
        "consumption_min": 0.0,
    }

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(BASE_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                return [(car["id"], car["full_name"]) for car in data.get("cars", [])]

        except httpx.ConnectError as e:
            logger.warning(f"⚠️ Ошибка подключения на {from_date}: {e}")
            await asyncio.sleep(3 + attempt)

    logger.error(f"❌ Пропускаем {from_date} — не удалось получить данные")
    return []


async def generate_matrix(days: int = 30):
    today = datetime.today()
    all_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    matrix = defaultdict(lambda: [0] * days)
    car_names = {}

    for i, day_str in enumerate(all_dates):
        logger.info(f"📅 Обрабатываю: {day_str}")
        cars = await fetch_car_ids_by_day(today + timedelta(days=i))
        for car_id, full_name in cars:
            matrix[car_id][i] = 1
            car_names[car_id] = full_name

    df = pd.DataFrame.from_dict(matrix, orient="index", columns=all_dates)
    df.insert(0, "Car", [car_names[i] for i in df.index])
    df = df.sort_index()

    df.to_excel("car_availability_matrix.xlsx", index_label="Car ID")
    logger.info("✅ Таблица сохранена в car_availability_matrix.xlsx")
