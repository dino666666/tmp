#!/usr/bin/env python3
"""
框架初始化脚本
用于初始化框架环境和创建示例数据
"""
import os
import sys
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_manager import data_manager
from utils.report_manager import report_manager
from utils.logger_manager import get_logger


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ 是必需的")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True


def check_dependencies():
    """检查依赖包"""
    try:
        import appium
        import selenium
        import pytest
        import allure
        print("✅ 核心依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False


def check_appium_server():
    """检查Appium服务"""
    try:
        result = subprocess.run(['appium', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Appium版本: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Appium未安装或未配置环境变量")
        print("请安装Appium: npm install -g appium")
        return False


def check_adb():
    """检查ADB"""
    try:
        result = subprocess.run(['adb', 'version'], 
                              capture_output=True, text=True, check=True)
        print("✅ ADB已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ADB未安装或未配置环境变量")
        print("请安装Android SDK并配置环境变量")
        return False


def check_allure():
    """检查Allure"""
    try:
        result = subprocess.run(['allure', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Allure版本: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Allure未安装（可选）")
        print("如需Allure报告，请安装: https://docs.qameta.io/allure/")
        return False


def create_sample_data():
    """创建示例数据"""
    try:
        data_manager.create_sample_data_files()
        print("✅ 示例数据文件已创建")
        return True
    except Exception as e:
        print(f"❌ 创建示例数据失败: {e}")
        return False


def setup_directories():
    """设置目录结构"""
    try:
        dirs = ['logs', 'reports', 'reports/screenshots', 'reports/allure-results', 'data']
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
        print("✅ 目录结构已创建")
        return True
    except Exception as e:
        print(f"❌ 创建目录失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 Appium自动化测试框架初始化\n")
    
    checks = [
        ("Python版本检查", check_python_version),
        ("依赖包检查", check_dependencies),
        ("Appium服务检查", check_appium_server),
        ("ADB检查", check_adb),
        ("Allure检查", check_allure),
        ("目录结构设置", setup_directories),
        ("示例数据创建", create_sample_data),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}...")
        result = check_func()
        results.append((name, result))
    
    print("\n" + "="*50)
    print("📊 初始化结果汇总:")
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\n通过: {success_count}/{total_count}")
    
    if success_count >= total_count - 1:  # 允许Allure检查失败
        print("\n🎉 框架初始化完成!")
        print("\n📖 后续步骤:")
        print("1. 启动Appium服务: appium")
        print("2. 连接Android设备并启用USB调试")
        print("3. 修改config/config.yaml中的应用配置")
        print("4. 运行测试: pytest tests/")
    else:
        print("\n⚠️  请解决上述问题后重新运行初始化脚本")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())