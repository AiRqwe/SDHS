from dbm import error
from operator import index

from selenium import webdriver
from  selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from  selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logging import log

from ceshi.neimengluwang.request.request import logger


class BrowserDriver:



      def __init__(self,browser):
          self.driver=None
          self.browser=browser

      def browser_driver(self):
          if self.browser == 'chrome':
              self.driver=webdriver.Chrome()
          elif self.browser == 'Edge':
              self.driver = webdriver.Edge()
          else:
              raise ValueError("请正确输入浏览器类型 'chrome', 'edge', or 'firefox'.")

          return self.driver
class PageOptions:


      def __init__(self,driver):
          self.driver=driver

      def find_method(self, by, locator, index=0, text=False, elements=None):
          elements= WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(locator))
          logger.info(f"定位方式{by};定位语句{locator}")
          if len(elements)> index:
              if text:
                  logger.info(f"元素{elements[index].text}")
                  return elements[index].text
              else:
                  raise IndexError(f"未找到索引为 {index} 的元素，定位方式: {by}, 定位语句: '{locator}'。")
          else:
              return None


      def element_find(self):











if __name__ == '__main__':
    login=BrowserDriver('firefox')
    o=login.browser_driver()
    o.get('http://10.105.18.25:38082')