@echo off
chcp 65001 >nul
echo 🀄 四川麻将积分系统 - Windows一键打包
echo ================================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.6+
    echo 💡 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

REM 检查主程序文件
if not exist "majiang_macos_compatible.py" (
    echo ❌ 错误：找不到主程序文件 majiang_macos_compatible.py
    echo 💡 请确保在正确的目录下运行此脚本
    pause
    exit /b 1
)

echo ✅ 主程序文件存在
echo.

REM 安装PyInstaller
echo 🔧 检查并安装PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装PyInstaller...
    python -m pip install pyinstaller>=5.0
    if errorlevel 1 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
    echo ✅ PyInstaller安装成功
) else (
    echo ✅ PyInstaller已安装
)

echo.

REM 清理旧文件
if exist "dist" (
    echo 🧹 清理旧的dist目录...
    rmdir /s /q "dist"
)
if exist "build" (
    echo 🧹 清理旧的build目录...
    rmdir /s /q "build"
)

echo.
echo 🏗️ 开始构建Windows版本...
echo 📝 这可能需要几分钟时间，请耐心等待...
echo.

REM 执行打包
pyinstaller --onefile --windowed --name="四川麻将积分系统" --clean majiang_macos_compatible.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败！
    echo 💡 请检查错误信息并重试
    pause
    exit /b 1
)

echo.
echo 🎉 打包成功！
echo.
echo 📁 输出文件：dist\四川麻将积分系统.exe
echo.

REM 检查文件是否存在
if exist "dist\四川麻将积分系统.exe" (
    echo ✅ 可执行文件已生成
    
    REM 显示文件大小
    for %%A in ("dist\四川麻将积分系统.exe") do (
        set /a size=%%~zA/1024/1024
        echo 📊 文件大小：!size! MB
    )
    
    echo.
    echo 📋 使用说明：
    echo • 双击运行 dist\四川麻将积分系统.exe
    echo • 首次运行可能需要几秒钟启动时间
    echo • 如果Windows Defender报警，请选择"仍要运行"
    echo • 游戏数据会自动保存在exe同目录下
    echo.
    
    REM 询问是否立即运行
    set /p choice="🚀 是否立即运行程序？(y/n): "
    if /i "%choice%"=="y" (
        echo 🎮 启动程序...
        start "" "dist\四川麻将积分系统.exe"
    )
    
) else (
    echo ❌ 错误：未找到生成的可执行文件
)

echo.
echo 👋 感谢使用四川麻将积分系统！
pause 