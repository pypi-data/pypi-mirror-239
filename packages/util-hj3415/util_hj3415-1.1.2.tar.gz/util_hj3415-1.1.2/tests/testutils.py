import datetime
import pprint
import time
import os
import unittest
from src.util_hj3415 import utils, noti


class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_to_float(self):
        a = ['1432', '1,432', '23%', 1432, float('nan'), None, float('inf')]
        for s in a:
            print(utils.to_float(s))

    def test_to_int(self):
        a = ['1432', '1,432', '23%', 1432, float('nan'), None, float('inf')]
        for s in a:
            print(utils.to_int(s))

    def test_deco_num(self):
        a = ['1432123331', '1,43223123', '23123123123%', 1432123123132, float('nan')]
        for s in a:
            print(utils.deco_num(s))

    def test_date_to_str(self):
        print(utils.date_to_str(datetime.datetime.today()))

    def test_str_to_date(self):
        print(utils.str_to_date('2021년 04월 13일'))
        print(utils.str_to_date('2021/04/13'))
        print(utils.str_to_date('2021-04-13'))
        print(utils.str_to_date('2021.04.13'))
        print(utils.str_to_date('20210413'))

    def test_get_price_now(self):
        print(utils.get_price_now(code='005930'))

    def test_scrape_simple_data(self):
        print(utils.scrape_simple_data(url='https://www.gsden.co.kr/',
                                       css_selector='#hero-fullscreen > div > h2'))

    def test_chk_date(self):
        dates = ['2021/11/10', '20210230', '2023/11', '2012.11.10']
        for date in dates:
            print('isYmd: ', date, utils.isYmd(date))
            print('isY/m: ', date, utils.isY_slash_m(date))

    def test_get_kor_amount(self):
        print(utils.get_kor_amount(1234567890))
        print(utils.get_kor_amount(1111111111))
        print(utils.get_kor_amount(1234567890, omit='억'))
        print(utils.get_kor_amount(1234567890, omit='천만'))
        print(utils.get_kor_amount(1234567890, omit='만'))
        print(utils.get_kor_amount(1234567890, omit='천'))
        print(utils.get_kor_amount(1234567890, str_suffix=''))

    def test_nan_to_zero(self):
        print(utils.nan_to_zero(float('nan')))
        print(utils.nan_to_zero(123))
        with self.assertRaises(TypeError):
            print(utils.nan_to_zero('123'))

    def test_get_driver(self):
        from selenium.webdriver.common.by import By

        wait = 1
        _CUR_DIR = os.path.dirname(os.path.realpath(__file__))
        _TEMP_DIR = os.path.join(_CUR_DIR, '_down_krx')
        addr = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage'
        driver = utils.get_driver(temp_dir=_TEMP_DIR)
        driver.get(addr)
        time.sleep(wait * 2)

    def test_get_driver_edge(self):
        wait = 1
        addr = 'https://www.gsden.co.kr'
        driver = utils.get_driver_edge()
        driver.get(addr)
        time.sleep(wait * 2)


    def test_get_driver_geolocation(self):
        driver = utils.get_driver(headless=False, geolocation=True)
        # driver.get("https://m.place.naver.com/hospital/13289684/home?subtab=location&selected_place_id=13289684")
        driver.get("https://www.google.co.kr/maps/?hl=ko")
        time.sleep(30)


    def test_get_driver_for_dentaljob(self):
        from selenium.webdriver.common.by import By

        driver = utils.get_driver()
        driver.implicitly_wait(10)
        driver.get('https://www.dentaljob.co.kr/00_Member/00_Login.aspx')
        print('Trying login and refresh...')

        try:
            print('Input id and password')
            driver.find_element(By.NAME, 'login_id').send_keys('hj3415')
            driver.find_element(By.NAME, 'login_pw').send_keys('piyrw421')

            print('Click the login button')
            driver.find_element(By.ID, 'ctl00_ctl00_cbody_cbody_btnLogin').click()
            print('Click the 개재중인 채용광고 link')
            driver.find_element(By.XPATH, '//*[@id="login_on"]/div[2]/p[1]/a').click()
            print('Click the JumpUp button')
            driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_cbody_cbody_pnViewMenuAuth"]/table/tbody/tr[1]/td[2]/p[2]/img[1]').click()
            print('Done.')
        except:
            #print('Wrong.')
            noti.telegram_to(botname="manager", text="Something wrong during dentaljob refreshing.")
        finally:
            driver.close()

    def test_code_divider(self):
        print(utils.code_divider_by_cpu_core(list(range(1, 200))))


    def test_get_ip_addr(self):
        print(utils.get_ip_addr())
        print(utils.get_pc_info())
