from RPA.HTTP import HTTP
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class NewsSearcher:
    def __init__(self, app_maanager, item_payload):
        self.output_path = app_maanager.output_path
        self.url = app_maanager.url
        self.sort_type = app_maanager.sort_type

        self.search_phrase = item_payload["search_phrase"].strip()
        self.topic = item_payload["topic"].strip()

        self.browser = app_maanager.browser
        self.locators = app_maanager.locators
        self.validator = app_maanager.validator
        self.logger = app_maanager.logger
        self.http = HTTP()

    def do_search_phrase(self):
        """Click search button, input search text and click submit button"""
        self.logger.info(f"Search phrase: {self.search_phrase}")

        self.browser.click_button(self.locators.search_btn())
        self.browser.input_text(self.locators.input_search(), self.search_phrase)
        self.browser.click_button(self.locators.submit_search_btn())
        self.browser.wait_until_page_contains_element(
            self.locators.results(), error="Results page didn't load", timeout=15
        )

    def choose_topic(self):
        """Click see all topics button and select a topic"""
        self.logger.info(f"Choosing topic: {self.topic}")
        try:
            self.browser.click_element(self.locators.see_all_topics())

            if self.browser.get_webelement(self.locators.topic(self.topic)):

                self.browser.select_checkbox(self.locators.topic(self.topic))
                self.logger.info("Topic checked")
        except:
            raise NoSuchElementException("Topic not found!")

    def sort_by(self):
        self.logger.info(f"Sorting by {self.sort_type}")
        self.browser.wait_until_element_is_enabled(self.locators.sort())
        self.browser.select_from_list_by_label(self.locators.sort(), self.sort_type)

    def perform_news_search(self):
        try:
            self.do_search_phrase()
            self.choose_topic()
            sleep(5)
            self.sort_by()
            sleep(5)

        except TimeoutException as e:
            self.logger.exception(f"Timeout occurred during news search: {e}")
            raise TimeoutException(e)

        except NoSuchElementException as e:
            self.logger.exception(f"Element not found during news search: {e}")
            raise NoSuchElementException(e)

        except Exception as e:
            self.logger.exception(f"Error during news search: {e}")
            raise Exception(e)
