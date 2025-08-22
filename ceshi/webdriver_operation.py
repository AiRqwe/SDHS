import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrowserDriver:
    def __init__(self, browser='chrome', headless=False, driver_path=None):
        """
        初始化浏览器驱动。

        :param browser: 浏览器类型，可选值为 'chrome', 'edge', 'firefox'
        :param headless: 是否启用无头模式
        :param driver_path: 本地驱动程序路径，如果未提供则自动管理驱动程序
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver_path = driver_path
        self.driver = None

    def _get_chrome_driver(self):
        """获取 Chrome 浏览器驱动"""
        options = ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        if self.driver_path:
            service = ChromeService(self.driver_path)
        else:
            service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _get_edge_driver(self):
        """获取 Edge 浏览器驱动"""
        options = EdgeOptions()
        if self.headless:
            options.add_argument('--headless')
        if self.driver_path:
            service = EdgeService(self.driver_path)
        else:
            service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    def _get_firefox_driver(self):
        """获取 Firefox 浏览器驱动"""
        options = FirefoxOptions()
        if self.headless:
            options.add_argument('--headless')
        if self.driver_path:
            service = FirefoxService(self.driver_path)
        else:
            service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    def get_driver(self):
        """根据浏览器类型返回相应的驱动实例"""
        if self.browser == 'chrome':
            self.driver = self._get_chrome_driver()
        elif self.browser == 'edge':
            self.driver = self._get_edge_driver()
        elif self.browser == 'firefox':
            self.driver = self._get_firefox_driver()
        else:
            raise ValueError("Unsupported browser type. Choose from 'chrome', 'edge', or 'firefox'.")
        return self.driver

    def close(self):
        """关闭浏览器驱动"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed successfully")

