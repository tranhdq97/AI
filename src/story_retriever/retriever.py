import os
import json
import logging
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)


class StoryRetriever:
    def __init__(self, link):
        self.link = link
        self.last_chapter_index = 3672
        self.base_dir = 'src/story_retriever/stories'
        self.driver = webdriver.Chrome()

    @staticmethod
    def __dump(obj, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)

    @staticmethod
    def __load(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def teardown_method(self):
        self.driver.quit()

    def __get_title(self):
        logging.info('---> GET TITLE')
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//div[@id='truyen']/div[1]/div[1]/h3"
        ))).text

    def __get_author(self):
        logging.info('---> GET AUTHOR')
        return self.driver.find_element(
            By.XPATH, '//div[@id="truyen"]/div[1]/div[1]/div[2]/div[2]/div[1]/a'
        ).get_attribute('title')

    def __get_story_categories(self):
        logging.info('---> GET STORY CATEGORIES')
        categories = self.driver.find_element(
            By.XPATH, '//div[@id="truyen"]/div[1]/div[1]/div[2]/div[2]/div[2]'
        )
        return ', '.join([category.get_attribute('title') for category in categories.find_elements(By.TAG_NAME, 'a')])

    def __get_chapter(self):
        index = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//div[@class='navbar-breadcrumb']/div/ol/li[3]/a/span"
        ))).text.split(' ')[-1]
        content = self.driver.find_element(
            By.XPATH, '//div[@id="chapter-big-container"]/div/div/h2/a'
        ).get_attribute('title') + '\n'
        if int(index) > 3672:
            exit()

        logging.info(f'---> GET CHAPTER: {index}')
        content_element = self.driver.find_element(
            By.XPATH, "//div[@id='chapter-big-container']/div/div/div[@class='chapter-c']"
        )
        content += content_element.text
        for child in content_element.find_elements(By.XPATH, './div'):
            content = content.replace(child.text, '')

        story_data = {
            'index': int(index),
            'url': self.driver.current_url,
            'created_date': str(datetime.now()),
            'content': content
        }
        self.__dump(story_data, f'{self.story_path}/{int(index):0>6d}.json')

    def __next_chapter(self):
        logging.info('---> NEXT CHAPTER')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, '//div[@id="chapter-nav-top"]/div/a[2]'
        ))).click()

    def __to_last_saved_chapter(self):
        logging.info('---> TO LAST SAVED CHAPTER')
        self.driver.get(self.link)
        title = self.__get_title()
        self.story_path = f'{self.base_dir}/{title}'
        os.makedirs(self.story_path, exist_ok=True)
        chapter_list = sorted(os.listdir(f'{self.story_path}'))
        if len(chapter_list) > 1:
            obj = self.__load(f'{self.story_path}/{chapter_list[-1]}')
            self.driver.get(obj['url'])
            self.__next_chapter()
            logging.info(f'---> START AT CHAPTER: {obj["index"] + 1}')
        else:
            logging.info(f'---> START AT CHAPTER: 1')
            story_info = {
                'title': title,
                'author': self.__get_author(),
                'categories': self.__get_story_categories(),
            }
            self.__dump(story_info, f'{self.story_path}/{0:0>6d}_meta.json')
            first_chapter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((
                By.XPATH, '//ul[@class="list-chapter"]/li[1]/a'
            )))
            ActionChains(self.driver).click(first_chapter).perform()

        logging.info('---> START CRAWLING')

    def run(self):
        logging.info('---> RUN')
        self.__to_last_saved_chapter()
        while True:
            self.__get_chapter()
            self.__next_chapter()

        self.teardown_method()
