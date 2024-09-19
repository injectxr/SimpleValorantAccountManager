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
import tkinter as tk
from bs4 import BeautifulSoup
import json
import pickle



TRACKERGG = "https://tracker.gg/valorant/profile/riot/"
valorantapiurl = "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/"

filename = 'valorant-rank.csv'
nowversion = "v 2.1.0 "
twitterid = "https://twitter.com/i/user/825939612690378752"
discord = "https://discord.gg/bqy2hdbhC5"
git = "https://github.com/injectxr/SimpleValorantAccountManager"
server = "https://status.henrikdev.xyz/"
dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
debug = True
global g_edit_num
global username
username = "AccountManager"
width = 500
hight = 320
states = "account_state"
folder_path = 'system_png/pickle'
themejson = "theme.json"

default_data = {
    "g_text_color": "#f2efec",
    "g_1_bg_color": "#242424",
    "g_1_hover_color": "#0F0F0F",
    "g_2_bg_color": "#2b2b2b",
    "g_line_color": "#f2efec",
    "g_button_color": "#e0e0e0",
    "g_button_hover_color": "#bfbfbf",
    "g_button_text_color": "#0F0F0F",
    "g_button_line_color": "#808080",
    "g_progress_color": "blue",
    "g_frame_in_frame_color": "#333333",
    "theme": "dark",
    "font" : "Meiryo UI",
}

g_text_color = "#f2efec"
g_1_bg_color = "#242424"
g_1_hover_color = "#0F0F0F"
g_2_bg_color = "#2b2b2b"
g_linecoloer = "#f2efec"
g_button_color = "#e0e0e0"
g_button_hover_color = "#bfbfbf"
g_button_text_color = "#0F0F0F"
g_button_line_color = "#808080"
g_progress_color = "blue"
g_frame_in_frame_color = "#333333"
g_ctk_theme = ["dark","dark-blue"]
FONT_TYPE = "Meiryo UI"
FONT_TYPE2 = "Meiryo UI"
iconfile = 'system_png\\valoicon.ico' 


def fileopen():
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            header = [
                "now rank", "0", "0", "6",
                "3", "C:/Riot Games/Riot Client/RiotClientServices.exe",""
            ]
            writer = csv.writer(f)
            writer.writerow(header)

    with open(filename, encoding='utf-8', newline='') as f:
        data = csv.reader(f)
        result = [line for line in data]
    return result

def themesetting():
    if not os.path.isfile(themejson):
        print(f"ファイル '{themejson}' が見つかりません。デフォルトデータを作成します。")
        with open(themejson, 'w') as file:
            json.dump(default_data, file, indent=4)
        data = default_data
    else:
        try:
            with open(themejson, 'r') as file:
                data = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            data = default_data

    global g_text_color, g_1_bg_color, g_1_hover_color, g_2_bg_color
    global g_line_color, g_button_color, g_button_hover_color, g_button_text_color
    global g_button_line_color, g_progress_color, g_frame_in_frame_color, g_ctk_theme, FONT_TYPE

    g_text_color = data['g_text_color']
    g_1_bg_color = data['g_1_bg_color']
    g_1_hover_color = data['g_1_hover_color']
    g_2_bg_color = data['g_2_bg_color']
    g_line_color = data['g_line_color']
    g_button_color = data['g_button_color']
    g_button_hover_color = data['g_button_hover_color']
    g_button_text_color = data['g_button_text_color']
    g_button_line_color = data['g_button_line_color']
    g_progress_color = data['g_progress_color']
    g_frame_in_frame_color = data['g_frame_in_frame_color']
    FONT_TYPE = data['font']

    if data["theme"] == "dark":
        g_ctk_theme = ["dark","dark-blue"]
    else:
        g_ctk_theme = ["light","green"]
        
