"""
通用工具函数
"""
import time
import random
import string
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils.logger_manager import get_logger


logger = get_logger(__name__)


def generate_random_string(length: int = 10, include_digits: bool = True, 
                          include_uppercase: bool = True, include_lowercase: bool = True) -> str:
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
        include_digits: 是否包含数字
        include_uppercase: 是否包含大写字母
        include_lowercase: 是否包含小写字母
        
    Returns:
        随机字符串
    """
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    
    if not characters:
        characters = string.ascii_letters + string.digits
    
    return ''.join(random.choice(characters) for _ in range(length))


def generate_test_email(domain: str = "test.com") -> str:
    """
    生成测试邮箱地址
    
    Args:
        domain: 邮箱域名
        
    Returns:
        邮箱地址
    """
    username = generate_random_string(8, include_uppercase=False)
    return f"{username}@{domain}"


def generate_test_phone() -> str:
    """
    生成测试手机号
    
    Returns:
        手机号字符串
    """
    # 生成11位手机号，以13/15/18开头
    prefix = random.choice(['13', '15', '18'])
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return prefix + suffix


def generate_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """
    生成时间戳字符串
    
    Args:
        format_str: 时间格式
        
    Returns:
        时间戳字符串
    """
    return datetime.now().strftime(format_str)


def wait_for_condition(condition_func, timeout: int = 30, interval: float = 1.0) -> bool:
    """
    等待条件满足
    
    Args:
        condition_func: 条件函数，返回布尔值
        timeout: 超时时间（秒）
        interval: 检查间隔（秒）
        
    Returns:
        条件是否在超时前满足
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            if condition_func():
                return True
        except Exception as e:
            logger.debug(f"条件检查异常: {e}")
        
        time.sleep(interval)
    
    return False


def retry_on_exception(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    异常重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔
        exceptions: 要捕获的异常类型
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"函数 {func.__name__} 第 {attempt + 1} 次尝试失败: {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"函数 {func.__name__} 重试 {max_retries} 次后仍失败")
            
            raise last_exception
        
        return wrapper
    return decorator


def calculate_file_hash(filepath: str, algorithm: str = "md5") -> str:
    """
    计算文件哈希值
    
    Args:
        filepath: 文件路径
        algorithm: 哈希算法 (md5, sha1, sha256)
        
    Returns:
        哈希值字符串
    """
    try:
        hash_obj = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
        
    except Exception as e:
        logger.error(f"计算文件哈希失败: {e}")
        return ""


def format_duration(seconds: float) -> str:
    """
    格式化持续时间
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
    """
    if seconds < 60:
        return f"{seconds:.2f}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}分{secs:.2f}秒"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}小时{minutes}分{secs:.2f}秒"


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个字典
    
    Args:
        *dicts: 要合并的字典
        
    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def safe_get_nested_value(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    安全获取嵌套字典的值
    
    Args:
        data: 数据字典
        key_path: 键路径，用'.'分隔
        default: 默认值
        
    Returns:
        获取到的值或默认值
    """
    try:
        keys = key_path.split('.')
        value = data
        
        for key in keys:
            value = value[key]
        
        return value
        
    except (KeyError, TypeError, AttributeError):
        return default


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        是否有效
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国大陆）
    
    Args:
        phone: 手机号
        
    Returns:
        是否有效
    """
    import re
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def convert_size_to_bytes(size_str: str) -> int:
    """
    将大小字符串转换为字节数
    
    Args:
        size_str: 大小字符串，如 "1MB", "500KB"
        
    Returns:
        字节数
    """
    import re
    
    # 移除空格并转换为大写
    size_str = size_str.strip().upper()
    
    # 匹配数字和单位
    match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$', size_str)
    
    if not match:
        raise ValueError(f"无效的大小格式: {size_str}")
    
    number = float(match.group(1))
    unit = match.group(2)
    
    # 转换倍数
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4
    }
    
    multiplier = multipliers.get(unit, 1)
    return int(number * multiplier)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断字符串
    
    Args:
        text: 原字符串
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        截断后的字符串
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix