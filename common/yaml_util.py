import yaml
import os


# 获取根目录
def get_obj_path():
    return os.path.dirname(__file__).split('common')[0]


# 读取yaml文件
def read_yaml(yamlpath):
    with open(get_obj_path()+yamlpath, mode='r', encoding='utf-8') as f:
        # 数据流；加上Loader=yaml.FullLoader 避免警告;返回字典或者列表（根据读取的文件）
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value


if __name__ == '__main__':
    x = read_yaml('test_test/test.yaml')
    print(x)