class PageOperations:
    def __init__(self, driver):
        """
        初始化页面操作类。

        :param driver: 已经初始化的浏览器驱动实例
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find(self, by, locator, custom_message='', index=0, text=False):
        """
        查找元素方法，支持根据多种定位方式查找元素。可选择返回元素的文本内容。
        
        :param by: 定位方式（XPATH、ID、NAME、CSS_SELECTOR、CLASS_NAME、TAG_NAME、LINK_TEXT）
        :param locator: 定位方式对应的定位元素
        :param custom_message: 自定义操作内容，用于日志记录
        :param index: 元素位置，默认为0
        :param text: 是否查找元素文本，默认为False
        :return: 元素或元素文本
        """
        try:
            by_method = getattr(By, by.upper())
            elements = self.wait.until(EC.presence_of_all_elements_located((by_method, locator)))
            logger.info(f"操作：【{custom_message}】，找到 {len(elements)} 个元素，定位方式: {by}, 定位语句: '{locator}'。")
            if elements:
                if len(elements) > index:
                    if text:
                        logger.info(f"{custom_message}:{elements[index].text}")
                        return elements[index].text
                    else:
                        return elements[index]
                else:
                    logger.error(f"未找到索引为 {index} 的元素，定位方式: {by}, 定位语句: '{locator}'。{custom_message}")
                    raise IndexError(f"未找到索引为 {index} 的元素，定位方式: {by}, 定位语句: '{locator}'。{custom_message}")
            else:
                logger.error(f"未找到元素，定位方式: {by}, 定位语句: '{locator}'。{custom_message}")
                return None
        except AttributeError:
            logger.error(f"无效的定位方式: '{by}'。{custom_message}")
            raise
        except TimeoutException:
            logger.error(f"未能找到元素，定位方式为 {by}: '{locator}'。{custom_message}")
            return None
        except IndexError:
            logger.error(f"未找到索引为 {index} 的元素，定位方式: {by}, 定位语句: '{locator}'。{custom_message}")
            return None
        except WebDriverException as e:
            logger.error(f"遇到WebDriverException异常: {e}。{custom_message}")
            return None

    def find_elements(self, by, locator, custom_message=''):
        """
        查找多个元素。

        :param by: 定位方式（XPATH、ID、NAME、CSS_SELECTOR、CLASS_NAME、TAG_NAME、LINK_TEXT）
        :param locator: 定位方式对应的定位元素
        :param custom_message: 自定义操作内容，用于日志记录
        :return: 元素列表
        """
        try:
            by_method = getattr(By, by.upper())
            elements = self.wait.until(EC.presence_of_all_elements_located((by_method, locator)))
            logger.info(f"操作：【{custom_message}】，找到 {len(elements)} 个元素，定位方式: {by}, 定位语句: '{locator}'。")
            return elements
        except AttributeError:
            logger.error(f"无效的定位方式: '{by}'。{custom_message}")
            raise
        except TimeoutException:
            logger.error(f"未能找到元素，定位方式为 {by}: '{locator}'。{custom_message}")
            return []
        except WebDriverException as e:
            logger.error(f"遇到WebDriverException异常: {e}。{custom_message}")
            return []

    def get_elements_count(self, by, locator, custom_message=''):
        """
        获取多个元素的数量。

        :param by: 定位方式（XPATH、ID、NAME、CSS_SELECTOR、CLASS_NAME、TAG_NAME、LINK_TEXT）
        :param locator: 定位方式对应的定位元素
        :param custom_message: 自定义操作内容，用于日志记录
        :return: 元素数量
        """
        elements = self.find_elements(by, locator, custom_message=custom_message)
        count = len(elements)
        logger.info(f"操作：【{custom_message}】，找到 {count} 个元素，定位方式: {by}, 定位语句: '{locator}'。")
        return count

    def operate_on_elements(self, by, locator, action, custom_message='', **kwargs):
        """
        对多个元素进行操作。

        :param by: 定位方式（XPATH、ID、NAME、CSS_SELECTOR、CLASS_NAME、TAG_NAME、LINK_TEXT）
        :param locator: 定位方式对应的定位元素
        :param action: 操作类型（如 'click', 'send_keys' 等）
        :param custom_message: 自定义操作内容，用于日志记录
        :param kwargs: 其他操作参数，如 send_keys 的 text
        """
        elements = self.find_elements(by, locator, custom_message=custom_message)
        if not elements:
            logger.error(f"未找到元素，定位方式: {by}, 定位语句: '{locator}'。{custom_message}")
            return

        for index, element in enumerate(elements):
            if action == 'click':
                element.click()
                logger.info(f"操作：【{custom_message}】，点击第 {index + 1} 个元素，定位方式: {by}, 定位语句: '{locator}'。")
            elif action == 'send_keys':
                text = kwargs.get('text', '')
                element.clear()
                element.send_keys(text)
                logger.info(f"操作：【{custom_message}】，在第 {index + 1} 个元素中输入文本 '{text}'，定位方式: {by}, 定位语句: '{locator}'。")
            elif action == 'get_text':
                text = element.text
                logger.info(f"操作：【{custom_message}】，获取第 {index + 1} 个元素的文本 '{text}'，定位方式: {by}, 定位语句: '{locator}'。")
            else:
                logger.error(f"不支持的操作类型: {action}。{custom_message}")

    def click_element(self, by, value, custom_message=None):
        """
        点击元素。

        :param by: 定位方式，如 'id', 'xpath' 等
        :param value: 定位值
        :param custom_message: 自定义操作内容，用于日志记录
        """
        try:
            element = self.find(by, value, custom_message=custom_message)
            element.click()
            message = f"Clicked element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
        except (TimeoutException, NoSuchElementException) as e:
            message = f"Failed to click element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")

    def get_element_text(self, by, value, custom_message=None):
        """
        获取元素文本。

        :param by: 定位方式，如 'id', 'xpath' 等
        :param value: 定位值
        :param custom_message: 自定义操作内容，用于日志记录
        :return: 元素文本，如果失败返回 None
        """
        try:
            text = self.find(by, value, custom_message=custom_message, text=True)
            message = f"Retrieved text from element: {value}. Text: {text}"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
            return text
        except (TimeoutException, NoSuchElementException) as e:
            message = f"Failed to retrieve text from element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")
            return None

    def js_click_element(self, by, value, custom_message=None):
        """
        使用 JavaScript 点击元素。

        :param by: 定位方式，如 'id', 'xpath' 等
        :param value: 定位值
        :param custom_message: 自定义操作内容，用于日志记录
        """
        try:
            element = self.find(by, value, custom_message=custom_message)
            self.driver.execute_script("arguments[0].click();", element)
            message = f"JS clicked element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
        except (TimeoutException, NoSuchElementException) as e:
            message = f"Failed to JS click element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")

    def switch_to_iframe(self, by, value, custom_message=None):
        """
        切换到 iframe。

        :param by: 定位方式，如 'id', 'xpath' 等
        :param value: 定位值
        :param custom_message: 自定义操作内容，用于日志记录
        """
        try:
            iframe = self.find(by, value, custom_message=custom_message)
            self.driver.switch_to.frame(iframe)
            message = f"Switched to iframe: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
        except (TimeoutException, NoSuchElementException) as e:
            message = f"Failed to switch to iframe: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")

    def switch_to_default_content(self, custom_message=None):
        """
        切换回默认内容。

        :param custom_message: 自定义操作内容，用于日志记录
        """
        try:
            self.driver.switch_to.default_content()
            message = "Switched back to default content"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
        except Exception as e:
            message = "Failed to switch back to default content"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")

    def input_text(self, by, value, text, custom_message=None):
        """
        输入文本到指定元素。

        :param by: 定位方式，如 'id', 'xpath' 等
        :param value: 定位值
        :param text: 要输入的文本
        :param custom_message: 自定义操作内容，用于日志记录
        """
        try:
            element = self.find(by, value, custom_message=custom_message)
            element.clear()
            element.send_keys(text)
            message = f"Input text '{text}' to element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
        except (TimeoutException, NoSuchElementException) as e:
            message = f"Failed to input text to element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")

    def select_option(self, by, value, option_value, custom_message=None):
        """
        选择下拉框中的选项。

        :param by: 定位方式，如 'id', 'xpath' 等
        :param value: 定位值
        :param option_value: 选项的值
        :param custom_message: 自定义操作内容，用于日志记录
        """
        try:
            element = self.find(by, value, custom_message=custom_message)
            select = Select(element)
            select.select_by_value(option_value)
            message = f"Selected option with value '{option_value}' in element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.info(message)
        except (TimeoutException, NoSuchElementException) as e:
            message = f"Failed to select option in element: {value}"
            if custom_message:
                message += f" - {custom_message}"
            logger.error(f"{message}. Error: {str(e)}")

    def close_browser(self):
        """关闭浏览器驱动"""
        try:
            self.driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Failed to close browser. Error: {str(e)}")

if __name__ == "__main__":
    # 示例用法
    driver_path = 'path/to/chromedriver'  # 请替换为你的WebDriver路径
    browser_driver = BrowserDriver(browser='chrome', driver_path=driver_path)
    driver = browser_driver.get_driver()

    page_ops = PageOperations(driver)

    # 打开网页
    page_ops.driver.get('https://example.com')

    # 点击元素
    page_ops.click_element('id', 'some-button-id', custom_message="点击按钮")

    # 获取元素文本
    text = page_ops.get_element_text('class_name', 'some-class-name', custom_message="获取文本")
    print(f"Element text: {text}")

    # 输入文本
    page_ops.input_text('id', 'input-field-id', 'Hello, World!', custom_message="输入文本")

    # 选择下拉框选项
    page_ops.select_option('id', 'select-box-id', 'option-value', custom_message="选择下拉框选项")

    # JS点击元素
    page_ops.js_click_element('xpath', '//button[@id="js-click-button"]', custom_message="JS点击按钮")

    # 切换到iframe
    page_ops.switch_to_iframe('name', 'some-iframe-name', custom_message="切换到iframe")

    # 在iframe中操作
    page_ops.click_element('id', 'iframe-button-id', custom_message="在iframe中点击按钮")

    # 切换回默认内容
    page_ops.switch_to_default_content(custom_message="切换回默认内容")

    # 获取多个元素
    elements = page_ops.find_elements('class_name', 'list-item', custom_message="查找多个元素")
    for element in elements:
        print(f"Element text: {element.text}")

    # 获取多个元素的数量
    count = page_ops.get_elements_count('class_name', 'list-item', custom_message="获取元素数量")
    print(f"Number of elements: {count}")

    # 对多个元素进行操作
    page_ops.operate_on_elements('class_name', 'list-item', 'click', custom_message="点击多个元素")
    page_ops.operate_on_elements('class_name', 'input-fields', 'send_keys', custom_message="在多个输入框中输入文本", text="Sample text")

    # 关闭浏览器
    page_ops.close_browser()