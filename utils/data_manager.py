"""
数据管理工具
负责测试数据的读取和管理
"""
import os
import json
import pandas as pd
from typing import Dict, List, Any, Optional

from config import config_manager
from utils.logger_manager import get_logger


class DataManager:
    """数据管理器"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = config_manager
        self.data_dir = self.config.get_project_path(
            self.config.get('data.test_data_dir', 'data')
        )
        os.makedirs(self.data_dir, exist_ok=True)
    
    def read_json_data(self, filename: str) -> Dict[str, Any]:
        """
        读取JSON数据文件
        
        Args:
            filename: 文件名
            
        Returns:
            JSON数据字典
        """
        try:
            filepath = os.path.join(self.data_dir, filename)
            
            if not os.path.exists(filepath):
                self.logger.warning(f"数据文件不存在: {filepath}")
                return {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"读取JSON数据成功: {filename}")
            return data
            
        except Exception as e:
            self.logger.error(f"读取JSON数据失败: {filename}, 错误: {e}")
            return {}
    
    def write_json_data(self, filename: str, data: Dict[str, Any]) -> bool:
        """
        写入JSON数据文件
        
        Args:
            filename: 文件名
            data: 要写入的数据
            
        Returns:
            是否成功
        """
        try:
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"写入JSON数据成功: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"写入JSON数据失败: {filename}, 错误: {e}")
            return False
    
    def read_excel_data(self, filename: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """
        读取Excel数据文件
        
        Args:
            filename: 文件名
            sheet_name: 工作表名称，如果为None则读取第一个工作表
            
        Returns:
            数据列表，每行为一个字典
        """
        try:
            filepath = os.path.join(self.data_dir, filename)
            
            if not os.path.exists(filepath):
                self.logger.warning(f"Excel文件不存在: {filepath}")
                return []
            
            # 读取Excel文件
            if sheet_name:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
            else:
                df = pd.read_excel(filepath)
            
            # 转换为字典列表
            data = df.to_dict('records')
            
            self.logger.info(f"读取Excel数据成功: {filename}, 行数: {len(data)}")
            return data
            
        except Exception as e:
            self.logger.error(f"读取Excel数据失败: {filename}, 错误: {e}")
            return []
    
    def get_test_data(self, test_name: str) -> Dict[str, Any]:
        """
        获取特定测试的数据
        
        Args:
            test_name: 测试名称
            
        Returns:
            测试数据字典
        """
        # 首先尝试读取专门的测试数据文件
        test_data_file = f"{test_name}_data.json"
        test_data = self.read_json_data(test_data_file)
        
        if test_data:
            return test_data
        
        # 如果没有专门的文件，尝试从通用数据文件中读取
        general_data_file = self.config.get('data.json_file', 'test_data.json')
        general_data = self.read_json_data(general_data_file)
        
        return general_data.get(test_name, {})
    
    def get_login_test_data(self) -> List[Dict[str, str]]:
        """获取登录测试数据"""
        # 尝试从Excel文件读取
        excel_file = self.config.get('data.excel_file', 'test_data.xlsx')
        excel_data = self.read_excel_data(excel_file, 'login_data')
        
        if excel_data:
            return excel_data
        
        # 如果Excel数据不存在，返回默认数据
        default_data = [
            {
                "username": "test_user",
                "password": "test_password",
                "expected_result": "success",
                "description": "有效登录"
            },
            {
                "username": "invalid_user",
                "password": "invalid_password",
                "expected_result": "failure",
                "description": "无效用户名密码"
            },
            {
                "username": "",
                "password": "password",
                "expected_result": "failure",
                "description": "空用户名"
            },
            {
                "username": "username",
                "password": "",
                "expected_result": "failure",
                "description": "空密码"
            }
        ]
        
        return default_data
    
    def create_sample_data_files(self):
        """创建示例数据文件"""
        try:
            # 创建JSON数据文件
            json_data = {
                "login_test": {
                    "valid_users": [
                        {"username": "admin", "password": "admin123"},
                        {"username": "user1", "password": "password1"},
                        {"username": "test", "password": "test123"}
                    ],
                    "invalid_users": [
                        {"username": "invalid", "password": "invalid"},
                        {"username": "wrong", "password": "wrong123"}
                    ]
                },
                "app_config": {
                    "timeout": 30,
                    "retry_count": 3,
                    "base_url": "https://api.example.com"
                }
            }
            
            self.write_json_data("test_data.json", json_data)
            
            # 创建Excel数据文件
            login_data = pd.DataFrame([
                {"username": "test_user", "password": "test_password", "expected_result": "success", "description": "有效登录"},
                {"username": "invalid_user", "password": "invalid_password", "expected_result": "failure", "description": "无效登录"},
                {"username": "", "password": "password", "expected_result": "failure", "description": "空用户名"},
                {"username": "username", "password": "", "expected_result": "failure", "description": "空密码"},
                {"username": "admin", "password": "admin123", "expected_result": "success", "description": "管理员登录"}
            ])
            
            excel_path = os.path.join(self.data_dir, "test_data.xlsx")
            with pd.ExcelWriter(excel_path) as writer:
                login_data.to_excel(writer, sheet_name='login_data', index=False)
            
            self.logger.info("示例数据文件创建成功")
            
        except Exception as e:
            self.logger.error(f"创建示例数据文件失败: {e}")


# 全局数据管理器实例
data_manager = DataManager()