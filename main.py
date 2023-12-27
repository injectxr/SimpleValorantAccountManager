import os
from typing import Optional, Tuple, Union
import urllib.error
import urllib.parse
import numpy as np
import requests
import tempfile
import csv
from PIL import Image
import customtkinter
import pyperclip
import webbrowser
import pandas as pd
import subprocess
import ctypes
import pygetwindow as gw
import pyautogui
import win32api
import win32con
import platform
from datetime import datetime
import psutil
import sys
import threading
from io import BytesIO
import shutil
import pickle
from os import path, getcwd, remove, mkdir
from time import time
import time as tm

import cfscrape
import requests

TRACKERGG = "https://tracker.gg/valorant/profile/riot/"
valorantapiurl = "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/"
FONT_TYPE = "Meiryo UI"
filename = 'valorant-rank.csv'
config = 'Config.json'
nowversion = "v 2.0.0 "
twitterid = "https://twitter.com/i/user/825939612690378752"
discord = "https://discord.gg/bqy2hdbhC5"
git = "https://github.com/injectxr/SimpleValorantAccountManager"
dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
debug = True
global g_edit_num
global username
username = "配布用"
width = 500
hight = 320
states = "account_state"
folder_path = 'system_png/pickle'

def fileopen():
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            # 新しいファイルを作成してヘッダーを書き込む
            header = [
                "now rank", "0", "0", "6",
                "3", "C:/Riot Games/Riot Client/RiotClientServices.exe"
            ]
            writer = csv.writer(f)
            writer.writerow(header)

    with open(filename, encoding='utf-8', newline='') as f:
        data = csv.reader(f)
        result = [line for line in data]
    
    return result
