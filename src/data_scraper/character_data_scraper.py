import argparse
import csv
import json
import os
import pickle

import tqdm
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def read_character_list(input_file):
    with open(input_file, 'r') as json_file:
        character_data = json.load(json_file)

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

        # This was added because in previous version we didn't scroll on each page and so we didn't get the whole data
        # We now have to repair those character data
        new_character_data = {}
        go = False
        for character_name in character_data.keys():
            if "" in character_data[character_name]:
                del character_data[character_name][""]
                new_character_data[character_name] = character_data[character_name].copy()

        error_characters = {}

        progress_bar = tqdm.tqdm(new_character_data.keys(),
                                 bar_format='{desc:<25.25}{percentage:3.0f}%|{bar:10}{r_bar}')

        for name in progress_bar:
            progress_bar.set_description(f"{name}")
            link = character_data[name]['link']

            try:
                self.driver.get(link)
                try:
                    self.resolve_cookies()
                except Exception as e:
                    tqdm.tqdm.write(f'{name} caused COOKIE an error!')
                    self.accept_cookies = True
                    self.resolve_cookies()

                # Get info box
                info_box = self.driver.find_element(By.CLASS_NAME, 'infobox')
                # Get all the information from infobox, that contains data about character
                rows = info_box.find_elements(By.XPATH,
                                              '//*[@id="mw-content-text"]/div/table[1]/tbody//tr[descendant::th['
                                              '@scope=\'row\']]')

                # Loop through rows and save the key-value pairs to data collection
                for row in rows:
                    # Find header element of current row in infobox table
                    header_element = row.find_element(By.XPATH, 'th')

                    # We need to scroll to the header element
                    actions = ActionChains(self.driver)
                    actions.move_to_element(header_element).perform()

                    try:
                        data_element = row.find_elements(By.XPATH, './td//li')
                        if len(data_element) > 0:
                            links = []
                            values = []
                            for element in data_element:
                                element_link = element.find_elements(By.XPATH, './/a')
                                if len(element_link) == 0:
                                    element_link = ''
                                else:
                                    element_link = element_link[0].get_attribute('href')
                                element_value = element.text

                                values.append(element_value)
                                links.append(element_link)

                            character_data[name][header_element.text] = {
                                'values': values,
                                'links': links
                            }
                        else:
                            data_element = row.find_element(By.XPATH, './td')
                            element_link = data_element.find_elements(By.XPATH, './/a')
                            if len(element_link) == 0:
                                element_link = ''
                            else:
                                element_link = element_link[0].get_attribute('href')
                            element_value = data_element.text
                            character_data[name][header_element.text] = {
                                'value': element_value,
                                'link': element_link
                            }

                    except Exception as e:
                        tqdm.tqdm.write(f'{name} caused ELEMENT NOT FOUND an error!')

            except Exception as e:
                error_characters[name] = e
                tqdm.tqdm.write(f'{name} caused an error! {e}')
                break

        self.driver.quit()

        # Save character data
        with open(output_file, "w") as outfile:
            json.dump(character_data, outfile)


def main():
    parser = argparse.ArgumentParser(description='Tracking Visualization Utility')

    parser.add_argument('--input_path', help='Path for the input list of characters and links to their wiki pages.',
                        default='../../data/character_data.json', type=str)
    parser.add_argument('--output_path', help='Path for the output list of characters and links to their wiki pages.',
                        default='../../data/character_data_new.json', type=str)
    parser.add_argument('--debug_mode', help='If True it will always open a browser window.', default=False, type=bool)

    args = parser.parse_args()

    scraper = Scraper()
    scraper.scrape_character_list(args.input_path, args.output_path)


if __name__ == "__main__":
    main()
