#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re

import chromedriver_autoinstaller
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class Booking:
    def __init__(self,
            id: str, 
            pwd: str, 
            reservation_time: datetime.datetime, 
            target: datetime.datetime,
            **kwargs: dict
            ) -> None:
        assert reservation_time > datetime.datetime.now(), "예약 시작 시간이 이미 지났습니다"
        assert target.minute % 30 == 0, "30분 단위만 가능합니다"

        # Credentials
        self.id = id
        self.pwd = pwd

        # Booking Information
        self.timeout = kwargs.get('timeout', 5)
        self.reservation_time = reservation_time
        self.target = target
        self.adult = kwargs.get('adult', 1)
        self.adolescent = kwargs.get('adolescent', 0)
        self.child = kwargs.get('child', 0)

        self.info = {kwargs.get(f'name{i}', None): kwargs.get(f'number{i}', None) for i in range(2, 5)}
        self.info = {k: v for k, v in self.info.items() if v is not None}
        assert 0 < self.adult + self.adolescent + self.child <= 4, "최소 1명, 최대 4명까지만 예약 가능합니다"
        assert len(self.info.keys()) + 1 == self.adult + self.adolescent + self.child, "정보가 부족합니다"
        assert target.weekday() in [0, 1, 3, 4, 6] and \
            datetime.time(10, 0) <= datetime.time(self.target.hour, self.target.minute) <= datetime.time(17, 0) or\
                target.weekday() in [2, 5] and \
                    datetime.time(10, 0) <= datetime.time(self.target.hour, self.target.minute) <= datetime.time(20, 0),\
                "예약가능시간은 10:00 ~ 17:00입니다. (수, 토요일은 10:00 ~ 20:00)"

        # Install ChromeDriver and prepare webdriver
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()

    @property
    def url(self) -> str:
        return 'https://www.museum.go.kr/site/main/reserve/specialhall/form'

    def refresh(self) -> None:
        self.driver.get(self.url)

    def login(self) -> None:
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, self.timeout).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'btn-lg2')))
        except TimeoutException:
            raise TimeoutException("로딩 중 오류가 발생했습니다")
        self.driver.find_element(By.ID, 'id').send_keys(self.id)
        self.driver.find_element(By.ID, 'pwd').send_keys(self.pwd)
        self.driver.find_element(By.CLASS_NAME, 'btn-lg2').click()
        try:
            WebDriverWait(self.driver, self.timeout).until(expected_conditions.presence_of_element_located((By.XPATH, '//span[contains(@class, "ui-datepicker-year")]')))
        except TimeoutException:
            raise TimeoutException("로그인에 실패하였습니다")

    def wait_until_time(self) -> None:
        now = lambda: datetime.datetime.strptime(
            self.driver.find_element(By.ID, 'serverTime1').text + self.driver.find_element(By.ID, 'serverTime2').text,
            '%Y-%m-%d %H:%M:%S'
        )
        WebDriverWait(self.driver, float('inf')).until(lambda driver: self.reservation_time <= now())

    def move_datepicker(self) -> None:
        now = lambda: datetime.date(
            int(self.driver.find_element(By.XPATH, '//span[contains(@class, "ui-datepicker-year")]').text),
            int(re.search(r'\d+', self.driver.find_element(By.XPATH, '//span[contains(@class, "ui-datepicker-month")]').text)[0]),
            1
        )
        tmp = datetime.date(self.target.year, self.target.month, 1)
        try:
            WebDriverWait(self.driver, self.timeout).until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[contains(@class, "ui-datepicker-next")]')))
        except TimeoutException:
            raise TimeoutException("날짜를 선택하는중 오류가 발생했습니다.")
        while tmp != now():
            self.driver.find_element(By.XPATH, '//a[contains(@class, "ui-datepicker-next")]').click()
        self.driver.find_element(By.XPATH, f'//a[text() = "{self.target.day}"]').click()

    def put_info(self):
        WebDriverWait(self.driver, self.timeout).until(expected_conditions.presence_of_element_located((By.XPATH, f'//tr[.//td/input[@value="{self.target.hour}:{self.target.second:02d}"]]/td[contains(@class, "tbl-btn")]/a')))
        self.driver.find_element(By.XPATH, f'//tr[.//td/input[@value="{self.target.hour}:{self.target.second:02d}"]]/td[contains(@class, "tbl-btn")]/a').click()
        WebDriverWait(self.driver, self.timeout).until(expected_conditions.presence_of_element_located((By.ID, 'prod_0')))
        self.driver.find_element(By.ID, 'prod_0').send_keys(f'{self.adult}')
        self.driver.find_element(By.ID, 'prod_1').send_keys(f'{self.adolescent}')
        self.driver.find_element(By.ID, 'prod_2').send_keys(f'{self.child}')
        for idx, (name, number) in enumerate(self.info.items()):
            self.driver.find_element(By.ID, f'name{idx + 2}').send_keys(name)
            self.driver.find_element(By.ID, f'min{idx + 2}_2').send_keys(number.split('-')[1])
            self.driver.find_element(By.ID, f'min{idx + 2}_3').send_keys(number.split('-')[2])
        self.driver.find_element(By.XPATH, '//a[contains(@onclick, "return reservation")]').click()
        WebDriverWait(self.driver, self.timeout).until(expected_conditions.alert_is_present())
        # self.driver.switch_to.alert.accept()

    def run(self) -> None:
        self.login()
        self.wait_until_time()
        self.refresh()
        self.move_datepicker()
        self.put_info()

if __name__ == '__main__':
    pass