class App(customtkinter.CTk):
    def __init__(self, master=None):
        super().__init__(master)
        # メンバー変数の設定
        self.minmin = (FONT_TYPE, 7,"bold")
        self.min = (FONT_TYPE, 10,"bold")
        self.fonts = (FONT_TYPE, 15,"bold")
        self.label = (FONT_TYPE, 24,"bold")
        self.labeltate = (FONT_TYPE, 800,"bold")
        self.resizable(False, False)
        # フォームサイズ設定
        global username 
        self.geometry(f"{width}x{hight}")
        self.title(f"SimpleValorantAccountManager")
        lists = fileopen()
        # self.wm_overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes('-topmost', False)
        self.geometry('+710+360')
        self.start_x = None
        self.start_y = None
        self.cnt = 0
        header_check()
        print("init")
        self.setup()
    def setup(self):
        #self.init()
        self.background_frame()
        self.main_widget()
        self.init_widget()
        self.side_widget()
        self.window_drag()
        self.Refresh_account()
        self.stateui()
        
        self.Register_window = None
        self.Edit_window     = None
        self.Setting_window  = None
        self.AccountEdit_Window  = None
        self.copy_Window  = None
    def init(self):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # サブフォルダを削除する場合
            except Exception as e:
                print(f"削除中にエラーが発生しました: {e}")    
    def background_frame(self):
        print("backgroundframe")
        fg = "#242424"
        h_color = "#0F0F0F"
        line_color ="#DCD3C9"
        sideframe_color = "#2b2b2b"
        text_color = "#f2efec"
        self.background_frame= customtkinter.CTkFrame(self, width=500, height=320,corner_radius=0,fg_color=fg,border_width=1,border_color=line_color)
        self.background_frame.place(x=0,y=0)
    def main_widget(self):
        print("main_widget")
        fg = "#242424"
        h_color = "#0F0F0F"
        line_color ="#DCD3C9"
        sideframe_color = "#2b2b2b"
        text_color = "#f2efec"
        fgsub = "#242424"
        
        self.main_frame = customtkinter.CTkFrame(self, width=327, height=320,corner_radius=0,fg_color=fg,border_width=1,border_color=line_color)
        self.main_frame.place(x=173,y=0)
        
        self.sub_frame = customtkinter.CTkFrame(self, width=327, height=320,corner_radius=0,fg_color=fgsub,border_width=1,border_color=line_color) 
        
        self.button8 = customtkinter.CTkButton(master=self.main_frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.sortbylist_up,image=customtkinter.CTkImage(Image.open("system_png//sort-up.png"),size=(16,16)),hover_color=h_color )
        self.button8.place(x=25, y=10)
        self.button8 = customtkinter.CTkButton(master=self.main_frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.sortbylist_down,image=customtkinter.CTkImage(Image.open("system_png//sort-down.png"),size=(16,16)),hover_color=h_color )
        self.button8.place(x=5, y=10)              
    def bind_drag_events(self, widget):
        widget.bind("<ButtonPress-1>", self.start_drag)
        widget.bind("<ButtonRelease-1>", self.stop_drag)
        widget.bind("<B1-Motion>", self.on_drag)
    def window_drag(self):
        widgets = [self.label2, self.sidebar_frame2, self.main_frame, self.sub_frame, self.background_frame]

        for widget in widgets:
            self.bind_drag_events(widget)               
    def start_drag(self, event):
        self.start_x = event.x_root - self.winfo_x()
        self.start_y = event.y_root - self.winfo_y()
    def stop_drag(self, event):
        self.start_x = None
        self.start_y = None
    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            x = event.x_root - self.start_x
            y = event.y_root - self.start_y
            self.geometry(f"{width}x{hight}+{x}+{y}")    
    def init_widget(self):
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.main_frame, width=290,height=265,
                                                                        command=self.label_button_frame_event1,
                                                                        command2=self.label_button_frame_event2,
                                                                        corner_radius=0)
        self.scrollable_label_button_frame.place(x=10,y=37)              
    def side_widget(self):
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        fg = "#242424"
        h_color = "#0F0F0F"
        line_color ="#DCD3C9"
        sideframe_color = "#2b2b2b"
        text_color = "#f2efec"
        
        # create sidebar frame with widgets
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=172, height=318,corner_radius=0,fg_color=sideframe_color,)
        self.sidebar_frame2.grid(row=10, column=0, rowspan=10, sticky="nsew",)
        self.sidebar_frame2.place(x=2,y=1)
        self.active_state_frame = customtkinter.CTkFrame(self, width=2, height=34,corner_radius=0,fg_color="#ffffff",)
        
        
        # current_dir = os.path.dirname(os.path.abspath(__file__))  
        self.label2 = customtkinter.CTkLabel(master=self.sidebar_frame2,text="", image=customtkinter.CTkImage(Image.open("system_png//valorantlogo.png"),size=(170, 170)))
        self.label2.place(x=1, y=1)      
        
        self.button0 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//User.png")), corner_radius=0,text="Account", anchor= "w", border_spacing= 5, command=self.button_account,font=self.fonts,width=170,height=20 ,fg_color="#2b2b2b",hover_color="#515151",text_color=text_color,)
        self.button0.place(x=0, y=162)
        self.button1 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//settings.png")), corner_radius=0,text="Setting", anchor= "w", border_spacing= 5, command=self.button_setting,font=self.fonts,width=170,height=20 ,fg_color="#2b2b2b",hover_color="#515151",text_color=text_color)
        self.button1.place(x=0, y=198)
        self.button2 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//refresh.png")), corner_radius=0,text="Update Rank", anchor= "w", border_spacing= 5, command=self.button_update,font=self.fonts,width=170,height=20,fg_color="#2b2b2b",hover_color="#515151",text_color=text_color)
        self.button2.place(x=0, y=233)
        self.button3 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//add.png")), corner_radius=0,text="Add Account", anchor= "w", border_spacing= 5, command=self.button_register,font=self.fonts,width=170,height=20,fg_color="#2b2b2b",hover_color="#515151",text_color=text_color)
        self.button3.place(x=0, y=269)
    def stateui(self):    
        state = self.get_state()
        fg = "#242424"
        h_color = "#0F0F0F"
        line_color ="#DCD3C9"
        sideframe_color = "#2b2b2b"
        text_color = "#f2efec"
        
        print("stateui :",state)
        self.delete_widgets_on_mainframe()
        
        if "account_state" != state:
            self.sub_frame.place(x=173,y=0)
            self.button9    = customtkinter.CTkButton(master=self.sub_frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.button_account,image=customtkinter.CTkImage(Image.open("system_png//close.png"),size=(19,19)),hover_color=h_color )
            self.button9.place(x=290, y=7)
        else:
            self.active_state_frame.place(x=-1000,y=-1000)
            self.sub_frame.place(x=-1000,y=1000)
        if   "account_state"    == state:
            self.active_state_frame.place(x=1,y=163)
        elif "update_state"     == state:
            lists = fileopen()
            self.active_state_frame.place(x=1,y=224)
            self.progressbar = customtkinter.CTkProgressBar(master=self.sub_frame)
            self.progressbar.place(x=60, y=150)
            self.progressbar.set(0)
            update_thread = threading.Thread(target=App.Update_Rank, args=(self,lists))
            update_thread.start() 
        elif "setting_state"    == state:
            self.active_state_frame.place(x=1,y=199)
            self.setting_ui(app_instance=self.sub_frame) 
        elif "addaccount_state" == state:
            self.active_state_frame.place(x=1,y=270)
            self.add_account_ui(app_instance=self.sub_frame)     
        elif "editaccount_state"== state:
            self.active_state_frame.place(x=1,y=163)
            self.edit_account_ui(app_instance=self.sub_frame)
        elif "shop_state" == state:
            self.active_state_frame.place(x=1,y=163)
            self.shop_ui(app_instance=self.sub_frame,app=App)
    def button_account(self):
        self.update_state("account_state") 
    def update_state(self, new_state):
        global states
        if states != new_state:
            states = new_state
            self.stateui()
    def button_setting(self):
        self.update_state("setting_state")
    def button_register(self):
        self.update_state("addaccount_state")
    def button_update(self):
        self.withdraw()
        Judgment = button_yesno("ランクを更新しますか？")
        if Judgment == "yes":
            # バックグラウンドスレッドで Update_Rank 関数を実行
            self.update_state("update_state")
            self.deiconify()
        else:
            self.deiconify() 
    def Update_Rank(self, lists):
        self.progressbar.set(0)
        # タスクの合計数を取得
        total_tasks = len(lists) - 1
        for i in range(total_tasks):
            self.after(0, up_rank(lists, i))
            # 進捗を計算してセットする
            progress = (i + 1) / total_tasks
            self.progressbar.set(progress)
            self.update_idletasks()  # イベントを処理してUIを更新する
            
        Savelist(lists)
        self.Refresh_account()
    def sortbylist_down(self):
        lists = fileopen()
        new = sorted(lists,key=valorantrank_sort_down)
        Savelist(new)    
        app.Refresh_account()  
    def sortbylist_up(self):
        lists = fileopen()
        new = sorted(lists,key=valorantrank_sort_up)
        Savelist(new)
        app.Refresh_account()  
    def get_state(self):
        global states
        return states
    def button_exit(self):
        self.destroy()    
    def debuglist(self):
        lists = fileopen()
        print(len(lists))
        print(lists)
    def label_button_frame_event1(self,i):
        self.withdraw()
        lists = fileopen()
        Judgment  = button_clicked_yesno(i,"を 起動しますか？")
        if Judgment == "yes":
            lists = fileopen()
            launch_riot_client(lists[i+1][3],lists[i+1][4])
            self.deiconify()
        else:
            self.deiconify()   
    def label_button_frame_event2(self,i):
        global g_edit_num
        g_edit_num = i
        self.update_state("shop_state") 
    def Refresh_account(self):
        lists = fileopen()
        num = lists[0][3]
        children = self.scrollable_label_button_frame.winfo_children()[:]
        for widget in children:
            try:
                #print(widget)
                widget.destroy()
            except customtkinter.TclError as e:
                print(f"Widget {widget} already destroyed: {e}")
        
        for i in range(len(lists) - 1):  # add items with image
            self.scrollable_label_button_frame.add_item(num,i,lists, lists[i + 1][1] + "#" + lists[i + 1][2],
                                                        image=customtkinter.CTkImage(
                                                            Image.open(Rankimagepath(lists[i + 1][0])))) 
        self.update_state("account_state")         
    def delete_widgets_on_mainframe(self):
        children = self.sub_frame.winfo_children()[:]  # Copy the list to avoid modification while iterating
        
        for widget in children:
            try:
                #print(widget)
                widget.destroy()
            except customtkinter.TclError as e:
                print(f"Widget {widget} already destroyed: {e}")  
    class setting_ui                (customtkinter.CTkCanvas):
        def __init__(self, app_instance,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance  # Appクラスのインスタンスを保持
            self.font = (FONT_TYPE, 9,"bold")
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.label = (FONT_TYPE, 32,"bold")
            self.small = (FONT_TYPE, 10,"bold")
            self.comment = (FONT_TYPE, 13)
            self.setup()
            
        def setup(self):
            lists = fileopen()
            fg = "#242424"
            h_color = "#0F0F0F"
            frame_bg = "#2b2b2b"
            default_value = lists[0][5]
            default_s = lists[0][4]
            default_num = lists[0][3]
            default_check = lists[0][2]
            default_check2 = lists[0][1]
            
            self.label0 = customtkinter.CTkLabel(master=self.app_instance, text="Setting", font=self.label)
            self.label0.place(x=18, y=15)

            self.label1 = customtkinter.CTkLabel(master=self.app_instance, text="・RiotClientの場所", font=self.fonts)
            self.label1.place(x=12, y=60)
            
            self.textbox1 = customtkinter.CTkEntry(master=self.app_instance, width=280,
                                                font=self.fonts,placeholder_text = "正しいRiotClientの場所を入れてください")
            self.textbox1.place(x=25, y=85)
            
            self.label1 = customtkinter.CTkLabel(master=self.app_instance, text=f"・ログイン処理の 待機時間", font=self.fonts)
            self.label1.place(x=12, y=115)
            
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"・アカウントの表示数[1~9]", font=self.fonts)
            self.label2.place(x=12, y=167)

            self.textbox2 = customtkinter.CTkEntry(master=self.app_instance, width=150,
                                                font=self.fonts,placeholder_text = "待機時間を入力してください")
            self.textbox2.place(x=25, y=140)
            
            self.textbox3 = customtkinter.CTkEntry(master=self.app_instance, width=150,
                                                font=self.fonts,placeholder_text = "表示数を入力してください[1~9]")
            self.textbox3.place(x=25, y=190)
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"  行", font=self.fonts,compound="right")
            self.label2.place(x=174.5, y=192)
            
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"  秒", font=self.fonts,compound="right")
            self.label2.place(x=174.5, y=140)
            
            self.button1 = customtkinter.CTkButton(master=self.app_instance, text="RESET", command=self.button_Reset,
                                                font=self.fonts,fg_color="#e0e0e0",hover_color="#bfbfbf",text_color="#0F0F0F")
            self.button1.place(x=18, y=260)
            self.button2 = customtkinter.CTkButton(master=self.app_instance, text="SAVE", command=self.button_Save,
                                                font=self.fonts,fg_color="#e0e0e0",hover_color="#bfbfbf",text_color="#0F0F0F")
            self.button2.place(x=170, y=260)
            self.button6 = customtkinter.CTkButton(master=self.app_instance,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.open_twitter_profile,image=customtkinter.CTkImage(Image.open("system_png//twitter.png"),size=(15,15)),hover_color=h_color )
            self.button6.place(x=105, y=293)
            self.button7 = customtkinter.CTkButton(master=self.app_instance,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.open_discord_profile,image=customtkinter.CTkImage(Image.open("system_png//discord.png"),size=(15,15)),hover_color=h_color )
            self.button7.place(x=130, y=293)
            self.button7 = customtkinter.CTkButton(master=self.app_instance,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.open_git_profile,image=customtkinter.CTkImage(Image.open("system_png//github.png"),size=(15,15)),hover_color=h_color )
            self.button7.place(x=155, y=293) 
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"{nowversion}", font=self.font)
            self.label2.place(x=70, y=290) 
            
            # CheckBox
            self.check_var = customtkinter.StringVar(value=default_check)
            checkbox = customtkinter.CTkCheckBox(master=self.app_instance, text="VALORANT自動起動", command=self.checkbox_event, variable=self.check_var, onvalue="1",offvalue="0",font=self.small)
            checkbox.place(x=25,y=230)
            self.check_var2 = customtkinter.StringVar(value=default_check2)
            checkbox2 = customtkinter.CTkCheckBox(master=self.app_instance, text="起動後自動アプリ終了", command=self.checkbox_event, variable=self.check_var2, onvalue="1",offvalue="0",font=self.small)
            checkbox2.place(x=176,y=230)
            
            self.textbox1.insert(index=1,string=f"{default_value}")
            self.textbox2.insert(index=1,string=f"{default_s}")
            self.textbox3.insert(index=1,string=f"{default_num}")
            
        def button_Save(self):
            error_messages = {
                "path_error": "RiotClientServices.exe以外のpathが入力されています",
                "int_error": "数値を入力してください"
            }

            # テキストボックスからの値を取得
            textbox1_value = str(self.textbox1.get())
            textbox2_value = str(self.textbox2.get())
            textbox3_value = str(self.textbox3.get())

            # ファイルオープンとリストの初期化
            lists = fileopen()

            # textbox1の値をチェックしてリストを更新
            if "RiotClientServices.exe" in textbox1_value:
                lists[0][5] = textbox1_value
            else:
                button_error("path_error", error_messages["path_error"])
                return

            # textbox2の値をチェックしてリストを更新
            if is_int(textbox2_value):
                lists[0][4] = textbox2_value if textbox2_value != "" else "3"
            else:
                button_error("int_error", error_messages["int_error"])
                return

            # textbox3の値をチェックしてリストを更新
            if is_int(textbox3_value):
                argument = int(textbox3_value)
                argument = max(1, min(9, argument))  # 1以上8以下の値に制限
                lists[0][3] = argument
            else:
                button_error("int_error", error_messages["int_error"])
                return

            # チェックボックスの値を更新
            if self.check_var.get() != lists[0][2]:
                lists[0][2] = self.check_var.get()
            if self.check_var2.get() != lists[0][1]:
                lists[0][1] = self.check_var2.get()

            # リストを保存してアカウントを更新
            Savelist(lists)
            app.Refresh_account()
            
        def button_Reset(self):
            
            lists = fileopen()
            lists[0][5] = str("C:\Riot Games\Riot Client\RiotClientServices.exe")
            lists[0][4] = str("3")
            lists[0][3] = str("6")
            lists[0][2] = str("0")
            lists[0][1] = str("0")
            
            Savelist(lists)
            app.Refresh_account()  
        def checkbox_event(self):
            print(self.check_var.get())
        def checkbox_event2(self):
            print(self.check_var2.get())
            
        def open_twitter_profile(self):
            url = twitterid
            webbrowser.open(url)
        def open_git_profile(self):
            url = git
            webbrowser.open(url)
        def open_discord_profile(self):
            url = discord
            webbrowser.open(url)   
    class add_account_ui            (customtkinter.CTkCanvas):
        def __init__(self, app_instance,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance  # Appクラスのインスタンスを保持
            # メンバー変数の設定
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            self.setup()
            
        def setup(self):
            customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
            customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
            fg = "#242424"
            h_color = "#0F0F0F"
            frame_bg = "#2b2b2b"
            

            frame = self.app_instance
            
            
            self.label0 = customtkinter.CTkLabel(master=frame, text="Register", font=self.big)
            self.label0.place(x=18, y=15)

            # テキストボックスを表示する
            self.textbox1 = customtkinter.CTkEntry(master=frame, placeholder_text="Riot ID", width=125,
                                                font=self.fonts)
            self.textbox1.place(x=34, y=120)

            self.textbox2 = customtkinter.CTkEntry(master=frame, placeholder_text="TAGLINE", width=125,
                                                font=self.fonts)
            self.textbox2.place(x=167, y=120)

            self.textbox3 = customtkinter.CTkEntry(master=frame, placeholder_text="Login ID", width=125,
                                                font=self.fonts)
            self.textbox3.place(x=34, y=158)

            self.textbox4 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", width=125,
                                                font=self.fonts,show="*")
            self.textbox4.place(x=167, y=158)

            self.button = customtkinter.CTkButton(master=frame, text="Enter", command=self.button_Enter,
                                                font=self.fonts,fg_color="#e0e0e0",hover_color="#bfbfbf",text_color="#0F0F0F")
            self.button.place(x=95, y=270)
            
        def button_Enter(self):
            # テキストボックスに入力されたテキストを表示する
            # 以下に追加の処理を行います
            lists = fileopen()
            rank = Reqrank(Inporturl(str(self.textbox1.get()), self.check_tag(self.textbox2.get())))
            newdata = [str(rank), self.textbox1.get(), self.check_tag(self.textbox2.get()), self.textbox3.get(), self.textbox4.get(),]
            lists.append(newdata)
            Savelist(lists)
            app.Refresh_account()

        def check_tag (self,tag): 
            if '#' in tag[0]:
                tag = tag.replace('#', '')  # '#' を空文字列に置換
            return tag 
    class edit_account_ui           (customtkinter.CTkCanvas):
        def __init__(self, app_instance,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance  # Appクラスのインスタンスを保持
            # メンバー変数の設定
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            
            self.setup()
            
        def setup(self):
            customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
            customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
            fg = "#242424"
            h_color = "#0F0F0F"
            frame_bg = "#2b2b2b"
            
            
            lists = fileopen()
            frame = self.app_instance
            global g_edit_num
            i = g_edit_num
            
            self.label0 = customtkinter.CTkLabel(master=frame, text="Register", font=self.big)
            self.label0.place(x=18, y=15)

            # テキストボックスを表示する
            self.textbox1 = customtkinter.CTkEntry(master=frame, placeholder_text="Riot ID", width=125,
                                                font=self.fonts)
            self.textbox1.place(x=34, y=120)

            self.textbox2 = customtkinter.CTkEntry(master=frame, placeholder_text="TAGLINE", width=125,
                                                font=self.fonts)
            self.textbox2.place(x=167, y=120)

            self.textbox3 = customtkinter.CTkEntry(master=frame, placeholder_text="Login ID", width=125,
                                                font=self.fonts)
            self.textbox3.place(x=34, y=158)

            self.textbox4 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", width=125,
                                                font=self.fonts,show="*")
            self.textbox4.place(x=167, y=158)

            # ボタンを表示する
            self.button9 = customtkinter.CTkButton(master=frame,width=1,  height=1,corner_radius=25,fg_color=fg,text="",command=self.button_delete,image=customtkinter.CTkImage(Image.open("system_png//delete.png"),size=(15,15)),hover_color=frame_bg)
            self.button9.place(x=297,  y=85)
            self.button8 = customtkinter.CTkButton(master=frame,width=0,  height=0,fg_color=fg,text="",command=self.button_copy1,image=customtkinter.CTkImage(Image.open("system_png//clipboard.png"),size=(15,15)),hover_color=frame_bg)
            self.button8.place(x=297,  y=123)
            self.button10 = customtkinter.CTkButton(master=frame,width=0, height=0,fg_color=fg,text="",command=self.button_copy2,image=customtkinter.CTkImage(Image.open("system_png//clipboard.png"),size=(15,15)),hover_color=frame_bg)
            self.button10.place(x=297, y=163)
            
            self.button = customtkinter.CTkButton(master=frame, text="Enter", command=self.button_Enter,
                                                font=self.fonts,fg_color="#e0e0e0",hover_color="#bfbfbf",text_color="#0F0F0F")
            self.button.place(x=95, y=270)
            self.textbox1.insert(index=1,string=f"{lists[i+1][1]}")
            self.textbox2.insert(index=1,string=f"{lists[i+1][2]}")
            self.textbox3.insert(index=1,string=f"{lists[i+1][3]}")
            self.textbox4.insert(index=1,string=f"{lists[i+1][4]}")

            
        def button_Enter(self):
            # テキストボックスに入力されたテキストを表示する
                
            i = g_edit_num
            lists = fileopen()
            lists[i+1][0] = Reqrank(Inporturl(str(self.textbox1.get()),str(self.textbox2.get())))
            lists[i+1][1] = self.textbox1.get()
            lists[i+1][2] = self.textbox2.get()
            lists[i+1][3] = self.textbox3.get()
            lists[i+1][4] = self.textbox4.get()
            lists[i+1][5] = " "
            
            Savelist(lists)
            app.Refresh_account()  
            
        def button_delete(self):
            i = g_edit_num
            app.withdraw()
            Judgment  = button_clicked_yesno(i,"を 削除しますか？")
            if Judgment == "yes":
                deletelist(i)  
                app.deiconify()
            else:
                app.deiconify() 
            
        def button_copy1(self):
            i = g_edit_num
            lists = fileopen()
            text = lists[i+1][1] + "#" + lists[i+1][2]
            pyperclip.copy(text)
                
        def button_copy2(self):
            i = g_edit_num
            lists = fileopen()
            text = lists[i+1][3] + ":" + lists[i+1][4]
            pyperclip.copy(text) 
    class shop_ui                   (customtkinter.CTkCanvas):
        def __init__(self, app_instance,app,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance  # Appクラスのインスタンスを保持
            self.app = app
            # メンバー変数の設定
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            self.progressnum = 0.1
            self.itemupdate = False
            self.setup()
            
        def setup(self):
            customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
            customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
            fg = "#242424"
            h_color = "#0F0F0F"
            frame_bg = "#2b2b2b"
            
            lists = fileopen()
            frame = self.app_instance
            global g_edit_num
            i = g_edit_num
            self.label0 = customtkinter.CTkLabel(master=frame, text="SHOP", font=self.big)
            self.label0.place(x=18, y=15)
            self.labelrank =customtkinter.CTkLabel(master=frame,text="",image=customtkinter.CTkImage(Image.open(Rankimagepath(lists[i + 1][0]))))
            self.labelrank.place(x=15, y=79)
            self.label0 = customtkinter.CTkLabel(master=frame,text=""+lists[i+1][1]+"#"+lists[i+1][2], font=self.fonts)
            self.label0.place(x=42, y=79)
            
            self.button7 = customtkinter.CTkButton(master=frame,width=1, height=1,corner_radius=25,fg_color="#242424",text="",command=self.delete,image=customtkinter.CTkImage(Image.open("system_png//delete.png"),size=(15,15)),hover_color=h_color)
            self.button7.place(x=242, y=81)
            
            self.button8 = customtkinter.CTkButton(master=frame,width=1, height=1,corner_radius=25,fg_color="#242424",text="",command=self.Refresh,image=customtkinter.CTkImage(Image.open("system_png//refresh.png"),size=(15,15)),hover_color=h_color)
            self.button8.place(x=266, y=81)
            self.button9 = customtkinter.CTkButton(master=frame,width=1, height=1,corner_radius=25,fg_color="#242424",text="",command=self.Edit,image=customtkinter.CTkImage(Image.open("system_png//edit.png"),size=(15,15)),hover_color=h_color)
            self.button9.place(x=290, y=81)
            
            self.shop_frame = customtkinter.CTkFrame(master=frame, width=300, height=195,corner_radius=6,border_width=1)
            self.shop_frame.place(x=12,y=110)
            showshop_thread = threading.Thread(target=self.show_item)
            showshop_thread.start()
        def show_item(self):
            self.itemupdate = True
            self.progressbar_frame = customtkinter.CTkFrame(master=self.shop_frame, width=300, height=195,corner_radius=6,border_width=1,fg_color="#2b2b2b")
            self.progressbar_frame.place(x=0,y=0)
            self.progressbar = customtkinter.CTkProgressBar(master=self.progressbar_frame)
            self.progressbar.place(x=55, y=90)
            self.progressbar.set(0)
            self.update_idletasks()  # イベントを処理してUIを更新する
            self.shopimage = self.valorantshop(0)
            self.update_idletasks()  # イベントを処理してUIを更新する
            if "shop_state" == app.get_state():
                if self.shopimage[0] != "Error":
                    self.item1_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130, height=80,corner_radius=10,border_width=1,)
                    self.item1_frame.place(x=15,y=12)
                    self.item2_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130, height=80,corner_radius=10,border_width=1,)
                    self.item2_frame.place(x=154,y=12)
                    self.item3_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130, height=80,corner_radius=10,border_width=1,)
                    self.item3_frame.place(x=15,y=102)
                    self.item4_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130, height=80,corner_radius=10,border_width=1,)
                    self.item4_frame.place(x=154,y=102)
                    
                    for i, image_info in enumerate(self.shopimage):
                        image_path = image_info[0]
                        self.update_idletasks()  # イベントを処理してUIを更新する
                        # 画像を読み込んでサイズを取得
                        image = image_path
                        width, height = image.size
                        
                        # アスペクト比を保持しつつy軸を25にするための計算
                        original_aspect_ratio = width / height
                        
                        # アスペクト比を保持しつつy軸を25にするための計算
                        new_height = 30
                        new_width = int(original_aspect_ratio * new_height)
                        
                        #横の大きさチェック
                        
                        #print(i,":",new_width,new_height)
                        if new_width  <= 80:
                            new_height = 45
                            new_width = int(original_aspect_ratio * new_height)
                        
                        
                        if new_width >= 125:
                            new_height = 23
                            new_width = int(original_aspect_ratio * new_height)
                        
                        
                        #print(i,":",new_width,new_height)
                        framecenter = [65,40]
                        imagecenter  = [new_width / 2 , new_height / 2]

                        print(new_width,"x",new_height,"-合計:",new_width*new_width)
                        
                        # 位置を計算して配置
                        if i == 0:
                            label1 = customtkinter.CTkLabel(master=self.item1_frame, image=customtkinter.CTkImage(image,size=(new_width,new_height)), text="")
                            label1.place(x=framecenter[0] - imagecenter[0], y=framecenter[1] - imagecenter[1])
                        elif i == 1:
                            label2 = customtkinter.CTkLabel(master=self.item2_frame, image=customtkinter.CTkImage(image,size=(new_width,new_height)), text="")
                            label2.place(x=framecenter[0] - imagecenter[0], y=framecenter[1] - imagecenter[1])
                        elif i == 2:
                            label3 = customtkinter.CTkLabel(master=self.item3_frame, image=customtkinter.CTkImage(image,size=(new_width,new_height)), text="")
                            label3.place(x=framecenter[0] - imagecenter[0], y=framecenter[1] - imagecenter[1])
                        elif i == 3:
                            label4 = customtkinter.CTkLabel(master=self.item4_frame, image=customtkinter.CTkImage(image,size=(new_width,new_height)), text="")
                            label4.place(x=framecenter[0] - imagecenter[0], y=framecenter[1] - imagecenter[1]) 
                else:
                    errorlabel = customtkinter.CTkLabel(master=self.shop_frame,text=f"ERROR\n{self.shopimage[1]}",font=self.fonts)
                    errorlabel.place(x=145,y=85,anchor="center") 
                
                self.update_idletasks()  # イベントを処理してUIを更新する
                self.progressbar.set(1)
                self.progressbar_frame.destroy()
                self.itemupdate = False   
        def Edit(self):
            app.update_state("editaccount_state")
        def valorantshop(self,progressnum):
            
            i = g_edit_num
            lists = fileopen()
            shop = []
            error = []
            import json
            try:
                self.progressbar.set(progressnum)
                self.update_idletasks()  # イベントを処理してUIを更新する
                valorant_store = ValorantStore(username=lists[i+1][3], password=lists[i+1][4], region="ap", sess_path="system_png/pickle", proxy=None)
               
            except Exception as e:
                error_message = str(e)  # エラーメッセージを取得
                # JSONレスポンスからエラータイプをチェックする代わりに、エラーメッセージを直接チェックします
                if "'type': 'auth', 'error': 'auth_failure'" in error_message:
                    error.append("Error")  # エラーメッセージをリストに追加
                    error.append("二段階認証を外してください")  # エラーメッセージをリストに追加
                    return error
                else:
                    print(error_message)
                    error.append("Error")  # エラーメッセージをリストに追加
                    error.append(error_message)  # エラーメッセージをリストに追加
                    return error
                
            skindata = self.extract_images(valorant_store.store(True))
            for i in range(4):
                response = requests.get(skindata[i])
                if response.status_code == 200:
                    image_bytes = response.content
                    image_data = BytesIO(image_bytes)
                    img = Image.open(image_data)
                    size = img.size  # 画像のサイズを取得
                    url_and_size = [img, size[0], size[1]]  # URLとサイズのリストを作成
                    shop.append(url_and_size)
                    progressnum = progressnum + 0.25
                    self.progressbar.set(progressnum)
                    self.update_idletasks()  # イベントを処理してUIを更新する

            self.progressnum = progressnum
            return shop
        def extract_images(self,json_data):
            images = []
            if 'daily_offers' in json_data and 'data' in json_data['daily_offers']:
                daily_offers = json_data['daily_offers']['data']
                for offer in daily_offers:
                    if 'image' in offer:
                        images.append(offer['image'])

            if 'bundles' in json_data and 'data' in json_data['bundles']:
                bundles = json_data['bundles']['data']
                for bundle in bundles:
                    if 'image' in bundle:
                        images.append(bundle['image'])

                        if 'items' in bundle:
                            items = bundle['items']
                            for item in items:
                                if 'image' in item:
                                    images.append(item['image'])

            return images
        def Refresh(self):
            if self.itemupdate == False:
                children = self.shop_frame.winfo_children()[:]  # Copy the list to avoid modification while iterating
                for widget in children:
                    try:
                        widget.destroy()
                    except customtkinter.TclError as e:
                        print(f"Widget {widget} already destroyed: {e}")
                        
                showshop_thread = threading.Thread(target=self.show_item)
                showshop_thread.start()
        def delete(self):
            i = g_edit_num
            app.withdraw()
            Judgment  = button_clicked_yesno(i,"を 削除しますか？")
            if Judgment == "yes":
                deletelist(i)  
                app.deiconify()
            else:
                app.deiconify()       
