# !/usr/bin/env python
# -*- coding: utf-8 -*-

from config import ClassConfig
from selenium import webdriver
from pyvirtualdisplay import Display


class ClassSpider(object):
    def __init__(self, account):
        """Конструктор класса подключает библиотеку Firefox и подключает модуль
        парсинга конфига"""
        self.account = account
        self.config = ClassConfig(account)
        self.vdisplay = Display(visible=0, size=(1680, 1050))
        self.vdisplay.start()
        self.driver = webdriver.Firefox()
        self.base_url = "http://aori.ru/"

    def __del__(self):
        """Деструктор класса закрывает вкладку браузера"""
        self.driver.close()
        self.vdisplay.stop()

    def foo_login(self):
        """Метод логина"""
        self.driver.get(self.base_url + 'mainpage1/login/?')
        self.driver.switch_to.frame('auth_frame')

        elem_login = self.driver.find_element_by_id('login')
        elem_login.send_keys(self.config.settings()['login'])

        elem_pass = self.driver.find_element_by_id('password')
        elem_pass.send_keys(self.config.settings()['password'])

        self.driver.find_element_by_css_selector('button.buttonOrange').click()
        self.driver.switch_to.default_content()

        cookie = {'name': 'foo', 'value': 'bar'}
        self.driver.add_cookie(cookie)

    def foo_balance(self):
        """Метод получения баланса аккаунта"""
        self.driver.get_cookies()
        self.driver.get(self.base_url + 'app/#/balance/payment')
        self.driver.implicitly_wait(5)

        monye_account = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div[2]/div/div/div/div[2]/div[1]/div/span').text
        monye_loose = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div[2]/div/div/div/div[2]/div[3]/span').text

        self.driver.get(self.base_url + 'app/#/campaigns')
        self.driver.implicitly_wait(5)

        acting = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div[2]/div/div/div/div[1]/div[1]/span[1]').text
        inacting = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div[2]/div/div/div/div[1]/div[1]/span[2]').text

        with open(self.config.path()['path_file'] + 'report.txt', 'a') as f:
            f.write(
                '''<strong>{0}</strong><br>\n
                <span style="color:rgb(50,144,209);font-family:Arial;font-size:28px">{1} RUB</span>/
                <span style="color:rgb(36,113,182);font-size:28px;line-height:normal">{2} RUB</span><br>
                {3}/{4}<br><br\n'''.format(
                    self.config.settings()['login'], monye_account, monye_loose, acting, inacting))
        f.close()

        self.driver.delete_all_cookies()

    def foo_account(self):
        a = list(self.config.accounts().keys())
        return a


def test_login():
    """Метод тестирования логина"""
    c = ClassSpider(account='')
    c.foo_login()


def test_balance():
    """Метод тестирования баланса"""
    c = ClassSpider(account='')
    c.foo_login()
    c.foo_balance()


def test_account():
    """Метод тестирования функции account"""
    c = ClassSpider(account='')
    c.foo_login()
    c.foo_account()


def start_bot():
    config = ClassConfig()
    c = ClassSpider(account='')
    list_accounts = c.foo_account()
    with open(config.path()['path_file'] + 'report.txt', 'w') as f:
        pass
    f.close()
    for account in list_accounts:
        c = ClassSpider(account)
        print(account)
        c.foo_login()
        c.foo_balance()


start_bot()
