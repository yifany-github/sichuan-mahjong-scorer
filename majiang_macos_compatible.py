import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from typing import Dict, List

class SichuanMahjongGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("四川麻将积分系统")
        self.root.geometry("1000x700")
        
        # 兼容性配色方案 - 使用更安全的颜色
        self.colors = {
            'primary': '#4A90E2',      # 更兼容的蓝色
            'secondary': '#9B59B6',    # 紫色
            'accent': '#F39C12',       # 橙色
            'success': '#27AE60',      # 绿色
            'danger': '#E74C3C',       # 红色
            'background': '#F8F9FA',   # 浅灰背景
            'surface': '#FFFFFF',      # 白色表面
            'text_primary': '#2C3E50', # 深色文字
            'text_secondary': '#7F8C8D', # 灰色文字
            'border': '#BDC3C7',       # 边框色
            'hover': '#ECF0F1'         # 悬停色
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # 设置窗口样式
        self.setup_window_style()

        # 基础数据
        self.players: List[str] = ["东家", "南家", "西家", "北家"]
        self.scores: Dict[str, int] = {p: 0 for p in self.players}
        self.game_history: List[Dict] = []
        self.current_round: int = 0
        self.data_file: str = "mahjong_scores.json"

        # 计分模式（传统｜血流成河）
        self.mode = tk.StringVar(value="传统")

        # 构建 UI
        self.create_widgets()
        self.load_data()
        self.update_display()

    def setup_window_style(self):
        """设置窗口样式"""
        # 设置窗口居中
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 设置最小窗口大小
        self.root.minsize(800, 600)

    # ---------- UI ----------
    def create_widgets(self):
        # ===== 顶部标题栏 =====
        self.create_header()
        
        # ===== 主体容器 =====
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # ===== 左侧积分面板 =====
        self.create_score_panel(main_container)
        
        # ===== 右侧控制面板 =====
        self.create_control_panel(main_container)

    def create_header(self):
        """创建简化的头部"""
        header_frame = tk.Frame(self.root, height=70, bg=self.colors['primary'])
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # 标题文字
        title_label = tk.Label(header_frame, 
                              text="🀄 四川麻将积分系统", 
                              font=('Arial', 20, 'bold'), 
                              fg='white', 
                              bg=self.colors['primary'])
        title_label.pack(expand=True)
        
        # 副标题
        subtitle_label = tk.Label(header_frame, 
                                 text="专业版 · 支持传统与血流成河模式", 
                                 font=('Arial', 10), 
                                 fg='#E8F4FD', 
                                 bg=self.colors['primary'])
        subtitle_label.pack()

    def create_score_panel(self, parent):
        """创建积分显示面板"""
        left_frame = tk.Frame(parent, bg=self.colors['background'])
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 积分卡片容器
        score_container = tk.Frame(left_frame, bg=self.colors['surface'], 
                                  relief='solid', bd=1)
        score_container.pack(fill='both', expand=True)
        
        # 标题区域
        title_frame = tk.Frame(score_container, bg=self.colors['surface'], height=50)
        title_frame.pack(fill='x', padx=20, pady=(20, 0))
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🏆 实时积分榜", 
                font=('Arial', 16, 'bold'),
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(side='left', pady=10)
        
        # 局数显示
        self.round_label = tk.Label(title_frame, text="第 0 局", 
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['surface'], 
                                   fg=self.colors['accent'])
        self.round_label.pack(side='right', pady=10)
        
        # 分隔线
        separator = tk.Frame(score_container, height=1, bg=self.colors['border'])
        separator.pack(fill='x', padx=20, pady=(0, 15))
        
        # 积分显示区域
        self.score_frame = tk.Frame(score_container, bg=self.colors['surface'])
        self.score_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    def create_control_panel(self, parent):
        """创建控制面板"""
        right_frame = tk.Frame(parent, bg=self.colors['background'])
        right_frame.pack(side='right', fill='both', expand=False)
        right_frame.configure(width=320)
        
        # 模式选择卡片
        self.create_mode_card(right_frame)
        
        # 操作按钮卡片
        self.create_action_card(right_frame)
        
        # 历史记录卡片
        self.create_history_card(right_frame)

    def create_mode_card(self, parent):
        """创建模式选择卡片"""
        mode_card = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        mode_card.pack(fill='x', pady=(0, 10))
        
        # 标题
        title_frame = tk.Frame(mode_card, bg=self.colors['surface'])
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="🎮 游戏模式", 
                font=('Arial', 14, 'bold'),
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # 模式选择按钮 - 使用传统的Radiobutton
        mode_frame = tk.Frame(mode_card, bg=self.colors['surface'])
        mode_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # 传统模式
        self.traditional_radio = tk.Radiobutton(mode_frame, 
                                               text="传统模式",
                                               variable=self.mode,
                                               value="传统",
                                               font=('Arial', 11),
                                               bg=self.colors['surface'],
                                               fg=self.colors['text_primary'],
                                               selectcolor=self.colors['primary'],
                                               activebackground=self.colors['hover'])
        self.traditional_radio.pack(anchor='w', pady=2)
        
        # 血流成河模式
        self.xueliu_radio = tk.Radiobutton(mode_frame, 
                                          text="血流成河",
                                          variable=self.mode,
                                          value="血流成河",
                                          font=('Arial', 11),
                                          bg=self.colors['surface'],
                                          fg=self.colors['text_primary'],
                                          selectcolor=self.colors['primary'],
                                          activebackground=self.colors['hover'])
        self.xueliu_radio.pack(anchor='w', pady=2)

    def create_action_card(self, parent):
        """创建操作按钮卡片"""
        action_card = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        action_card.pack(fill='x', pady=(0, 10))
        
        # 标题
        title_frame = tk.Frame(action_card, bg=self.colors['surface'])
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="⚡ 快速操作", 
                font=('Arial', 14, 'bold'),
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # 按钮容器
        button_container = tk.Frame(action_card, bg=self.colors['surface'])
        button_container.pack(fill='x', padx=15, pady=(0, 15))
        
        # 创建兼容性按钮
        buttons_config = [
            ("👥 设置玩家", self.colors['primary'], self.set_players),
            ("📝 记录分数", self.colors['success'], self.add_score),
            ("↩️ 撤销上局", self.colors['accent'], self.undo_last),
            ("🏁 结束本局", self.colors['secondary'], self.end_current_round),
            ("🔄 重置游戏", '#6C757D', self.reset_game),
            ("📊 导出结果", '#17A2B8', self.export_results)
        ]
        
        for i, (text, color, command) in enumerate(buttons_config):
            btn = tk.Button(button_container, text=text,
                          font=('Arial', 10, 'bold'),
                          bg=color, fg='white',
                          relief='raised', bd=2,
                          height=2,
                          command=command,
                          cursor='hand2')
            btn.pack(fill='x', pady=2)
            
            # 添加简单的悬停效果
            self.add_simple_hover_effect(btn, color)

    def add_simple_hover_effect(self, button, original_color):
        """添加简单的按钮悬停效果"""
        def on_enter(e):
            button.configure(relief='sunken')
        
        def on_leave(e):
            button.configure(relief='raised')
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def create_history_card(self, parent):
        """创建历史记录卡片"""
        history_card = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        history_card.pack(fill='both', expand=True)
        
        # 标题
        title_frame = tk.Frame(history_card, bg=self.colors['surface'])
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="📜 游戏历史", 
                font=('Arial', 14, 'bold'),
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # 历史记录容器
        history_container = tk.Frame(history_card, bg=self.colors['surface'])
        history_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # 创建带滚动条的文本框
        text_frame = tk.Frame(history_container, bg=self.colors['surface'])
        text_frame.pack(fill='both', expand=True)
        
        self.history_text = tk.Text(text_frame, 
                                   font=('Arial', 9), 
                                   bg='#F8F9FA', 
                                   fg=self.colors['text_primary'],
                                   relief='sunken', bd=1,
                                   state='disabled',
                                   wrap='word')
        
        # 传统滚动条
        scrollbar = tk.Scrollbar(text_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        self.history_text.pack(fill='both', expand=True)
        
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)

    # ---------- 数据与显示 ----------
    def update_display(self):
        # 清空
        for w in self.score_frame.winfo_children():
            w.destroy()

        # 排序显示
        sorted_players = sorted(self.scores.items(),
                                key=lambda x: x[1],
                                reverse=True)
        
        for idx, (player, score) in enumerate(sorted_players, 1):
            self.create_player_card(self.score_frame, idx, player, score)

        self.round_label.config(text=f"第 {self.current_round} 局")
        self.update_history_display()

    def create_player_card(self, parent, rank, player, score):
        """创建玩家积分卡片"""
        # 主卡片
        card = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        card.pack(fill='x', pady=5)
        
        content_frame = tk.Frame(card, bg=self.colors['surface'])
        content_frame.pack(fill='x', padx=15, pady=10)
        
        # 排名显示
        rank_colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#95A5A6']  # 金银铜和普通
        rank_color = rank_colors[min(rank-1, 3)]
        
        rank_label = tk.Label(content_frame, text=f"{rank}",
                             font=('Arial', 14, 'bold'),
                             bg=rank_color, fg='white',
                             width=3, height=1,
                             relief='raised', bd=2)
        rank_label.pack(side='left', padx=(0, 10))
        
        # 玩家信息
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        info_frame.pack(side='left', fill='x', expand=True)
        
        # 玩家名称
        name_label = tk.Label(info_frame, text=player,
                             font=('Arial', 14, 'bold'),
                             bg=self.colors['surface'], 
                             fg=self.colors['text_primary'])
        name_label.pack(anchor='w')
        
        # 积分变化趋势
        trend = "📈" if score > 0 else "📉" if score < 0 else "➖"
        trend_label = tk.Label(info_frame, text=f"{trend} 当前积分",
                              font=('Arial', 9),
                              bg=self.colors['surface'], 
                              fg=self.colors['text_secondary'])
        trend_label.pack(anchor='w')
        
        # 积分显示
        score_color = self.colors['success'] if score >= 0 else self.colors['danger']
        score_label = tk.Label(content_frame, text=f"{score:+d}",
                              font=('Arial', 16, 'bold'),
                              bg=self.colors['surface'], 
                              fg=score_color)
        score_label.pack(side='right', padx=(10, 0))

    def update_history_display(self):
        """更新历史记录显示"""
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        
        if not self.game_history:
            self.history_text.insert(tk.END, "暂无游戏记录\n开始您的第一局游戏吧！ 🎮")
        else:
            for i, rec in enumerate(self.game_history[-8:], 1):  # 只显示最近8条
                hand_info = ""
                if rec.get('hand_num', 1) > 1 or not rec.get('round_ended', True):
                    hand_info = f"第{rec.get('hand_num', 1)}手 "
                
                status = ""
                if not rec.get('round_ended', True):
                    status = " 🔄"
                else:
                    status = " ✅"
                
                # 格式化历史记录
                record_text = f"🎯 第{rec['round']}局{hand_info}\n"
                record_text += f"   {rec['description']} | 胜者: {rec['winner']}{status}\n"
                record_text += f"   {rec['timestamp']}\n"
                
                if i < len(self.game_history[-8:]):
                    record_text += "   " + "-" * 25 + "\n"
                
                self.history_text.insert(tk.END, record_text)
        
        self.history_text.config(state='disabled')

    # ---------- 按钮功能 ----------
    def set_players(self):
        dialog = PlayerSetupDialog(self.root, self.players)
        if dialog.result:
            old_scores = self.scores.copy()
            old_players = self.players.copy()
            self.players = dialog.result

            # 更新分数映射
            new_scores = {}
            for i, new_p in enumerate(self.players):
                new_scores[new_p] = old_scores.get(old_players[i], 0)
            self.scores = new_scores
            self.save_data()
            self.update_display()
            messagebox.showinfo("成功", "玩家姓名已更新！")

    def add_score(self):
        dialog = ScoreInputDialog(self.root, self.players, self.mode.get())
        if dialog.result:
            winners, desc, round_scores = dialog.result

            # 更新积分
            for player, sc in round_scores.items():
                self.scores[player] += sc

            # 记录历史
            if self.mode.get() == "血流成河":
                # 血流成河模式：同一局可以有多次胡牌
                if not self.game_history or self.game_history[-1].get('round_ended', False):
                    # 开始新的一局
                    self.current_round += 1
                    round_num = self.current_round
                    hand_num = 1
                else:
                    # 同一局的后续胡牌
                    round_num = self.current_round
                    last_hand = self.game_history[-1].get('hand_num', 1)
                    hand_num = last_hand + 1
                
                self.game_history.append({
                    'round': round_num,
                    'hand_num': hand_num,
                    'scores': round_scores.copy(),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'description': desc,
                    'winner': ','.join(winners),
                    'round_ended': False  # 血流成河局未结束
                })
                
                # 询问是否结束本局
                if messagebox.askyesno("继续游戏", f"第{round_num}局第{hand_num}手已记录！\n是否继续本局游戏？\n\n选择'是'继续本局，选择'否'结束本局"):
                    msg = f"第{round_num}局第{hand_num}手分数已记录！本局继续..."
                else:
                    # 标记本局结束
                    if self.game_history:
                        self.game_history[-1]['round_ended'] = True
                    msg = f"第{round_num}局已结束！共{hand_num}手"
            else:
                # 传统模式：一次胡牌结束一局
                self.current_round += 1
                self.game_history.append({
                    'round': self.current_round,
                    'hand_num': 1,
                    'scores': round_scores.copy(),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'description': desc,
                    'winner': ','.join(winners),
                    'round_ended': True
                })
                msg = f"第{self.current_round}局分数已记录！"

            self.save_data()
            self.update_display()
            messagebox.showinfo("成功", msg)

    def undo_last(self):
        if not self.game_history:
            messagebox.showwarning("警告", "没有可撤销的记录")
            return
        last = self.game_history[-1]
        
        hand_info = ""
        if last.get('hand_num', 1) > 1:
            hand_info = f"第{last.get('hand_num', 1)}手"
        
        msg = f"撤销第{last['round']}局{hand_info}?\n{last['description']}\n"
        for p, sc in last['scores'].items():
            msg += f"{p}: {sc:+d}\n"
        
        if messagebox.askyesno("确认撤销", msg):
            for p, sc in last['scores'].items():
                self.scores[p] -= sc
            
            # 检查是否需要调整局数
            removed_record = self.game_history.pop()
            
            # 如果撤销的是第一手，且没有其他记录，则减少局数
            if (removed_record.get('hand_num', 1) == 1 and 
                (not self.game_history or 
                 self.game_history[-1]['round'] != removed_record['round'])):
                self.current_round -= 1
            
            self.save_data()
            self.update_display()
            messagebox.showinfo("成功", "已撤销！")

    def end_current_round(self):
        """结束当前血流成河局"""
        if self.mode.get() != "血流成河":
            messagebox.showinfo("提示", "只有血流成河模式才需要手动结束本局")
            return
        
        if not self.game_history:
            messagebox.showinfo("提示", "当前没有进行中的游戏")
            return
        
        last_record = self.game_history[-1]
        if last_record.get('round_ended', True):
            messagebox.showinfo("提示", "当前没有进行中的局")
            return
        
        round_num = last_record['round']
        hand_count = sum(1 for rec in self.game_history if rec['round'] == round_num)
        
        if messagebox.askyesno("确认结束", f"确认结束第{round_num}局？\n本局共进行了{hand_count}手"):
            # 标记本局结束
            for rec in reversed(self.game_history):
                if rec['round'] == round_num:
                    rec['round_ended'] = True
                else:
                    break
            
            self.save_data()
            self.update_display()
            messagebox.showinfo("成功", f"第{round_num}局已结束！共{hand_count}手")

    def reset_game(self):
        if messagebox.askyesno("确认", "重置所有数据？"):
            self.scores = {p: 0 for p in self.players}
            self.game_history = []
            self.current_round = 0
            self.save_data()
            self.update_display()
            messagebox.showinfo("成功", "已重置！")

    def export_results(self):
        fname = f"mahjong_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write("四川麻将积分记录\n" + "=" * 30 + "\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总局数: {self.current_round}\n\n")
                f.write("最终排名:\n")
                for i, (p, sc) in enumerate(sorted(self.scores.items(), key=lambda x: x[1], reverse=True), 1):
                    f.write(f"{i}. {p}: {sc}\n")
                f.write("\n详细记录:\n")
                for rec in self.game_history:
                    hand_info = ""
                    if rec.get('hand_num', 1) > 1:
                        hand_info = f"第{rec.get('hand_num', 1)}手 "
                    
                    status = ""
                    if not rec.get('round_ended', True):
                        status = " [进行中]"
                    
                    f.write(f"\n第{rec['round']}局{hand_info}- {rec['timestamp']}{status}\n")
                    f.write(f"类型: {rec['description']}, 胡牌: {rec['winner']}\n")
                    for p, sc in rec['scores'].items():
                        f.write(f"  {p}: {sc:+d}\n")
            messagebox.showinfo("成功", f"已导出到 {fname}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    # ---------- 持久化 ----------
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.players = data.get('players', self.players)
                self.scores = data.get('scores', self.scores)
                self.game_history = data.get('game_history', [])
                self.current_round = data.get('current_round', 0)
            except Exception as e:
                messagebox.showerror("错误", f"加载数据失败: {e}")

    def save_data(self):
        try:
            data = {
                'players': self.players,
                'scores': self.scores,
                'game_history': self.game_history,
                'current_round': self.current_round,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败: {e}")

    def run(self):
        self.root.mainloop()


# ---------- 对话框 ----------
class PlayerSetupDialog:
    def __init__(self, parent, current_players):
        self.result: List[str] = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("设置玩家姓名")
        self.dialog.geometry("450x350")
        self.dialog.configure(bg='#F8F9FA')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.center_window()
        
        # 创建UI
        self.create_ui(current_players)
        
        self.entries[0].focus()
        self.dialog.wait_window()
    
    def center_window(self):
        """窗口居中"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self, current_players):
        """创建UI"""
        # 主容器
        main_container = tk.Frame(self.dialog, bg='#FFFFFF', relief='solid', bd=1)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = tk.Frame(main_container, bg='#FFFFFF', height=60)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="👥 设置玩家姓名",
                 font=('Arial', 16, 'bold'),
                 bg='#FFFFFF', 
                 fg='#2C3E50').pack(expand=True)

        # 输入区域
        input_frame = tk.Frame(main_container, bg='#FFFFFF')
        input_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.entries = []
        positions = ["东家", "南家", "西家", "北家"]
        position_icons = ["🀀", "🀁", "🀂", "🀃"]
        
        for i, (pos, icon) in enumerate(zip(positions, position_icons)):
            # 输入组容器
            input_group = tk.Frame(input_frame, bg='#FFFFFF')
            input_group.pack(fill='x', pady=8)
            
            # 标签
            label_frame = tk.Frame(input_group, bg='#FFFFFF')
            label_frame.pack(fill='x', pady=(0, 5))
            
            tk.Label(label_frame, text=f"{icon} {pos}",
                     font=('Arial', 12, 'bold'),
                     bg='#FFFFFF', 
                     fg='#2C3E50').pack(side='left')
            
            # 输入框
            ent = tk.Entry(input_group, font=('Arial', 12), 
                          bg='#F8F9FA', 
                          fg='#2C3E50',
                          relief='solid', bd=1)
            ent.pack(fill='x', ipady=5)
            ent.insert(0, current_players[i])
            self.entries.append(ent)

        # 按钮区域
        button_frame = tk.Frame(main_container, bg='#FFFFFF')
        button_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # 确定按钮
        ok_btn = tk.Button(button_frame, text="✅ 确定",
                          font=('Arial', 11, 'bold'),
                          bg='#27AE60', fg='white',
                          relief='raised', bd=2,
                          height=2, width=12,
                          command=self.ok)
        ok_btn.pack(side='left', padx=(0, 10))
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="❌ 取消",
                              font=('Arial', 11, 'bold'),
                              bg='#E74C3C', fg='white',
                              relief='raised', bd=2,
                              height=2, width=12,
                              command=self.cancel)
        cancel_btn.pack(side='right', padx=(10, 0))

    def ok(self):
        names = [e.get().strip() for e in self.entries]
        if all(names):
            self.result = names
            self.dialog.destroy()
        else:
            messagebox.showwarning("警告", "请填写所有玩家姓名！")

    def cancel(self):
        self.dialog.destroy()


class ScoreInputDialog:
    def __init__(self, parent, players: List[str], mode: str):
        self.players = players
        self.mode = mode  # "传统" or "血流成河"
        self.result = None
        self.calculated_result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("记录分数")
        self.dialog.geometry("600x700")
        self.dialog.configure(bg='#F8F9FA')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.center_window()

        self.create_score_input()
        self.dialog.wait_window()
    
    def center_window(self):
        """窗口居中"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')

    # ----- UI -----
    def create_score_input(self):
        # 主容器
        main_container = tk.Frame(self.dialog, bg='#FFFFFF', relief='solid', bd=1)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # 标题区域
        header_frame = tk.Frame(main_container, bg='#FFFFFF', height=60)
        header_frame.pack(fill='x', pady=(15, 0))
        header_frame.pack_propagate(False)
        
        mode_text = "血流成河" if self.mode == "血流成河" else "传统"
        tk.Label(header_frame, text=f"📝 记录本局分数 - {mode_text}模式",
                 font=('Arial', 16, 'bold'),
                 bg='#FFFFFF', 
                 fg='#2C3E50').pack(expand=True)

        # 创建滚动区域
        canvas = tk.Canvas(main_container, bg='#FFFFFF', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#FFFFFF')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

        # 主内容区域
        content_frame = tk.Frame(scrollable_frame, bg='#FFFFFF')
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)

        # 胡牌玩家
        if self.mode == "血流成河":
            self.create_section(content_frame, "🎯 胡牌玩家 (可多选)", self.create_winner_section)
        else:
            self.create_section(content_frame, "🎯 胡牌玩家", self.create_winner_section)
        
        # 胡牌类型
        self.create_section(content_frame, "🀄 胡牌类型", self.create_type_section)
        
        # 血流成河模式说明
        if self.mode == "血流成河":
            self.create_section(content_frame, "📋 血流成河规则说明", self.create_rules_section)
        
        # 点炮玩家
        if self.mode == "传统":
            self.create_section(content_frame, "💥 点炮玩家 (非自摸时选择)", self.create_pao_section)
        else:
            self.create_section(content_frame, "💥 点炮玩家 (可选)", self.create_pao_section)

        # 预览
        self.create_section(content_frame, "📊 分数预览", self.create_preview_section)

        # 按钮区域
        self.create_buttons(content_frame)

        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 设置自动计算
        self.setup_auto_calculate()

    def create_section(self, parent, title, content_creator):
        """创建区域"""
        # 主容器
        section_container = tk.Frame(parent, bg='#FFFFFF')
        section_container.pack(fill='x', pady=10)
        
        # 卡片容器
        card_frame = tk.Frame(section_container, bg='#FFFFFF', relief='solid', bd=1)
        card_frame.pack(fill='x')
        
        # 标题区域
        title_frame = tk.Frame(card_frame, bg='#ECF0F1', height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=title,
                              font=('Arial', 12, 'bold'),
                              bg='#ECF0F1', 
                              fg='#2C3E50')
        title_label.pack(side='left', padx=15, pady=10)
        
        # 内容区域
        content_frame = tk.Frame(card_frame, bg='#FFFFFF')
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        content_creator(content_frame)

    def create_winner_section(self, parent):
        """创建胡牌玩家选择区域"""
        if self.mode == "传统":
            self.winner_var = tk.StringVar()
            for i, p in enumerate(self.players):
                rb = tk.Radiobutton(parent, text=p,
                                   variable=self.winner_var,
                                   value=p,
                                   font=('Arial', 11),
                                   bg='#FFFFFF',
                                   fg='#2C3E50',
                                   selectcolor='#4A90E2',
                                   command=self.auto_calculate)
                rb.pack(anchor='w', pady=2)
        else:  # 血流
            self.winner_vars = {p: tk.BooleanVar() for p in self.players}
            for i, (p, var) in enumerate(self.winner_vars.items()):
                cb = tk.Checkbutton(parent, text=p,
                                   variable=var,
                                   font=('Arial', 11),
                                   bg='#FFFFFF',
                                   fg='#2C3E50',
                                   selectcolor='#4A90E2',
                                   command=self.auto_calculate)
                cb.pack(anchor='w', pady=2)

    def create_type_section(self, parent):
        """创建胡牌类型选择区域"""
        if self.mode == "传统":
            self.score_types = {
                '平胡': (1, tk.BooleanVar()),
                '碰碰胡': (2, tk.BooleanVar()),
                '清一色': (4, tk.BooleanVar()),
                '七对': (4, tk.BooleanVar()),
                '杠上开花': (2, tk.BooleanVar()),
                '抢杠胡': (2, tk.BooleanVar()),
                '海底捞月': (2, tk.BooleanVar()),
                '自摸': (1, tk.BooleanVar())
            }
        else:  # 血流成河模式
            self.score_types = {
                '平胡': (1, tk.BooleanVar()),
                '碰碰胡': (2, tk.BooleanVar()),
                '清一色': (4, tk.BooleanVar()),
                '七对': (4, tk.BooleanVar()),
                '龙七对': (8, tk.BooleanVar()),
                '清七对': (8, tk.BooleanVar()),
                '清龙七对': (16, tk.BooleanVar()),
                '杠上开花': (2, tk.BooleanVar()),
                '抢杠胡': (2, tk.BooleanVar()),
                '海底捞月': (2, tk.BooleanVar()),
                '天胡': (8, tk.BooleanVar()),
                '地胡': (8, tk.BooleanVar()),
                '自摸': (1, tk.BooleanVar())
            }
        
        # 创建两列布局
        left_col = tk.Frame(parent, bg='#FFFFFF')
        right_col = tk.Frame(parent, bg='#FFFFFF')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        right_col.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        items = list(self.score_types.items())
        mid_point = (len(items) + 1) // 2
        
        for i, (name, (fan, var)) in enumerate(items):
            parent_col = left_col if i < mid_point else right_col
            cb = tk.Checkbutton(parent_col, text=f"{name} ({fan}番)",
                               variable=var,
                               font=('Arial', 10),
                               bg='#FFFFFF',
                               fg='#2C3E50',
                               selectcolor='#F39C12',
                               command=self.auto_calculate)
            cb.pack(anchor='w', pady=1)

    def create_pao_section(self, parent):
        """创建点炮玩家选择区域"""
        self.pao_var = tk.StringVar(value="")
        
        # 无点炮选项
        rb = tk.Radiobutton(parent, text="无 (自摸)",
                           variable=self.pao_var,
                           value="",
                           font=('Arial', 11),
                           bg='#FFFFFF',
                           fg='#2C3E50',
                           selectcolor='#9B59B6',
                           command=self.auto_calculate)
        rb.pack(anchor='w', pady=2)
        
        # 玩家选项
        for p in self.players:
            rb = tk.Radiobutton(parent, text=p,
                               variable=self.pao_var,
                               value=p,
                               font=('Arial', 11),
                               bg='#FFFFFF',
                               fg='#2C3E50',
                               selectcolor='#9B59B6',
                               command=self.auto_calculate)
            rb.pack(anchor='w', pady=2)

    def create_rules_section(self, parent):
        """创建血流成河规则说明区域"""
        rules_text = tk.Text(parent, height=5, 
                            font=('Arial', 9), 
                            bg='#FFF9C4', 
                            fg='#2C3E50',
                            relief='solid', bd=1,
                            state='disabled',
                            wrap='word')
        rules_text.pack(fill='both', expand=True)
        
        rules_content = """🎮 血流成河规则说明：

• 每局可以有多次胡牌，胡牌后继续游戏直到手动结束本局
• 可多人同时胡牌，未胡牌的玩家称为"查叫"
• 自摸时：每个胡家从每个查叫玩家收取相应分数
• 点炮时：点炮玩家承担所有胡家的分数，其他查叫玩家无关
• 七对类型互斥：普通七对、龙七对、清七对、清龙七对只能选一种
• 组合类型已包含基础类型，无需重复选择"""
        
        rules_text.config(state='normal')
        rules_text.insert(tk.END, rules_content)
        rules_text.config(state='disabled')

    def create_preview_section(self, parent):
        """创建预览区域"""
        self.preview_text = tk.Text(parent, height=5, 
                                   font=('Arial', 10), 
                                   bg='#F8F9FA', 
                                   fg='#2C3E50',
                                   relief='solid', bd=1,
                                   state='disabled',
                                   wrap='word')
        self.preview_text.pack(fill='both', expand=True)

    def create_buttons(self, parent):
        """创建底部按钮"""
        # 按钮容器
        button_container = tk.Frame(parent, bg='#FFFFFF')
        button_container.pack(fill='x', pady=15)
        
        # 计算按钮
        calc_btn = tk.Button(button_container, text="🧮 计算分数",
                           font=('Arial', 12, 'bold'),
                           bg='#4A90E2', fg='white',
                           relief='raised', bd=2,
                           height=2, width=20,
                           command=self.calculate_score)
        calc_btn.pack(pady=(0, 10))
        
        # 确定取消按钮
        btn_frame = tk.Frame(button_container, bg='#FFFFFF')
        btn_frame.pack()
        
        # 确定按钮
        ok_btn = tk.Button(btn_frame, text="✅ 确定记录",
                          font=('Arial', 11, 'bold'),
                          bg='#27AE60', fg='white',
                          relief='raised', bd=2,
                          height=2, width=15,
                          command=self.ok_clicked)
        ok_btn.pack(side='left', padx=(0, 10))
        
        # 取消按钮
        cancel_btn = tk.Button(btn_frame, text="❌ 取消",
                              font=('Arial', 11, 'bold'),
                              bg='#E74C3C', fg='white',
                              relief='raised', bd=2,
                              height=2, width=15,
                              command=self.cancel_clicked)
        cancel_btn.pack(side='right', padx=(10, 0))

    def setup_auto_calculate(self):
        """设置自动计算"""
        for _, var in self.score_types.values():
            var.trace_add('write', lambda *args: self.auto_calculate())
        if self.mode == "传统":
            self.winner_var.trace_add('write', lambda *args: self.auto_calculate())
            self.pao_var.trace_add('write', lambda *args: self.auto_calculate())
        else:
            for var in self.winner_vars.values():
                var.trace_add('write', lambda *args: self.auto_calculate())

    def auto_calculate(self):
        try:
            self.calculate_score()
        except Exception:
            pass

    # ----- 计算逻辑 -----
    def calculate_score(self):
        if self.mode == "传统":
            self._calculate_traditional()
        else:
            self._calculate_xueliu()

    def _collect_fan_info(self):
        total_fan = 0
        desc = []
        is_zimo = False
        selected_types = []
        
        for name, (fan, var) in self.score_types.items():
            if var.get():
                selected_types.append(name)
                total_fan += fan
                desc.append(f"{name}({fan}番)")
                if name == "自摸":
                    is_zimo = True
        
        # 血流成河模式的规则验证
        if self.mode == "血流成河":
            # 检查互斥的胡牌类型
            seven_types = ['七对', '龙七对', '清七对', '清龙七对']
            selected_seven = [t for t in selected_types if t in seven_types]
            if len(selected_seven) > 1:
                raise ValueError(f"七对类型互斥，不能同时选择: {', '.join(selected_seven)}")
            
            # 天胡地胡互斥
            if '天胡' in selected_types and '地胡' in selected_types:
                raise ValueError("天胡和地胡不能同时选择")
            
            # 清龙七对已包含清一色和龙七对，不需要重复计算
            if '清龙七对' in selected_types:
                if '清一色' in selected_types or '龙七对' in selected_types or '七对' in selected_types:
                    raise ValueError("清龙七对已包含其他七对和清一色，请勿重复选择")
            
            # 清七对已包含清一色和七对
            if '清七对' in selected_types:
                if '清一色' in selected_types or '七对' in selected_types:
                    raise ValueError("清七对已包含清一色和七对，请勿重复选择")
            
            # 龙七对已包含七对
            if '龙七对' in selected_types and '七对' in selected_types:
                raise ValueError("龙七对已包含七对，请勿重复选择")
        
        return total_fan, desc, is_zimo

    def _calculate_traditional(self):
        winner = self.winner_var.get()
        if not winner:
            self._show_msg("请先选择胡牌玩家")
            return

        try:
            total_fan, desc, is_zimo = self._collect_fan_info()
        except ValueError as e:
            self._show_msg(str(e))
            return
            
        if total_fan == 0:
            self._show_msg("请选择至少一种胡牌类型")
            return

        base = 1
        final = base * (2 ** total_fan)
        round_scores = {p: 0 for p in self.players}
        pao = self.pao_var.get()

        if is_zimo or not pao:
            for p in self.players:
                if p == winner:
                    round_scores[p] = final * 3
                else:
                    round_scores[p] = -final
        else:
            if pao == winner:
                self._show_msg("点炮玩家不能是胡牌玩家！")
                return
            for p in self.players:
                if p == winner:
                    round_scores[p] = final
                elif p == pao:
                    round_scores[p] = -final
                else:
                    round_scores[p] = 0

        preview = f"胡牌: {winner}\n类型: {' + '.join(desc)}\n"
        preview += f"单家分值: {final}\n分配:\n"
        for p, sc in round_scores.items():
            preview += f"  {p}: {sc:+d}\n"
        
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        self.preview_text.config(state='disabled')

        self.calculated_result = ([winner], ' + '.join(desc), round_scores)

    def _calculate_xueliu(self):
        winners = [p for p, var in self.winner_vars.items() if var.get()]
        if not winners:
            self._show_msg("请至少勾选一名胡家")
            return

        try:
            total_fan, desc, is_zimo = self._collect_fan_info()
        except ValueError as e:
            self._show_msg(str(e))
            return
            
        if total_fan == 0:
            self._show_msg("请选择至少一种胡牌类型")
            return

        # 血流成河计分规则：
        # 1. 基础分为1分，按番数翻倍
        # 2. 如果有点炮，点炮玩家承担所有胡家的分数
        # 3. 如果没有点炮（自摸），每个胡家从每个未胡家收取相应分数
        base = 1
        final = base * (2 ** total_fan)
        round_scores = {p: 0 for p in self.players}
        pao = self.pao_var.get()
        
        # 计算未胡家（查叫的玩家）
        losers = [p for p in self.players if p not in winners]
        
        if len(winners) == len(self.players):
            # 所有人都胡牌，这种情况下没有输家，分数为0
            self._show_msg("血流成河模式下不能所有人都胡牌！")
            return
        
        # 检查点炮玩家是否合法
        if pao and pao in winners:
            self._show_msg("点炮玩家不能是胡牌玩家！")
            return
        
        if is_zimo or not pao:
            # 自摸情况：每个胡家从每个未胡家收取分数
            for winner in winners:
                # 胡家得分 = 单家分值 × 未胡家人数
                round_scores[winner] = final * len(losers)
            
            for loser in losers:
                # 未胡家失分 = 单家分值 × 胡家人数
                round_scores[loser] = -final * len(winners)
            
            pao_info = "自摸"
        else:
            # 点炮情况：点炮玩家承担所有胡家的分数
            total_pao_cost = final * len(winners)
            
            for winner in winners:
                # 每个胡家得到单家分值
                round_scores[winner] = final
            
            # 点炮玩家承担所有费用
            round_scores[pao] = -total_pao_cost
            
            # 其他未胡家不用付分
            for loser in losers:
                if loser != pao:
                    round_scores[loser] = 0
            
            pao_info = f"点炮: {pao}"

        # 验证分数平衡（总和应该为0）
        total_check = sum(round_scores.values())
        if total_check != 0:
            self._show_msg(f"分数计算错误，总和不为0: {total_check}")
            return

        preview = f"胡家: {', '.join(winners)}\n类型: {' + '.join(desc)}\n"
        preview += f"单家分值: {final}\n"
        preview += f"胡家人数: {len(winners)}，未胡家人数: {len(losers)}\n"
        preview += f"结算方式: {pao_info}\n"
        preview += "分配:\n"
        for p, sc in round_scores.items():
            if p in winners:
                status = "胡家"
            elif pao and p == pao:
                status = "点炮"
            elif sc == 0:
                status = "无关"
            else:
                status = "查叫"
            preview += f"  {p} ({status}): {sc:+d}\n"
        
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        self.preview_text.config(state='disabled')

        self.calculated_result = (winners, ' + '.join(desc), round_scores)

    # ----- 其他 -----
    def _show_msg(self, txt: str):
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, txt)
        self.preview_text.config(state='disabled')
        self.calculated_result = None

    def ok_clicked(self):
        if self.calculated_result:
            self.result = self.calculated_result
            self.dialog.destroy()
        else:
            messagebox.showwarning("警告", "请先正确计算分数！")

    def cancel_clicked(self):
        self.dialog.destroy()


# ---------- main ----------
if __name__ == "__main__":
    app = SichuanMahjongGUI()
    app.run() 