class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, command2 = None ,command3=None ,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        self.command = command
        self.command2 = command2
        self.command3 = command3
        self.fonts = (FONT_TYPE, 12,)
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []
        self.button2_list = []

    def add_item(self,num,i,lists, item, image = None):
        
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        fg = "#242424"
        h_color = "#0F0F0F"
        frame_bg = "#2b2b2b"
        text_color = "#f2efec"
            
        changed_num = change_correct_number(num)
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w",text_color = text_color,font=self.fonts)
        
        button1 = customtkinter.CTkButton(self,width=1, height=1,corner_radius=25,fg_color=frame_bg,text="",image=customtkinter.CTkImage(Image.open("system_png\play.png"),size=(15,15)),hover_color=h_color)
        button2 = customtkinter.CTkButton(self,width=1, height=1,corner_radius=25,fg_color=frame_bg, text="",image=customtkinter.CTkImage(Image.open("system_png\shop.png"),size=(15,15)),hover_color=h_color)
        
        if self.command is not None:
            button1.configure(command=lambda: self.command(i))
        if self.command2 is not None:
            button2.configure(command=lambda: self.command2(i))
        if self.command3 is not None:
            button2.configure(command=lambda: self.command3(i))
             
        label.grid(row=len(self.label_list), column=0, pady=(0, changed_num), sticky="w")
        
        button1.grid(row=len(self.button_list), column=2, pady=(0, changed_num), padx=2)
        button2.grid(row=len(self.button_list), column=1, pady=(0, changed_num), padx=2)
        
        self.label_list.append(label)
        self.button_list.append(button1)
        
    def Edit_item(self,i, item, image = None,):
        label = customtkinter.CTkLabel(self, text=item, image=image, padx=5)
        
        button1 = customtkinter.CTkButton(self,width=1, height=1,corner_radius=25,fg_color="#2b2b2b",text="",image=customtkinter.CTkImage(Image.open("system_png\Edit.png"),size=(15,15)))
        button2 = customtkinter.CTkButton(self,width=1, height=1,corner_radius=25,fg_color="#2b2b2b", text="",image=customtkinter.CTkImage(Image.open("system_png\delete.png"),size=(15,15)))
        if self.command is not None:
            button1.configure(command=lambda: self.command(i))
        if self.command2 is not None:
            button2.configure(command=lambda: self.command2(i))
             
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        
        button1.grid(row=len(self.button_list), column=2, pady=(0, 10), padx=2)
        button2.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=2)
        
        self.label_list.append(label)
        self.button_list.append(button1)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return                         
