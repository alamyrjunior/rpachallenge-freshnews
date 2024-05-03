class Locators:
    @staticmethod
    def search_btn():
        return "//button[@data-element='search-button']"

    @staticmethod
    def input_search():
        return "//input[@placeholder='Search']"

    @staticmethod
    def submit_search_btn():
        return "//button[@data-element='search-submit-button']"

    @staticmethod
    def topic(topic):
        return f"//span[text()='{topic}']/ancestor::label/input[@type='checkbox']"

    @staticmethod
    def see_all_topics():
        return "(//span[contains(@class,'see-all-text')])[1]"

    @staticmethod
    def sort():
        return "//select[@class='select-input']"

    @staticmethod
    def results():
        return "//ul[@class='search-results-module-results-menu']/li"

    @staticmethod
    def heading(index):
        return f"//ul[@class='search-results-module-results-menu']/li[{index}]//h3[@class='promo-title']/a"

    @staticmethod
    def description(index):
        return f"//ul[@class='search-results-module-results-menu']/li[{index}]//p[@class='promo-description']"

    @staticmethod
    def date(index):
        return f"//ul[@class='search-results-module-results-menu']/li[{index}]//p[@class='promo-timestamp']"

    @staticmethod
    def picture(index):
        return f"//ul[@class='search-results-module-results-menu']/li[{index}]//picture/img"

    @staticmethod
    def picture_attr():
        return "src"

    @staticmethod
    def next_page():
        return "//div[@class='search-results-module-next-page']/a"
