import os
import selenium
from urllib.request import urlretrieve
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


class StoryTeller:
    def __init__(self, story_name):
        self.story_dir = 'src/story_retriever/stories'
        self.chapter_list = [
            f'{self.story_dir}/{story_name}/{chapter}' for chapter in
            sorted(os.listdir(f'{self.story_dir}/{story_name}'))[1:]
        ]
        self.sound_synthesis_url = 'https://vbee.vn/'
        self.driver = webdriver.Chrome()

    def __download_sound(self, filename):
        logging.info('---> DOWNLOAD SOUND')
        sound_file = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[2]/div/div/div[1]/audio'
        )))
        urlretrieve(sound_file.get_attribute('src'), filename)

    def __turn_of_ad(self):
        logging.info('---> TURN OF ADV')
        logging.info('---> GET TITLE')
        not_display_checkbox = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="__next"]/div[1]/div/div/div/div/div[2]/div/input'
        )))
        not_display_checkbox.click()
        exit_btn = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div/div/div/div[1]/button')
        exit_btn.click()

    def __choose_voice(self):
        logging.info('---> CHOOSE VOICE')
        element = self.driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[3]/div/div/div/div[1]/div/div[2]/div[2]'
        )
        ActionChains(self.driver).move_to_element(element).perform()
        voice_dropdown = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((
            By.XPATH,
            '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/button'
        )))
        ActionChains(self.driver).move_to_element(voice_dropdown).click().perform()
        self.driver.find_element(
            By.XPATH,
            '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[2]/div/div/' +
            'div[1]/div[2]/div[1]/div[1]/div/div/div/button[8]'
        ).click()

    def __enter_text(self, content):
        logging.info('---> ENTER TEXT')
        input_area = self.driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[2]/div/div/div[1]/textarea'
        )
        input_area.send_keys(content)
        btn = self.driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[2]/div/div/div[1]/div[2]/div[2]/button'
        )
        btn.click()
        btn = WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="__next"]/div[2]/main/div/div[2]/main/div[2]/div/div/div[1]/div[2]/div[2]/button'
        )))
        if btn.find_element(By.XPATH, './p').text.lower() == 'tạm dừng':
            btn.click()

    def __load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __text_to_speech(self):
        for chapter in self.chapter_list:
            chapter_index = chapter.split('/')[-1].split('.')[0]
            logging.info(f'-> Chapter: {chapter_index}')
            chapter_content = self.__load(chapter)
            chapter_words = chapter_content.split(' ')
            for word in chapter_words:
                pass

        self.__enter_text('xx')
        self.__download_sound('xx')

    def run(self):
        logging.info('---> RUN')
        self.driver.get(self.sound_synthesis_url)
        self.__turn_of_ad()
        self.__choose_voice()
        self.__text_to_speech()
        self.exit()

    def exit(self):
        self.driver.quit()
