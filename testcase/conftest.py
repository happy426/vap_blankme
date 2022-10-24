import time

import pytest
from playwright.sync_api import Browser
from common import env_util


@pytest.fixture(scope='session')
def login_hyx(browser: Browser):
    context = browser.new_context(locale="zh-CN")
    # context.add_init_script(js)
    page = context.new_page()
    page.goto(f"https://whale-login.{env_util.env}.meetwhale.com/login")
    page.wait_for_timeout(5000)
    # 输入账号密码
    page.fill(':nth-match(.ant-input, 1)', "18816525685")
    page.fill(':nth-match(.ant-input, 2)', "Huang666")
    # Check input[type="checkbox"]
    page.locator('.ant-checkbox-input').check()
    # Click button:has-text("登 录")
    page.locator('[class="ant-btn ant-btn-primary ant-btn-block"]').click()
    page.wait_for_timeout(5000)
    # page.locator('//*[@id="whale_privacy_btn_ok"]').click()
    # Save storage state into the file
    # 保存json  此处的相对路径是根据main函数的相对路径
    context.storage_state(path="./data/blankMe_cookie_hyx.json")
    print("登录成功")
    yield
    print("执行完毕")


@pytest.fixture(scope='session')
def api(playwright):
    request_context = playwright.request.new_context(
        base_url=f'https://blankme.{env_util.env}.meetwhale.com'
    )
    yield request_context
    request_context.dispose()

