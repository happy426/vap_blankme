import time
from common import env_util
from common.robot_image import SendMsg
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
    page = context.new_page()

    page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/detail/3785987999176311552")
    page.locator("text=确定").click()
    page.wait_for_timeout(5000)
    page.click("[class= 'ql-vap-product ql-standardInject'] >> //div/div/div/div/div[2]/div/div[1]/div[2]/div[1]")
    page.wait_for_timeout(5000)
    with context.expect_page() as new_page_info:
        page.click("text='关键话术排行'")
        page.mouse.wheel(0, 1000)
        page.locator("text='相关直播' >> //../ul/li[1]").click()
    new_page = new_page_info.value

    time.sleep(3)
