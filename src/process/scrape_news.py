from time import sleep
from datetime import datetime
import os


class ScrapeNews:
    def __init__(self, app_manager, item_payload):
        self.app_manager = app_manager
        self.max_news = item_payload["max_news"]
        self.n_months = item_payload["n_months"]
        self.search_phrase = item_payload["search_phrase"].strip()
        self.output_path = app_manager.output_path
        self.http = app_manager.http

    def scrape_news(self):
        browser = self.app_manager.browser
        locators = self.app_manager.locators
        validator = self.app_manager.validator
        logger = self.app_manager.logger

        news_counter = 1
        page = 1
        data = []
        has_finished = False
        logger.info("Starting scrape")
        while news_counter <= self.max_news and not has_finished:

            if news_counter > 1:
                page = self._next_page(browser, locators, page)

            if page == 0:
                break

            search_results = browser.find_elements(locators.results())

            for news_index, news in enumerate(search_results, 1):
                try:
                    logger.info(f"Starting scraping of news: {str(news_counter)}")

                    # Validate limit date and scrape news data
                    news_date = browser.get_text(locators.date(news_index))
                    has_finished = validator.validate_date_limit(
                        news_date, self.n_months
                    )

                    if has_finished:
                        break

                    news_heading = browser.get_text(locators.heading(news_index))
                    news_description = browser.get_text(
                        locators.description(news_index)
                    )
                    picture_url = browser.get_element_attribute(
                        locators.picture(news_index), locators.picture_attr()
                    )

                    logger.info("Starting validations for news")
                    # Validate phrases count and if it has monetary values
                    heading_phrases_count = validator.count_phrase_occurrences(
                        self.search_phrase, news_heading
                    )
                    description_phrases_count = validator.count_phrase_occurrences(
                        self.search_phrase, news_description
                    )
                    has_monetary_values = validator.has_monetary_values(
                        [news_heading, news_description]
                    )

                    # Download picture and save it
                    picture_path = self._download_picture(
                        picture_url, self.search_phrase, news_counter
                    )

                    # Create dictionary and append it to the data array
                    result = {
                        "Heading": news_heading,
                        "Description": news_description,
                        "Date": news_date,
                        "Phrases in Heading": heading_phrases_count,
                        "Phrases in Description": description_phrases_count,
                        "Has Money Amount": has_monetary_values,
                        "Picture Path": picture_path,
                    }
                    data.append(result)
                    logger.info("News appended to data successfully.")

                    news_counter += 1

                except Exception as e:
                    news_counter += 1
                    logger.exception(f"Error scraping news {news_index}: {str(e)}")
                    continue

        return data

    def _next_page(self, browser, locators, page):
        try:
            logger = self.app_manager.logger
            page += 1
            logger.info(f"Going to next page: {str(page)}")

            browser.click_element(locators.next_page())
            sleep(4)

            location = browser.get_location()
            if not location.endswith(str(page)):
                logger.exception("Couldn't find next page")
                raise Exception("Couldn't find next page")

            return page

        except:
            logger.info("No next page found, scrapping is finished.")
            return 0

    def _download_picture(self, picture_url, search_phrase, news_counter):
        logger = self.app_manager.logger
        logger.info("Downloading picture...")
        todays_date = datetime.now().strftime("%Y-%m-%d")
        # output_path = os.path.join(self.output_path, todays_date, search_phrase, "pictures")

        picture_name = f"news_pic_{search_phrase}_{todays_date}_{news_counter}.jpg"
        picture_path = os.path.join(self.output_path, picture_name)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.http.download(picture_url, picture_path)

        return picture_path