class App(customtkinter.CTk): 
    def __init__(self, master=None):
        super().__init__(master)
        themesetting()
        self.minmin = (FONT_TYPE, 7,"bold")
        self.min = (FONT_TYPE, 10,"bold")
        self.fonts = (FONT_TYPE, 15,"bold")
        self.label = (FONT_TYPE, 24,"bold")
        self.labeltate = (FONT_TYPE, 800,"bold")
        self.resizable(False, False)
        global username 
        self.geometry(f"{width}x{hight}")
        self.title(username)
        self.attributes("-topmost", True)
        self.attributes('-topmost', False)
        self.geometry('+710+360')
        self.start_x = None
        self.start_y = None
        self.cnt = 0
        header_check()
        
        customtkinter.set_appearance_mode(g_ctk_theme[0]) 
        customtkinter.set_default_color_theme(g_ctk_theme[1])  
        
        self.setup()
    def setup(self):
        self.background_frame()
        self.main_widget()
        self.init_widget()
        self.side_widget()
        self.window_drag()
        
        Refresh_account = threading.Thread(target=self.Refresh_account)
        Refresh_account.start()
        self.stateui()
        
        self.Register_window         = None
        self.Edit_window             = None
        self.Setting_window          = None
        self.AccountEdit_Window      = None
        self.copy_Window             = None
    def init(self):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"削除中にエラーが発生しました: {e}")    
    def background_frame(self):
        fg = g_1_bg_color
        self.background_frame= customtkinter.CTkFrame(self, width=500, height=320,corner_radius=0,fg_color=fg)
        self.background_frame.place(x=0,y=0)   
    def main_widget(self):
        fg = g_1_bg_color
        h_color = g_1_hover_color
        line_color = g_linecoloer
        
        self.main_frame = customtkinter.CTkFrame(self, width=328, height=320,corner_radius=0,fg_color=fg)
        self.main_frame.place(x=173,y=0)
        self.sub_frame = customtkinter.CTkFrame(self, width=327, height=320,corner_radius=0,fg_color=fg) 
        
        self.button8 = customtkinter.CTkButton(master=self.main_frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.sortbylist_up,image=customtkinter.CTkImage(Image.open("system_png//sort-up.png"),size=(16,16)),hover_color=h_color )
        self.button8.place(x=25, y=10)
        self.button8 = customtkinter.CTkButton(master=self.main_frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.sortbylist_down,image=customtkinter.CTkImage(Image.open("system_png//sort-down.png"),size=(16,16)),hover_color=h_color,)
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
        self.main_back_frame = customtkinter.CTkFrame(master=self.main_frame, width=310,height=274,corner_radius=8,fg_color=g_2_bg_color,border_color=g_button_line_color,border_width=1)
        self.main_back_frame.place(x=9,y=38)
        
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.main_back_frame, width=280,height=257,
                                                                        command=self.label_button_frame_event1,
                                                                        command2=self.label_button_frame_event2,
                                                                        fg_color=g_2_bg_color)
        self.scrollable_label_button_frame.place(x=2.5,y=1.6)

    def side_widget(self):
        sideframe_color = g_2_bg_color
        text_color = g_text_color
        
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=173, height=320,corner_radius=0,fg_color=sideframe_color)
        self.sidebar_frame2.grid(row=10, column=0, rowspan=10, sticky="nsew",)
        self.sidebar_frame2.place(x=0,y=0)
        self.active_state_frame = customtkinter.CTkFrame(self, width=2, height=34,corner_radius=0,fg_color=g_linecoloer)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.label2 = customtkinter.CTkLabel(master=self.sidebar_frame2,text="", image=customtkinter.CTkImage(Image.open("system_png//valorantlogo.png"),size=(170, 170)))
        self.label2.place(x=1, y=1)    
        
        self.button0 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//User.png")), corner_radius=0,text="Account", anchor= "w", border_spacing= 5, command=self.button_account,font=self.fonts,width=172,height=20 ,fg_color=g_2_bg_color,hover_color=g_1_hover_color,text_color=text_color,)
        self.button0.place(x=0, y=162)
        self.button1 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//settings.png")), corner_radius=0,text="Setting", anchor= "w", border_spacing= 5, command=self.button_setting,font=self.fonts,width=172,height=20 ,fg_color=g_2_bg_color,hover_color=g_1_hover_color,text_color=text_color)
        self.button1.place(x=0, y=198)
        self.button2 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//refresh.png")), corner_radius=0,text="Update Rank", anchor= "w", border_spacing= 5, command=self.button_update,font=self.fonts,width=172,height=20,fg_color=g_2_bg_color,hover_color=g_1_hover_color,text_color=text_color)
        self.button2.place(x=0, y=233)
        self.button3 = customtkinter.CTkButton(master=self.sidebar_frame2,image=customtkinter.CTkImage(Image.open("system_png//add.png")), corner_radius=0,text="Add Account", anchor= "w", border_spacing= 5, command=self.button_register,font=self.fonts,width=172,height=20,fg_color=g_2_bg_color,hover_color=g_1_hover_color,text_color=text_color)
        self.button3.place(x=0, y=269)
    def stateui(self):    
        state = self.get_state()
        fg = g_1_bg_color
        h_color = g_1_hover_color
        
        print("now    state :",state)
        self.delete_widgets_on_mainframe()
        
        if "account_state" != state:
            self.sub_frame.place(x=173,y=0)
            self.button9    = customtkinter.CTkButton(master=self.sub_frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.button_account,image=customtkinter.CTkImage(Image.open("system_png//close.png"),size=(19,19)),hover_color=h_color )
            self.button9.place(x=290, y=7)
        else:
            self.active_state_frame.place(x=-1000,y=-1000)
            self.sub_frame.place(x=-1000,y=1000)
        if   "account_state"    == state:
            self.Refresh_account()
            self.active_state_frame.place(x=1,y=162)
        elif "update_state"     == state:
            self.active_state_frame.place(x=1,y=233)
            self.update_ui(app_instance=self.sub_frame)
        elif "setting_state"    == state:
            self.active_state_frame.place(x=1,y=198)
            self.setting_ui(app_instance=self.sub_frame) 
        elif "addaccount_state" == state:
            self.active_state_frame.place(x=1,y=269)
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
            print(f"update state : {states} -> {new_state}")
            states = new_state
            self.stateui()
    def button_setting(self):
        self.update_state("setting_state")
    def button_register(self):
        self.update_state("addaccount_state")
    def button_update(self):
        self.update_state("update_state")
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
        # print(len(lists))
        # print(lists)
    def label_button_frame_event1(self,i):
        self.withdraw()
        lists = fileopen()
        Judgment  = button_clicked_yesno(i,"を 起動しますか？")
        if Judgment == "yes":
            lists = fileopen()
            flg = close_existing_riot_client()
            launch_riot_client(lists[i+1][3],lists[i+1][4],flg)
            
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
                if widget.winfo_exists():
                    widget.destroy()
                else:
                    print(f"Widget {widget} does not exist anymore.")
            except customtkinter.TclError as e:
                print(f"Error destroying widget {widget}: {e}")
        
        for i in range(len(lists) - 1):
            if self.stateui != "shop_state":
                self.scrollable_label_button_frame.add_item(num, i, lists, lists[i + 1][1] + "#" + lists[i + 1][2],
                                                            image=customtkinter.CTkImage(
                                                                Image.open(Rankimagepath(lists[i + 1][0]))))
        self.update_state("account_state")
            
    def delete_widgets_on_mainframe(self):
        children = self.sub_frame.winfo_children()[:] 
        
        for widget in children:
            try:
                widget.destroy()
            except customtkinter.TclError as e:
                print(f"Widget {widget} already destroyed: {e}")  
    class setting_ui                (customtkinter.CTkCanvas):
        def __init__(self, app_instance,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance 
            self.font = (FONT_TYPE, 9,"bold")
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.label = (FONT_TYPE, 32,"bold")
            self.small = (FONT_TYPE, 10,"bold")
            self.comment = (FONT_TYPE, 13)
            self.setup()
            
        def setup(self):
            lists = fileopen()
            fg = g_1_bg_color
            h_color = g_1_hover_color
            frame_bg = g_2_bg_color
            default_value = lists[0][5]
            default_s = lists[0][4]
            default_num = lists[0][3]
            default_check = lists[0][2]
            default_check2 = lists[0][1]
            apikey = lists[0][6]
            
            self.label0 = customtkinter.CTkLabel(master=self.app_instance, text="Setting", font=self.label)
            self.label0.place(x=18, y=15)

            self.label1 = customtkinter.CTkLabel(master=self.app_instance, text="・RiotClientの場所", font=self.fonts)
            self.label1.place(x=12, y=60)
            self.label1 = customtkinter.CTkLabel(master=self.app_instance, text=f"・login処理待機時間", font=self.fonts)
            self.label1.place(x=12, y=115)
            
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"・アカウント表示[1~9]", font=self.fonts)
            self.label2.place(x=160, y=115)
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"  秒", font=self.fonts,compound="right")
            self.label2.place(x=124.5, y=140)
            
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"  行", font=self.fonts,compound="right")
            self.label2.place(x=274.5, y=140)
            
            
            self.label3 = customtkinter.CTkLabel(master=self.app_instance, text="・APIKEY (HenrikDev Systems)", font=self.fonts)
            self.label3.place(x=12, y=165)
            self.textbox1 = customtkinter.CTkEntry(master=self.app_instance, width=280,
                                                font=self.fonts,placeholder_text = "正しいRiotClientの場所を入れてください")
            self.textbox1.place(x=25, y=85)

            self.textbox2 = customtkinter.CTkEntry(master=self.app_instance, width=100,
                                                font=self.fonts,placeholder_text = "待機時間を入力してください")
            self.textbox2.place(x=25, y=140)
            
            self.textbox3 = customtkinter.CTkEntry(master=self.app_instance, width=100,
                                                font=self.fonts,placeholder_text = "表示数を入力してください[1~9]")
            self.textbox3.place(x=175, y=140)
            
            self.textbox4 = customtkinter.CTkEntry(master=self.app_instance, width=280,
                                                font=self.fonts,placeholder_text = "APIKEY")
            self.textbox4.place(x=25, y=190)
            
            
            self.button1 = customtkinter.CTkButton(master=self.app_instance, text="RESET", command=self.button_Reset,
                                                font=self.fonts,fg_color=g_button_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_color=g_button_line_color,border_width=1)
            self.button1.place(x=18, y=260)
            self.button2 = customtkinter.CTkButton(master=self.app_instance, text="SAVE", command=self.button_Save,
                                                font=self.fonts,fg_color=g_button_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_color=g_button_line_color,border_width=1)
            
            
            
            self.button2.place(x=170, y=260)
            self.button6 = customtkinter.CTkButton(master=self.app_instance,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.open_twitter_profile,image=customtkinter.CTkImage(Image.open("system_png//twitter.png"),size=(15,15)),hover_color=h_color )
            self.button6.place(x=105, y=293)
            self.button7 = customtkinter.CTkButton(master=self.app_instance,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.open_discord_profile,image=customtkinter.CTkImage(Image.open("system_png//discord.png"),size=(15,15)),hover_color=h_color )
            self.button7.place(x=130, y=293)
            self.button7 = customtkinter.CTkButton(master=self.app_instance,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.open_git_profile,image=customtkinter.CTkImage(Image.open("system_png//github.png"),size=(15,15)),hover_color=h_color )
            self.button7.place(x=155, y=293) 
            self.label2 = customtkinter.CTkLabel(master=self.app_instance, text=f"{nowversion}", font=self.font)
            self.label2.place(x=60, y=290) 
            
            self.check_var = customtkinter.StringVar(value=default_check)
            checkbox = customtkinter.CTkCheckBox(master=self.app_instance, text="VALORANT自動起動", command=self.checkbox_event, variable=self.check_var, onvalue="1",offvalue="0",font=self.small)
            checkbox.place(x=25,y=230)
            self.check_var2 = customtkinter.StringVar(value=default_check2)
            checkbox2 = customtkinter.CTkCheckBox(master=self.app_instance, text="起動後自動アプリ終了", command=self.checkbox_event2, variable=self.check_var2, onvalue="1",offvalue="0",font=self.small)
            checkbox2.place(x=176,y=230)
            
            self.textbox1.insert(index=1,string=f"{default_value}")
            self.textbox2.insert(index=1,string=f"{default_s}")
            self.textbox3.insert(index=1,string=f"{default_num}")
            
            if apikey != None or len(apikey) == 0:
                self.textbox4.insert(index=1,string=f"{apikey}")
            
        def button_Save(self):
            error_messages = {
                "path_error": "RiotClientServices.exe以外のpathが入力されています",
                "int_error": "数値を入力してください",
                "apikey_error": "APIキーが無効です"
            }

            textbox1_value = str(self.textbox1.get())
            textbox2_value = str(self.textbox2.get())
            textbox3_value = str(self.textbox3.get())
            textbox4_value = str(self.textbox4.get())
        
            lists = fileopen()

            if "RiotClientServices.exe" in textbox1_value:
                lists[0][5] = textbox1_value
            else:
                button_error("path_error", error_messages["path_error"])
                return

            if is_int(textbox2_value):
                lists[0][4] = textbox2_value if textbox2_value != "" else "3"
            else:
                button_error("int_error", error_messages["int_error"])
                return

            if is_int(textbox3_value):
                argument = int(textbox3_value)
                argument = max(1, min(9, argument))  
                lists[0][3] = argument
            else:
                button_error("int_error", error_messages["int_error"])
                return

            if textbox4_value != lists[0][6]:  
                lists[0][6] = textbox4_value
            

            if self.check_var.get() != lists[0][2]:
                lists[0][2] = self.check_var.get()
            if self.check_var2.get() != lists[0][1]:
                lists[0][1] = self.check_var2.get()
                
            
            Savelist(lists)
            app.Refresh_account()
        def is_valid_apikey(apikey):
            return True
            
        def button_Reset(self):
            
            lists = fileopen()
            lists[0][5] = str("C:\Riot Games\Riot Client\RiotClientServices.exe")
            lists[0][4] = str("3")
            lists[0][3] = str("6")
            lists[0][2] = str("0")
            lists[0][1] = str("0")
            lists[0][6] = str("")
            
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
            self.app_instance = app_instance  
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            self.setup()
            
        def setup(self):

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
                                                font=self.fonts,fg_color=g_button_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_color=g_button_line_color,border_width=1)
            self.button.place(x=95, y=270)
            
        def button_Enter(self):
            lists = fileopen()
            rank = Reqrank(Inporturl(str(self.textbox1.get()), self.check_tag(self.textbox2.get())))
            newdata = [str(rank), self.textbox1.get(), self.check_tag(self.textbox2.get()), self.textbox3.get(), self.textbox4.get(),]
            lists.append(newdata)
            Savelist(lists)
            app.Refresh_account()

        def check_tag (self,tag): 
            if '#' in tag[0]:
                tag = tag.replace('#', '')  
            return tag 
    class edit_account_ui           (customtkinter.CTkCanvas):
        def __init__(self, app_instance,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance  
            # メンバー変数の設定
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            
            self.setup()
            
        def setup(self):
            fg = g_1_bg_color
            frame_bg = g_2_bg_color
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
                                                font=self.fonts,fg_color=g_button_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_color=g_button_line_color,border_width=1)
            self.button.place(x=95, y=270)
            self.textbox1.insert(index=1,string=f"{lists[i+1][1]}")
            self.textbox2.insert(index=1,string=f"{lists[i+1][2]}")
            self.textbox3.insert(index=1,string=f"{lists[i+1][3]}")
            self.textbox4.insert(index=1,string=f"{lists[i+1][4]}")
        def button_Enter(self):
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
            self.app_instance = app_instance 
            self.app = app
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            self.progressnum = 0.1
            self.itemupdate = False
            self.setup()
            
        def setup(self):
            fg = g_1_bg_color 
            h_color = g_1_hover_color
            frame_bg = g_2_bg_color
            
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
            
            self.button6 = customtkinter.CTkButton(master=frame,width=1, height=1,fg_color=fg,text="",command=self.button_copy1,image=customtkinter.CTkImage(Image.open("system_png//clipboard.png"),size=(15,15)),hover_color=frame_bg)
            self.button6.place(x=218, y=81)
            self.button7 = customtkinter.CTkButton(master=frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.delete,image=customtkinter.CTkImage(Image.open("system_png//delete.png"),size=(15,15)),hover_color=h_color)
            self.button7.place(x=242, y=81)

            self.button8 = customtkinter.CTkButton(master=frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.rank_updateThread,image=customtkinter.CTkImage(Image.open("system_png//refresh.png"),size=(15,15)),hover_color=h_color)
            self.button8.place(x=266, y=81)
            self.button9 = customtkinter.CTkButton(master=frame,width=1, height=1,corner_radius=25,fg_color=fg,text="",command=self.Edit,image=customtkinter.CTkImage(Image.open("system_png//edit.png"),size=(15,15)),hover_color=h_color)
            self.button9.place(x=290, y=81)
            
            self.shop_frame = customtkinter.CTkFrame(master=frame,fg_color=frame_bg, width=300, height=195,corner_radius=6,border_width=1,border_color=g_button_line_color)
            self.shop_frame.place(x=12,y=110)
            
            self.button10 = customtkinter.CTkButton(master=self.shop_frame,text="Show Shop",command=self.shop_update,font=self.fonts,fg_color=g_button_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_color=g_button_line_color,border_width=1)
            self.button10.place(x=78, y=80)
            
        
        def shop_update(self):
            self.button10.destroy()
            self.label12 = customtkinter.CTkLabel(master=self.shop_frame, text="修正中", font=self.big)
            self.label12.place(x=95, y=70)
            # self.button10.destroy()
            # showshop_thread = threading.Thread(target=self.show_item)
            # showshop_thread.start()
        def rank_updateThread(self):
            rank_update_thread = threading.Thread(target=self.rank_update)
            rank_update_thread.start()
        def rank_update(self):
            lists = fileopen()
            global g_edit_num
            i = g_edit_num
            url = Inporturl(lists[i+1][1],lists[i+1][2])
            rank = Reqrank(url)
            lists[i+1][0] = rank
            print(rank)
            Savelist(lists)
            
        def show_item(self):
            fg = g_1_bg_color 
            h_color = g_1_hover_color
            frame_bg = g_2_bg_color
            progress_color = g_progress_color
            
            self.itemupdate = True
            self.progressbar = customtkinter.CTkProgressBar(master=self.shop_frame,progress_color=progress_color)
            self.progressbar.place(x=55, y=90)
            self.progressbar.set(0)
            self.update_idletasks()  
            self.shopimage = self.valorantshop(0)
            self.update_idletasks()  
            self.progressbar.set(1)
            self.progressbar.destroy()
            if "shop_state" == app.get_state():
                if self.shopimage[0] != "Error":
                    self.item1_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130,fg_color=g_frame_in_frame_color, height=80,corner_radius=10,border_width=1,border_color=g_button_line_color)
                    self.item1_frame.place(x=15,y=12)
                    self.item2_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130,fg_color=g_frame_in_frame_color, height=80,corner_radius=10,border_width=1,border_color=g_button_line_color)
                    self.item2_frame.place(x=154,y=12)
                    self.item3_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130,fg_color=g_frame_in_frame_color, height=80,corner_radius=10,border_width=1,border_color=g_button_line_color)
                    self.item3_frame.place(x=15,y=102)
                    self.item4_frame = customtkinter.CTkFrame(master=self.shop_frame, width=130,fg_color=g_frame_in_frame_color, height=80,corner_radius=10,border_width=1,border_color=g_button_line_color)
                    self.item4_frame.place(x=154,y=102)
                    
                    for i, image_info in enumerate(self.shopimage):
                        image_path = image_info[0]
                        image = image_path
                        width, height = image.size
                        original_aspect_ratio = width / height
                        new_height = 30
                        new_width = int(original_aspect_ratio * new_height)
                        if new_width  <= 80:
                            new_height = 45
                            new_width = int(original_aspect_ratio * new_height)
                        
                        
                        if new_width >= 119:
                            new_width = 119
                            new_height = int(new_width / original_aspect_ratio)
                        framecenter = [65,40]
                        imagecenter  = [new_width / 2 , new_height / 2]

                        print(new_width,"x",new_height,"-合計:",new_width*new_width)
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
                
                self.update_idletasks() 
                
                self.itemupdate = False   
        def Edit(self):
            app.update_state("editaccount_state")
        def valorantshop(self,progressnum):
            
            i = g_edit_num
            lists = fileopen()
            shop = []
            error = []
            import json
            # progressnum = progressnum
            # try:
            #     self.progressbar.set(progressnum)
            #     self.update_idletasks()  # イベントを処理してUIを更新する
            #     #valorant_store = ValorantStore(username=lists[i+1][3], password=lists[i+1][4], region="ap", sess_path="system_png/pickle", proxy=None)
               
            # except Exception as e:
            #     error_message = str(e)  # エラーメッセージを取得
            #     # JSONレスポンスからエラータイプをチェックする代わりに、エラーメッセージを直接チェックします
            #     if "'type': 'auth', 'error': 'auth_failure'" in error_message:
            #         error.append("Error")  # エラーメッセージをリストに追加
            #         error.append("二段階認証を外してください")  # エラーメッセージをリストに追加
            #         return error
            #     else:
            #         print(error_message)
            #         error.append("Error")  # エラーメッセージをリストに追加
            #         error.append(error_message)  # エラーメッセージをリストに追加
            #         return error
                
            # #skindata = self.extract_images(valorant_store.store(True))
            # for i in range(4):
            #     response = requests.get(skindata[i])
            #     if response.status_code == 200:
            #         image_bytes = response.content
            #         image_data = BytesIO(image_bytes)
            #         img = Image.open(image_data)
            #         size = img.size  # 画像のサイズを取得
            #         url_and_size = [img, size[0], size[1]]  # URLとサイズのリストを作成
            #         shop.append(url_and_size)
            #         for i in range(25):
            #             progressnum = progressnum + 25 / 10
                        
            #         self.progressbar.set(progressnum)
            #         self.update_idletasks()  # イベントを処理してUIを更新する

            # self.progressnum = progressnum
            # return shop

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
                children = self.shop_frame.winfo_children()[:] 
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
        def button_copy1(self):
            i = g_edit_num
            lists = fileopen()
            text = lists[i+1][1] + "#" + lists[i+1][2]
            pyperclip.copy(text)      
    class update_ui                 (customtkinter.CTkCanvas):
        def __init__(self, app_instance,master=None, **kwargs):
            super().__init__(master,**kwargs)
            self.app_instance = app_instance  
            self.font = (FONT_TYPE, 10,"bold")
            self.fonts = (FONT_TYPE, 13,"bold")
            self.path = (FONT_TYPE, 11,"bold")
            self.logfont = (FONT_TYPE2, 8,"bold")
            self.label = (FONT_TYPE, 32,"bold")
            self.small = (FONT_TYPE, 10,"bold")
            self.big = (FONT_TYPE, 32,"bold")
            self.comment = (FONT_TYPE, 13)
            self.setup()
        def setup(self):
            self.label0 = customtkinter.CTkLabel(master=self.app_instance, text="Update", font=self.big)
            self.label0.place(x=18, y=15)
            self.update_frame = customtkinter.CTkFrame(master=self.app_instance,fg_color=g_2_bg_color, width=122, height=255,corner_radius=6,border_width=1)
            self.update_frame.place(x=4, y=62)
            self.log_text = customtkinter.CTkTextbox(master=self.app_instance, fg_color=g_2_bg_color,font=self.logfont, width=192, height=255,corner_radius=6,border_width=1)
            self.log_text.place(x=130, y=62)
            self.button1 = customtkinter.CTkButton(master=self.update_frame,text="Server Check",width=110,command=self.checkserverThread,font=self.fonts,fg_color=g_button_color,border_color=g_button_line_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_width=1)
            self.button1.place(x=6, y=7)
            self.button2 = customtkinter.CTkButton(master=self.update_frame,text="APIkey Check",width=110,command=self.checkAPIThread,font=self.fonts,fg_color=g_button_color,border_color=g_button_line_color, hover_color=g_button_hover_color, text_color=g_button_text_color,border_width=1)
            self.button2.place(x=6, y=41)
            self.button3 = customtkinter.CTkButton(master=self.update_frame,text="Rank Update",width=110,command=self.update_button,font=self.fonts,fg_color=g_button_color,border_color=g_button_line_color,  hover_color=g_button_hover_color, text_color=g_button_text_color,border_width=1)
            self.button3.place(x=6, y=75)
            self.log(f"system : Init") 
            
        def checkserverThread(self):
            thread = threading.Thread(target=self.checkserver)
            self.log(f"system : Check Server") 
            thread.start() 
        def checkAPIThread(self):
            thread = threading.Thread(target=self.checkAPIkey)
            self.log(f"system : Check API") 
            thread.start() 
        def checkAPIkey(self):
            text = self.apikeytest()
            self.log(f"{text}")
        def checkserver(self):
            url = server
            r = requests.get(url)
            # soup = BeautifulSoup(r.content, "html.parser")
            # text = soup.select_one("h1").get_text()
            # text2 = soup.select_one("p").get_text()
            webbrowser.open(url)
        def servertest(self):
            url = server
            r = requests.get(url)
            # soup = BeautifulSoup(r.content, "html.parser")
            # text = soup.select_one("h1").get_text()
            # text2 = soup.select_one("p").get_text()
            webbrowser.open(url)

        def log(self, message):
            self.log_text.insert(tk.END, message + '\n')
            self.log_text.see(tk.END)  # ログを最新にスクロール  
        def update_button(self): 
            self.log("system : Start Update") 
            update_thread = threading.Thread(target=self.update_start)
            update_thread.start()
        def update_start(self):
            if self.apikeytest() == "system : APIKEY Success": 
                lists = fileopen()
                total_tasks = len(lists) - 1
                for i in range(total_tasks):
                    self.after(0, self.update_req(lists, i))
                    self.update_idletasks() 

            else:
                self.log("system : API Error")
            self.log(f"system : Save")    
            Savelist(lists)
                
            
        def Inport_url(self,name, tag):
            lists = fileopen()
            APIKEY = lists[0][6]
            valorantID = name + "/" + tag + "?api_key=" + APIKEY
            url = urllib.parse.urljoin(valorantapiurl, valorantID)
            return url
        def apikeytest(self):
            lists = fileopen()
            Apikey = lists[0][6]
            url = f"https://api.henrikdev.xyz/valorant/v1/esports/schedule?api_key={Apikey}"
        
            timeout=10
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    print("OK")
                    return f"system : APIKEY Success"
                elif response.status_code == 403:
                    print("apikey error")
                    return f"system : APIKEY Failure {response.status_code}"
                elif response.status_code == 429:
                    return f"system : APIKEY limit {response.status_code}"
                else:
                    print("error")
                    return f"system : Error {response.status_code}"
                
            except:
                print("error")
                return f"system : REQUEST Error {response.status_code}"
        def Req_rank(self,url,id,tag):
            timeout=10
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    json_data = response.json()
                    data = json_data["data"]
                    
                    for item in data:
                        current_tier = item["currenttierpatched"]
                        print("rank", current_tier)
                        self.log(f"{current_tier} {id}#{tag}")
                        return current_tier
                    current_tier = "Unranked"
                    return current_tier
                else:
                    if response.status_code >= 500:
                        current_tier = "Unranked"
                        self.log(f"{current_tier} :{id}#{tag}")
                        return current_tier
                    if response.status_code >= 403:
                        self.log(f"APIKEYError : {response.status_code}")
                    else:
                        self.log(f"APIError {response.status_code} :{id}#{tag}")
                        return f"APIError : {response.status_code}"
            except requests.exceptions.Timeout:
                self.log(f"TimeOutError : {id}#{tag} ")
                return "TimeOutError"
            except requests.exceptions.ConnectionError:
                self.log(f"ConnectionError : {id}#{tag} ")
                return "ConnectionError"          
        def update_req(self,lists,i):
            rank = self.Req_rank(self.Inport_url(lists[i+1][1],lists[i+1][2]),lists[i+1][1],lists[i+1][2])
            if rank != lists[i+1][0]:
                lists[i + 1][0] = rank 
     
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
        h_color = g_1_hover_color
        frame_bg = g_2_bg_color
        text_color = g_text_color
        
            
        changed_num = change_correct_number(num)
        label = customtkinter.CTkLabel(self, text=" " + item, image=image, compound="left", padx=0, anchor="w",text_color = text_color,font=self.fonts)
        
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
        
        button1 = customtkinter.CTkButton(self,width=1, height=1,corner_radius=25,fg_color=g_2_bg_color ,text="",image=customtkinter.CTkImage(Image.open("system_png\Edit.png"),size=(15,15)))
        button2 = customtkinter.CTkButton(self,width=1, height=1,corner_radius=25,fg_color=g_2_bg_color , text="",image=customtkinter.CTkImage(Image.open("system_png\delete.png"),size=(15,15)))
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
    sizes = {'now rank': 0, '\ufeffnow rank': 1, 'Unranked': 2,'Unrated': 2, 'Iron 1': 3, 'Iron 2': 4, 'Iron 3': 5, 'Bronze 1': 6, 'Bronze 2': 7,
             'Bronze 3': 8, 'Silver 1': 9, 'Silver 2': 10, 'Silver 3': 11, 'Gold 1': 12, 'Gold 2': 13, 'Gold 3': 14,
             'Platinum 1': 15, 'Platinum 2': 16, 'Platinum 3': 17, 'Diamond 1': 18, 'Diamond 2': 19, 'Diamond 3': 20,
             'Ascendant 1': 21, 'Ascendant 2': 22, 'Ascendant 3': 23, 'Immortal 1': 24, 'Immortal 2': 25,
             'Immortal 3': 26, 'Radiant': 27, '': 28}
    return sizes.get(arr[0], float('inf'))