def valorantrank_sort_up(arr):
    sizes = {'now rank': 0, 'Unranked': 1, 'Iron 1': 2, 'Iron 2': 3, 'Iron 3': 4, 'Bronze 1': 5, 'Bronze 2': 6,
             'Bronze 3': 7, 'Silver 1': 8, 'Silver 2': 9, 'Silver 3': 10, 'Gold 1': 11, 'Gold 2': 12, 'Gold 3': 13,
             'Platinum 1': 14, 'Platinum 2': 15, 'Platinum 3': 16, 'Diamond 1': 17, 'Diamond 2': 18, 'Diamond 3': 19,
             'Ascendant 1': 20, 'Ascendant 2': 21, 'Ascendant 3': 22, 'Immortal 1': 23, 'Immortal 2': 24,
             'Immortal 3': 25, 'Radiant': 26, '': 27}
    return sizes.get(arr[0], float('inf'))
def valorantrank_sort_down(arr):
    sizes = {'now rank': 0, 'Iron 1': 25, 'Iron 2': 24, 'Iron 3': 23, 'Bronze 1': 22, 'Bronze 2': 21, 'Bronze 3': 20,
             'Silver 1': 19, 'Silver 2': 18, 'Silver 3': 17, 'Gold 1': 16, 'Gold 2': 15, 'Gold 3': 14,
             'Platinum 1': 13, 'Platinum 2': 12, 'Platinum 3': 11, 'Diamond 1': 10, 'Diamond 2': 9, 'Diamond 3': 8,
             'Ascendant 1': 7, 'Ascendant 2': 6, 'Ascendant 3': 5, 'Immortal 1': 4, 'Immortal 2': 3, 'Immortal 3': 2,
             'Radiant': 1, 'Unranked': 26, '': 27}
    return sizes.get(arr[0], float('inf'))
