import time
import inspect
import threading
from .log import *
from typing import Optional
from queue import PriorityQueue
from .requestXpath import prequest
from concurrent.futures import ThreadPoolExecutor, as_completed


class _IT:
    def __init__(self, level, data):
        self.level = level
        self.data = data

    def __lt__(self, other):
        if self.level == other.level:
            return len(self.data) < len(other.data)
        return self.level < other.level


class settions(object):
    """设置"""
    thread_num: Optional[int] = 10  # 线程数
    request_num: Optional[int] = 0  # 请求数
    retry_num: Optional[int] = 0  # 重试数
    success_num: Optional[int] = 0  # 成功请求数
    false_num: Optional[int] = 0  # 失败请求数
    start_urls: Optional[list] = None  # 默认请求起始url
    executor: Optional[object] = object  # 线程池处理器
    retry: Optional[bool] = True  # 重试开关，默认开启
    retry_xpath: Optional[str] = None  # 重试开关，默认开启
    pid: Optional[int] = os.getppid()  # 程序进程id
    start_time: Optional[int] = time.time()  # 开始时间
    download_delay: Optional[int] = 0  # 请求下载周期 默认 0s
    download_num: Optional[int] = 5  # 请求下载数量 默认 5/次
    logger: Optional[bool or str] = False  # 日志存储开关，默认关闭；可选（bool|文件名）
    log_level: Optional[str] = 'info'  # 日志等级，默认info
    log_stdout: Optional[bool] = False  # 日志控制台重定向，默认关闭
    futures: Optional[list] = set()  # 线程池对象
    init: Optional[int] = 0  # 日志初始化
    Queues: Optional[object] = PriorityQueue()
    deep_func: Optional[list] = []


