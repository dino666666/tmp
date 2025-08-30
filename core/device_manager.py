"""
设备管理模块
负责设备的发现、连接和状态检查
"""
import subprocess
import re
import time
from typing import List, Dict, Optional
from utils.logger_manager import get_logger


class DeviceManager:
    """设备管理器"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def get_android_devices(self) -> List[Dict[str, str]]:
        """
        获取所有连接的Android设备
        
        Returns:
            设备列表，每个设备包含device_id和status
        """
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # 跳过第一行标题
            
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        device_id = parts[0].strip()
                        status = parts[1].strip()
                        devices.append({
                            'device_id': device_id,
                            'status': status,
                            'platform': 'Android'
                        })
            
            self.logger.info(f"发现 {len(devices)} 个Android设备")
            return devices
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"获取Android设备失败: {e}")
            return []
        except FileNotFoundError:
            self.logger.error("ADB未找到，请确保Android SDK已安装并配置环境变量")
            return []
    
    def get_ios_devices(self) -> List[Dict[str, str]]:
        """
        获取所有连接的iOS设备
        
        Returns:
            设备列表
        """
        try:
            # 使用xcrun simctl list devices命令获取模拟器设备
            result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', '--json'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            import json
            data = json.loads(result.stdout)
            devices = []
            
            for runtime, device_list in data['devices'].items():
                for device in device_list:
                    if device['state'] == 'Booted':
                        devices.append({
                            'device_id': device['udid'],
                            'device_name': device['name'],
                            'status': device['state'],
                            'platform': 'iOS',
                            'runtime': runtime
                        })
            
            # 获取真机设备（需要libimobiledevice）
            try:
                result = subprocess.run(['idevice_id', '-l'], 
                                      capture_output=True, 
                                      text=True, 
                                      check=True)
                
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        devices.append({
                            'device_id': line.strip(),
                            'device_name': 'Real Device',
                            'status': 'connected',
                            'platform': 'iOS',
                            'runtime': 'Real Device'
                        })
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.warning("libimobiledevice未安装，无法检测iOS真机设备")
            
            self.logger.info(f"发现 {len(devices)} 个iOS设备")
            return devices
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"获取iOS设备失败: {e}")
            return []
        except FileNotFoundError:
            self.logger.error("Xcode Command Line Tools未找到")
            return []
    
    def get_device_info(self, device_id: str, platform: str = "android") -> Optional[Dict[str, str]]:
        """
        获取设备详细信息
        
        Args:
            device_id: 设备ID
            platform: 平台类型
            
        Returns:
            设备信息字典
        """
        if platform.lower() == "android":
            return self._get_android_device_info(device_id)
        elif platform.lower() == "ios":
            return self._get_ios_device_info(device_id)
        else:
            self.logger.error(f"不支持的平台: {platform}")
            return None
    
    def _get_android_device_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """获取Android设备信息"""
        try:
            # 获取设备基本信息
            props_cmd = ['adb', '-s', device_id, 'shell', 'getprop']
            result = subprocess.run(props_cmd, capture_output=True, text=True, check=True)
            
            info = {'device_id': device_id, 'platform': 'Android'}
            
            # 解析关键属性
            prop_patterns = {
                'model': r'\[ro\.product\.model\]: \[(.*?)\]',
                'brand': r'\[ro\.product\.brand\]: \[(.*?)\]',
                'version': r'\[ro\.build\.version\.release\]: \[(.*?)\]',
                'sdk_version': r'\[ro\.build\.version\.sdk\]: \[(.*?)\]',
                'manufacturer': r'\[ro\.product\.manufacturer\]: \[(.*?)\]'
            }
            
            for key, pattern in prop_patterns.items():
                match = re.search(pattern, result.stdout)
                if match:
                    info[key] = match.group(1)
            
            return info
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"获取Android设备信息失败: {e}")
            return None
    
    def _get_ios_device_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """获取iOS设备信息"""
        try:
            # 对于模拟器，使用xcrun simctl
            cmd = ['xcrun', 'simctl', 'list', 'devices', '--json']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            import json
            data = json.loads(result.stdout)
            
            for runtime, device_list in data['devices'].items():
                for device in device_list:
                    if device['udid'] == device_id:
                        return {
                            'device_id': device_id,
                            'platform': 'iOS',
                            'name': device['name'],
                            'state': device['state'],
                            'runtime': runtime
                        }
            
            # 对于真机，尝试使用ideviceinfo
            try:
                result = subprocess.run(['ideviceinfo', '-u', device_id], 
                                      capture_output=True, text=True, check=True)
                
                info = {'device_id': device_id, 'platform': 'iOS'}
                for line in result.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
                
                return info
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            return None
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.logger.error(f"获取iOS设备信息失败: {e}")
            return None
    
    def install_app(self, device_id: str, app_path: str, platform: str = "android") -> bool:
        """
        安装应用
        
        Args:
            device_id: 设备ID
            app_path: 应用路径
            platform: 平台类型
            
        Returns:
            安装是否成功
        """
        if platform.lower() == "android":
            return self._install_android_app(device_id, app_path)
        elif platform.lower() == "ios":
            return self._install_ios_app(device_id, app_path)
        else:
            self.logger.error(f"不支持的平台: {platform}")
            return False
    
    def _install_android_app(self, device_id: str, apk_path: str) -> bool:
        """安装Android应用"""
        try:
            cmd = ['adb', '-s', device_id, 'install', '-r', apk_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if 'Success' in result.stdout:
                self.logger.info(f"应用安装成功: {apk_path}")
                return True
            else:
                self.logger.error(f"应用安装失败: {result.stdout}")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"安装Android应用失败: {e}")
            return False
    
    def _install_ios_app(self, device_id: str, ipa_path: str) -> bool:
        """安装iOS应用"""
        try:
            # 对于模拟器
            cmd = ['xcrun', 'simctl', 'install', device_id, ipa_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            self.logger.info(f"iOS应用安装成功: {ipa_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"安装iOS应用失败: {e}")
            return False
    
    def uninstall_app(self, device_id: str, package_name: str, platform: str = "android") -> bool:
        """
        卸载应用
        
        Args:
            device_id: 设备ID
            package_name: 包名或Bundle ID
            platform: 平台类型
            
        Returns:
            卸载是否成功
        """
        if platform.lower() == "android":
            return self._uninstall_android_app(device_id, package_name)
        elif platform.lower() == "ios":
            return self._uninstall_ios_app(device_id, package_name)
        else:
            self.logger.error(f"不支持的平台: {platform}")
            return False
    
    def _uninstall_android_app(self, device_id: str, package_name: str) -> bool:
        """卸载Android应用"""
        try:
            cmd = ['adb', '-s', device_id, 'uninstall', package_name]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if 'Success' in result.stdout:
                self.logger.info(f"应用卸载成功: {package_name}")
                return True
            else:
                self.logger.error(f"应用卸载失败: {result.stdout}")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"卸载Android应用失败: {e}")
            return False
    
    def _uninstall_ios_app(self, device_id: str, bundle_id: str) -> bool:
        """卸载iOS应用"""
        try:
            cmd = ['xcrun', 'simctl', 'uninstall', device_id, bundle_id]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            self.logger.info(f"iOS应用卸载成功: {bundle_id}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"卸载iOS应用失败: {e}")
            return False


# 全局设备管理器实例
device_manager = DeviceManager()