import time
import re
import allure
import pytest
from playwright.sync_api import Browser
from common.robot_image import SendMsg
from common import env_util


@allure.feature("直播复盘模块")
class TestAliviaBlankMeZhiBo:

    @allure.title("1-应用中心进入直播复盘列表页")
    @allure.severity("critical")
    def test_blankme_zhibo01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/app-center?app_id=VAP')
        page.wait_for_timeout(3000)
        # 进入商品复盘
        page.locator("text=直播复盘 >> nth=1").click()
        page.wait_for_url(f"https://blankme.{env_util.env}.meetwhale.com/vap/entry")
        page.locator("text=确定").click()
        page.wait_for_timeout(3000)
        assert f"https://blankme.{env_util.env}.meetwhale.com/vap/entry" == page.url
        allure.attach(page.screenshot(), '直播复盘列表页进入成功', allure.attachment_type.PNG)

    @allure.title("2-直播复盘列表页进入直播复盘页面")
    @allure.severity("critical")
    def test_blankme_zhibo02(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/entry")
        page.wait_for_timeout(3000)
        page.click(':nth-match([class="ant-table-row ant-table-row-level-0"], 2)')
        page.wait_for_timeout(3000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f"https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/" in page.url:
            allure.attach(page.screenshot(), '直播复盘进入成功', allure.attachment_type.PNG)
        else:
            title = "直播复盘进入失败"
            describe = "直播复盘详情页进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '直播复盘进入失败', allure.attachment_type.PNG)

    @allure.title("3-直播间热卖商品进入商品复盘列表页")
    @allure.severity("critical")
    def test_blankme_zhibo03(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/entry")
        page.wait_for_timeout(3000)
        page.click(':nth-match([class="ant-table-row ant-table-row-level-0"], 2)')
        with context.expect_page() as new_page_info:
            page.locator('//*[@id="rc-tabs-0-panel-BasicInfo"]/div/div[4]/div[2]/div[1]/div[1]').click()
        new_page = new_page_info.value
        page.wait_for_timeout(3000)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail/' in new_page.url
        allure.attach(page.screenshot(), '直播间进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '商品复盘进入成功', allure.attachment_type.PNG)

    @allure.title("4-直播间评论区进入商品复盘列表页")
    @allure.severity("critical")
    def test_blankme_zhibo04(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/entry")
        page.wait_for_timeout(3000)
        # 第二场直播间，第一场可能没有商品
        page.click(':nth-match([class="ant-table-row ant-table-row-level-0"], 2)')
        page.locator("text=直播评论").click()
        page.wait_for_timeout(5000)
        # 光标移动至滚动条所在框中
        page.click(".container--2haQR")
        for i in range(100):
            text = page.inner_html('.container--2haQR')
            # 滚动鼠标 , 参数给一个较大值，以保证直接移动至最后
            page.mouse.wheel(0, 100 * i)
            if "title--2OCu9" in text:
                break
        with page.expect_popup() as popup_info:
            page.locator(':nth-match(.title--2OCu9, 1)').click()
        new_page = popup_info.value
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail/' in new_page.url
        allure.attach(page.screenshot(), '直播复盘进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '商品复盘进入成功', allure.attachment_type.PNG)

    @allure.title("5-直播间主播头像进入主播复盘")
    @allure.severity("critical")
    def test_blankme_zhibo05(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/725")
        page.wait_for_timeout(3000)
        page.locator("text=确定").click()
        with context.expect_page() as new_page_info:
            page.locator(
                '//*[@id="rc-tabs-0-panel-BasicInfo"]/div/div[3]/div/div/div[3]/div[1]/span[1]/div/span/span/img').click()
        new_page = new_page_info.value
        time.sleep(3)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail?anchorId=' in new_page.url
        allure.attach(page.screenshot(), '直播间进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '主播复盘进入成功', allure.attachment_type.PNG)


@allure.feature("商品复盘模块")
class TestAliviaBlankMeShangPin:

    @allure.title("1-应用中心进入商品复盘列表页")
    @allure.severity("critical")
    def test_blankme_shangpin_login01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/app-center?app_id=VAP")
        page.wait_for_timeout(3000)
        # 进入商品复盘
        page.locator("text=商品复盘").click()
        page.wait_for_url(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-list")
        page.locator("text=确定").click()
        page.wait_for_timeout(3000)
        assert f"https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-list" == page.url
        allure.attach(page.screenshot(), '进入成功', allure.attachment_type.PNG)

    @allure.title("2-列表页进入商品复盘")
    @allure.severity("critical")
    def test_blankme_shangpin_login02(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-list")
        page.click('.ant-table-tbody >> //tr[2]')
        time.sleep(3)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f"https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail/" in page.url:
            allure.attach(page.screenshot(), '商品复盘进入成功', allure.attachment_type.PNG)
        else:
            title = "商品复盘进入失败"
            describe = "商品复盘详情页进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '商品复盘进入失败', allure.attachment_type.PNG)

    @allure.title("3-商品复盘列表页进入主播复盘")
    @allure.severity("critical")
    def test_blankme_shangpin_login03(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-list")
        page.wait_for_timeout(3000)
        with context.expect_page() as new_page_info:
            # 需要做一下判断，判断里面是否有主播
            page.locator('.ant-table-tbody >> //tr[2]/td[2]/div/div/div[1]/span/div').click()
        new_page = new_page_info.value
        time.sleep(3)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail?anchorId=' in new_page.url
        allure.attach(page.screenshot(), '列表页', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '主播复盘进入成功', allure.attachment_type.PNG)

    @allure.title("4-商品复盘进入直播间")
    @allure.severity("critical")
    def test_blankme_shangpin_login04(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-list')
        page.wait_for_timeout(3000)
        page.click('.ant-table-tbody >> //tr[2]')
        page.wait_for_timeout(3000)
        with page.expect_popup() as popup_info:
            page.click(':nth-match(.session--3-eeo, 2)')
        new_page = popup_info.value
        time.sleep(3)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/' in new_page.url
        allure.attach(page.screenshot(), '商品复盘进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '直播间进入成功', allure.attachment_type.PNG)

    @allure.title("5-商品复盘进入主播复盘")
    @allure.severity("critical")
    def test_blankme_shangpin_login05(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-list')
        page.wait_for_timeout(3000)
        page.click('.ant-table-tbody >> //tr[2]')
        page.wait_for_timeout(3000)
        with page.expect_popup() as popup_info:
            page.click('.anchorList--2uHBA > div > .ant-badge > .ant-avatar > img')
        new_page = popup_info.value
        time.sleep(3)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail?anchorId=' in new_page.url
        allure.attach(page.screenshot(), '商品复盘进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '主播复盘进入成功', allure.attachment_type.PNG)


@allure.feature("主播复盘模块")
class TestAliviaBlankMeZhuBo:

    @allure.title("1-应用中心进入主播复盘列表页")
    @allure.severity("critical")
    def test_blankme_zhubo_login01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/app-center?app_id=VAP')
        page.wait_for_timeout(3000)
        # 进入主播复盘
        page.locator("text=主播复盘").click()
        page.wait_for_url(f"https://blankme.{env_util.env}.meetwhale.com/vap/anchor-list")
        page.locator("text=确定").click()
        time.sleep(3)
        assert f"https://blankme.{env_util.env}.meetwhale.com/vap/anchor-list" == page.url
        allure.attach(page.screenshot(), '进入成功', allure.attachment_type.PNG)

    @allure.title("2-列表页进入主播复盘")
    @allure.severity("critical")
    def test_blankme_zhubo_login02(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/anchor-list")
        page.wait_for_timeout(3000)
        page.click('//*[@id="root-content"]/div/div/div/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr[2]')
        time.sleep(3)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail?anchorId=' in page.url:
            allure.attach(page.screenshot(), '主播复盘进入成功', allure.attachment_type.PNG)
        else:
            title = "主播复盘进入失败"
            describe = "主播复盘详情页进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '主播复盘进入失败', allure.attachment_type.PNG)

    @allure.title("3-主播复盘进入直播间")
    @allure.severity("critical")
    def test_blankme_zhubo_login03(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/anchor-list")
        page.wait_for_timeout(3000)
        page.click('.ant-table-tbody >> //tr[2]')
        page.wait_for_timeout(3000)
        with page.expect_popup() as popup_info:
            page.click('.session--3-eeo')
        new_page = popup_info.value
        time.sleep(3)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/' in new_page.url
        allure.attach(page.screenshot(), '主播复盘进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '直播间进入成功', allure.attachment_type.PNG)

    @allure.title("4-主播复盘进入商品复盘")
    @allure.severity("critical")
    def test_blankme_zhubo_login04(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/anchor-list")
        page.wait_for_timeout(3000)
        page.click('.ant-table-tbody >> //tr[2]')
        page.wait_for_timeout(3000)
        with page.expect_popup() as popup_info:
            page.click('.cardWrap--230Vs')
        new_page = popup_info.value
        time.sleep(3)
        assert f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail/' in new_page.url
        allure.attach(page.screenshot(), '主播复盘进入成功', allure.attachment_type.PNG)
        allure.attach(new_page.screenshot(), '商品复盘进入成功', allure.attachment_type.PNG)


@allure.feature("内容中心模块")
class TestAliviaBlankMeNeiRong:

    @allure.title("1-我的空间")
    @allure.severity("critical")
    def test_blankme_neirong01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content?path=vap")
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/assets-new/content?path=vap' == page.url:
            allure.attach(page.screenshot(), '我的空间进入成功', allure.attachment_type.PNG)
        else:
            title = "我的空间进入失败"
            describe = "我的空间进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '我的空间进入失败', allure.attachment_type.PNG)

    @allure.title("2-与我共享")
    @allure.severity("critical")
    def test_blankme_neirong02(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content/share?microApp=vap")
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/assets-new/content/share?microApp=vap' == page.url:
            allure.attach(page.screenshot(), '与我共享进入成功', allure.attachment_type.PNG)
        else:
            title = "与我共享进入失败"
            describe = "与我共享进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '与我共享进入失败', allure.attachment_type.PNG)

    @allure.title("3-收藏")
    @allure.severity("critical")
    def test_blankme_neirong03(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content/collect?microApp=vap")
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/assets-new/content/collect?microApp=vap' == page.url:
            allure.attach(page.screenshot(), '收藏进入成功', allure.attachment_type.PNG)
        else:
            title = "收藏进入失败"
            describe = "收藏进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '收藏进入失败', allure.attachment_type.PNG)

    @allure.title("4-知识图谱")
    @allure.severity("critical")
    def test_blankme_neirong04(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/knowledge-graph?microApp=vap")
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/vap/knowledge-graph?microApp=vap' == page.url:
            allure.attach(page.screenshot(), '知识图谱进入成功', allure.attachment_type.PNG)
        else:
            title = "知识图谱进入失败"
            describe = "知识图谱进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '知识图谱进入失败', allure.attachment_type.PNG)

    @allure.title("5-知识库")
    @allure.severity("critical")
    def test_blankme_neirong05(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/qa-list")
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/vap/qa-list' == page.url:
            allure.attach(page.screenshot(), '知识库进入成功', allure.attachment_type.PNG)
        else:
            title = "知识库进入失败"
            describe = "知识库进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '知识库进入失败', allure.attachment_type.PNG)

    @allure.title("6-回收站")
    @allure.severity("critical")
    def test_blankme_neirong06(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content/recycle?microApp=vap")
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/assets-new/content/recycle?microApp=vap' == page.url:
            allure.attach(page.screenshot(), '回收站进入成功', allure.attachment_type.PNG)
        else:
            title = "回收站进入失败"
            describe = "回收站进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '回收站进入失败', allure.attachment_type.PNG)

    @allure.title("7-视频裁切")
    @allure.severity("critical")
    def test_blankme_neirong07(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content?path=vap")
        page.wait_for_timeout(5000)
        page.locator("text=确定").click()
        page.locator(":nth-match(.ant-row, 2) >> text='caiqie.mp4'").click(button='right')
        page.click('text="视频智能剪辑"')
        page.wait_for_timeout(5000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/assets-new/video-cut?id=3785988000511022592' == page.url:
            allure.attach(page.screenshot(), '视频裁切进入成功', allure.attachment_type.PNG)
        else:
            title = "视频裁切进入失败"
            describe = "视频裁切进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '视频裁切进入失败', allure.attachment_type.PNG)

    @allure.title("8-与我共享进入直播复盘")
    @allure.severity("critical")
    def test_blankme_neirong8(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content/share")
        page.wait_for_timeout(3000)
        page.click('.ant-row >> text="抖音直播视频"')
        page.wait_for_timeout(4000)
        assert f'https://blankme.{env_util.env}.meetwhale.com/assets-new/fileList?' in page.url
        allure.attach(page.screenshot(), '进入视频列表页', allure.attachment_type.PNG)
        # 分析完成的进入直播复盘
        page.locator(':nth-match([class="ant-checkbox"], 2) >> //input/../../..').click(button="right")
        page.wait_for_timeout(3000)
        page.click("text='直播复盘' >> visible=true")
        page.wait_for_timeout(3000)
        # 创建飞书消息对象
        feishu = SendMsg()
        if f'https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/' in page.url:
            allure.attach(page.screenshot(), '与我共享进入直播复盘进入成功', allure.attachment_type.PNG)
        else:
            title = "与我共享进入直播复盘进入失败"
            describe = "与我共享进入直播复盘进入失败，请进入alivia查看"
            feishu.send_post(title, env=env_util.env, bug='严重', describe=describe, path=page.screenshot())
            pytest.fail()
            allure.attach(page.screenshot(), '与我共享进入直播复盘进入失败', allure.attachment_type.PNG)


@allure.feature("直播场控模块")
class TestAliviaBlankMeChangKong:

    @allure.title("1-进入场控视角")
    @allure.severity("critical")
    def test_blankme_cksj01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-list")
        text = page.inner_text('.ant-table-tbody >> //tr[2]//td/div')
        page.wait_for_timeout(5000)
        page.click('.ant-table-tbody >> //tr[2]')
        with context.expect_page() as new_page_info:
            page.click("text='场控视角'")
        new_page = new_page_info.value
        page.wait_for_timeout(3000)
        assert f"https://blankme.{env_util.env}.meetwhale.com/vap/live-control-detail/{text}" in new_page.url
        allure.attach(new_page.screenshot(), '场控视角进入成功', allure.attachment_type.PNG)

    @allure.title("2-进入主播视角")
    @allure.severity("critical")
    def test_blankme_zbsj01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-list")
        page.wait_for_timeout(5000)
        text = page.inner_text('.ant-table-tbody >> //tr[2]//td/div')
        page.click('.ant-table-tbody >> //tr[2]')
        with context.expect_page() as new_page_info:
            page.click("text='主播视角'")
        new_page = new_page_info.value
        page.wait_for_timeout(3000)
        assert f"https://blankme.{env_util.env}.meetwhale.com/vap/live-control-detail/{text}/anchor" in new_page.url
        allure.attach(new_page.screenshot(), '主播视角进入成功', allure.attachment_type.PNG)


@allure.feature("直播话术模块")
class TestAliviaBlankMeHuaShu:

    @allure.title("1-商品话术")
    @allure.severity("critical")
    def test_blankme_huashu01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/content?path=vap")
        page.click('text="确定"')
        page.wait_for_timeout(3000)
        page.locator(".ant-row >> text='商品话术'").click()
        page.wait_for_url(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/detail/3785987999176311552")
        page.wait_for_timeout(5000)
        assert f"https://blankme.{env_util.env}.meetwhale.com/assets-new/detail/3785987999176311552" == page.url
        allure.attach(page.screenshot(), '话术进入成功', allure.attachment_type.PNG)

    @allure.title("2-商品话术跳转相关直播")
    @allure.severity("critical")
    def test_blankme_huashu02(self, browser: Browser, login_hyx):
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
        page.wait_for_timeout(5000)
        assert f"https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/" in new_page.url
        allure.attach(new_page.screenshot(), '跳转直播复盘成功', allure.attachment_type.PNG)

    @allure.title("3-商品话术关键话术排行")
    @allure.severity("critical")
    def test_blankme_huashu03(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/detail/3785987999176311552")
        page.locator("text=确定").click()
        page.wait_for_timeout(5000)
        page.click("[class= 'ql-vap-product ql-standardInject'] >> //div/div/div/div/div[2]/div/div[1]/div[2]/div[1]")
        page.wait_for_timeout(5000)
        page.locator('text="关键话术排行" >> text="成交金额"').hover()
        page.wait_for_timeout(1000)
        text = page.inner_text(
            '[class="ant-dropdown-menu ant-dropdown-menu-root ant-dropdown-menu-vertical ant-dropdown-menu-light"]')
        for i in ['成交金额', '商品千次曝光成交', '商品点击率', '曝光-成交转化率', '互动率', '加粉率', '加团率']:
            assert i in text
        allure.attach(page.screenshot(), '关键话术排行', allure.attachment_type.PNG)

    # @allure.title("4-商品话术素材搜索")
    # @allure.severity("critical")
    # def test_blankme_huashu04(self, browser: Browser, login_hyx):
    #     context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
    #     page = context.new_page()
    #     page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/detail/3785987999176311552")
    #     page.locator("text=确定").click()
    #     page.wait_for_timeout(5000)
    #     page.click("[class= 'ql-vap-product ql-standardInject'] >> //div/div/div/div/div[2]/div/div[1]/div[2]/div[1]")
    #     page.wait_for_timeout(5000)
    #     page.locator(':nth-match(.whale-vap-writing-assistant-tab-label, 1)').click()
    #     goods = page.inner_text(
    #         '//*[@id="js-scroller"]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]')
    #     value = page.input_value('[class="ant-input-affix-wrapper whale-vap-assets-search-input"] >> input')
    #     page.wait_for_timeout(3000)
    #     res = page.inner_text('.whale-vap-assets-search-result-label')
    #     num = re.findall(r'\d+', res)
    #     assert goods == value and int(num[0]) > 0
    #     allure.attach(page.screenshot(), '素材搜索', allure.attachment_type.PNG)
    #
    # @allure.title("5-商品话术竞对话术")
    # @allure.severity("critical")
    # def test_blankme_huashu05(self, browser: Browser, login_hyx):
    #     context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
    #     page = context.new_page()
    #     page.goto(f"https://blankme.{env_util.env}.meetwhale.com/assets-new/detail/3785987999176311552")
    #     page.locator("text=确定").click()
    #     page.wait_for_timeout(5000)
    #     page.click("[class= 'ql-vap-product ql-standardInject'] >> //div/div/div/div/div[2]/div/div[1]/div[2]/div[1]")
    #     page.wait_for_timeout(5000)
    #     page.locator(':nth-match(.whale-vap-writing-assistant-tab-label, 2)').click()
    #     page.wait_for_timeout(3000)
    #     page.fill('.whale-vap-compete-word >> //div[1]/div[1]/span/input', '防晒')
    #     page.wait_for_timeout(3000)
    #     res = page.inner_text('.whale-vap-compete-word-result-label')
    #     num = re.findall(r'\d+', res)
    #     assert int(num[0]) > 0
    #     allure.attach(page.screenshot(), '竞对话术搜索结果', allure.attachment_type.PNG)
