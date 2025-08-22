import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import re
@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page

class TestCeshi1:
    def test_login_and_event_management(self, page):
        page.goto("http://10.166.157.188/#/password-login-weixin3")

        page.get_by_placeholder("请输入账户").click()
        page.get_by_placeholder("请输入账户").click()
        page.get_by_placeholder("请输入账户").fill("caoxueyan")
        page.get_by_placeholder("请输入密码").click()
        page.get_by_placeholder("请输入密码").press("CapsLock")
        page.get_by_placeholder("请输入密码").fill("S")
        page.get_by_placeholder("请输入密码").press("CapsLock")
        page.get_by_placeholder("请输入密码").fill("Sdhs@123456a")
        page.get_by_placeholder("请输入验证码").click()
        page.get_by_placeholder("请输入验证码").fill("1")
        page.get_by_role("button", name="登录").click()
        time.sleep(3)
        page.locator(".list-closer").click()
        time.sleep(3)
        page.get_by_role("menubar").get_by_text("路网监测").click()
        time.sleep(3)
        page.get_by_role("menuitem", name="路况监测").locator("span").click()
        time.sleep(3)
        page.locator("div").filter(has_text=re.compile(r"^事件监测$")).click()
        time.sleep(3)
        page.locator(".d2-theme-container-main-body > div").first.click()
        time.sleep(3)
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_role("button", name="事件录入").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("li").filter(has_text="交通事故").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_placeholder("报警人姓名").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_placeholder("报警人姓名").fill("测试")
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_placeholder("报警人手机号码或固话(如:0531-96659)").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_placeholder("报警人手机号码或固话(如:0531-96659)").fill("13122221111")
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("form div").filter(has_text="路线(*):G2京沪高速G2001济南绕城高速G22").get_by_placeholder("请选择").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_text("G2京沪高速", exact=True).click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("div").filter(has_text=re.compile(r"^K$")).get_by_placeholder("000").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("div").filter(has_text=re.compile(r"^K$")).get_by_placeholder("000").fill("475")
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("div").filter(has_text=re.compile(r"^\+$")).get_by_placeholder("000").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("div").filter(has_text=re.compile(r"^\+$")).get_by_placeholder("000").fill("900")
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("div").filter(has_text=re.compile(r"^压车\(公里\):$")).get_by_role("spinbutton").click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("div").filter(has_text=re.compile(r"^压车\(公里\):$")).get_by_role("spinbutton").fill("01")
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("label").filter(has_text="行2").locator("span").nth(1).click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.locator("label").filter(has_text="事件已确认").locator("span").nth(1).click()
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_role("button", name="确认").click()
        time.sleep(3)
        page.locator("[id=\"http\\:\\/\\/10\\.166\\.157\\.188\\/emergency\\/\\#\\/login\\?code\\=\\{authCode\\}\\&\\&asideCollapse\\=\\{asideCollapse\\}\\&\\&route\\=emergency\\/eventmanagement\"]").content_frame.get_by_role("button", name="发布").click()

        # Add assertions here
        assert page.get_by_text("事件发布成功").is_visible()

if __name__ == "__main__":
    pytest.main()         