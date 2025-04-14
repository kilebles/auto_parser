import asyncio
import logging
from datetime import datetime, timedelta

from auto_parser.api_fetcher import fetch_cars_from_api
from auto_parser.parser import parse_cars_from_html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    start_date = datetime.strptime("2025-04-14", "%Y-%m-%d")
    months = 3
    step_days = 3

    end_date = start_date + timedelta(days=months * 30)
    current = start_date

    while current < end_date:
        to_date = current + timedelta(days=step_days)
        from_str = current.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")

        logger.info(f"\n Period: {from_str} -> {to_str}")

        cars = await fetch_cars_from_api(from_str, to_str)

        if not cars:
            logger.info("No cars available")
        else:
            for car in cars:
                logger.info(f"🚗 {car}")

        current = to_date


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("\n Process interrupted by user.")