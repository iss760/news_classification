from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

import datetime


class Crawler():
    def __init__(self):
        self.driver = self.driver = webdriver.Chrome('c://chromedriver.exe')

    # '많이 본 뉴스' 네이버 뉴스 크롤링 함수
    def popular_naver_news_crawler(self, url, number):
        """
        :param url: 시작 주소
        :param number: 크롤링 할 기사의 갯수
        :return: 크롤링 한 기사의 본문 리스트
        """
        driver = self.driver
        date = url.split('date=')[1]
        count = 0
        date = datetime.datetime.strptime(date, '%Y%m%d')

        news_body_contents_list = []
        while True:
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            news_url_boxes = soup.findAll('div', {'class': 'ranking_headline'})

            news_url_list = []
            # 한 페이지에서 기사들 url 수집
            for news_url_box in news_url_boxes:
                temp = str(news_url_box).split('href="')
                temp2 = temp[1].split('" title')
                news_url = temp2[0].replace('amp;', '')
                news_url_list.append(news_url)

            sleep(2)

            # 기사 본문 수집
            for news_url in news_url_list:
                try:
                    driver.get('https://news.naver.com' + str(news_url))
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    news_body_contents = soup.find('div', {'id': 'articleBodyContents'}).text
                    news_body_contents = str(news_body_contents).replace('\n', '')
                    news_body_contents = news_body_contents.split('function _flash_removeCallback() {}')[1]
                    news_body_contents_list.append(news_body_contents)
                except Exception as e:
                    print(e)
                    continue

                # 필요 갯수 기사 수집 후 return
                count = count + 1
                if count >= number:
                    return news_body_contents_list

            # 날짜 처리로 다음 페이지 url 제공
            date = date - datetime.timedelta(14)
            date_y = str(date.year)
            date_m = str(date.month)
            date_d = str(date.day)
            if len(date_m) is 1: date_m = '0' + date_m
            if len(date_d) is 1: date_d = '0' + date_d
            date = date_y + date_m + date_d
            url = url.replace(url.split('date=')[1], str(date))
            date = datetime.datetime.strptime(date, '%Y%m%d')



