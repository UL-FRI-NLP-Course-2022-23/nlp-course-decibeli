import argparse
import csv
import json
import pickle

import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def read_character_list(input_file):
    character_data = {}
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            name, link = row

            character_data[name] = {}
            character_data[name]['link'] = link

    return character_data


class Scraper:

    def __init__(self, debug_mode=False):
        self.accept_cookies = True
        self.driver = None
        self.options = None
        self.debug_mode = debug_mode
        self.init_driver()

    def init_driver(self):
        self.options = uc.ChromeOptions()
        if not self.debug_mode:
            self.options.add_argument('-headless')
            self.options.add_argument("--window-size=1920,1200")

        # self.options.headless = False
        self.options.add_argument('--disable-browser-side-navigation')
        self.driver = uc.Chrome(use_subprocess=True, options=self.options)

    def resolve_cookies(self):
        # First time on page we need to accept cookies and save them
        if self.accept_cookies:
            # switch to the iframe and then click the link
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'sp_message_iframe_633212'))
            )
            self.driver.switch_to.frame(iframe)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[5]/button[2]'))
            ).click()

            self.driver.switch_to.default_content()
            self.accept_cookies = False
            pickle.dump(self.driver.get_cookies(), open("tmp_data/cookies.pkl", "wb"))

        # If we already accepted cookies we can read them from file
        else:
            cookies = pickle.load(open("tmp_data/cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def scrape_character_list(self, input_file, output_file):
        character_data = read_character_list(input_file)

        error_characters = {}

        progress_bar = tqdm.tqdm(character_data.keys(), bar_format='{desc:<25.25}{percentage:3.0f}%|{bar:10}{r_bar}')

        for name in progress_bar:
            progress_bar.set_description(f"{name}")
            link = character_data[name]['link']

            try:
                self.driver.get(link)

                # Get info box
                info_box = self.driver.find_element(By.CLASS_NAME, 'infobox')
                # Get all the information from infobox, that contains data about character
                rows = info_box.find_elements(By.XPATH,
                                              '//*[@id="mw-content-text"]/div/table[1]/tbody//tr[descendant::th['
                                              '@scope=\'row\']]')

                # Loop through rows and save the key-value pairs to data collection
                for row in rows:
                    header = row.find_element(By.XPATH, 'th')
                    value = row.find_element(By.XPATH, 'td')

                    character_data[name][header.text] = value.text.split('\n')

            except Exception as e:
                error_characters[name] = e
                tqdm.tqdm.write(f'{name} caused an error!')

        self.driver.quit()

        # Save character data
        with open(output_file, "w") as outfile:
            json.dump(character_data, outfile)


def main():
    parser = argparse.ArgumentParser(description='Tracking Visualization Utility')

    parser.add_argument('--input_path', help='Path for the input list of characters and links to their wiki pages.',
                        default='../../data/character_link_list.csv', type=str)
    parser.add_argument('--output_path', help='Path for the output list of characters and links to their wiki pages.',
                        default='../../data/character_data.json', type=str)
    parser.add_argument('--debug_mode', help='If True it will always open a browser window.', default=False, type=bool)

    args = parser.parse_args()

    scraper = Scraper()
    scraper.scrape_character_list(args.input_path, args.output_path)


if __name__ == "__main__":
    main()