def valorantrank_sort_down(arr):
    sizes = {'now rank': 0, '\ufeffnow rank': 1, 'Iron 1': 25, 'Iron 2': 24, 'Iron 3': 23, 'Bronze 1': 22, 'Bronze 2': 21, 'Bronze 3': 20,
             'Silver 1': 19, 'Silver 2': 18, 'Silver 3': 17, 'Gold 1': 16, 'Gold 2': 15, 'Gold 3': 14,
             'Platinum 1': 13, 'Platinum 2': 12, 'Platinum 3': 11, 'Diamond 1': 10, 'Diamond 2': 9, 'Diamond 3': 8,
             'Ascendant 1': 7, 'Ascendant 2': 6, 'Ascendant 3': 5, 'Immortal 1': 4, 'Immortal 2': 3, 'Immortal 3': 2,
             'Radiant': 1, 'Unranked': 26,'Unrated': 26, '': 27}
    return sizes.get(arr[0], float('inf'))
def Rankimagepath(rank):
    rank_paths = {
        "Unranked": 'rank_png\Rank.png',
        "Unrated": 'rank_png\Rank.png',
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
    lists = fileopen()
    APIKEY = lists[0][6]
    valorantID = name + "/" + tag + "?api_key=" + APIKEY
    url = urllib.parse.urljoin(valorantapiurl, valorantID)
    return url
def apikeytest(name,tag,APIKEY):
    lists = fileopen()
    valorantID = name + "/" + tag + "?api_key/" + APIKEY
    url = urllib.parse.urljoin(valorantapiurl, valorantID)

    timeout=10

    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print("OK")
            return "OK"
        elif response.status_code == 403:
            print("apikey error")
            return "api_key error"
        else:
            print("error")
            return "error"
    except:
        print("error")
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
def launch_riot_client(username,password,flg):
    lists = fileopen()
    riot_client_path = lists[0][5]
    try:
        subprocess.Popen(riot_client_path)
        input_credentials_to_riot_client(username,password,flg)      
    except FileNotFoundError:
        button_error("起動エラー","Riotクライアントが見つかりませんでした。Settingでパスを確認してください。")          
def button_error(error,errormessage):
    ctypes.windll.user32.MessageBoxW(0, errormessage, error, 0x30)
def ok_message_box(title, message):
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, message, title, 0x00000000 | 0x00000040) 
def button_clicked_yesno(i,message):
    lists = fileopen()
    result = win32api.MessageBox(0, f"{lists[i+1][0]}\n{lists[i+1][1]} #{lists[i+1][2]} {message}", "警告", 4)
    if result == 6:  
            return "yes"
    elif result == 7: 
            return "no"
