from datetime import datetime
from dateutil.relativedelta import relativedelta
from loguru import logger
import re


class DataValidator:
    def validate_date_limit(self, news_date: str, months_to_scrape: int) -> bool:
        logger.info(f"validating limit date for: {news_date}")

        if "minute" in news_date or "hour" in news_date:
            return False

        news_date = self._try_parse_date(news_date)

        limit_date = datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        if months_to_scrape > 1:
            limit_date = limit_date - relativedelta(months=(months_to_scrape - 1))

        if news_date < limit_date:

            logger.info(
                f"This news date '{news_date}' is not within the limit date '{limit_date}', finishing scrape..."
            )
            return True

        return False

    def _try_parse_date(self, news_date: str) -> datetime:
        logger.info(f"Trying to parse date: {news_date}")
        date_formats = ["%B %d, %Y", "%B. %d, %Y", "%b. %d, %Y"]

        for fmt in date_formats:
            try:
                news_date = datetime.strptime(news_date, fmt)
                return news_date
            except ValueError:
                continue

        raise ValueError(f"No valid date format found for {news_date}")

    def count_phrase_occurrences(self, phrase: str, string: str) -> int:
        count = string.lower().split().count(phrase.lower())
        return count

    def has_monetary_values(self, arr: list) -> bool:
        pattern = r"\$[\d,]+(\.\d+)?\b|\b\d+\s*(dollars|USD)\b"
        for string in arr:
            matches = re.findall(pattern, string)
            if matches:
                return True

        return False

    def validate_payload(self, payload: dict) -> bool:
        if not payload:
            raise Exception("Payload is empty.")

        expected_template = {
            "search_phrase": str,
            "topic": str,
            "n_months": int,
            "max_news": int,
        }

        missing_keys = [key for key in expected_template if key not in payload]
        if missing_keys:
            missing_key = missing_keys[0]
            raise Exception(f"Missing key '{missing_key}' in payload")

        for key, value in expected_template.items():
            print(key, value)

            # Check if value is empty
            if payload[key] == "":
                raise Exception(f"Payload key {key} is empty.")

            if not isinstance(payload[key], value):
                try:
                    # Convert to right type
                    payload[key] = value(payload[key])
                except ValueError:
                    raise Exception(f"Payload key {key} is not of type {value}.")

        return payload