def Rankimagepath(rank):
    rank_paths = {
        "Unranked": 'rank_png\Rank.png',
        "Iron 1": 'rank_png\iron_1_Rank.png',
        "Iron 2": 'rank_png\iron_2_Rank.png',
        "Iron 3": 'rank_png\iron_3_Rank.png',
        "Bronze 1": 'rank_png\Bronze_1_Rank.png',
        "Bronze 2": 'rank_png\Bronze_2_Rank.png',
        "Bronze 3": 'rank_png\Bronze_3_Rank.png',
        "Silver 1": 'rank_png\Silver_1_Rank.png',
        "Silver 2": 'rank_png\Silver_2_Rank.png',
        "Silver 3": 'rank_png\Silver_3_Rank.png',
        "Gold 1": 'rank_png\Gold_1_Rank.png',
        "Gold 2": 'rank_png\Gold_2_Rank.png',
        "Gold 3": 'rank_png\Gold_3_Rank.png',
        "Platinum 1": 'rank_png\Platinum_1_Rank.png',
        "Platinum 2": 'rank_png\Platinum_2_Rank.png',
        "Platinum 3": 'rank_png\Platinum_3_Rank.png',
        "Diamond 1": 'rank_png\Diamond_1_Rank.png',
        "Diamond 2": 'rank_png\Diamond_2_Rank.png',
        "Diamond 3": 'rank_png\Diamond_3_Rank.png',
        "Ascendant 1": 'rank_png\Ascendant_1_Rank.png',
        "Ascendant 2": 'rank_png\Ascendant_2_Rank.png',
        "Ascendant 3": 'rank_png\Ascendant_3_Rank.png',
        "Immortal 1": 'rank_png\Immortal_1_Rank.png',
        "Immortal 2": 'rank_png\Immortal_2_Rank.png',
        "Immortal 3": 'rank_png\Immortal_3_Rank.png',
        "Radiant": 'rank_png\Radiant_Rank.png',
        "None": 'rank_png\_bad_Rank.png'
    }
    
    return rank_paths.get(rank, 'rank_png\_bad_Rank.png')