def button_yesno(messege):
    result = win32api.MessageBox(0,f"{messege}", "確認", 4)
    if result == 6: 
            return "yes"
    elif result == 7: 
            return "no"
def deletelist(i):
    lists = fileopen()
    del lists[i+1]
    Savelist(lists)
    app.Refresh_account()  
def Savelist(lists):
    df = pd.DataFrame(lists)
    df.to_csv(filename,header=False, index=False)    
def input_credentials_to_riot_client(username, password,flg):
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
    i = 0
    while True:
        process_name = "RiotClientServices.exe"
        process_check_cmd = f'tasklist /FI "IMAGENAME eq {process_name}" /FO CSV /NH'
        output = subprocess.check_output(process_check_cmd, shell=True, encoding="cp932")

        if process_name in output:
            riot_client_windows = gw.getWindowsWithTitle('Riot Client')
            if riot_client_windows:
                print("みつかりました")
                riot_client_window = riot_client_windows[0]
                
                thread = StoppableThread(riot_client_window) 
                thread.start()
                if flg:
                    tm.sleep(int(launch_second)+3)
                else:
                    tm.sleep(int(launch_second))
                riot_client_window.activate()
                pyautogui.write(username)
                riot_client_window.activate()
                pyautogui.press('tab')
                riot_client_window.activate()
                pyautogui.write(password)
                riot_client_window.activate()
                login_button = (riot_client_window.left + 220, riot_client_window.top + 650)
                pyautogui.click(login_button)
                
                if int(lists[0][2]) == 1:
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                

                if int(lists[0][1]) == 1:
                    sys.exit()
                thread.stop()
                break
            else:
                if i > 20:
                    print("みつからなかったので終了")
                    thread.stop()
                    break
                    
                else:
                    i = i + 1
                    print("みつかりません",i)
        tm.sleep(1)       
