import requests
import time
import logging
from collections import Counter


def use_proxy(proxy_arg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if callable(proxy_arg):
                proxies = proxy_arg()  # 프록시 IP를 가져옴
            elif isinstance(proxy_arg, requests.sessions.ProxyDict):
                proxies = proxy_arg
            else:
                raise ValueError("Invalid proxy argument")

            return func(proxies=proxies, *args, **kwargs)

        return wrapper
    return decorator


# def retryV2(max_attempts=3, retry_interval=3., request_wait_time=0, response_wait_time=0, proxies=None):
def retryV2(max_attempts=3, retry_interval=3., request_wait_time=0, response_wait_time=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    if request_wait_time > 0:
                        time.sleep(request_wait_time)  # 요청 전 대기 시간 설정
                    response = func(*args, **kwargs)

                    if response_wait_time > 0:
                        time.sleep(response_wait_time)  # 요청 후 대기 시간 설정

                    return response

                except requests.exceptions.RequestException as e:
                    time.sleep(retry_interval)  # 재시도 간격 설정
                    attempts += 1
            logging.error("모든 프록시를 시도한 후에도 요청이 실패했습니다.")

        return wrapper

    return decorator


def retry(max_attempts=3, retry_interval=3., request_wait_time=0, response_wait_time=0, proxies=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            proxy_counts = Counter()

            while attempts < max_attempts:
                # 프록시 우선순위를 정하는 함수
                def proxy_priority(proxy):
                    return proxy_counts[proxy]
                if proxies:
                    proxy = min(proxies, key=proxy_priority)
                else:
                    proxy = None
                try:
                    if request_wait_time > 0:
                        time.sleep(request_wait_time)  # 요청 전 대기 시간 설정

                    response = func(proxy=proxy, *args, **kwargs)

                    if response_wait_time > 0:
                        time.sleep(response_wait_time)  # 요청 후 대기 시간 설정

                    logging.info(f"프록시 {proxy}를 사용하여 요청 성공")
                    return response

                except requests.exceptions.RequestException as e:
                    logging.info(f"프록시 {proxy}를 사용하여 요청 실패: {e}")
                    time.sleep(retry_interval)  # 재시도 간격 설정
                    attempts += 1
                    proxy_counts[proxy] += 1

            logging.error("모든 프록시를 시도한 후에도 요청이 실패했습니다.")

        return wrapper

    return decorator
