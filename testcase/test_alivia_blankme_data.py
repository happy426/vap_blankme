import time
import re
import allure
import pytest
from playwright.sync_api import Browser
from common.robot_image import SendMsg
from common import env_util


@allure.feature("数据对比")
class TestAliviaBlankMeData:

    @allure.title("直播复盘列表页")
    def test_blankme_shuju01(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        # 接口数据
        data = {
            "operationName": "searchFormValue",
            "variables": {
                "form_slug": "vap_douyin_list",
                "limit": 50,
                "offset": 0,
                "order_by": [],
                "filter_entities": [
                    {
                        "filter_key": "status",
                        "operation": 8,
                        "filter_value": "[\"4\"]"
                    }
                ],
                "relation": 1
            },
            "query": "query searchFormValue($form_slug: String, $filters: JSON, $order_by: [OrderByEntity], $limit: Int, $offset: Int, $filter_entities: JSON, $relation: Int, $full_text_search_keyword: String) {\n  searchFormValue(form_slug: $form_slug, filters: $filters, order_by: $order_by, offset: $offset, limit: $limit, filter_entities: $filter_entities, relation: $relation, full_text_search_keyword: $full_text_search_keyword) {\n    items\n    total\n    limit\n    offset\n  }\n}\n"
        }
        response = page.request.post(url=f'https://blankme.{env_util.env}.meetwhale.com/graphql', data=data)
        # 当status=4时，分析完成
        num = 0
        for i in range(50):
            if response.json()['data']['searchFormValue']['items'][i]['status'] == '4':
                num = i
                break
        res_data = response.json()['data']['searchFormValue']['items'][num]
        vid = res_data['vid']  # 直播间序号
        gmv = res_data['gmv']  # 成交金额
        gpm = res_data['gpm']
        live_watch_ucount = res_data['live_watch_ucount']  # 总观看人数
        click_rate = res_data['click_rate']  # 点击率
        order_conversion_rate = res_data['order_conversion_rate']  # 成交转换率
        interaction_rate = res_data['interaction_rate']  # 互动率
        add_fans_rate = res_data['add_fans_rate']  # 加粉率
        add_club_rate = res_data['add_club_rate']  # 加团率
        list_num = [gmv, gpm, live_watch_ucount, click_rate, order_conversion_rate, interaction_rate, add_fans_rate,
                    add_club_rate]

        # 根据vid进入直播间
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/vap/live-detail/{vid}')
        page.wait_for_timeout(10000)
        gmv_in = page.inner_text(':nth-match(.list--2x72Z, 1) >> //div[1]/span[2]').replace(',', '')[0:-1]
        gpm_in = page.inner_text(':nth-match(.list--2x72Z, 1) >> //div[2]/span[2]').replace(',', '')[0:-1]
        live_watch_ucount_in = page.inner_text(':nth-match(.list--2x72Z, 1) >> //div[3]/span[2]').replace(',', '')[0:-1]
        click_rate_in = page.inner_text(':nth-match(.list--2x72Z, 1) >> //div[4]/span[2]').replace(',', '')[0:-1]
        order_conversion_rate_in = page.inner_text(':nth-match(.list--2x72Z, 1) >> //div[5]/span[2]').replace(',', '')[
                                   0:-1]
        interaction_rate_in = page.inner_text(':nth-match(.list--2x72Z, 2) >> //div[1]/span[2]').replace(',', '')[0:-1]
        add_fans_rate_in = page.inner_text(':nth-match(.list--2x72Z, 2) >> //div[2]/span[2]').replace(',', '')[0:-1]
        add_club_rate_in = page.inner_text(':nth-match(.list--2x72Z, 3) >> //div[1]/span[2]').replace(',', '')[0:-1]

        index = ['gmv', 'gpm', 'live_watch_ucount', 'click_rate', 'order_conversion_rate', 'interaction_rate', 'add_fans_rate',
                    'add_club_rate']
        list_num_in = [gmv_in, gpm_in, live_watch_ucount_in, click_rate_in,
                       order_conversion_rate_in, interaction_rate_in, add_fans_rate_in, add_club_rate_in]

        # 预警——创建飞书消息对象
        feishu = SendMsg()
        for i in range(8):
            if float(list_num_in[i]) != float(list_num[i]):
                title = "直播复盘列表页与场内数据不同"
                describe = index[i] + ':场次内' + list_num_in[i] + '不等于场次外' + list_num[i]
                feishu.send_post(title, env=env_util.env, bug='一般', describe=describe, path=page.screenshot())

    @allure.title("商品复盘列表页")
    def test_blankme_shuju02(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        # 接口数据
        data = {
            "operationName": "searchFormValue",
            "variables": {
                "form_slug": "vap_topic_analysis_list",
                "limit": 50,
                "offset": 0,
                "order_by": [
                    {
                        "order_key": "lives_count",
                        "order_option": "DESC"
                    }
                ],
                "filter_entities": [],
                "relation": 1
            },
            "query": "query searchFormValue($form_slug: String, $filters: JSON, $order_by: [OrderByEntity], $limit: Int, $offset: Int, $filter_entities: JSON, $relation: Int, $full_text_search_keyword: String) {\n  searchFormValue(form_slug: $form_slug, filters: $filters, order_by: $order_by, offset: $offset, limit: $limit, filter_entities: $filter_entities, relation: $relation, full_text_search_keyword: $full_text_search_keyword) {\n    items\n    total\n    limit\n    offset\n  }\n}\n"
        }
        response = page.request.post(url=f'https://blankme.{env_util.env}.meetwhale.com/graphql', data=data)

        res_data = response.json()['data']['searchFormValue']['items'][0]
        tid = res_data['tid']  # 商品序号
        gmv = res_data['gmv']  # 成交金额
        gpm = res_data['gpm']
        watch_num = res_data['watch_num']  # 曝光人数
        click_rate = res_data['click_rate']  # 商品点击率
        add_club_rate = res_data['add_club_rate']  # 加团率
        lives_count = res_data['lives_count']  # 场次
        conversion_rate = res_data['conversion_rate']  # 成交转换率
        interaction_rate = res_data['interaction_rate']  # 互动率
        likes_count = res_data['likes_count']  # 点赞数
        comments_count = res_data['comments_count']  # 评论数
        add_fans_rate = res_data['add_fans_rate']  # 加粉率
        add_fans = res_data['add_fans']  # 加粉数
        shares_count = res_data['shares_count']  # 分享数
        list_num = [gmv, gpm, watch_num, click_rate, add_club_rate, lives_count, conversion_rate,
                    interaction_rate, likes_count, comments_count, add_fans_rate, add_fans, shares_count]

        # 根据vid进入直播间
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail/{tid}')
        page.wait_for_timeout(10000)
        gmv_in = page.inner_text('.container--3jst- >> //div[1]/div[1]/div[2]/span').replace(',', '')
        gpm_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[1]/div/div[2]/span').replace(',', '')
        watch_num_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[2]/div/div[2]/span').replace(',',
                                                                                                                  '')
        click_rate_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[3]/div/div[2]/span').replace(',',
                                                                                                                   '')
        add_club_rate_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[4]/div/div[2]/span').replace(
            ',', '')
        lives_count_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[5]/div/div[2]/span').replace(',',
                                                                                                                    '')
        conversion_rate_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[6]/div/div[2]/span').replace(
            ',', '')

        interaction_rate_in = page.inner_text(
            '[class="right--1hy23 bg--TN6Er"] >> //div/div[1]/div[1]/div[2]/span').replace(',', '')
        likes_count_in = page.inner_text('.container--3jst- >> //div[2]/div/div[1]/div[2]/div[1]/div[2]').replace(',',
                                                                                                                  '')
        comments_count_in = page.inner_text('.container--3jst- >> //div[2]/div/div[1]/div[2]/div[2]/div[2]').replace(
            ',', '')
        add_fans_rate_in = page.inner_text(
            '[class="right--1hy23 bg--TN6Er"] >> //div/div[2]/div[1]/div[2]/span').replace(',', '')
        add_fans_in = page.inner_text('.container--3jst- >> //div[2]/div/div[2]/div[2]/div[1]/div[2]').replace(',', '')
        shares_count_in = page.inner_text('.container--3jst- >> //div[2]/div/div[2]/div[2]/div[2]/div[2]').replace(',',
                                                                                                                   '')
        index = ['gmv', 'gpm', 'watch_num', 'click_rate', 'add_club_rate', 'lives_count', 'conversion_rate',
                    'interaction_rate', 'likes_count', 'comments_count', 'add_fans_rate', 'add_fans', 'shares_count']
        list_num_in = [gmv_in, gpm_in, watch_num_in, click_rate_in, add_club_rate_in, lives_count_in,
                       conversion_rate_in,
                       interaction_rate_in, likes_count_in, comments_count_in, add_fans_rate_in, add_fans_in,
                       shares_count_in]

        # 预警——创建飞书消息对象
        feishu = SendMsg()
        for i in range(13):
            if float(list_num_in[i]) != float(list_num[i]):
                title = "商品复盘列表页与场内数据不同"
                describe = index[i] + ':场次内' + list_num_in[i] + '不等于场次外' + list_num[i]
                feishu.send_post(title, env=env_util.env, bug='一般', describe=describe, path=page.screenshot())

    @allure.title("主播复盘列表页")
    def test_blankme_shuju03(self, browser: Browser, login_hyx):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        # 接口数据
        data = {
            "operationName": "searchFormValue",
            "variables": {
                "form_slug": "vap_anchor_list",
                "limit": 50,
                "offset": 0,
                "order_by": [
                    {
                        "order_key": "add_fans_club_rate",
                        "order_option": "DESC"
                    }
                ],
                "filter_entities": [],
                "relation": 1
            },
            "query": "query searchFormValue($form_slug: String, $filters: JSON, $order_by: [OrderByEntity], $limit: Int, $offset: Int, $filter_entities: JSON, $relation: Int, $full_text_search_keyword: String) {\n  searchFormValue(form_slug: $form_slug, filters: $filters, order_by: $order_by, offset: $offset, limit: $limit, filter_entities: $filter_entities, relation: $relation, full_text_search_keyword: $full_text_search_keyword) {\n    items\n    total\n    limit\n    offset\n  }\n}\n"
        }
        response = page.request.post(url=f'https://blankme.{env_util.env}.meetwhale.com/graphql', data=data)

        res_data = response.json()['data']['searchFormValue']['items'][0]
        id = res_data['id']  # 主播id
        gmv = res_data['gmv']  # 成交金额
        gpm = res_data['gpm']
        live_watch_count = res_data['live_watch_count']  # 曝光人数
        product_click_rate = res_data['product_click_rate']  # 商品点击率
        add_fans_club_rate = res_data['add_fans_club_rate']  # 加团率
        lives_count = res_data['lives_count']  # 场次
        transaction_conversion_rate = res_data['transaction_conversion_rate']  # 成交转换率
        interactive_rate = res_data['interactive_rate']  # 互动率
        add_fans_rate = res_data['add_fans_rate']  # 加粉率

        list_num = [gmv, gpm, live_watch_count, product_click_rate, add_fans_club_rate, lives_count,
                    transaction_conversion_rate, interactive_rate, add_fans_rate]

        # 根据vid进入直播间
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/vap/live-analysis-detail?anchorId={id}')
        page.wait_for_timeout(10000)
        gmv_in = page.inner_text('.container--3jst- >> //div[1]/div[1]/div[2]/span').replace(',', '')
        gpm_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[1]/div/div[2]/span').replace(',', '')
        watch_num_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[2]/div/div[2]/span').replace(',',
                                                                                                                  '')
        click_rate_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[3]/div/div[2]/span').replace(',',
                                                                                                                   '')
        add_club_rate_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[4]/div/div[2]/span').replace(
            ',', '')
        lives_count_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[5]/div/div[2]/span').replace(',',
                                                                                                                    '')
        conversion_rate_in = page.inner_text('.container--3jst- >> //div[1]/div[2]/div/div[6]/div/div[2]/span').replace(
            ',', '')

        interaction_rate_in = page.inner_text(
            '[class="right--1hy23 bg--TN6Er"] >> //div/div[1]/div[1]/div[2]/span').replace(',', '')
        add_fans_rate_in = page.inner_text(
            '[class="right--1hy23 bg--TN6Er"] >> //div/div[2]/div[1]/div[2]/span').replace(',', '')

        index = ['gmv', 'gpm', 'live_watch_count', 'product_click_rate', 'add_fans_club_rate', 'lives_count',
                 'transaction_conversion_rate', 'interactive_rate', 'add_fans_rate']
        list_num_in = [gmv_in, gpm_in, watch_num_in, click_rate_in, add_club_rate_in, lives_count_in,
                       conversion_rate_in, interaction_rate_in, add_fans_rate_in]

        # 预警——创建飞书消息对象
        feishu = SendMsg()
        for i in range(9):
            if float(list_num_in[i]) != float(list_num[i]):
                title = "主播复盘列表页与场内数据不同"
                describe = index[i] + ':场次内' + list_num_in[i] + '不等于场次外' + list_num[i]
                feishu.send_post(title, env=env_util.env, bug='一般', describe=describe, path=page.screenshot())


