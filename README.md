# 🀄 四川麻将积分系统

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/sichuan-mahjong-scorer)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0-orange.svg)](https://github.com/yourusername/sichuan-mahjong-scorer/releases)

> 🎮 专业的四川麻将积分计算器，支持传统模式和血流成河模式，现代化GUI界面，自动计分，数据持久化。

## ✨ 功能特色

### 🎯 双模式支持
- **传统模式**：经典四川麻将计分规则
- **血流成河模式**：支持多次胡牌的连续游戏模式

### 🎨 现代化界面
- 美观的图形用户界面
- 实时积分榜显示
- 卡片式布局设计
- 直观的操作按钮

### 🧮 智能计分
- 自动计算各种胡牌类型分数
- 支持多种番型组合
- 实时分数预览
- 防错误输入验证

### 📊 数据管理
- 自动保存游戏数据
- 详细的历史记录
- 支持撤销操作
- 导出游戏结果

## 🚀 快速开始

### 💻 直接下载运行（推荐）

#### Windows用户
1. 下载 [四川麻将积分系统.exe](https://github.com/yifany-github/sichuan-mahjong-scorer/releases)
2. 双击运行即可，无需安装Python

#### macOS用户
1. 下载 [四川麻将积分系统.app](https://github.com/yifany-github/sichuan-mahjong-scorer/releases)
2. 双击运行，如遇安全警告请在系统偏好设置中允许

### 🐍 从源码运行

```bash
# 克隆项目
git clone https://github.com/yifany-github/sichuan-mahjong-scorer.git
cd sichuan-mahjong-scorer

# 安装依赖（可选）
pip install -r requirements.txt

# 运行程序
python majiang_macos_compatible.py
```

## 📖 使用说明

### 🎮 基本操作

1. **设置玩家**：点击"👥 设置玩家"自定义玩家姓名
2. **选择模式**：在右侧面板选择"传统模式"或"血流成河"
3. **记录分数**：点击"📝 记录分数"输入胡牌信息
4. **查看排名**：左侧实时显示积分排行榜

### 🀄 计分规则

#### 传统模式
- 基础分值：1分
- 按番数翻倍：最终分数 = 1 × 2^总番数
- 一次胡牌结束一局

#### 血流成河模式
- 支持多次胡牌，直到手动结束本局
- 查叫机制：未胡牌的玩家承担相应分数
- 自摸：每个胡家从每个查叫玩家收取分数
- 点炮：点炮玩家承担所有胡家的分数

### 🎯 胡牌类型及番数

| 胡牌类型 | 番数 | 适用模式 |
|---------|------|----------|
| 平胡 | 1番 | 传统 + 血流 |
| 碰碰胡 | 2番 | 传统 + 血流 |
| 清一色 | 4番 | 传统 + 血流 |
| 七对 | 4番 | 传统 + 血流 |
| 龙七对 | 8番 | 血流成河 |
| 清七对 | 8番 | 血流成河 |
| 清龙七对 | 16番 | 血流成河 |
| 天胡/地胡 | 8番 | 血流成河 |
| 杠上开花 | 2番 | 传统 + 血流 |
| 抢杠胡 | 2番 | 传统 + 血流 |
| 海底捞月 | 2番 | 传统 + 血流 |
| 自摸 | 1番 | 传统 + 血流 |

## 📱 系统要求

- **Windows**: Windows 10 或更高版本
- **macOS**: macOS 10.14 (Mojave) 或更高版本
- **Python**: 3.6+ （仅源码运行需要）

## 🛠️ 开发者指南

### 环境搭建

```bash
# 克隆项目
git clone https://github.com/yifany-github/sichuan-mahjong-scorer.git
cd sichuan-mahjong-scorer

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 打包可执行文件

#### 自动化打包（推荐）
```bash
# Windows
build_windows.bat

# macOS
python build_scripts.py
```

#### 手动打包
```bash
# Windows
pyinstaller --onefile --windowed --name="四川麻将积分系统" majiang_macos_compatible.py

# macOS
pyinstaller --onedir --windowed --name="四川麻将积分系统" majiang_macos_compatible.py
```

### 项目结构

```
sichuan-mahjong-scorer/
├── majiang_macos_compatible.py    # 主程序文件
├── requirements.txt               # 依赖包列表
├── build_scripts.py               # 自动打包脚本
├── build_windows.bat              # Windows一键打包
├── build_windows_simple.py        # Windows简化打包脚本
├── build_windows.spec             # Windows PyInstaller配置
├── build_macos.spec               # macOS PyInstaller配置
├── 打包说明.md                    # 详细打包说明
├── 快速开始.md                    # 快速开始指南
└── README.md                      # 项目说明文档
```

## 🎯 功能演示

### 主界面
![主界面](screenshots/main-interface.png)

### 记录分数
![记录分数](screenshots/score-input.png)

### 历史记录
![历史记录](screenshots/game-history.png)

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2024-05-26)
- ✨ 初始版本发布
- 🎮 支持传统模式和血流成河模式
- 🎨 现代化GUI界面
- 📊 实时积分榜和历史记录
- 💾 自动数据保存
- 📦 支持Windows和macOS打包

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢所有四川麻将爱好者的支持
- 感谢Python和tkinter社区
- 感谢PyInstaller项目

## 📞 联系方式

- 项目主页：[GitHub](https://github.com/yifany-github/sichuan-mahjong-scorer)
- 问题反馈：[Issues](https://github.com/yifany-github/sichuan-mahjong-scorer/issues)

---

<div align="center">

**🀄 享受四川麻将的乐趣，让计分变得简单！**

[⬆ 回到顶部](#-四川麻将积分系统)

</div> 