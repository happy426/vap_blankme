import requests
from requests_toolbelt import MultipartEncoder


class SendMsg:
    def __init__(self):
        # self.app_id = app_id  # 发送图片时需要
        # self.app_secret = app_secret  # 发送图片时需要
        # self.web_hook_url = web_hook_url  # 机器人web_hook地址 下面我写死了
        self.app_id = 'cli_a26d2aae6ca4d00c'
        self.app_secret = 'olH6HhohXAbPzLZyaO09zgdT8tGMn8cY'
        self.web_hook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/74d0a3e4-b215-4f22-85c9-c607d6f7be25'

    # 获取token为上传图片时使用
    def get_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        body = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        r = requests.request(method='post', url=url, json=body)
        # print(r.json())
        return r.json()['tenant_access_token']

    # 上传图片生成image id
    def uploadImage(self, image_rb):
        tenant_access_token = self.get_tenant_access_token()
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        # form = {'image_type': 'message',
        #         'image': (open(image_rb, 'rb'))}  # image_rb:是本地路径里的图
        form = {'image_type': 'message',
                'image': image_rb}  # image_rb:是以rb格式读的图片内容，也可以是ui自动截的图，直接传过来
        multi_form = MultipartEncoder(form)
        headers = {'Authorization': 'Bearer {}'.format(tenant_access_token), 'Content-Type': multi_form.content_type}
        response = requests.request("POST", url, headers=headers, data=multi_form)
        # print(response.headers['X-Tt-Logid'])  # for debug or oncall
        # print(response.json())  # Print Response
        return response.json()['data']['image_key']

    def send_post(self, title, bug, env, describe, path):
        """
        title: 发送消息的标题
        content: 使用富文本格式:https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json
        """
        body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [{
                                "tag": "text",
                                "text": "缺陷等级:"  # 第一行
                            },
                                {
                                    "tag": "text",
                                    "text": bug
                                },
                                {
                                    "tag": "at",
                                    "user_id": "all",
                                    "user_name": "all"
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": "测试环境:"  # 第二行
                            },
                                {
                                    "tag": "text",
                                    "text": env
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": "问题描述:"  # 第三行
                            },
                                {
                                    "tag": "text",
                                    "text": describe
                                }
                            ],
                            [{
                                "tag": "img",
                                "image_key": SendMsg().uploadImage(path)
                            }]
                        ]
                    }
                }
            }
        }
        r = requests.request(method='post', url=self.web_hook_url, json=body)
        # print(r.json())

# content = [
#         [{
#             "tag": "text",
#             "text": "缺陷等级 :"
#         },
#             {
#                 "tag": "a",
#                 "href": "http://www.feishu.cn",
#                 "text": "超链接"
#             },
#             {
#                 "tag": "at",
#                 "user_id": "all",
#                 "user_name": "all"
#             }
#         ],
#         [{
#             "tag": "text",
#             "text": "第二行:"
#         },
#             {
#                 "tag": "text",
#                 "text": "文本测试"
#             }
#         ],
#         [{
#             "tag": "img",
#             "image_key": image_key
#         }]
#     ]


# if __name__ == '__main__':
#     feishu = SendMsg()
#     path = '/Users/edy/Desktop/头像01.jpeg'
#     feishu.send_post(title='这是测试', bug='debug', env='stage', path=path)

