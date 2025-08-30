#!/usr/bin/env python3
"""
测试运行脚本
提供各种测试运行选项
"""
import os
import sys
import argparse
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.report_manager import report_manager
from utils.logger_manager import get_logger


def run_tests(test_path=None, markers=None, workers=None, report_type="allure", 
              reruns=0, verbose=False, collect_only=False):
    """
    运行测试
    
    Args:
        test_path: 测试路径
        markers: pytest标记
        workers: 并行worker数量
        report_type: 报告类型 (allure, html, both)
        reruns: 失败重试次数
        verbose: 详细输出
        collect_only: 仅收集测试，不执行
    """
    logger = get_logger(__name__)
    
    # 构建pytest命令
    cmd = ["pytest"]
    
    # 测试路径
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # 详细输出
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-s")
    
    # 标记过滤
    if markers:
        cmd.extend(["-m", markers])
    
    # 并行执行
    if workers and workers > 1:
        cmd.extend(["-n", str(workers)])
    
    # 失败重试
    if reruns > 0:
        cmd.extend(["--reruns", str(reruns)])
    
    # 仅收集测试
    if collect_only:
        cmd.append("--collect-only")
        cmd.append("-q")
    
    # 报告配置
    if not collect_only:
        if report_type in ["allure", "both"]:
            # 清理旧的Allure结果
            report_manager.clean_allure_results()
            cmd.extend(["--alluredir", report_manager.allure_results_dir])
        
        if report_type in ["html", "both"]:
            html_args = report_manager.generate_pytest_html_report()
            cmd.extend(html_args.split())
    
    # 执行测试
    logger.info(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=False)
        
        # 生成报告
        if not collect_only and result.returncode in [0, 1]:  # 0=成功, 1=有失败
            if report_type in ["allure", "both"]:
                logger.info("生成Allure报告...")
                if report_manager.generate_allure_report():
                    logger.info(f"Allure报告已生成: {report_manager.html_report_dir}")
        
        return result.returncode
        
    except KeyboardInterrupt:
        logger.info("测试被用户中断")
        return 130
    except Exception as e:
        logger.error(f"执行测试失败: {e}")
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Appium自动化测试运行器")
    
    # 测试路径
    parser.add_argument("test_path", nargs="?", default=None,
                       help="测试文件或目录路径 (默认: tests/)")
    
    # 测试标记
    parser.add_argument("-m", "--markers", 
                       help="pytest标记过滤 (例如: smoke, regression)")
    
    # 并行执行
    parser.add_argument("-n", "--workers", type=int, default=1,
                       help="并行worker数量 (默认: 1)")
    
    # 报告类型
    parser.add_argument("-r", "--report", choices=["allure", "html", "both"],
                       default="allure", help="报告类型 (默认: allure)")
    
    # 失败重试
    parser.add_argument("--reruns", type=int, default=0,
                       help="失败重试次数 (默认: 0)")
    
    # 详细输出
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="详细输出")
    
    # 仅收集测试
    parser.add_argument("--collect-only", action="store_true",
                       help="仅收集测试，不执行")
    
    # 报告操作
    parser.add_argument("--open-report", action="store_true",
                       help="执行后打开测试报告")
    
    # 服务报告
    parser.add_argument("--serve-report", action="store_true",
                       help="启动Allure报告服务")
    
    # 清理报告
    parser.add_argument("--clean-reports", action="store_true",
                       help="清理旧报告")
    
    args = parser.parse_args()
    
    # 处理报告操作
    if args.clean_reports:
        print("🧹 清理旧报告...")
        report_manager.clean_allure_results()
        report_manager.cleanup_old_reports()
        print("✅ 报告清理完成")
        return 0
    
    if args.serve_report:
        print("🌐 启动Allure报告服务...")
        report_manager.serve_allure_report()
        return 0
    
    # 运行测试
    print("🚀 开始执行测试...")
    
    exit_code = run_tests(
        test_path=args.test_path,
        markers=args.markers,
        workers=args.workers,
        report_type=args.report,
        reruns=args.reruns,
        verbose=args.verbose,
        collect_only=args.collect_only
    )
    
    # 处理测试结果
    if args.collect_only:
        print("📋 测试收集完成")
    elif exit_code == 0:
        print("✅ 所有测试通过")
    elif exit_code == 1:
        print("⚠️  部分测试失败")
    else:
        print("❌ 测试执行出错")
    
    # 打开报告
    if args.open_report and not args.collect_only:
        if args.report in ["allure", "both"]:
            print("📊 打开Allure报告...")
            report_manager.open_allure_report()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())