class PrSpiders2(settions):

    def __init__(self, **kwargs):
        settions.init += 1
        if settions.init <= 1:
            Log(self.log_stdout, self.log_level, self.logger).loggering()
        settions.request_num = self.request_num
        settions.success_num = self.success_num
        settions.false_num = self.false_num
        settions.retry = self.retry
        settions.retry_xpath = self.retry_xpath
        settions.futures = self.futures
        settions.thread_num = self.thread_num
        settions.download_delay = self.download_delay
        settions.executor = ThreadPoolExecutor(settions.thread_num)
        settions.download_num = self.download_num
        settions.logger = self.logger
        settions.log_stdout = self.log_stdout
        settions.log_level = self.log_level
        settions.Queues = self.Queues
        loguercor.log('Start',
                      "<red>~~~ @PrSpider Start  @Thread Num %s  @Retry %s  @Pid %s @Download_Delay %s @Download_Num %s @LOG_LEVEL %s ~~~</red>"
                      % (
                          self.thread_num,
                          self.retry,
                          self.pid,
                          self.download_delay,
                          self.download_num,
                          self.log_level.upper(),
                      )
                      )
        self.spider_run()

    def spider_run(self):
        """
        线程一: 爬虫业务代码（请求入队列）
        线程二: 监听队列
        """
        self.thread_requests = threading.Thread(target=self.start_call)
        self.thread_queue = threading.Thread(target=self.start_queue)

        # 启动线程
        self.thread_requests.start()
        self.thread_queue.start()

        # 等待线程结束
        self.thread_requests.join()
        self.thread_queue.join()

    def start_queue(self):
        while True:
            qlist = []
            qsize = self.Queues.qsize()
            # 检查队列是否为空
            if not self.Queues.empty():
                queue_list = []
                if qsize >= self.download_num:
                    # 从队列中获取数据
                    for i in range(self.download_num):
                        data = settions.Queues.get().data
                        wait = data.get('wait')
                        queue_list.append(data)
                        del data['wait']
                        if wait:
                            break

                else:
                    for i in range(qsize):
                        data = settions.Queues.get().data
                        wait = data.get('wait')
                        queue_list.append(data)
                        del data['wait']
                        if wait:
                            break
                qlist.append(queue_list)

                for qdata in qlist:
                    for item in qdata:
                        task = self.executor.submit(self.make_request, **item)
                        self.futures.add(task)
                    for future in as_completed(self.futures):
                        worker_exception = future.exception()
                        self.futures.remove(future)
                        if worker_exception:
                            loguercor.error(f"<red>[PrSpider Exception] %s</red>" % worker_exception)
                    time.sleep(settions.download_delay)
            else:
                if self.thread_requests.is_alive():
                    pass
                else:
                    break

    def start_call(self, *args, **kwargs):
        self.open_spider()
        self.start_requests(*args, **kwargs)
        while True:
            if not settions.futures and not self.Queues.qsize():
                break
            time.sleep(0.5)
        self.close_spider()

    def open_spider(self):
        pass

    def close_spider(self):
        pass

    def start_requests(self, *args, **kwargs):
        if self.start_urls is None:
            raise AttributeError("Crawling could not start: 'start_urls' not found ")
        if isinstance(self.start_urls, list):
            for url in self.start_urls:
                self.Request(url=url, callback=self.parse)
        else:
            self.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        pass

    @staticmethod
    def Request(url, headers=None, method="GET", meta=None, retry=True, callback=None, retry_num=3,
                encoding="utf-8", retry_time=3, timeout=30, priority=0, wait=False, **kwargs):
        query = {
            "url": url,
            "headers": headers,
            "method": method,
            "meta": meta,
            "retry": retry,
            "callback": callback,
            "retry_num": retry_num,
            "encoding": encoding,
            "retry_time": retry_time,
            "timeout": timeout,
            "wait": wait,
        }
        frame = inspect.currentframe().f_back
        caller_name = frame.f_code.co_name
        if caller_name == 'start_requests':
            deep = priority
        else:
            if priority != 0:
                deep = priority
            else:
                if caller_name not in settions.deep_func:
                    settions.deep_func.append(caller_name)
                deep = -(settions.deep_func.index(caller_name)) - 1
        query.update(**kwargs)
        item = _IT(deep, query)
        settions.Queues.put(item)

    def make_request(self, url, callback, headers=None, retry_num=3, method="GET", meta=None, retry=True,
                     encoding="utf-8", retry_time=1, timeout=30, **kwargs):
        settions.request_num += 1
        loguercor.log('Crawl',
                      f"<red>{method.upper()}</red> <blue>{url}</blue>")
        response = prequest().get(
            url,
            headers=headers,
            retry_time=retry_num,
            method=method,
            meta=meta,
            retry=retry,
            encoding=encoding,
            retry_interval=retry_time,
            timeout=timeout,
            settion=settions,
            **kwargs,
        )
        self.retry_num += int(response.meta.get("retry_num"))
        if response:
            if response.ok:
                settions.success_num += 1
                return callable(callback(response))
            else:
                settions.false_num += 1
                return callable(callback(response))
        else:
            settions.false_num += 1
            callback(response)
            return self

    def process_timestamp(self, t):
        timeArray = time.localtime(int(t))
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return formatTime

    def __del__(self):
        end_time = time.time()
        spend_time = end_time - self.start_time
        try:
            average_time = spend_time / self.request_num
        except ZeroDivisionError:
            average_time = 0
        m = """<green><Spider End>
| ------------------ | ----------------------                               
| `Workers`          | `%s`                                             
| `Download Delay`   | `%s`                                             
| `Download Num`     | `%s`                                             
| `Request Num`      | `%s`                                             
| `Success Num`      | `%s`                                             
| `False Num`        | `%s`                                              
| `Retry Num`        | `%s`                                              
| `Start Time`       | `%s`                                              
| `End Time`         | `%s`                                             
| `Spend Time`       | `%.3fs`                                          
| `Average Time`     | `%.3fs`         
| ------------------ | ---------------------- </green>                          
        """ % (
            self.thread_num,
            self.download_delay,
            self.download_num,
            self.request_num,
            self.success_num,
            self.false_num,
            self.retry_num,
            self.process_timestamp(self.start_time),
            self.process_timestamp(end_time),
            spend_time,
            average_time,
        )
        loguer.opt(colors=True).info(m)