def Inporturl(name, tag):
    valorantID = name + "/" + tag
    url = urllib.parse.urljoin(valorantapiurl, valorantID)
    return url
def Reqrank(url):
    timeout=10
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            json_data = response.json()
            data = json_data["data"]
            
            for item in data:
                current_tier = item["currenttierpatched"]
                print("rank", current_tier)
                return current_tier
            current_tier = "Unranked"
            return current_tier
        else:
            if response.status_code >= 500:
                current_tier = "Unranked"
                return current_tier
            else:
                return f"APIError:{response.status_code}"
            
    except requests.exceptions.Timeout:
        return "TimeOutError"
    except requests.exceptions.ConnectionError:
        return "ConnectionError"            
def up_rank(lists,i):
        rank = Reqrank(Inporturl(lists[i+1][1],lists[i+1][2]))
        if rank != lists[i+1][0]:
            lists[i + 1][0] = rank       
def finish_update(self):
        ok_message_box("Alert", "Finish")                    
def launch_riot_client(username,password):
    lists = fileopen()
    riot_client_path = lists[0][5]
    try:
        subprocess.Popen(riot_client_path)
        input_credentials_to_riot_client(username,password)      
    except FileNotFoundError:
        button_error("起動エラー","Riotクライアントが見つかりませんでした。Settingでパスを確認してください。")          
def button_error(error,errormessage):
    # 警告ポップアップを表示
    ctypes.windll.user32.MessageBoxW(0, errormessage, error, 0x30)
def ok_message_box(title, message):
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, message, title, 0x00000000 | 0x00000040) 
def button_clicked_yesno(i,message):
    lists = fileopen()
    result = win32api.MessageBox(0, f"{lists[i+1][0]}\n{lists[i+1][1]} #{lists[i+1][2]} {message}", "警告", 4)
    if result == 6:  # Yesが選択された場合
            return "yes"
    elif result == 7:  # Noが選択された場合
            return "no"
def button_yesno(messege):
    result = win32api.MessageBox(0,f"{messege}", "確認", 4)
    if result == 6:  # Yesが選択された場合
            return "yes"
    elif result == 7:  # Noが選択された場合
            return "no"
def deletelist(i):
    print(i)
    lists = fileopen()
    del lists[i+1]
    Savelist(lists)
    app.Refresh_account()  
def Savelist(lists):
    df = pd.DataFrame(lists)
    df.to_csv(filename,header=False, index=False)    
