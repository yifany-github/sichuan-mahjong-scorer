#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四川麻将积分系统 - 自动化打包脚本
支持Windows和macOS平台
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("🔧 正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0"])
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败")
        return False

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)

def build_windows():
    """构建Windows可执行文件"""
    print("\n🏗️ 开始构建Windows版本...")
    
    # 使用简单的命令行参数
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 无控制台窗口
        "--name=四川麻将积分系统",        # 可执行文件名称
        "--distpath=dist/windows",      # 输出目录
        "--workpath=build/windows",     # 工作目录
        "majiang_macos_compatible.py"   # 主文件
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Windows版本构建成功！")
        print(f"📁 输出位置: dist/windows/四川麻将积分系统.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows版本构建失败: {e}")
        return False

def build_macos():
    """构建macOS应用程序"""
    print("\n🏗️ 开始构建macOS版本...")
    
    # 使用简单的命令行参数
    cmd = [
        "pyinstaller",
        "--onedir",                     # 打包成目录（macOS推荐）
        "--windowed",                   # 无控制台窗口
        "--name=四川麻将积分系统",        # 应用名称
        "--distpath=dist/macos",        # 输出目录
        "--workpath=build/macos",       # 工作目录
        "majiang_macos_compatible.py"   # 主文件
    ]
    
    try:
        subprocess.check_call(cmd)
        
        # 创建.app包
        app_cmd = [
            "pyinstaller",
            "--onedir",
            "--windowed",
            "--name=四川麻将积分系统",
            "--distpath=dist/macos",
            "--workpath=build/macos",
            "--osx-bundle-identifier=com.majiang.scorekeeper",
            "majiang_macos_compatible.py"
        ]
        
        subprocess.check_call(app_cmd)
        print("✅ macOS版本构建成功！")
        print(f"📁 输出位置: dist/macos/四川麻将积分系统/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS版本构建失败: {e}")
        return False

def create_dmg_macos():
    """创建macOS的DMG安装包（可选）"""
    print("\n📦 尝试创建DMG安装包...")
    
    # 检查是否有create-dmg工具
    try:
        subprocess.check_call(["which", "create-dmg"], stdout=subprocess.DEVNULL)
        
        dmg_cmd = [
            "create-dmg",
            "--volname", "四川麻将积分系统",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--app-drop-link", "425", "120",
            "dist/四川麻将积分系统.dmg",
            "dist/macos/"
        ]
        
        subprocess.check_call(dmg_cmd)
        print("✅ DMG安装包创建成功！")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ 无法创建DMG包（需要安装create-dmg工具）")
        print("💡 可以手动安装: brew install create-dmg")
        return False

def main():
    """主函数"""
    print("🀄 四川麻将积分系统 - 自动化打包工具")
    print("=" * 50)
    
    # 检查当前系统
    current_os = platform.system()
    print(f"🖥️ 当前系统: {current_os}")
    
    # 检查必要文件
    if not os.path.exists("majiang_macos_compatible.py"):
        print("❌ 找不到主程序文件: majiang_macos_compatible.py")
        return False
    
    # 检查并安装PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # 创建输出目录
    os.makedirs("dist", exist_ok=True)
    
    success = False
    
    if current_os == "Windows":
        success = build_windows()
    elif current_os == "Darwin":  # macOS
        success = build_macos()
        if success:
            create_dmg_macos()  # 尝试创建DMG（可选）
    else:
        print(f"⚠️ 不支持的操作系统: {current_os}")
        print("💡 支持的系统: Windows, macOS")
        return False
    
    if success:
        print("\n🎉 打包完成！")
        print("\n📋 使用说明:")
        if current_os == "Windows":
            print("• Windows用户: 运行 dist/windows/四川麻将积分系统.exe")
        elif current_os == "Darwin":
            print("• macOS用户: 打开 dist/macos/四川麻将积分系统/ 文件夹")
            print("• 或者双击运行其中的可执行文件")
        
        print("\n💡 提示:")
        print("• 首次运行可能需要几秒钟启动时间")
        print("• 如果遇到安全警告，请在系统设置中允许运行")
        print("• 游戏数据会自动保存在程序同目录下")
        
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1) 