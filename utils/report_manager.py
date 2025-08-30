"""
报告管理工具
负责测试报告的生成和管理
"""
import os
import shutil
import subprocess
from datetime import datetime
from typing import Optional

from config import config_manager
from utils.logger_manager import get_logger


class ReportManager:
    """报告管理器"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = config_manager
        self.reports_dir = self.config.get_project_path("reports")
        self.allure_results_dir = self.config.get_project_path(
            self.config.get('report.allure_results_dir', 'reports/allure-results')
        )
        self.html_report_dir = self.config.get_project_path(
            self.config.get('report.html_report_dir', 'reports/html')
        )
        
        # 创建报告目录
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.allure_results_dir, exist_ok=True)
        os.makedirs(self.html_report_dir, exist_ok=True)
    
    def clean_allure_results(self):
        """清理Allure结果目录"""
        try:
            if os.path.exists(self.allure_results_dir):
                shutil.rmtree(self.allure_results_dir)
                os.makedirs(self.allure_results_dir, exist_ok=True)
                self.logger.info("Allure结果目录已清理")
        except Exception as e:
            self.logger.error(f"清理Allure结果目录失败: {e}")
    
    def generate_allure_report(self, clean_first: bool = True) -> bool:
        """
        生成Allure报告
        
        Args:
            clean_first: 是否先清理旧报告
            
        Returns:
            是否生成成功
        """
        try:
            if clean_first and os.path.exists(self.html_report_dir):
                shutil.rmtree(self.html_report_dir)
                os.makedirs(self.html_report_dir, exist_ok=True)
            
            # 检查Allure是否安装
            try:
                subprocess.run(['allure', '--version'], 
                             capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.error("Allure未安装或未配置环境变量")
                return False
            
            # 生成Allure报告
            cmd = ['allure', 'generate', self.allure_results_dir, 
                   '-o', self.html_report_dir, '--clean']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Allure报告生成成功: {self.html_report_dir}")
                return True
            else:
                self.logger.error(f"Allure报告生成失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"生成Allure报告异常: {e}")
            return False
    
    def open_allure_report(self) -> bool:
        """
        打开Allure报告
        
        Returns:
            是否打开成功
        """
        try:
            # 检查报告是否存在
            index_file = os.path.join(self.html_report_dir, "index.html")
            if not os.path.exists(index_file):
                self.logger.warning("Allure报告不存在，正在生成...")
                if not self.generate_allure_report():
                    return False
            
            # 使用allure open命令打开报告
            cmd = ['allure', 'open', self.html_report_dir]
            subprocess.Popen(cmd)
            
            self.logger.info("Allure报告已打开")
            return True
            
        except Exception as e:
            self.logger.error(f"打开Allure报告失败: {e}")
            return False
    
    def serve_allure_report(self, port: int = 8080) -> bool:
        """
        启动Allure报告服务
        
        Args:
            port: 服务端口
            
        Returns:
            是否启动成功
        """
        try:
            cmd = ['allure', 'serve', self.allure_results_dir, '-p', str(port)]
            subprocess.Popen(cmd)
            
            self.logger.info(f"Allure报告服务已启动，端口: {port}")
            return True
            
        except Exception as e:
            self.logger.error(f"启动Allure报告服务失败: {e}")
            return False
    
    def generate_pytest_html_report(self, output_path: str = None) -> str:
        """
        生成pytest-html报告的参数
        
        Args:
            output_path: 输出路径
            
        Returns:
            pytest命令参数
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.html_report_dir, f"pytest_report_{timestamp}.html")
        
        return f"--html={output_path} --self-contained-html"
    
    def get_latest_report_path(self) -> Optional[str]:
        """
        获取最新的报告路径
        
        Returns:
            最新报告的路径
        """
        try:
            # 查找最新的HTML报告
            html_files = []
            for file in os.listdir(self.html_report_dir):
                if file.endswith('.html'):
                    filepath = os.path.join(self.html_report_dir, file)
                    html_files.append((filepath, os.path.getmtime(filepath)))
            
            if html_files:
                # 按修改时间排序，返回最新的
                latest_file = max(html_files, key=lambda x: x[1])
                return latest_file[0]
            
            # 如果没有HTML文件，检查Allure报告
            allure_index = os.path.join(self.html_report_dir, "index.html")
            if os.path.exists(allure_index):
                return allure_index
            
            return None
            
        except Exception as e:
            self.logger.error(f"获取最新报告路径失败: {e}")
            return None
    
    def cleanup_old_reports(self, keep_days: int = 7):
        """
        清理旧报告
        
        Args:
            keep_days: 保留天数
        """
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (keep_days * 24 * 60 * 60)
            
            for root, dirs, files in os.walk(self.reports_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    if os.path.getmtime(filepath) < cutoff_time:
                        os.remove(filepath)
                        self.logger.debug(f"删除旧报告文件: {filepath}")
            
            self.logger.info(f"清理 {keep_days} 天前的旧报告完成")
            
        except Exception as e:
            self.logger.error(f"清理旧报告失败: {e}")
    
    def archive_reports(self, archive_name: str = None) -> bool:
        """
        打包归档报告
        
        Args:
            archive_name: 归档文件名
            
        Returns:
            是否归档成功
        """
        try:
            if archive_name is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                archive_name = f"test_reports_{timestamp}"
            
            archive_path = os.path.join(self.reports_dir, archive_name)
            
            # 创建ZIP归档
            shutil.make_archive(archive_path, 'zip', self.reports_dir)
            
            self.logger.info(f"报告归档成功: {archive_path}.zip")
            return True
            
        except Exception as e:
            self.logger.error(f"报告归档失败: {e}")
            return False


# 全局报告管理器实例
report_manager = ReportManager()