from inspect import stack
from json import loads
from os import path
from re import findall, I
from time import time
from urllib import parse
from urllib.parse import parse_qs, urlparse

from jinja2 import Template


class AnalyObj:
    """解析对象"""

    def __init__(self, url: str, method: str,
                 data: dict, headers: dict, cookies: dict):
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers
        self.cookies = cookies


class CodeGener:
    def __init__(self, analy: AnalyObj, template_name: str):
        self.analy = analy

        current_path = path.abspath(__file__)  # 绝对路径获取
        parent_dir = path.dirname(path.dirname(current_path))

        # 读取Jinja2模板
        with open(path.join(parent_dir, 'template', template_name),
                  encoding='utf-8') as f:
            self.template = Template(f.read())

    def crawler_craft(self) -> str:
        """crawles 代码与模板合成传参"""
        args = 'data' if self.analy.method == 'post' else 'params'

        return self.template.render(url=self.analy.url, cookies=self.analy.cookies,
                                    headers=self.analy.headers, args=args,
                                    data=self.analy.data, method=self.analy.method,
                                    time=time())


class CurlAnaly:
    def __init__(self, curl_text):
        self.curl_text = curl_text.replace('^', '') \
            .replace('   -', ' \n   -') \
            .replace("'", '"')  # 预处理

    def url_args_get(self) -> (str, dict):
        """url和请求参数的获取"""
        # 提取 URL
        url = findall('''curl\s*['"](.*?)['"]''', self.curl_text)[0]

        # 提取参数
        parsed_url = urlparse(url)  # url
        query_params = parse_qs(parsed_url.query)  # args

        # 格式化参数为字典
        data_dict = {key: value[0] for key, value in query_params.items()}
        url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
        return url, data_dict

    def headers_get(self) -> (dict, dict):
        """headers cookies"""
        head_data = findall('''-H ['"](.*)['"] ''', self.curl_text)

        if not head_data:
            return {}, {}

        head_dict = {}
        cookies = {}
        for data in head_data:  # 将文本以行进行分割
            data: str = data.strip()
            if not data:  # 过滤掉空的数据
                continue
            if data.startswith(':'):  # 去重字符串的第一个冒号
                data = data.lstrip(':')

            key, value = data.split(':', maxsplit=1)
            if findall('cookie', key, flags=I):  # cookie 解析
                cookie_list = [str(c).strip().split('=', 1) for c in str(value).split(';')]
                cookies = {i[0]: i[1] for i in cookie_list if len(i) == 2}
            else:
                head_dict[key] = value.strip()

        return head_dict, cookies

    def data_get(self) -> (str, dict):
        """method and data"""

        data_list: list = findall('''--data-raw ['"](.*?)['"] ''', self.curl_text)
        if not data_list:
            return 'get', dict()

        data_str: str = data_list[0]
        if data_str.startswith('{') and data_str.endswith('}'):
            return 'json_post', loads(data_str)
        else:
            data = {key: value for key, value in (i.split('=') for i in data_str.split('&'))}
            return 'post', data

    def curl_analy(self) -> AnalyObj:
        """请求数据解析"""
        url, data = self.url_args_get()  # 参数解析
        headers, cookies = self.headers_get()
        method, data_dict = self.data_get()

        data = {k: parse.unquote(v) for k, v in {**data, **data_dict}.items()}
        headers = {k: parse.unquote(v) for k, v in headers.items()}
        cookies = {k: parse.unquote(v) for k, v in cookies.items()}

        return AnalyObj(url, method, data, headers, cookies)


class TemplateDecor:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # 获取文件调用
        frame_info = stack()[1]
        filepath = frame_info[1]
        del frame_info

        filepath = path.abspath(filepath)

        self.result = self.func(*args, **kwargs)

        # 复写文件
        f = open(filepath, 'w+', encoding='utf-8')
        f.write(self.result)
        f.close()

        return self.result


@TemplateDecor
def curl_anal(curl_str) -> str:
    """基础模板"""
    curl_anal_ = CurlAnaly(curl_str).curl_analy()
    # 数据解析 curl_anal
    # base_crawler.j2 使用的模板文件
    # crawler_craft 调用的合成方法
    return CodeGener(curl_anal_, 'base_crawler.j2').crawler_craft()


@TemplateDecor
def curl_anal_cls(curl_str) -> str:
    """类模板"""
    curl_anal_ = CurlAnaly(curl_str).curl_analy()  # 数据解析
    return CodeGener(curl_anal_, 'class_crawler.j2').crawler_craft()


@TemplateDecor
def curl_anal_thread(curl_str) -> str:
    """线程模板"""
    curl_anal_ = CurlAnaly(curl_str).curl_analy()  # 数据解析
    return CodeGener(curl_anal_, 'thread_crawler.j2').crawler_craft()


if __name__ == '__main__':
    pass
