import argparse
import json

import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def scrape_character_list(output_file, debug_mode=False):

    options = Options()
    if not debug_mode:
        options.add_argument('-headless')
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Firefox(options=options)
    driver.get("https://awoiaf.westeros.org/index.php/List_of_characters")

    # switch to the iframe and then click the link
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sp_message_iframe_633212'))
    )

    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[5]/button[2]'))
    ).click()

    driver.switch_to.default_content()

    tmp = driver.find_element(By.CSS_SELECTOR, "#mw-content-text > div")
    list_items = tmp.find_elements(By.CSS_SELECTOR, 'li')

    character_data = {}
    print('Scraping list of characters and links...')
    for list_item in tqdm.tqdm(list_items):
        character_link_html = list_item.find_element(By.TAG_NAME, 'a')

        character_link = character_link_html.get_attribute("href")
        character_name = character_link_html.get_attribute("title")

        character_data[character_name] = {}
        character_data[character_name]['link'] = character_link

    driver.quit()

    # Save character data
    with open(output_file, "w") as outfile:
        json.dump(character_data, outfile, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Tracking Visualization Utility')

    parser.add_argument('--output_path', help='Path for the output list of characters and links to their wiki pages.',
                        default='../../data/character_data.json', type=str)
    parser.add_argument('--debug_mode', help='If True it will always open a browser window.', default=False, type=bool)

    args = parser.parse_args()

    scrape_character_list(args.output_path, args.debug_mode)


if __name__ == "__main__":
    main()
