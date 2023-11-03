from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from copy import copy
from queue import Queue, Empty
from threading import Lock
from time import time

from .._api.api import post, get


class Pipeline(metaclass=ABCMeta):
    concurrency = 10  # 并发数量
    __name__ = 'Pipeline'

    @abstractmethod
    def save_data(self, item):
        pass

    @abstractmethod
    def close(self):
        pass


class Item(dict):  # 传输数据对象
    __name__ = 'Item'


class Request:  # 请求对象
    __name__ = 'Request'

    def __init__(self):
        self.url = None
        self.cookies = {}
        self.headers = {}
        self.callback = None
        self.method = 'GET'
        self.data = {}
        self.index = 0


class ThreadPool(metaclass=ABCMeta):
    save_class = None  # 爬虫存储类
    concurrency = 16  # 并发数量
    timeout = 3  # 等待时间
    info_display = True  # 爬取信息显示

    # 是否重试 待完成
    # 重试次数 待完成

    def __init__(self):
        self._qsize = 0  # 队列大小
        self._produce = 5  # 生产者数量
        self._consume = 10  # 消费者数量
        self.timeout_ = 0.2  # 超时断开
        self.request_index = 0  # 请求次数记录

        self.request = Request()  # 请求对象
        self.queue_ = Queue(self._qsize)  # 队列
        self.executor = ThreadPoolExecutor(self.concurrency)  # 线程池
        self.lock = Lock()  # 锁
        if self.save_class is not None:  # 存储对象初始化
            self.save_class_ = self.save_class()

        self.request_obj = False  # 请求对象 用于判断请求是否已经完成
        self.futures = []  # 任务表

        self.run()

    def run(self):
        start_time = time()
        # 初始化启动线程
        ThreadPoolExecutor(max_workers=1).submit(self.start_request)

        # 运行消费者
        _consume_list = [ThreadPoolExecutor(max_workers=1).submit(self.data_save_)
                         for _ in range(self.save_class.concurrency)]

        while self.futures:  # 等待请求线程池完成
            completed = [future for future in self.futures if future.done()]
            [self.futures.remove(future) for future in completed]

        self.request_obj = True  # 生产者完成，那消费者也可以停止了

        # 等待消费者线程完成
        wait(_consume_list, return_when=ALL_COMPLETED)

        if self.save_class:
            self.save_class_.close()  # 关闭文件存储

        self.executor.shutdown()  # 关闭线程池

        stop_time = time()
        if self.info_display:
            print(f'运行用时:{round(stop_time - start_time, 2)}秒 '
                  f'请求次数:{self.request_index}')

    def start_request(self) -> None:  # 初始链接请求
        for index, request_ in enumerate(self.start_requests(self.request), start=1):
            with self.lock:
                self.request_index += 1
                request_.index = self.request_index
            self.futures.append(self.executor.submit(self.callback_, copy(request_)))

    def callback_(self, request_: Request):  # 回调获取
        # 获取响应体

        request_.method = request_.method.upper()
        if request_.method == 'POST':
            response = post(request_.url, data=request_.data, timeout=3)
        elif request_.method == 'JSON_POST':
            response = post(request_.url, json=request_.data, timeout=3)
        elif request_.method == 'GET':
            response = get(request_.url, params=request_.data, timeout=3)
        else:
            raise ValueError(f'request_.method:未知的请求类型{request_.method}:POST/JSON_POST/GET')

        # 爬取信息显示
        if self.info_display:
            with self.lock:
                print(f'status:{response} index:{request_.index}')

        # 回调数据获取
        for return_ in request_.callback(Item(), request_, response):

            if return_.__name__ == 'Request':
                with self.lock:  # 全局请求次数锁
                    self.request_index += 1
                    request_.index = self.request_index
                self.futures.append(self.executor.submit(self.callback_, copy(request_)))

            elif return_.__name__ == 'Item' or isinstance(return_, dict):
                self.queue_.put(return_)

    def data_save_(self) -> None:  # 数据存储
        while True:
            try:
                items = self.queue_.get(timeout=self.timeout_)
                if self.save_class:
                    self.executor.submit(self.save_class_.save_data, items)
                else:
                    break
            except Empty:
                if self.request_obj:  # 请求队列完成了，可以结束了
                    break
            except Exception as e:
                print(e)

    @abstractmethod
    def start_requests(self, request_: Request):
        pass

    @abstractmethod
    def parse(self, item: Item, request_: Request, response):
        pass
