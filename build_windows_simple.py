#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四川麻将积分系统 - Windows简化打包脚本
在Windows系统上运行此脚本来生成exe文件
"""

import os
import sys
import subprocess
import shutil

def main():
    print("🀄 四川麻将积分系统 - Windows打包工具")
    print("=" * 50)
    
    # 检查必要文件
    if not os.path.exists("majiang_macos_compatible.py"):
        print("❌ 找不到主程序文件: majiang_macos_compatible.py")
        return False
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
    except ImportError:
        print("🔧 正在安装PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0"])
            print("✅ PyInstaller安装成功")
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False
    
    # 清理旧文件
    if os.path.exists("dist"):
        print("🧹 清理旧的dist目录...")
        shutil.rmtree("dist")
    if os.path.exists("build"):
        print("🧹 清理旧的build目录...")
        shutil.rmtree("build")
    
    print("\n🏗️ 开始构建Windows版本...")
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 单文件
        "--windowed",                   # 无控制台
        "--name=四川麻将积分系统",        # 文件名
        "--clean",                      # 清理缓存
        "majiang_macos_compatible.py"   # 主文件
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Windows版本构建成功！")
        print(f"📁 输出位置: dist/四川麻将积分系统.exe")
        
        # 检查文件大小
        exe_path = "dist/四川麻将积分系统.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📊 文件大小: {size_mb:.1f} MB")
        
        print("\n🎉 打包完成！")
        print("\n📋 使用说明:")
        print("• 双击运行 dist/四川麻将积分系统.exe")
        print("• 首次运行可能需要几秒钟启动时间")
        print("• 如果Windows Defender报警，请选择'仍要运行'")
        print("• 游戏数据会自动保存在exe同目录下")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows版本构建失败: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        input("\n按回车键退出...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        input("\n按回车键退出...")
        sys.exit(1) 