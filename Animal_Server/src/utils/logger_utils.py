import logging

def log_common(msg: str):
    """
    记录日志信息
    Args:
        msg (str): 日志信息
    """
    logger = logging.getLogger('django')
    logger.info(msg)
    

def log_request(request_body: str):
    """
    记录请求体的日志。
    Args:
        request_body (str): 请求体数据。
    """
    logger = logging.getLogger('django')
    log_message = f'Request Body: {request_body}'
    logger.info(log_message)


def log_response(response_body: str):
    """
    记录响应体的日志。
    Args:
        response_body (str): 响应体数据。
    """
    logger = logging.getLogger('django')
    log_message = f'Response Body: {response_body}'
    logger.info(log_message)


if __name__ == '__main__':
    pass
