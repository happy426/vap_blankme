import time

import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler


class FeishuAlert():
    def __init__(self):
        self.webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/74d0a3e4-b215-4f22-85c9-c607d6f7be25"
        self.headers = {'Content-Type': 'application/json'}

    def post_to_robot(self, alert_headers: str, alert_content: str):
        # webhook：飞书群地址url
        webhook = self.webhook
        # headers: 请求头
        headers = self.headers

        # alert_headers: 告警消息标题
        alert_headers = alert_headers
        # alert_content: 告警消息内容，用户可根据自身业务内容，定义告警内容
        alert_content = alert_content
        # message_body: 请求信息主体
        message_body = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": alert_content,
                            "tag": "lark_md"
                        }
                    }
                ],
                "header": {
                    "template": "red",
                    "title": {
                        "content": alert_headers,
                        "tag": "plain_text"
                    }
                }
            }}
        response = requests.request("POST", webhook, headers=headers, data=json.dumps(message_body))
        print(response)


if __name__ == '__main__':
    """
        "msg_type"参数说明： 飞书告警目前只支持类型4个参数
        post  富文本
        image 图片
        share_chat	分享群名片
        interactive	 消息卡片
        template"参数说明： 主体颜色
    """
    alert = FeishuAlert()
    title = "测试告警"
    content = "这是一个bug"
    while True:
        alert.post_to_robot(title, content)
        time.sleep(10)