def input_credentials_to_riot_client(username, password):
    print("input_credentials_to_riot_client()")
    x,y = pyautogui.position()
    lists = fileopen()
    launch_second = lists[0][4]
    riot_client_path = lists[0][5]
    command = [
        riot_client_path,
        "--launch-product=valorant",
        "--launch-patchline=live"
    ]
    while True:
        #Riotクライアントのプロセスが起動しているか確認
        process_name = "RiotClientServices.exe"
        process_check_cmd = f'tasklist /FI "IMAGENAME eq {process_name}" /FO CSV /NH'
        output = subprocess.check_output(process_check_cmd, shell=True).decode()

        if process_name in output:
            # Riotクライアントのウィンドウを取得
            riot_client_windows = gw.getWindowsWithTitle('Riot Client')
            if riot_client_windows:
                riot_client_window = riot_client_windows[0]
                #Riotクライアントのウィンドウがアクティブになるまで待機

                #Riotクライアントのウィンドウが最前面に表示されるようにする
                riot_client_window.maximize()
                tm.sleep(int(launch_second))
                
                # ユーザー名とパスワードのテキストボックスの位置を取得
                username_box = (riot_client_window.left + 155, riot_client_window.top + 250)
                password_box = (riot_client_window.left + 155, riot_client_window.top + 340)

                # ユーザー名とパスワードを入力
                pyautogui.click(username_box)
                pyautogui.typewrite(username)
                pyautogui.click(password_box)
                pyautogui.typewrite(password)

                # ログインボタンの位置を取得
                login_button = (riot_client_window.left + 220, riot_client_window.top + 700)
                # ログインボタンをクリック
                pyautogui.click(login_button)
                if int(lists[0][2]) == 1:
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                
                #ウィンドウを元のサイズに戻す
                riot_client_window.restore()
                if int(lists[0][1]) == 1:
                    sys.exit()
                
                pyautogui.moveTo(x,y)
                break
        tm.sleep(1)       
def mask_text(txt):
    masked_txt = '*' * len(txt)
    return masked_txt     
def is_int(num):
    while True:
        try:
            result = int(num)
            return True
        except:
            return False       
def create_debug_log(FunctionName):
    log_file_name = "debug log.txt"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.platform()
    running_apps = get_running_apps()
    
    log_content = f"Debug Log - {nowversion} - {current_time}\n"
    log_content += "---------------------------------\n"
    log_content += f"{FunctionName}\n"
    log_content += f"OS: {os_info}\n"
    

    log_content += "---------------------------------\n"
    log_content += "Running Apps:\n"
    log_content += "\n".join(running_apps) + "\n"
    log_content += "---------------------------------\n"

    with open(log_file_name, "w") as log_file:
        log_file.write(log_content)

    print(f"Debug log '{log_file_name}' has been created.")
def get_running_apps():
    running_apps = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        running_apps.append(proc.info['name'])
    return running_apps
def change_correct_number(num):
    argument = int(num)
    
    if int(argument):
        if argument <= 0:
            argument = 1
        elif argument >= 9:
            argument = 8
    
    mapping = {
        1: 220,
        2: 90,
        3: 55,
        4: 35,
        5: 19,
        6: 11, #defalt
        7: 5,
        8: 1
    }

    closest_key = min(mapping.keys(), key=lambda x: abs(x - argument))
    return mapping[closest_key]
def header_check():
    lists = fileopen()
    
    try:
        int(lists[0][3])
    except:
        lists[0][3] = "6"
        df = pd.DataFrame(lists)
        df.to_csv(filename,header=False, index=False)
    
    try:
        int(lists[0][4])
    except:
        lists[0][3] = "3"
        df = pd.DataFrame(lists)
        df.to_csv(filename,header=False, index=False)
        
    try:
        int(lists[0][2])
    except:
        lists[0][2] = "0"
        df = pd.DataFrame(lists)
        df.to_csv(filename,header=False, index=False)
        
    try:
        int(lists[0][1])
    except:
        lists[0][1] = "0"
        df = pd.DataFrame(lists)
        df.to_csv(filename,header=False, index=False)

class ValorantStoreException(Exception):
    def __init__(self, exception_type: str, exception_message: str, response=None) -> None:
        if response:
            print(response.status_code)
            print(response.headers)
            print(response.text)
        super().__init__(f"{exception_type.title()}: {exception_message.capitalize()} error")

