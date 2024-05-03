from datetime import datetime
from RPA.Excel.Files import Files

import os


class SaveData:
    def __init__(self, app_manager):
        self.app_manager = app_manager
        self.excel = Files()
        

    def create_excel_file(self, data, search_phrase: str):
        try:
            logger = self.app_manager.logger
            logger.info("Creating Excel file")
            output_path = self.app_manager.output_path
            
            todays_date = datetime.now().strftime("%Y-%m-%d")

            #output_path = os.path.join(output_path, todays_date, search_phrase.lower())  
            filename = f"fresh_news_{search_phrase}_{todays_date}.xlsx"

            # Check if output_path exists, if not create it
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            self.excel.create_workbook(os.path.join(output_path, filename))
            self.excel.create_worksheet("fresh_news", content=data, header=True)
            self.excel.save_workbook()
        except Exception as e:
            logger.exception(f"Error creating Excel file:", e)
            raise Exception(f"Error creating Excel file:", e)

        logger.info("Saved Excel file")
