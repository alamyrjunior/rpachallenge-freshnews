from robocorp.tasks import task
from robocorp import workitems
from src.process.search_news import NewsSearcher
from src.process.scrape_news import ScrapeNews
from src.process.save_data import SaveData
from src.apps.app_manager import ApplicationManager


@task
def run_process():
    
    app_manager = ApplicationManager()
    app_manager.initialize()
    logger = app_manager.logger

    for item in workitems.inputs:
        try:
            payload = app_manager.validator.validate_payload(item.payload)
            logger.info(f"Item payload: {payload}")

            search_news = NewsSearcher(app_manager, payload)
            scrape_news = ScrapeNews(app_manager, payload)
            save_data = SaveData(app_manager)

            search_news.perform_news_search()
            data = scrape_news.scrape_news()
            save_data.create_excel_file(data, payload["search_phrase"])

            item.done()
            logger.info(f"Scrape of phrase '{payload['search_phrase']}' finished.")

        except Exception as e:
            item.fail(message=f"Error: {e}")
            logger.error(f"Error scraping fresh news: {str(e)}")
            raise Exception(e)

    app_manager.end_process()
    logger.info("Finishing process: Scrape Fresh News...")