class ValorantStore:
    __auth = {}

    def __init__(self, username: str, password: str, region: str = "eu", sess_path: str = None, proxy=None):
        self.__username = username.lower().strip()
        self.__password = password
        self.__region = region
        self.__proxy = proxy
        self.__sess_path = sess_path if sess_path else getcwd()
        if not path.exists(self.__sess_path):
            mkdir(self.__sess_path)
        self.__auth_file = path.join(self.__sess_path, f"riot_auth_{self.__username}.pickle")
        self.__cookie_file = path.join(self.__sess_path, f"riot_cookie_{self.__username}.pickle")
        if path.isfile(self.__auth_file) and time() - path.getmtime(self.__auth_file) < 3600:
            try:
                with open(self.__auth_file, "rb") as auth:
                    self.__auth = pickle.load(auth)
            except Exception:
                remove(self.__auth_file)
                self.__login()
        else:
            self.__login()
        self.headers = {
            "X-Riot-Entitlements-JWT": self.__auth["entitlements_token"],
            "Authorization": "Bearer " + self.__auth["access_token"],
        }
        self.request = requests.session()

    @staticmethod
    def __get_access_token(url: str) -> str:
        return [i.split("=")[-1] for i in url.split("#", 1)[-1].split("&") if i.startswith("access_token" + "=")][0]

    @staticmethod
    def __skin_image(skin: str) -> str:
        return f"https://media.valorant-api.com/weaponskinlevels/{skin}/displayicon.png"

    @staticmethod
    def __buddy_image(buddy: str) -> str:
        return f"https://media.valorant-api.com/buddylevels/{buddy}/displayicon.png"

    @staticmethod
    def __card_image(card: str) -> str:
        return f"https://media.valorant-api.com/playercards/{card}/largeart.png"

    @staticmethod
    def __spray_image(spray: str) -> str:
        return f"https://media.valorant-api.com/sprays/{spray}/fulltransparenticon.png"

    @staticmethod
    def __bundle_image(bundle: str) -> str:
        return f"https://media.valorant-api.com/bundles/{bundle}/displayicon.png"

    @staticmethod
    def skin_info(skin: str) -> dict:
        response = requests.get(f"https://valorant-api.com/v1/weapons/skinlevels/{skin}")
        try:
            return response.json()["data"]
        except Exception:
            raise ValorantStoreException("skin_info", "request", response)

    @staticmethod
    def buddy_info(buddy: str) -> dict:
        response = requests.get(f"https://valorant-api.com/v1/buddies/levels/{buddy}")
        try:
            return response.json()["data"]
        except Exception:
            raise ValorantStoreException("buddy_info", "request", response)

    @staticmethod
    def card_info(card: str) -> dict:
        response = requests.get(f"https://valorant-api.com/v1/playercards/{card}")
        try:
            return response.json()["data"]
        except Exception:
            raise ValorantStoreException("card_info", "request", response)

    @staticmethod
    def spray_info(spray: str) -> dict:
        response = requests.get(f"https://valorant-api.com/v1/sprays/{spray}")
        try:
            return response.json()["data"]
        except Exception:
            raise ValorantStoreException("spray_info", "request", response)

    @staticmethod
    def bundle_info(bundle: str) -> dict:
        response = requests.get(f"https://valorant-api.com/v1/bundles/{bundle}")
        try:
            return response.json()["data"]
        except Exception:
            raise ValorantStoreException("skin info", "request", response)

    @property
    def region(self) -> str:
        return self.__region

    @property
    def username(self) -> str:
        return self.__username

    @property
    def auth(self) -> dict:
        return self.__auth

    @property
    def sess_path(self) -> str:
        return self.__sess_path

    @property
    def proxy(self) -> str:
        return self.__proxy

    @property
    def auth_file(self) -> str:
        return self.__auth_file

    @property
    def cookie_file(self) -> str:
        return self.__cookie_file

    def __login(self):
        scraper = cfscrape.create_scraper()
        if self.__proxy:
            scraper.proxies = {
                'http': self.__proxy,
                'https': self.__proxy,
            }
        if path.isfile(self.__cookie_file):
            try:
                with open(self.__cookie_file, "rb") as cookies:
                    scraper.cookies = pickle.load(cookies)
                login_response = scraper.get(
                    "https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id"
                    "=play-valorant-web-prod&response_type=token%20id_token&nonce=1", allow_redirects=False, timeout=15)
                if login_response.status_code != 303 or login_response.headers.get("location").find(
                        "access_token") == -1:
                    remove(self.__cookie_file)
                    return self.__login()
                else:
                    self.__auth["access_token"] = self.__get_access_token(login_response.headers.get("location"))
            except Exception:
                remove(self.__cookie_file)
                return self.__login()
        else:
            cookie_response = scraper.post("https://auth.riotgames.com/api/v1/authorization", json={
                "client_id": "play-valorant-web-prod",
                "nonce": "1",
                "redirect_uri": "https://playvalorant.com/opt_in",
                "response_type": "token id_token"
            }, timeout=15)
            try:
                cookie = cookie_response.json()
            except Exception:
                raise ValorantStoreException("cookie", "request", cookie_response)
            if "type" not in cookie:
                raise ValorantStoreException("cookie", "request", cookie_response)
            elif cookie["type"] != "auth":
                raise ValorantStoreException("cookie", "type", cookie_response)
            else:
                login_response = scraper.put("https://auth.riotgames.com/api/v1/authorization", json={
                    "type": "auth",
                    "username": self.__username,
                    "password": self.__password,
                    "remember": True,
                    "language": "en_US"
                }, timeout=15)
                with open(self.__cookie_file, "wb") as cookies:
                    pickle.dump(scraper.cookies, cookies)
            try:
                login = login_response.json()
            except Exception:
                raise ValorantStoreException("access", "request", login_response)
            if "type" in login and login["type"] == "multifactor":
                raise ValorantStoreException("access", "multifactor", login_response)
            try:
                self.__auth["access_token"] = self.__get_access_token(login["response"]["parameters"]["uri"])
            except Exception:
                raise ValorantStoreException("access", "token", login_response)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.__auth["access_token"]
        }
        entitlements_response = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=headers,
                                             timeout=15)
        try:
            entitlements = entitlements_response.json()
            self.__auth["entitlements_token"] = entitlements["entitlements_token"]
        except Exception:
            raise ValorantStoreException("entitlements", "request", entitlements_response)
        player_response = scraper.get("https://auth.riotgames.com/userinfo", headers=headers, timeout=15)
        try:
            player = player_response.json()
            self.__auth["player"] = player["sub"]
        except Exception:
            raise ValorantStoreException("player", "request", player_response)
        with open(self.__auth_file, "wb") as auth:
            pickle.dump(self.__auth, auth)

    def wallet(self, format_response: bool = True) -> dict:
        response = self.request.get(f"https://pd.{self.__region}.a.pvp.net/store/v1/wallet/{self.__auth['player']}",
                                    headers=self.headers)
        try:
            wallet = response.json()
            if format_response:
                return {
                    "valorant_points": wallet["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                    "radianite_points": wallet["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"],
                    "free_agents": wallet["Balances"]["f08d4ae3-939c-4576-ab26-09ce1f23bb37"]
                }
            else:
                return wallet
        except Exception:
            raise ValorantStoreException("wallet", "request", response)

    def store(self, format_response: bool = True) -> dict:
        response = self.request.get(
            f"https://pd.{self.__region}.a.pvp.net/store/v2/storefront/{self.__auth['player']}",
            headers=self.headers)
        try:
            store = response.json()
            if format_response:
                offers = []
                for offer in store["SkinsPanelLayout"]["SingleItemOffers"]:
                    offers.append({
                        "id": offer,
                        "type": "skin",
                        "image": self.__skin_image(offer)
                    })
                data = {
                    "daily_offers": {
                        "remaining_duration": store["SkinsPanelLayout"]["SingleItemOffersRemainingDurationInSeconds"],
                        "data": offers
                    }
                }
                if "BonusStore" in store:
                    bonuses = []
                    for bonus in store["BonusStore"]["BonusStoreOffers"]:
                        bonuses.append({
                            "id": bonus["Offer"]["OfferID"],
                            "type": "skin",
                            "image": self.__skin_image(bonus["Offer"]["OfferID"]),
                            "original_cost": bonus["Offer"]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                            "discount_cost": bonus["DiscountCosts"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                            "discount_percent": bonus["DiscountPercent"]
                        })
                    data["night_market"] = {
                        "remaining_duration": store["BonusStore"]["BonusStoreRemainingDurationInSeconds"],
                        "data": bonuses
                    }

                if "FeaturedBundle" in store:
                    bundles = []
                    for bundle in store["FeaturedBundle"]["Bundles"]:
                        items = []
                        for item in bundle["Items"]:
                            add = {
                                "id": item["Item"]["ItemID"],
                                "amount": item["Item"]["Amount"]
                            }
                            if item["Item"]["ItemTypeID"] == "e7c63390-eda7-46e0-bb7a-a6abdacd2433":
                                add["type"] = "skin"
                                add["image"] = self.__skin_image(item["Item"]["ItemID"])
                            elif item["Item"]["ItemTypeID"] == "dd3bf334-87f3-40bd-b043-682a57a8dc3a":
                                add["type"] = "buddy"
                                add["image"] = self.__buddy_image(item["Item"]["ItemID"])
                            elif item["Item"]["ItemTypeID"] == "3f296c07-64c3-494c-923b-fe692a4fa1bd":
                                add["type"] = "card"
                                add["image"] = self.__card_image(item["Item"]["ItemID"])
                            elif item["Item"]["ItemTypeID"] == "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475":
                                add["type"] = "spray"
                                add["image"] = self.__spray_image(item["Item"]["ItemID"])
                            items.append(add)
                        bundles.append({
                            "id": bundle["DataAssetID"],
                            "image": self.__bundle_image(bundle["DataAssetID"]),
                            "items": items,
                            "remaining_duration": bundle["DurationRemainingInSeconds"]
                        })
                        data["bundles"] = {
                            "remaining_duration": store["FeaturedBundle"]["BundleRemainingDurationInSeconds"],
                            "data": bundles
                        }
                return data
            else:
                return store
        except Exception:
            raise ValorantStoreException("store", "request", response)

    def session(self) -> dict:
        response = self.request.get(
            f"https://glz-{self.__region}-1.{self.__region}.a.pvp.net/session/v1/sessions/{self.__auth['player']}",
            headers=self.headers)
        try:
            return response.json()
        except Exception:
            raise ValorantStoreException("session", "request", response)
 
if __name__ == "__main__":
    app = App()
    iconfile = 'system_png\\valoicon.ico' 
    app.iconbitmap(iconfile)
    app.mainloop()    