class StoppableThread(threading.Thread):
    def __init__(self, hWnd, *args, **kwargs):
        super().__init__()
        self._stop_event = threading.Event()
        self.hWnd = hWnd
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while not self._stop_event.is_set():
            try:
                print("アクティブ")
                hwnd = int(self.hWnd) 
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.ShowWindow(hwnd, 5)  
                ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0003) 
                ctypes.windll.user32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0003) 
                time.sleep(1) 
            except Exception as e:
                print(f"ウィンドウを最前面に表示できませんでした: {e}")
                time.sleep(1)  
        print("Thread is stopping")

    def stop(self):
        self._stop_event.set()
   
def close_existing_riot_client():
    process_name = "RiotClientServices.exe"
    process_check_cmd = f'taskkill /F /IM {process_name}'
    try:
        subprocess.run(process_check_cmd, shell=True, check=True)
        tm.sleep(3)
        return True
    except subprocess.CalledProcessError:
        return False
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
        6: 11,
        7: 5,
        8: 1
    }

    closest_key = min(mapping.keys(), key=lambda x: abs(x - argument))
    return mapping[closest_key]
def header_check():
    lists = fileopen()
    while len(lists[0]) <= 5:
        lists[0].append("none")

    for index, default_value in [(3, "6"), (4, "3"), (2, "0"), (1, "0")]:
        try:
            int(lists[0][index])
        except (ValueError, IndexError):
            lists[0][index] = default_value

    df = pd.DataFrame(lists)
    df.to_csv(filename, header=False, index=False)




if __name__ == "__main__":
    app = App()
    app.iconbitmap(iconfile)
    app.mainloop()    
