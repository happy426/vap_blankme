# 测试框架
## python3 + pytest + playwright + allure
## 下载镜像加速：
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple
## 调试
playwright codegen wikipedia.org
## 模块解释：
- common 存放需要调用的函数（log,yaml等函数）
- data 存放日志文件，界面定位元素（yaml）
- report 存放测试报告
- temp 存放allure生成的临时json
- testcase存放测试用例。
- all.py 运行脚本
- pytest.ini pytest执行配置文件
- robot.py 输出到飞书机器人
- env_util.py 更改用例环境