@allure.feature('数据校验')
class TestAliviaBlankMeDataTF:

    @allure.title("直播复盘列表数据")
    def test_blankme_zbfp01(self, browser: Browser):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        # 接口数据
        data = {
            "operationName": "searchFormValue",
            "variables": {
                "form_slug": "vap_douyin_list",
                "limit": 50,
                "offset": 0,
                "order_by": [],
                "filter_entities": [
                    {
                        "filter_key": "status",
                        "operation": 8,
                        "filter_value": "[\"4\"]"  # 分析完成的状态
                    }
                ],
                "relation": 1
            },
            "query": "query searchFormValue($form_slug: String, $filters: JSON, $order_by: [OrderByEntity], $limit: Int, $offset: Int, $filter_entities: JSON, $relation: Int, $full_text_search_keyword: String) {\n  searchFormValue(form_slug: $form_slug, filters: $filters, order_by: $order_by, offset: $offset, limit: $limit, filter_entities: $filter_entities, relation: $relation, full_text_search_keyword: $full_text_search_keyword) {\n    items\n    total\n    limit\n    offset\n  }\n}\n"
        }
        response = page.request.post(url=f'https://blankme.{env_util.env}.meetwhale.com/graphql', data=data)
        list_data = response.json()['data']['searchFormValue']['items']
        page.goto(f'https://blankme.{env_util.env}.meetwhale.com/vap/entry')
        page.wait_for_timeout(5000)
        res = []
        for i in range(len(list_data)):
            res_data = list_data[i]
            vid = int(res_data['vid'])  # 直播间序号
            gmv = float(res_data['gmv'])  # 成交金额
            gpm = float(res_data['gpm'])
            live_watch_ucount = float(res_data['live_watch_ucount'])  # 总观看人数
            click_rate = float(res_data['click_rate'])  # 点击率
            order_conversion_rate = float(res_data['order_conversion_rate'])  # 成交转换率
            interaction_rate = float(res_data['interaction_rate'])  # 互动率
            add_fans_rate = float(res_data['add_fans_rate'])  # 加粉率
            add_club_rate = float(res_data['add_club_rate'])  # 加团率
            list_num = [gmv, gpm, live_watch_ucount, click_rate,
                        order_conversion_rate, interaction_rate, add_fans_rate, add_club_rate]
            zero_num = 0
            for j in range(len(list_num)):
                if list_num[j] == 0:
                    zero_num += 1
            # 至少有3个为0才告警
            if zero_num >= 3:
                res.append(f"直播间{vid}有{zero_num}个指标为0")
        if len(res) > 0:
            # 预警——创建飞书消息对象
            feishu = SendMsg()
            title = "直播复盘列表页数据问题"
            describe = str(res)
            feishu.send_post(title, env=env_util.env, bug='一般', describe=describe, path=page.screenshot())

    @allure.title("直播场控数据")
    def test_blankme_zbck01(self, browser: Browser):
        context = browser.new_context(storage_state="./data/blankMe_cookie_hyx.json")
        page = context.new_page()
        page.goto(f"https://blankme.{env_util.env}.meetwhale.com/vap/live-list")
        text = page.inner_text('.ant-table-tbody >> //tr[2]//td/div')
        page.wait_for_timeout(1000)
        page.click('.ant-table-tbody >> //tr[2]')
        with context.expect_page() as new_page_info:
            page.click("text='场控视角'")
        new_page = new_page_info.value
        new_page.wait_for_timeout(5000)
        content = new_page.inner_html('text="实时直播内容" >> //../div[2]')
        if "暂无直播内容</div>" in content:
            feishu = SendMsg()
            title = "直播场控数据问题"
            describe = "直播场控暂无评论"
            feishu.send_post(title, env=env_util.env, bug='一般', describe=describe, path=new_page.screenshot())




