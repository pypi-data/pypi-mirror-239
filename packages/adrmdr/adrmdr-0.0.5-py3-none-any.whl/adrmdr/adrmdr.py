#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周

# 第二部分：导入基本模块及初始化 ########################################################################
 
import tkinter as Tk #line:11
import os #line:12
import traceback #line:13
import ast #line:14
import re #line:15
import xlrd #line:16
import xlwt #line:17
import openpyxl #line:18
import pandas as pd #line:19
import numpy as np #line:20
import math #line:21
import scipy .stats as st #line:22
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:23
import tkinter .font as tkFont #line:24
from tkinter .messagebox import showinfo #line:25
from tkinter .scrolledtext import ScrolledText #line:26
import matplotlib as plt #line:27
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:28
from matplotlib .figure import Figure #line:29
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:30
import collections #line:31
from collections import Counter #line:32
import datetime #line:33
from datetime import datetime ,timedelta #line:34
import xlsxwriter #line:35
import time #line:36
import threading #line:37
import warnings #line:38
from matplotlib .ticker import PercentFormatter #line:39
import sqlite3 #line:40
from sqlalchemy import create_engine #line:41
from sqlalchemy import text as sqltext #line:42
import webbrowser #line:44
global ori #line:47
ori =0 #line:48
global auto_guize #line:49
global biaozhun #line:52
global dishi #line:53
biaozhun =""#line:54
dishi =""#line:55
global ini #line:59
ini ={}#line:60
ini ["四个品种"]=1 #line:61
import random #line:64
import requests #line:65
global version_now #line:66
global usergroup #line:67
global setting_cfg #line:68
global csdir #line:69
global peizhidir #line:70
version_now ="0.0.5"#line:71
usergroup ="用户组=0"#line:72
setting_cfg =""#line:73
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:74
if csdir =="":#line:75
    csdir =str (os .path .dirname (__file__ ))#line:76
    csdir =csdir +csdir .split ("adrmdr")[0 ][-1 ]#line:77
title_all ="药械妆不良反应报表统计分析工作站 V"+version_now #line:80
title_all2 ="药械妆不良反应报表统计分析工作站 V"+version_now #line:81
def extract_zip_file (O00OOOO0O000O000O ,O00O0OO0O00000OOO ):#line:88
    import zipfile #line:90
    if O00O0OO0O00000OOO =="":#line:91
        return 0 #line:92
    with zipfile .ZipFile (O00OOOO0O000O000O ,'r')as OO0OO000O0000OO0O :#line:93
        for O0O00O0OO000O00OO in OO0OO000O0000OO0O .infolist ():#line:94
            O0O00O0OO000O00OO .filename =O0O00O0OO000O00OO .filename .encode ('cp437').decode ('gbk')#line:96
            OO0OO000O0000OO0O .extract (O0O00O0OO000O00OO ,O00O0OO0O00000OOO )#line:97
def get_directory_path (O00OO0OOO00000OO0 ):#line:103
    global csdir #line:105
    if not (os .path .isfile (os .path .join (O00OO0OOO00000OO0 ,'0（范例）比例失衡关键字库.xls'))):#line:107
        extract_zip_file (csdir +"def.py",O00OO0OOO00000OO0 )#line:112
    if O00OO0OOO00000OO0 =="":#line:114
        quit ()#line:115
    return O00OO0OOO00000OO0 #line:116
def convert_and_compare_dates (OOO000O0OO0O00OOO ):#line:120
    import datetime #line:121
    O0OOOOOO00OOOO000 =datetime .datetime .now ()#line:122
    try :#line:124
       O00OOOO0O00O0O0OO =datetime .datetime .strptime (str (int (int (OOO000O0OO0O00OOO )/4 )),"%Y%m%d")#line:125
    except :#line:126
        print ("fail")#line:127
        return "已过期"#line:128
    if O00OOOO0O00O0O0OO >O0OOOOOO00OOOO000 :#line:130
        return "未过期"#line:132
    else :#line:133
        return "已过期"#line:134
def read_setting_cfg ():#line:136
    global csdir #line:137
    if os .path .exists (csdir +'setting.cfg'):#line:139
        text .insert (END ,"已完成初始化\n")#line:140
        with open (csdir +'setting.cfg','r')as O00OOOO00O0OO0OOO :#line:141
            O000O00O0O0O00000 =eval (O00OOOO00O0OO0OOO .read ())#line:142
    else :#line:143
        OOOOOOO0OO0O0O0O0 =csdir +'setting.cfg'#line:145
        with open (OOOOOOO0OO0O0O0O0 ,'w')as O00OOOO00O0OO0OOO :#line:146
            O00OOOO00O0OO0OOO .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:147
        text .insert (END ,"未初始化，正在初始化...\n")#line:148
        O000O00O0O0O00000 =read_setting_cfg ()#line:149
    return O000O00O0O0O00000 #line:150
def open_setting_cfg ():#line:153
    global csdir #line:154
    with open (csdir +"setting.cfg","r")as OO0OOO000O0O0OOO0 :#line:156
        O0OO0O0OO0OOO0O0O =eval (OO0OOO000O0O0OOO0 .read ())#line:158
    return O0OO0O0OO0OOO0O0O #line:159
def update_setting_cfg (O00OO000OOO00O0OO ,O0000OO0OOO00O000 ):#line:161
    global csdir #line:162
    with open (csdir +"setting.cfg","r")as O0OOOO00OO0OOO0O0 :#line:164
        O00OO00000O0OO000 =eval (O0OOOO00OO0OOO0O0 .read ())#line:166
    if O00OO00000O0OO000 [O00OO000OOO00O0OO ]==0 or O00OO00000O0OO000 [O00OO000OOO00O0OO ]=="11111180000808":#line:168
        O00OO00000O0OO000 [O00OO000OOO00O0OO ]=O0000OO0OOO00O000 #line:169
        with open (csdir +"setting.cfg","w")as O0OOOO00OO0OOO0O0 :#line:171
            O0OOOO00OO0OOO0O0 .write (str (O00OO00000O0OO000 ))#line:172
def generate_random_file ():#line:175
    OO0OO0OOOOOOO0OO0 =random .randint (200000 ,299999 )#line:177
    update_setting_cfg ("sidori",OO0OO0OOOOOOO0OO0 )#line:179
def display_random_number ():#line:181
    global csdir #line:182
    O00OO00000OOO000O =Toplevel ()#line:183
    O00OO00000OOO000O .title ("ID")#line:184
    OO00O00O00O00O0O0 =O00OO00000OOO000O .winfo_screenwidth ()#line:186
    OO0O0O000O0000000 =O00OO00000OOO000O .winfo_screenheight ()#line:187
    OO00OOOOOO00O0000 =80 #line:189
    OO0000O00O0OOOO00 =70 #line:190
    O0OOOOO0OOOO00OOO =(OO00O00O00O00O0O0 -OO00OOOOOO00O0000 )/2 #line:192
    OOO0O00OO0O0O0000 =(OO0O0O000O0000000 -OO0000O00O0OOOO00 )/2 #line:193
    O00OO00000OOO000O .geometry ("%dx%d+%d+%d"%(OO00OOOOOO00O0000 ,OO0000O00O0OOOO00 ,O0OOOOO0OOOO00OOO ,OOO0O00OO0O0O0000 ))#line:194
    with open (csdir +"setting.cfg","r")as O0O0OOO00000OOOOO :#line:197
        O000OO00OOOOOOO00 =eval (O0O0OOO00000OOOOO .read ())#line:199
    O00O000OO0O000OO0 =int (O000OO00OOOOOOO00 ["sidori"])#line:200
    O0OOOO00OOOO000OO =O00O000OO0O000OO0 *2 +183576 #line:201
    print (O0OOOO00OOOO000OO )#line:203
    O0OO0OOOOOOOOO000 =ttk .Label (O00OO00000OOO000O ,text =f"机器码: {O00O000OO0O000OO0}")#line:205
    OO00O0O0O0000OOOO =ttk .Entry (O00OO00000OOO000O )#line:206
    O0OO0OOOOOOOOO000 .pack ()#line:209
    OO00O0O0O0000OOOO .pack ()#line:210
    ttk .Button (O00OO00000OOO000O ,text ="验证",command =lambda :check_input (OO00O0O0O0000OOOO .get (),O0OOOO00OOOO000OO )).pack ()#line:214
def check_input (OOOO0O0O0OOO0O000 ,OO00000O000OOOO0O ):#line:216
    try :#line:220
        O0O00OO00O0000000 =int (str (OOOO0O0O0OOO0O000 )[0 :6 ])#line:221
        OO0OO0OO0O0O0OO00 =convert_and_compare_dates (str (OOOO0O0O0OOO0O000 )[6 :14 ])#line:222
    except :#line:223
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:224
        return 0 #line:225
    if O0O00OO00O0000000 ==OO00000O000OOOO0O and OO0OO0OO0O0O0OO00 =="未过期":#line:227
        update_setting_cfg ("sidfinal",OOOO0O0O0OOO0O000 )#line:228
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:229
        quit ()#line:230
    else :#line:231
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:232
def update_software (OO0000OOO00OO0OO0 ):#line:237
    global version_now #line:239
    text .insert (END ,"当前版本为："+version_now +",正在检查更新...(您可以同时执行分析任务)")#line:240
    try :#line:241
        O000O0OO0OOOOOO0O =requests .get (f"https://pypi.org/pypi/{OO0000OOO00OO0OO0}/json",timeout =2 ).json ()["info"]["version"]#line:242
    except :#line:243
        return "...更新失败。"#line:244
    if O000O0OO0OOOOOO0O >version_now :#line:245
        text .insert (END ,"\n最新版本为："+O000O0OO0OOOOOO0O +",正在尝试自动更新....")#line:246
        pip .main (['install',OO0000OOO00OO0OO0 ,'--upgrade'])#line:248
        text .insert (END ,"\n您可以开展工作。")#line:249
        return "...更新成功。"#line:250
def TOOLS_ror_mode1 (OO0O0OOOO000O00OO ,O0000O00O00O00O00 ):#line:267
	O0000OO0000O0O000 =[]#line:268
	for OOO000000OO00OO0O in ("事件发生年份","性别","年龄段","报告类型-严重程度","停药减药后反应是否减轻或消失","再次使用可疑药是否出现同样反应","对原患疾病影响","不良反应结果","关联性评价"):#line:269
		OO0O0OOOO000O00OO [OOO000000OO00OO0O ]=OO0O0OOOO000O00OO [OOO000000OO00OO0O ].astype (str )#line:270
		OO0O0OOOO000O00OO [OOO000000OO00OO0O ]=OO0O0OOOO000O00OO [OOO000000OO00OO0O ].fillna ("不详")#line:271
		OO0OO00O0OOOOOO00 =0 #line:273
		for O000O0OOOOOOOOOOO in OO0O0OOOO000O00OO [O0000O00O00O00O00 ].drop_duplicates ():#line:274
			OO0OO00O0OOOOOO00 =OO0OO00O0OOOOOO00 +1 #line:275
			OO00O0O00O0OOO00O =OO0O0OOOO000O00OO [(OO0O0OOOO000O00OO [O0000O00O00O00O00 ]==O000O0OOOOOOOOOOO )].copy ()#line:276
			OO0OOOO00OO0000OO =str (O000O0OOOOOOOOOOO )+"计数"#line:278
			O000O0O0O000O00OO =str (O000O0OOOOOOOOOOO )+"构成比(%)"#line:279
			O0OOOO00O0O0O0O00 =OO00O0O00O0OOO00O .groupby (OOO000000OO00OO0O ).agg (计数 =("报告编码","nunique")).sort_values (by =OOO000000OO00OO0O ,ascending =[True ],na_position ="last").reset_index ()#line:280
			O0OOOO00O0O0O0O00 [O000O0O0O000O00OO ]=round (100 *O0OOOO00O0O0O0O00 ["计数"]/O0OOOO00O0O0O0O00 ["计数"].sum (),2 )#line:281
			O0OOOO00O0O0O0O00 =O0OOOO00O0O0O0O00 .rename (columns ={OOO000000OO00OO0O :"项目"})#line:282
			O0OOOO00O0O0O0O00 =O0OOOO00O0O0O0O00 .rename (columns ={"计数":OO0OOOO00OO0000OO })#line:283
			if OO0OO00O0OOOOOO00 >1 :#line:284
				OO0000OOOOO0O000O =pd .merge (OO0000OOOOO0O000O ,O0OOOO00O0O0O0O00 ,on =["项目"],how ="outer")#line:285
			else :#line:286
				OO0000OOOOO0O000O =O0OOOO00O0O0O0O00 .copy ()#line:287
		OO0000OOOOO0O000O ["类别"]=OOO000000OO00OO0O #line:289
		O0000OO0000O0O000 .append (OO0000OOOOO0O000O .copy ().reset_index (drop =True ))#line:290
	OO00O0O0OO00OOO00 =pd .concat (O0000OO0000O0O000 ,ignore_index =True ).fillna (0 )#line:293
	OO00O0O0OO00OOO00 ["报表类型"]="KETI"#line:294
	TABLE_tree_Level_2 (OO00O0O0OO00OOO00 ,1 ,OO00O0O0OO00OOO00 )#line:295
def TOOLS_ror_mode2 (O0OO0000OOOO0O0OO ,OOOO000O0000000O0 ):#line:297
	OOOO0O0000OO00000 =Countall (O0OO0000OOOO0O0OO ).df_ror (["产品类别",OOOO000O0000000O0 ]).reset_index ()#line:298
	OOOO0O0000OO00000 ["四分表"]=OOOO0O0000OO00000 ["四分表"].str .replace ("(","")#line:299
	OOOO0O0000OO00000 ["四分表"]=OOOO0O0000OO00000 ["四分表"].str .replace (")","")#line:300
	OOOO0O0000OO00000 ["ROR信号（0-否，1-是）"]=0 #line:301
	OOOO0O0000OO00000 ["PRR信号（0-否，1-是）"]=0 #line:302
	OOOO0O0000OO00000 ["分母核验"]=0 #line:303
	for OOOO0OO0OOOOO0OO0 ,O00O00O00O00O0000 in OOOO0O0000OO00000 .iterrows ():#line:304
		O00O0OOOO00O0O0O0 =tuple (O00O00O00O00O0000 ["四分表"].split (","))#line:305
		OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"a"]=int (O00O0OOOO00O0O0O0 [0 ])#line:306
		OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"b"]=int (O00O0OOOO00O0O0O0 [1 ])#line:307
		OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"c"]=int (O00O0OOOO00O0O0O0 [2 ])#line:308
		OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"d"]=int (O00O0OOOO00O0O0O0 [3 ])#line:309
		if int (O00O0OOOO00O0O0O0 [1 ])*int (O00O0OOOO00O0O0O0 [2 ])*int (O00O0OOOO00O0O0O0 [3 ])*int (O00O0OOOO00O0O0O0 [0 ])==0 :#line:310
			OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"分母核验"]=1 #line:311
		if O00O00O00O00O0000 ['ROR值的95%CI下限']>1 and O00O00O00O00O0000 ['出现频次']>=3 :#line:312
			OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"ROR信号（0-否，1-是）"]=1 #line:313
		if O00O00O00O00O0000 ['PRR值的95%CI下限']>1 and O00O00O00O00O0000 ['出现频次']>=3 :#line:314
			OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"PRR信号（0-否，1-是）"]=1 #line:315
		OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"事件分类"]=str (TOOLS_get_list (OOOO0O0000OO00000 .loc [OOOO0OO0OOOOO0OO0 ,"特定关键字"])[0 ])#line:316
	OOOO0O0000OO00000 =pd .pivot_table (OOOO0O0000OO00000 ,values =["出现频次",'ROR值',"ROR值的95%CI下限","ROR信号（0-否，1-是）",'PRR值',"PRR值的95%CI下限","PRR信号（0-否，1-是）","a","b","c","d","分母核验","风险评分"],index ='事件分类',columns =OOOO000O0000000O0 ,aggfunc ='sum').reset_index ().fillna (0 )#line:318
	try :#line:321
		OOO0O0OO0000O000O =peizhidir +"0（范例）比例失衡关键字库.xls"#line:322
		if "报告类型-新的"in O0OO0000OOOO0O0OO .columns :#line:323
			OOOOOOO0O0OOO00OO ="药品"#line:324
		else :#line:325
			OOOOOOO0O0OOO00OO ="器械"#line:326
		O0O000O00OO0OOO00 =pd .read_excel (OOO0O0OO0000O000O ,header =0 ,sheet_name =OOOOOOO0O0OOO00OO ).reset_index (drop =True )#line:327
	except :#line:328
		pass #line:329
	for OOOO0OO0OOOOO0OO0 ,O00O00O00O00O0000 in O0O000O00OO0OOO00 .iterrows ():#line:331
		OOOO0O0000OO00000 .loc [OOOO0O0000OO00000 ["事件分类"].str .contains (O00O00O00O00O0000 ["值"],na =False ),"器官系统损害"]=TOOLS_get_list (O00O00O00O00O0000 ["值"])[0 ]#line:332
	try :#line:335
		OOO0OOO000OO00000 =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:336
		try :#line:337
			O00O00OO00OOOOOOO =pd .read_excel (OOO0OOO000OO00000 ,sheet_name ="onept",header =0 ,index_col =0 ).reset_index ()#line:338
		except :#line:339
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:340
		try :#line:342
			O0O0000000000O00O =pd .read_excel (OOO0OOO000OO00000 ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:343
		except :#line:344
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:345
		O00O00OO00OOOOOOO =pd .concat ([O0O0000000000O00O ,O00O00OO00OOOOOOO ],ignore_index =True ).drop_duplicates ("code")#line:347
		O00O00OO00OOOOOOO ["code"]=O00O00OO00OOOOOOO ["code"].astype (str )#line:348
		OOOO0O0000OO00000 ["事件分类"]=OOOO0O0000OO00000 ["事件分类"].astype (str )#line:349
		O00O00OO00OOOOOOO ["事件分类"]=O00O00OO00OOOOOOO ["PT"]#line:350
		OOO0OO0O000OO0O0O =pd .merge (OOOO0O0000OO00000 ,O00O00OO00OOOOOOO ,on =["事件分类"],how ="left")#line:351
		for OOOO0OO0OOOOO0OO0 ,O00O00O00O00O0000 in OOO0OO0O000OO0O0O .iterrows ():#line:352
			OOOO0O0000OO00000 .loc [OOOO0O0000OO00000 ["事件分类"]==O00O00O00O00O0000 ["事件分类"],"Chinese"]=O00O00O00O00O0000 ["Chinese"]#line:353
			OOOO0O0000OO00000 .loc [OOOO0O0000OO00000 ["事件分类"]==O00O00O00O00O0000 ["事件分类"],"PT"]=O00O00O00O00O0000 ["PT"]#line:354
			OOOO0O0000OO00000 .loc [OOOO0O0000OO00000 ["事件分类"]==O00O00O00O00O0000 ["事件分类"],"HLT"]=O00O00O00O00O0000 ["HLT"]#line:355
			OOOO0O0000OO00000 .loc [OOOO0O0000OO00000 ["事件分类"]==O00O00O00O00O0000 ["事件分类"],"HLGT"]=O00O00O00O00O0000 ["HLGT"]#line:356
			OOOO0O0000OO00000 .loc [OOOO0O0000OO00000 ["事件分类"]==O00O00O00O00O0000 ["事件分类"],"SOC"]=O00O00O00O00O0000 ["SOC"]#line:357
	except :#line:358
		pass #line:359
	OOOO0O0000OO00000 ["报表类型"]="KETI"#line:362
	TABLE_tree_Level_2 (OOOO0O0000OO00000 ,1 ,OOOO0O0000OO00000 )#line:363
def TOOLS_ror_mode3 (O0OO0O00OO000OO00 ,OO00O00OOO0OOO0O0 ):#line:365
	O0OO0O00OO000OO00 ["css"]=0 #line:366
	TOOLS_ror_mode2 (O0OO0O00OO000OO00 ,OO00O00OOO0OOO0O0 )#line:367
def TOOLS_ror_mode4 (OOOO0O0O000O0O0OO ,O0OOOO0OOO00000OO ):#line:369
	OO0O0OO0O0000000O =[]#line:370
	for O000OO0O0O0000OO0 ,OO0O000O0O0000O0O in data .drop_duplicates (O0OOOO0OOO00000OO ).iterrows ():#line:371
		OO00OOO0OO0OOOOOO =data [(OOOO0O0O000O0O0OO [O0OOOO0OOO00000OO ]==OO0O000O0O0000O0O [O0OOOO0OOO00000OO ])]#line:372
		OOOOO0OOOOOO0O0O0 =Countall (OO00OOO0OO0OOOOOO ).df_psur ()#line:373
		OOOOO0OOOOOO0O0O0 [O0OOOO0OOO00000OO ]=OO0O000O0O0000O0O [O0OOOO0OOO00000OO ]#line:374
		if len (OOOOO0OOOOOO0O0O0 )>0 :#line:375
			OO0O0OO0O0000000O .append (OOOOO0OOOOOO0O0O0 )#line:376
	OO00OOOOOO00O000O =pd .concat (OO0O0OO0O0000000O ,ignore_index =True ).sort_values (by ="关键字标记",ascending =[False ],na_position ="last").reset_index ()#line:378
	OO00OOOOOO00O000O ["报表类型"]="KETI"#line:379
	TABLE_tree_Level_2 (OO00OOOOOO00O000O ,1 ,OO00OOOOOO00O000O )#line:380
def STAT_pinzhong (O0000OO0OOO0OOOOO ,O00OOOO0OOO0O0000 ,O000000O0OOO0O0O0 ):#line:382
	O0000OOO0OOOO0O00 =[O00OOOO0OOO0O0000 ]#line:384
	if O000000O0OOO0O0O0 ==-1 :#line:385
		OO0OOO0OOOO00000O =O0000OO0OOO0OOOOO .drop_duplicates ("报告编码").copy ()#line:386
		OOOO00O0OOOO0OO00 =OO0OOO0OOOO00000O .groupby ([O00OOOO0OOO0O0000 ]).agg (计数 =("报告编码","nunique")).sort_values (by =O00OOOO0OOO0O0000 ,ascending =[True ],na_position ="last").reset_index ()#line:387
		OOOO00O0OOOO0OO00 ["构成比(%)"]=round (100 *OOOO00O0OOOO0OO00 ["计数"]/OOOO00O0OOOO0OO00 ["计数"].sum (),2 )#line:388
		OOOO00O0OOOO0OO00 [O00OOOO0OOO0O0000 ]=OOOO00O0OOOO0OO00 [O00OOOO0OOO0O0000 ].astype (str )#line:389
		OOOO00O0OOOO0OO00 ["报表类型"]="dfx_deepview"+"_"+str (O0000OOO0OOOO0O00 )#line:390
		TABLE_tree_Level_2 (OOOO00O0OOOO0OO00 ,1 ,OO0OOO0OOOO00000O )#line:391
	if O000000O0OOO0O0O0 ==1 :#line:393
		OO0OOO0OOOO00000O =O0000OO0OOO0OOOOO .copy ()#line:394
		OOOO00O0OOOO0OO00 =OO0OOO0OOOO00000O .groupby ([O00OOOO0OOO0O0000 ]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:395
		OOOO00O0OOOO0OO00 ["构成比(%)"]=round (100 *OOOO00O0OOOO0OO00 ["计数"]/OOOO00O0OOOO0OO00 ["计数"].sum (),2 )#line:396
		OOOO00O0OOOO0OO00 ["报表类型"]="dfx_deepview"+"_"+str (O0000OOO0OOOO0O00 )#line:397
		TABLE_tree_Level_2 (OOOO00O0OOOO0OO00 ,1 ,OO0OOO0OOOO00000O )#line:398
	if O000000O0OOO0O0O0 ==4 :#line:400
		OO0OOO0OOOO00000O =O0000OO0OOO0OOOOO .copy ()#line:401
		OO0OOO0OOOO00000O .loc [OO0OOO0OOOO00000O ["不良反应结果"].str .contains ("好转",na =False ),"不良反应结果2"]="好转"#line:402
		OO0OOO0OOOO00000O .loc [OO0OOO0OOOO00000O ["不良反应结果"].str .contains ("痊愈",na =False ),"不良反应结果2"]="痊愈"#line:403
		OO0OOO0OOOO00000O .loc [OO0OOO0OOOO00000O ["不良反应结果"].str .contains ("无进展",na =False ),"不良反应结果2"]="无进展"#line:404
		OO0OOO0OOOO00000O .loc [OO0OOO0OOOO00000O ["不良反应结果"].str .contains ("死亡",na =False ),"不良反应结果2"]="死亡"#line:405
		OO0OOO0OOOO00000O .loc [OO0OOO0OOOO00000O ["不良反应结果"].str .contains ("不详",na =False ),"不良反应结果2"]="不详"#line:406
		OO0OOO0OOOO00000O .loc [OO0OOO0OOOO00000O ["不良反应结果"].str .contains ("未好转",na =False ),"不良反应结果2"]="未好转"#line:407
		OOOO00O0OOOO0OO00 =OO0OOO0OOOO00000O .groupby (["不良反应结果2"]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:408
		OOOO00O0OOOO0OO00 ["构成比(%)"]=round (100 *OOOO00O0OOOO0OO00 ["计数"]/OOOO00O0OOOO0OO00 ["计数"].sum (),2 )#line:409
		OOOO00O0OOOO0OO00 ["报表类型"]="dfx_deepview"+"_"+str (["不良反应结果2"])#line:410
		TABLE_tree_Level_2 (OOOO00O0OOOO0OO00 ,1 ,OO0OOO0OOOO00000O )#line:411
	if O000000O0OOO0O0O0 ==5 :#line:413
		OO0OOO0OOOO00000O =O0000OO0OOO0OOOOO .copy ()#line:414
		OO0OOO0OOOO00000O ["关联性评价汇总"]="("+OO0OOO0OOOO00000O ["评价状态"].astype (str )+"("+OO0OOO0OOOO00000O ["县评价"].astype (str )+"("+OO0OOO0OOOO00000O ["市评价"].astype (str )+"("+OO0OOO0OOOO00000O ["省评价"].astype (str )+"("+OO0OOO0OOOO00000O ["国家评价"].astype (str )+")"#line:416
		OO0OOO0OOOO00000O ["关联性评价汇总"]=OO0OOO0OOOO00000O ["关联性评价汇总"].str .replace ("(nan","",regex =False )#line:417
		OO0OOO0OOOO00000O ["关联性评价汇总"]=OO0OOO0OOOO00000O ["关联性评价汇总"].str .replace ("nan)","",regex =False )#line:418
		OO0OOO0OOOO00000O ["关联性评价汇总"]=OO0OOO0OOOO00000O ["关联性评价汇总"].str .replace ("nan","",regex =False )#line:419
		OO0OOO0OOOO00000O ['最终的关联性评价']=OO0OOO0OOOO00000O ["关联性评价汇总"].str .extract ('.*\((.*)\).*',expand =False )#line:420
		OOOO00O0OOOO0OO00 =OO0OOO0OOOO00000O .groupby ('最终的关联性评价').agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:421
		OOOO00O0OOOO0OO00 ["构成比(%)"]=round (100 *OOOO00O0OOOO0OO00 ["计数"]/OOOO00O0OOOO0OO00 ["计数"].sum (),2 )#line:422
		OOOO00O0OOOO0OO00 ["报表类型"]="dfx_deepview"+"_"+str (['最终的关联性评价'])#line:423
		TABLE_tree_Level_2 (OOOO00O0OOOO0OO00 ,1 ,OO0OOO0OOOO00000O )#line:424
	if O000000O0OOO0O0O0 ==0 :#line:426
		O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ]=O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ].fillna ("未填写")#line:427
		O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ]=O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ].str .replace ("*","",regex =False )#line:428
		OOOO0O00OO0OOO000 ="use("+str (O00OOOO0OOO0O0000 )+").file"#line:429
		OOO0O0O000000O0OO =str (Counter (TOOLS_get_list0 (OOOO0O00OO0OOO000 ,O0000OO0OOO0OOOOO ,1000 ))).replace ("Counter({","{")#line:430
		OOO0O0O000000O0OO =OOO0O0O000000O0OO .replace ("})","}")#line:431
		OOO0O0O000000O0OO =ast .literal_eval (OOO0O0O000000O0OO )#line:432
		OOOO00O0OOOO0OO00 =pd .DataFrame .from_dict (OOO0O0O000000O0OO ,orient ="index",columns =["计数"]).reset_index ()#line:433
		OOOO00O0OOOO0OO00 ["构成比(%)"]=round (100 *OOOO00O0OOOO0OO00 ["计数"]/OOOO00O0OOOO0OO00 ["计数"].sum (),2 )#line:435
		OOOO00O0OOOO0OO00 ["报表类型"]="dfx_deepvie2"+"_"+str (O0000OOO0OOOO0O00 )#line:436
		TABLE_tree_Level_2 (OOOO00O0OOOO0OO00 ,1 ,O0000OO0OOO0OOOOO )#line:437
	if O000000O0OOO0O0O0 ==2 or O000000O0OOO0O0O0 ==3 :#line:441
		O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ]=O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ].astype (str )#line:442
		O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ]=O0000OO0OOO0OOOOO [O00OOOO0OOO0O0000 ].fillna ("未填写")#line:443
		OOOO0O00OO0OOO000 ="use("+str (O00OOOO0OOO0O0000 )+").file"#line:445
		OOO0O0O000000O0OO =str (Counter (TOOLS_get_list0 (OOOO0O00OO0OOO000 ,O0000OO0OOO0OOOOO ,1000 ))).replace ("Counter({","{")#line:446
		OOO0O0O000000O0OO =OOO0O0O000000O0OO .replace ("})","}")#line:447
		OOO0O0O000000O0OO =ast .literal_eval (OOO0O0O000000O0OO )#line:448
		OOOO00O0OOOO0OO00 =pd .DataFrame .from_dict (OOO0O0O000000O0OO ,orient ="index",columns =["计数"]).reset_index ()#line:449
		print ("正在统计，请稍后...")#line:450
		OOO0O0O00OOO000OO =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:451
		try :#line:452
			OOO0O00OOOOOO0O00 =pd .read_excel (OOO0O0O00OOO000OO ,sheet_name ="simple",header =0 ,index_col =0 ).reset_index ()#line:453
		except :#line:454
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:455
			return 0 #line:456
		try :#line:457
			OO00O00OOOO00OOO0 =pd .read_excel (OOO0O0O00OOO000OO ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:458
		except :#line:459
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:460
			return 0 #line:461
		OOO0O00OOOOOO0O00 =pd .concat ([OO00O00OOOO00OOO0 ,OOO0O00OOOOOO0O00 ],ignore_index =True ).drop_duplicates ("code")#line:462
		OOO0O00OOOOOO0O00 ["code"]=OOO0O00OOOOOO0O00 ["code"].astype (str )#line:463
		OOOO00O0OOOO0OO00 ["index"]=OOOO00O0OOOO0OO00 ["index"].astype (str )#line:464
		OOOO00O0OOOO0OO00 =OOOO00O0OOOO0OO00 .rename (columns ={"index":"code"})#line:466
		OOOO00O0OOOO0OO00 =pd .merge (OOOO00O0OOOO0OO00 ,OOO0O00OOOOOO0O00 ,on =["code"],how ="left")#line:467
		OOOO00O0OOOO0OO00 ["code构成比(%)"]=round (100 *OOOO00O0OOOO0OO00 ["计数"]/OOOO00O0OOOO0OO00 ["计数"].sum (),2 )#line:468
		OOO0OO0OO00OO0000 =OOOO00O0OOOO0OO00 .groupby ("SOC").agg (SOC计数 =("计数","sum")).sort_values (by ="SOC计数",ascending =[False ],na_position ="last").reset_index ()#line:469
		OOO0OO0OO00OO0000 ["soc构成比(%)"]=round (100 *OOO0OO0OO00OO0000 ["SOC计数"]/OOO0OO0OO00OO0000 ["SOC计数"].sum (),2 )#line:470
		OOO0OO0OO00OO0000 ["SOC计数"]=OOO0OO0OO00OO0000 ["SOC计数"].astype (int )#line:471
		OOOO00O0OOOO0OO00 =pd .merge (OOOO00O0OOOO0OO00 ,OOO0OO0OO00OO0000 ,on =["SOC"],how ="left")#line:472
		if O000000O0OOO0O0O0 ==3 :#line:474
			OOO0OO0OO00OO0000 ["具体名称"]=""#line:475
			for O0O0OOO0O0O00OO00 ,OOOOOO00OO00O0OO0 in OOO0OO0OO00OO0000 .iterrows ():#line:476
				O0000OOO00O0O000O =""#line:477
				O00OOOO0OOO00000O =OOOO00O0OOOO0OO00 .loc [OOOO00O0OOOO0OO00 ["SOC"].str .contains (OOOOOO00OO00O0OO0 ["SOC"],na =False )].copy ()#line:478
				for OOOOOOOOOOO0OO00O ,O00OOO0OO0O0O0OOO in O00OOOO0OOO00000O .iterrows ():#line:479
					O0000OOO00O0O000O =O0000OOO00O0O000O +str (O00OOO0OO0O0O0OOO ["PT"])+"("+str (O00OOO0OO0O0O0OOO ["计数"])+")、"#line:480
				OOO0OO0OO00OO0000 .loc [O0O0OOO0O0O00OO00 ,"具体名称"]=O0000OOO00O0O000O #line:481
			OOO0OO0OO00OO0000 ["报表类型"]="dfx_deepvie2"+"_"+str (["SOC"])#line:482
			TABLE_tree_Level_2 (OOO0OO0OO00OO0000 ,1 ,OOOO00O0OOOO0OO00 )#line:483
		if O000000O0OOO0O0O0 ==2 :#line:485
			OOOO00O0OOOO0OO00 ["报表类型"]="dfx_deepvie2"+"_"+str (O0000OOO0OOOO0O00 )#line:486
			TABLE_tree_Level_2 (OOOO00O0OOOO0OO00 ,1 ,O0000OO0OOO0OOOOO )#line:487
	pass #line:490
def DRAW_pre (O0OO000000000OOOO ):#line:492
	""#line:493
	OO000O0OOOO00O00O =list (O0OO000000000OOOO ["报表类型"])[0 ].replace ("1","")#line:501
	if "dfx_org监测机构"in OO000O0OOOO00O00O :#line:503
		O0OO000000000OOOO =O0OO000000000OOOO [:-1 ]#line:504
		DRAW_make_one (O0OO000000000OOOO ,"报告图","监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:505
	elif "dfx_org市级监测机构"in OO000O0OOOO00O00O :#line:506
		O0OO000000000OOOO =O0OO000000000OOOO [:-1 ]#line:507
		DRAW_make_one (O0OO000000000OOOO ,"报告图","市级监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:508
	elif "dfx_user"in OO000O0OOOO00O00O :#line:509
		O0OO000000000OOOO =O0OO000000000OOOO [:-1 ]#line:510
		DRAW_make_one (O0OO000000000OOOO ,"报告单位图","单位名称","报告数量","超级托帕斯图(严重伤害数)")#line:511
	elif "dfx_deepview"in OO000O0OOOO00O00O :#line:514
		DRAW_make_one (O0OO000000000OOOO ,"柱状图",O0OO000000000OOOO .columns [0 ],"计数","柱状图")#line:515
	elif "dfx_chiyouren"in OO000O0OOOO00O00O :#line:517
		O0OO000000000OOOO =O0OO000000000OOOO [:-1 ]#line:518
		DRAW_make_one (O0OO000000000OOOO ,"涉及持有人图","上市许可持有人名称","总报告数","超级托帕斯图(总待评价数量)")#line:519
	elif "dfx_zhenghao"in OO000O0OOOO00O00O :#line:521
		O0OO000000000OOOO ["产品"]=O0OO000000000OOOO ["产品名称"]+"("+O0OO000000000OOOO ["注册证编号/曾用注册证编号"]+")"#line:522
		DRAW_make_one (O0OO000000000OOOO ,"涉及产品图","产品","证号计数","超级托帕斯图(严重伤害数)")#line:523
	elif "dfx_pihao"in OO000O0OOOO00O00O :#line:525
		if len (O0OO000000000OOOO ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:526
			O0OO000000000OOOO ["产品"]=O0OO000000000OOOO ["产品名称"]+"("+O0OO000000000OOOO ["注册证编号/曾用注册证编号"]+"--"+O0OO000000000OOOO ["产品批号"]+")"#line:527
			DRAW_make_one (O0OO000000000OOOO ,"涉及批号图","产品","批号计数","超级托帕斯图(严重伤害数)")#line:528
		else :#line:529
			DRAW_make_one (O0OO000000000OOOO ,"涉及批号图","产品批号","批号计数","超级托帕斯图(严重伤害数)")#line:530
	elif "dfx_xinghao"in OO000O0OOOO00O00O :#line:532
		if len (O0OO000000000OOOO ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:533
			O0OO000000000OOOO ["产品"]=O0OO000000000OOOO ["产品名称"]+"("+O0OO000000000OOOO ["注册证编号/曾用注册证编号"]+"--"+O0OO000000000OOOO ["型号"]+")"#line:534
			DRAW_make_one (O0OO000000000OOOO ,"涉及型号图","产品","型号计数","超级托帕斯图(严重伤害数)")#line:535
		else :#line:536
			DRAW_make_one (O0OO000000000OOOO ,"涉及型号图","型号","型号计数","超级托帕斯图(严重伤害数)")#line:537
	elif "dfx_guige"in OO000O0OOOO00O00O :#line:539
		if len (O0OO000000000OOOO ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:540
			O0OO000000000OOOO ["产品"]=O0OO000000000OOOO ["产品名称"]+"("+O0OO000000000OOOO ["注册证编号/曾用注册证编号"]+"--"+O0OO000000000OOOO ["规格"]+")"#line:541
			DRAW_make_one (O0OO000000000OOOO ,"涉及规格图","产品","规格计数","超级托帕斯图(严重伤害数)")#line:542
		else :#line:543
			DRAW_make_one (O0OO000000000OOOO ,"涉及规格图","规格","规格计数","超级托帕斯图(严重伤害数)")#line:544
	elif "PSUR"in OO000O0OOOO00O00O :#line:546
		DRAW_make_mutibar (O0OO000000000OOOO ,"总数量","严重","事件分类","总数量","严重","表现分类统计图")#line:547
	elif "keyword_findrisk"in OO000O0OOOO00O00O :#line:549
		O00OOO0O00OOOOOOO =O0OO000000000OOOO .columns .to_list ()#line:551
		OOOO0OO0000O0O0O0 =O00OOO0O00OOOOOOO [O00OOO0O00OOOOOOO .index ("关键字")+1 ]#line:552
		OO0O00000OO00OOOO =pd .pivot_table (O0OO000000000OOOO ,index =OOOO0OO0000O0O0O0 ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:563
		OO0O00000OO00OOOO .columns =OO0O00000OO00OOOO .columns .droplevel (0 )#line:564
		OO0O00000OO00OOOO =OO0O00000OO00OOOO [:-1 ].reset_index ()#line:565
		OO0O00000OO00OOOO =pd .merge (OO0O00000OO00OOOO ,O0OO000000000OOOO [[OOOO0OO0000O0O0O0 ,"该元素总数量"]].drop_duplicates (OOOO0OO0000O0O0O0 ),on =[OOOO0OO0000O0O0O0 ],how ="left")#line:567
		del OO0O00000OO00OOOO ["All"]#line:569
		DRAW_make_risk_plot (OO0O00000OO00OOOO ,OOOO0OO0000O0O0O0 ,[OO0OOOO0O000OO000 for OO0OOOO0O000OO000 in OO0O00000OO00OOOO .columns if OO0OOOO0O000OO000 !=OOOO0OO0000O0O0O0 ],"关键字趋势图",100 )#line:574
def DRAW_make_risk_plot (O0OOO00OOOOO00O0O ,OO0O00OOOOO0OOOO0 ,O00O000O0OOO0OO00 ,O0OO000OO0O0O00OO ,OO0OO00OOO00O0OOO ,*O00O0OO0000OOO000 ):#line:579
    ""#line:580
    OO00000OO0OOOOOOO =Toplevel ()#line:583
    OO00000OO0OOOOOOO .title (O0OO000OO0O0O00OO )#line:584
    O0OO00000O0OOOO0O =ttk .Frame (OO00000OO0OOOOOOO ,height =20 )#line:585
    O0OO00000O0OOOO0O .pack (side =TOP )#line:586
    O0OOOO0000O00O000 =Figure (figsize =(12 ,6 ),dpi =100 )#line:588
    OOO00000OOOO0OO0O =FigureCanvasTkAgg (O0OOOO0000O00O000 ,master =OO00000OO0OOOOOOO )#line:589
    OOO00000OOOO0OO0O .draw ()#line:590
    OOO00000OOOO0OO0O .get_tk_widget ().pack (expand =1 )#line:591
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:593
    plt .rcParams ['axes.unicode_minus']=False #line:594
    OO0O00O0OOO00O0OO =NavigationToolbar2Tk (OOO00000OOOO0OO0O ,OO00000OO0OOOOOOO )#line:596
    OO0O00O0OOO00O0OO .update ()#line:597
    OOO00000OOOO0OO0O .get_tk_widget ().pack ()#line:598
    O00000OOO000OOOO0 =O0OOOO0000O00O000 .add_subplot (111 )#line:600
    O00000OOO000OOOO0 .set_title (O0OO000OO0O0O00OO )#line:602
    O00OO000OOO0O00O0 =O0OOO00OOOOO00O0O [OO0O00OOOOO0OOOO0 ]#line:603
    if OO0OO00OOO00O0OOO !=999 :#line:606
        O00000OOO000OOOO0 .set_xticklabels (O00OO000OOO0O00O0 ,rotation =-90 ,fontsize =8 )#line:607
    O0OOO0O0OO0OOO0OO =range (0 ,len (O00OO000OOO0O00O0 ),1 )#line:610
    try :#line:615
        O00000OOO000OOOO0 .bar (O00OO000OOO0O00O0 ,O0OOO00OOOOO00O0O ["报告总数"],color ='skyblue',label ="报告总数")#line:616
        O00000OOO000OOOO0 .bar (O00OO000OOO0O00O0 ,height =O0OOO00OOOOO00O0O ["严重伤害数"],color ="orangered",label ="严重伤害数")#line:617
    except :#line:618
        pass #line:619
    for OO000000000O0O00O in O00O000O0OOO0OO00 :#line:622
        O0OOOOOOOOO0OOOOO =O0OOO00OOOOO00O0O [OO000000000O0O00O ].astype (float )#line:623
        if OO000000000O0O00O =="关注区域":#line:625
            O00000OOO000OOOO0 .plot (list (O00OO000OOO0O00O0 ),list (O0OOOOOOOOO0OOOOO ),label =str (OO000000000O0O00O ),color ="red")#line:626
        else :#line:627
            O00000OOO000OOOO0 .plot (list (O00OO000OOO0O00O0 ),list (O0OOOOOOOOO0OOOOO ),label =str (OO000000000O0O00O ))#line:628
        if OO0OO00OOO00O0OOO ==100 :#line:631
            for O000O0O0OOOOO00O0 ,O0000OOO0000000OO in zip (O00OO000OOO0O00O0 ,O0OOOOOOOOO0OOOOO ):#line:632
                if O0000OOO0000000OO ==max (O0OOOOOOOOO0OOOOO )and O0000OOO0000000OO >=3 :#line:633
                     O00000OOO000OOOO0 .text (O000O0O0OOOOO00O0 ,O0000OOO0000000OO ,(str (OO000000000O0O00O )+":"+str (int (O0000OOO0000000OO ))),color ='black',size =8 )#line:634
    try :#line:644
        if O00O0OO0000OOO000 [0 ]:#line:645
            OO0OOOOOO000OO0O0 =O00O0OO0000OOO000 [0 ]#line:646
    except :#line:647
        OO0OOOOOO000OO0O0 ="ucl"#line:648
    if len (O00O000O0OOO0OO00 )==1 :#line:650
        if OO0OOOOOO000OO0O0 =="更多控制线分位数":#line:652
            OOO0O0000O0000OO0 =O0OOO00OOOOO00O0O [O00O000O0OOO0OO00 ].astype (float ).values #line:653
            O00O0000OO0OOO0O0 =np .where (OOO0O0000O0000OO0 >0 ,1 ,0 )#line:654
            O0O00O0O0O00OO000 =np .nonzero (O00O0000OO0OOO0O0 )#line:655
            OOO0O0000O0000OO0 =OOO0O0000O0000OO0 [O0O00O0O0O00OO000 ]#line:656
            O000O0O0OO00O0O0O =np .median (OOO0O0000O0000OO0 )#line:657
            OO000000O0O000OO0 =np .percentile (OOO0O0000O0000OO0 ,25 )#line:658
            OO0OO00OO00OOO0O0 =np .percentile (OOO0O0000O0000OO0 ,75 )#line:659
            O0OO00O00OO000OOO =OO0OO00OO00OOO0O0 -OO000000O0O000OO0 #line:660
            O000000O0O00O0O0O =OO0OO00OO00OOO0O0 +1.5 *O0OO00O00OO000OOO #line:661
            OOOOOO0OO0O00O0O0 =OO000000O0O000OO0 -1.5 *O0OO00O00OO000OOO #line:662
            O00000OOO000OOOO0 .axhline (OOOOOO0OO0O00O0O0 ,color ='c',linestyle ='--',label ='异常下限')#line:665
            O00000OOO000OOOO0 .axhline (OO000000O0O000OO0 ,color ='r',linestyle ='--',label ='第25百分位数')#line:667
            O00000OOO000OOOO0 .axhline (O000O0O0OO00O0O0O ,color ='g',linestyle ='--',label ='中位数')#line:668
            O00000OOO000OOOO0 .axhline (OO0OO00OO00OOO0O0 ,color ='r',linestyle ='--',label ='第75百分位数')#line:669
            O00000OOO000OOOO0 .axhline (O000000O0O00O0O0O ,color ='c',linestyle ='--',label ='异常上限')#line:671
            O00O0OO0O0OOOO000 =ttk .Label (OO00000OO0OOOOOOO ,text ="中位数="+str (O000O0O0OO00O0O0O )+"; 第25百分位数="+str (OO000000O0O000OO0 )+"; 第75百分位数="+str (OO0OO00OO00OOO0O0 )+"; 异常上限(第75百分位数+1.5IQR)="+str (O000000O0O00O0O0O )+"; IQR="+str (O0OO00O00OO000OOO ))#line:672
            O00O0OO0O0OOOO000 .pack ()#line:673
        elif OO0OOOOOO000OO0O0 =="更多控制线STD":#line:675
            OOO0O0000O0000OO0 =O0OOO00OOOOO00O0O [O00O000O0OOO0OO00 ].astype (float ).values #line:676
            O00O0000OO0OOO0O0 =np .where (OOO0O0000O0000OO0 >0 ,1 ,0 )#line:677
            O0O00O0O0O00OO000 =np .nonzero (O00O0000OO0OOO0O0 )#line:678
            OOO0O0000O0000OO0 =OOO0O0000O0000OO0 [O0O00O0O0O00OO000 ]#line:679
            O0O00000O0O0O0O0O =OOO0O0000O0000OO0 .mean ()#line:681
            O00OOOO00OO0OOO0O =OOO0O0000O0000OO0 .std (ddof =1 )#line:682
            OOO0OO00O0OOO00OO =O0O00000O0O0O0O0O +3 *O00OOOO00OO0OOO0O #line:683
            OO00000O00O00OO0O =O00OOOO00OO0OOO0O -3 *O00OOOO00OO0OOO0O #line:684
            if len (OOO0O0000O0000OO0 )<30 :#line:686
                O00OO0OO0OO00000O =st .t .interval (0.95 ,df =len (OOO0O0000O0000OO0 )-1 ,loc =np .mean (OOO0O0000O0000OO0 ),scale =st .sem (OOO0O0000O0000OO0 ))#line:687
            else :#line:688
                O00OO0OO0OO00000O =st .norm .interval (0.95 ,loc =np .mean (OOO0O0000O0000OO0 ),scale =st .sem (OOO0O0000O0000OO0 ))#line:689
            O00OO0OO0OO00000O =O00OO0OO0OO00000O [1 ]#line:690
            O00000OOO000OOOO0 .axhline (OOO0OO00O0OOO00OO ,color ='r',linestyle ='--',label ='UCL')#line:691
            O00000OOO000OOOO0 .axhline (O0O00000O0O0O0O0O +2 *O00OOOO00OO0OOO0O ,color ='m',linestyle ='--',label ='μ+2σ')#line:692
            O00000OOO000OOOO0 .axhline (O0O00000O0O0O0O0O +O00OOOO00OO0OOO0O ,color ='m',linestyle ='--',label ='μ+σ')#line:693
            O00000OOO000OOOO0 .axhline (O0O00000O0O0O0O0O ,color ='g',linestyle ='--',label ='CL')#line:694
            O00000OOO000OOOO0 .axhline (O0O00000O0O0O0O0O -O00OOOO00OO0OOO0O ,color ='m',linestyle ='--',label ='μ-σ')#line:695
            O00000OOO000OOOO0 .axhline (O0O00000O0O0O0O0O -2 *O00OOOO00OO0OOO0O ,color ='m',linestyle ='--',label ='μ-2σ')#line:696
            O00000OOO000OOOO0 .axhline (OO00000O00O00OO0O ,color ='r',linestyle ='--',label ='LCL')#line:697
            O00000OOO000OOOO0 .axhline (O00OO0OO0OO00000O ,color ='g',linestyle ='-',label ='95CI')#line:698
            OOOO0OO00O0OOOO00 =ttk .Label (OO00000OO0OOOOOOO ,text ="mean="+str (O0O00000O0O0O0O0O )+"; std="+str (O00OOOO00OO0OOO0O )+"; 99.73%:UCL(μ+3σ)="+str (OOO0OO00O0OOO00OO )+"; LCL(μ-3σ)="+str (OO00000O00O00OO0O )+"; 95%CI="+str (O00OO0OO0OO00000O ))#line:699
            OOOO0OO00O0OOOO00 .pack ()#line:700
            O00O0OO0O0OOOO000 =ttk .Label (OO00000OO0OOOOOOO ,text ="68.26%:μ+σ="+str (O0O00000O0O0O0O0O +O00OOOO00OO0OOO0O )+"; 95.45%:μ+2σ="+str (O0O00000O0O0O0O0O +2 *O00OOOO00OO0OOO0O ))#line:702
            O00O0OO0O0OOOO000 .pack ()#line:703
        else :#line:705
            OOO0O0000O0000OO0 =O0OOO00OOOOO00O0O [O00O000O0OOO0OO00 ].astype (float ).values #line:706
            O00O0000OO0OOO0O0 =np .where (OOO0O0000O0000OO0 >0 ,1 ,0 )#line:707
            O0O00O0O0O00OO000 =np .nonzero (O00O0000OO0OOO0O0 )#line:708
            OOO0O0000O0000OO0 =OOO0O0000O0000OO0 [O0O00O0O0O00OO000 ]#line:709
            O0O00000O0O0O0O0O =OOO0O0000O0000OO0 .mean ()#line:710
            O00OOOO00OO0OOO0O =OOO0O0000O0000OO0 .std (ddof =1 )#line:711
            OOO0OO00O0OOO00OO =O0O00000O0O0O0O0O +3 *O00OOOO00OO0OOO0O #line:712
            OO00000O00O00OO0O =O00OOOO00OO0OOO0O -3 *O00OOOO00OO0OOO0O #line:713
            O00000OOO000OOOO0 .axhline (OOO0OO00O0OOO00OO ,color ='r',linestyle ='--',label ='UCL')#line:714
            O00000OOO000OOOO0 .axhline (O0O00000O0O0O0O0O ,color ='g',linestyle ='--',label ='CL')#line:715
            O00000OOO000OOOO0 .axhline (OO00000O00O00OO0O ,color ='r',linestyle ='--',label ='LCL')#line:716
            OOOO0OO00O0OOOO00 =ttk .Label (OO00000OO0OOOOOOO ,text ="mean="+str (O0O00000O0O0O0O0O )+"; std="+str (O00OOOO00OO0OOO0O )+"; UCL(μ+3σ)="+str (OOO0OO00O0OOO00OO )+"; LCL(μ-3σ)="+str (OO00000O00O00OO0O ))#line:717
            OOOO0OO00O0OOOO00 .pack ()#line:718
    O00000OOO000OOOO0 .set_title ("控制图")#line:721
    O00000OOO000OOOO0 .set_xlabel ("项")#line:722
    O0OOOO0000O00O000 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:723
    OOO000O00OOO000OO =O00000OOO000OOOO0 .get_position ()#line:724
    O00000OOO000OOOO0 .set_position ([OOO000O00OOO000OO .x0 ,OOO000O00OOO000OO .y0 ,OOO000O00OOO000OO .width *0.7 ,OOO000O00OOO000OO .height ])#line:725
    O00000OOO000OOOO0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:726
    O0O0O00OO000O0O00 =StringVar ()#line:729
    OOO00OOOOOO000O00 =ttk .Combobox (O0OO00000O0OOOO0O ,width =15 ,textvariable =O0O0O00OO000O0O00 ,state ='readonly')#line:730
    OOO00OOOOOO000O00 ['values']=O00O000O0OOO0OO00 #line:731
    OOO00OOOOOO000O00 .pack (side =LEFT )#line:732
    OOO00OOOOOO000O00 .current (0 )#line:733
    OO0OO0OOO0000O0OO =Button (O0OO00000O0OOOO0O ,text ="控制图（单项-UCL(μ+3σ)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0OOO00OOOOO00O0O ,OO0O00OOOOO0OOOO0 ,[OOO00OO0OO0O000OO for OOO00OO0OO0O000OO in O00O000O0OOO0OO00 if O0O0O00OO000O0O00 .get ()in OOO00OO0OO0O000OO ],O0OO000OO0O0O00OO ,OO0OO00OOO00O0OOO ))#line:743
    OO0OO0OOO0000O0OO .pack (side =LEFT ,anchor ="ne")#line:744
    OO0000OOOO0O00O0O =Button (O0OO00000O0OOOO0O ,text ="控制图（单项-UCL(标准差法)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0OOO00OOOOO00O0O ,OO0O00OOOOO0OOOO0 ,[OOO0O0OOOO0OO000O for OOO0O0OOOO0OO000O in O00O000O0OOO0OO00 if O0O0O00OO000O0O00 .get ()in OOO0O0OOOO0OO000O ],O0OO000OO0O0O00OO ,OO0OO00OOO00O0OOO ,"更多控制线STD"))#line:752
    OO0000OOOO0O00O0O .pack (side =LEFT ,anchor ="ne")#line:753
    OO0000OOOO0O00O0O =Button (O0OO00000O0OOOO0O ,text ="控制图（单项-分位数）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0OOO00OOOOO00O0O ,OO0O00OOOOO0OOOO0 ,[OO0O000OOOO0O0000 for OO0O000OOOO0O0000 in O00O000O0OOO0OO00 if O0O0O00OO000O0O00 .get ()in OO0O000OOOO0O0000 ],O0OO000OO0O0O00OO ,OO0OO00OOO00O0OOO ,"更多控制线分位数"))#line:761
    OO0000OOOO0O00O0O .pack (side =LEFT ,anchor ="ne")#line:762
    OOO0OO0OO000O0O00 =Button (O0OO00000O0OOOO0O ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0OOO00OOOOO00O0O ,OO0O00OOOOO0OOOO0 ,O00O000O0OOO0OO00 ,O0OO000OO0O0O00OO ,0 ))#line:771
    OOO0OO0OO000O0O00 .pack (side =LEFT ,anchor ="ne")#line:773
    OOO00000OOOO0OO0O .draw ()#line:774
def DRAW_make_one (OOOOO0000OO0000OO ,OOO00OOOOOO0OOOO0 ,OO0O0OO000OOOOOO0 ,O0O0O0O0O00OO00OO ,O0OOOO00O0O000OO0 ):#line:778
    ""#line:779
    warnings .filterwarnings ("ignore")#line:780
    OOOO00000OOOOOO00 =Toplevel ()#line:781
    OOOO00000OOOOOO00 .title (OOO00OOOOOO0OOOO0 )#line:782
    O00OOOO0000000OOO =ttk .Frame (OOOO00000OOOOOO00 ,height =20 )#line:783
    O00OOOO0000000OOO .pack (side =TOP )#line:784
    O00O0O0O000O00O00 =Figure (figsize =(12 ,6 ),dpi =100 )#line:786
    OOOO0OOOOO00O0O00 =FigureCanvasTkAgg (O00O0O0O000O00O00 ,master =OOOO00000OOOOOO00 )#line:787
    OOOO0OOOOO00O0O00 .draw ()#line:788
    OOOO0OOOOO00O0O00 .get_tk_widget ().pack (expand =1 )#line:789
    O00O00OOO000O0O00 =O00O0O0O000O00O00 .add_subplot (111 )#line:790
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:792
    plt .rcParams ['axes.unicode_minus']=False #line:793
    O0O000OOOO0OO0000 =NavigationToolbar2Tk (OOOO0OOOOO00O0O00 ,OOOO00000OOOOOO00 )#line:795
    O0O000OOOO0OO0000 .update ()#line:796
    OOOO0OOOOO00O0O00 .get_tk_widget ().pack ()#line:798
    try :#line:801
        OOOOO0OOOO0OOOOOO =OOOOO0000OO0000OO .columns #line:802
        OOOOO0000OO0000OO =OOOOO0000OO0000OO .sort_values (by =O0O0O0O0O00OO00OO ,ascending =[False ],na_position ="last")#line:803
    except :#line:804
        OOO0O0O0OO000O0OO =eval (OOOOO0000OO0000OO )#line:805
        OOO0O0O0OO000O0OO =pd .DataFrame .from_dict (OOO0O0O0OO000O0OO ,orient =OO0O0OO000OOOOOO0 ,columns =[O0O0O0O0O00OO00OO ]).reset_index ()#line:808
        OOOOO0000OO0000OO =OOO0O0O0OO000O0OO .sort_values (by =O0O0O0O0O00OO00OO ,ascending =[False ],na_position ="last")#line:809
    if ("日期"in OOO00OOOOOO0OOOO0 or "时间"in OOO00OOOOOO0OOOO0 or "季度"in OOO00OOOOOO0OOOO0 )and "饼图"not in O0OOOO00O0O000OO0 :#line:813
        OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ]=pd .to_datetime (OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],format ="%Y/%m/%d").dt .date #line:814
        OOOOO0000OO0000OO =OOOOO0000OO0000OO .sort_values (by =OO0O0OO000OOOOOO0 ,ascending =[True ],na_position ="last")#line:815
    elif "批号"in OOO00OOOOOO0OOOO0 :#line:816
        OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ]=OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ].astype (str )#line:817
        OOOOO0000OO0000OO =OOOOO0000OO0000OO .sort_values (by =OO0O0OO000OOOOOO0 ,ascending =[True ],na_position ="last")#line:818
        O00O00OOO000O0O00 .set_xticklabels (OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],rotation =-90 ,fontsize =8 )#line:819
    else :#line:820
        OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ]=OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ].astype (str )#line:821
        O00O00OOO000O0O00 .set_xticklabels (OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],rotation =-90 ,fontsize =8 )#line:822
    O0OOOO000OO0OOO00 =OOOOO0000OO0000OO [O0O0O0O0O00OO00OO ]#line:824
    O0O00OO00OOO00000 =range (0 ,len (O0OOOO000OO0OOO00 ),1 )#line:825
    O00O00OOO000O0O00 .set_title (OOO00OOOOOO0OOOO0 )#line:827
    if O0OOOO00O0O000OO0 =="柱状图":#line:831
        O00O00OOO000O0O00 .bar (x =OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],height =O0OOOO000OO0OOO00 ,width =0.2 ,color ="#87CEFA")#line:832
    elif O0OOOO00O0O000OO0 =="饼图":#line:833
        O00O00OOO000O0O00 .pie (x =O0OOOO000OO0OOO00 ,labels =OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],autopct ="%0.2f%%")#line:834
    elif O0OOOO00O0O000OO0 =="折线图":#line:835
        O00O00OOO000O0O00 .plot (OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],O0OOOO000OO0OOO00 ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:836
    elif "托帕斯图"in str (O0OOOO00O0O000OO0 ):#line:838
        OOO00OOO0O0OOO00O =OOOOO0000OO0000OO [O0O0O0O0O00OO00OO ].fillna (0 )#line:839
        OOO00O0OO0OOOOO00 =OOO00OOO0O0OOO00O .cumsum ()/OOO00OOO0O0OOO00O .sum ()*100 #line:843
        O0O0O0000OOOO0O00 =OOO00O0OO0OOOOO00 [OOO00O0OO0OOOOO00 >0.8 ].index [0 ]#line:845
        OOO000OOO0O0O0OO0 =OOO00OOO0O0OOO00O .index .tolist ().index (O0O0O0000OOOO0O00 )#line:846
        O00O00OOO000O0O00 .bar (x =OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],height =OOO00OOO0O0OOO00O ,color ="C0",label =O0O0O0O0O00OO00OO )#line:850
        O0OOOO00O000OO000 =O00O00OOO000O0O00 .twinx ()#line:851
        O0OOOO00O000OO000 .plot (OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],OOO00O0OO0OOOOO00 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:852
        O0OOOO00O000OO000 .yaxis .set_major_formatter (PercentFormatter ())#line:853
        O00O00OOO000O0O00 .tick_params (axis ="y",colors ="C0")#line:858
        O0OOOO00O000OO000 .tick_params (axis ="y",colors ="C1")#line:859
        if "超级托帕斯图"in str (O0OOOO00O0O000OO0 ):#line:862
            OOO0O00OOOOOO0OO0 =re .compile (r'[(](.*?)[)]',re .S )#line:863
            OOO0OOO0O0000O00O =re .findall (OOO0O00OOOOOO0OO0 ,O0OOOO00O0O000OO0 )[0 ]#line:864
            O00O00OOO000O0O00 .bar (x =OOOOO0000OO0000OO [OO0O0OO000OOOOOO0 ],height =OOOOO0000OO0000OO [OOO0OOO0O0000O00O ],color ="orangered",label =OOO0OOO0O0000O00O )#line:865
    O00O0O0O000O00O00 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:867
    OO00O0OO0OOOOO000 =O00O00OOO000O0O00 .get_position ()#line:868
    O00O00OOO000O0O00 .set_position ([OO00O0OO0OOOOO000 .x0 ,OO00O0OO0OOOOO000 .y0 ,OO00O0OO0OOOOO000 .width *0.7 ,OO00O0OO0OOOOO000 .height ])#line:869
    O00O00OOO000O0O00 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:870
    OOOO0OOOOO00O0O00 .draw ()#line:873
    if len (O0OOOO000OO0OOO00 )<=20 and O0OOOO00O0O000OO0 !="饼图":#line:876
        for O0OOOO0000OO0OO00 ,O00O0OO0O0000000O in zip (O0O00OO00OOO00000 ,O0OOOO000OO0OOO00 ):#line:877
            OOO00OOOOO00000O0 =str (O00O0OO0O0000000O )#line:878
            O000000O00O000OO0 =(O0OOOO0000OO0OO00 ,O00O0OO0O0000000O +0.3 )#line:879
            O00O00OOO000O0O00 .annotate (OOO00OOOOO00000O0 ,xy =O000000O00O000OO0 ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:880
    O000O0O0O0O0O0OOO =Button (O00OOOO0000000OOO ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OOOOO0000OO0000OO ),)#line:890
    O000O0O0O0O0O0OOO .pack (side =RIGHT )#line:891
    O00OO0O00OOOOOOO0 =Button (O00OOOO0000000OOO ,relief =GROOVE ,text ="查看原始数据",command =lambda :TOOLS_view_dict (OOOOO0000OO0000OO ,0 ))#line:895
    O00OO0O00OOOOOOO0 .pack (side =RIGHT )#line:896
    OOO0OOOO00OOO0O0O =Button (O00OOOO0000000OOO ,relief =GROOVE ,text ="饼图",command =lambda :DRAW_make_one (OOOOO0000OO0000OO ,OOO00OOOOOO0OOOO0 ,OO0O0OO000OOOOOO0 ,O0O0O0O0O00OO00OO ,"饼图"),)#line:904
    OOO0OOOO00OOO0O0O .pack (side =LEFT )#line:905
    OOO0OOOO00OOO0O0O =Button (O00OOOO0000000OOO ,relief =GROOVE ,text ="柱状图",command =lambda :DRAW_make_one (OOOOO0000OO0000OO ,OOO00OOOOOO0OOOO0 ,OO0O0OO000OOOOOO0 ,O0O0O0O0O00OO00OO ,"柱状图"),)#line:912
    OOO0OOOO00OOO0O0O .pack (side =LEFT )#line:913
    OOO0OOOO00OOO0O0O =Button (O00OOOO0000000OOO ,relief =GROOVE ,text ="折线图",command =lambda :DRAW_make_one (OOOOO0000OO0000OO ,OOO00OOOOOO0OOOO0 ,OO0O0OO000OOOOOO0 ,O0O0O0O0O00OO00OO ,"折线图"),)#line:919
    OOO0OOOO00OOO0O0O .pack (side =LEFT )#line:920
    OOO0OOOO00OOO0O0O =Button (O00OOOO0000000OOO ,relief =GROOVE ,text ="托帕斯图",command =lambda :DRAW_make_one (OOOOO0000OO0000OO ,OOO00OOOOOO0OOOO0 ,OO0O0OO000OOOOOO0 ,O0O0O0O0O00OO00OO ,"托帕斯图"),)#line:927
    OOO0OOOO00OOO0O0O .pack (side =LEFT )#line:928
def DRAW_make_mutibar (O0O000O00OOOOOOOO ,O0OOOO00OO0OOOO00 ,O0O0OO00000OOO0OO ,O000OO0OOO00OOO0O ,OO0OOOOO0O0O000OO ,OOO0OO00O00OOOO0O ,OOOOOOO00O0OOO000 ):#line:929
    ""#line:930
    O0000OO00O00OO00O =Toplevel ()#line:931
    O0000OO00O00OO00O .title (OOOOOOO00O0OOO000 )#line:932
    O0O0OOO0OO00O0O00 =ttk .Frame (O0000OO00O00OO00O ,height =20 )#line:933
    O0O0OOO0OO00O0O00 .pack (side =TOP )#line:934
    O000000OO00O0OOOO =0.2 #line:936
    O00OO00OOO0000O0O =Figure (figsize =(12 ,6 ),dpi =100 )#line:937
    OOO00OOOO00O0000O =FigureCanvasTkAgg (O00OO00OOO0000O0O ,master =O0000OO00O00OO00O )#line:938
    OOO00OOOO00O0000O .draw ()#line:939
    OOO00OOOO00O0000O .get_tk_widget ().pack (expand =1 )#line:940
    O0OOO0O0O0OOOO0O0 =O00OO00OOO0000O0O .add_subplot (111 )#line:941
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:943
    plt .rcParams ['axes.unicode_minus']=False #line:944
    O00OO0000O0OO0O0O =NavigationToolbar2Tk (OOO00OOOO00O0000O ,O0000OO00O00OO00O )#line:946
    O00OO0000O0OO0O0O .update ()#line:947
    OOO00OOOO00O0000O .get_tk_widget ().pack ()#line:949
    O0OOOO00OO0OOOO00 =O0O000O00OOOOOOOO [O0OOOO00OO0OOOO00 ]#line:950
    O0O0OO00000OOO0OO =O0O000O00OOOOOOOO [O0O0OO00000OOO0OO ]#line:951
    O000OO0OOO00OOO0O =O0O000O00OOOOOOOO [O000OO0OOO00OOO0O ]#line:952
    OOO0OOO000O00O00O =range (0 ,len (O0OOOO00OO0OOOO00 ),1 )#line:954
    O0OOO0O0O0OOOO0O0 .set_xticklabels (O000OO0OOO00OOO0O ,rotation =-90 ,fontsize =8 )#line:955
    O0OOO0O0O0OOOO0O0 .bar (OOO0OOO000O00O00O ,O0OOOO00OO0OOOO00 ,align ="center",tick_label =O000OO0OOO00OOO0O ,label =OO0OOOOO0O0O000OO )#line:958
    O0OOO0O0O0OOOO0O0 .bar (OOO0OOO000O00O00O ,O0O0OO00000OOO0OO ,align ="center",label =OOO0OO00O00OOOO0O )#line:961
    O0OOO0O0O0OOOO0O0 .set_title (OOOOOOO00O0OOO000 )#line:962
    O0OOO0O0O0OOOO0O0 .set_xlabel ("项")#line:963
    O0OOO0O0O0OOOO0O0 .set_ylabel ("数量")#line:964
    O00OO00OOO0000O0O .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:966
    O0OOOOO0O00OOOOO0 =O0OOO0O0O0OOOO0O0 .get_position ()#line:967
    O0OOO0O0O0OOOO0O0 .set_position ([O0OOOOO0O00OOOOO0 .x0 ,O0OOOOO0O00OOOOO0 .y0 ,O0OOOOO0O00OOOOO0 .width *0.7 ,O0OOOOO0O00OOOOO0 .height ])#line:968
    O0OOO0O0O0OOOO0O0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:969
    OOO00OOOO00O0000O .draw ()#line:971
    OOOO0OOO0O00000OO =Button (O0O0OOO0OO00O0O00 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O0O000O00OOOOOOOO ),)#line:978
    OOOO0OOO0O00000OO .pack (side =RIGHT )#line:979
def CLEAN_hzp (OOOO0OO00000OO00O ):#line:984
    ""#line:985
    if "报告编码"not in OOOO0OO00000OO00O .columns :#line:986
            OOOO0OO00000OO00O ["特殊化妆品注册证书编号/普通化妆品备案编号"]=OOOO0OO00000OO00O ["特殊化妆品注册证书编号/普通化妆品备案编号"].fillna ("-未填写-")#line:987
            OOOO0OO00000OO00O ["省级评价结果"]=OOOO0OO00000OO00O ["省级评价结果"].fillna ("-未填写-")#line:988
            OOOO0OO00000OO00O ["生产企业"]=OOOO0OO00000OO00O ["生产企业"].fillna ("-未填写-")#line:989
            OOOO0OO00000OO00O ["提交人"]="不适用"#line:990
            OOOO0OO00000OO00O ["医疗机构类别"]="不适用"#line:991
            OOOO0OO00000OO00O ["经营企业或使用单位"]="不适用"#line:992
            OOOO0OO00000OO00O ["报告状态"]="报告单位评价"#line:993
            OOOO0OO00000OO00O ["所属地区"]="不适用"#line:994
            OOOO0OO00000OO00O ["医院名称"]="不适用"#line:995
            OOOO0OO00000OO00O ["报告地区名称"]="不适用"#line:996
            OOOO0OO00000OO00O ["提交人"]="不适用"#line:997
            OOOO0OO00000OO00O ["型号"]=OOOO0OO00000OO00O ["化妆品分类"]#line:998
            OOOO0OO00000OO00O ["关联性评价"]=OOOO0OO00000OO00O ["上报单位评价结果"]#line:999
            OOOO0OO00000OO00O ["规格"]="不适用"#line:1000
            OOOO0OO00000OO00O ["器械故障表现"]=OOOO0OO00000OO00O ["初步判断"]#line:1001
            OOOO0OO00000OO00O ["伤害表现"]=OOOO0OO00000OO00O ["自觉症状"]+OOOO0OO00000OO00O ["皮损部位"]+OOOO0OO00000OO00O ["皮损形态"]#line:1002
            OOOO0OO00000OO00O ["事件原因分析"]="不适用"#line:1003
            OOOO0OO00000OO00O ["事件原因分析描述"]="不适用"#line:1004
            OOOO0OO00000OO00O ["调查情况"]="不适用"#line:1005
            OOOO0OO00000OO00O ["具体控制措施"]="不适用"#line:1006
            OOOO0OO00000OO00O ["未采取控制措施原因"]="不适用"#line:1007
            OOOO0OO00000OO00O ["报告地区名称"]="不适用"#line:1008
            OOOO0OO00000OO00O ["上报单位所属地区"]="不适用"#line:1009
            OOOO0OO00000OO00O ["持有人报告状态"]="不适用"#line:1010
            OOOO0OO00000OO00O ["年龄类型"]="岁"#line:1011
            OOOO0OO00000OO00O ["经营企业使用单位报告状态"]="不适用"#line:1012
            OOOO0OO00000OO00O ["产品归属"]="化妆品"#line:1013
            OOOO0OO00000OO00O ["管理类别"]="不适用"#line:1014
            OOOO0OO00000OO00O ["超时标记"]="不适用"#line:1015
            OOOO0OO00000OO00O =OOOO0OO00000OO00O .rename (columns ={"报告表编号":"报告编码","报告类型":"伤害","报告地区":"监测机构","报告单位名称":"单位名称","患者/消费者姓名":"姓名","不良反应发生日期":"事件发生日期","过程描述补充说明":"使用过程","化妆品名称":"产品名称","化妆品分类":"产品类别","生产企业":"上市许可持有人名称","生产批号":"产品批号","特殊化妆品注册证书编号/普通化妆品备案编号":"注册证编号/曾用注册证编号",})#line:1034
            OOOO0OO00000OO00O ["时隔"]=pd .to_datetime (OOOO0OO00000OO00O ["事件发生日期"])-pd .to_datetime (OOOO0OO00000OO00O ["开始使用日期"])#line:1035
            OOOO0OO00000OO00O .loc [(OOOO0OO00000OO00O ["省级评价结果"]!="-未填写-"),"有效报告"]=1 #line:1036
            OOOO0OO00000OO00O ["伤害"]=OOOO0OO00000OO00O ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:1037
            try :#line:1038
	            OOOO0OO00000OO00O =TOOL_guizheng (OOOO0OO00000OO00O ,4 ,True )#line:1039
            except :#line:1040
                pass #line:1041
            return OOOO0OO00000OO00O #line:1042
def CLEAN_yp (OOOOO0OOOOOO0O00O ):#line:1047
    ""#line:1048
    if "报告编码"not in OOOOO0OOOOOO0O00O .columns :#line:1049
        if "反馈码"in OOOOO0OOOOOO0O00O .columns and "报告表编码"not in OOOOO0OOOOOO0O00O .columns :#line:1051
            OOOOO0OOOOOO0O00O ["提交人"]="不适用"#line:1053
            OOOOO0OOOOOO0O00O ["经营企业或使用单位"]="不适用"#line:1054
            OOOOO0OOOOOO0O00O ["报告状态"]="报告单位评价"#line:1055
            OOOOO0OOOOOO0O00O ["所属地区"]="不适用"#line:1056
            OOOOO0OOOOOO0O00O ["产品类别"]="无源"#line:1057
            OOOOO0OOOOOO0O00O ["医院名称"]="不适用"#line:1058
            OOOOO0OOOOOO0O00O ["报告地区名称"]="不适用"#line:1059
            OOOOO0OOOOOO0O00O ["提交人"]="不适用"#line:1060
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"反馈码":"报告表编码","序号":"药品序号","新的":"报告类型-新的","报告类型":"报告类型-严重程度","用药-日数":"用法-日","用药-次数":"用法-次",})#line:1073
        if "唯一标识"not in OOOOO0OOOOOO0O00O .columns :#line:1078
            OOOOO0OOOOOO0O00O ["报告编码"]=OOOOO0OOOOOO0O00O ["报告表编码"].astype (str )+OOOOO0OOOOOO0O00O ["患者姓名"].astype (str )#line:1079
        if "唯一标识"in OOOOO0OOOOOO0O00O .columns :#line:1080
            OOOOO0OOOOOO0O00O ["唯一标识"]=OOOOO0OOOOOO0O00O ["唯一标识"].astype (str )#line:1081
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"唯一标识":"报告编码"})#line:1082
        if "医疗机构类别"not in OOOOO0OOOOOO0O00O .columns :#line:1083
            OOOOO0OOOOOO0O00O ["医疗机构类别"]="医疗机构"#line:1084
            OOOOO0OOOOOO0O00O ["经营企业使用单位报告状态"]="已提交"#line:1085
        try :#line:1086
            OOOOO0OOOOOO0O00O ["年龄和单位"]=OOOOO0OOOOOO0O00O ["年龄"].astype (str )+OOOOO0OOOOOO0O00O ["年龄单位"]#line:1087
        except :#line:1088
            OOOOO0OOOOOO0O00O ["年龄和单位"]=OOOOO0OOOOOO0O00O ["年龄"].astype (str )+OOOOO0OOOOOO0O00O ["年龄类型"]#line:1089
        OOOOO0OOOOOO0O00O .loc [(OOOOO0OOOOOO0O00O ["报告类型-新的"]=="新的"),"管理类别"]="Ⅲ类"#line:1090
        OOOOO0OOOOOO0O00O .loc [(OOOOO0OOOOOO0O00O ["报告类型-严重程度"]=="严重"),"管理类别"]="Ⅲ类"#line:1091
        text .insert (END ,"剔除已删除报告和重复报告...")#line:1092
        if "删除标识"in OOOOO0OOOOOO0O00O .columns :#line:1093
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O [(OOOOO0OOOOOO0O00O ["删除标识"]!="删除")]#line:1094
        if "重复报告"in OOOOO0OOOOOO0O00O .columns :#line:1095
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O [(OOOOO0OOOOOO0O00O ["重复报告"]!="重复报告")]#line:1096
        OOOOO0OOOOOO0O00O ["报告类型-新的"]=OOOOO0OOOOOO0O00O ["报告类型-新的"].fillna (" ")#line:1099
        OOOOO0OOOOOO0O00O .loc [(OOOOO0OOOOOO0O00O ["报告类型-严重程度"]=="严重"),"伤害"]="严重伤害"#line:1100
        OOOOO0OOOOOO0O00O ["伤害"]=OOOOO0OOOOOO0O00O ["伤害"].fillna ("所有一般")#line:1101
        OOOOO0OOOOOO0O00O ["伤害PSUR"]=OOOOO0OOOOOO0O00O ["报告类型-新的"].astype (str )+OOOOO0OOOOOO0O00O ["报告类型-严重程度"].astype (str )#line:1102
        OOOOO0OOOOOO0O00O ["用量用量单位"]=OOOOO0OOOOOO0O00O ["用量"].astype (str )+OOOOO0OOOOOO0O00O ["用量单位"].astype (str )#line:1103
        OOOOO0OOOOOO0O00O ["规格"]="不适用"#line:1105
        OOOOO0OOOOOO0O00O ["事件原因分析"]="不适用"#line:1106
        OOOOO0OOOOOO0O00O ["事件原因分析描述"]="不适用"#line:1107
        OOOOO0OOOOOO0O00O ["初步处置情况"]="不适用"#line:1108
        OOOOO0OOOOOO0O00O ["伤害表现"]=OOOOO0OOOOOO0O00O ["不良反应名称"]#line:1109
        OOOOO0OOOOOO0O00O ["产品类别"]="无源"#line:1110
        OOOOO0OOOOOO0O00O ["调查情况"]="不适用"#line:1111
        OOOOO0OOOOOO0O00O ["具体控制措施"]="不适用"#line:1112
        OOOOO0OOOOOO0O00O ["上报单位所属地区"]=OOOOO0OOOOOO0O00O ["报告地区名称"]#line:1113
        OOOOO0OOOOOO0O00O ["未采取控制措施原因"]="不适用"#line:1114
        OOOOO0OOOOOO0O00O ["报告单位评价"]=OOOOO0OOOOOO0O00O ["报告类型-新的"].astype (str )+OOOOO0OOOOOO0O00O ["报告类型-严重程度"].astype (str )#line:1115
        OOOOO0OOOOOO0O00O .loc [(OOOOO0OOOOOO0O00O ["报告类型-新的"]=="新的"),"持有人报告状态"]="待评价"#line:1116
        OOOOO0OOOOOO0O00O ["用法temp日"]="日"#line:1117
        OOOOO0OOOOOO0O00O ["用法temp次"]="次"#line:1118
        OOOOO0OOOOOO0O00O ["用药频率"]=(OOOOO0OOOOOO0O00O ["用法-日"].astype (str )+OOOOO0OOOOOO0O00O ["用法temp日"]+OOOOO0OOOOOO0O00O ["用法-次"].astype (str )+OOOOO0OOOOOO0O00O ["用法temp次"])#line:1124
        try :#line:1125
            OOOOO0OOOOOO0O00O ["相关疾病信息[疾病名称]-术语"]=OOOOO0OOOOOO0O00O ["原患疾病"]#line:1126
            OOOOO0OOOOOO0O00O ["治疗适应症-术语"]=OOOOO0OOOOOO0O00O ["用药原因"]#line:1127
        except :#line:1128
            pass #line:1129
        try :#line:1131
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"提交日期":"报告日期"})#line:1132
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"提交人":"报告人"})#line:1133
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"报告状态":"持有人报告状态"})#line:1134
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"所属地区":"使用单位、经营企业所属监测机构"})#line:1135
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"医院名称":"单位名称"})#line:1136
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"批准文号":"注册证编号/曾用注册证编号"})#line:1137
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"通用名称":"产品名称"})#line:1138
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"生产厂家":"上市许可持有人名称"})#line:1139
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"不良反应发生时间":"事件发生日期"})#line:1140
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"不良反应名称":"器械故障表现"})#line:1141
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"不良反应过程描述":"使用过程"})#line:1142
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"生产批号":"产品批号"})#line:1143
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"报告地区名称":"使用单位、经营企业所属监测机构"})#line:1144
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"剂型":"型号"})#line:1145
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"报告人评价":"关联性评价"})#line:1146
            OOOOO0OOOOOO0O00O =OOOOO0OOOOOO0O00O .rename (columns ={"年龄单位":"年龄类型"})#line:1147
        except :#line:1148
            text .insert (END ,"数据规整失败。")#line:1149
            return 0 #line:1150
        OOOOO0OOOOOO0O00O ['报告日期']=OOOOO0OOOOOO0O00O ['报告日期'].str .strip ()#line:1153
        OOOOO0OOOOOO0O00O ['事件发生日期']=OOOOO0OOOOOO0O00O ['事件发生日期'].str .strip ()#line:1154
        OOOOO0OOOOOO0O00O ['用药开始时间']=OOOOO0OOOOOO0O00O ['用药开始时间'].str .strip ()#line:1155
        return OOOOO0OOOOOO0O00O #line:1157
    if "报告编码"in OOOOO0OOOOOO0O00O .columns :#line:1158
        return OOOOO0OOOOOO0O00O #line:1159
def CLEAN_qx (OO0OO0000O0O00000 ):#line:1161
		""#line:1162
		if "使用单位、经营企业所属监测机构"not in OO0OO0000O0O00000 .columns and "监测机构"not in OO0OO0000O0O00000 .columns :#line:1164
			OO0OO0000O0O00000 ["使用单位、经营企业所属监测机构"]="本地"#line:1165
		if "上市许可持有人名称"not in OO0OO0000O0O00000 .columns :#line:1166
			OO0OO0000O0O00000 ["上市许可持有人名称"]=OO0OO0000O0O00000 ["单位名称"]#line:1167
		if "注册证编号/曾用注册证编号"not in OO0OO0000O0O00000 .columns :#line:1168
			OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号"]#line:1169
		if "事件原因分析描述"not in OO0OO0000O0O00000 .columns :#line:1170
			OO0OO0000O0O00000 ["事件原因分析描述"]="  "#line:1171
		if "初步处置情况"not in OO0OO0000O0O00000 .columns :#line:1172
			OO0OO0000O0O00000 ["初步处置情况"]="  "#line:1173
		text .insert (END ,"\n正在执行格式规整和增加有关时间、年龄、性别等统计列...")#line:1176
		OO0OO0000O0O00000 =OO0OO0000O0O00000 .rename (columns ={"使用单位、经营企业所属监测机构":"监测机构"})#line:1177
		OO0OO0000O0O00000 ["报告编码"]=OO0OO0000O0O00000 ["报告编码"].astype ("str")#line:1178
		OO0OO0000O0O00000 ["产品批号"]=OO0OO0000O0O00000 ["产品批号"].astype ("str")#line:1179
		OO0OO0000O0O00000 ["型号"]=OO0OO0000O0O00000 ["型号"].astype ("str")#line:1180
		OO0OO0000O0O00000 ["规格"]=OO0OO0000O0O00000 ["规格"].astype ("str")#line:1181
		OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1182
		OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1183
		OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1184
		OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1185
		OO0OO0000O0O00000 ["产品名称"]=OO0OO0000O0O00000 ["产品名称"].str .replace ("*","※",regex =False )#line:1186
		OO0OO0000O0O00000 ["产品批号"]=OO0OO0000O0O00000 ["产品批号"].str .replace ("(","（",regex =False )#line:1187
		OO0OO0000O0O00000 ["产品批号"]=OO0OO0000O0O00000 ["产品批号"].str .replace (")","）",regex =False )#line:1188
		OO0OO0000O0O00000 ["产品批号"]=OO0OO0000O0O00000 ["产品批号"].str .replace ("*","※",regex =False )#line:1189
		OO0OO0000O0O00000 ["上市许可持有人名称"]=OO0OO0000O0O00000 ["上市许可持有人名称"].fillna ("-未填写-")#line:1193
		OO0OO0000O0O00000 ["产品类别"]=OO0OO0000O0O00000 ["产品类别"].fillna ("-未填写-")#line:1194
		OO0OO0000O0O00000 ["产品名称"]=OO0OO0000O0O00000 ["产品名称"].fillna ("-未填写-")#line:1195
		OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1196
		OO0OO0000O0O00000 ["产品批号"]=OO0OO0000O0O00000 ["产品批号"].fillna ("-未填写-")#line:1197
		OO0OO0000O0O00000 ["型号"]=OO0OO0000O0O00000 ["型号"].fillna ("-未填写-")#line:1198
		OO0OO0000O0O00000 ["规格"]=OO0OO0000O0O00000 ["规格"].fillna ("-未填写-")#line:1199
		OO0OO0000O0O00000 ["伤害与评价"]=OO0OO0000O0O00000 ["伤害"]+OO0OO0000O0O00000 ["持有人报告状态"]#line:1202
		OO0OO0000O0O00000 ["注册证备份"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]#line:1203
		OO0OO0000O0O00000 ['报告日期']=pd .to_datetime (OO0OO0000O0O00000 ['报告日期'],format ='%Y-%m-%d',errors ='coerce')#line:1206
		OO0OO0000O0O00000 ['事件发生日期']=pd .to_datetime (OO0OO0000O0O00000 ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1207
		OO0OO0000O0O00000 ["报告月份"]=OO0OO0000O0O00000 ["报告日期"].dt .to_period ("M").astype (str )#line:1209
		OO0OO0000O0O00000 ["报告季度"]=OO0OO0000O0O00000 ["报告日期"].dt .to_period ("Q").astype (str )#line:1210
		OO0OO0000O0O00000 ["报告年份"]=OO0OO0000O0O00000 ["报告日期"].dt .to_period ("Y").astype (str )#line:1211
		OO0OO0000O0O00000 ["事件发生月份"]=OO0OO0000O0O00000 ["事件发生日期"].dt .to_period ("M").astype (str )#line:1212
		OO0OO0000O0O00000 ["事件发生季度"]=OO0OO0000O0O00000 ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1213
		OO0OO0000O0O00000 ["事件发生年份"]=OO0OO0000O0O00000 ["事件发生日期"].dt .to_period ("Y").astype (str )#line:1214
		if ini ["模式"]=="器械":#line:1218
			OO0OO0000O0O00000 ['发现或获知日期']=pd .to_datetime (OO0OO0000O0O00000 ['发现或获知日期'],format ='%Y-%m-%d',errors ='coerce')#line:1219
			OO0OO0000O0O00000 ["时隔"]=pd .to_datetime (OO0OO0000O0O00000 ["发现或获知日期"])-pd .to_datetime (OO0OO0000O0O00000 ["事件发生日期"])#line:1220
			OO0OO0000O0O00000 ["报告时限"]=pd .to_datetime (OO0OO0000O0O00000 ["报告日期"])-pd .to_datetime (OO0OO0000O0O00000 ["发现或获知日期"])#line:1221
			OO0OO0000O0O00000 ["报告时限"]=OO0OO0000O0O00000 ["报告时限"].dt .days #line:1222
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>20 )&(OO0OO0000O0O00000 ["伤害"]=="严重伤害"),"超时标记"]=1 #line:1223
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>30 )&(OO0OO0000O0O00000 ["伤害"]=="其他"),"超时标记"]=1 #line:1224
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>7 )&(OO0OO0000O0O00000 ["伤害"]=="死亡"),"超时标记"]=1 #line:1225
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["经营企业使用单位报告状态"]=="审核通过"),"有效报告"]=1 #line:1227
		if ini ["模式"]=="药品":#line:1230
			OO0OO0000O0O00000 ['用药开始时间']=pd .to_datetime (OO0OO0000O0O00000 ['用药开始时间'],format ='%Y-%m-%d',errors ='coerce')#line:1231
			OO0OO0000O0O00000 ["时隔"]=pd .to_datetime (OO0OO0000O0O00000 ["事件发生日期"])-pd .to_datetime (OO0OO0000O0O00000 ["用药开始时间"])#line:1232
			OO0OO0000O0O00000 ["报告时限"]=pd .to_datetime (OO0OO0000O0O00000 ["报告日期"])-pd .to_datetime (OO0OO0000O0O00000 ["事件发生日期"])#line:1233
			OO0OO0000O0O00000 ["报告时限"]=OO0OO0000O0O00000 ["报告时限"].dt .days #line:1234
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>15 )&(OO0OO0000O0O00000 ["报告类型-严重程度"]=="严重"),"超时标记"]=1 #line:1235
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>30 )&(OO0OO0000O0O00000 ["报告类型-严重程度"]=="一般"),"超时标记"]=1 #line:1236
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>15 )&(OO0OO0000O0O00000 ["报告类型-新的"]=="新的"),"超时标记"]=1 #line:1237
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["报告时限"]>1 )&(OO0OO0000O0O00000 ["报告类型-严重程度"]=="死亡"),"超时标记"]=1 #line:1238
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["评价状态"]!="未评价"),"有效报告"]=1 #line:1240
		OO0OO0000O0O00000 .loc [((OO0OO0000O0O00000 ["年龄"]=="未填写")|OO0OO0000O0O00000 ["年龄"].isnull ()),"年龄"]=-1 #line:1242
		OO0OO0000O0O00000 ["年龄"]=OO0OO0000O0O00000 ["年龄"].astype (float )#line:1243
		OO0OO0000O0O00000 ["年龄"]=OO0OO0000O0O00000 ["年龄"].fillna (-1 )#line:1244
		OO0OO0000O0O00000 ["性别"]=OO0OO0000O0O00000 ["性别"].fillna ("未填写")#line:1245
		OO0OO0000O0O00000 ["年龄段"]="未填写"#line:1246
		try :#line:1247
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄类型"]=="月"),"年龄"]=OO0OO0000O0O00000 ["年龄"].values /12 #line:1248
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄类型"]=="月"),"年龄类型"]="岁"#line:1249
		except :#line:1250
			pass #line:1251
		try :#line:1252
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄类型"]=="天"),"年龄"]=OO0OO0000O0O00000 ["年龄"].values /365 #line:1253
			OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄类型"]=="天"),"年龄类型"]="岁"#line:1254
		except :#line:1255
			pass #line:1256
		OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄"].values <=4 ),"年龄段"]="0-婴幼儿（0-4）"#line:1257
		OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄"].values >=5 ),"年龄段"]="1-少儿（5-14）"#line:1258
		OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄"].values >=15 ),"年龄段"]="2-青壮年（15-44）"#line:1259
		OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄"].values >=45 ),"年龄段"]="3-中年期（45-64）"#line:1260
		OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄"].values >=65 ),"年龄段"]="4-老年期（≥65）"#line:1261
		OO0OO0000O0O00000 .loc [(OO0OO0000O0O00000 ["年龄"].values ==-1 ),"年龄段"]="未填写"#line:1262
		OO0OO0000O0O00000 ["规整后品类"]="N"#line:1266
		OO0OO0000O0O00000 =TOOL_guizheng (OO0OO0000O0O00000 ,2 ,True )#line:1267
		if ini ['模式']in ["器械"]:#line:1270
			OO0OO0000O0O00000 =TOOL_guizheng (OO0OO0000O0O00000 ,3 ,True )#line:1271
		OO0OO0000O0O00000 =TOOL_guizheng (OO0OO0000O0O00000 ,"课题",True )#line:1275
		try :#line:1277
			OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"]=OO0OO0000O0O00000 ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1278
		except :#line:1279
			pass #line:1280
		OO0OO0000O0O00000 ["数据清洗完成标记"]="是"#line:1282
		OOOOOOO0OOOO0000O =OO0OO0000O0O00000 .loc [:]#line:1283
		return OO0OO0000O0O00000 #line:1284
def TOOLS_fileopen ():#line:1290
    ""#line:1291
    warnings .filterwarnings ('ignore')#line:1292
    O0000000O0O000000 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1293
    OOOOO0O0O00000OOO =Useful_tools_openfiles (O0000000O0O000000 ,0 )#line:1294
    try :#line:1295
        OOOOO0O0O00000OOO =OOOOO0O0O00000OOO .loc [:,~OOOOO0O0O00000OOO .columns .str .contains ("^Unnamed")]#line:1296
    except :#line:1297
        pass #line:1298
    ini ["模式"]="其他"#line:1300
    OO000OOOOOOO00O00 =OOOOO0O0O00000OOO #line:1301
    TABLE_tree_Level_2 (OO000OOOOOOO00O00 ,0 ,OO000OOOOOOO00O00 )#line:1302
def TOOLS_pinzhong (O00OOOOO0O000O000 ):#line:1305
    ""#line:1306
    O00OOOOO0O000O000 ["患者姓名"]=O00OOOOO0O000O000 ["报告表编码"]#line:1307
    O00OOOOO0O000O000 ["用量"]=O00OOOOO0O000O000 ["用法用量"]#line:1308
    O00OOOOO0O000O000 ["评价状态"]=O00OOOOO0O000O000 ["报告单位评价"]#line:1309
    O00OOOOO0O000O000 ["用量单位"]=""#line:1310
    O00OOOOO0O000O000 ["单位名称"]="不适用"#line:1311
    O00OOOOO0O000O000 ["报告地区名称"]="不适用"#line:1312
    O00OOOOO0O000O000 ["用法-日"]="不适用"#line:1313
    O00OOOOO0O000O000 ["用法-次"]="不适用"#line:1314
    O00OOOOO0O000O000 ["不良反应发生时间"]=O00OOOOO0O000O000 ["不良反应发生时间"].str [0 :10 ]#line:1315
    O00OOOOO0O000O000 ["持有人报告状态"]="待评价"#line:1317
    O00OOOOO0O000O000 =O00OOOOO0O000O000 .rename (columns ={"是否非预期":"报告类型-新的","不良反应-术语":"不良反应名称","持有人/生产厂家":"上市许可持有人名称"})#line:1322
    return O00OOOOO0O000O000 #line:1323
def Useful_tools_openfiles (OOO0OOO0OOOOOOO0O ,OOOO000OO0O00000O ):#line:1328
    ""#line:1329
    OO0O0O0OOO00000OO =[pd .read_excel (OO000O0O000O00OO0 ,header =0 ,sheet_name =OOOO000OO0O00000O )for OO000O0O000O00OO0 in OOO0OOO0OOOOOOO0O ]#line:1330
    O0O0O0OOO0000O000 =pd .concat (OO0O0O0OOO00000OO ,ignore_index =True ).drop_duplicates ()#line:1331
    return O0O0O0OOO0000O000 #line:1332
def TOOLS_allfileopen ():#line:1334
    ""#line:1335
    global ori #line:1336
    global ini #line:1337
    global data #line:1338
    ini ["原始模式"]="否"#line:1339
    warnings .filterwarnings ('ignore')#line:1340
    OO0O000OOO0000OOO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1342
    ori =Useful_tools_openfiles (OO0O000OOO0000OOO ,0 )#line:1343
    try :#line:1347
        O0OOOO0OO0000OOO0 =Useful_tools_openfiles (OO0O000OOO0000OOO ,"报告信息")#line:1348
        if "是否非预期"in O0OOOO0OO0000OOO0 .columns :#line:1349
            ori =TOOLS_pinzhong (O0OOOO0OO0000OOO0 )#line:1350
    except :#line:1351
        pass #line:1352
    ini ["模式"]="其他"#line:1354
    try :#line:1356
        ori =Useful_tools_openfiles (OO0O000OOO0000OOO ,"字典数据")#line:1357
        ini ["原始模式"]="是"#line:1358
        if "UDI"in ori .columns :#line:1359
            ini ["模式"]="器械"#line:1360
            data =ori #line:1361
        if "报告类型-新的"in ori .columns :#line:1362
            ini ["模式"]="药品"#line:1363
            data =ori #line:1364
        else :#line:1365
            ini ["模式"]="其他"#line:1366
    except :#line:1367
        pass #line:1368
    try :#line:1371
        ori =ori .loc [:,~ori .columns .str .contains ("^Unnamed")]#line:1372
    except :#line:1373
        pass #line:1374
    if "UDI"in ori .columns and ini ["原始模式"]!="是":#line:1378
        text .insert (END ,"识别出为器械报表,正在进行数据规整...")#line:1379
        ini ["模式"]="器械"#line:1380
        ori =CLEAN_qx (ori )#line:1381
        data =ori #line:1382
    if "报告类型-新的"in ori .columns and ini ["原始模式"]!="是":#line:1383
        text .insert (END ,"识别出为药品报表,正在进行数据规整...")#line:1384
        ini ["模式"]="药品"#line:1385
        ori =CLEAN_yp (ori )#line:1386
        ori =CLEAN_qx (ori )#line:1387
        data =ori #line:1388
    if "光斑贴试验"in ori .columns and ini ["原始模式"]!="是":#line:1389
        text .insert (END ,"识别出为化妆品报表,正在进行数据规整...")#line:1390
        ini ["模式"]="化妆品"#line:1391
        ori =CLEAN_hzp (ori )#line:1392
        ori =CLEAN_qx (ori )#line:1393
        data =ori #line:1394
    if ini ["模式"]=="其他":#line:1397
        text .insert (END ,"\n数据读取成功，行数："+str (len (ori )))#line:1398
        data =ori #line:1399
        O0O0O0OO0O0O000OO =Menu (root )#line:1400
        root .config (menu =O0O0O0OO0O0O000OO )#line:1401
        try :#line:1402
            ini ["button"][0 ].pack_forget ()#line:1403
            ini ["button"][1 ].pack_forget ()#line:1404
            ini ["button"][2 ].pack_forget ()#line:1405
            ini ["button"][3 ].pack_forget ()#line:1406
            ini ["button"][4 ].pack_forget ()#line:1407
        except :#line:1408
            pass #line:1409
    else :#line:1411
        ini ["清洗后的文件"]=data #line:1412
        ini ["证号"]=Countall (data ).df_zhenghao ()#line:1413
        text .insert (END ,"\n数据读取成功，行数："+str (len (data )))#line:1414
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1415
        try :#line:1416
            ini ["button"][0 ].pack_forget ()#line:1417
            ini ["button"][1 ].pack_forget ()#line:1418
            ini ["button"][2 ].pack_forget ()#line:1419
            ini ["button"][3 ].pack_forget ()#line:1420
            ini ["button"][4 ].pack_forget ()#line:1421
        except :#line:1422
            pass #line:1423
        OO00OO000O0OOOOOO =Button (frame0 ,text ="地市统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("市级监测机构"),1 ,ori ),)#line:1434
        OO00OO000O0OOOOOO .pack ()#line:1435
        O0O0OOOOOOO0OO00O =Button (frame0 ,text ="县区统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("监测机构"),1 ,ori ),)#line:1448
        O0O0OOOOOOO0OO00O .pack ()#line:1449
        OOOO0OO0OOO0OO0O0 =Button (frame0 ,text ="上报单位",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_user (),1 ,ori ),)#line:1462
        OOOO0OO0OOO0OO0O0 .pack ()#line:1463
        OOOO0OOO00OOO00O0 =Button (frame0 ,text ="生产企业",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_chiyouren (),1 ,ori ),)#line:1474
        OOOO0OOO00OOO00O0 .pack ()#line:1475
        OOOOOO000OOO0OO00 =Button (frame0 ,text ="产品统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ini ["证号"],1 ,ori ,ori ,"dfx_zhenghao"),)#line:1486
        OOOOOO000OOO0OO00 .pack ()#line:1487
        ini ["button"]=[OO00OO000O0OOOOOO ,O0O0OOOOOOO0OO00O ,OOOO0OO0OOO0OO0O0 ,OOOO0OOO00OOO00O0 ,OOOOOO000OOO0OO00 ]#line:1488
    text .insert (END ,"\n")#line:1490
def TOOLS_sql (O0O0OO00000OOOOO0 ):#line:1492
    ""#line:1493
    warnings .filterwarnings ("ignore")#line:1494
    try :#line:1495
        O00O0O0OOOO0OO0OO =O0O0OO00000OOOOO0 .columns #line:1496
    except :#line:1497
        return 0 #line:1498
    def O0000OOOO00000000 (O00OO0OO00O0OO000 ):#line:1500
        try :#line:1501
            OOOOO0O0OOO0OO0OO =pd .read_sql_query (sqltext (O00OO0OO00O0OO000 ),con =OO0O0OOO000O0OOOO )#line:1502
        except :#line:1503
            showinfo (title ="提示",message ="SQL语句有误。")#line:1504
            return 0 #line:1505
        try :#line:1506
            del OOOOO0O0OOO0OO0OO ["level_0"]#line:1507
        except :#line:1508
            pass #line:1509
        TABLE_tree_Level_2 (OOOOO0O0OOO0OO0OO ,1 ,O0O0OO00000OOOOO0 )#line:1510
    O0OOOOO0O000O0O0O ='sqlite://'#line:1514
    OOOOOOO0O0000000O =create_engine (O0OOOOO0O000O0O0O )#line:1515
    try :#line:1516
        O0O0OO00000OOOOO0 .to_sql ('data',con =OOOOOOO0O0000000O ,chunksize =10000 ,if_exists ='replace',index =True )#line:1517
    except :#line:1518
        showinfo (title ="提示",message ="不支持该表格。")#line:1519
        return 0 #line:1520
    OO0O0OOO000O0OOOO =OOOOOOO0O0000000O .connect ()#line:1522
    O0OOO00000OOO00OO ="select * from data"#line:1523
    O0O0O0O0OOOO00O00 =Toplevel ()#line:1526
    O0O0O0O0OOOO00O00 .title ("SQL查询")#line:1527
    O0O0O0O0OOOO00O00 .geometry ("700x500")#line:1528
    O0OOO0O00O0O00000 =ttk .Frame (O0O0O0O0OOOO00O00 ,width =700 ,height =20 )#line:1530
    O0OOO0O00O0O00000 .pack (side =TOP )#line:1531
    O000000O000000000 =ttk .Frame (O0O0O0O0OOOO00O00 ,width =700 ,height =20 )#line:1532
    O000000O000000000 .pack (side =BOTTOM )#line:1533
    try :#line:1536
        OOO0000O0O0OOO0O0 =StringVar ()#line:1537
        OOO0000O0O0OOO0O0 .set ("select * from data WHERE 单位名称='佛山市第一人民医院'")#line:1538
        OO0OOOOOO00OO0OO0 =Label (O0OOO0O00O0O00000 ,text ="SQL查询",anchor ='w')#line:1540
        OO0OOOOOO00OO0OO0 .pack (side =LEFT )#line:1541
        OOO0000000OOO0000 =Label (O0OOO0O00O0O00000 ,text ="检索：")#line:1542
        O0O00O000OO0O00O0 =Button (O000000O000000000 ,text ="执行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",width =700 ,command =lambda :O0000OOOO00000000 (OO0O0OOO0000000O0 .get ("1.0","end")),)#line:1556
        O0O00O000OO0O00O0 .pack (side =LEFT )#line:1557
    except EE :#line:1560
        pass #line:1561
    OOO0OOO00OO0OOOOO =Scrollbar (O0O0O0O0OOOO00O00 )#line:1563
    OO0O0OOO0000000O0 =Text (O0O0O0O0OOOO00O00 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1564
    OOO0OOO00OO0OOOOO .pack (side =RIGHT ,fill =Y )#line:1565
    OO0O0OOO0000000O0 .pack ()#line:1566
    OOO0OOO00OO0OOOOO .config (command =OO0O0OOO0000000O0 .yview )#line:1567
    OO0O0OOO0000000O0 .config (yscrollcommand =OOO0OOO00OO0OOOOO .set )#line:1568
    def OOO00O0OO0O0OO0OO (event =None ):#line:1569
        OO0O0OOO0000000O0 .event_generate ('<<Copy>>')#line:1570
    def O0OO000OOOOO00OO0 (event =None ):#line:1571
        OO0O0OOO0000000O0 .event_generate ('<<Paste>>')#line:1572
    def O00000O000OOOO00O (O0OOO0O0OO0O00O00 ,O0O0O00O0000O000O ):#line:1573
         TOOLS_savetxt (O0OOO0O0OO0O00O00 ,O0O0O00O0000O000O ,1 )#line:1574
    OOO0O000OOOO00000 =Menu (OO0O0OOO0000000O0 ,tearoff =False ,)#line:1575
    OOO0O000OOOO00000 .add_command (label ="复制",command =OOO00O0OO0O0OO0OO )#line:1576
    OOO0O000OOOO00000 .add_command (label ="粘贴",command =O0OO000OOOOO00OO0 )#line:1577
    OOO0O000OOOO00000 .add_command (label ="源文件列",command =lambda :PROGRAM_helper (O0O0OO00000OOOOO0 .columns .to_list ()))#line:1578
    def OO0000OO0OOOO0O00 (O00O0OO0OO0O0OOO0 ):#line:1579
         OOO0O000OOOO00000 .post (O00O0OO0OO0O0OOO0 .x_root ,O00O0OO0OO0O0OOO0 .y_root )#line:1580
    OO0O0OOO0000000O0 .bind ("<Button-3>",OO0000OO0OOOO0O00 )#line:1581
    OO0O0OOO0000000O0 .insert (END ,O0OOO00000OOO00OO )#line:1585
def TOOLS_view_dict (O0OO0000OO000O0O0 ,OOOOOOO00O00000O0 ):#line:1589
    ""#line:1590
    OOOO0OO0000OOO0O0 =Toplevel ()#line:1591
    OOOO0OO0000OOO0O0 .title ("查看数据")#line:1592
    OOOO0OO0000OOO0O0 .geometry ("700x500")#line:1593
    O00OOO00O00O00O0O =Scrollbar (OOOO0OO0000OOO0O0 )#line:1595
    O0000O000O0O0OO00 =Text (OOOO0OO0000OOO0O0 ,height =100 ,width =150 )#line:1596
    O00OOO00O00O00O0O .pack (side =RIGHT ,fill =Y )#line:1597
    O0000O000O0O0OO00 .pack ()#line:1598
    O00OOO00O00O00O0O .config (command =O0000O000O0O0OO00 .yview )#line:1599
    O0000O000O0O0OO00 .config (yscrollcommand =O00OOO00O00O00O0O .set )#line:1600
    if OOOOOOO00O00000O0 ==1 :#line:1601
        O0000O000O0O0OO00 .insert (END ,O0OO0000OO000O0O0 )#line:1603
        O0000O000O0O0OO00 .insert (END ,"\n\n")#line:1604
        return 0 #line:1605
    for O0O0O000OOOO0O00O in range (len (O0OO0000OO000O0O0 )):#line:1606
        O0000O000O0O0OO00 .insert (END ,O0OO0000OO000O0O0 .iloc [O0O0O000OOOO0O00O ,0 ])#line:1607
        O0000O000O0O0OO00 .insert (END ,":")#line:1608
        O0000O000O0O0OO00 .insert (END ,O0OO0000OO000O0O0 .iloc [O0O0O000OOOO0O00O ,1 ])#line:1609
        O0000O000O0O0OO00 .insert (END ,"\n\n")#line:1610
def TOOLS_save_dict (O000000000000OOOO ):#line:1612
    ""#line:1613
    O0O0000000O0OO000 =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="排序后的原始数据",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1619
    try :#line:1620
        O000000000000OOOO ["详细描述T"]=O000000000000OOOO ["详细描述T"].astype (str )#line:1621
    except :#line:1622
        pass #line:1623
    try :#line:1624
        O000000000000OOOO ["报告编码"]=O000000000000OOOO ["报告编码"].astype (str )#line:1625
    except :#line:1626
        pass #line:1627
    OO0OO0OO0O00OO00O =pd .ExcelWriter (O0O0000000O0OO000 ,engine ="xlsxwriter")#line:1629
    O000000000000OOOO .to_excel (OO0OO0OO0O00OO00O ,sheet_name ="字典数据")#line:1630
    OO0OO0OO0O00OO00O .close ()#line:1631
    showinfo (title ="提示",message ="文件写入成功。")#line:1632
def TOOLS_savetxt (OOOO00OO0000OO0O0 ,OOOO000OOOO000O0O ,OOO0OOO0000OO00OO ):#line:1634
	""#line:1635
	O0OOO0O0O0O0OOOO0 =open (OOOO000OOOO000O0O ,"w",encoding ='utf-8')#line:1636
	O0OOO0O0O0O0OOOO0 .write (OOOO00OO0000OO0O0 )#line:1637
	O0OOO0O0O0O0OOOO0 .flush ()#line:1639
	if OOO0OOO0000OO00OO ==1 :#line:1640
		showinfo (title ="提示信息",message ="保存成功。")#line:1641
def TOOLS_deep_view (O00O000OOOO0O0OOO ,OOOO0O00OOO0O0O00 ,OOO000O0000O0OOOO ,O0000O00OOO0O00O0 ):#line:1644
    ""#line:1645
    if O0000O00OOO0O00O0 ==0 :#line:1646
        try :#line:1647
            O00O000OOOO0O0OOO [OOOO0O00OOO0O0O00 ]=O00O000OOOO0O0OOO [OOOO0O00OOO0O0O00 ].fillna ("这个没有填写")#line:1648
        except :#line:1649
            pass #line:1650
        OOO0OO0OOOOOO0O00 =O00O000OOOO0O0OOO .groupby (OOOO0O00OOO0O0O00 ).agg (计数 =(OOO000O0000O0OOOO [0 ],OOO000O0000O0OOOO [1 ]))#line:1651
    if O0000O00OOO0O00O0 ==1 :#line:1652
            OOO0OO0OOOOOO0O00 =pd .pivot_table (O00O000OOOO0O0OOO ,index =OOOO0O00OOO0O0O00 [:-1 ],columns =OOOO0O00OOO0O0O00 [-1 ],values =[OOO000O0000O0OOOO [0 ]],aggfunc ={OOO000O0000O0OOOO [0 ]:OOO000O0000O0OOOO [1 ]},fill_value ="0",margins =True ,dropna =False ,)#line:1663
            OOO0OO0OOOOOO0O00 .columns =OOO0OO0OOOOOO0O00 .columns .droplevel (0 )#line:1664
            OOO0OO0OOOOOO0O00 =OOO0OO0OOOOOO0O00 .rename (columns ={"All":"计数"})#line:1665
    if "日期"in OOOO0O00OOO0O0O00 or "时间"in OOOO0O00OOO0O0O00 or "季度"in OOOO0O00OOO0O0O00 :#line:1668
        OOO0OO0OOOOOO0O00 =OOO0OO0OOOOOO0O00 .sort_values ([OOOO0O00OOO0O0O00 ],ascending =False ,na_position ="last")#line:1671
    else :#line:1672
        OOO0OO0OOOOOO0O00 =OOO0OO0OOOOOO0O00 .sort_values (by =["计数"],ascending =False ,na_position ="last")#line:1676
    OOO0OO0OOOOOO0O00 =OOO0OO0OOOOOO0O00 .reset_index ()#line:1677
    OOO0OO0OOOOOO0O00 ["构成比(%)"]=round (100 *OOO0OO0OOOOOO0O00 ["计数"]/OOO0OO0OOOOOO0O00 ["计数"].sum (),2 )#line:1678
    if O0000O00OOO0O00O0 ==0 :#line:1679
        OOO0OO0OOOOOO0O00 ["报表类型"]="dfx_deepview"+"_"+str (OOOO0O00OOO0O0O00 )#line:1680
    if O0000O00OOO0O00O0 ==1 :#line:1681
        OOO0OO0OOOOOO0O00 ["报表类型"]="dfx_deepview"+"_"+str (OOOO0O00OOO0O0O00 [:-1 ])#line:1682
    return OOO0OO0OOOOOO0O00 #line:1683
def TOOLS_easyreadT (O00O000OOOO00O000 ):#line:1687
    ""#line:1688
    O00O000OOOO00O000 ["#####分隔符#########"]="######################################################################"#line:1691
    OO0OOO0O0OOO0O00O =O00O000OOOO00O000 .stack (dropna =False )#line:1692
    OO0OOO0O0OOO0O00O =pd .DataFrame (OO0OOO0O0OOO0O00O ).reset_index ()#line:1693
    OO0OOO0O0OOO0O00O .columns =["序号","条目","详细描述T"]#line:1694
    OO0OOO0O0OOO0O00O ["逐条查看"]="逐条查看"#line:1695
    return OO0OOO0O0OOO0O00O #line:1696
def TOOLS_data_masking (O0O000O0OOO0OOOO0 ):#line:1698
    ""#line:1699
    from random import choices #line:1700
    from string import ascii_letters ,digits #line:1701
    O0O000O0OOO0OOOO0 =O0O000O0OOO0OOOO0 .reset_index (drop =True )#line:1703
    if "单位名称.1"in O0O000O0OOO0OOOO0 .columns :#line:1704
        OOOOOOOO0OOO0O00O ="器械"#line:1705
    else :#line:1706
        OOOOOOOO0OOO0O00O ="药品"#line:1707
    O00OO0O00O00O0OO0 =peizhidir +""+"0（范例）数据脱敏"+".xls"#line:1708
    try :#line:1709
        O000OOOOOO0OO000O =pd .read_excel (O00OO0O00O00O0OO0 ,sheet_name =OOOOOOOO0OOO0O00O ,header =0 ,index_col =0 ).reset_index ()#line:1712
    except :#line:1713
        showinfo (title ="错误信息",message ="该功能需要配置文件才能使用！")#line:1714
        return 0 #line:1715
    O0OO0OOOOOO00OOOO =0 #line:1716
    OOOO00OOOOOO000O0 =len (O0O000O0OOO0OOOO0 )#line:1717
    O0O000O0OOO0OOOO0 ["abcd"]="□"#line:1718
    for OOO0OO00O0OOO0000 in O000OOOOOO0OO000O ["要脱敏的列"]:#line:1719
        O0OO0OOOOOO00OOOO =O0OO0OOOOOO00OOOO +1 #line:1720
        PROGRAM_change_schedule (O0OO0OOOOOO00OOOO ,OOOO00OOOOOO000O0 )#line:1721
        text .insert (END ,"\n正在对以下列进行脱敏处理：")#line:1722
        text .see (END )#line:1723
        text .insert (END ,OOO0OO00O0OOO0000 )#line:1724
        try :#line:1725
            OO0OOO00O0O0O0OO0 =set (O0O000O0OOO0OOOO0 [OOO0OO00O0OOO0000 ])#line:1726
        except :#line:1727
            showinfo (title ="提示",message ="脱敏文件配置错误，请修改配置表。")#line:1728
            return 0 #line:1729
        O0O0OOOO0O000000O ={OOOO0OOOOOO0000OO :"".join (choices (digits ,k =10 ))for OOOO0OOOOOO0000OO in OO0OOO00O0O0O0OO0 }#line:1730
        O0O000O0OOO0OOOO0 [OOO0OO00O0OOO0000 ]=O0O000O0OOO0OOOO0 [OOO0OO00O0OOO0000 ].map (O0O0OOOO0O000000O )#line:1731
        O0O000O0OOO0OOOO0 [OOO0OO00O0OOO0000 ]=O0O000O0OOO0OOOO0 ["abcd"]+O0O000O0OOO0OOOO0 [OOO0OO00O0OOO0000 ].astype (str )#line:1732
    try :#line:1733
        PROGRAM_change_schedule (10 ,10 )#line:1734
        del O0O000O0OOO0OOOO0 ["abcd"]#line:1735
        O0O000OOOO00O000O =filedialog .asksaveasfilename (title =u"保存脱敏后的文件",initialfile ="脱敏后的文件",defaultextension ="xlsx",filetypes =[("Excel 工作簿","*.xlsx"),("Excel 97-2003 工作簿","*.xls")],)#line:1741
        O0OOO0OOOOOOOO000 =pd .ExcelWriter (O0O000OOOO00O000O ,engine ="xlsxwriter")#line:1742
        O0O000O0OOO0OOOO0 .to_excel (O0OOO0OOOOOOOO000 ,sheet_name ="sheet0")#line:1743
        O0OOO0OOOOOOOO000 .close ()#line:1744
    except :#line:1745
        text .insert (END ,"\n文件未保存，但导入的数据已按要求脱敏。")#line:1746
    text .insert (END ,"\n脱敏操作完成。")#line:1747
    text .see (END )#line:1748
    return O0O000O0OOO0OOOO0 #line:1749
def TOOLS_get_new (O0OO0OO00O0000O00 ,OO0O0000O00OOO000 ):#line:1751
	""#line:1752
	def O0OO00O0O00O00000 (O000OO00O0O000OO0 ):#line:1753
		""#line:1754
		O000OO00O0O000OO0 =O000OO00O0O000OO0 .drop_duplicates ("报告编码")#line:1755
		O0000OO0OOO0O0OO0 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",O000OO00O0O000OO0 ,1000 ))).replace ("Counter({","{")#line:1756
		O0000OO0OOO0O0OO0 =O0000OO0OOO0O0OO0 .replace ("})","}")#line:1757
		import ast #line:1758
		OOOO0O0O0OOOOO0O0 =ast .literal_eval (O0000OO0OOO0O0OO0 )#line:1759
		OO0OO00OOO00OOOOO =TOOLS_easyreadT (pd .DataFrame ([OOOO0O0O0OOOOO0O0 ]))#line:1760
		OO0OO00OOO00OOOOO =OO0OO00OOO00OOOOO .rename (columns ={"逐条查看":"ADR名称规整"})#line:1761
		return OO0OO00OOO00OOOOO #line:1762
	if OO0O0000O00OOO000 =="证号":#line:1763
		root .attributes ("-topmost",True )#line:1764
		root .attributes ("-topmost",False )#line:1765
		O0OOOOOOOOO0OOO0O =O0OO0OO00O0000O00 .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1766
		OOO00O00OOO0OOOOO =O0OOOOOOOOO0OOO0O .drop_duplicates ("注册证编号/曾用注册证编号").copy ()#line:1767
		OOO00O00OOO0OOOOO ["所有不良反应"]=""#line:1768
		OOO00O00OOO0OOOOO ["关注建议"]=""#line:1769
		OOO00O00OOO0OOOOO ["疑似新的"]=""#line:1770
		OOO00O00OOO0OOOOO ["疑似旧的"]=""#line:1771
		OOO00O00OOO0OOOOO ["疑似新的（高敏）"]=""#line:1772
		OOO00O00OOO0OOOOO ["疑似旧的（高敏）"]=""#line:1773
		OOO0O00OO0OOO00OO =1 #line:1774
		O00OOOO0OO00O00O0 =int (len (OOO00O00OOO0OOOOO ))#line:1775
		for OOOOO00OO00OOO0OO ,OO00OOOO00O00OOOO in OOO00O00OOO0OOOOO .iterrows ():#line:1776
			O0O0O0OO0OOOOOO0O =O0OO0OO00O0000O00 [(O0OO0OO00O0000O00 ["注册证编号/曾用注册证编号"]==OO00OOOO00O00OOOO ["注册证编号/曾用注册证编号"])]#line:1777
			O0O0O00O00OOO0O00 =O0O0O0OO0OOOOOO0O .loc [O0O0O0OO0OOOOOO0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1778
			OO00O000000OO00OO =O0O0O0OO0OOOOOO0O .loc [~O0O0O0OO0OOOOOO0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1779
			OOO0000000O00OO00 =O0OO00O0O00O00000 (O0O0O00O00OOO0O00 )#line:1780
			O00OOO000000OO0OO =O0OO00O0O00O00000 (OO00O000000OO00OO )#line:1781
			O0OO0000OO0OOOO0O =O0OO00O0O00O00000 (O0O0O0OO0OOOOOO0O )#line:1782
			PROGRAM_change_schedule (OOO0O00OO0OOO00OO ,O00OOOO0OO00O00O0 )#line:1783
			OOO0O00OO0OOO00OO =OOO0O00OO0OOO00OO +1 #line:1784
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in O0OO0000OO0OOOO0O .iterrows ():#line:1786
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]:#line:1787
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1788
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"所有不良反应"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"所有不良反应"]+O000OOO0OO0OO0000 #line:1789
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in O00OOO000000OO0OO .iterrows ():#line:1791
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]:#line:1792
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1793
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的"]+O000OOO0OO0OO0000 #line:1794
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]and int (O0O0O000OOOO0OO00 ["详细描述T"])>=2 :#line:1796
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1797
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的（高敏）"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的（高敏）"]+O000OOO0OO0OO0000 #line:1798
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in OOO0000000O00OO00 .iterrows ():#line:1800
				if str (O0O0O000OOOO0OO00 ["条目"]).strip ()not in str (OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的"])and "分隔符"not in str (O0O0O000OOOO0OO00 ["条目"]):#line:1801
					O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1802
					OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的"]+O000OOO0OO0OO0000 #line:1803
					if int (O0O0O000OOOO0OO00 ["详细描述T"])>=3 :#line:1804
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]+"！"#line:1805
					if int (O0O0O000OOOO0OO00 ["详细描述T"])>=5 :#line:1806
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]+"●"#line:1807
				if str (O0O0O000OOOO0OO00 ["条目"]).strip ()not in str (OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的（高敏）"])and "分隔符"not in str (O0O0O000OOOO0OO00 ["条目"])and int (O0O0O000OOOO0OO00 ["详细描述T"])>=2 :#line:1809
					O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1810
					OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的（高敏）"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的（高敏）"]+O000OOO0OO0OO0000 #line:1811
		OOO00O00OOO0OOOOO ["疑似新的"]="{"+OOO00O00OOO0OOOOO ["疑似新的"]+"}"#line:1813
		OOO00O00OOO0OOOOO ["疑似旧的"]="{"+OOO00O00OOO0OOOOO ["疑似旧的"]+"}"#line:1814
		OOO00O00OOO0OOOOO ["所有不良反应"]="{"+OOO00O00OOO0OOOOO ["所有不良反应"]+"}"#line:1815
		OOO00O00OOO0OOOOO ["疑似新的（高敏）"]="{"+OOO00O00OOO0OOOOO ["疑似新的（高敏）"]+"}"#line:1816
		OOO00O00OOO0OOOOO ["疑似旧的（高敏）"]="{"+OOO00O00OOO0OOOOO ["疑似旧的（高敏）"]+"}"#line:1817
		OOO00O00OOO0OOOOO =OOO00O00OOO0OOOOO .rename (columns ={"器械待评价(药品新的报告比例)":"新的报告比例"})#line:1819
		OOO00O00OOO0OOOOO =OOO00O00OOO0OOOOO .rename (columns ={"严重伤害待评价比例(药品严重中新的比例)":"严重报告中新的比例"})#line:1820
		OOO00O00OOO0OOOOO ["报表类型"]="dfx_zhenghao"#line:1821
		OOOO0O0OO0OOOOO0O =pd .pivot_table (O0OO0OO00O0000O00 ,values =["报告编码"],index =["注册证编号/曾用注册证编号"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1823
		OOOO0O0OO0OOOOO0O .columns =OOOO0O0OO0OOOOO0O .columns .droplevel (0 )#line:1824
		OOO00O00OOO0OOOOO =pd .merge (OOO00O00OOO0OOOOO ,OOOO0O0OO0OOOOO0O .reset_index (),on =["注册证编号/曾用注册证编号"],how ="left")#line:1825
		TABLE_tree_Level_2 (OOO00O00OOO0OOOOO .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O0OO0OO00O0000O00 )#line:1829
	if OO0O0000O00OOO000 =="品种":#line:1830
		root .attributes ("-topmost",True )#line:1831
		root .attributes ("-topmost",False )#line:1832
		O0OOOOOOOOO0OOO0O =O0OO0OO00O0000O00 .groupby (["产品类别","产品名称"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1833
		OOO00O00OOO0OOOOO =O0OOOOOOOOO0OOO0O .drop_duplicates ("产品名称").copy ()#line:1834
		OOO00O00OOO0OOOOO ["产品名称"]=OOO00O00OOO0OOOOO ["产品名称"].str .replace ("*","",regex =False )#line:1835
		OOO00O00OOO0OOOOO ["所有不良反应"]=""#line:1836
		OOO00O00OOO0OOOOO ["关注建议"]=""#line:1837
		OOO00O00OOO0OOOOO ["疑似新的"]=""#line:1838
		OOO00O00OOO0OOOOO ["疑似旧的"]=""#line:1839
		OOO00O00OOO0OOOOO ["疑似新的（高敏）"]=""#line:1840
		OOO00O00OOO0OOOOO ["疑似旧的（高敏）"]=""#line:1841
		OOO0O00OO0OOO00OO =1 #line:1842
		O00OOOO0OO00O00O0 =int (len (OOO00O00OOO0OOOOO ))#line:1843
		for OOOOO00OO00OOO0OO ,OO00OOOO00O00OOOO in OOO00O00OOO0OOOOO .iterrows ():#line:1846
			O0O0O0OO0OOOOOO0O =O0OO0OO00O0000O00 [(O0OO0OO00O0000O00 ["产品名称"]==OO00OOOO00O00OOOO ["产品名称"])]#line:1848
			O0O0O00O00OOO0O00 =O0O0O0OO0OOOOOO0O .loc [O0O0O0OO0OOOOOO0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1850
			OO00O000000OO00OO =O0O0O0OO0OOOOOO0O .loc [~O0O0O0OO0OOOOOO0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1851
			O0OO0000OO0OOOO0O =O0OO00O0O00O00000 (O0O0O0OO0OOOOOO0O )#line:1852
			OOO0000000O00OO00 =O0OO00O0O00O00000 (O0O0O00O00OOO0O00 )#line:1853
			O00OOO000000OO0OO =O0OO00O0O00O00000 (OO00O000000OO00OO )#line:1854
			PROGRAM_change_schedule (OOO0O00OO0OOO00OO ,O00OOOO0OO00O00O0 )#line:1855
			OOO0O00OO0OOO00OO =OOO0O00OO0OOO00OO +1 #line:1856
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in O0OO0000OO0OOOO0O .iterrows ():#line:1858
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]:#line:1859
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1860
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"所有不良反应"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"所有不良反应"]+O000OOO0OO0OO0000 #line:1861
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in O00OOO000000OO0OO .iterrows ():#line:1864
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]:#line:1865
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1866
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的"]+O000OOO0OO0OO0000 #line:1867
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]and int (O0O0O000OOOO0OO00 ["详细描述T"])>=2 :#line:1869
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1870
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的（高敏）"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的（高敏）"]+O000OOO0OO0OO0000 #line:1871
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in OOO0000000O00OO00 .iterrows ():#line:1873
				if str (O0O0O000OOOO0OO00 ["条目"]).strip ()not in str (OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的"])and "分隔符"not in str (O0O0O000OOOO0OO00 ["条目"]):#line:1874
					O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1875
					OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的"]+O000OOO0OO0OO0000 #line:1876
					if int (O0O0O000OOOO0OO00 ["详细描述T"])>=3 :#line:1877
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]+"！"#line:1878
					if int (O0O0O000OOOO0OO00 ["详细描述T"])>=5 :#line:1879
						OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"关注建议"]+"●"#line:1880
				if str (O0O0O000OOOO0OO00 ["条目"]).strip ()not in str (OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似旧的（高敏）"])and "分隔符"not in str (O0O0O000OOOO0OO00 ["条目"])and int (O0O0O000OOOO0OO00 ["详细描述T"])>=2 :#line:1882
					O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1883
					OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的（高敏）"]=OOO00O00OOO0OOOOO .loc [OOOOO00OO00OOO0OO ,"疑似新的（高敏）"]+O000OOO0OO0OO0000 #line:1884
		OOO00O00OOO0OOOOO ["疑似新的"]="{"+OOO00O00OOO0OOOOO ["疑似新的"]+"}"#line:1886
		OOO00O00OOO0OOOOO ["疑似旧的"]="{"+OOO00O00OOO0OOOOO ["疑似旧的"]+"}"#line:1887
		OOO00O00OOO0OOOOO ["所有不良反应"]="{"+OOO00O00OOO0OOOOO ["所有不良反应"]+"}"#line:1888
		OOO00O00OOO0OOOOO ["疑似新的（高敏）"]="{"+OOO00O00OOO0OOOOO ["疑似新的（高敏）"]+"}"#line:1889
		OOO00O00OOO0OOOOO ["疑似旧的（高敏）"]="{"+OOO00O00OOO0OOOOO ["疑似旧的（高敏）"]+"}"#line:1890
		OOO00O00OOO0OOOOO ["报表类型"]="dfx_chanpin"#line:1891
		OOOO0O0OO0OOOOO0O =pd .pivot_table (O0OO0OO00O0000O00 ,values =["报告编码"],index =["产品名称"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1893
		OOOO0O0OO0OOOOO0O .columns =OOOO0O0OO0OOOOO0O .columns .droplevel (0 )#line:1894
		OOO00O00OOO0OOOOO =pd .merge (OOO00O00OOO0OOOOO ,OOOO0O0OO0OOOOO0O .reset_index (),on =["产品名称"],how ="left")#line:1895
		TABLE_tree_Level_2 (OOO00O00OOO0OOOOO .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O0OO0OO00O0000O00 )#line:1896
	if OO0O0000O00OOO000 =="页面":#line:1898
		OO0O0OOOOO0000OO0 =""#line:1899
		O0O000OOO00OO00O0 =""#line:1900
		O0O0O00O00OOO0O00 =O0OO0OO00O0000O00 .loc [O0OO0OO00O0000O00 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1901
		OO00O000000OO00OO =O0OO0OO00O0000O00 .loc [~O0OO0OO00O0000O00 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1902
		OOO0000000O00OO00 =O0OO00O0O00O00000 (O0O0O00O00OOO0O00 )#line:1903
		O00OOO000000OO0OO =O0OO00O0O00O00000 (OO00O000000OO00OO )#line:1904
		if 1 ==1 :#line:1905
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in O00OOO000000OO0OO .iterrows ():#line:1906
					if "分隔符"not in O0O0O000OOOO0OO00 ["条目"]:#line:1907
						O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1908
						O0O000OOO00OO00O0 =O0O000OOO00OO00O0 +O000OOO0OO0OO0000 #line:1909
			for OOO00OOO000O0OO00 ,O0O0O000OOOO0OO00 in OOO0000000O00OO00 .iterrows ():#line:1910
				if str (O0O0O000OOOO0OO00 ["条目"]).strip ()not in O0O000OOO00OO00O0 and "分隔符"not in str (O0O0O000OOOO0OO00 ["条目"]):#line:1911
					O000OOO0OO0OO0000 ="'"+str (O0O0O000OOOO0OO00 ["条目"])+"':"+str (O0O0O000OOOO0OO00 ["详细描述T"])+","#line:1912
					OO0O0OOOOO0000OO0 =OO0O0OOOOO0000OO0 +O000OOO0OO0OO0000 #line:1913
		O0O000OOO00OO00O0 ="{"+O0O000OOO00OO00O0 +"}"#line:1914
		OO0O0OOOOO0000OO0 ="{"+OO0O0OOOOO0000OO0 +"}"#line:1915
		O0OOOOOOO00O00OOO ="\n可能是新的不良反应：\n\n"+OO0O0OOOOO0000OO0 +"\n\n\n可能不是新的不良反应：\n\n"+O0O000OOO00OO00O0 #line:1916
		TOOLS_view_dict (O0OOOOOOO00O00OOO ,1 )#line:1917
def TOOLS_strdict_to_pd (OO0000000000OOOOO ):#line:1919
	""#line:1920
	return pd .DataFrame .from_dict (eval (OO0000000000OOOOO ),orient ="index",columns =["content"]).reset_index ()#line:1921
def TOOLS_xuanze (OO00OO0O000O000O0 ,O0O0O0O000000OOO0 ):#line:1923
    ""#line:1924
    if O0O0O0O000000OOO0 ==0 :#line:1925
        O00O000000O0O00O0 =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLS",".xls")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1926
    else :#line:1927
        O00O000000O0O00O0 =pd .read_excel (peizhidir +"0（范例）批量筛选.xls",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1928
    OO00OO0O000O000O0 ["temppr"]=""#line:1929
    for OO00000OO0000000O in O00O000000O0O00O0 .columns .tolist ():#line:1930
        OO00OO0O000O000O0 ["temppr"]=OO00OO0O000O000O0 ["temppr"]+"----"+OO00OO0O000O000O0 [OO00000OO0000000O ]#line:1931
    O0OOOOOOO000O00O0 ="测试字段MMMMM"#line:1932
    for OO00000OO0000000O in O00O000000O0O00O0 .columns .tolist ():#line:1933
        for O0O00OO0O0O000O00 in O00O000000O0O00O0 [OO00000OO0000000O ].drop_duplicates ():#line:1935
            if O0O00OO0O0O000O00 :#line:1936
                O0OOOOOOO000O00O0 =O0OOOOOOO000O00O0 +"|"+str (O0O00OO0O0O000O00 )#line:1937
    OO00OO0O000O000O0 =OO00OO0O000O000O0 .loc [OO00OO0O000O000O0 ["temppr"].str .contains (O0OOOOOOO000O00O0 ,na =False )].copy ()#line:1938
    del OO00OO0O000O000O0 ["temppr"]#line:1939
    OO00OO0O000O000O0 =OO00OO0O000O000O0 .reset_index (drop =True )#line:1940
    TABLE_tree_Level_2 (OO00OO0O000O000O0 ,0 ,OO00OO0O000O000O0 )#line:1942
def TOOLS_add_c (O000O00O00OOOOO00 ,O000O00O00O0O00O0 ):#line:1944
			O000O00O00OOOOO00 ["关键字查找列o"]=""#line:1945
			for O0OO0O00O00OO00OO in TOOLS_get_list (O000O00O00O0O00O0 ["查找列"]):#line:1946
				O000O00O00OOOOO00 ["关键字查找列o"]=O000O00O00OOOOO00 ["关键字查找列o"]+O000O00O00OOOOO00 [O0OO0O00O00OO00OO ].astype ("str")#line:1947
			if O000O00O00O0O00O0 ["条件"]=="等于":#line:1948
				O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 [O000O00O00O0O00O0 ["查找列"]].astype (str )==str (O000O00O00O0O00O0 ["条件值"])),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1949
			if O000O00O00O0O00O0 ["条件"]=="大于":#line:1950
				O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 [O000O00O00O0O00O0 ["查找列"]].astype (float )>O000O00O00O0O00O0 ["条件值"]),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1951
			if O000O00O00O0O00O0 ["条件"]=="小于":#line:1952
				O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 [O000O00O00O0O00O0 ["查找列"]].astype (float )<O000O00O00O0O00O0 ["条件值"]),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1953
			if O000O00O00O0O00O0 ["条件"]=="介于":#line:1954
				OO0OO00O000OO0O00 =TOOLS_get_list (O000O00O00O0O00O0 ["条件值"])#line:1955
				O000O00O00OOOOO00 .loc [((O000O00O00OOOOO00 [O000O00O00O0O00O0 ["查找列"]].astype (float )<float (OO0OO00O000OO0O00 [1 ]))&(O000O00O00OOOOO00 [O000O00O00O0O00O0 ["查找列"]].astype (float )>float (OO0OO00O000OO0O00 [0 ]))),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1956
			if O000O00O00O0O00O0 ["条件"]=="不含":#line:1957
				O000O00O00OOOOO00 .loc [(~O000O00O00OOOOO00 ["关键字查找列o"].str .contains (O000O00O00O0O00O0 ["条件值"])),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1958
			if O000O00O00O0O00O0 ["条件"]=="包含":#line:1959
				O000O00O00OOOOO00 .loc [O000O00O00OOOOO00 ["关键字查找列o"].str .contains (O000O00O00O0O00O0 ["条件值"],na =False ),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1960
			if O000O00O00O0O00O0 ["条件"]=="同时包含":#line:1961
				OO000OOO0OOO0O0OO =TOOLS_get_list0 (O000O00O00O0O00O0 ["条件值"],0 )#line:1962
				if len (OO000OOO0OOO0O0OO )==1 :#line:1963
				    O000O00O00OOOOO00 .loc [O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [0 ],na =False ),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1964
				if len (OO000OOO0OOO0O0OO )==2 :#line:1965
				    O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [0 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [1 ],na =False )),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1966
				if len (OO000OOO0OOO0O0OO )==3 :#line:1967
				    O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [0 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [1 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [2 ],na =False )),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1968
				if len (OO000OOO0OOO0O0OO )==4 :#line:1969
				    O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [0 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [1 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [2 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [3 ],na =False )),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1970
				if len (OO000OOO0OOO0O0OO )==5 :#line:1971
				    O000O00O00OOOOO00 .loc [(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [0 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [1 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [2 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [3 ],na =False ))&(O000O00O00OOOOO00 ["关键字查找列o"].str .contains (OO000OOO0OOO0O0OO [4 ],na =False )),O000O00O00O0O00O0 ["赋值列名"]]=O000O00O00O0O00O0 ["赋值"]#line:1972
			return O000O00O00OOOOO00 #line:1973
def TOOL_guizheng (OO0OO0OOO000OOO0O ,OOO0000O0O0OO0000 ,O0OOO0OOOOO000OO0 ):#line:1976
	""#line:1977
	if OOO0000O0O0OO0000 ==0 :#line:1978
		OO000O0OO000O0O0O =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLSX",".xlsx")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1979
		OO000O0OO000O0O0O =OO000O0OO000O0O0O [(OO000O0OO000O0O0O ["执行标记"]=="是")].reset_index ()#line:1980
		for O0OOOOOOOOOOOOO0O ,OO00OO0O00OO000OO in OO000O0OO000O0O0O .iterrows ():#line:1981
			OO0OO0OOO000OOO0O =TOOLS_add_c (OO0OO0OOO000OOO0O ,OO00OO0O00OO000OO )#line:1982
		del OO0OO0OOO000OOO0O ["关键字查找列o"]#line:1983
	elif OOO0000O0O0OO0000 ==1 :#line:1985
		OO000O0OO000O0O0O =pd .read_excel (peizhidir +"0（范例）数据规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1986
		OO000O0OO000O0O0O =OO000O0OO000O0O0O [(OO000O0OO000O0O0O ["执行标记"]=="是")].reset_index ()#line:1987
		for O0OOOOOOOOOOOOO0O ,OO00OO0O00OO000OO in OO000O0OO000O0O0O .iterrows ():#line:1988
			OO0OO0OOO000OOO0O =TOOLS_add_c (OO0OO0OOO000OOO0O ,OO00OO0O00OO000OO )#line:1989
		del OO0OO0OOO000OOO0O ["关键字查找列o"]#line:1990
	elif OOO0000O0O0OO0000 =="课题":#line:1992
		OO000O0OO000O0O0O =pd .read_excel (peizhidir +"0（范例）品类规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1993
		OO000O0OO000O0O0O =OO000O0OO000O0O0O [(OO000O0OO000O0O0O ["执行标记"]=="是")].reset_index ()#line:1994
		for O0OOOOOOOOOOOOO0O ,OO00OO0O00OO000OO in OO000O0OO000O0O0O .iterrows ():#line:1995
			OO0OO0OOO000OOO0O =TOOLS_add_c (OO0OO0OOO000OOO0O ,OO00OO0O00OO000OO )#line:1996
		del OO0OO0OOO000OOO0O ["关键字查找列o"]#line:1997
	elif OOO0000O0O0OO0000 ==2 :#line:1999
		text .insert (END ,"\n开展报告单位和监测机构名称规整...")#line:2000
		O0OO0O0OOOO0OO0OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2001
		OOO0OO0O0O00000OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2002
		OO0OO00OO0O000OOO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="地市清单",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2003
		for O0OOOOOOOOOOOOO0O ,OO00OO0O00OO000OO in O0OO0O0OOOO0OO0OO .iterrows ():#line:2004
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["曾用名1"]),"单位名称"]=OO00OO0O00OO000OO ["单位名称"]#line:2005
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["曾用名2"]),"单位名称"]=OO00OO0O00OO000OO ["单位名称"]#line:2006
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["曾用名3"]),"单位名称"]=OO00OO0O00OO000OO ["单位名称"]#line:2007
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["曾用名4"]),"单位名称"]=OO00OO0O00OO000OO ["单位名称"]#line:2008
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["曾用名5"]),"单位名称"]=OO00OO0O00OO000OO ["单位名称"]#line:2009
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["单位名称"]),"医疗机构类别"]=OO00OO0O00OO000OO ["医疗机构类别"]#line:2011
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["单位名称"]),"监测机构"]=OO00OO0O00OO000OO ["监测机构"]#line:2012
		for O0OOOOOOOOOOOOO0O ,OO00OO0O00OO000OO in OOO0OO0O0O00000OO .iterrows ():#line:2014
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["监测机构"]==OO00OO0O00OO000OO ["曾用名1"]),"监测机构"]=OO00OO0O00OO000OO ["监测机构"]#line:2015
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["监测机构"]==OO00OO0O00OO000OO ["曾用名2"]),"监测机构"]=OO00OO0O00OO000OO ["监测机构"]#line:2016
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["监测机构"]==OO00OO0O00OO000OO ["曾用名3"]),"监测机构"]=OO00OO0O00OO000OO ["监测机构"]#line:2017
		for OOOOO0OOO000OO00O in OO0OO00OO0O000OOO ["地市列表"]:#line:2019
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["上报单位所属地区"].str .contains (OOOOO0OOO000OO00O ,na =False )),"市级监测机构"]=OOOOO0OOO000OO00O #line:2020
		OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构"]="佛山"#line:2023
		OO0OO0OOO000OOO0O ["市级监测机构"]=OO0OO0OOO000OOO0O ["市级监测机构"].fillna ("-未规整的-")#line:2024
	elif OOO0000O0O0OO0000 ==3 :#line:2026
			O00O00O00O00O00O0 =(OO0OO0OOO000OOO0O .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).aggregate ({"报告编码":"count"}).reset_index ())#line:2031
			O00O00O00O00O00O0 =O00O00O00O00O00O0 .sort_values (by =["注册证编号/曾用注册证编号","报告编码"],ascending =[False ,False ],na_position ="last").reset_index ()#line:2034
			text .insert (END ,"\n开展产品名称规整..")#line:2035
			del O00O00O00O00O00O0 ["报告编码"]#line:2036
			O00O00O00O00O00O0 =O00O00O00O00O00O0 .drop_duplicates (["注册证编号/曾用注册证编号"])#line:2037
			OO0OO0OOO000OOO0O =OO0OO0OOO000OOO0O .rename (columns ={"上市许可持有人名称":"上市许可持有人名称（规整前）","产品类别":"产品类别（规整前）","产品名称":"产品名称（规整前）"})#line:2039
			OO0OO0OOO000OOO0O =pd .merge (OO0OO0OOO000OOO0O ,O00O00O00O00O00O0 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2040
	elif OOO0000O0O0OO0000 ==4 :#line:2042
		text .insert (END ,"\n正在开展化妆品注册单位规整...")#line:2043
		OOO0OO0O0O00000OO =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="机构列表",header =0 ,index_col =0 ,).reset_index ()#line:2044
		for O0OOOOOOOOOOOOO0O ,OO00OO0O00OO000OO in OOO0OO0O0O00000OO .iterrows ():#line:2046
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["中文全称"]),"监测机构"]=OO00OO0O00OO000OO ["归属地区"]#line:2047
			OO0OO0OOO000OOO0O .loc [(OO0OO0OOO000OOO0O ["单位名称"]==OO00OO0O00OO000OO ["中文全称"]),"市级监测机构"]=OO00OO0O00OO000OO ["地市"]#line:2048
		OO0OO0OOO000OOO0O ["监测机构"]=OO0OO0OOO000OOO0O ["监测机构"].fillna ("未规整")#line:2049
		OO0OO0OOO000OOO0O ["市级监测机构"]=OO0OO0OOO000OOO0O ["市级监测机构"].fillna ("未规整")#line:2050
	if O0OOO0OOOOO000OO0 ==True :#line:2051
		return OO0OO0OOO000OOO0O #line:2052
	else :#line:2053
		TABLE_tree_Level_2 (OO0OO0OOO000OOO0O ,0 ,OO0OO0OOO000OOO0O )#line:2054
def TOOL_person (OOOO0O000OOO0O0OO ):#line:2056
	""#line:2057
	O00O0OO0O00O0OOO0 =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="专家列表",header =0 ,index_col =0 ,).reset_index ()#line:2058
	for OO0OO000000O0000O ,OO0O00O0OO0O0O0OO in O00O0OO0O00O0OOO0 .iterrows ():#line:2059
		OOOO0O000OOO0O0OO .loc [(OOOO0O000OOO0O0OO ["市级监测机构"]==OO0O00O0OO0O0O0OO ["市级监测机构"]),"评表人员"]=OO0O00O0OO0O0O0OO ["评表人员"]#line:2060
		OOOO0O000OOO0O0OO ["评表人员"]=OOOO0O000OOO0O0OO ["评表人员"].fillna ("未规整")#line:2061
		OO00O0O00O0O0OOO0 =OOOO0O000OOO0O0OO .groupby (["评表人员"]).agg (报告数量 =("报告编码","nunique"),地市 =("市级监测机构",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:2065
	TABLE_tree_Level_2 (OO00O0O00O0O0OOO0 ,0 ,OO00O0O00O0O0OOO0 )#line:2066
def TOOLS_get_list (O0OO0OO0OO000O00O ):#line:2068
    ""#line:2069
    O0OO0OO0OO000O00O =str (O0OO0OO0OO000O00O )#line:2070
    OOOO0O000O0O00OOO =[]#line:2071
    OOOO0O000O0O00OOO .append (O0OO0OO0OO000O00O )#line:2072
    OOOO0O000O0O00OOO =",".join (OOOO0O000O0O00OOO )#line:2073
    OOOO0O000O0O00OOO =OOOO0O000O0O00OOO .split ("|")#line:2074
    O0O00OO00O000O000 =OOOO0O000O0O00OOO [:]#line:2075
    OOOO0O000O0O00OOO =list (set (OOOO0O000O0O00OOO ))#line:2076
    OOOO0O000O0O00OOO .sort (key =O0O00OO00O000O000 .index )#line:2077
    return OOOO0O000O0O00OOO #line:2078
def TOOLS_get_list0 (O00OOO0000OO000OO ,OO00O0O00000000OO ,*O00000OO0O00O00OO ):#line:2080
    ""#line:2081
    O00OOO0000OO000OO =str (O00OOO0000OO000OO )#line:2082
    if pd .notnull (O00OOO0000OO000OO ):#line:2084
        try :#line:2085
            if "use("in str (O00OOO0000OO000OO ):#line:2086
                OOOO0O0OOOO0O0000 =O00OOO0000OO000OO #line:2087
                O000OOOO00O0O0000 =re .compile (r"[(](.*?)[)]",re .S )#line:2088
                OOOO0OOO00000O000 =re .findall (O000OOOO00O0O0000 ,OOOO0O0OOOO0O0000 )#line:2089
                OOO00O00000O0000O =[]#line:2090
                if ").list"in O00OOO0000OO000OO :#line:2091
                    O0OOOO0O0OO00OOO0 =peizhidir +""+str (OOOO0OOO00000O000 [0 ])+".xls"#line:2092
                    O0OOO0O0OO0O00O0O =pd .read_excel (O0OOOO0O0OO00OOO0 ,sheet_name =OOOO0OOO00000O000 [0 ],header =0 ,index_col =0 ).reset_index ()#line:2095
                    O0OOO0O0OO0O00O0O ["检索关键字"]=O0OOO0O0OO0O00O0O ["检索关键字"].astype (str )#line:2096
                    OOO00O00000O0000O =O0OOO0O0OO0O00O0O ["检索关键字"].tolist ()+OOO00O00000O0000O #line:2097
                if ").file"in O00OOO0000OO000OO :#line:2098
                    OOO00O00000O0000O =OO00O0O00000000OO [OOOO0OOO00000O000 [0 ]].astype (str ).tolist ()+OOO00O00000O0000O #line:2100
                try :#line:2103
                    if "报告类型-新的"in OO00O0O00000000OO .columns :#line:2104
                        OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2105
                        OOO00O00000O0000O =OOO00O00000O0000O .split (";")#line:2106
                        OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2107
                        OOO00O00000O0000O =OOO00O00000O0000O .split ("；")#line:2108
                        OOO00O00000O0000O =[OOOO0O0OO000000OO .replace ("（严重）","")for OOOO0O0OO000000OO in OOO00O00000O0000O ]#line:2109
                        OOO00O00000O0000O =[OOOOOO0000O0O0OO0 .replace ("（一般）","")for OOOOOO0000O0O0OO0 in OOO00O00000O0000O ]#line:2110
                except :#line:2111
                    pass #line:2112
                OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2115
                OOO00O00000O0000O =OOO00O00000O0000O .split ("、")#line:2116
                OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2117
                OOO00O00000O0000O =OOO00O00000O0000O .split ("，")#line:2118
                OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2119
                OOO00O00000O0000O =OOO00O00000O0000O .split (",")#line:2120
                OO00O0000O0000000 =OOO00O00000O0000O [:]#line:2122
                try :#line:2123
                    if O00000OO0O00O00OO [0 ]==1000 :#line:2124
                      pass #line:2125
                except :#line:2126
                      OOO00O00000O0000O =list (set (OOO00O00000O0000O ))#line:2127
                OOO00O00000O0000O .sort (key =OO00O0000O0000000 .index )#line:2128
            else :#line:2130
                O00OOO0000OO000OO =str (O00OOO0000OO000OO )#line:2131
                OOO00O00000O0000O =[]#line:2132
                OOO00O00000O0000O .append (O00OOO0000OO000OO )#line:2133
                OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2134
                OOO00O00000O0000O =OOO00O00000O0000O .split ("、")#line:2135
                OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2136
                OOO00O00000O0000O =OOO00O00000O0000O .split ("，")#line:2137
                OOO00O00000O0000O =",".join (OOO00O00000O0000O )#line:2138
                OOO00O00000O0000O =OOO00O00000O0000O .split (",")#line:2139
                OO00O0000O0000000 =OOO00O00000O0000O [:]#line:2141
                try :#line:2142
                    if O00000OO0O00O00OO [0 ]==1000 :#line:2143
                      OOO00O00000O0000O =list (set (OOO00O00000O0000O ))#line:2144
                except :#line:2145
                      pass #line:2146
                OOO00O00000O0000O .sort (key =OO00O0000O0000000 .index )#line:2147
                OOO00O00000O0000O .sort (key =OO00O0000O0000000 .index )#line:2148
        except ValueError2 :#line:2150
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:2151
            return False #line:2152
    return OOO00O00000O0000O #line:2154
def TOOLS_easyread2 (O0OOOO0O00O00OO0O ):#line:2156
    ""#line:2157
    O0OOOO0O00O00OO0O ["分隔符"]="●"#line:2159
    O0OOOO0O00O00OO0O ["上报机构描述"]=(O0OOOO0O00O00OO0O ["使用过程"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["事件原因分析"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["事件原因分析描述"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["初步处置情况"].astype ("str"))#line:2168
    O0OOOO0O00O00OO0O ["持有人处理描述"]=(O0OOOO0O00O00OO0O ["关联性评价"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["调查情况"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["事件原因分析"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["具体控制措施"].astype ("str")+O0OOOO0O00O00OO0O ["分隔符"]+O0OOOO0O00O00OO0O ["未采取控制措施原因"].astype ("str"))#line:2179
    O0OO0OO0OOO0O0O0O =O0OOOO0O00O00OO0O [["报告编码","事件发生日期","报告日期","单位名称","产品名称","注册证编号/曾用注册证编号","产品批号","型号","规格","上市许可持有人名称","管理类别","伤害","伤害表现","器械故障表现","上报机构描述","持有人处理描述","经营企业使用单位报告状态","监测机构","产品类别","医疗机构类别","年龄","年龄类型","性别"]]#line:2206
    O0OO0OO0OOO0O0O0O =O0OO0OO0OOO0O0O0O .sort_values (by =["事件发生日期"],ascending =[False ],na_position ="last",)#line:2211
    O0OO0OO0OOO0O0O0O =O0OO0OO0OOO0O0O0O .rename (columns ={"报告编码":"规整编码"})#line:2212
    return O0OO0OO0OOO0O0O0O #line:2213
def fenci0 (OOOOOOOO0O000OO0O ):#line:2216
	""#line:2217
	OO000OO00000OO000 =Toplevel ()#line:2218
	OO000OO00000OO000 .title ('词频统计')#line:2219
	OOOO0O00O0O000O0O =OO000OO00000OO000 .winfo_screenwidth ()#line:2220
	O0OOOOOO0O00OOO0O =OO000OO00000OO000 .winfo_screenheight ()#line:2222
	O0OOOOOOO00O00O0O =400 #line:2224
	OO0O0OOOOO00OO000 =120 #line:2225
	O0O00O000000OOO0O =(OOOO0O00O0O000O0O -O0OOOOOOO00O00O0O )/2 #line:2227
	OOOO00O0O0OO00O0O =(O0OOOOOO0O00OOO0O -OO0O0OOOOO00OO000 )/2 #line:2228
	OO000OO00000OO000 .geometry ("%dx%d+%d+%d"%(O0OOOOOOO00O00O0O ,OO0O0OOOOO00OO000 ,O0O00O000000OOO0O ,OOOO00O0O0OO00O0O ))#line:2229
	O0O0O00O0000O0O00 =Label (OO000OO00000OO000 ,text ="配置文件：")#line:2230
	O0O0O00O0000O0O00 .pack ()#line:2231
	OO0000O000OOO0O0O =Label (OO000OO00000OO000 ,text ="需要分词的列：")#line:2232
	O00OOOO0OOOOOO0OO =Entry (OO000OO00000OO000 ,width =80 )#line:2234
	O00OOOO0OOOOOO0OO .insert (0 ,peizhidir +"0（范例）中文分词工作文件.xls")#line:2235
	O0OOO000OOOOO0O00 =Entry (OO000OO00000OO000 ,width =80 )#line:2236
	O0OOO000OOOOO0O00 .insert (0 ,"器械故障表现，伤害表现")#line:2237
	O00OOOO0OOOOOO0OO .pack ()#line:2238
	OO0000O000OOO0O0O .pack ()#line:2239
	O0OOO000OOOOO0O00 .pack ()#line:2240
	OO0O0O000O0OOOOO0 =LabelFrame (OO000OO00000OO000 )#line:2241
	OOO0O0OO0OO0000OO =Button (OO0O0O000O0OOOOO0 ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (tree_Level_2 ,fenci (O00OOOO0OOOOOO0OO .get (),O0OOO000OOOOO0O00 .get (),OOOOOOOO0O000OO0O ),1 ,0 ))#line:2242
	OOO0O0OO0OO0000OO .pack (side =LEFT ,padx =1 ,pady =1 )#line:2243
	OO0O0O000O0OOOOO0 .pack ()#line:2244
def fenci (OOOO0OOO00O00OO00 ,OOO00OO0O0O0OO0O0 ,O0OO0O0O0OOOOOOOO ):#line:2246
    ""#line:2247
    import glob #line:2248
    import jieba #line:2249
    import random #line:2250
    try :#line:2252
        O0OO0O0O0OOOOOOOO =O0OO0O0O0OOOOOOOO .drop_duplicates (["报告编码"])#line:2253
    except :#line:2254
        pass #line:2255
    def OOOOO00000OO0OOOO (O00O000000OOOOOOO ,O00OOOO000000000O ):#line:2256
        OO00OOO000OOOO0O0 ={}#line:2257
        for O0O00OOOOOOOOOO0O in O00O000000OOOOOOO :#line:2258
            OO00OOO000OOOO0O0 [O0O00OOOOOOOOOO0O ]=OO00OOO000OOOO0O0 .get (O0O00OOOOOOOOOO0O ,0 )+1 #line:2259
        return sorted (OO00OOO000OOOO0O0 .items (),key =lambda OOO0OO0OO0O00OO00 :OOO0OO0OO0O00OO00 [1 ],reverse =True )[:O00OOOO000000000O ]#line:2260
    O000OOOOO0O00O0O0 =pd .read_excel (OOOO0OOO00O00OO00 ,sheet_name ="初始化",header =0 ,index_col =0 ).reset_index ()#line:2264
    O0O0O000O0O0O00OO =O000OOOOO0O00O0O0 .iloc [0 ,2 ]#line:2266
    O0OO0O00OOO0OOO0O =pd .read_excel (OOOO0OOO00O00OO00 ,sheet_name ="停用词",header =0 ,index_col =0 ).reset_index ()#line:2269
    O0OO0O00OOO0OOO0O ["停用词"]=O0OO0O00OOO0OOO0O ["停用词"].astype (str )#line:2271
    OO0O0O00O0OO00O0O =[OO0O00OOO00O00OO0 .strip ()for OO0O00OOO00O00OO0 in O0OO0O00OOO0OOO0O ["停用词"]]#line:2272
    O0OO0O000O0O0OOOO =pd .read_excel (OOOO0OOO00O00OO00 ,sheet_name ="本地词库",header =0 ,index_col =0 ).reset_index ()#line:2275
    OOOO00O0OOOO00OOO =O0OO0O000O0O0OOOO ["本地词库"]#line:2276
    jieba .load_userdict (OOOO00O0OOOO00OOO )#line:2277
    O00000OOO00000OO0 =""#line:2280
    OOOO0000O0OO000OO =get_list0 (OOO00OO0O0O0OO0O0 ,O0OO0O0O0OOOOOOOO )#line:2283
    try :#line:2284
        for OO0O0O000O00OOO00 in OOOO0000O0OO000OO :#line:2285
            for O000OOOOOO0O0O00O in O0OO0O0O0OOOOOOOO [OO0O0O000O00OOO00 ]:#line:2286
                O00000OOO00000OO0 =O00000OOO00000OO0 +str (O000OOOOOO0O0O00O )#line:2287
    except :#line:2288
        text .insert (END ,"分词配置文件未正确设置，将对整个表格进行分词。")#line:2289
        for OO0O0O000O00OOO00 in O0OO0O0O0OOOOOOOO .columns .tolist ():#line:2290
            for O000OOOOOO0O0O00O in O0OO0O0O0OOOOOOOO [OO0O0O000O00OOO00 ]:#line:2291
                O00000OOO00000OO0 =O00000OOO00000OO0 +str (O000OOOOOO0O0O00O )#line:2292
    OO0OOOOO0O00O00O0 =[]#line:2293
    OO0OOOOO0O00O00O0 =OO0OOOOO0O00O00O0 +[O0OOOOO0O0O00OOO0 for O0OOOOO0O0O00OOO0 in jieba .cut (O00000OOO00000OO0 )if O0OOOOO0O0O00OOO0 not in OO0O0O00O0OO00O0O ]#line:2294
    OO0OOOO0O000O0OO0 =dict (OOOOO00000OO0OOOO (OO0OOOOO0O00O00O0 ,O0O0O000O0O0O00OO ))#line:2295
    OOOO0OOOO0O00O00O =pd .DataFrame ([OO0OOOO0O000O0OO0 ]).T #line:2296
    OOOO0OOOO0O00O00O =OOOO0OOOO0O00O00O .reset_index ()#line:2297
    return OOOO0OOOO0O00O00O #line:2298
def TOOLS_time (O00OO0OO00O0000O0 ,OOO000OOOOO00O00O ,OO0OO00O0000OOO00 ):#line:2300
	""#line:2301
	O0OO0000000O0OO0O =O00OO0OO00O0000O0 .drop_duplicates (["报告编码"]).groupby ([OOO000OOOOO00O00O ]).agg (报告总数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda O0O000O0OO00O0O00 :STAT_countpx (O0O000O0OO00O0O00 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O00OOO00OO00OOO :STAT_countpx (O0O00OOO00OO00OOO .values ,"死亡")),).sort_values (by =OOO000OOOOO00O00O ,ascending =[True ],na_position ="last").reset_index ()#line:2306
	O0OO0000000O0OO0O =O0OO0000000O0OO0O .set_index (OOO000OOOOO00O00O )#line:2310
	O0OO0000000O0OO0O =O0OO0000000O0OO0O .resample ('D').asfreq (fill_value =0 )#line:2312
	O0OO0000000O0OO0O ["time"]=O0OO0000000O0OO0O .index .values #line:2314
	O0OO0000000O0OO0O ["time"]=pd .to_datetime (O0OO0000000O0OO0O ["time"],format ="%Y/%m/%d").dt .date #line:2315
	if OO0OO00O0000OOO00 ==1 :#line:2317
		return O0OO0000000O0OO0O .reset_index (drop =True )#line:2319
	O0OO0000000O0OO0O ["30天累计数"]=O0OO0000000O0OO0O ["报告总数"].rolling (30 ,min_periods =1 ).agg (lambda OOO0OOO0O0O000000 :sum (OOO0OOO0O0O000000 )).astype (int )#line:2321
	O0OO0000000O0OO0O ["30天严重伤害累计数"]=O0OO0000000O0OO0O ["严重伤害数"].rolling (30 ,min_periods =1 ).agg (lambda O00O0OO0O0O0O0O0O :sum (O00O0OO0O0O0O0O0O )).astype (int )#line:2322
	O0OO0000000O0OO0O ["30天死亡累计数"]=O0OO0000000O0OO0O ["死亡数量"].rolling (30 ,min_periods =1 ).agg (lambda OO000OOOO0OO0OOO0 :sum (OO000OOOO0OO0OOO0 )).astype (int )#line:2323
	O0OO0000000O0OO0O .loc [(((O0OO0000000O0OO0O ["30天累计数"]>=3 )&(O0OO0000000O0OO0O ["30天严重伤害累计数"]>=1 ))|(O0OO0000000O0OO0O ["30天累计数"]>=5 )|(O0OO0000000O0OO0O ["30天死亡累计数"]>=1 )),"关注区域"]=O0OO0000000O0OO0O ["30天累计数"]#line:2344
	DRAW_make_risk_plot (O0OO0000000O0OO0O ,"time",["30天累计数","30天严重伤害累计数","关注区域"],"折线图",999 )#line:2349
def TOOLS_keti (O0O0O00O00O000000 ):#line:2353
	""#line:2354
	import datetime #line:2355
	def O0OOOO0OOOO000OO0 (OO000O000OO0O0O0O ,O00O00000O0OOO0OO ):#line:2357
		if ini ["模式"]=="药品":#line:2358
			OO0OOOO0O000OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:2359
		if ini ["模式"]=="器械":#line:2360
			OO0OOOO0O000OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:2361
		if ini ["模式"]=="化妆品":#line:2362
			OO0OOOO0O000OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:2363
		OOOO00OOOOO0O000O =OO0OOOO0O000OO00O ["权重"][0 ]#line:2364
		OOOO00OO0O0OOOO00 =OO0OOOO0O000OO00O ["权重"][1 ]#line:2365
		O00000000OOO00O00 =OO0OOOO0O000OO00O ["权重"][2 ]#line:2366
		O0000O0O0OO0O0OO0 =OO0OOOO0O000OO00O ["权重"][3 ]#line:2367
		OO00000O0O0OOOO0O =OO0OOOO0O000OO00O ["值"][3 ]#line:2368
		OOO0O0OO000OO0OOO =OO0OOOO0O000OO00O ["权重"][4 ]#line:2370
		O0O00O0OOO0OO0O00 =OO0OOOO0O000OO00O ["值"][4 ]#line:2371
		OO00O0OO00OOOOO0O =OO0OOOO0O000OO00O ["权重"][5 ]#line:2373
		OO00000000OOO0000 =OO0OOOO0O000OO00O ["值"][5 ]#line:2374
		O0OO0O0OO0O00OOOO =OO0OOOO0O000OO00O ["权重"][6 ]#line:2376
		O0O00OOO0OO0O00O0 =OO0OOOO0O000OO00O ["值"][6 ]#line:2377
		O0O0OOO00O0OOOOO0 =pd .to_datetime (OO000O000OO0O0O0O )#line:2379
		OO0OO0OOOOO0OOO0O =O00O00000O0OOO0OO .copy ().set_index ('报告日期')#line:2380
		OO0OO0OOOOO0OOO0O =OO0OO0OOOOO0OOO0O .sort_index ()#line:2381
		if ini ["模式"]=="器械":#line:2382
			OO0OO0OOOOO0OOO0O ["关键字查找列"]=OO0OO0OOOOO0OOO0O ["器械故障表现"].astype (str )+OO0OO0OOOOO0OOO0O ["伤害表现"].astype (str )+OO0OO0OOOOO0OOO0O ["使用过程"].astype (str )+OO0OO0OOOOO0OOO0O ["事件原因分析描述"].astype (str )+OO0OO0OOOOO0OOO0O ["初步处置情况"].astype (str )#line:2383
		else :#line:2384
			OO0OO0OOOOO0OOO0O ["关键字查找列"]=OO0OO0OOOOO0OOO0O ["器械故障表现"].astype (str )#line:2385
		OO0OO0OOOOO0OOO0O .loc [OO0OO0OOOOO0OOO0O ["关键字查找列"].str .contains (OO00000O0O0OOOO0O ,na =False ),"高度关注关键字"]=1 #line:2386
		OO0OO0OOOOO0OOO0O .loc [OO0OO0OOOOO0OOO0O ["关键字查找列"].str .contains (O0O00O0OOO0OO0O00 ,na =False ),"二级敏感词"]=1 #line:2387
		OO0OO0OOOOO0OOO0O .loc [OO0OO0OOOOO0OOO0O ["关键字查找列"].str .contains (OO00000000OOO0000 ,na =False ),"减分项"]=1 #line:2388
		OOOO0O00O00OOO0O0 =OO0OO0OOOOO0OOO0O .loc [O0O0OOO00O0OOOOO0 -pd .Timedelta (days =30 ):O0O0OOO00O0OOOOO0 ].reset_index ()#line:2390
		OO000O0OO0O00OOOO =OO0OO0OOOOO0OOO0O .loc [O0O0OOO00O0OOOOO0 -pd .Timedelta (days =365 ):O0O0OOO00O0OOOOO0 ].reset_index ()#line:2391
		O000000O00OO00O0O =OOOO0O00O00OOO0O0 .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:2404
		O000000O0O0OO000O =OOOO0O00O00OOO0O0 .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda O0OOO0OOOOO0O00OO :STAT_countpx (O0OOO0OOOOO0O00OO .values ,"严重伤害")),死亡数量 =("伤害",lambda O000O0OO000O0000O :STAT_countpx (O000O0OO000O0000O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OO000O00OOOOO00OO :STAT_countpx (OO000O00OOOOO00OO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O00OOOO00O0OOO00O :STAT_countpx (O00OOOO00O0OOO00O .values ,"严重伤害待评价")),高度关注关键字 =("高度关注关键字","sum"),二级敏感词 =("二级敏感词","sum"),减分项 =("减分项","sum"),).reset_index ()#line:2416
		O0OO0O0OO0O0000OO =pd .merge (O000000O00OO00O0O ,O000000O0O0OO000O ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2418
		O0O0O000O00O0OO00 =OOOO0O00O00OOO0O0 .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:2425
		O0O0O000O00O0OO00 =O0O0O000O00O0OO00 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2426
		O00O000O00OO0OOOO =OOOO0O00O00OOO0O0 .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda OOO00OO0OO00O00O0 :STAT_countpx (OOO00OO0OO00O00O0 .values ,"严重伤害")),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:2431
		O00O000O00OO0OOOO ["风险评分-影响"]=0 #line:2435
		O00O000O00OO0OOOO ["评分说明"]=""#line:2436
		O00O000O00OO0OOOO .loc [((O00O000O00OO0OOOO ["批号计数"]>=3 )&(O00O000O00OO0OOOO ["严重伤害数"]>=1 )&(O00O000O00OO0OOOO ["产品类别"]!="有源"))|((O00O000O00OO0OOOO ["批号计数"]>=5 )&(O00O000O00OO0OOOO ["产品类别"]!="有源")),"风险评分-影响"]=O00O000O00OO0OOOO ["风险评分-影响"]+3 #line:2437
		O00O000O00OO0OOOO .loc [(O00O000O00OO0OOOO ["风险评分-影响"]>=3 ),"评分说明"]=O00O000O00OO0OOOO ["评分说明"]+"●符合省中心无源规则+3;"#line:2438
		O00O000O00OO0OOOO =O00O000O00OO0OOOO .sort_values (by ="风险评分-影响",ascending =[False ],na_position ="last").reset_index (drop =True )#line:2442
		O00O000O00OO0OOOO =O00O000O00OO0OOOO .drop_duplicates ("注册证编号/曾用注册证编号")#line:2443
		O0O0O000O00O0OO00 =O0O0O000O00O0OO00 [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号","型号计数"]]#line:2444
		O00O000O00OO0OOOO =O00O000O00OO0OOOO [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号","批号计数","风险评分-影响","评分说明"]]#line:2445
		O0OO0O0OO0O0000OO =pd .merge (O0OO0O0OO0O0000OO ,O0O0O000O00O0OO00 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2446
		O0OO0O0OO0O0000OO =pd .merge (O0OO0O0OO0O0000OO ,O00O000O00OO0OOOO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2448
		O0OO0O0OO0O0000OO .loc [((O0OO0O0OO0O0000OO ["证号计数"]>=3 )&(O0OO0O0OO0O0000OO ["严重伤害数"]>=1 )&(O0OO0O0OO0O0000OO ["产品类别"]=="有源"))|((O0OO0O0OO0O0000OO ["证号计数"]>=5 )&(O0OO0O0OO0O0000OO ["产品类别"]=="有源")),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+3 #line:2452
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-影响"]>=3 )&(O0OO0O0OO0O0000OO ["产品类别"]=="有源"),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"●符合省中心有源规则+3;"#line:2453
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["死亡数量"]>=1 ),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+10 #line:2458
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-影响"]>=10 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"存在死亡报告;"#line:2459
		OOO0OOO0O00000OOO =round (OOOO00OOOOO0O000O *(O0OO0O0OO0O0000OO ["严重伤害数"]/O0OO0O0OO0O0000OO ["证号计数"]),2 )#line:2462
		O0OO0O0OO0O0000OO ["风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+OOO0OOO0O00000OOO #line:2463
		O0OO0O0OO0O0000OO ["评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"严重比评分"+OOO0OOO0O00000OOO .astype (str )+";"#line:2464
		OOOO000000OO0O000 =round (OOOO00OO0O0OOOO00 *(np .log (O0OO0O0OO0O0000OO ["单位个数"])),2 )#line:2467
		O0OO0O0OO0O0000OO ["风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+OOOO000000OO0O000 #line:2468
		O0OO0O0OO0O0000OO ["评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"报告单位评分"+OOOO000000OO0O000 .astype (str )+";"#line:2469
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["产品类别"]=="有源")&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+O00000000OOO00O00 *O0OO0O0OO0O0000OO ["型号计数"]/O0OO0O0OO0O0000OO ["证号计数"]#line:2472
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["产品类别"]=="有源")&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"型号集中度评分"+(round (O00000000OOO00O00 *O0OO0O0OO0O0000OO ["型号计数"]/O0OO0O0OO0O0000OO ["证号计数"],2 )).astype (str )+";"#line:2473
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["产品类别"]!="有源")&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+O00000000OOO00O00 *O0OO0O0OO0O0000OO ["批号计数"]/O0OO0O0OO0O0000OO ["证号计数"]#line:2474
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["产品类别"]!="有源")&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"批号集中度评分"+(round (O00000000OOO00O00 *O0OO0O0OO0O0000OO ["批号计数"]/O0OO0O0OO0O0000OO ["证号计数"],2 )).astype (str )+";"#line:2475
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["高度关注关键字"]>=1 ),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+O0000O0O0OO0O0OO0 #line:2478
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["高度关注关键字"]>=1 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"●含有高度关注关键字评分"+str (O0000O0O0OO0O0OO0 )+"；"#line:2479
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["二级敏感词"]>=1 ),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+OOO0O0OO000OO0OOO #line:2482
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["二级敏感词"]>=1 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"含有二级敏感词评分"+str (OOO0O0OO000OO0OOO )+"；"#line:2483
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["减分项"]>=1 ),"风险评分-影响"]=O0OO0O0OO0O0000OO ["风险评分-影响"]+OO00O0OO00OOOOO0O #line:2486
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["减分项"]>=1 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"减分项评分"+str (OO00O0OO00OOOOO0O )+"；"#line:2487
		OOO0O0OO0O0000OO0 =Countall (OO000O0OO0O00OOOO ).df_findrisk ("事件发生月份")#line:2490
		OOO0O0OO0O0000OO0 =OOO0O0OO0O0000OO0 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2491
		OOO0O0OO0O0000OO0 =OOO0O0OO0O0000OO0 [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2492
		O0OO0O0OO0O0000OO =pd .merge (O0OO0O0OO0O0000OO ,OOO0O0OO0O0000OO0 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2493
		O0OO0O0OO0O0000OO ["风险评分-月份"]=1 #line:2495
		O0OO0O0OO0O0000OO ["mfc"]=""#line:2496
		O0OO0O0OO0O0000OO .loc [((O0OO0O0OO0O0000OO ["证号计数"]>O0OO0O0OO0O0000OO ["均值"])&(O0OO0O0OO0O0000OO ["标准差"].astype (str )=="nan")),"风险评分-月份"]=O0OO0O0OO0O0000OO ["风险评分-月份"]+1 #line:2497
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>O0OO0O0OO0O0000OO ["均值"]),"mfc"]="月份计数超过历史均值"+O0OO0O0OO0O0000OO ["均值"].astype (str )+"；"#line:2498
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=(O0OO0O0OO0O0000OO ["均值"]+O0OO0O0OO0O0000OO ["标准差"]))&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"风险评分-月份"]=O0OO0O0OO0O0000OO ["风险评分-月份"]+1 #line:2500
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=(O0OO0O0OO0O0000OO ["均值"]+O0OO0O0OO0O0000OO ["标准差"]))&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"mfc"]="月份计数超过3例超过历史均值一个标准差("+O0OO0O0OO0O0000OO ["标准差"].astype (str )+")；"#line:2501
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"风险评分-月份"]=O0OO0O0OO0O0000OO ["风险评分-月份"]+2 #line:2503
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=3 ),"mfc"]="月份计数超过3例且超过历史95%CI上限("+O0OO0O0OO0O0000OO ["CI上限"].astype (str )+")；"#line:2504
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=5 ),"风险评分-月份"]=O0OO0O0OO0O0000OO ["风险评分-月份"]+1 #line:2506
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=5 ),"mfc"]="月份计数超过5例且超过历史95%CI上限("+O0OO0O0OO0O0000OO ["CI上限"].astype (str )+")；"#line:2507
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=7 ),"风险评分-月份"]=O0OO0O0OO0O0000OO ["风险评分-月份"]+1 #line:2509
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=7 ),"mfc"]="月份计数超过7例且超过历史95%CI上限("+O0OO0O0OO0O0000OO ["CI上限"].astype (str )+")；"#line:2510
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=9 ),"风险评分-月份"]=O0OO0O0OO0O0000OO ["风险评分-月份"]+1 #line:2512
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["证号计数"]>=9 ),"mfc"]="月份计数超过9例且超过历史95%CI上限("+O0OO0O0OO0O0000OO ["CI上限"].astype (str )+")；"#line:2513
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=3 )&(O0OO0O0OO0O0000OO ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2517
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["证号计数"]>=3 )&(O0OO0O0OO0O0000OO ["标准差"].astype (str )=="nan"),"mfc"]="无历史数据但数量超过3例；"#line:2518
		O0OO0O0OO0O0000OO ["评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"●●证号数量："+O0OO0O0OO0O0000OO ["证号计数"].astype (str )+";"+O0OO0O0OO0O0000OO ["mfc"]#line:2521
		del O0OO0O0OO0O0000OO ["mfc"]#line:2522
		O0OO0O0OO0O0000OO =O0OO0O0OO0O0000OO .rename (columns ={"均值":"月份均值","标准差":"月份标准差","CI上限":"月份CI上限"})#line:2523
		OOO0O0OO0O0000OO0 =Countall (OO000O0OO0O00OOOO ).df_findrisk ("产品批号")#line:2527
		OOO0O0OO0O0000OO0 =OOO0O0OO0O0000OO0 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2528
		OOO0O0OO0O0000OO0 =OOO0O0OO0O0000OO0 [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2529
		O0OO0O0OO0O0000OO =pd .merge (O0OO0O0OO0O0000OO ,OOO0O0OO0O0000OO0 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2530
		O0OO0O0OO0O0000OO ["风险评分-批号"]=1 #line:2532
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["产品类别"]!="有源"),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"●●高峰批号数量："+O0OO0O0OO0O0000OO ["批号计数"].astype (str )+";"#line:2533
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>O0OO0O0OO0O0000OO ["均值"]),"风险评分-批号"]=O0OO0O0OO0O0000OO ["风险评分-批号"]+1 #line:2535
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>O0OO0O0OO0O0000OO ["均值"]),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"高峰批号计数超过历史均值"+O0OO0O0OO0O0000OO ["均值"].astype (str )+"；"#line:2536
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>(O0OO0O0OO0O0000OO ["均值"]+O0OO0O0OO0O0000OO ["标准差"]))&(O0OO0O0OO0O0000OO ["批号计数"]>=3 ),"风险评分-批号"]=O0OO0O0OO0O0000OO ["风险评分-批号"]+1 #line:2537
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>(O0OO0O0OO0O0000OO ["均值"]+O0OO0O0OO0O0000OO ["标准差"]))&(O0OO0O0OO0O0000OO ["批号计数"]>=3 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"高峰批号计数超过3例超过历史均值一个标准差("+O0OO0O0OO0O0000OO ["标准差"].astype (str )+")；"#line:2538
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["批号计数"]>=3 ),"风险评分-批号"]=O0OO0O0OO0O0000OO ["风险评分-批号"]+1 #line:2539
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>O0OO0O0OO0O0000OO ["CI上限"])&(O0OO0O0OO0O0000OO ["批号计数"]>=3 ),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"高峰批号计数超过3例且超过历史95%CI上限("+O0OO0O0OO0O0000OO ["CI上限"].astype (str )+")；"#line:2540
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>=3 )&(O0OO0O0OO0O0000OO ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2542
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["批号计数"]>=3 )&(O0OO0O0OO0O0000OO ["标准差"].astype (str )=="nan"),"评分说明"]=O0OO0O0OO0O0000OO ["评分说明"]+"无历史数据但数量超过3例；"#line:2543
		O0OO0O0OO0O0000OO =O0OO0O0OO0O0000OO .rename (columns ={"均值":"高峰批号均值","标准差":"高峰批号标准差","CI上限":"高峰批号CI上限"})#line:2544
		O0OO0O0OO0O0000OO ["风险评分-影响"]=round (O0OO0O0OO0O0000OO ["风险评分-影响"],2 )#line:2547
		O0OO0O0OO0O0000OO ["风险评分-月份"]=round (O0OO0O0OO0O0000OO ["风险评分-月份"],2 )#line:2548
		O0OO0O0OO0O0000OO ["风险评分-批号"]=round (O0OO0O0OO0O0000OO ["风险评分-批号"],2 )#line:2549
		O0OO0O0OO0O0000OO ["总体评分"]=O0OO0O0OO0O0000OO ["风险评分-影响"].copy ()#line:2551
		O0OO0O0OO0O0000OO ["关注建议"]=""#line:2552
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-影响"]>=3 ),"关注建议"]=O0OO0O0OO0O0000OO ["关注建议"]+"●建议关注(影响范围)；"#line:2553
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-月份"]>=3 ),"关注建议"]=O0OO0O0OO0O0000OO ["关注建议"]+"●建议关注(当月数量异常)；"#line:2554
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-批号"]>=3 ),"关注建议"]=O0OO0O0OO0O0000OO ["关注建议"]+"●建议关注(高峰批号数量异常)。"#line:2555
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-月份"]>=O0OO0O0OO0O0000OO ["风险评分-批号"]),"总体评分"]=O0OO0O0OO0O0000OO ["风险评分-影响"]*O0OO0O0OO0O0000OO ["风险评分-月份"]#line:2559
		O0OO0O0OO0O0000OO .loc [(O0OO0O0OO0O0000OO ["风险评分-月份"]<O0OO0O0OO0O0000OO ["风险评分-批号"]),"总体评分"]=O0OO0O0OO0O0000OO ["风险评分-影响"]*O0OO0O0OO0O0000OO ["风险评分-批号"]#line:2560
		O0OO0O0OO0O0000OO ["总体评分"]=round (O0OO0O0OO0O0000OO ["总体评分"],2 )#line:2562
		O0OO0O0OO0O0000OO ["评分说明"]=O0OO0O0OO0O0000OO ["关注建议"]+O0OO0O0OO0O0000OO ["评分说明"]#line:2563
		O0OO0O0OO0O0000OO =O0OO0O0OO0O0000OO .sort_values (by =["总体评分","风险评分-影响"],ascending =[False ,False ],na_position ="last").reset_index (drop =True )#line:2564
		O0OO0O0OO0O0000OO ["主要故障分类"]=""#line:2567
		for O0OOO00O0O0OOOOO0 ,O0O0O00O0O000O0OO in O0OO0O0OO0O0000OO .iterrows ():#line:2568
			O0OO0OOOO00OOOOO0 =OOOO0O00O00OOO0O0 [(OOOO0O00O00OOO0O0 ["注册证编号/曾用注册证编号"]==O0O0O00O0O000O0OO ["注册证编号/曾用注册证编号"])].copy ()#line:2569
			if O0O0O00O0O000O0OO ["总体评分"]>=float (O0OO0O0OO0O00OOOO ):#line:2570
				if O0O0O00O0O000O0OO ["规整后品类"]!="N":#line:2571
					O0OO00O000000O00O =Countall (O0OO0OOOO00OOOOO0 ).df_psur ("特定品种",O0O0O00O0O000O0OO ["规整后品类"])#line:2572
				elif O0O0O00O0O000O0OO ["产品类别"]=="无源":#line:2573
					O0OO00O000000O00O =Countall (O0OO0OOOO00OOOOO0 ).df_psur ("通用无源")#line:2574
				elif O0O0O00O0O000O0OO ["产品类别"]=="有源":#line:2575
					O0OO00O000000O00O =Countall (O0OO0OOOO00OOOOO0 ).df_psur ("通用有源")#line:2576
				elif O0O0O00O0O000O0OO ["产品类别"]=="体外诊断试剂":#line:2577
					O0OO00O000000O00O =Countall (O0OO0OOOO00OOOOO0 ).df_psur ("体外诊断试剂")#line:2578
				OO0OO000000O00000 =O0OO00O000000O00O [["事件分类","总数量"]].copy ()#line:2580
				O0OO000O0O0000000 =""#line:2581
				for O0O0OO00OO0OO00O0 ,O000000O00OO0OOOO in OO0OO000000O00000 .iterrows ():#line:2582
					O0OO000O0O0000000 =O0OO000O0O0000000 +str (O000000O00OO0OOOO ["事件分类"])+":"+str (O000000O00OO0OOOO ["总数量"])+";"#line:2583
				O0OO0O0OO0O0000OO .loc [O0OOO00O0O0OOOOO0 ,"主要故障分类"]=O0OO000O0O0000000 #line:2584
			else :#line:2585
				break #line:2586
		O0OO0O0OO0O0000OO =O0OO0O0OO0O0000OO [["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","证号计数","严重伤害数","死亡数量","总体评分","风险评分-影响","风险评分-月份","风险评分-批号","主要故障分类","评分说明","单位个数","单位列表","批号个数","批号列表","型号个数","型号列表","规格个数","规格列表","待评价数","严重伤害待评价数","高度关注关键字","二级敏感词","月份均值","月份标准差","月份CI上限","高峰批号均值","高峰批号标准差","高峰批号CI上限","型号","型号计数","产品批号","批号计数"]]#line:2590
		O0OO0O0OO0O0000OO ["报表类型"]="dfx_zhenghao"#line:2591
		TABLE_tree_Level_2 (O0OO0O0OO0O0000OO ,1 ,OOOO0O00O00OOO0O0 ,OO000O0OO0O00OOOO )#line:2592
		pass #line:2593
	OO0O00OOO0O000OO0 =Toplevel ()#line:2596
	OO0O00OOO0O000OO0 .title ('风险预警')#line:2597
	O0000000O0OO0O00O =OO0O00OOO0O000OO0 .winfo_screenwidth ()#line:2598
	O00000OO00O0O0OO0 =OO0O00OOO0O000OO0 .winfo_screenheight ()#line:2600
	O0O0OOO000OO0O0OO =350 #line:2602
	O00OO0O0O0OO00O0O =35 #line:2603
	OO0OOOOOOO00OO0O0 =(O0000000O0OO0O00O -O0O0OOO000OO0O0OO )/2 #line:2605
	O0O00O00000O0OO0O =(O00000OO00O0O0OO0 -O00OO0O0O0OO00O0O )/2 #line:2606
	OO0O00OOO0O000OO0 .geometry ("%dx%d+%d+%d"%(O0O0OOO000OO0O0OO ,O00OO0O0O0OO00O0O ,OO0OOOOOOO00OO0O0 ,O0O00O00000O0OO0O ))#line:2607
	OOO00000OOO00O00O =Label (OO0O00OOO0O000OO0 ,text ="预警日期：")#line:2609
	OOO00000OOO00O00O .grid (row =1 ,column =0 ,sticky ="w")#line:2610
	OOO0OOO00OO00O000 =Entry (OO0O00OOO0O000OO0 ,width =30 )#line:2611
	OOO0OOO00OO00O000 .insert (0 ,datetime .date .today ())#line:2612
	OOO0OOO00OO00O000 .grid (row =1 ,column =1 ,sticky ="w")#line:2613
	OOO0O00OO0O00000O =Button (OO0O00OOO0O000OO0 ,text ="确定",width =10 ,command =lambda :TABLE_tree_Level_2 (O0OOOO0OOOO000OO0 (OOO0OOO00OO00O000 .get (),O0O0O00O00O000000 ),1 ,O0O0O00O00O000000 ))#line:2617
	OOO0O00OO0O00000O .grid (row =1 ,column =3 ,sticky ="w")#line:2618
	pass #line:2620
def TOOLS_autocount (OO00OO00OOOO00O0O ,OOOOOO0OO0OO0OO00 ):#line:2622
    ""#line:2623
    OO0OO0O000O000O0O =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ).reset_index ()#line:2626
    O0OO0O0O0OO0OOOO0 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ).reset_index ()#line:2629
    OO00O0O0O00OO0000 =O0OO0O0O0OO0OOOO0 [(O0OO0O0O0OO0OOOO0 ["是否属于二级以上医疗机构"]=="是")]#line:2630
    if OOOOOO0OO0OO0OO00 =="药品":#line:2633
        OO00OO00OOOO00O0O =OO00OO00OOOO00O0O .reset_index (drop =True )#line:2634
        if "再次使用可疑药是否出现同样反应"not in OO00OO00OOOO00O0O .columns :#line:2635
            showinfo (title ="错误信息",message ="导入的疑似不是药品报告表。")#line:2636
            return 0 #line:2637
        OOO0O0O000OOOO000 =Countall (OO00OO00OOOO00O0O ).df_org ("监测机构")#line:2639
        OOO0O0O000OOOO000 =pd .merge (OOO0O0O000OOOO000 ,OO0OO0O000O000O0O ,on ="监测机构",how ="left")#line:2640
        OOO0O0O000OOOO000 =OOO0O0O000OOOO000 [["监测机构序号","监测机构","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2641
        O00000000O0O00OOO =["药品数量指标","审核通过数","报告数量"]#line:2642
        OOO0O0O000OOOO000 [O00000000O0O00OOO ]=OOO0O0O000OOOO000 [O00000000O0O00OOO ].apply (lambda O00O00000OOO0OOO0 :O00O00000OOO0OOO0 .astype (int ))#line:2643
        OO0OOOOOO0OOO0OO0 =Countall (OO00OO00OOOO00O0O ).df_user ()#line:2645
        OO0OOOOOO0OOO0OO0 =pd .merge (OO0OOOOOO0OOO0OO0 ,O0OO0O0O0OO0OOOO0 ,on =["监测机构","单位名称"],how ="left")#line:2646
        OO0OOOOOO0OOO0OO0 =pd .merge (OO0OOOOOO0OOO0OO0 ,OO0OO0O000O000O0O [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2647
        OO0OOOOOO0OOO0OO0 =OO0OOOOOO0OOO0OO0 [["监测机构序号","监测机构","单位名称","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2649
        O00000000O0O00OOO =["药品数量指标","审核通过数","报告数量"]#line:2650
        OO0OOOOOO0OOO0OO0 [O00000000O0O00OOO ]=OO0OOOOOO0OOO0OO0 [O00000000O0O00OOO ].apply (lambda OOOO00OO00OOOOO00 :OOOO00OO00OOOOO00 .astype (int ))#line:2651
        OOO00OO000O0000OO =pd .merge (OO00O0O0O00OO0000 ,OO0OOOOOO0OOO0OO0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2653
        OOO00OO000O0000OO =OOO00OO000O0000OO [(OOO00OO000O0000OO ["审核通过数"]<1 )]#line:2654
        OOO00OO000O0000OO =OOO00OO000O0000OO [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2655
    if OOOOOO0OO0OO0OO00 =="器械":#line:2657
        OO00OO00OOOO00O0O =OO00OO00OOOO00O0O .reset_index (drop =True )#line:2658
        if "产品编号"not in OO00OO00OOOO00O0O .columns :#line:2659
            showinfo (title ="错误信息",message ="导入的疑似不是器械报告表。")#line:2660
            return 0 #line:2661
        OOO0O0O000OOOO000 =Countall (OO00OO00OOOO00O0O ).df_org ("监测机构")#line:2663
        OOO0O0O000OOOO000 =pd .merge (OOO0O0O000OOOO000 ,OO0OO0O000O000O0O ,on ="监测机构",how ="left")#line:2664
        OOO0O0O000OOOO000 =OOO0O0O000OOOO000 [["监测机构序号","监测机构","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2665
        O00000000O0O00OOO =["器械数量指标","审核通过数","报告数量"]#line:2666
        OOO0O0O000OOOO000 [O00000000O0O00OOO ]=OOO0O0O000OOOO000 [O00000000O0O00OOO ].apply (lambda O0OO00O0OOOO000OO :O0OO00O0OOOO000OO .astype (int ))#line:2667
        OO0OOOOOO0OOO0OO0 =Countall (OO00OO00OOOO00O0O ).df_user ()#line:2669
        OO0OOOOOO0OOO0OO0 =pd .merge (OO0OOOOOO0OOO0OO0 ,O0OO0O0O0OO0OOOO0 ,on =["监测机构","单位名称"],how ="left")#line:2670
        OO0OOOOOO0OOO0OO0 =pd .merge (OO0OOOOOO0OOO0OO0 ,OO0OO0O000O000O0O [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2671
        OO0OOOOOO0OOO0OO0 =OO0OOOOOO0OOO0OO0 [["监测机构序号","监测机构","单位名称","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2673
        O00000000O0O00OOO =["器械数量指标","审核通过数","报告数量"]#line:2674
        OO0OOOOOO0OOO0OO0 [O00000000O0O00OOO ]=OO0OOOOOO0OOO0OO0 [O00000000O0O00OOO ].apply (lambda OO00OO000OOO0000O :OO00OO000OOO0000O .astype (int ))#line:2676
        OOO00OO000O0000OO =pd .merge (OO00O0O0O00OO0000 ,OO0OOOOOO0OOO0OO0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2678
        OOO00OO000O0000OO =OOO00OO000O0000OO [(OOO00OO000O0000OO ["审核通过数"]<1 )]#line:2679
        OOO00OO000O0000OO =OOO00OO000O0000OO [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2680
    if OOOOOO0OO0OO0OO00 =="化妆品":#line:2683
        OO00OO00OOOO00O0O =OO00OO00OOOO00O0O .reset_index (drop =True )#line:2684
        if "初步判断"not in OO00OO00OOOO00O0O .columns :#line:2685
            showinfo (title ="错误信息",message ="导入的疑似不是化妆品报告表。")#line:2686
            return 0 #line:2687
        OOO0O0O000OOOO000 =Countall (OO00OO00OOOO00O0O ).df_org ("监测机构")#line:2689
        OOO0O0O000OOOO000 =pd .merge (OOO0O0O000OOOO000 ,OO0OO0O000O000O0O ,on ="监测机构",how ="left")#line:2690
        OOO0O0O000OOOO000 =OOO0O0O000OOOO000 [["监测机构序号","监测机构","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2691
        O00000000O0O00OOO =["化妆品数量指标","审核通过数","报告数量"]#line:2692
        OOO0O0O000OOOO000 [O00000000O0O00OOO ]=OOO0O0O000OOOO000 [O00000000O0O00OOO ].apply (lambda O00000O0OO0000O0O :O00000O0OO0000O0O .astype (int ))#line:2693
        OO0OOOOOO0OOO0OO0 =Countall (OO00OO00OOOO00O0O ).df_user ()#line:2695
        OO0OOOOOO0OOO0OO0 =pd .merge (OO0OOOOOO0OOO0OO0 ,O0OO0O0O0OO0OOOO0 ,on =["监测机构","单位名称"],how ="left")#line:2696
        OO0OOOOOO0OOO0OO0 =pd .merge (OO0OOOOOO0OOO0OO0 ,OO0OO0O000O000O0O [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2697
        OO0OOOOOO0OOO0OO0 =OO0OOOOOO0OOO0OO0 [["监测机构序号","监测机构","单位名称","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2698
        O00000000O0O00OOO =["化妆品数量指标","审核通过数","报告数量"]#line:2699
        OO0OOOOOO0OOO0OO0 [O00000000O0O00OOO ]=OO0OOOOOO0OOO0OO0 [O00000000O0O00OOO ].apply (lambda O0O00000OO00O00O0 :O0O00000OO00O00O0 .astype (int ))#line:2700
        OOO00OO000O0000OO =pd .merge (OO00O0O0O00OO0000 ,OO0OOOOOO0OOO0OO0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2702
        OOO00OO000O0000OO =OOO00OO000O0000OO [(OOO00OO000O0000OO ["审核通过数"]<1 )]#line:2703
        OOO00OO000O0000OO =OOO00OO000O0000OO [["监测机构","单位名称","报告数量","审核通过数"]]#line:2704
    O0OO0O0OOO0O0OOO0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile =OOOOOO0OO0OO0OO00 ,defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:2711
    O00OO0O00OOO00OO0 =pd .ExcelWriter (O0OO0O0OOO0O0OOO0 ,engine ="xlsxwriter")#line:2712
    OOO0O0O000OOOO000 .to_excel (O00OO0O00OOO00OO0 ,sheet_name ="监测机构")#line:2713
    OO0OOOOOO0OOO0OO0 .to_excel (O00OO0O00OOO00OO0 ,sheet_name ="上报单位")#line:2714
    OOO00OO000O0000OO .to_excel (O00OO0O00OOO00OO0 ,sheet_name ="未上报的二级以上医疗机构")#line:2715
    O00OO0O00OOO00OO0 .close ()#line:2716
    showinfo (title ="提示",message ="文件写入成功。")#line:2717
def TOOLS_web_view (O0OOOO000000000O0 ):#line:2719
    ""#line:2720
    import pybi as pbi #line:2721
    O0OOO00O0O0O00O0O =pd .ExcelWriter ("temp_webview.xls")#line:2722
    O0OOOO000000000O0 .to_excel (O0OOO00O0O0O00O0O ,sheet_name ="temp_webview")#line:2723
    O0OOO00O0O0O00O0O .close ()#line:2724
    O0OOOO000000000O0 =pd .read_excel ("temp_webview.xls",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:2725
    O0O0O000OO0O000OO =pbi .set_source (O0OOOO000000000O0 )#line:2726
    with pbi .flowBox ():#line:2727
        for OOO00000O00OO0000 in O0OOOO000000000O0 .columns :#line:2728
            pbi .add_slicer (O0O0O000OO0O000OO [OOO00000O00OO0000 ])#line:2729
    pbi .add_table (O0O0O000OO0O000OO )#line:2730
    OOOO0OOO0OOOO0O00 ="temp_webview.html"#line:2731
    pbi .to_html (OOOO0OOO0OOOO0O00 )#line:2732
    webbrowser .open_new_tab (OOOO0OOO0OOOO0O00 )#line:2733
def TOOLS_Autotable_0 (O0000OO0OOOO00000 ,OOO0000O0OO00000O ,*O0OOO00O0OO0OO0O0 ):#line:2738
    ""#line:2739
    OO0O0O00OO00OO0OO =[O0OOO00O0OO0OO0O0 [0 ],O0OOO00O0OO0OO0O0 [1 ],O0OOO00O0OO0OO0O0 [2 ]]#line:2741
    OOOO000O00000O00O =list (set ([OOO00OOO0O0OO0OOO for OOO00OOO0O0OO0OOO in OO0O0O00OO00OO0OO if OOO00OOO0O0OO0OOO !='']))#line:2743
    OOOO000O00000O00O .sort (key =OO0O0O00OO00OO0OO .index )#line:2744
    if len (OOOO000O00000O00O )==0 :#line:2745
        showinfo (title ="提示信息",message ="分组项请选择至少一列。")#line:2746
        return 0 #line:2747
    OO0OO00O000000O00 =[O0OOO00O0OO0OO0O0 [3 ],O0OOO00O0OO0OO0O0 [4 ]]#line:2748
    if (O0OOO00O0OO0OO0O0 [3 ]==""or O0OOO00O0OO0OO0O0 [4 ]=="")and OOO0000O0OO00000O in ["数据透视","分组统计"]:#line:2749
        if "报告编码"in O0000OO0OOOO00000 .columns :#line:2750
            OO0OO00O000000O00 [0 ]="报告编码"#line:2751
            OO0OO00O000000O00 [1 ]="nunique"#line:2752
            text .insert (END ,"值项未配置,将使用报告编码进行唯一值计数。")#line:2753
        else :#line:2754
            showinfo (title ="提示信息",message ="值项未配置。")#line:2755
            return 0 #line:2756
    if O0OOO00O0OO0OO0O0 [4 ]=="计数":#line:2758
        OO0OO00O000000O00 [1 ]="count"#line:2759
    elif O0OOO00O0OO0OO0O0 [4 ]=="求和":#line:2760
        OO0OO00O000000O00 [1 ]="sum"#line:2761
    elif O0OOO00O0OO0OO0O0 [4 ]=="唯一值计数":#line:2762
        OO0OO00O000000O00 [1 ]="nunique"#line:2763
    if OOO0000O0OO00000O =="分组统计":#line:2766
        TABLE_tree_Level_2 (TOOLS_deep_view (O0000OO0OOOO00000 ,OOOO000O00000O00O ,OO0OO00O000000O00 ,0 ),1 ,O0000OO0OOOO00000 )#line:2767
    if OOO0000O0OO00000O =="数据透视":#line:2769
        TABLE_tree_Level_2 (TOOLS_deep_view (O0000OO0OOOO00000 ,OOOO000O00000O00O ,OO0OO00O000000O00 ,1 ),1 ,O0000OO0OOOO00000 )#line:2770
    if OOO0000O0OO00000O =="描述性统计":#line:2772
        TABLE_tree_Level_2 (O0000OO0OOOO00000 [OOOO000O00000O00O ].describe ().reset_index (),1 ,O0000OO0OOOO00000 )#line:2773
    if OOO0000O0OO00000O =="追加外部表格信息":#line:2776
        O00O0OO0OO0000O00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2779
        O00OO0O00O00000O0 =[pd .read_excel (OO0O000OO0O00OO00 ,header =0 ,sheet_name =0 )for OO0O000OO0O00OO00 in O00O0OO0OO0000O00 ]#line:2780
        O00OOOO0O0O0OOO0O =pd .concat (O00OO0O00O00000O0 ,ignore_index =True ).drop_duplicates (OOOO000O00000O00O )#line:2781
        O0OO0OO000O0OO0O0 =pd .merge (O0000OO0OOOO00000 ,O00OOOO0O0O0OOO0O ,on =OOOO000O00000O00O ,how ="left")#line:2782
        TABLE_tree_Level_2 (O0OO0OO000O0OO0O0 ,1 ,O0OO0OO000O0OO0O0 )#line:2783
    if OOO0000O0OO00000O =="添加到外部表格":#line:2785
        O00O0OO0OO0000O00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2788
        O00OO0O00O00000O0 =[pd .read_excel (O000OO0O000OO000O ,header =0 ,sheet_name =0 )for O000OO0O000OO000O in O00O0OO0OO0000O00 ]#line:2789
        O00OOOO0O0O0OOO0O =pd .concat (O00OO0O00O00000O0 ,ignore_index =True ).drop_duplicates ()#line:2790
        O0OO0OO000O0OO0O0 =pd .merge (O00OOOO0O0O0OOO0O ,O0000OO0OOOO00000 .drop_duplicates (OOOO000O00000O00O ),on =OOOO000O00000O00O ,how ="left")#line:2791
        TABLE_tree_Level_2 (O0OO0OO000O0OO0O0 ,1 ,O0OO0OO000O0OO0O0 )#line:2792
    if OOO0000O0OO00000O =="饼图(XY)":#line:2795
        DRAW_make_one (O0000OO0OOOO00000 ,"饼图",O0OOO00O0OO0OO0O0 [0 ],O0OOO00O0OO0OO0O0 [1 ],"饼图")#line:2796
    if OOO0000O0OO00000O =="柱状图(XY)":#line:2797
        DRAW_make_one (O0000OO0OOOO00000 ,"柱状图",O0OOO00O0OO0OO0O0 [0 ],O0OOO00O0OO0OO0O0 [1 ],"柱状图")#line:2798
    if OOO0000O0OO00000O =="折线图(XY)":#line:2799
        DRAW_make_one (O0000OO0OOOO00000 ,"折线图",O0OOO00O0OO0OO0O0 [0 ],O0OOO00O0OO0OO0O0 [1 ],"折线图")#line:2800
    if OOO0000O0OO00000O =="托帕斯图(XY)":#line:2801
        DRAW_make_one (O0000OO0OOOO00000 ,"托帕斯图",O0OOO00O0OO0OO0O0 [0 ],O0OOO00O0OO0OO0O0 [1 ],"托帕斯图")#line:2802
    if OOO0000O0OO00000O =="堆叠柱状图（X-YZ）":#line:2803
        DRAW_make_mutibar (O0000OO0OOOO00000 ,OO0O0O00OO00OO0OO [1 ],OO0O0O00OO00OO0OO [2 ],OO0O0O00OO00OO0OO [0 ],OO0O0O00OO00OO0OO [1 ],OO0O0O00OO00OO0OO [2 ],"堆叠柱状图")#line:2804
def STAT_countx (O0O0O00O0O00OOOOO ):#line:2814
	""#line:2815
	return O0O0O00O0O00OOOOO .value_counts ().to_dict ()#line:2816
def STAT_countpx (OO00OO0O0O0000O0O ,O000O000OOOO00OO0 ):#line:2818
	""#line:2819
	return len (OO00OO0O0O0000O0O [(OO00OO0O0O0000O0O ==O000O000OOOO00OO0 )])#line:2820
def STAT_countnpx (OO0OO0O0OO0000OOO ,O0O000O0OO00O0OO0 ):#line:2822
	""#line:2823
	return len (OO0OO0O0OO0000OOO [(OO0OO0O0OO0000OOO not in O0O000O0OO00O0OO0 )])#line:2824
def STAT_get_max (OOOOOOO0OOOO0O0O0 ):#line:2826
	""#line:2827
	return OOOOOOO0OOOO0O0O0 .value_counts ().max ()#line:2828
def STAT_get_mean (O0OO0OOOO0000OOO0 ):#line:2830
	""#line:2831
	return round (O0OO0OOOO0000OOO0 .value_counts ().mean (),2 )#line:2832
def STAT_get_std (O0000O0O0OOOO0OO0 ):#line:2834
	""#line:2835
	return round (O0000O0O0OOOO0OO0 .value_counts ().std (ddof =1 ),2 )#line:2836
def STAT_get_95ci (OO000O00OO00O0OO0 ):#line:2838
	""#line:2839
	OOO0OO00O0O00OO0O =0.95 #line:2840
	O00000O0O0O000OO0 =OO000O00OO00O0OO0 .value_counts ().tolist ()#line:2841
	if len (O00000O0O0O000OO0 )<30 :#line:2842
		O0O0000O00O0OOOOO =st .t .interval (OOO0OO00O0O00OO0O ,df =len (O00000O0O0O000OO0 )-1 ,loc =np .mean (O00000O0O0O000OO0 ),scale =st .sem (O00000O0O0O000OO0 ))#line:2843
	else :#line:2844
		O0O0000O00O0OOOOO =st .norm .interval (OOO0OO00O0O00OO0O ,loc =np .mean (O00000O0O0O000OO0 ),scale =st .sem (O00000O0O0O000OO0 ))#line:2845
	return round (O0O0000O00O0OOOOO [1 ],2 )#line:2846
def STAT_get_mean_std_ci (O0O000O00OOO0OOO0 ,O0OO0OO0O00OOOOOO ):#line:2848
	""#line:2849
	warnings .filterwarnings ("ignore")#line:2850
	O0O000O0OOO0OO00O =TOOLS_strdict_to_pd (str (O0O000O00OOO0OOO0 ))["content"].values /O0OO0OO0O00OOOOOO #line:2851
	O0O0OOOOO00O00O0O =round (O0O000O0OOO0OO00O .mean (),2 )#line:2852
	OOO000O0OO0O000OO =round (O0O000O0OOO0OO00O .std (ddof =1 ),2 )#line:2853
	if len (O0O000O0OOO0OO00O )<30 :#line:2855
		OO000O00000OOO0OO =st .t .interval (0.95 ,df =len (O0O000O0OOO0OO00O )-1 ,loc =np .mean (O0O000O0OOO0OO00O ),scale =st .sem (O0O000O0OOO0OO00O ))#line:2856
	else :#line:2857
		OO000O00000OOO0OO =st .norm .interval (0.95 ,loc =np .mean (O0O000O0OOO0OO00O ),scale =st .sem (O0O000O0OOO0OO00O ))#line:2858
	return pd .Series ((O0O0OOOOO00O00O0O ,OOO000O0OO0O000OO ,OO000O00000OOO0OO [1 ]))#line:2862
def STAT_findx_value (O0O00O0OOO0OOO0OO ,O0OOOO0OO0O0O0OOO ):#line:2864
	""#line:2865
	warnings .filterwarnings ("ignore")#line:2866
	OO000OOO0OOOO00O0 =TOOLS_strdict_to_pd (str (O0O00O0OOO0OOO0OO ))#line:2867
	O00OO0OOOO0OO0O0O =OO000OOO0OOOO00O0 .where (OO000OOO0OOOO00O0 ["index"]==str (O0OOOO0OO0O0O0OOO ))#line:2869
	print (O00OO0OOOO0OO0O0O )#line:2870
	return O00OO0OOOO0OO0O0O #line:2871
def STAT_judge_x (O0O00OO0O0OO0O0OO ,OO0000000000000OO ):#line:2873
	""#line:2874
	for O0O000OOO0O0O0000 in OO0000000000000OO :#line:2875
		if O0O00OO0O0OO0O0OO .find (O0O000OOO0O0O0000 )>-1 :#line:2876
			return 1 #line:2877
def STAT_recent30 (OO0000O00000OOOOO ,O0OOOOO0O0000OOO0 ):#line:2879
	""#line:2880
	import datetime #line:2881
	OOO0O00000O00O000 =OO0000O00000OOOOO [(OO0000O00000OOOOO ["报告日期"].dt .date >(datetime .date .today ()-datetime .timedelta (days =30 )))]#line:2885
	O00OOOOOOO0O0O000 =OOO0O00000O00O000 .drop_duplicates (["报告编码"]).groupby (O0OOOOO0O0000OOO0 ).agg (最近30天报告数 =("报告编码","nunique"),最近30天报告严重伤害数 =("伤害",lambda O000OO0O0O0OOOO00 :STAT_countpx (O000OO0O0O0OOOO00 .values ,"严重伤害")),最近30天报告死亡数量 =("伤害",lambda O0000OOOOOO0O0O0O :STAT_countpx (O0000OOOOOO0O0O0O .values ,"死亡")),最近30天报告单位个数 =("单位名称","nunique"),).reset_index ()#line:2892
	O00OOOOOOO0O0O000 =STAT_basic_risk (O00OOOOOOO0O0O000 ,"最近30天报告数","最近30天报告严重伤害数","最近30天报告死亡数量","最近30天报告单位个数").fillna (0 )#line:2893
	O00OOOOOOO0O0O000 =O00OOOOOOO0O0O000 .rename (columns ={"风险评分":"最近30天风险评分"})#line:2895
	return O00OOOOOOO0O0O000 #line:2896
def STAT_PPR_ROR_1 (O000O0O00O0OOO00O ,O0OOOO00O0O0O0OOO ,OOO00OOOOOOOO00O0 ,O0O000000000OO00O ,O00OOOOOO0O0O0O00 ):#line:2899
    ""#line:2900
    O0OOOO0O0OO0O0OOO =O00OOOOOO0O0O0O00 [(O00OOOOOO0O0O0O00 [O000O0O00O0OOO00O ]==O0OOOO00O0O0O0OOO )]#line:2903
    O0O000O00OO0OO0OO =O0OOOO0O0OO0O0OOO .loc [O0OOOO0O0OO0O0OOO [OOO00OOOOOOOO00O0 ].str .contains (O0O000000000OO00O ,na =False )]#line:2904
    OOOO00000000O0000 =O00OOOOOO0O0O0O00 [(O00OOOOOO0O0O0O00 [O000O0O00O0OOO00O ]!=O0OOOO00O0O0O0OOO )]#line:2905
    OOOO000OOOOOOOO0O =OOOO00000000O0000 .loc [OOOO00000000O0000 [OOO00OOOOOOOO00O0 ].str .contains (O0O000000000OO00O ,na =False )]#line:2906
    OOO00000OOOOO0OOO =(len (O0O000O00OO0OO0OO ),(len (O0OOOO0O0OO0O0OOO )-len (O0O000O00OO0OO0OO )),len (OOOO000OOOOOOOO0O ),(len (OOOO00000000O0000 )-len (OOOO000OOOOOOOO0O )))#line:2907
    if len (O0O000O00OO0OO0OO )>0 :#line:2908
        OO000OO0OOOO00O0O =STAT_PPR_ROR_0 (len (O0O000O00OO0OO0OO ),(len (O0OOOO0O0OO0O0OOO )-len (O0O000O00OO0OO0OO )),len (OOOO000OOOOOOOO0O ),(len (OOOO00000000O0000 )-len (OOOO000OOOOOOOO0O )))#line:2909
    else :#line:2910
        OO000OO0OOOO00O0O =(0 ,0 ,0 ,0 ,0 )#line:2911
    OO000OO000O0O0OOO =len (O0OOOO0O0OO0O0OOO )#line:2914
    if OO000OO000O0O0OOO ==0 :#line:2915
        OO000OO000O0O0OOO =0.5 #line:2916
    return (O0O000000000OO00O ,len (O0O000O00OO0OO0OO ),round (len (O0O000O00OO0OO0OO )/OO000OO000O0O0OOO *100 ,2 ),round (OO000OO0OOOO00O0O [0 ],2 ),round (OO000OO0OOOO00O0O [1 ],2 ),round (OO000OO0OOOO00O0O [2 ],2 ),round (OO000OO0OOOO00O0O [3 ],2 ),round (OO000OO0OOOO00O0O [4 ],2 ),str (OOO00000OOOOO0OOO ),)#line:2927
def STAT_basic_risk (OOOO00OOOO0O0O000 ,OOO0OOO0O0O00OOO0 ,OO00O000O0O00OO00 ,OOOO00O00OO0O0000 ,O000OO0O0O000O00O ):#line:2931
	""#line:2932
	OOOO00OOOO0O0O000 ["风险评分"]=0 #line:2933
	OOOO00OOOO0O0O000 .loc [((OOOO00OOOO0O0O000 [OOO0OOO0O0O00OOO0 ]>=3 )&(OOOO00OOOO0O0O000 [OO00O000O0O00OO00 ]>=1 ))|(OOOO00OOOO0O0O000 [OOO0OOO0O0O00OOO0 ]>=5 ),"风险评分"]=OOOO00OOOO0O0O000 ["风险评分"]+5 #line:2934
	OOOO00OOOO0O0O000 .loc [(OOOO00OOOO0O0O000 [OO00O000O0O00OO00 ]>=3 ),"风险评分"]=OOOO00OOOO0O0O000 ["风险评分"]+1 #line:2935
	OOOO00OOOO0O0O000 .loc [(OOOO00OOOO0O0O000 [OOOO00O00OO0O0000 ]>=1 ),"风险评分"]=OOOO00OOOO0O0O000 ["风险评分"]+10 #line:2936
	OOOO00OOOO0O0O000 ["风险评分"]=OOOO00OOOO0O0O000 ["风险评分"]+OOOO00OOOO0O0O000 [O000OO0O0O000O00O ]/100 #line:2937
	return OOOO00OOOO0O0O000 #line:2938
def STAT_PPR_ROR_0 (OO0O000OOO000OO00 ,OOOOO0OOOOOOOOOO0 ,O00OO0O00000000OO ,O0OO0000000O00O0O ):#line:2941
    ""#line:2942
    if OO0O000OOO000OO00 *OOOOO0OOOOOOOOOO0 *O00OO0O00000000OO *O0OO0000000O00O0O ==0 :#line:2947
        OO0O000OOO000OO00 =OO0O000OOO000OO00 +1 #line:2948
        OOOOO0OOOOOOOOOO0 =OOOOO0OOOOOOOOOO0 +1 #line:2949
        O00OO0O00000000OO =O00OO0O00000000OO +1 #line:2950
        O0OO0000000O00O0O =O0OO0000000O00O0O +1 #line:2951
    O0O000000O00O00OO =(OO0O000OOO000OO00 /(OO0O000OOO000OO00 +OOOOO0OOOOOOOOOO0 ))/(O00OO0O00000000OO /(O00OO0O00000000OO +O0OO0000000O00O0O ))#line:2952
    OO00O00O000O0O0OO =math .sqrt (1 /OO0O000OOO000OO00 -1 /(OO0O000OOO000OO00 +OOOOO0OOOOOOOOOO0 )+1 /O00OO0O00000000OO -1 /(O00OO0O00000000OO +O0OO0000000O00O0O ))#line:2953
    O000O0OOOO00OOOOO =(math .exp (math .log (O0O000000O00O00OO )-1.96 *OO00O00O000O0O0OO ),math .exp (math .log (O0O000000O00O00OO )+1.96 *OO00O00O000O0O0OO ),)#line:2957
    OOO00OO0OO000O0OO =(OO0O000OOO000OO00 /O00OO0O00000000OO )/(OOOOO0OOOOOOOOOO0 /O0OO0000000O00O0O )#line:2958
    OOOOOOOO0O0O0O0O0 =math .sqrt (1 /OO0O000OOO000OO00 +1 /OOOOO0OOOOOOOOOO0 +1 /O00OO0O00000000OO +1 /O0OO0000000O00O0O )#line:2959
    O0OO0OO00O0O0OOOO =(math .exp (math .log (OOO00OO0OO000O0OO )-1.96 *OOOOOOOO0O0O0O0O0 ),math .exp (math .log (OOO00OO0OO000O0OO )+1.96 *OOOOOOOO0O0O0O0O0 ),)#line:2963
    O0OOO000O00O0OO0O =((OO0O000OOO000OO00 *OOOOO0OOOOOOOOOO0 -OOOOO0OOOOOOOOOO0 *O00OO0O00000000OO )*(OO0O000OOO000OO00 *OOOOO0OOOOOOOOOO0 -OOOOO0OOOOOOOOOO0 *O00OO0O00000000OO )*(OO0O000OOO000OO00 +OOOOO0OOOOOOOOOO0 +O00OO0O00000000OO +O0OO0000000O00O0O ))/((OO0O000OOO000OO00 +OOOOO0OOOOOOOOOO0 )*(O00OO0O00000000OO +O0OO0000000O00O0O )*(OO0O000OOO000OO00 +O00OO0O00000000OO )*(OOOOO0OOOOOOOOOO0 +O0OO0000000O00O0O ))#line:2966
    return OOO00OO0OO000O0OO ,O0OO0OO00O0O0OOOO [0 ],O0O000000O00O00OO ,O000O0OOOO00OOOOO [0 ],O0OOO000O00O0OO0O #line:2967
def STAT_find_keyword_risk (O0OOOOO0000O0OOOO ,O0000O0O00OO0OO00 ,OOO0OO00O000O000O ,OO0OOOO0O00OOOOOO ,O00O00O0OO00O00O0 ):#line:2969
		""#line:2970
		O0OOOOO0000O0OOOO =O0OOOOO0000O0OOOO .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:2971
		OO00O0OOO0OO00OOO =O0OOOOO0000O0OOOO .groupby (O0000O0O00OO0OO00 ).agg (证号关键字总数量 =(OOO0OO00O000O000O ,"count"),包含元素个数 =(OO0OOOO0O00OOOOOO ,"nunique"),包含元素 =(OO0OOOO0O00OOOOOO ,STAT_countx ),).reset_index ()#line:2976
		O0O0000O0OOOOOO0O =O0000O0O00OO0OO00 .copy ()#line:2978
		O0O0000O0OOOOOO0O .append (OO0OOOO0O00OOOOOO )#line:2979
		OOOO00O0O0000O0O0 =O0OOOOO0000O0OOOO .groupby (O0O0000O0OOOOOO0O ).agg (计数 =(OO0OOOO0O00OOOOOO ,"count"),严重伤害数 =("伤害",lambda OO0OO0000O0000OOO :STAT_countpx (OO0OO0000O0000OOO .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O0OO0O00OO00O0O :STAT_countpx (O0O0OO0O00OO00O0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:2986
		OO0OOOOOO0OO0OOOO =O0O0000O0OOOOOO0O .copy ()#line:2989
		OO0OOOOOO0OO0OOOO .remove ("关键字")#line:2990
		O0OO0OO0OO0OOOO00 =O0OOOOO0000O0OOOO .groupby (OO0OOOOOO0OO0OOOO ).agg (该元素总数 =(OO0OOOO0O00OOOOOO ,"count"),).reset_index ()#line:2993
		OOOO00O0O0000O0O0 ["证号总数"]=O00O00O0OO00O00O0 #line:2995
		OO00OO00OOO00O0OO =pd .merge (OOOO00O0O0000O0O0 ,OO00O0OOO0OO00OOO ,on =O0000O0O00OO0OO00 ,how ="left")#line:2996
		if len (OO00OO00OOO00O0OO )>0 :#line:3001
			OO00OO00OOO00O0OO [['数量均值','数量标准差','数量CI']]=OO00OO00OOO00O0OO .包含元素 .apply (lambda O00O0OO0OOOOOO0O0 :STAT_get_mean_std_ci (O00O0OO0OOOOOO0O0 ,1 ))#line:3002
		return OO00OO00OOO00O0OO #line:3005
def STAT_find_risk (OO00OOOOOO0OO0OO0 ,OO000OOO0000OO0O0 ,OO0OO0OO0OOOOOOOO ,OO000O0OOOO00OO0O ):#line:3011
		""#line:3012
		OO00OOOOOO0OO0OO0 =OO00OOOOOO0OO0OO0 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3013
		O0OO00O000000OOO0 =OO00OOOOOO0OO0OO0 .groupby (OO000OOO0000OO0O0 ).agg (证号总数量 =(OO0OO0OO0OOOOOOOO ,"count"),包含元素个数 =(OO000O0OOOO00OO0O ,"nunique"),包含元素 =(OO000O0OOOO00OO0O ,STAT_countx ),均值 =(OO000O0OOOO00OO0O ,STAT_get_mean ),标准差 =(OO000O0OOOO00OO0O ,STAT_get_std ),CI上限 =(OO000O0OOOO00OO0O ,STAT_get_95ci ),).reset_index ()#line:3021
		OO00OOO000OO0OO00 =OO000OOO0000OO0O0 .copy ()#line:3023
		OO00OOO000OO0OO00 .append (OO000O0OOOO00OO0O )#line:3024
		O0O0O0O000000O0O0 =OO00OOOOOO0OO0OO0 .groupby (OO00OOO000OO0OO00 ).agg (计数 =(OO000O0OOOO00OO0O ,"count"),严重伤害数 =("伤害",lambda O000000000OO0O0OO :STAT_countpx (O000000000OO0O0OO .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0OO0O0O0OO0OOO0 :STAT_countpx (OO0OO0O0O0OO0OOO0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3031
		O0OOO00OOO0O0O0O0 =pd .merge (O0O0O0O000000O0O0 ,O0OO00O000000OOO0 ,on =OO000OOO0000OO0O0 ,how ="left")#line:3033
		O0OOO00OOO0O0O0O0 ["风险评分"]=0 #line:3035
		O0OOO00OOO0O0O0O0 ["报表类型"]="dfx_findrisk"+OO000O0OOOO00OO0O #line:3036
		O0OOO00OOO0O0O0O0 .loc [((O0OOO00OOO0O0O0O0 ["计数"]>=3 )&(O0OOO00OOO0O0O0O0 ["严重伤害数"]>=1 )|(O0OOO00OOO0O0O0O0 ["计数"]>=5 )),"风险评分"]=O0OOO00OOO0O0O0O0 ["风险评分"]+5 #line:3037
		O0OOO00OOO0O0O0O0 .loc [(O0OOO00OOO0O0O0O0 ["计数"]>=(O0OOO00OOO0O0O0O0 ["均值"]+O0OOO00OOO0O0O0O0 ["标准差"])),"风险评分"]=O0OOO00OOO0O0O0O0 ["风险评分"]+1 #line:3038
		O0OOO00OOO0O0O0O0 .loc [(O0OOO00OOO0O0O0O0 ["计数"]>=O0OOO00OOO0O0O0O0 ["CI上限"]),"风险评分"]=O0OOO00OOO0O0O0O0 ["风险评分"]+1 #line:3039
		O0OOO00OOO0O0O0O0 .loc [(O0OOO00OOO0O0O0O0 ["严重伤害数"]>=3 )&(O0OOO00OOO0O0O0O0 ["风险评分"]>=7 ),"风险评分"]=O0OOO00OOO0O0O0O0 ["风险评分"]+1 #line:3040
		O0OOO00OOO0O0O0O0 .loc [(O0OOO00OOO0O0O0O0 ["死亡数量"]>=1 ),"风险评分"]=O0OOO00OOO0O0O0O0 ["风险评分"]+10 #line:3041
		O0OOO00OOO0O0O0O0 ["风险评分"]=O0OOO00OOO0O0O0O0 ["风险评分"]+O0OOO00OOO0O0O0O0 ["单位个数"]/100 #line:3042
		O0OOO00OOO0O0O0O0 =O0OOO00OOO0O0O0O0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:3043
		return O0OOO00OOO0O0O0O0 #line:3045
def TABLE_tree_Level_2 (O0O0O000OO0000000 ,OOOO0000000OOOO00 ,O000OOOOOO00OO0O0 ,*OO0O00000O000O0OO ):#line:3052
    ""#line:3053
    try :#line:3055
        OOOO00000O0O0O0OO =O0O0O000OO0000000 .columns #line:3056
    except :#line:3057
        return 0 #line:3058
    if "报告编码"in O0O0O000OO0000000 .columns :#line:3060
        OOOO0000000OOOO00 =0 #line:3061
    try :#line:3062
        O0O0000OOOOO0O0OO =len (np .unique (O0O0O000OO0000000 ["注册证编号/曾用注册证编号"].values ))#line:3063
    except :#line:3064
        O0O0000OOOOO0O0OO =10 #line:3065
    OOO0O00O0O000OOO0 =Toplevel ()#line:3068
    OOO0O00O0O000OOO0 .title ("报表查看器")#line:3069
    O00OO0OOOO0OOOOO0 =OOO0O00O0O000OOO0 .winfo_screenwidth ()#line:3070
    O0OO0O0000O0O0000 =OOO0O00O0O000OOO0 .winfo_screenheight ()#line:3072
    O0OO00O0OOOOO00O0 =1310 #line:3074
    O0O000OOOO0O0OOOO =600 #line:3075
    O0O00OOO00O00OO0O =(O00OO0OOOO0OOOOO0 -O0OO00O0OOOOO00O0 )/2 #line:3077
    OOO0OO0O0OO00000O =(O0OO0O0000O0O0000 -O0O000OOOO0O0OOOO )/2 #line:3078
    OOO0O00O0O000OOO0 .geometry ("%dx%d+%d+%d"%(O0OO00O0OOOOO00O0 ,O0O000OOOO0O0OOOO ,O0O00OOO00O00OO0O ,OOO0OO0O0OO00000O ))#line:3079
    O0O0OO0O0O00OOO0O =ttk .Frame (OOO0O00O0O000OOO0 ,width =1310 ,height =20 )#line:3082
    O0O0OO0O0O00OOO0O .pack (side =TOP )#line:3083
    O0OOOOO00000OO0O0 =ttk .Frame (OOO0O00O0O000OOO0 ,width =1310 ,height =20 )#line:3084
    O0OOOOO00000OO0O0 .pack (side =BOTTOM )#line:3085
    OO0OO0O0O0000O0OO =ttk .Frame (OOO0O00O0O000OOO0 ,width =1310 ,height =600 )#line:3086
    OO0OO0O0O0000O0OO .pack (fill ="both",expand ="false")#line:3087
    if OOOO0000000OOOO00 ==0 :#line:3091
        PROGRAM_Menubar (OOO0O00O0O000OOO0 ,O0O0O000OO0000000 ,OOOO0000000OOOO00 ,O000OOOOOO00OO0O0 )#line:3092
    try :#line:3095
        O0O000OOO000OOO00 =StringVar ()#line:3096
        O0O000OOO000OOO00 .set ("产品类别")#line:3097
        def OO000O0OOOOOOO0OO (*OO000OOOO0O000000 ):#line:3098
            O0O000OOO000OOO00 .set (OOO0O00O0OO0OO000 .get ())#line:3099
        O000OOOO0O00O00OO =StringVar ()#line:3100
        O000OOOO0O00O00OO .set ("无源|诊断试剂")#line:3101
        O0O0OO00OO0OO0000 =Label (O0O0OO0O0O00OOO0O ,text ="")#line:3102
        O0O0OO00OO0OO0000 .pack (side =LEFT )#line:3103
        O0O0OO00OO0OO0000 =Label (O0O0OO0O0O00OOO0O ,text ="位置：")#line:3104
        O0O0OO00OO0OO0000 .pack (side =LEFT )#line:3105
        O0OO000OOOO0OOO0O =StringVar ()#line:3106
        OOO0O00O0OO0OO000 =ttk .Combobox (O0O0OO0O0O00OOO0O ,width =12 ,height =30 ,state ="readonly",textvariable =O0OO000OOOO0OOO0O )#line:3109
        OOO0O00O0OO0OO000 ["values"]=O0O0O000OO0000000 .columns .tolist ()#line:3110
        OOO0O00O0OO0OO000 .current (0 )#line:3111
        OOO0O00O0OO0OO000 .bind ("<<ComboboxSelected>>",OO000O0OOOOOOO0OO )#line:3112
        OOO0O00O0OO0OO000 .pack (side =LEFT )#line:3113
        O00OO0OO00OOO00OO =Label (O0O0OO0O0O00OOO0O ,text ="检索：")#line:3114
        O00OO0OO00OOO00OO .pack (side =LEFT )#line:3115
        OOO0O0O0O0OOO0O00 =Entry (O0O0OO0O0O00OOO0O ,width =12 ,textvariable =O000OOOO0O00O00OO ).pack (side =LEFT )#line:3116
        def OO0OOOOOO00O000OO ():#line:3118
            pass #line:3119
        OOO00000O0O0OOO0O =Button (O0O0OO0O0O00OOO0O ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (O0O0O000OO0000000 ),)#line:3133
        OOO00000O0O0OOO0O .pack (side =LEFT )#line:3134
        O000000O0OOO0O00O =Button (O0O0OO0O0O00OOO0O ,text ="视图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyreadT (O0O0O000OO0000000 ),1 ,O000OOOOOO00OO0O0 ),)#line:3143
        if "详细描述T"not in O0O0O000OO0000000 .columns :#line:3144
            O000000O0OOO0O00O .pack (side =LEFT )#line:3145
        O000000O0OOO0O00O =Button (O0O0OO0O0O00OOO0O ,text ="网",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_web_view (O0O0O000OO0000000 ),)#line:3155
        if "详细描述T"not in O0O0O000OO0000000 .columns :#line:3156
            O000000O0OOO0O00O .pack (side =LEFT )#line:3157
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="含",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .loc [O0O0O000OO0000000 [O0O000OOO000OOO00 .get ()].astype (str ).str .contains (str (O000OOOO0O00O00OO .get ()),na =False )],1 ,O000OOOOOO00OO0O0 ,),)#line:3175
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3176
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="无",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .loc [~O0O0O000OO0000000 [O0O000OOO000OOO00 .get ()].astype (str ).str .contains (str (O000OOOO0O00O00OO .get ()),na =False )],1 ,O000OOOOOO00OO0O0 ,),)#line:3193
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3194
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="大",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .loc [O0O0O000OO0000000 [O0O000OOO000OOO00 .get ()].astype (float )>float (O000OOOO0O00O00OO .get ())],1 ,O000OOOOOO00OO0O0 ,),)#line:3209
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3210
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="小",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .loc [O0O0O000OO0000000 [O0O000OOO000OOO00 .get ()].astype (float )<float (O000OOOO0O00O00OO .get ())],1 ,O000OOOOOO00OO0O0 ,),)#line:3225
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3226
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="等",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .loc [O0O0O000OO0000000 [O0O000OOO000OOO00 .get ()].astype (float )==float (O000OOOO0O00O00OO .get ())],1 ,O000OOOOOO00OO0O0 ,),)#line:3241
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3242
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="式",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_findin (O0O0O000OO0000000 ,O000OOOOOO00OO0O0 ))#line:3251
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3252
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="前",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .head (int (O000OOOO0O00O00OO .get ())),1 ,O000OOOOOO00OO0O0 ,),)#line:3267
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3268
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="升",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .sort_values (by =(O0O000OOO000OOO00 .get ()),ascending =[True ],na_position ="last"),1 ,O000OOOOOO00OO0O0 ,),)#line:3283
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3284
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="降",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 .sort_values (by =(O0O000OOO000OOO00 .get ()),ascending =[False ],na_position ="last"),1 ,O000OOOOOO00OO0O0 ,),)#line:3299
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3300
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="SQL",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_sql (O0O0O000OO0000000 ),)#line:3310
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3311
    except :#line:3314
        pass #line:3315
    if ini ["模式"]!="其他":#line:3318
        OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="近月",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 [(O0O0O000OO0000000 ["最近30天报告单位个数"]>=1 )],1 ,O000OOOOOO00OO0O0 ,),)#line:3331
        if "最近30天报告数"in O0O0O000OO0000000 .columns :#line:3332
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3333
        O0000OO00O0OO0O00 =Button (O0O0OO0O0O00OOO0O ,text ="图表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (O0O0O000OO0000000 ),)#line:3345
        if OOOO0000000OOOO00 !=0 :#line:3346
            O0000OO00O0OO0O00 .pack (side =LEFT )#line:3347
        def O0000OO00O0000OOO ():#line:3352
            pass #line:3353
        if OOOO0000000OOOO00 ==0 :#line:3356
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="精简",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyread2 (O0O0O000OO0000000 ),1 ,O000OOOOOO00OO0O0 ,),)#line:3370
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3371
        if OOOO0000000OOOO00 ==0 :#line:3374
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="证号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_zhenghao (),1 ,O000OOOOOO00OO0O0 ,),)#line:3388
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3389
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O000OO0000000 ).df_zhenghao ()))#line:3398
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3399
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="批号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_pihao (),1 ,O000OOOOOO00OO0O0 ,),)#line:3414
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3415
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O000OO0000000 ).df_pihao ()))#line:3424
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3425
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="型号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_xinghao (),1 ,O000OOOOOO00OO0O0 ,),)#line:3440
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3441
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O000OO0000000 ).df_xinghao ()))#line:3450
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3451
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="规格",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_guige (),1 ,O000OOOOOO00OO0O0 ,),)#line:3466
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3467
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O000OO0000000 ).df_guige ()))#line:3476
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3477
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="企业",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_chiyouren (),1 ,O000OOOOOO00OO0O0 ,),)#line:3492
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3493
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="县区",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_org ("监测机构"),1 ,O000OOOOOO00OO0O0 ,),)#line:3509
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3510
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="单位",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_user (),1 ,O000OOOOOO00OO0O0 ,),)#line:3523
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3524
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="年龄",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_age (),1 ,O000OOOOOO00OO0O0 ,),)#line:3538
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3539
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="时隔",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_deep_view (O0O0O000OO0000000 ,["时隔"],["报告编码","nunique"],0 ),1 ,O000OOOOOO00OO0O0 ,),)#line:3553
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3554
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O000OO0000000 ).df_psur (),1 ,O000OOOOOO00OO0O0 ,),)#line:3568
            if "UDI"not in O0O0O000OO0000000 .columns :#line:3569
                OOO000OO0OOOOO00O .pack (side =LEFT )#line:3570
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_get_guize2 (O0O0O000OO0000000 ),1 ,O000OOOOOO00OO0O0 ,),)#line:3583
            if "UDI"in O0O0O000OO0000000 .columns :#line:3584
                OOO000OO0OOOOO00O .pack (side =LEFT )#line:3585
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="发生时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_time (O0O0O000OO0000000 ,"事件发生日期",0 ),)#line:3594
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3595
            OOO000OO0OOOOO00O =Button (O0O0OO0O0O00OOO0O ,text ="报告时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_one (TOOLS_time (O0O0O000OO0000000 ,"报告日期",1 ),"时间托帕斯图","time","报告总数","超级托帕斯图(严重伤害数)"),)#line:3605
            OOO000OO0OOOOO00O .pack (side =LEFT )#line:3606
    try :#line:3612
        OO0OOOOOOO0OOOO0O =ttk .Label (O0OOOOO00000OO0O0 ,text ="方法：")#line:3614
        OO0OOOOOOO0OOOO0O .pack (side =LEFT )#line:3615
        OOOOOO0O0O0000000 =StringVar ()#line:3616
        OOOOOOOO00O00O00O =ttk .Combobox (O0OOOOO00000OO0O0 ,width =15 ,textvariable =OOOOOO0O0O0000000 ,state ='readonly')#line:3617
        OOOOOOOO00O00O00O ['values']=("分组统计","数据透视","描述性统计","饼图(XY)","柱状图(XY)","折线图(XY)","托帕斯图(XY)","堆叠柱状图（X-YZ）","追加外部表格信息","添加到外部表格")#line:3618
        OOOOOOOO00O00O00O .pack (side =LEFT )#line:3622
        OOOOOOOO00O00O00O .current (0 )#line:3623
        O0OO0O0OO000O0OOO =ttk .Label (O0OOOOO00000OO0O0 ,text ="分组列（X-Y-Z）:")#line:3624
        O0OO0O0OO000O0OOO .pack (side =LEFT )#line:3625
        OO000000OO00OOOO0 =StringVar ()#line:3628
        OO00OO00O0OO00O00 =ttk .Combobox (O0OOOOO00000OO0O0 ,width =15 ,textvariable =OO000000OO00OOOO0 ,state ='readonly')#line:3629
        OO00OO00O0OO00O00 ['values']=O0O0O000OO0000000 .columns .tolist ()#line:3630
        OO00OO00O0OO00O00 .pack (side =LEFT )#line:3631
        O0OOO00OO00OOO0O0 =StringVar ()#line:3632
        OO00O0O0O0OO0OOO0 =ttk .Combobox (O0OOOOO00000OO0O0 ,width =15 ,textvariable =O0OOO00OO00OOO0O0 ,state ='readonly')#line:3633
        OO00O0O0O0OO0OOO0 ['values']=O0O0O000OO0000000 .columns .tolist ()#line:3634
        OO00O0O0O0OO0OOO0 .pack (side =LEFT )#line:3635
        O0OO0000000000000 =StringVar ()#line:3636
        OO00OOO00O00O0OOO =ttk .Combobox (O0OOOOO00000OO0O0 ,width =15 ,textvariable =O0OO0000000000000 ,state ='readonly')#line:3637
        OO00OOO00O00O0OOO ['values']=O0O0O000OO0000000 .columns .tolist ()#line:3638
        OO00OOO00O00O0OOO .pack (side =LEFT )#line:3639
        O0O000OO0O0OOO0OO =StringVar ()#line:3640
        OO000O00OOOO0O00O =StringVar ()#line:3641
        O0OO0O0OO000O0OOO =ttk .Label (O0OOOOO00000OO0O0 ,text ="计算列（V-M）:")#line:3642
        O0OO0O0OO000O0OOO .pack (side =LEFT )#line:3643
        O0O0OOOOOO0000O00 =ttk .Combobox (O0OOOOO00000OO0O0 ,width =10 ,textvariable =O0O000OO0O0OOO0OO ,state ='readonly')#line:3645
        O0O0OOOOOO0000O00 ['values']=O0O0O000OO0000000 .columns .tolist ()#line:3646
        O0O0OOOOOO0000O00 .pack (side =LEFT )#line:3647
        OOO0OO00000O00OO0 =ttk .Combobox (O0OOOOO00000OO0O0 ,width =10 ,textvariable =OO000O00OOOO0O00O ,state ='readonly')#line:3648
        OOO0OO00000O00OO0 ['values']=["计数","求和","唯一值计数"]#line:3649
        OOO0OO00000O00OO0 .pack (side =LEFT )#line:3650
        O0OOOO00O0OO0OOOO =Button (O0OOOOO00000OO0O0 ,text ="自助报表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_Autotable_0 (O0O0O000OO0000000 ,OOOOOOOO00O00O00O .get (),OO000000OO00OOOO0 .get (),O0OOO00OO00OOO0O0 .get (),O0OO0000000000000 .get (),O0O000OO0O0OOO0OO .get (),OO000O00OOOO0O00O .get (),O0O0O000OO0000000 ))#line:3652
        O0OOOO00O0OO0OOOO .pack (side =LEFT )#line:3653
        O0000OO00O0OO0O00 =Button (O0OOOOO00000OO0O0 ,text ="去首行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 [1 :],1 ,O000OOOOOO00OO0O0 ,))#line:3670
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3671
        O0000OO00O0OO0O00 =Button (O0OOOOO00000OO0O0 ,text ="去尾行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O000OO0000000 [:-1 ],1 ,O000OOOOOO00OO0O0 ,),)#line:3686
        O0000OO00O0OO0O00 .pack (side =LEFT )#line:3687
        OOO000OO0OOOOO00O =Button (O0OOOOO00000OO0O0 ,text ="行数:"+str (len (O0O0O000OO0000000 )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:3697
        OOO000OO0OOOOO00O .pack (side =LEFT )#line:3698
    except :#line:3701
        showinfo (title ="提示信息",message ="界面初始化失败。")#line:3702
    OO0OOOO00O0O0O0O0 =O0O0O000OO0000000 .values .tolist ()#line:3708
    OO0OOOOOO0O0OOO0O =O0O0O000OO0000000 .columns .values .tolist ()#line:3709
    O0O0000OOO00O000O =ttk .Treeview (OO0OO0O0O0000O0OO ,columns =OO0OOOOOO0O0OOO0O ,show ="headings",height =45 )#line:3710
    for O000OO0O00O0000OO in OO0OOOOOO0O0OOO0O :#line:3713
        O0O0000OOO00O000O .heading (O000OO0O00O0000OO ,text =O000OO0O00O0000OO )#line:3714
    for O00OO0OO00OOOOOOO in OO0OOOO00O0O0O0O0 :#line:3715
        O0O0000OOO00O000O .insert ("","end",values =O00OO0OO00OOOOOOO )#line:3716
    for O0OOO0000OOO00O00 in OO0OOOOOO0O0OOO0O :#line:3718
        try :#line:3719
            O0O0000OOO00O000O .column (O0OOO0000OOO00O00 ,minwidth =0 ,width =80 ,stretch =NO )#line:3720
            if "只剩"in O0OOO0000OOO00O00 :#line:3721
                O0O0000OOO00O000O .column (O0OOO0000OOO00O00 ,minwidth =0 ,width =150 ,stretch =NO )#line:3722
        except :#line:3723
            pass #line:3724
    O0O0O0000O00O0000 =["评分说明"]#line:3728
    O0000O0O0O0OO000O =["该单位喜好上报的品种统计","报告编码","产品名称","上报机构描述","持有人处理描述","该注册证编号/曾用注册证编号报告数量","通用名称","该批准文号报告数量","上市许可持有人名称",]#line:3741
    OO00OO00O00O000O0 =["注册证编号/曾用注册证编号","监测机构","报告月份","报告季度","单位列表","单位名称",]#line:3749
    OO0OOOO00OO0OO0O0 =["管理类别",]#line:3753
    for O0OOO0000OOO00O00 in O0000O0O0O0OO000O :#line:3756
        try :#line:3757
            O0O0000OOO00O000O .column (O0OOO0000OOO00O00 ,minwidth =0 ,width =200 ,stretch =NO )#line:3758
        except :#line:3759
            pass #line:3760
    for O0OOO0000OOO00O00 in OO00OO00O00O000O0 :#line:3763
        try :#line:3764
            O0O0000OOO00O000O .column (O0OOO0000OOO00O00 ,minwidth =0 ,width =140 ,stretch =NO )#line:3765
        except :#line:3766
            pass #line:3767
    for O0OOO0000OOO00O00 in OO0OOOO00OO0OO0O0 :#line:3768
        try :#line:3769
            O0O0000OOO00O000O .column (O0OOO0000OOO00O00 ,minwidth =0 ,width =40 ,stretch =NO )#line:3770
        except :#line:3771
            pass #line:3772
    for O0OOO0000OOO00O00 in O0O0O0000O00O0000 :#line:3773
        try :#line:3774
            O0O0000OOO00O000O .column (O0OOO0000OOO00O00 ,minwidth =0 ,width =800 ,stretch =NO )#line:3775
        except :#line:3776
            pass #line:3777
    try :#line:3779
        O0O0000OOO00O000O .column ("请选择需要查看的表格",minwidth =1 ,width =300 ,stretch =NO )#line:3782
    except :#line:3783
        pass #line:3784
    try :#line:3786
        O0O0000OOO00O000O .column ("详细描述T",minwidth =1 ,width =2300 ,stretch =NO )#line:3789
    except :#line:3790
        pass #line:3791
    O0OO00OOO0OO0OOO0 =Scrollbar (OO0OO0O0O0000O0OO ,orient ="vertical")#line:3793
    O0OO00OOO0OO0OOO0 .pack (side =RIGHT ,fill =Y )#line:3794
    O0OO00OOO0OO0OOO0 .config (command =O0O0000OOO00O000O .yview )#line:3795
    O0O0000OOO00O000O .config (yscrollcommand =O0OO00OOO0OO0OOO0 .set )#line:3796
    O0OOO000OO00O0O0O =Scrollbar (OO0OO0O0O0000O0OO ,orient ="horizontal")#line:3798
    O0OOO000OO00O0O0O .pack (side =BOTTOM ,fill =X )#line:3799
    O0OOO000OO00O0O0O .config (command =O0O0000OOO00O000O .xview )#line:3800
    O0O0000OOO00O000O .config (yscrollcommand =O0OO00OOO0OO0OOO0 .set )#line:3801
    def O00OOOOO00O00000O (O0O0OO000OO0OOO00 ,OO0O0O00O00O00O0O ,OO0OOOO00000OOOOO ):#line:3804
        for O0OOOOO0O0OO000O0 in O0O0000OOO00O000O .selection ():#line:3806
            O0000O0O00OO0OOOO =O0O0000OOO00O000O .item (O0OOOOO0O0OO000O0 ,"values")#line:3807
        OOOO0OOO0O000O000 =dict (zip (OO0O0O00O00O00O0O ,O0000O0O00OO0OOOO ))#line:3808
        if "详细描述T"in OO0O0O00O00O00O0O and "{"in OOOO0OOO0O000O000 ["详细描述T"]:#line:3812
            OOO0O000O00OOO00O =eval (OOOO0OOO0O000O000 ["详细描述T"])#line:3813
            OOO0O000O00OOO00O =pd .DataFrame .from_dict (OOO0O000O00OOO00O ,orient ="index",columns =["content"]).reset_index ()#line:3814
            OOO0O000O00OOO00O =OOO0O000O00OOO00O .sort_values (by ="content",ascending =[False ],na_position ="last")#line:3815
            DRAW_make_one (OOO0O000O00OOO00O ,OOOO0OOO0O000O000 ["条目"],"index","content","饼图")#line:3816
            return 0 #line:3817
        if "dfx_deepview"in OOOO0OOO0O000O000 ["报表类型"]:#line:3822
            OO0OOOOOO00OOOOO0 =eval (OOOO0OOO0O000O000 ["报表类型"][13 :])#line:3823
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO .copy ()#line:3824
            for O00OOO0O000OO0O0O in OO0OOOOOO00OOOOO0 :#line:3825
                OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO [(OOOOOOOO0OOOO0OOO [O00OOO0O000OO0O0O ].astype (str )==O0000O0O00OO0OOOO [OO0OOOOOO00OOOOO0 .index (O00OOO0O000OO0O0O )])].copy ()#line:3826
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_deepview"#line:3827
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3828
            return 0 #line:3829
        if "dfx_deepvie2"in OOOO0OOO0O000O000 ["报表类型"]:#line:3832
            OO0OOOOOO00OOOOO0 =eval (OOOO0OOO0O000O000 ["报表类型"][13 :])#line:3833
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO .copy ()#line:3834
            for O00OOO0O000OO0O0O in OO0OOOOOO00OOOOO0 :#line:3835
                OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO [OOOOOOOO0OOOO0OOO [O00OOO0O000OO0O0O ].str .contains (O0000O0O00OO0OOOO [OO0OOOOOO00OOOOO0 .index (O00OOO0O000OO0O0O )],na =False )].copy ()#line:3836
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_deepview"#line:3837
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3838
            return 0 #line:3839
        if "dfx_zhenghao"in OOOO0OOO0O000O000 ["报表类型"]:#line:3843
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["注册证编号/曾用注册证编号"]==OOOO0OOO0O000O000 ["注册证编号/曾用注册证编号"])].copy ()#line:3844
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_zhenghao"#line:3845
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3846
            return 0 #line:3847
        if ("dfx_pihao"in OOOO0OOO0O000O000 ["报表类型"]or "dfx_findrisk"in OOOO0OOO0O000O000 ["报表类型"]or "dfx_xinghao"in OOOO0OOO0O000O000 ["报表类型"]or "dfx_guige"in OOOO0OOO0O000O000 ["报表类型"])and O0O0000OOOOO0O0OO ==1 :#line:3851
            OO0O0OO0O00OOO00O ="CLT"#line:3852
            if "pihao"in OOOO0OOO0O000O000 ["报表类型"]or "产品批号"in OOOO0OOO0O000O000 ["报表类型"]:#line:3853
                OO0O0OO0O00OOO00O ="产品批号"#line:3854
            if "xinghao"in OOOO0OOO0O000O000 ["报表类型"]or "型号"in OOOO0OOO0O000O000 ["报表类型"]:#line:3855
                OO0O0OO0O00OOO00O ="型号"#line:3856
            if "guige"in OOOO0OOO0O000O000 ["报表类型"]or "规格"in OOOO0OOO0O000O000 ["报表类型"]:#line:3857
                OO0O0OO0O00OOO00O ="规格"#line:3858
            if "事件发生季度"in OOOO0OOO0O000O000 ["报表类型"]:#line:3859
                OO0O0OO0O00OOO00O ="事件发生季度"#line:3860
            if "事件发生月份"in OOOO0OOO0O000O000 ["报表类型"]:#line:3861
                OO0O0OO0O00OOO00O ="事件发生月份"#line:3862
            if "性别"in OOOO0OOO0O000O000 ["报表类型"]:#line:3863
                OO0O0OO0O00OOO00O ="性别"#line:3864
            if "年龄段"in OOOO0OOO0O000O000 ["报表类型"]:#line:3865
                OO0O0OO0O00OOO00O ="年龄段"#line:3866
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["注册证编号/曾用注册证编号"]==OOOO0OOO0O000O000 ["注册证编号/曾用注册证编号"])&(OO0OOOO00000OOOOO [OO0O0OO0O00OOO00O ]==OOOO0OOO0O000O000 [OO0O0OO0O00OOO00O ])].copy ()#line:3867
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_pihao"#line:3868
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3869
            return 0 #line:3870
        if ("findrisk"in OOOO0OOO0O000O000 ["报表类型"]or "dfx_pihao"in OOOO0OOO0O000O000 ["报表类型"]or "dfx_xinghao"in OOOO0OOO0O000O000 ["报表类型"]or "dfx_guige"in OOOO0OOO0O000O000 ["报表类型"])and O0O0000OOOOO0O0OO !=1 :#line:3874
            OOOOOOOO0OOOO0OOO =O0O0O000OO0000000 [(O0O0O000OO0000000 ["注册证编号/曾用注册证编号"]==OOOO0OOO0O000O000 ["注册证编号/曾用注册证编号"])].copy ()#line:3875
            OOOOOOOO0OOOO0OOO ["报表类型"]=OOOO0OOO0O000O000 ["报表类型"]+"1"#line:3876
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,1 ,OO0OOOO00000OOOOO )#line:3877
            return 0 #line:3879
        if "dfx_org监测机构"in OOOO0OOO0O000O000 ["报表类型"]:#line:3882
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["监测机构"]==OOOO0OOO0O000O000 ["监测机构"])].copy ()#line:3883
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_org"#line:3884
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3885
            return 0 #line:3886
        if "dfx_org市级监测机构"in OOOO0OOO0O000O000 ["报表类型"]:#line:3888
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["市级监测机构"]==OOOO0OOO0O000O000 ["市级监测机构"])].copy ()#line:3889
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_org"#line:3890
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3891
            return 0 #line:3892
        if "dfx_user"in OOOO0OOO0O000O000 ["报表类型"]:#line:3895
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["单位名称"]==OOOO0OOO0O000O000 ["单位名称"])].copy ()#line:3896
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_user"#line:3897
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3898
            return 0 #line:3899
        if "dfx_chiyouren"in OOOO0OOO0O000O000 ["报表类型"]:#line:3903
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["上市许可持有人名称"]==OOOO0OOO0O000O000 ["上市许可持有人名称"])].copy ()#line:3904
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_chiyouren"#line:3905
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3906
            return 0 #line:3907
        if "dfx_chanpin"in OOOO0OOO0O000O000 ["报表类型"]:#line:3909
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["产品名称"]==OOOO0OOO0O000O000 ["产品名称"])].copy ()#line:3910
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_chanpin"#line:3911
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3912
            return 0 #line:3913
        if "dfx_findrisk事件发生季度1"in OOOO0OOO0O000O000 ["报表类型"]:#line:3918
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["注册证编号/曾用注册证编号"]==OOOO0OOO0O000O000 ["注册证编号/曾用注册证编号"])&(OO0OOOO00000OOOOO ["事件发生季度"]==OOOO0OOO0O000O000 ["事件发生季度"])].copy ()#line:3919
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_findrisk事件发生季度"#line:3920
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3921
            return 0 #line:3922
        if "dfx_findrisk事件发生月份1"in OOOO0OOO0O000O000 ["报表类型"]:#line:3925
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["注册证编号/曾用注册证编号"]==OOOO0OOO0O000O000 ["注册证编号/曾用注册证编号"])&(OO0OOOO00000OOOOO ["事件发生月份"]==OOOO0OOO0O000O000 ["事件发生月份"])].copy ()#line:3926
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_dfx_findrisk事件发生月份"#line:3927
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3928
            return 0 #line:3929
        if ("keyword_findrisk"in OOOO0OOO0O000O000 ["报表类型"])and O0O0000OOOOO0O0OO ==1 :#line:3932
            OO0O0OO0O00OOO00O ="CLT"#line:3933
            if "批号"in OOOO0OOO0O000O000 ["报表类型"]:#line:3934
                OO0O0OO0O00OOO00O ="产品批号"#line:3935
            if "事件发生季度"in OOOO0OOO0O000O000 ["报表类型"]:#line:3936
                OO0O0OO0O00OOO00O ="事件发生季度"#line:3937
            if "事件发生月份"in OOOO0OOO0O000O000 ["报表类型"]:#line:3938
                OO0O0OO0O00OOO00O ="事件发生月份"#line:3939
            if "性别"in OOOO0OOO0O000O000 ["报表类型"]:#line:3940
                OO0O0OO0O00OOO00O ="性别"#line:3941
            if "年龄段"in OOOO0OOO0O000O000 ["报表类型"]:#line:3942
                OO0O0OO0O00OOO00O ="年龄段"#line:3943
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO [(OO0OOOO00000OOOOO ["注册证编号/曾用注册证编号"]==OOOO0OOO0O000O000 ["注册证编号/曾用注册证编号"])&(OO0OOOO00000OOOOO [OO0O0OO0O00OOO00O ]==OOOO0OOO0O000O000 [OO0O0OO0O00OOO00O ])].copy ()#line:3944
            OOOOOOOO0OOOO0OOO ["关键字查找列"]=""#line:3945
            for OO00O0OOOO0OO000O in TOOLS_get_list (OOOO0OOO0O000O000 ["关键字查找列"]):#line:3946
                OOOOOOOO0OOOO0OOO ["关键字查找列"]=OOOOOOOO0OOOO0OOO ["关键字查找列"]+OOOOOOOO0OOOO0OOO [OO00O0OOOO0OO000O ].astype ("str")#line:3947
            OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO [(OOOOOOOO0OOOO0OOO ["关键字查找列"].str .contains (OOOO0OOO0O000O000 ["关键字组合"],na =False ))]#line:3948
            if str (OOOO0OOO0O000O000 ["排除值"])!="nan":#line:3950
                OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO .loc [~OOOOOOOO0OOOO0OOO ["关键字查找列"].str .contains (OOOO0OOO0O000O000 ["排除值"],na =False )]#line:3951
            OOOOOOOO0OOOO0OOO ["报表类型"]="ori_"+OOOO0OOO0O000O000 ["报表类型"]#line:3953
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3954
            return 0 #line:3955
        if ("PSUR"in OOOO0OOO0O000O000 ["报表类型"]):#line:3960
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO .copy ()#line:3961
            if ini ["模式"]=="器械":#line:3962
                OOOOOOOO0OOOO0OOO ["关键字查找列"]=OOOOOOOO0OOOO0OOO ["器械故障表现"].astype (str )+OOOOOOOO0OOOO0OOO ["伤害表现"].astype (str )+OOOOOOOO0OOOO0OOO ["使用过程"].astype (str )+OOOOOOOO0OOOO0OOO ["事件原因分析描述"].astype (str )+OOOOOOOO0OOOO0OOO ["初步处置情况"].astype (str )#line:3963
            else :#line:3964
                OOOOOOOO0OOOO0OOO ["关键字查找列"]=OOOOOOOO0OOOO0OOO ["器械故障表现"]#line:3965
            if "-其他关键字-"in str (OOOO0OOO0O000O000 ["关键字标记"]):#line:3967
                OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO .loc [~OOOOOOOO0OOOO0OOO ["关键字查找列"].str .contains (OOOO0OOO0O000O000 ["关键字标记"],na =False )].copy ()#line:3968
                TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3969
                return 0 #line:3970
            OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO [(OOOOOOOO0OOOO0OOO ["关键字查找列"].str .contains (OOOO0OOO0O000O000 ["关键字标记"],na =False ))]#line:3973
            if str (OOOO0OOO0O000O000 ["排除值"])!="没有排除值":#line:3974
                OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO .loc [~OOOOOOOO0OOOO0OOO ["关键字查找列"].str .contains (OOOO0OOO0O000O000 ["排除值"],na =False )]#line:3975
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:3979
            return 0 #line:3980
        if ("ROR"in OOOO0OOO0O000O000 ["报表类型"]):#line:3983
            O0O00O0O0O0O00000 ={'nan':"-未定义-"}#line:3984
            OOOO0O0O0000OOO00 =eval (OOOO0OOO0O000O000 ["报表定位"],O0O00O0O0O0O00000 )#line:3985
            OOOOOOOO0OOOO0OOO =OO0OOOO00000OOOOO .copy ()#line:3986
            for OOOO0O000OOO00000 ,OO0000O00OOOOOO0O in OOOO0O0O0000OOO00 .items ():#line:3988
                if OOOO0O000OOO00000 =="合并列"and OO0000O00OOOOOO0O !={}:#line:3990
                    for OO0OOO0OO0O000OOO ,OO00O00OOO00O0OOO in OO0000O00OOOOOO0O .items ():#line:3991
                        if OO00O00OOO00O0OOO !="-未定义-":#line:3992
                            OO0OO000OO000OOO0 =TOOLS_get_list (OO00O00OOO00O0OOO )#line:3993
                            OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ]=""#line:3994
                            for OO0OO0OOO0000O00O in OO0OO000OO000OOO0 :#line:3995
                                OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ]=OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ]+OOOOOOOO0OOOO0OOO [OO0OO0OOO0000O00O ].astype ("str")#line:3996
                if OOOO0O000OOO00000 =="等于"and OO0000O00OOOOOO0O !={}:#line:3998
                    for OO0OOO0OO0O000OOO ,OO00O00OOO00O0OOO in OO0000O00OOOOOO0O .items ():#line:3999
                        OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO [(OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ]==OO00O00OOO00O0OOO )]#line:4000
                if OOOO0O000OOO00000 =="不等于"and OO0000O00OOOOOO0O !={}:#line:4002
                    for OO0OOO0OO0O000OOO ,OO00O00OOO00O0OOO in OO0000O00OOOOOO0O .items ():#line:4003
                        if OO00O00OOO00O0OOO !="-未定义-":#line:4004
                            OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO [(OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ]!=OO00O00OOO00O0OOO )]#line:4005
                if OOOO0O000OOO00000 =="包含"and OO0000O00OOOOOO0O !={}:#line:4007
                    for OO0OOO0OO0O000OOO ,OO00O00OOO00O0OOO in OO0000O00OOOOOO0O .items ():#line:4008
                        if OO00O00OOO00O0OOO !="-未定义-":#line:4009
                            OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO .loc [OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ].str .contains (OO00O00OOO00O0OOO ,na =False )]#line:4010
                if OOOO0O000OOO00000 =="不包含"and OO0000O00OOOOOO0O !={}:#line:4012
                    for OO0OOO0OO0O000OOO ,OO00O00OOO00O0OOO in OO0000O00OOOOOO0O .items ():#line:4013
                        if OO00O00OOO00O0OOO !="-未定义-":#line:4014
                            OOOOOOOO0OOOO0OOO =OOOOOOOO0OOOO0OOO .loc [~OOOOOOOO0OOOO0OOO [OO0OOO0OO0O000OOO ].str .contains (OO00O00OOO00O0OOO ,na =False )]#line:4015
            TABLE_tree_Level_2 (OOOOOOOO0OOOO0OOO ,0 ,OOOOOOOO0OOOO0OOO )#line:4017
            return 0 #line:4018
    try :#line:4022
        if OO0O00000O000O0OO [1 ]=="dfx_zhenghao":#line:4023
            O0O0OO0O00O0OO0OO ="dfx_zhenghao"#line:4024
            OOOOO00O0O0O0O0O0 =""#line:4025
    except :#line:4026
            O0O0OO0O00O0OO0OO =""#line:4027
            OOOOO00O0O0O0O0O0 ="近一年"#line:4028
    if (("总体评分"in OOO0O00O0OO0OO000 ["values"])and ("高峰批号均值"in OOO0O00O0OO0OO000 ["values"])and ("月份均值"in OOO0O00O0OO0OO000 ["values"]))or O0O0OO0O00O0OO0OO =="dfx_zhenghao":#line:4029
            def OOO00O0OO0OO0OO0O (event =None ):#line:4032
                for O00O0000OO0O00000 in O0O0000OOO00O000O .selection ():#line:4033
                    OO00000O00O0OOOOO =O0O0000OOO00O000O .item (O00O0000OO0O00000 ,"values")#line:4034
                OOOOOO00O0O0O00OO =dict (zip (OO0OOOOOO0O0OOO0O ,OO00000O00O0OOOOO ))#line:4035
                OOOO0OOO0O0O000OO =O000OOOOOO00OO0O0 [(O000OOOOOO00OO0O0 ["注册证编号/曾用注册证编号"]==OOOOOO00O0O0O00OO ["注册证编号/曾用注册证编号"])].copy ()#line:4036
                OOOO0OOO0O0O000OO ["报表类型"]=OOOOOO00O0O0O00OO ["报表类型"]+"1"#line:4037
                TABLE_tree_Level_2 (OOOO0OOO0O0O000OO ,1 ,O000OOOOOO00OO0O0 )#line:4038
            def O0O00OO000OO0O0O0 (event =None ):#line:4039
                for OO0OO00OOOOOO0OOO in O0O0000OOO00O000O .selection ():#line:4040
                    OOO0OOO0OOOOOOOO0 =O0O0000OOO00O000O .item (OO0OO00OOOOOO0OOO ,"values")#line:4041
                O0O00OO0000OO0O0O =dict (zip (OO0OOOOOO0O0OOO0O ,OOO0OOO0OOOOOOOO0 ))#line:4042
                OOOO0OOOOOOO00O00 =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==O0O00OO0000OO0O0O ["注册证编号/曾用注册证编号"])].copy ()#line:4043
                OOOO0OOOOOOO00O00 ["报表类型"]=O0O00OO0000OO0O0O ["报表类型"]+"1"#line:4044
                TABLE_tree_Level_2 (OOOO0OOOOOOO00O00 ,1 ,OO0O00000O000O0OO [0 ])#line:4045
            def O00OO0O0O000OO00O (OO00O0O00O0OO000O ):#line:4046
                for OOO00OO00000O00OO in O0O0000OOO00O000O .selection ():#line:4047
                    O000OO0O000000000 =O0O0000OOO00O000O .item (OOO00OO00000O00OO ,"values")#line:4048
                OO0OOO0O00O0O0O00 =dict (zip (OO0OOOOOO0O0OOO0O ,O000OO0O000000000 ))#line:4049
                O000OOO0OO0O0O00O =O000OOOOOO00OO0O0 [(O000OOOOOO00OO0O0 ["注册证编号/曾用注册证编号"]==OO0OOO0O00O0O0O00 ["注册证编号/曾用注册证编号"])].copy ()#line:4052
                O000OOO0OO0O0O00O ["报表类型"]=OO0OOO0O00O0O0O00 ["报表类型"]+"1"#line:4053
                OO00O0000O00O0OO0 =Countall (O000OOO0OO0O0O00O ).df_psur (OO00O0O00O0OO000O ,OO0OOO0O00O0O0O00 ["规整后品类"])[["关键字标记","总数量","严重比"]]#line:4054
                OO00O0000O00O0OO0 =OO00O0000O00O0OO0 .rename (columns ={"总数量":"最近30天总数量"})#line:4055
                OO00O0000O00O0OO0 =OO00O0000O00O0OO0 .rename (columns ={"严重比":"最近30天严重比"})#line:4056
                O000OOO0OO0O0O00O =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==OO0OOO0O00O0O0O00 ["注册证编号/曾用注册证编号"])].copy ()#line:4058
                O000OOO0OO0O0O00O ["报表类型"]=OO0OOO0O00O0O0O00 ["报表类型"]+"1"#line:4059
                O00O00O00O0OO0OO0 =Countall (O000OOO0OO0O0O00O ).df_psur (OO00O0O00O0OO000O ,OO0OOO0O00O0O0O00 ["规整后品类"])#line:4060
                OOO0OOOO00O000OO0 =pd .merge (O00O00O00O0OO0OO0 ,OO00O0000O00O0OO0 ,on ="关键字标记",how ="left")#line:4062
                del OOO0OOOO00O000OO0 ["报表类型"]#line:4063
                OOO0OOOO00O000OO0 ["报表类型"]="PSUR"#line:4064
                TABLE_tree_Level_2 (OOO0OOOO00O000OO0 ,1 ,O000OOO0OO0O0O00O )#line:4066
            def OOOO000OO0OOOOOOO (OO00OOOOO00OOO00O ):#line:4069
                for OOO00OOOO000OOO0O in O0O0000OOO00O000O .selection ():#line:4070
                    OO0OOOO00OO000000 =O0O0000OOO00O000O .item (OOO00OOOO000OOO0O ,"values")#line:4071
                O0OO000000OOOO0O0 =dict (zip (OO0OOOOOO0O0OOO0O ,OO0OOOO00OO000000 ))#line:4072
                O00OOOOOO0O0OO00O =OO0O00000O000O0OO [0 ]#line:4073
                if O0OO000000OOOO0O0 ["规整后品类"]=="N":#line:4074
                    if OO00OOOOO00OOO00O =="特定品种":#line:4075
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4076
                        return 0 #line:4077
                    O00OOOOOO0O0OO00O =O00OOOOOO0O0OO00O .loc [O00OOOOOO0O0OO00O ["产品名称"].str .contains (O0OO000000OOOO0O0 ["产品名称"],na =False )].copy ()#line:4078
                else :#line:4079
                    O00OOOOOO0O0OO00O =O00OOOOOO0O0OO00O .loc [O00OOOOOO0O0OO00O ["规整后品类"].str .contains (O0OO000000OOOO0O0 ["规整后品类"],na =False )].copy ()#line:4080
                O00OOOOOO0O0OO00O =O00OOOOOO0O0OO00O .loc [O00OOOOOO0O0OO00O ["产品类别"].str .contains (O0OO000000OOOO0O0 ["产品类别"],na =False )].copy ()#line:4081
                O00OOOOOO0O0OO00O ["报表类型"]=O0OO000000OOOO0O0 ["报表类型"]+"1"#line:4083
                if OO00OOOOO00OOO00O =="特定品种":#line:4084
                    TABLE_tree_Level_2 (Countall (O00OOOOOO0O0OO00O ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],O0OO000000OOOO0O0 ["规整后品类"],O0OO000000OOOO0O0 ["注册证编号/曾用注册证编号"]),1 ,O00OOOOOO0O0OO00O )#line:4085
                else :#line:4086
                    TABLE_tree_Level_2 (Countall (O00OOOOOO0O0OO00O ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],OO00OOOOO00OOO00O ,O0OO000000OOOO0O0 ["注册证编号/曾用注册证编号"]),1 ,O00OOOOOO0O0OO00O )#line:4087
            def O0O0OO0OO0O0O00O0 (event =None ):#line:4089
                for OO00OO0O0O00OO000 in O0O0000OOO00O000O .selection ():#line:4090
                    OOOO0OOO0O000000O =O0O0000OOO00O000O .item (OO00OO0O0O00OO000 ,"values")#line:4091
                OOOO00O0O000O0O00 =dict (zip (OO0OOOOOO0O0OOO0O ,OOOO0OOO0O000000O ))#line:4092
                OOO000O0O0000OO0O =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==OOOO00O0O000O0O00 ["注册证编号/曾用注册证编号"])].copy ()#line:4093
                OOO000O0O0000OO0O ["报表类型"]=OOOO00O0O000O0O00 ["报表类型"]+"1"#line:4094
                TABLE_tree_Level_2 (Countall (OOO000O0O0000OO0O ).df_pihao (),1 ,OOO000O0O0000OO0O ,)#line:4099
            def O000O0OOO0OOO0O00 (event =None ):#line:4101
                for O000OO0OOO0O0O00O in O0O0000OOO00O000O .selection ():#line:4102
                    O0OOO0O000OOOO00O =O0O0000OOO00O000O .item (O000OO0OOO0O0O00O ,"values")#line:4103
                OOO00OO00OO00O00O =dict (zip (OO0OOOOOO0O0OOO0O ,O0OOO0O000OOOO00O ))#line:4104
                OO00OO0OOOOO00O00 =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==OOO00OO00OO00O00O ["注册证编号/曾用注册证编号"])].copy ()#line:4105
                OO00OO0OOOOO00O00 ["报表类型"]=OOO00OO00OO00O00O ["报表类型"]+"1"#line:4106
                TABLE_tree_Level_2 (Countall (OO00OO0OOOOO00O00 ).df_xinghao (),1 ,OO00OO0OOOOO00O00 ,)#line:4111
            def OOO00OO000O00O0O0 (event =None ):#line:4113
                for O0O0O00O0000000O0 in O0O0000OOO00O000O .selection ():#line:4114
                    OO000O000O0O0000O =O0O0000OOO00O000O .item (O0O0O00O0000000O0 ,"values")#line:4115
                O000O0O0O00O0OO00 =dict (zip (OO0OOOOOO0O0OOO0O ,OO000O000O0O0000O ))#line:4116
                O00OO000OOO0OO00O =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==O000O0O0O00O0OO00 ["注册证编号/曾用注册证编号"])].copy ()#line:4117
                O00OO000OOO0OO00O ["报表类型"]=O000O0O0O00O0OO00 ["报表类型"]+"1"#line:4118
                TABLE_tree_Level_2 (Countall (O00OO000OOO0OO00O ).df_user (),1 ,O00OO000OOO0OO00O ,)#line:4123
            def OOO00O000O000O0O0 (event =None ):#line:4125
                for OO00O00O00O0OOOO0 in O0O0000OOO00O000O .selection ():#line:4127
                    O000O0OO0OO0O0OO0 =O0O0000OOO00O000O .item (OO00O00O00O0OOOO0 ,"values")#line:4128
                OO00OO0O00000O0OO =dict (zip (OO0OOOOOO0O0OOO0O ,O000O0OO0OO0O0OO0 ))#line:4129
                OO00O0O00OOOO0O0O =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==OO00OO0O00000O0OO ["注册证编号/曾用注册证编号"])].copy ()#line:4130
                OO00O0O00OOOO0O0O ["报表类型"]=OO00OO0O00000O0OO ["报表类型"]+"1"#line:4131
                OO000O0OOOO000000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:4132
                if ini ["模式"]=="药品":#line:4133
                    OO000O0OOOO000000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:4134
                if ini ["模式"]=="器械":#line:4135
                    OO000O0OOOO000000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:4136
                if ini ["模式"]=="化妆品":#line:4137
                    OO000O0OOOO000000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:4138
                O000000OO00OO0OO0 =OO000O0OOOO000000 ["值"][3 ]+"|"+OO000O0OOOO000000 ["值"][4 ]#line:4139
                if ini ["模式"]=="器械":#line:4140
                    OO00O0O00OOOO0O0O ["关键字查找列"]=OO00O0O00OOOO0O0O ["器械故障表现"].astype (str )+OO00O0O00OOOO0O0O ["伤害表现"].astype (str )+OO00O0O00OOOO0O0O ["使用过程"].astype (str )+OO00O0O00OOOO0O0O ["事件原因分析描述"].astype (str )+OO00O0O00OOOO0O0O ["初步处置情况"].astype (str )#line:4141
                else :#line:4142
                    OO00O0O00OOOO0O0O ["关键字查找列"]=OO00O0O00OOOO0O0O ["器械故障表现"].astype (str )#line:4143
                OO00O0O00OOOO0O0O =OO00O0O00OOOO0O0O .loc [OO00O0O00OOOO0O0O ["关键字查找列"].str .contains (O000000OO00OO0OO0 ,na =False )].copy ().reset_index (drop =True )#line:4144
                TABLE_tree_Level_2 (OO00O0O00OOOO0O0O ,0 ,OO00O0O00OOOO0O0O ,)#line:4150
            def O0OO0OO000O000OOO (event =None ):#line:4153
                for OOO0OOOO000O00OOO in O0O0000OOO00O000O .selection ():#line:4154
                    O00000OO0OO0OOO0O =O0O0000OOO00O000O .item (OOO0OOOO000O00OOO ,"values")#line:4155
                O0000OO00O0O0OOOO =dict (zip (OO0OOOOOO0O0OOO0O ,O00000OO0OO0OOO0O ))#line:4156
                O0O00O0O00000OOOO =OO0O00000O000O0OO [0 ][(OO0O00000O000O0OO [0 ]["注册证编号/曾用注册证编号"]==O0000OO00O0O0OOOO ["注册证编号/曾用注册证编号"])].copy ()#line:4157
                O0O00O0O00000OOOO ["报表类型"]=O0000OO00O0O0OOOO ["报表类型"]+"1"#line:4158
                TOOLS_time (O0O00O0O00000OOOO ,"事件发生日期",0 )#line:4159
            def OOO0OO0000O00OO00 (O0O00O000OOO0000O ,O000OO0000000O0O0 ):#line:4161
                for OO0OO0OOOO0OOO000 in O0O0000OOO00O000O .selection ():#line:4163
                    O0O0000OOOO000OO0 =O0O0000OOO00O000O .item (OO0OO0OOOO0OOO000 ,"values")#line:4164
                OOO0000O000OO0OO0 =dict (zip (OO0OOOOOO0O0OOO0O ,O0O0000OOOO000OO0 ))#line:4165
                O00O0O0O0000000O0 =OO0O00000O000O0OO [0 ]#line:4166
                if OOO0000O000OO0OO0 ["规整后品类"]=="N":#line:4167
                    if O0O00O000OOO0000O =="特定品种":#line:4168
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4169
                        return 0 #line:4170
                O00O0O0O0000000O0 =O00O0O0O0000000O0 .loc [O00O0O0O0000000O0 ["注册证编号/曾用注册证编号"].str .contains (OOO0000O000OO0OO0 ["注册证编号/曾用注册证编号"],na =False )].copy ()#line:4171
                O00O0O0O0000000O0 ["报表类型"]=OOO0000O000OO0OO0 ["报表类型"]+"1"#line:4172
                if O0O00O000OOO0000O =="特定品种":#line:4173
                    TABLE_tree_Level_2 (Countall (O00O0O0O0000000O0 ).df_find_all_keword_risk (O000OO0000000O0O0 ,OOO0000O000OO0OO0 ["规整后品类"]),1 ,O00O0O0O0000000O0 )#line:4174
                else :#line:4175
                    TABLE_tree_Level_2 (Countall (O00O0O0O0000000O0 ).df_find_all_keword_risk (O000OO0000000O0O0 ,O0O00O000OOO0000O ),1 ,O00O0O0O0000000O0 )#line:4176
            O000OO0O0000O000O =Menu (OOO0O00O0O000OOO0 ,tearoff =False ,)#line:4180
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"故障表现分类（无源）",command =lambda :O00OO0O0O000OO00O ("通用无源"))#line:4181
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"故障表现分类（有源）",command =lambda :O00OO0O0O000OO00O ("通用有源"))#line:4182
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"故障表现分类（特定品种）",command =lambda :O00OO0O0O000OO00O ("特定品种"))#line:4183
            O000OO0O0000O000O .add_separator ()#line:4185
            if O0O0OO0O00O0OO0OO =="":#line:4186
                O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"同类比较(ROR-无源)",command =lambda :OOOO000OO0OOOOOOO ("无源"))#line:4187
                O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"同类比较(ROR-有源)",command =lambda :OOOO000OO0OOOOOOO ("有源"))#line:4188
                O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"同类比较(ROR-特定品种)",command =lambda :OOOO000OO0OOOOOOO ("特定品种"))#line:4189
            O000OO0O0000O000O .add_separator ()#line:4191
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(批号-无源)",command =lambda :OOO0OO0000O00OO00 ("无源","产品批号"))#line:4192
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(批号-特定品种)",command =lambda :OOO0OO0000O00OO00 ("特定品种","产品批号"))#line:4193
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(月份-无源)",command =lambda :OOO0OO0000O00OO00 ("无源","事件发生月份"))#line:4194
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(月份-有源)",command =lambda :OOO0OO0000O00OO00 ("有源","事件发生月份"))#line:4195
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(月份-特定品种)",command =lambda :OOO0OO0000O00OO00 ("特定品种","事件发生月份"))#line:4196
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(季度-无源)",command =lambda :OOO0OO0000O00OO00 ("无源","事件发生季度"))#line:4197
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(季度-有源)",command =lambda :OOO0OO0000O00OO00 ("有源","事件发生季度"))#line:4198
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"关键字趋势(季度-特定品种)",command =lambda :OOO0OO0000O00OO00 ("特定品种","事件发生季度"))#line:4199
            O000OO0O0000O000O .add_separator ()#line:4201
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"各批号报送情况",command =O0O0OO0OO0O0O00O0 )#line:4202
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"各型号报送情况",command =O000O0OOO0OOO0O00 )#line:4203
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"报告单位情况",command =OOO00OO000O00O0O0 )#line:4204
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"事件发生时间曲线",command =O0OO0OO000O000OOO )#line:4205
            O000OO0O0000O000O .add_separator ()#line:4206
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"原始数据",command =O0O00OO000OO0O0O0 )#line:4207
            if O0O0OO0O00O0OO0OO =="":#line:4208
                O000OO0O0000O000O .add_command (label ="近30天原始数据",command =OOO00O0OO0OO0OO0O )#line:4209
            O000OO0O0000O000O .add_command (label =OOOOO00O0O0O0O0O0 +"高度关注(一级和二级)",command =OOO00O000O000O0O0 )#line:4210
            def O00O0OO0OO0OO00O0 (OOO000O0OOO0OOOO0 ):#line:4212
                O000OO0O0000O000O .post (OOO000O0OOO0OOOO0 .x_root ,OOO000O0OOO0OOOO0 .y_root )#line:4213
            OOO0O00O0O000OOO0 .bind ("<Button-3>",O00O0OO0OO0OO00O0 )#line:4214
    if OOOO0000000OOOO00 ==0 or "规整编码"in O0O0O000OO0000000 .columns :#line:4217
        O0O0000OOO00O000O .bind ("<Double-1>",lambda O0O0OOOOOOO00OOO0 :OO0OOO0OO0O00O000 (O0O0OOOOOOO00OOO0 ,O0O0O000OO0000000 ))#line:4218
    if OOOO0000000OOOO00 ==1 and "规整编码"not in O0O0O000OO0000000 .columns :#line:4219
        O0O0000OOO00O000O .bind ("<Double-1>",lambda O0OO0O0O00O0000OO :O00OOOOO00O00000O (O0OO0O0O00O0000OO ,OO0OOOOOO0O0OOO0O ,O000OOOOOO00OO0O0 ))#line:4220
    def OO0OO0O0O0000OO0O (O00O00O0OOO000O00 ,OO0O0O0OO0O0OO0O0 ,OOO0O0O0O0O0O0000 ):#line:4223
        O000OO000O0000OO0 =[(O00O00O0OOO000O00 .set (OOO00O00OOO0O000O ,OO0O0O0OO0O0OO0O0 ),OOO00O00OOO0O000O )for OOO00O00OOO0O000O in O00O00O0OOO000O00 .get_children ("")]#line:4224
        O000OO000O0000OO0 .sort (reverse =OOO0O0O0O0O0O0000 )#line:4225
        for OO0OO000OOOO00O0O ,(OOOO0OOO00O0OO0O0 ,O00OOO00000OO00OO )in enumerate (O000OO000O0000OO0 ):#line:4227
            O00O00O0OOO000O00 .move (O00OOO00000OO00OO ,"",OO0OO000OOOO00O0O )#line:4228
        O00O00O0OOO000O00 .heading (OO0O0O0OO0O0OO0O0 ,command =lambda :OO0OO0O0O0000OO0O (O00O00O0OOO000O00 ,OO0O0O0OO0O0OO0O0 ,not OOO0O0O0O0O0O0000 ))#line:4231
    for OOO00000O0OOO00O0 in OO0OOOOOO0O0OOO0O :#line:4233
        O0O0000OOO00O000O .heading (OOO00000O0OOO00O0 ,text =OOO00000O0OOO00O0 ,command =lambda _col =OOO00000O0OOO00O0 :OO0OO0O0O0000OO0O (O0O0000OOO00O000O ,_col ,False ),)#line:4238
    def OO0OOO0OO0O00O000 (O0O00OOO0O00O00O0 ,OOO000OOO0000OO00 ):#line:4242
        if "规整编码"in OOO000OOO0000OO00 .columns :#line:4244
            OOO000OOO0000OO00 =OOO000OOO0000OO00 .rename (columns ={"规整编码":"报告编码"})#line:4245
        for O0000O000000OOO00 in O0O0000OOO00O000O .selection ():#line:4247
            O0OO0O0O0OOOO0OOO =O0O0000OOO00O000O .item (O0000O000000OOO00 ,"values")#line:4248
            O0OO00OO00O0O0O00 =Toplevel ()#line:4251
            O000OO0OO0000O0O0 =O0OO00OO00O0O0O00 .winfo_screenwidth ()#line:4253
            O0OOO0O0O0O0OOO00 =O0OO00OO00O0O0O00 .winfo_screenheight ()#line:4255
            OO0O0O00OO000O0OO =800 #line:4257
            O0OO000000OO00000 =600 #line:4258
            O0OOOOO0O00OOO0OO =(O000OO0OO0000O0O0 -OO0O0O00OO000O0OO )/2 #line:4260
            OOO00O0OO00O0OOOO =(O0OOO0O0O0O0OOO00 -O0OO000000OO00000 )/2 #line:4261
            O0OO00OO00O0O0O00 .geometry ("%dx%d+%d+%d"%(OO0O0O00OO000O0OO ,O0OO000000OO00000 ,O0OOOOO0O00OOO0OO ,OOO00O0OO00O0OOOO ))#line:4262
            OOO0O00O00OO0OO0O =ScrolledText (O0OO00OO00O0O0O00 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:4266
            OOO0O00O00OO0OO0O .pack (padx =10 ,pady =10 )#line:4267
            def O0O0OO0O00O0O0OO0 (event =None ):#line:4268
                OOO0O00O00OO0OO0O .event_generate ('<<Copy>>')#line:4269
            def OO00OO00OOO00OO0O (OO0O000OO00000O0O ,O00OO0O0O0OO0000O ):#line:4270
                TOOLS_savetxt (OO0O000OO00000O0O ,O00OO0O0O0OO0000O ,1 )#line:4271
            O0OOO0000000OOOO0 =Menu (OOO0O00O00OO0OO0O ,tearoff =False ,)#line:4272
            O0OOO0000000OOOO0 .add_command (label ="复制",command =O0O0OO0O00O0O0OO0 )#line:4273
            O0OOO0000000OOOO0 .add_command (label ="导出",command =lambda :PROGRAM_thread_it (OO00OO00OOO00OO0O ,OOO0O00O00OO0OO0O .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =OOO000OOO0000OO00 .iloc [0 ,0 ],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:4274
            def O00OO000O0OO00O00 (O0O0O0OOOO0OO000O ):#line:4276
                O0OOO0000000OOOO0 .post (O0O0O0OOOO0OO000O .x_root ,O0O0O0OOOO0OO000O .y_root )#line:4277
            OOO0O00O00OO0OO0O .bind ("<Button-3>",O00OO000O0OO00O00 )#line:4278
            try :#line:4280
                O0OO00OO00O0O0O00 .title (str (O0OO0O0O0OOOO0OOO [0 ]))#line:4281
                OOO000OOO0000OO00 ["报告编码"]=OOO000OOO0000OO00 ["报告编码"].astype ("str")#line:4282
                OOOOO0OO0O000O000 =OOO000OOO0000OO00 [(OOO000OOO0000OO00 ["报告编码"]==str (O0OO0O0O0OOOO0OOO [0 ]))]#line:4283
            except :#line:4284
                pass #line:4285
            O0O00OO0000O0O000 =OOO000OOO0000OO00 .columns .values .tolist ()#line:4287
            for OOOO00000OO0O0O00 in range (len (O0O00OO0000O0O000 )):#line:4288
                try :#line:4290
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="报告编码.1":#line:4291
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4292
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="产品名称":#line:4293
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4294
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="事件发生日期":#line:4295
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4296
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="是否开展了调查":#line:4297
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4298
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="市级监测机构":#line:4299
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4300
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="上报机构描述":#line:4301
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4302
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]=="持有人处理描述":#line:4303
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4304
                    if OOOO00000OO0O0O00 >1 and O0O00OO0000O0O000 [OOOO00000OO0O0O00 -1 ]=="持有人处理描述":#line:4305
                        OOO0O00O00OO0OO0O .insert (END ,"\n\n")#line:4306
                except :#line:4308
                    pass #line:4309
                try :#line:4310
                    if O0O00OO0000O0O000 [OOOO00000OO0O0O00 ]in ["单位名称","产品名称ori","上报机构描述","持有人处理描述","产品名称","注册证编号/曾用注册证编号","型号","规格","产品批号","上市许可持有人名称ori","上市许可持有人名称","伤害","伤害表现","器械故障表现","使用过程","事件原因分析描述","初步处置情况","调查情况","关联性评价","事件原因分析.1","具体控制措施"]:#line:4311
                        OOO0O00O00OO0OO0O .insert (END ,"●")#line:4312
                except :#line:4313
                    pass #line:4314
                OOO0O00O00OO0OO0O .insert (END ,O0O00OO0000O0O000 [OOOO00000OO0O0O00 ])#line:4315
                OOO0O00O00OO0OO0O .insert (END ,"：")#line:4316
                try :#line:4317
                    OOO0O00O00OO0OO0O .insert (END ,OOOOO0OO0O000O000 .iloc [0 ,OOOO00000OO0O0O00 ])#line:4318
                except :#line:4319
                    OOO0O00O00OO0OO0O .insert (END ,O0OO0O0O0OOOO0OOO [OOOO00000OO0O0O00 ])#line:4320
                OOO0O00O00OO0OO0O .insert (END ,"\n")#line:4321
            OOO0O00O00OO0OO0O .config (state =DISABLED )#line:4322
    O0O0000OOO00O000O .pack ()#line:4324
def TOOLS_get_guize2 (O0OO00OOO0OOO000O ):#line:4327
	""#line:4328
	O00OO0OOOOO0OOO00 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4329
	OO0OO000OOO0000OO =pd .read_excel (O00OO0OOOOO0OOO00 ,header =0 ,sheet_name ="器械")#line:4330
	OOOOOO000OO000O00 =OO0OO000OOO0000OO [["适用范围列","适用范围"]].drop_duplicates ("适用范围")#line:4331
	text .insert (END ,OOOOOO000OO000O00 )#line:4332
	text .see (END )#line:4333
	O000OO0OO000O0OO0 =Toplevel ()#line:4334
	O000OO0OO000O0OO0 .title ('切换通用规则')#line:4335
	OOO0O0O000OO0OOO0 =O000OO0OO000O0OO0 .winfo_screenwidth ()#line:4336
	OOO000O00O0000O0O =O000OO0OO000O0OO0 .winfo_screenheight ()#line:4338
	OOOO000OO00OOO0O0 =450 #line:4340
	O00O0O0O0O0O0O0OO =100 #line:4341
	O0OO0OOOOO0O0000O =(OOO0O0O000OO0OOO0 -OOOO000OO00OOO0O0 )/2 #line:4343
	OOOO000O000OOO000 =(OOO000O00O0000O0O -O00O0O0O0O0O0O0OO )/2 #line:4344
	O000OO0OO000O0OO0 .geometry ("%dx%d+%d+%d"%(OOOO000OO00OOO0O0 ,O00O0O0O0O0O0O0OO ,O0OO0OOOOO0O0000O ,OOOO000O000OOO000 ))#line:4345
	OO000OOO000O0OO0O =Label (O000OO0OO000O0OO0 ,text ="查找位置：器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况")#line:4346
	OO000OOO000O0OO0O .pack ()#line:4347
	OO00OOO00O0OO000O =Label (O000OO0OO000O0OO0 ,text ="请选择您所需要的通用规则关键字：")#line:4348
	OO00OOO00O0OO000O .pack ()#line:4349
	def O00O00O0OO0O0OO0O (*O0000OO000O000OOO ):#line:4350
		OOOOOO0O0000O0000 .set (O0000OO0O0OO000O0 .get ())#line:4351
	OOOOOO0O0000O0000 =StringVar ()#line:4352
	O0000OO0O0OO000O0 =ttk .Combobox (O000OO0OO000O0OO0 ,width =14 ,height =30 ,state ="readonly",textvariable =OOOOOO0O0000O0000 )#line:4353
	O0000OO0O0OO000O0 ["values"]=OOOOOO000OO000O00 ["适用范围"].to_list ()#line:4354
	O0000OO0O0OO000O0 .current (0 )#line:4355
	O0000OO0O0OO000O0 .bind ("<<ComboboxSelected>>",O00O00O0OO0O0OO0O )#line:4356
	O0000OO0O0OO000O0 .pack ()#line:4357
	O0000OOO000OO0OO0 =LabelFrame (O000OO0OO000O0OO0 )#line:4360
	OO0OO0OOO00OO0OOO =Button (O0000OOO000OO0OO0 ,text ="确定",width =10 ,command =lambda :OOO0OOOO0OO0O0O00 (OO0OO000OOO0000OO ,OOOOOO0O0000O0000 .get ()))#line:4361
	OO0OO0OOO00OO0OOO .pack (side =LEFT ,padx =1 ,pady =1 )#line:4362
	O0000OOO000OO0OO0 .pack ()#line:4363
	def OOO0OOOO0OO0O0O00 (OOOOOO000O000OO00 ,O0O0000O00OOOO00O ):#line:4365
		OOO0O000O00O00000 =OOOOOO000O000OO00 .loc [OOOOOO000O000OO00 ["适用范围"].str .contains (O0O0000O00OOOO00O ,na =False )].copy ().reset_index (drop =True )#line:4366
		TABLE_tree_Level_2 (Countall (O0OO00OOO0OOO000O ).df_psur ("特定品种作为通用关键字",OOO0O000O00O00000 ),1 ,O0OO00OOO0OOO000O )#line:4367
def TOOLS_findin (O0O0000O0O0O00OO0 ,O0O0OO0OO00OOO00O ):#line:4368
	""#line:4369
	OO00O000O000O0000 =Toplevel ()#line:4370
	OO00O000O000O0000 .title ('高级查找')#line:4371
	O0000OO000000O0O0 =OO00O000O000O0000 .winfo_screenwidth ()#line:4372
	OOO0OOOOOOOOO0O0O =OO00O000O000O0000 .winfo_screenheight ()#line:4374
	OO000OO000O000O0O =400 #line:4376
	O000O00000OO0OOOO =120 #line:4377
	OOO0O0OO0OO00O00O =(O0000OO000000O0O0 -OO000OO000O000O0O )/2 #line:4379
	O0000O0OOO00O0000 =(OOO0OOOOOOOOO0O0O -O000O00000OO0OOOO )/2 #line:4380
	OO00O000O000O0000 .geometry ("%dx%d+%d+%d"%(OO000OO000O000O0O ,O000O00000OO0OOOO ,OOO0O0OO0OO00O00O ,O0000O0OOO00O0000 ))#line:4381
	OOOO0O0O00OOO000O =Label (OO00O000O000O0000 ,text ="需要查找的关键字（用|隔开）：")#line:4382
	OOOO0O0O00OOO000O .pack ()#line:4383
	O00O0OO0OO0OO000O =Label (OO00O000O000O0000 ,text ="在哪些列查找（用|隔开）：")#line:4384
	OO0OO0O00O00OO0O0 =Entry (OO00O000O000O0000 ,width =80 )#line:4386
	OO0OO0O00O00OO0O0 .insert (0 ,"破裂|断裂")#line:4387
	O0OOO0O0O000O0OO0 =Entry (OO00O000O000O0000 ,width =80 )#line:4388
	O0OOO0O0O000O0OO0 .insert (0 ,"器械故障表现|伤害表现")#line:4389
	OO0OO0O00O00OO0O0 .pack ()#line:4390
	O00O0OO0OO0OO000O .pack ()#line:4391
	O0OOO0O0O000O0OO0 .pack ()#line:4392
	OO0OOO0OOO000000O =LabelFrame (OO00O000O000O0000 )#line:4393
	O0O000O00OOO00OO0 =Button (OO0OOO0OOO000000O ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (TABLE_tree_Level_2 ,OO00000000OO000O0 (OO0OO0O00O00OO0O0 .get (),O0OOO0O0O000O0OO0 .get (),O0O0000O0O0O00OO0 ),1 ,O0O0OO0OO00OOO00O ))#line:4394
	O0O000O00OOO00OO0 .pack (side =LEFT ,padx =1 ,pady =1 )#line:4395
	OO0OOO0OOO000000O .pack ()#line:4396
	def OO00000000OO000O0 (O00000O0O0OOOOOOO ,O000OOOOO0O00OOO0 ,OO0000000OO00OO0O ):#line:4399
		OO0000000OO00OO0O ["关键字查找列10"]="######"#line:4400
		for O000OO00OOO0O000O in TOOLS_get_list (O000OOOOO0O00OOO0 ):#line:4401
			OO0000000OO00OO0O ["关键字查找列10"]=OO0000000OO00OO0O ["关键字查找列10"].astype (str )+OO0000000OO00OO0O [O000OO00OOO0O000O ].astype (str )#line:4402
		OO0000000OO00OO0O =OO0000000OO00OO0O .loc [OO0000000OO00OO0O ["关键字查找列10"].str .contains (O00000O0O0OOOOOOO ,na =False )]#line:4403
		del OO0000000OO00OO0O ["关键字查找列10"]#line:4404
		return OO0000000OO00OO0O #line:4405
def PROGRAM_about ():#line:4407
    ""#line:4408
    OO00OO0OOO0OO0OOO =" 佛山市食品药品检验检测中心 \n(佛山市药品不良反应监测中心)\n蔡权周（QQ或微信411703730）\n仅供政府设立的不良反应监测机构使用。"#line:4409
    showinfo (title ="关于",message =OO00OO0OOO0OO0OOO )#line:4410
def PROGRAM_thread_it (O000OO00OOO0OOOOO ,*O0OO00OOO000O0O0O ):#line:4413
    ""#line:4414
    OO0O0000OO00O00OO =threading .Thread (target =O000OO00OOO0OOOOO ,args =O0OO00OOO000O0O0O )#line:4416
    OO0O0000OO00O00OO .setDaemon (True )#line:4418
    OO0O0000OO00O00OO .start ()#line:4420
def PROGRAM_Menubar (O0O0O00O00OO0O00O ,O0OOO0OOO0OOOOOO0 ,OO000000OOOOO00OO ,O0OO00O0O0OO00O0O ):#line:4421
	""#line:4422
	if ini ["模式"]=="其他":#line:4423
		return 0 #line:4424
	O0OO0O0OO0O0OOO00 =Menu (O0O0O00O00OO0O00O )#line:4425
	O0O0O00O00OO0O00O .config (menu =O0OO0O0OO0O0OOO00 )#line:4427
	OOOO00O0O0OOOO000 =Menu (O0OO0O0OO0O0OOO00 ,tearoff =0 )#line:4431
	O0OO0O0OO0O0OOO00 .add_cascade (label ="信号检测",menu =OOOO00O0O0OOOO000 )#line:4432
	OOOO00O0O0OOOO000 .add_command (label ="数量比例失衡监测-证号内批号",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_findrisk ("产品批号"),1 ,O0OO00O0O0OO00O0O ))#line:4435
	OOOO00O0O0OOOO000 .add_command (label ="数量比例失衡监测-证号内季度",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_findrisk ("事件发生季度"),1 ,O0OO00O0O0OO00O0O ))#line:4437
	OOOO00O0O0OOOO000 .add_command (label ="数量比例失衡监测-证号内月份",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_findrisk ("事件发生月份"),1 ,O0OO00O0O0OO00O0O ))#line:4439
	OOOO00O0O0OOOO000 .add_command (label ="数量比例失衡监测-证号内性别",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_findrisk ("性别"),1 ,O0OO00O0O0OO00O0O ))#line:4441
	OOOO00O0O0OOOO000 .add_command (label ="数量比例失衡监测-证号内年龄段",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_findrisk ("年龄段"),1 ,O0OO00O0O0OO00O0O ))#line:4443
	OOOO00O0O0OOOO000 .add_separator ()#line:4445
	OOOO00O0O0OOOO000 .add_command (label ="关键字检测（同证号内不同批号比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_find_all_keword_risk ("产品批号"),1 ,O0OO00O0O0OO00O0O ))#line:4447
	OOOO00O0O0OOOO000 .add_command (label ="关键字检测（同证号内不同月份比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_find_all_keword_risk ("事件发生月份"),1 ,O0OO00O0O0OO00O0O ))#line:4449
	OOOO00O0O0OOOO000 .add_command (label ="关键字检测（同证号内不同季度比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_find_all_keword_risk ("事件发生季度"),1 ,O0OO00O0O0OO00O0O ))#line:4451
	OOOO00O0O0OOOO000 .add_command (label ="关键字检测（同证号内不同性别比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_find_all_keword_risk ("性别"),1 ,O0OO00O0O0OO00O0O ))#line:4453
	OOOO00O0O0OOOO000 .add_command (label ="关键字检测（同证号内不同年龄段比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_find_all_keword_risk ("年龄段"),1 ,O0OO00O0O0OO00O0O ))#line:4455
	OOOO00O0O0OOOO000 .add_separator ()#line:4457
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同证号的批号间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","产品批号"]),1 ,O0OO00O0O0OO00O0O ))#line:4459
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同证号的月份间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生月份"]),1 ,O0OO00O0O0OO00O0O ))#line:4461
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同证号的季度间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生季度"]),1 ,O0OO00O0O0OO00O0O ))#line:4463
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同证号的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","年龄段"]),1 ,O0OO00O0O0OO00O0O ))#line:4465
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同证号的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","性别"]),1 ,O0OO00O0O0OO00O0O ))#line:4467
	OOOO00O0O0OOOO000 .add_separator ()#line:4469
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同品名的证号间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]),1 ,O0OO00O0O0OO00O0O ))#line:4471
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同品名的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["产品类别","规整后品类","产品名称","年龄段"]),1 ,O0OO00O0O0OO00O0O ))#line:4473
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同品名的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["产品类别","规整后品类","产品名称","性别"]),1 ,O0OO00O0O0OO00O0O ))#line:4475
	OOOO00O0O0OOOO000 .add_separator ()#line:4477
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同类别的名称间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["产品类别","产品名称"]),1 ,O0OO00O0O0OO00O0O ))#line:4479
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同类别的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["产品类别","年龄段"]),1 ,O0OO00O0O0OO00O0O ))#line:4481
	OOOO00O0O0OOOO000 .add_command (label ="关键字ROR-页面内同类别的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_ror (["产品类别","性别"]),1 ,O0OO00O0O0OO00O0O ))#line:4483
	OOOO00O0O0OOOO000 .add_separator ()#line:4494
	if ini ["模式"]=="药品":#line:4495
		OOOO00O0O0OOOO000 .add_command (label ="新的不良反应检测(证号)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0OO00O0O0OO00O0O ,"证号"))#line:4498
		OOOO00O0O0OOOO000 .add_command (label ="新的不良反应检测(品种)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0OO00O0O0OO00O0O ,"品种"))#line:4501
	O0000O00O0OO0OO0O =Menu (O0OO0O0OO0O0OOO00 ,tearoff =0 )#line:4504
	O0OO0O0OO0O0OOO00 .add_cascade (label ="简报制作",menu =O0000O00O0OO0OO0O )#line:4505
	O0000O00O0OO0OO0O .add_command (label ="药品简报",command =lambda :TOOLS_autocount (O0OOO0OOO0OOOOOO0 ,"药品"))#line:4508
	O0000O00O0OO0OO0O .add_command (label ="器械简报",command =lambda :TOOLS_autocount (O0OOO0OOO0OOOOOO0 ,"器械"))#line:4510
	O0000O00O0OO0OO0O .add_command (label ="化妆品简报",command =lambda :TOOLS_autocount (O0OOO0OOO0OOOOOO0 ,"化妆品"))#line:4512
	O0000OO0O00000000 =Menu (O0OO0O0OO0O0OOO00 ,tearoff =0 )#line:4516
	O0OO0O0OO0O0OOO00 .add_cascade (label ="品种评价",menu =O0000OO0O00000000 )#line:4517
	O0000OO0O00000000 .add_command (label ="报告年份",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"报告年份",-1 ))#line:4519
	O0000OO0O00000000 .add_command (label ="发生年份",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"事件发生年份",-1 ))#line:4521
	O0000OO0O00000000 .add_separator ()#line:4522
	O0000OO0O00000000 .add_command (label ="怀疑/并用",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"怀疑/并用",1 ))#line:4524
	O0000OO0O00000000 .add_command (label ="涉及企业",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"上市许可持有人名称",1 ))#line:4526
	O0000OO0O00000000 .add_command (label ="产品名称",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"产品名称",1 ))#line:4528
	O0000OO0O00000000 .add_command (label ="注册证号",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_zhenghao (),1 ,O0OO00O0O0OO00O0O ))#line:4530
	O0000OO0O00000000 .add_separator ()#line:4531
	O0000OO0O00000000 .add_command (label ="年龄段分布",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"年龄段",1 ))#line:4533
	O0000OO0O00000000 .add_command (label ="性别分布",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"性别",1 ))#line:4535
	O0000OO0O00000000 .add_command (label ="年龄性别分布",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_age (),1 ,O0OO00O0O0OO00O0O ,))#line:4537
	O0000OO0O00000000 .add_separator ()#line:4538
	O0000OO0O00000000 .add_command (label ="不良反应发生时间",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"时隔",1 ))#line:4540
	O0000OO0O00000000 .add_command (label ="报告类型-严重程度",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"报告类型-严重程度",1 ))#line:4543
	O0000OO0O00000000 .add_command (label ="停药减药后反应是否减轻或消失",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"停药减药后反应是否减轻或消失",1 ))#line:4545
	O0000OO0O00000000 .add_command (label ="再次使用可疑药是否出现同样反应",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"再次使用可疑药是否出现同样反应",1 ))#line:4547
	O0000OO0O00000000 .add_command (label ="对原患疾病影响",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"对原患疾病影响",1 ))#line:4549
	O0000OO0O00000000 .add_command (label ="不良反应结果",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"不良反应结果",1 ))#line:4551
	O0000OO0O00000000 .add_command (label ="报告单位关联性评价",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"关联性评价",1 ))#line:4553
	O0000OO0O00000000 .add_separator ()#line:4554
	O0000OO0O00000000 .add_command (label ="不良反应转归情况",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"不良反应结果2",4 ))#line:4556
	O0000OO0O00000000 .add_command (label ="关联性评价汇总",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"关联性评价汇总",5 ))#line:4558
	O0000OO0O00000000 .add_separator ()#line:4562
	O0000OO0O00000000 .add_command (label ="不良反应-术语",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"器械故障表现",0 ))#line:4564
	O0000OO0O00000000 .add_command (label ="不良反应器官系统-术语",command =lambda :TABLE_tree_Level_2 (Countall (O0OOO0OOO0OOOOOO0 ).df_psur (),1 ,O0OO00O0O0OO00O0O ))#line:4566
	O0000OO0O00000000 .add_command (label ="不良反应-由code转化",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"不良反应-code",2 ))#line:4568
	O0000OO0O00000000 .add_command (label ="不良反应器官系统-由code转化",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"不良反应-code",3 ))#line:4570
	O0000OO0O00000000 .add_separator ()#line:4572
	O0000OO0O00000000 .add_command (label ="疾病名称-术语",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"相关疾病信息[疾病名称]-术语",0 ))#line:4574
	O0000OO0O00000000 .add_command (label ="疾病名称-由code转化",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"相关疾病信息[疾病名称]-code",2 ))#line:4576
	O0000OO0O00000000 .add_command (label ="疾病器官系统-由code转化",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"相关疾病信息[疾病名称]-code",3 ))#line:4578
	O0000OO0O00000000 .add_separator ()#line:4579
	O0000OO0O00000000 .add_command (label ="适应症-术语",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"治疗适应症-术语",0 ))#line:4581
	O0000OO0O00000000 .add_command (label ="适应症-由code转化",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"治疗适应症-code",2 ))#line:4583
	O0000OO0O00000000 .add_command (label ="适应症器官系统-由code转化",command =lambda :STAT_pinzhong (O0OOO0OOO0OOOOOO0 ,"治疗适应症-code",3 ))#line:4585
	O0OO00OOO00O000O0 =Menu (O0OO0O0OO0O0OOO00 ,tearoff =0 )#line:4587
	O0OO0O0OO0O0OOO00 .add_cascade (label ="基础研究",menu =O0OO00OOO00O000O0 )#line:4588
	O0OO00OOO00O000O0 .add_command (label ="基础信息批量操作（品名）",command =lambda :TOOLS_ror_mode1 (O0OOO0OOO0OOOOOO0 ,"产品名称"))#line:4590
	O0OO00OOO00O000O0 .add_command (label ="器官系统分类批量操作（品名）",command =lambda :TOOLS_ror_mode4 (O0OOO0OOO0OOOOOO0 ,"产品名称"))#line:4592
	O0OO00OOO00O000O0 .add_command (label ="器官系统ROR批量操作（品名）",command =lambda :TOOLS_ror_mode2 (O0OOO0OOO0OOOOOO0 ,"产品名称"))#line:4594
	O0OO00OOO00O000O0 .add_command (label ="ADR-ROR批量操作（品名）",command =lambda :TOOLS_ror_mode3 (O0OOO0OOO0OOOOOO0 ,"产品名称"))#line:4596
	O0OO00OOO00O000O0 .add_separator ()#line:4597
	O0OO00OOO00O000O0 .add_command (label ="基础信息批量操作（注册证号）",command =lambda :TOOLS_ror_mode1 (O0OOO0OOO0OOOOOO0 ,"注册证编号/曾用注册证编号"))#line:4599
	O0OO00OOO00O000O0 .add_command (label ="器官系统分类批量操作（注册证号）",command =lambda :TOOLS_ror_mode4 (O0OOO0OOO0OOOOOO0 ,"注册证编号/曾用注册证编号"))#line:4601
	O0OO00OOO00O000O0 .add_command (label ="器官系统ROR批量操作（注册证号）",command =lambda :TOOLS_ror_mode2 (O0OOO0OOO0OOOOOO0 ,"注册证编号/曾用注册证编号"))#line:4603
	O0OO00OOO00O000O0 .add_command (label ="ADR-ROR批量操作（注册证号）",command =lambda :TOOLS_ror_mode3 (O0OOO0OOO0OOOOOO0 ,"注册证编号/曾用注册证编号"))#line:4605
	O0OOOOOO0O00O0000 =Menu (O0OO0O0OO0O0OOO00 ,tearoff =0 )#line:4607
	O0OO0O0OO0O0OOO00 .add_cascade (label ="风险预警",menu =O0OOOOOO0O00O0000 )#line:4608
	O0OOOOOO0O00O0000 .add_command (label ="预警（单日）",command =lambda :TOOLS_keti (O0OOO0OOO0OOOOOO0 ))#line:4610
	O0OOOOOO0O00O0000 .add_command (label ="事件分布（器械）",command =lambda :TOOLS_get_guize2 (O0OOO0OOO0OOOOOO0 ))#line:4613
	O000OO0OOO000O0OO =Menu (O0OO0O0OO0O0OOO00 ,tearoff =0 )#line:4620
	O0OO0O0OO0O0OOO00 .add_cascade (label ="实用工具",menu =O000OO0OOO000O0OO )#line:4621
	O000OO0OOO000O0OO .add_command (label ="数据规整（报告单位）",command =lambda :TOOL_guizheng (O0OOO0OOO0OOOOOO0 ,2 ,False ))#line:4625
	O000OO0OOO000O0OO .add_command (label ="数据规整（产品名称）",command =lambda :TOOL_guizheng (O0OOO0OOO0OOOOOO0 ,3 ,False ))#line:4627
	O000OO0OOO000O0OO .add_command (label ="数据规整（自定义）",command =lambda :TOOL_guizheng (O0OOO0OOO0OOOOOO0 ,0 ,False ))#line:4629
	O000OO0OOO000O0OO .add_separator ()#line:4631
	O000OO0OOO000O0OO .add_command (label ="原始导入",command =TOOLS_fileopen )#line:4633
	O000OO0OOO000O0OO .add_command (label ="脱敏保存",command =lambda :TOOLS_data_masking (O0OOO0OOO0OOOOOO0 ))#line:4635
	O000OO0OOO000O0OO .add_separator ()#line:4636
	O000OO0OOO000O0OO .add_command (label ="批量筛选（默认）",command =lambda :TOOLS_xuanze (O0OOO0OOO0OOOOOO0 ,1 ))#line:4638
	O000OO0OOO000O0OO .add_command (label ="批量筛选（自定义）",command =lambda :TOOLS_xuanze (O0OOO0OOO0OOOOOO0 ,0 ))#line:4640
	O000OO0OOO000O0OO .add_separator ()#line:4641
	O000OO0OOO000O0OO .add_command (label ="评价人员（广东化妆品）",command =lambda :TOOL_person (O0OOO0OOO0OOOOOO0 ))#line:4643
	O000OO0OOO000O0OO .add_separator ()#line:4644
	O000OO0OOO000O0OO .add_command (label ="意见反馈",command =lambda :PROGRAM_helper (["","  药械妆不良反应报表统计分析工作站","  开发者：蔡权周","  邮箱：411703730@qq.com","  微信号：sysucai","  手机号：18575757461"]))#line:4648
	O000OO0OOO000O0OO .add_command (label ="更改用户组",command =lambda :PROGRAM_thread_it (display_random_number ))#line:4650
def PROGRAM_helper (O00OOOOO000O0OOO0 ):#line:4654
    ""#line:4655
    OO000O0O00O0OO0OO =Toplevel ()#line:4656
    OO000O0O00O0OO0OO .title ("信息查看")#line:4657
    OO000O0O00O0OO0OO .geometry ("700x500")#line:4658
    O0OOOOOO0OO00OOOO =Scrollbar (OO000O0O00O0OO0OO )#line:4660
    O0OO00OO00O000OO0 =Text (OO000O0O00O0OO0OO ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:4661
    O0OOOOOO0OO00OOOO .pack (side =RIGHT ,fill =Y )#line:4662
    O0OO00OO00O000OO0 .pack ()#line:4663
    O0OOOOOO0OO00OOOO .config (command =O0OO00OO00O000OO0 .yview )#line:4664
    O0OO00OO00O000OO0 .config (yscrollcommand =O0OOOOOO0OO00OOOO .set )#line:4665
    for OOOOO0OO00OO0OOOO in O00OOOOO000O0OOO0 :#line:4667
        O0OO00OO00O000OO0 .insert (END ,OOOOO0OO00OO0OOOO )#line:4668
        O0OO00OO00O000OO0 .insert (END ,"\n")#line:4669
    def O0OO00OOO0O000OO0 (event =None ):#line:4672
        O0OO00OO00O000OO0 .event_generate ('<<Copy>>')#line:4673
    OOOO000OO0O0O0OO0 =Menu (O0OO00OO00O000OO0 ,tearoff =False ,)#line:4676
    OOOO000OO0O0O0OO0 .add_command (label ="复制",command =O0OO00OOO0O000OO0 )#line:4677
    def OO00OO0O0O000OOO0 (OOO00O0O00OOO0OOO ):#line:4678
         OOOO000OO0O0O0OO0 .post (OOO00O0O00OOO0OOO .x_root ,OOO00O0O00OOO0OOO .y_root )#line:4679
    O0OO00OO00O000OO0 .bind ("<Button-3>",OO00OO0O0O000OOO0 )#line:4680
    O0OO00OO00O000OO0 .config (state =DISABLED )#line:4682
def PROGRAM_change_schedule (OOOOOOOO00000O0O0 ,O00OOOO00000OOOO0 ):#line:4684
    ""#line:4685
    canvas .coords (fill_rec ,(5 ,5 ,(OOOOOOOO00000O0O0 /O00OOOO00000OOOO0 )*680 ,25 ))#line:4687
    root .update ()#line:4688
    x .set (str (round (OOOOOOOO00000O0O0 /O00OOOO00000OOOO0 *100 ,2 ))+"%")#line:4689
    if round (OOOOOOOO00000O0O0 /O00OOOO00000OOOO0 *100 ,2 )==100.00 :#line:4690
        x .set ("完成")#line:4691
def PROGRAM_showWelcome ():#line:4694
    ""#line:4695
    OOO0000OO0OO000OO =roox .winfo_screenwidth ()#line:4696
    OOO0O00OO00O0O0O0 =roox .winfo_screenheight ()#line:4698
    roox .overrideredirect (True )#line:4700
    roox .attributes ("-alpha",1 )#line:4701
    OOOO00O0O000OO0OO =(OOO0000OO0OO000OO -475 )/2 #line:4702
    OO000OOOOO000O000 =(OOO0O00OO00O0O0O0 -200 )/2 #line:4703
    roox .geometry ("675x130+%d+%d"%(OOOO00O0O000OO0OO ,OO000OOOOO000O000 ))#line:4705
    roox ["bg"]="green"#line:4706
    O0O0OOOO00O0000OO =Label (roox ,text =title_all2 ,fg ="white",bg ="green",font =("微软雅黑",20 ))#line:4709
    O0O0OOOO00O0000OO .place (x =0 ,y =15 ,width =675 ,height =90 )#line:4710
    OO0000OO0OOO0OO0O =Label (roox ,text ="仅供监测机构使用 ",fg ="white",bg ="black",font =("微软雅黑",15 ))#line:4713
    OO0000OO0OOO0OO0O .place (x =0 ,y =90 ,width =675 ,height =40 )#line:4714
def PROGRAM_closeWelcome ():#line:4717
    ""#line:4718
    for O0O0O000O00000OO0 in range (2 ):#line:4719
        root .attributes ("-alpha",0 )#line:4720
        time .sleep (1 )#line:4721
    root .attributes ("-alpha",1 )#line:4722
    roox .destroy ()#line:4723
class Countall ():#line:4738
	""#line:4739
	def __init__ (OOOO0O000000O0O0O ,OO000OOOOOO00O00O ):#line:4740
		""#line:4741
		OOOO0O000000O0O0O .df =OO000OOOOOO00O00O #line:4742
		OOOO0O000000O0O0O .mode =ini ["模式"]#line:4743
	def df_org (O00000OO000O000O0 ,O0OOOO00000O00O0O ):#line:4745
		""#line:4746
		O0OO0O0OO00O00O0O =O00000OO000O000O0 .df .drop_duplicates (["报告编码"]).groupby ([O0OOOO00000O00O0O ]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda O00OOOOOO00OO0O00 :STAT_countpx (O00OOOOOO00OO0O00 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOOO00O0O000OOOO :STAT_countpx (OOOOO00O0O000OOOO .values ,"死亡")),超时报告数 =("超时标记",lambda OOO000OOOOOO0OOO0 :STAT_countpx (OOO000OOOOOO0OOO0 .values ,1 )),有源 =("产品类别",lambda O00OO0O000O0OOO00 :STAT_countpx (O00OO0O000O0OOO00 .values ,"有源")),无源 =("产品类别",lambda O0OO0OO0OOO00OOOO :STAT_countpx (O0OO0OO0OOO00OOOO .values ,"无源")),体外诊断试剂 =("产品类别",lambda O00O000000O0OOO0O :STAT_countpx (O00O000000O0OOO0O .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda OOO0O0OOO0OO00O00 :STAT_countpx (OOO0O0OOO0OO00O00 .values ,"Ⅲ类")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4761
		OOO0O0O0O000OOOO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量","单位个数"]#line:4763
		O0OO0O0OO00O00O0O .loc ["合计"]=O0OO0O0OO00O00O0O [OOO0O0O0O000OOOO0 ].apply (lambda OOOOO00000O00OO00 :OOOOO00000O00OO00 .sum ())#line:4764
		O0OO0O0OO00O00O0O [OOO0O0O0O000OOOO0 ]=O0OO0O0OO00O00O0O [OOO0O0O0O000OOOO0 ].apply (lambda OOOOOO00OOOOO0OO0 :OOOOOO00OOOOO0OO0 .astype (int ))#line:4765
		O0OO0O0OO00O00O0O .iloc [-1 ,0 ]="合计"#line:4766
		O0OO0O0OO00O00O0O ["严重比"]=round ((O0OO0O0OO00O00O0O ["严重伤害数"]+O0OO0O0OO00O00O0O ["死亡数量"])/O0OO0O0OO00O00O0O ["报告数量"]*100 ,2 )#line:4768
		O0OO0O0OO00O00O0O ["Ⅲ类比"]=round ((O0OO0O0OO00O00O0O ["三类数量"])/O0OO0O0OO00O00O0O ["报告数量"]*100 ,2 )#line:4769
		O0OO0O0OO00O00O0O ["超时比"]=round ((O0OO0O0OO00O00O0O ["超时报告数"])/O0OO0O0OO00O00O0O ["报告数量"]*100 ,2 )#line:4770
		O0OO0O0OO00O00O0O ["报表类型"]="dfx_org"+O0OOOO00000O00O0O #line:4771
		if ini ["模式"]=="药品":#line:4774
			del O0OO0O0OO00O00O0O ["有源"]#line:4776
			del O0OO0O0OO00O00O0O ["无源"]#line:4777
			del O0OO0O0OO00O00O0O ["体外诊断试剂"]#line:4778
			O0OO0O0OO00O00O0O =O0OO0O0OO00O00O0O .rename (columns ={"三类数量":"新的和严重的数量"})#line:4779
			O0OO0O0OO00O00O0O =O0OO0O0OO00O00O0O .rename (columns ={"Ⅲ类比":"新严比"})#line:4780
		return O0OO0O0OO00O00O0O #line:4782
	def df_user (OO0O0O0O00O00O0O0 ):#line:4786
		""#line:4787
		OO0O0O0O00O00O0O0 .df ["医疗机构类别"]=OO0O0O0O00O00O0O0 .df ["医疗机构类别"].fillna ("未填写")#line:4788
		OO0OOOO0OOO0O0OO0 =OO0O0O0O00O00O0O0 .df .drop_duplicates (["报告编码"]).groupby (["监测机构","单位名称","医疗机构类别"]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OO0O0O00OO0O000O0 :STAT_countpx (OO0O0O00OO0O000O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO000O0O000O0O00 :STAT_countpx (OOO000O0O000O0O00 .values ,"死亡")),超时报告数 =("超时标记",lambda OOO0OO0OOO0OO00O0 :STAT_countpx (OOO0OO0OOO0OO00O0 .values ,1 )),有源 =("产品类别",lambda OOO0OO00O0O0OOO0O :STAT_countpx (OOO0OO00O0O0OOO0O .values ,"有源")),无源 =("产品类别",lambda O00OOOO00000000O0 :STAT_countpx (O00OOOO00000000O0 .values ,"无源")),体外诊断试剂 =("产品类别",lambda OOO0O0OOOOOO0OOO0 :STAT_countpx (OOO0O0OOOOOO0OOO0 .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda O00OOOO00OOO0OO0O :STAT_countpx (O00OOOO00OOO0OO0O .values ,"Ⅲ类")),产品数量 =("产品名称","nunique"),产品清单 =("产品名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4803
		O0OOOOO00000O0OO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量"]#line:4806
		OO0OOOO0OOO0O0OO0 .loc ["合计"]=OO0OOOO0OOO0O0OO0 [O0OOOOO00000O0OO0 ].apply (lambda OO0OO00O0O0OOOO00 :OO0OO00O0O0OOOO00 .sum ())#line:4807
		OO0OOOO0OOO0O0OO0 [O0OOOOO00000O0OO0 ]=OO0OOOO0OOO0O0OO0 [O0OOOOO00000O0OO0 ].apply (lambda O0O0OO0O0O00OO00O :O0O0OO0O0O00OO00O .astype (int ))#line:4808
		OO0OOOO0OOO0O0OO0 .iloc [-1 ,0 ]="合计"#line:4809
		OO0OOOO0OOO0O0OO0 ["严重比"]=round ((OO0OOOO0OOO0O0OO0 ["严重伤害数"]+OO0OOOO0OOO0O0OO0 ["死亡数量"])/OO0OOOO0OOO0O0OO0 ["报告数量"]*100 ,2 )#line:4811
		OO0OOOO0OOO0O0OO0 ["Ⅲ类比"]=round ((OO0OOOO0OOO0O0OO0 ["三类数量"])/OO0OOOO0OOO0O0OO0 ["报告数量"]*100 ,2 )#line:4812
		OO0OOOO0OOO0O0OO0 ["超时比"]=round ((OO0OOOO0OOO0O0OO0 ["超时报告数"])/OO0OOOO0OOO0O0OO0 ["报告数量"]*100 ,2 )#line:4813
		OO0OOOO0OOO0O0OO0 ["报表类型"]="dfx_user"#line:4814
		if ini ["模式"]=="药品":#line:4816
			del OO0OOOO0OOO0O0OO0 ["有源"]#line:4818
			del OO0OOOO0OOO0O0OO0 ["无源"]#line:4819
			del OO0OOOO0OOO0O0OO0 ["体外诊断试剂"]#line:4820
			OO0OOOO0OOO0O0OO0 =OO0OOOO0OOO0O0OO0 .rename (columns ={"三类数量":"新的和严重的数量"})#line:4821
			OO0OOOO0OOO0O0OO0 =OO0OOOO0OOO0O0OO0 .rename (columns ={"Ⅲ类比":"新严比"})#line:4822
		return OO0OOOO0OOO0O0OO0 #line:4824
	def df_zhenghao (OO000OO00OOOO0OOO ):#line:4829
		""#line:4830
		O0OO0O000000OO0O0 =OO000OO00OOOO0OOO .df .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:4840
		O0OO00000OOOO0O0O =OO000OO00OOOO0OOO .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda O000OOO0OOO0OOOO0 :STAT_countpx (O000OOO0OOO0OOOO0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOOO00O0OO0O000O :STAT_countpx (OOOOO00O0OO0O000O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O00O0OO00O0OO00OO :STAT_countpx (O00O0OO00O0OO00OO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OOOO0000O00OOO000 :STAT_countpx (OOOO0000O00OOO000 .values ,"严重伤害待评价")),).reset_index ()#line:4849
		O0O0O00OO0OO0OOO0 =pd .merge (O0OO0O000000OO0O0 ,O0OO00000OOOO0O0O ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:4851
		O0O0O00OO0OO0OOO0 =STAT_basic_risk (O0O0O00OO0OO0OOO0 ,"证号计数","严重伤害数","死亡数量","单位个数")#line:4852
		O0O0O00OO0OO0OOO0 =pd .merge (O0O0O00OO0OO0OOO0 ,STAT_recent30 (OO000OO00OOOO0OOO .df ,["注册证编号/曾用注册证编号"]),on =["注册证编号/曾用注册证编号"],how ="left")#line:4854
		O0O0O00OO0OO0OOO0 ["最近30天报告数"]=O0O0O00OO0OO0OOO0 ["最近30天报告数"].fillna (0 ).astype (int )#line:4855
		O0O0O00OO0OO0OOO0 ["最近30天报告严重伤害数"]=O0O0O00OO0OO0OOO0 ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:4856
		O0O0O00OO0OO0OOO0 ["最近30天报告死亡数量"]=O0O0O00OO0OO0OOO0 ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:4857
		O0O0O00OO0OO0OOO0 ["最近30天报告单位个数"]=O0O0O00OO0OO0OOO0 ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:4858
		O0O0O00OO0OO0OOO0 ["最近30天风险评分"]=O0O0O00OO0OO0OOO0 ["最近30天风险评分"].fillna (0 ).astype (int )#line:4859
		O0O0O00OO0OO0OOO0 ["报表类型"]="dfx_zhenghao"#line:4861
		if ini ["模式"]=="药品":#line:4863
			O0O0O00OO0OO0OOO0 =O0O0O00OO0OO0OOO0 .rename (columns ={"待评价数":"新的数量"})#line:4864
			O0O0O00OO0OO0OOO0 =O0O0O00OO0OO0OOO0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4865
		return O0O0O00OO0OO0OOO0 #line:4867
	def df_pihao (OOO0OO00O0OOOO00O ):#line:4869
		""#line:4870
		OOO0O0000OOOO000O =OOO0OO00O0OOOO00O .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:4877
		O0OOO0O000OOO00O0 =OOO0OO00O0OOOO00O .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (严重伤害数 =("伤害",lambda O00OOOOO00000OOOO :STAT_countpx (O00OOOOO00000OOOO .values ,"严重伤害")),死亡数量 =("伤害",lambda O00OOOO0O00OOO0OO :STAT_countpx (O00OOOO0O00OOO0OO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOO0OOO000000O0O0 :STAT_countpx (OOO0OOO000000O0O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O00OO00OOO0OOO00O :STAT_countpx (O00OO00OOO0OOO00O .values ,"严重伤害待评价")),).reset_index ()#line:4886
		O00O0OO000OOO0000 =pd .merge (OOO0O0000OOOO000O ,O0OOO0O000OOO00O0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"],how ="left")#line:4888
		O00O0OO000OOO0000 =STAT_basic_risk (O00O0OO000OOO0000 ,"批号计数","严重伤害数","死亡数量","单位个数")#line:4890
		O00O0OO000OOO0000 =pd .merge (O00O0OO000OOO0000 ,STAT_recent30 (OOO0OO00O0OOOO00O .df ,["注册证编号/曾用注册证编号","产品批号"]),on =["注册证编号/曾用注册证编号","产品批号"],how ="left")#line:4892
		O00O0OO000OOO0000 ["最近30天报告数"]=O00O0OO000OOO0000 ["最近30天报告数"].fillna (0 ).astype (int )#line:4893
		O00O0OO000OOO0000 ["最近30天报告严重伤害数"]=O00O0OO000OOO0000 ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:4894
		O00O0OO000OOO0000 ["最近30天报告死亡数量"]=O00O0OO000OOO0000 ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:4895
		O00O0OO000OOO0000 ["最近30天报告单位个数"]=O00O0OO000OOO0000 ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:4896
		O00O0OO000OOO0000 ["最近30天风险评分"]=O00O0OO000OOO0000 ["最近30天风险评分"].fillna (0 ).astype (int )#line:4897
		O00O0OO000OOO0000 ["报表类型"]="dfx_pihao"#line:4899
		if ini ["模式"]=="药品":#line:4900
			O00O0OO000OOO0000 =O00O0OO000OOO0000 .rename (columns ={"待评价数":"新的数量"})#line:4901
			O00O0OO000OOO0000 =O00O0OO000OOO0000 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4902
		return O00O0OO000OOO0000 #line:4903
	def df_xinghao (OOOO0000O0O0OO0OO ):#line:4905
		""#line:4906
		O0O0OO0O000000OO0 =OOOO0000O0O0OO0OO .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:4913
		O00OO0O0000O000O0 =OOOO0000O0O0OO0OO .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (严重伤害数 =("伤害",lambda O0O00O0O0OOOO0O0O :STAT_countpx (O0O00O0O0OOOO0O0O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO000O00O000O00O0 :STAT_countpx (OO000O00O000O00O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OO00OOO0O00OOO0O0 :STAT_countpx (OO00OOO0O00OOO0O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO0O0000O0OO00O0O :STAT_countpx (OO0O0000O0OO00O0O .values ,"严重伤害待评价")),).reset_index ()#line:4922
		O0O0O000O0OOO0OO0 =pd .merge (O0O0OO0O000000OO0 ,O00OO0O0000O000O0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"],how ="left")#line:4924
		O0O0O000O0OOO0OO0 ["报表类型"]="dfx_xinghao"#line:4927
		if ini ["模式"]=="药品":#line:4928
			O0O0O000O0OOO0OO0 =O0O0O000O0OOO0OO0 .rename (columns ={"待评价数":"新的数量"})#line:4929
			O0O0O000O0OOO0OO0 =O0O0O000O0OOO0OO0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4930
		return O0O0O000O0OOO0OO0 #line:4932
	def df_guige (OO00OOO00OOO00O0O ):#line:4934
		""#line:4935
		O00O0000OO00O000O =OO00OOO00OOO00O0O .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (规格计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),).sort_values (by ="规格计数",ascending =[False ],na_position ="last").reset_index ()#line:4942
		O0OO0OO0OOOOO00O0 =OO00OOO00OOO00O0O .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (严重伤害数 =("伤害",lambda O00OO00OOOO0O00O0 :STAT_countpx (O00OO00OOOO0O00O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00O0O0OO0000000O :STAT_countpx (O00O0O0OO0000000O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OO0O000OOO00O0O00 :STAT_countpx (OO0O000OOO00O0O00 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO0OO0O0OOO000000 :STAT_countpx (OO0OO0O0OOO000000 .values ,"严重伤害待评价")),).reset_index ()#line:4951
		O00O00OOOOOO0O0O0 =pd .merge (O00O0000OO00O000O ,O0OO0OO0OOOOO00O0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"],how ="left")#line:4953
		O00O00OOOOOO0O0O0 ["报表类型"]="dfx_guige"#line:4955
		if ini ["模式"]=="药品":#line:4956
			O00O00OOOOOO0O0O0 =O00O00OOOOOO0O0O0 .rename (columns ={"待评价数":"新的数量"})#line:4957
			O00O00OOOOOO0O0O0 =O00O00OOOOOO0O0O0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4958
		return O00O00OOOOOO0O0O0 #line:4960
	def df_findrisk (OO000OO000OOOO0O0 ,OO00OOO0OOO0000O0 ):#line:4962
		""#line:4963
		if OO00OOO0OOO0000O0 =="产品批号":#line:4964
			return STAT_find_risk (OO000OO000OOOO0O0 .df [(OO000OO000OOOO0O0 .df ["产品类别"]!="有源")],["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",OO00OOO0OOO0000O0 )#line:4965
		else :#line:4966
			return STAT_find_risk (OO000OO000OOOO0O0 .df ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",OO00OOO0OOO0000O0 )#line:4967
	def df_find_all_keword_risk (O00O00000O0O0000O ,O00O00O0O0OO0000O ,*O000O00OO00O0OOO0 ):#line:4969
		""#line:4970
		O0OOO0OO0OOO0O0O0 =O00O00000O0O0000O .df .copy ()#line:4972
		O0OOO0OO0OOO0O0O0 =O0OOO0OO0OOO0O0O0 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:4973
		OOOO0000O0OO00O0O =time .time ()#line:4974
		OO0OOO0O0O00O0O00 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4975
		if "报告类型-新的"in O0OOO0OO0OOO0O0O0 .columns :#line:4976
			O0O00O0OO0OOOO0OO ="药品"#line:4977
		else :#line:4978
			O0O00O0OO0OOOO0OO ="器械"#line:4979
		OOOOOOOO0OOO00OO0 =pd .read_excel (OO0OOO0O0O00O0O00 ,header =0 ,sheet_name =O0O00O0OO0OOOO0OO ).reset_index (drop =True )#line:4980
		try :#line:4983
			if len (O000O00OO00O0OOO0 [0 ])>0 :#line:4984
				OOOOOOOO0OOO00OO0 =OOOOOOOO0OOO00OO0 .loc [OOOOOOOO0OOO00OO0 ["适用范围"].str .contains (O000O00OO00O0OOO0 [0 ],na =False )].copy ().reset_index (drop =True )#line:4985
		except :#line:4986
			pass #line:4987
		O00OOOO0OO000OOOO =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]#line:4989
		O000OO0O000O00O00 =O00OOOO0OO000OOOO [-1 ]#line:4990
		OO000OOO000000O00 =O0OOO0OO0OOO0O0O0 .groupby (O00OOOO0OO000OOOO ).agg (总数量 =(O000OO0O000O00O00 ,"count"),严重伤害数 =("伤害",lambda O00OOO000OO0OOO0O :STAT_countpx (O00OOO000OO0OOO0O .values ,"严重伤害")),死亡数量 =("伤害",lambda O000O0000O00O0O0O :STAT_countpx (O000O0000O00O0O0O .values ,"死亡")),)#line:4995
		O000OO0O000O00O00 =O00OOOO0OO000OOOO [-1 ]#line:4996
		OO0O0O0O00O00OOO0 =O00OOOO0OO000OOOO .copy ()#line:4998
		OO0O0O0O00O00OOO0 .append (O00O00O0O0OO0000O )#line:4999
		OOOOO0O000OO00O00 =O0OOO0OO0OOO0O0O0 .groupby (OO0O0O0O00O00OOO0 ).agg (该元素总数量 =(O000OO0O000O00O00 ,"count"),).reset_index ()#line:5002
		OO000OOO000000O00 =OO000OOO000000O00 [(OO000OOO000000O00 ["总数量"]>=3 )].reset_index ()#line:5005
		OO00OOOO0OO0OO0O0 =[]#line:5006
		O000OOOOOOOOO00O0 =0 #line:5010
		OOOO0O0O00OO00OOO =int (len (OO000OOO000000O00 ))#line:5011
		for O0OO0OOO0OOO0000O ,OOOO000O00O0OO00O ,OOO0O0OOO0O000OO0 ,OOOO0OOO00O0O0O0O in zip (OO000OOO000000O00 ["产品名称"].values ,OO000OOO000000O00 ["产品类别"].values ,OO000OOO000000O00 [O000OO0O000O00O00 ].values ,OO000OOO000000O00 ["总数量"].values ):#line:5012
			O000OOOOOOOOO00O0 +=1 #line:5013
			if (time .time ()-OOOO0000O0OO00O0O )>3 :#line:5015
				root .attributes ("-topmost",True )#line:5016
				PROGRAM_change_schedule (O000OOOOOOOOO00O0 ,OOOO0O0O00OO00OOO )#line:5017
				root .attributes ("-topmost",False )#line:5018
			OOOOO0OO00000000O =O0OOO0OO0OOO0O0O0 [(O0OOO0OO0OOO0O0O0 [O000OO0O000O00O00 ]==OOO0O0OOO0O000OO0 )].copy ()#line:5019
			OOOOOOOO0OOO00OO0 ["SELECT"]=OOOOOOOO0OOO00OO0 .apply (lambda O00O0OO0OO0O0OO0O :(O00O0OO0OO0O0OO0O ["适用范围"]in O0OO0OOO0OOO0000O )or (O00O0OO0OO0O0OO0O ["适用范围"]in OOOO000O00O0OO00O )or (O00O0OO0OO0O0OO0O ["适用范围"]=="通用"),axis =1 )#line:5020
			OOOOOOOOO0O0OO0OO =OOOOOOOO0OOO00OO0 [(OOOOOOOO0OOO00OO0 ["SELECT"]==True )].reset_index ()#line:5021
			if len (OOOOOOOOO0O0OO0OO )>0 :#line:5022
				for O000000O000OOO000 ,OO0OO00O0O0O0O00O ,OOOO0O0O0OO0O00O0 in zip (OOOOOOOOO0O0OO0OO ["值"].values ,OOOOOOOOO0O0OO0OO ["查找位置"].values ,OOOOOOOOO0O0OO0OO ["排除值"].values ):#line:5024
					O0OOO0O00000OO00O =OOOOO0OO00000000O .copy ()#line:5025
					OOOO0O0O0OO00OOO0 =TOOLS_get_list (O000000O000OOO000 )[0 ]#line:5026
					O0OOO0O00000OO00O ["关键字查找列"]=""#line:5028
					for O0O0O0000O0OO00O0 in TOOLS_get_list (OO0OO00O0O0O0O00O ):#line:5029
						O0OOO0O00000OO00O ["关键字查找列"]=O0OOO0O00000OO00O ["关键字查找列"]+O0OOO0O00000OO00O [O0O0O0000O0OO00O0 ].astype ("str")#line:5030
					O0OOO0O00000OO00O .loc [O0OOO0O00000OO00O ["关键字查找列"].str .contains (O000000O000OOO000 ,na =False ),"关键字"]=OOOO0O0O0OO00OOO0 #line:5032
					if str (OOOO0O0O0OO0O00O0 )!="nan":#line:5035
						O0OOO0O00000OO00O =O0OOO0O00000OO00O .loc [~O0OOO0O00000OO00O ["关键字查找列"].str .contains (OOOO0O0O0OO0O00O0 ,na =False )].copy ()#line:5036
					if (len (O0OOO0O00000OO00O ))<1 :#line:5038
						continue #line:5039
					OO0OOO000OOO000O0 =STAT_find_keyword_risk (O0OOO0O00000OO00O ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","关键字"],"关键字",O00O00O0O0OO0000O ,int (OOOO0OOO00O0O0O0O ))#line:5041
					if len (OO0OOO000OOO000O0 )>0 :#line:5042
						OO0OOO000OOO000O0 ["关键字组合"]=O000000O000OOO000 #line:5043
						OO0OOO000OOO000O0 ["排除值"]=OOOO0O0O0OO0O00O0 #line:5044
						OO0OOO000OOO000O0 ["关键字查找列"]=OO0OO00O0O0O0O00O #line:5045
						OO00OOOO0OO0OO0O0 .append (OO0OOO000OOO000O0 )#line:5046
		O0OO0O0OO0OO0OOO0 =pd .concat (OO00OOOO0OO0OO0O0 )#line:5050
		O0OO0O0OO0OO0OOO0 =pd .merge (O0OO0O0OO0OO0OOO0 ,OOOOO0O000OO00O00 ,on =OO0O0O0O00O00OOO0 ,how ="left")#line:5053
		O0OO0O0OO0OO0OOO0 ["关键字数量比例"]=round (O0OO0O0OO0OO0OOO0 ["计数"]/O0OO0O0OO0OO0OOO0 ["该元素总数量"],2 )#line:5054
		O0OO0O0OO0OO0OOO0 =O0OO0O0OO0OO0OOO0 .reset_index (drop =True )#line:5056
		if len (O0OO0O0OO0OO0OOO0 )>0 :#line:5057
			O0OO0O0OO0OO0OOO0 ["风险评分"]=0 #line:5058
			O0OO0O0OO0OO0OOO0 ["报表类型"]="keyword_findrisk"+O00O00O0O0OO0000O #line:5059
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["计数"]>=3 ),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+3 #line:5060
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["计数"]>=(O0OO0O0OO0OO0OOO0 ["数量均值"]+O0OO0O0OO0OO0OOO0 ["数量标准差"])),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+1 #line:5061
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["计数"]>=O0OO0O0OO0OO0OOO0 ["数量CI"]),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+1 #line:5062
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["关键字数量比例"]>0.5 )&(O0OO0O0OO0OO0OOO0 ["计数"]>=3 ),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+1 #line:5063
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["严重伤害数"]>=3 ),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+1 #line:5064
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["单位个数"]>=3 ),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+1 #line:5065
			O0OO0O0OO0OO0OOO0 .loc [(O0OO0O0OO0OO0OOO0 ["死亡数量"]>=1 ),"风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+10 #line:5066
			O0OO0O0OO0OO0OOO0 ["风险评分"]=O0OO0O0OO0OO0OOO0 ["风险评分"]+O0OO0O0OO0OO0OOO0 ["单位个数"]/100 #line:5067
			O0OO0O0OO0OO0OOO0 =O0OO0O0OO0OO0OOO0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5068
		print ("耗时：",(time .time ()-OOOO0000O0OO00O0O ))#line:5074
		return O0OO0O0OO0OO0OOO0 #line:5075
	def df_ror (O0OOOO00OO000000O ,O00O0O0O0O000O000 ,*OOOOO0OO00O000OOO ):#line:5078
		""#line:5079
		O00OOO0O00OO000O0 =O0OOOO00OO000000O .df .copy ()#line:5081
		O0OOOO0O0O0O000O0 =time .time ()#line:5082
		O000OO0O0OOO000O0 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5083
		if "报告类型-新的"in O00OOO0O00OO000O0 .columns :#line:5084
			OO0OO00O0O00000O0 ="药品"#line:5085
		else :#line:5087
			OO0OO00O0O00000O0 ="器械"#line:5088
		O000OO00O00O0O000 =pd .read_excel (O000OO0O0OOO000O0 ,header =0 ,sheet_name =OO0OO00O0O00000O0 ).reset_index (drop =True )#line:5089
		if "css"in O00OOO0O00OO000O0 .columns :#line:5092
			OOOOOOOOOO0O0O00O =O00OOO0O00OO000O0 .copy ()#line:5093
			OOOOOOOOOO0O0O00O ["器械故障表现"]=OOOOOOOOOO0O0O00O ["器械故障表现"].fillna ("未填写")#line:5094
			OOOOOOOOOO0O0O00O ["器械故障表现"]=OOOOOOOOOO0O0O00O ["器械故障表现"].str .replace ("*","",regex =False )#line:5095
			OOOOOO000OO00OOO0 ="use("+str ("器械故障表现")+").file"#line:5096
			O000OOO0O0OOOOO0O =str (Counter (TOOLS_get_list0 (OOOOOO000OO00OOO0 ,OOOOOOOOOO0O0O00O ,1000 ))).replace ("Counter({","{")#line:5097
			O000OOO0O0OOOOO0O =O000OOO0O0OOOOO0O .replace ("})","}")#line:5098
			O000OOO0O0OOOOO0O =ast .literal_eval (O000OOO0O0OOOOO0O )#line:5099
			O000OO00O00O0O000 =pd .DataFrame .from_dict (O000OOO0O0OOOOO0O ,orient ="index",columns =["计数"]).reset_index ()#line:5100
			O000OO00O00O0O000 ["适用范围列"]="产品类别"#line:5101
			O000OO00O00O0O000 ["适用范围"]="无源"#line:5102
			O000OO00O00O0O000 ["查找位置"]="伤害表现"#line:5103
			O000OO00O00O0O000 ["值"]=O000OO00O00O0O000 ["index"]#line:5104
			O000OO00O00O0O000 ["排除值"]="-没有排除值-"#line:5105
			del O000OO00O00O0O000 ["index"]#line:5106
		OOO0O00O00OO00000 =O00O0O0O0O000O000 [-2 ]#line:5109
		OO00OOO0000O00OOO =O00O0O0O0O000O000 [-1 ]#line:5110
		O000OO0O00OOOOOOO =O00O0O0O0O000O000 [:-1 ]#line:5111
		try :#line:5114
			if len (OOOOO0OO00O000OOO [0 ])>0 :#line:5115
				OOO0O00O00OO00000 =O00O0O0O0O000O000 [-3 ]#line:5116
				O000OO00O00O0O000 =O000OO00O00O0O000 .loc [O000OO00O00O0O000 ["适用范围"].str .contains (OOOOO0OO00O000OOO [0 ],na =False )].copy ().reset_index (drop =True )#line:5117
				OO0O0OO0OO0OO0000 =O00OOO0O00OO000O0 .groupby (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (该元素总数量 =(OO00OOO0000O00OOO ,"count"),该元素严重伤害数 =("伤害",lambda O000O0O0OO00OOOO0 :STAT_countpx (O000O0O0OO00OOOO0 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O000000O0O0O00OOO :STAT_countpx (O000000O0O0O00OOO .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5124
				O00OOOOO00O0000O0 =O00OOO0O00OO000O0 .groupby (["产品类别","规整后品类"]).agg (所有元素总数量 =(OOO0O00O00OO00000 ,"count"),所有元素严重伤害数 =("伤害",lambda OOOO000OOOO000OOO :STAT_countpx (OOOO000OOOO000OOO .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O0OOO0OO0O0O00O0O :STAT_countpx (O0OOO0OO0O0O00O0O .values ,"死亡")),)#line:5129
				if len (O00OOOOO00O0000O0 )>1 :#line:5130
					text .insert (END ,"注意，产品类别有两种，产品名称规整疑似不正确！")#line:5131
				OO0O0OO0OO0OO0000 =pd .merge (OO0O0OO0OO0OO0000 ,O00OOOOO00O0000O0 ,on =["产品类别","规整后品类"],how ="left").reset_index ()#line:5133
		except :#line:5135
			text .insert (END ,"\n目前结果为未进行名称规整的结果！\n")#line:5136
			OO0O0OO0OO0OO0000 =O00OOO0O00OO000O0 .groupby (O00O0O0O0O000O000 ).agg (该元素总数量 =(OO00OOO0000O00OOO ,"count"),该元素严重伤害数 =("伤害",lambda O0O0OOOO0OO0OO000 :STAT_countpx (O0O0OOOO0OO0OO000 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O00O00OOOO000O0OO :STAT_countpx (O00O00OOOO000O0OO .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5143
			O00OOOOO00O0000O0 =O00OOO0O00OO000O0 .groupby (O000OO0O00OOOOOOO ).agg (所有元素总数量 =(OOO0O00O00OO00000 ,"count"),所有元素严重伤害数 =("伤害",lambda OOO00OOO000O00O0O :STAT_countpx (OOO00OOO000O00O0O .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O0OOOOOO0O000O000 :STAT_countpx (O0OOOOOO0O000O000 .values ,"死亡")),)#line:5149
			OO0O0OO0OO0OO0000 =pd .merge (OO0O0OO0OO0OO0000 ,O00OOOOO00O0000O0 ,on =O000OO0O00OOOOOOO ,how ="left").reset_index ()#line:5153
		O00OOOOO00O0000O0 =O00OOOOO00O0000O0 [(O00OOOOO00O0000O0 ["所有元素总数量"]>=3 )].reset_index ()#line:5155
		O0O0OOO00000000O0 =[]#line:5156
		if ("产品名称"not in O00OOOOO00O0000O0 .columns )and ("规整后品类"not in O00OOOOO00O0000O0 .columns ):#line:5158
			O00OOOOO00O0000O0 ["产品名称"]=O00OOOOO00O0000O0 ["产品类别"]#line:5159
		if "规整后品类"not in O00OOOOO00O0000O0 .columns :#line:5165
			O00OOOOO00O0000O0 ["规整后品类"]="不适用"#line:5166
		O000O0000OO00O0O0 =0 #line:5169
		O0O0000OOOO0OOOO0 =int (len (O00OOOOO00O0000O0 ))#line:5170
		for O000O0000000O00O0 ,OOO0OO00OO0OOOO0O ,O0O000OOOO000000O ,O0OO0O000OO0OO000 in zip (O00OOOOO00O0000O0 ["规整后品类"],O00OOOOO00O0000O0 ["产品类别"],O00OOOOO00O0000O0 [OOO0O00O00OO00000 ],O00OOOOO00O0000O0 ["所有元素总数量"]):#line:5171
			O000O0000OO00O0O0 +=1 #line:5172
			if (time .time ()-O0OOOO0O0O0O000O0 )>3 :#line:5173
				root .attributes ("-topmost",True )#line:5174
				PROGRAM_change_schedule (O000O0000OO00O0O0 ,O0O0000OOOO0OOOO0 )#line:5175
				root .attributes ("-topmost",False )#line:5176
			OO0O00O00OOO00OOO =O00OOO0O00OO000O0 [(O00OOO0O00OO000O0 [OOO0O00O00OO00000 ]==O0O000OOOO000000O )].copy ()#line:5177
			O000OO00O00O0O000 ["SELECT"]=O000OO00O00O0O000 .apply (lambda OO00OOOO00000O0OO :((O000O0000000O00O0 in OO00OOOO00000O0OO ["适用范围"])or (OO00OOOO00000O0OO ["适用范围"]in OOO0OO00OO0OOOO0O )),axis =1 )#line:5178
			O0O0OO0000000000O =O000OO00O00O0O000 [(O000OO00O00O0O000 ["SELECT"]==True )].reset_index ()#line:5179
			if len (O0O0OO0000000000O )>0 :#line:5180
				for OOO00OOO00O0O00OO ,O0OO0000000O00OO0 ,O0000000000O00OOO in zip (O0O0OO0000000000O ["值"].values ,O0O0OO0000000000O ["查找位置"].values ,O0O0OO0000000000O ["排除值"].values ):#line:5182
					OO0OOO0OOO0O0OOOO =OO0O00O00OOO00OOO .copy ()#line:5183
					OO00O0OO00OOO0O00 =TOOLS_get_list (OOO00OOO00O0O00OO )[0 ]#line:5184
					OO00O00OO0O0OO0O0 ="关键字查找列"#line:5185
					OO0OOO0OOO0O0OOOO [OO00O00OO0O0OO0O0 ]=""#line:5186
					for OOOOO00OO00O0OOOO in TOOLS_get_list (O0OO0000000O00OO0 ):#line:5187
						OO0OOO0OOO0O0OOOO [OO00O00OO0O0OO0O0 ]=OO0OOO0OOO0O0OOOO [OO00O00OO0O0OO0O0 ]+OO0OOO0OOO0O0OOOO [OOOOO00OO00O0OOOO ].astype ("str")#line:5188
					OO0OOO0OOO0O0OOOO .loc [OO0OOO0OOO0O0OOOO [OO00O00OO0O0OO0O0 ].str .contains (OOO00OOO00O0O00OO ,na =False ),"关键字"]=OO00O0OO00OOO0O00 #line:5190
					if str (O0000000000O00OOO )!="nan":#line:5193
						OO0OOO0OOO0O0OOOO =OO0OOO0OOO0O0OOOO .loc [~OO0OOO0OOO0O0OOOO ["关键字查找列"].str .contains (O0000000000O00OOO ,na =False )].copy ()#line:5194
					if (len (OO0OOO0OOO0O0OOOO ))<1 :#line:5197
						continue #line:5198
					for O000O000O0000O000 in zip (OO0OOO0OOO0O0OOOO [OO00OOO0000O00OOO ].drop_duplicates ()):#line:5200
						try :#line:5203
							if O000O000O0000O000 [0 ]!=OOOOO0OO00O000OOO [1 ]:#line:5204
								continue #line:5205
						except :#line:5206
							pass #line:5207
						OOOOO00000O000000 ={"合并列":{OO00O00OO0O0OO0O0 :O0OO0000000O00OO0 },"等于":{OOO0O00O00OO00000 :O0O000OOOO000000O ,OO00OOO0000O00OOO :O000O000O0000O000 [0 ]},"不等于":{},"包含":{OO00O00OO0O0OO0O0 :OOO00OOO00O0O00OO },"不包含":{OO00O00OO0O0OO0O0 :O0000000000O00OOO }}#line:5215
						OOOOO0O0OOO0O0000 =STAT_PPR_ROR_1 (OO00OOO0000O00OOO ,str (O000O000O0000O000 [0 ]),"关键字查找列",OOO00OOO00O0O00OO ,OO0OOO0OOO0O0OOOO )+(OOO00OOO00O0O00OO ,O0000000000O00OOO ,O0OO0000000O00OO0 ,O0O000OOOO000000O ,O000O000O0000O000 [0 ],str (OOOOO00000O000000 ))#line:5217
						if OOOOO0O0OOO0O0000 [1 ]>0 :#line:5219
							O00OO00000O0OOO0O =pd .DataFrame (columns =["特定关键字","出现频次","占比","ROR值","ROR值的95%CI下限","PRR值","PRR值的95%CI下限","卡方值","四分表","关键字组合","排除值","关键字查找列",OOO0O00O00OO00000 ,OO00OOO0000O00OOO ,"报表定位"])#line:5221
							O00OO00000O0OOO0O .loc [0 ]=OOOOO0O0OOO0O0000 #line:5222
							O0O0OOO00000000O0 .append (O00OO00000O0OOO0O )#line:5223
		OO0O0000OO0OOO0O0 =pd .concat (O0O0OOO00000000O0 )#line:5227
		OO0O0000OO0OOO0O0 =pd .merge (OO0O0OO0OO0OO0000 ,OO0O0000OO0OOO0O0 ,on =[OOO0O00O00OO00000 ,OO00OOO0000O00OOO ],how ="right")#line:5231
		OO0O0000OO0OOO0O0 =OO0O0000OO0OOO0O0 .reset_index (drop =True )#line:5232
		del OO0O0000OO0OOO0O0 ["index"]#line:5233
		if len (OO0O0000OO0OOO0O0 )>0 :#line:5234
			OO0O0000OO0OOO0O0 ["风险评分"]=0 #line:5235
			OO0O0000OO0OOO0O0 ["报表类型"]="ROR"#line:5236
			OO0O0000OO0OOO0O0 .loc [(OO0O0000OO0OOO0O0 ["出现频次"]>=3 ),"风险评分"]=OO0O0000OO0OOO0O0 ["风险评分"]+3 #line:5237
			OO0O0000OO0OOO0O0 .loc [(OO0O0000OO0OOO0O0 ["ROR值的95%CI下限"]>1 ),"风险评分"]=OO0O0000OO0OOO0O0 ["风险评分"]+1 #line:5238
			OO0O0000OO0OOO0O0 .loc [(OO0O0000OO0OOO0O0 ["PRR值的95%CI下限"]>1 ),"风险评分"]=OO0O0000OO0OOO0O0 ["风险评分"]+1 #line:5239
			OO0O0000OO0OOO0O0 ["风险评分"]=OO0O0000OO0OOO0O0 ["风险评分"]+OO0O0000OO0OOO0O0 ["该元素单位个数"]/100 #line:5240
			OO0O0000OO0OOO0O0 =OO0O0000OO0OOO0O0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5241
		print ("耗时：",(time .time ()-O0OOOO0O0O0O000O0 ))#line:5247
		return OO0O0000OO0OOO0O0 #line:5248
	def df_chiyouren (OOO0O000O000O0OOO ):#line:5254
		""#line:5255
		OOOO000O00O0OOO0O =OOO0O000O000O0OOO .df .copy ().reset_index (drop =True )#line:5256
		OOOO000O00O0OOO0O ["总报告数"]=data ["报告编码"].copy ()#line:5257
		OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"总待评价数量"]=data ["报告编码"]#line:5258
		OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["伤害"]=="严重伤害"),"严重伤害报告数"]=data ["报告编码"]#line:5259
		OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价")&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害"),"严重伤害待评价数量"]=data ["报告编码"]#line:5260
		OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价")&(OOOO000O00O0OOO0O ["伤害"]=="其他"),"其他待评价数量"]=data ["报告编码"]#line:5261
		OO0O0OOO0O00O000O =OOOO000O00O0OOO0O .groupby (["上市许可持有人名称"]).aggregate ({"总报告数":"nunique","总待评价数量":"nunique","严重伤害报告数":"nunique","严重伤害待评价数量":"nunique","其他待评价数量":"nunique"})#line:5264
		OO0O0OOO0O00O000O ["严重伤害待评价比例"]=round (OO0O0OOO0O00O000O ["严重伤害待评价数量"]/OO0O0OOO0O00O000O ["严重伤害报告数"]*100 ,2 )#line:5269
		OO0O0OOO0O00O000O ["总待评价比例"]=round (OO0O0OOO0O00O000O ["总待评价数量"]/OO0O0OOO0O00O000O ["总报告数"]*100 ,2 )#line:5272
		OO0O0OOO0O00O000O ["总报告数"]=OO0O0OOO0O00O000O ["总报告数"].fillna (0 )#line:5273
		OO0O0OOO0O00O000O ["总待评价比例"]=OO0O0OOO0O00O000O ["总待评价比例"].fillna (0 )#line:5274
		OO0O0OOO0O00O000O ["严重伤害报告数"]=OO0O0OOO0O00O000O ["严重伤害报告数"].fillna (0 )#line:5275
		OO0O0OOO0O00O000O ["严重伤害待评价比例"]=OO0O0OOO0O00O000O ["严重伤害待评价比例"].fillna (0 )#line:5276
		OO0O0OOO0O00O000O ["总报告数"]=OO0O0OOO0O00O000O ["总报告数"].astype (int )#line:5277
		OO0O0OOO0O00O000O ["总待评价比例"]=OO0O0OOO0O00O000O ["总待评价比例"].astype (int )#line:5278
		OO0O0OOO0O00O000O ["严重伤害报告数"]=OO0O0OOO0O00O000O ["严重伤害报告数"].astype (int )#line:5279
		OO0O0OOO0O00O000O ["严重伤害待评价比例"]=OO0O0OOO0O00O000O ["严重伤害待评价比例"].astype (int )#line:5280
		OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .sort_values (by =["总报告数","总待评价比例"],ascending =[False ,False ],na_position ="last")#line:5283
		if "场所名称"in OOOO000O00O0OOO0O .columns :#line:5285
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["审核日期"]=="未填写"),"审核日期"]=3000 -12 -12 #line:5286
			OOOO000O00O0OOO0O ["报告时限"]=pd .Timestamp .today ()-pd .to_datetime (OOOO000O00O0OOO0O ["审核日期"])#line:5287
			OOOO000O00O0OOO0O ["报告时限2"]=45 -(pd .Timestamp .today ()-pd .to_datetime (OOOO000O00O0OOO0O ["审核日期"])).dt .days #line:5288
			OOOO000O00O0OOO0O ["报告时限"]=OOOO000O00O0OOO0O ["报告时限"].dt .days #line:5289
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限"]>45 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（严重）"]=1 #line:5290
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限"]>45 )&(OOOO000O00O0OOO0O ["伤害"]=="其他")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（其他）"]=1 #line:5291
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限"]>30 )&(OOOO000O00O0OOO0O ["伤害"]=="死亡")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"待评价且超出当前日期30天（死亡）"]=1 #line:5292
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]<=1 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["报告时限2"]>0 )&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩1天"]=1 #line:5294
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]>1 )&(OOOO000O00O0OOO0O ["报告时限2"]<=3 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩1-3天"]=1 #line:5295
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]>3 )&(OOOO000O00O0OOO0O ["报告时限2"]<=5 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩3-5天"]=1 #line:5296
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]>5 )&(OOOO000O00O0OOO0O ["报告时限2"]<=10 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩5-10天"]=1 #line:5297
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]>10 )&(OOOO000O00O0OOO0O ["报告时限2"]<=20 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩10-20天"]=1 #line:5298
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]>20 )&(OOOO000O00O0OOO0O ["报告时限2"]<=30 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩20-30天"]=1 #line:5299
			OOOO000O00O0OOO0O .loc [(OOOO000O00O0OOO0O ["报告时限2"]>30 )&(OOOO000O00O0OOO0O ["报告时限2"]<=45 )&(OOOO000O00O0OOO0O ["伤害"]=="严重伤害")&(OOOO000O00O0OOO0O ["持有人报告状态"]=="待评价"),"严重待评价且只剩30-45天"]=1 #line:5300
			del OOOO000O00O0OOO0O ["报告时限2"]#line:5301
			O00O0O000OOO0OOOO =(OOOO000O00O0OOO0O .groupby (["上市许可持有人名称"]).aggregate ({"待评价且超出当前日期45天（严重）":"sum","待评价且超出当前日期45天（其他）":"sum","待评价且超出当前日期30天（死亡）":"sum","严重待评价且只剩1天":"sum","严重待评价且只剩1-3天":"sum","严重待评价且只剩3-5天":"sum","严重待评价且只剩5-10天":"sum","严重待评价且只剩10-20天":"sum","严重待评价且只剩20-30天":"sum","严重待评价且只剩30-45天":"sum"}).reset_index ())#line:5303
			OO0O0OOO0O00O000O =pd .merge (OO0O0OOO0O00O000O ,O00O0O000OOO0OOOO ,on =["上市许可持有人名称"],how ="outer",)#line:5304
			OO0O0OOO0O00O000O ["待评价且超出当前日期45天（严重）"]=OO0O0OOO0O00O000O ["待评价且超出当前日期45天（严重）"].fillna (0 )#line:5305
			OO0O0OOO0O00O000O ["待评价且超出当前日期45天（严重）"]=OO0O0OOO0O00O000O ["待评价且超出当前日期45天（严重）"].astype (int )#line:5306
			OO0O0OOO0O00O000O ["待评价且超出当前日期45天（其他）"]=OO0O0OOO0O00O000O ["待评价且超出当前日期45天（其他）"].fillna (0 )#line:5307
			OO0O0OOO0O00O000O ["待评价且超出当前日期45天（其他）"]=OO0O0OOO0O00O000O ["待评价且超出当前日期45天（其他）"].astype (int )#line:5308
			OO0O0OOO0O00O000O ["待评价且超出当前日期30天（死亡）"]=OO0O0OOO0O00O000O ["待评价且超出当前日期30天（死亡）"].fillna (0 )#line:5309
			OO0O0OOO0O00O000O ["待评价且超出当前日期30天（死亡）"]=OO0O0OOO0O00O000O ["待评价且超出当前日期30天（死亡）"].astype (int )#line:5310
			OO0O0OOO0O00O000O ["严重待评价且只剩1天"]=OO0O0OOO0O00O000O ["严重待评价且只剩1天"].fillna (0 )#line:5312
			OO0O0OOO0O00O000O ["严重待评价且只剩1天"]=OO0O0OOO0O00O000O ["严重待评价且只剩1天"].astype (int )#line:5313
			OO0O0OOO0O00O000O ["严重待评价且只剩1-3天"]=OO0O0OOO0O00O000O ["严重待评价且只剩1-3天"].fillna (0 )#line:5314
			OO0O0OOO0O00O000O ["严重待评价且只剩1-3天"]=OO0O0OOO0O00O000O ["严重待评价且只剩1-3天"].astype (int )#line:5315
			OO0O0OOO0O00O000O ["严重待评价且只剩3-5天"]=OO0O0OOO0O00O000O ["严重待评价且只剩3-5天"].fillna (0 )#line:5316
			OO0O0OOO0O00O000O ["严重待评价且只剩3-5天"]=OO0O0OOO0O00O000O ["严重待评价且只剩3-5天"].astype (int )#line:5317
			OO0O0OOO0O00O000O ["严重待评价且只剩5-10天"]=OO0O0OOO0O00O000O ["严重待评价且只剩5-10天"].fillna (0 )#line:5318
			OO0O0OOO0O00O000O ["严重待评价且只剩5-10天"]=OO0O0OOO0O00O000O ["严重待评价且只剩5-10天"].astype (int )#line:5319
			OO0O0OOO0O00O000O ["严重待评价且只剩10-20天"]=OO0O0OOO0O00O000O ["严重待评价且只剩10-20天"].fillna (0 )#line:5320
			OO0O0OOO0O00O000O ["严重待评价且只剩10-20天"]=OO0O0OOO0O00O000O ["严重待评价且只剩10-20天"].astype (int )#line:5321
			OO0O0OOO0O00O000O ["严重待评价且只剩20-30天"]=OO0O0OOO0O00O000O ["严重待评价且只剩20-30天"].fillna (0 )#line:5322
			OO0O0OOO0O00O000O ["严重待评价且只剩20-30天"]=OO0O0OOO0O00O000O ["严重待评价且只剩20-30天"].astype (int )#line:5323
			OO0O0OOO0O00O000O ["严重待评价且只剩30-45天"]=OO0O0OOO0O00O000O ["严重待评价且只剩30-45天"].fillna (0 )#line:5324
			OO0O0OOO0O00O000O ["严重待评价且只剩30-45天"]=OO0O0OOO0O00O000O ["严重待评价且只剩30-45天"].astype (int )#line:5325
		OO0O0OOO0O00O000O ["总待评价数量"]=OO0O0OOO0O00O000O ["总待评价数量"].fillna (0 )#line:5327
		OO0O0OOO0O00O000O ["总待评价数量"]=OO0O0OOO0O00O000O ["总待评价数量"].astype (int )#line:5328
		OO0O0OOO0O00O000O ["严重伤害待评价数量"]=OO0O0OOO0O00O000O ["严重伤害待评价数量"].fillna (0 )#line:5329
		OO0O0OOO0O00O000O ["严重伤害待评价数量"]=OO0O0OOO0O00O000O ["严重伤害待评价数量"].astype (int )#line:5330
		OO0O0OOO0O00O000O ["其他待评价数量"]=OO0O0OOO0O00O000O ["其他待评价数量"].fillna (0 )#line:5331
		OO0O0OOO0O00O000O ["其他待评价数量"]=OO0O0OOO0O00O000O ["其他待评价数量"].astype (int )#line:5332
		O00O0O0O00O0OO00O =["总报告数","总待评价数量","严重伤害报告数","严重伤害待评价数量","其他待评价数量"]#line:5335
		OO0O0OOO0O00O000O .loc ["合计"]=OO0O0OOO0O00O000O [O00O0O0O00O0OO00O ].apply (lambda O0OO0OO0000OO0O0O :O0OO0OO0000OO0O0O .sum ())#line:5336
		OO0O0OOO0O00O000O [O00O0O0O00O0OO00O ]=OO0O0OOO0O00O000O [O00O0O0O00O0OO00O ].apply (lambda OOOO0000OOOOOOO0O :OOOO0000OOOOOOO0O .astype (int ))#line:5337
		OO0O0OOO0O00O000O .iloc [-1 ,0 ]="合计"#line:5338
		if "场所名称"in OOOO000O00O0OOO0O .columns :#line:5340
			OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .reset_index (drop =True )#line:5341
		else :#line:5342
			OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .reset_index ()#line:5343
		if ini ["模式"]=="药品":#line:5345
			OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .rename (columns ={"总待评价数量":"新的数量"})#line:5346
			OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .rename (columns ={"严重伤害待评价数量":"新的严重的数量"})#line:5347
			OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .rename (columns ={"严重伤害待评价比例":"新的严重的比例"})#line:5348
			OO0O0OOO0O00O000O =OO0O0OOO0O00O000O .rename (columns ={"总待评价比例":"新的比例"})#line:5349
			del OO0O0OOO0O00O000O ["其他待评价数量"]#line:5351
		OO0O0OOO0O00O000O ["报表类型"]="dfx_chiyouren"#line:5352
		return OO0O0OOO0O00O000O #line:5353
	def df_age (OOOOOOO0O0000OO00 ):#line:5355
		""#line:5356
		O0OO0O0O0O000OOOO =OOOOOOO0O0000OO00 .df .copy ()#line:5357
		O0OO0O0O0O000OOOO =O0OO0O0O0O000OOOO .drop_duplicates ("报告编码").copy ()#line:5358
		OOOO00OO0O000O00O =pd .pivot_table (O0OO0O0O0O000OOOO .drop_duplicates ("报告编码"),values =["报告编码"],index ="年龄段",columns ="性别",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"}).reset_index ()#line:5359
		OOOO00OO0O000O00O .columns =OOOO00OO0O000O00O .columns .droplevel (0 )#line:5360
		OOOO00OO0O000O00O ["构成比(%)"]=round (100 *OOOO00OO0O000O00O ["All"]/len (O0OO0O0O0O000OOOO ),2 )#line:5361
		OOOO00OO0O000O00O ["累计构成比(%)"]=OOOO00OO0O000O00O ["构成比(%)"].cumsum ()#line:5362
		OOOO00OO0O000O00O ["报表类型"]="年龄性别表"#line:5363
		return OOOO00OO0O000O00O #line:5364
	def df_psur (O0OOO0O0OO0O00OO0 ,*OO0OO0OO0O0OO0000 ):#line:5366
		""#line:5367
		OO0O000OOOOO00000 =O0OOO0O0OO0O00OO0 .df .copy ()#line:5368
		O0OOOOO0000OOOOOO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5369
		OOOO0OO0OO000OOO0 =len (OO0O000OOOOO00000 .drop_duplicates ("报告编码"))#line:5370
		if "报告类型-新的"in OO0O000OOOOO00000 .columns :#line:5374
			O0OOO00OOO0OOO0OO ="药品"#line:5375
		elif "皮损形态"in OO0O000OOOOO00000 .columns :#line:5376
			O0OOO00OOO0OOO0OO ="化妆品"#line:5377
		else :#line:5378
			O0OOO00OOO0OOO0OO ="器械"#line:5379
		O0OO00OOOO00O0O0O =pd .read_excel (O0OOOOO0000OOOOOO ,header =0 ,sheet_name =O0OOO00OOO0OOO0OO )#line:5382
		OOO00000OOO0OOOO0 =(O0OO00OOOO00O0O0O .loc [O0OO00OOOO00O0O0O ["适用范围"].str .contains ("通用监测关键字|无源|有源",na =False )].copy ().reset_index (drop =True ))#line:5385
		try :#line:5388
			if OO0OO0OO0O0OO0000 [0 ]in ["特定品种","通用无源","通用有源"]:#line:5389
				O0000OO0O0O0OO00O =""#line:5390
				if OO0OO0OO0O0OO0000 [0 ]=="特定品种":#line:5391
					O0000OO0O0O0OO00O =O0OO00OOOO00O0O0O .loc [O0OO00OOOO00O0O0O ["适用范围"].str .contains (OO0OO0OO0O0OO0000 [1 ],na =False )].copy ().reset_index (drop =True )#line:5392
				if OO0OO0OO0O0OO0000 [0 ]=="通用无源":#line:5394
					O0000OO0O0O0OO00O =O0OO00OOOO00O0O0O .loc [O0OO00OOOO00O0O0O ["适用范围"].str .contains ("通用监测关键字|无源",na =False )].copy ().reset_index (drop =True )#line:5395
				if OO0OO0OO0O0OO0000 [0 ]=="通用有源":#line:5396
					O0000OO0O0O0OO00O =O0OO00OOOO00O0O0O .loc [O0OO00OOOO00O0O0O ["适用范围"].str .contains ("通用监测关键字|有源",na =False )].copy ().reset_index (drop =True )#line:5397
				if OO0OO0OO0O0OO0000 [0 ]=="体外诊断试剂":#line:5398
					O0000OO0O0O0OO00O =O0OO00OOOO00O0O0O .loc [O0OO00OOOO00O0O0O ["适用范围"].str .contains ("体外诊断试剂",na =False )].copy ().reset_index (drop =True )#line:5399
				if len (O0000OO0O0O0OO00O )<1 :#line:5400
					showinfo (title ="提示",message ="未找到相应的自定义规则，任务结束。")#line:5401
					return 0 #line:5402
				else :#line:5403
					OOO00000OOO0OOOO0 =O0000OO0O0O0OO00O #line:5404
		except :#line:5406
			pass #line:5407
		try :#line:5411
			if O0OOO00OOO0OOO0OO =="器械"and OO0OO0OO0O0OO0000 [0 ]=="特定品种作为通用关键字":#line:5412
				OOO00000OOO0OOOO0 =OO0OO0OO0O0OO0000 [1 ]#line:5413
		except dddd :#line:5415
			pass #line:5416
		OOOOOOOO0O00OO00O =""#line:5419
		O0O000OOOOOO0OO00 ="-其他关键字-不含："#line:5420
		for O0O00O000OO0000O0 ,OO00O00O000O000O0 in OOO00000OOO0OOOO0 .iterrows ():#line:5421
			O0O000OOOOOO0OO00 =O0O000OOOOOO0OO00 +"|"+str (OO00O00O000O000O0 ["值"])#line:5422
			O00O00OOOO00OO0O0 =OO00O00O000O000O0 #line:5423
		O00O00OOOO00OO0O0 [2 ]="通用监测关键字"#line:5424
		O00O00OOOO00OO0O0 [4 ]=O0O000OOOOOO0OO00 #line:5425
		OOO00000OOO0OOOO0 .loc [len (OOO00000OOO0OOOO0 )]=O00O00OOOO00OO0O0 #line:5426
		OOO00000OOO0OOOO0 =OOO00000OOO0OOOO0 .reset_index (drop =True )#line:5427
		if ini ["模式"]=="器械":#line:5431
			OO0O000OOOOO00000 ["关键字查找列"]=OO0O000OOOOO00000 ["器械故障表现"].astype (str )+OO0O000OOOOO00000 ["伤害表现"].astype (str )+OO0O000OOOOO00000 ["使用过程"].astype (str )+OO0O000OOOOO00000 ["事件原因分析描述"].astype (str )+OO0O000OOOOO00000 ["初步处置情况"].astype (str )#line:5432
		else :#line:5433
			OO0O000OOOOO00000 ["关键字查找列"]=OO0O000OOOOO00000 ["器械故障表现"]#line:5434
		text .insert (END ,"\n药品查找列默认为不良反应表现,药品规则默认为通用规则。\n器械默认查找列为器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况，器械默认规则为无源通用规则+有源通用规则。\n")#line:5435
		O0OOOO00OOO00OO0O =[]#line:5437
		for O0O00O000OO0000O0 ,OO00O00O000O000O0 in OOO00000OOO0OOOO0 .iterrows ():#line:5439
			O0O0O00O0OOOO0OOO =OO00O00O000O000O0 ["值"]#line:5440
			if "-其他关键字-"not in O0O0O00O0OOOO0OOO :#line:5442
				OOO0OOOOOOO0OOO0O =OO0O000OOOOO00000 .loc [OO0O000OOOOO00000 ["关键字查找列"].str .contains (O0O0O00O0OOOO0OOO ,na =False )].copy ()#line:5445
				if str (OO00O00O000O000O0 ["排除值"])!="nan":#line:5446
					OOO0OOOOOOO0OOO0O =OOO0OOOOOOO0OOO0O .loc [~OOO0OOOOOOO0OOO0O ["关键字查找列"].str .contains (str (OO00O00O000O000O0 ["排除值"]),na =False )].copy ()#line:5448
			else :#line:5450
				OOO0OOOOOOO0OOO0O =OO0O000OOOOO00000 .loc [~OO0O000OOOOO00000 ["关键字查找列"].str .contains (O0O0O00O0OOOO0OOO ,na =False )].copy ()#line:5453
			OOO0OOOOOOO0OOO0O ["关键字标记"]=str (O0O0O00O0OOOO0OOO )#line:5454
			OOO0OOOOOOO0OOO0O ["关键字计数"]=1 #line:5455
			if len (OOO0OOOOOOO0OOO0O )>0 :#line:5461
				try :#line:5462
					O00OO0O0OOOO0O00O =pd .pivot_table (OOO0OOOOOOO0OOO0O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害PSUR",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5472
				except :#line:5474
					O00OO0O0OOOO0O00O =pd .pivot_table (OOO0OOOOOOO0OOO0O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5484
				O00OO0O0OOOO0O00O =O00OO0O0OOOO0O00O [:-1 ]#line:5485
				O00OO0O0OOOO0O00O .columns =O00OO0O0OOOO0O00O .columns .droplevel (0 )#line:5486
				O00OO0O0OOOO0O00O =O00OO0O0OOOO0O00O .reset_index ()#line:5487
				if len (O00OO0O0OOOO0O00O )>0 :#line:5490
					O0OO00OO00O00O0O0 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",OOO0OOOOOOO0OOO0O ,1000 ))).replace ("Counter({","{")#line:5491
					O0OO00OO00O00O0O0 =O0OO00OO00O00O0O0 .replace ("})","}")#line:5492
					O0OO00OO00O00O0O0 =ast .literal_eval (O0OO00OO00O00O0O0 )#line:5493
					O00OO0O0OOOO0O00O .loc [0 ,"事件分类"]=str (TOOLS_get_list (O00OO0O0OOOO0O00O .loc [0 ,"关键字标记"])[0 ])#line:5495
					O00OO0O0OOOO0O00O .loc [0 ,"不良事件名称1"]=str ({O000O0O00OOO0O00O :OO000OOOO00O00O00 for O000O0O00OOO0O00O ,OO000OOOO00O00O00 in O0OO00OO00O00O0O0 .items ()if STAT_judge_x (str (O000O0O00OOO0O00O ),TOOLS_get_list (O0O0O00O0OOOO0OOO ))==1 })#line:5496
					O00OO0O0OOOO0O00O .loc [0 ,"不良事件名称2"]=str ({O0000OO0O00O000OO :OOO0OOOO00000OOO0 for O0000OO0O00O000OO ,OOO0OOOO00000OOO0 in O0OO00OO00O00O0O0 .items ()if STAT_judge_x (str (O0000OO0O00O000OO ),TOOLS_get_list (O0O0O00O0OOOO0OOO ))!=1 })#line:5497
					if ini ["模式"]=="药品":#line:5508
						for O00OO0O0O0OOO0OOO in ["SOC","HLGT","HLT","PT"]:#line:5509
							O00OO0O0OOOO0O00O [O00OO0O0O0OOO0OOO ]=OO00O00O000O000O0 [O00OO0O0O0OOO0OOO ]#line:5510
					if ini ["模式"]=="器械":#line:5511
						for O00OO0O0O0OOO0OOO in ["国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]:#line:5512
							O00OO0O0OOOO0O00O [O00OO0O0O0OOO0OOO ]=OO00O00O000O000O0 [O00OO0O0O0OOO0OOO ]#line:5513
					O0OOOO00OOO00OO0O .append (O00OO0O0OOOO0O00O )#line:5516
		OOOOOOOO0O00OO00O =pd .concat (O0OOOO00OOO00OO0O )#line:5517
		OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:5522
		OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .reset_index ()#line:5523
		OOOOOOOO0O00OO00O ["All占比"]=round (OOOOOOOO0O00OO00O ["All"]/OOOO0OO0OO000OOO0 *100 ,2 )#line:5525
		OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:5526
		try :#line:5527
			OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .rename (columns ={"其他":"一般"})#line:5528
		except :#line:5529
			pass #line:5530
		try :#line:5532
			OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .rename (columns ={" 一般":"一般"})#line:5533
		except :#line:5534
			pass #line:5535
		try :#line:5536
			OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .rename (columns ={" 严重":"严重"})#line:5537
		except :#line:5538
			pass #line:5539
		try :#line:5540
			OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .rename (columns ={"严重伤害":"严重"})#line:5541
		except :#line:5542
			pass #line:5543
		try :#line:5544
			OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O .rename (columns ={"死亡":"死亡(仅支持器械)"})#line:5545
		except :#line:5546
			pass #line:5547
		for OOOO0O00O00O0O0OO in ["一般","新的一般","严重","新的严重"]:#line:5550
			if OOOO0O00O00O0O0OO not in OOOOOOOO0O00OO00O .columns :#line:5551
				OOOOOOOO0O00OO00O [OOOO0O00O00O0O0OO ]=0 #line:5552
		try :#line:5554
			OOOOOOOO0O00OO00O ["严重比"]=round ((OOOOOOOO0O00OO00O ["严重"].fillna (0 )+OOOOOOOO0O00OO00O ["死亡(仅支持器械)"].fillna (0 ))/OOOOOOOO0O00OO00O ["总数量"]*100 ,2 )#line:5555
		except :#line:5556
			OOOOOOOO0O00OO00O ["严重比"]=round ((OOOOOOOO0O00OO00O ["严重"].fillna (0 )+OOOOOOOO0O00OO00O ["新的严重"].fillna (0 ))/OOOOOOOO0O00OO00O ["总数量"]*100 ,2 )#line:5557
		OOOOOOOO0O00OO00O ["构成比"]=round ((OOOOOOOO0O00OO00O ["总数量"].fillna (0 ))/OOOOOOOO0O00OO00O ["总数量"].sum ()*100 ,2 )#line:5559
		if ini ["模式"]=="药品":#line:5561
			try :#line:5562
				OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","死亡(仅支持器械)","SOC","HLGT","HLT","PT"]]#line:5563
			except :#line:5564
				OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","SOC","HLGT","HLT","PT"]]#line:5565
		elif ini ["模式"]=="器械":#line:5566
			try :#line:5567
				OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","死亡(仅支持器械)","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5568
			except :#line:5569
				OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5570
		else :#line:5572
			try :#line:5573
				OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","死亡(仅支持器械)"]]#line:5574
			except :#line:5575
				OOOOOOOO0O00OO00O =OOOOOOOO0O00OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2"]]#line:5576
		for O00OO00O0000OO0OO ,OO000O0OO0000O000 in OOO00000OOO0OOOO0 .iterrows ():#line:5578
			OOOOOOOO0O00OO00O .loc [(OOOOOOOO0O00OO00O ["关键字标记"].astype (str )==str (OO000O0OO0000O000 ["值"])),"排除值"]=OO000O0OO0000O000 ["排除值"]#line:5579
		OOOOOOOO0O00OO00O ["排除值"]=OOOOOOOO0O00OO00O ["排除值"].fillna ("没有排除值")#line:5581
		for O0000OOO0OOO00OO0 in ["一般","新的一般","严重","新的严重","总数量","总数量占比","严重比"]:#line:5585
			OOOOOOOO0O00OO00O [O0000OOO0OOO00OO0 ]=OOOOOOOO0O00OO00O [O0000OOO0OOO00OO0 ].fillna (0 )#line:5586
		for O0000OOO0OOO00OO0 in ["一般","新的一般","严重","新的严重","总数量"]:#line:5588
			OOOOOOOO0O00OO00O [O0000OOO0OOO00OO0 ]=OOOOOOOO0O00OO00O [O0000OOO0OOO00OO0 ].astype (int )#line:5589
		OOOOOOOO0O00OO00O ["RPN"]="未定义"#line:5592
		OOOOOOOO0O00OO00O ["故障原因"]="未定义"#line:5593
		OOOOOOOO0O00OO00O ["可造成的伤害"]="未定义"#line:5594
		OOOOOOOO0O00OO00O ["应采取的措施"]="未定义"#line:5595
		OOOOOOOO0O00OO00O ["发生率"]="未定义"#line:5596
		OOOOOOOO0O00OO00O ["报表类型"]="PSUR"#line:5598
		return OOOOOOOO0O00OO00O #line:5599
def A0000_Main ():#line:5609
	print ("")#line:5610
if __name__ =='__main__':#line:5612
	root =Tk .Tk ()#line:5615
	root .title (title_all )#line:5616
	try :#line:5617
		root .iconphoto (True ,PhotoImage (file =peizhidir +"0（范例）ico.png"))#line:5618
	except :#line:5619
		pass #line:5620
	sw_root =root .winfo_screenwidth ()#line:5621
	sh_root =root .winfo_screenheight ()#line:5623
	ww_root =700 #line:5625
	wh_root =620 #line:5626
	x_root =(sw_root -ww_root )/2 #line:5628
	y_root =(sh_root -wh_root )/2 #line:5629
	root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:5630
	framecanvas =Frame (root )#line:5635
	canvas =Canvas (framecanvas ,width =680 ,height =30 )#line:5636
	canvas .pack ()#line:5637
	x =StringVar ()#line:5638
	out_rec =canvas .create_rectangle (5 ,5 ,680 ,25 ,outline ="silver",width =1 )#line:5639
	fill_rec =canvas .create_rectangle (5 ,5 ,5 ,25 ,outline ="",width =0 ,fill ="silver")#line:5640
	canvas .create_text (350 ,15 ,text ="总执行进度")#line:5641
	framecanvas .pack ()#line:5642
	try :#line:5649
		frame0 =ttk .Frame (root ,width =90 ,height =20 )#line:5650
		frame0 .pack (side =LEFT )#line:5651
		B_open_files1 =Button (frame0 ,text ="导入数据",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =TOOLS_allfileopen ,)#line:5662
		B_open_files1 .pack ()#line:5663
		B_open_files3 =Button (frame0 ,text ="数据查看",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ori ,0 ,ori ),)#line:5678
		B_open_files3 .pack ()#line:5679
	except KEY :#line:5682
		pass #line:5683
	text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF")#line:5687
	text .pack (padx =5 ,pady =5 )#line:5688
	text .insert (END ,"\n 本程序适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。如您有改进建议，请点击实用工具-意见反馈。\n")#line:5691
	text .insert (END ,"\n\n")#line:5692
	setting_cfg =read_setting_cfg ()#line:5695
	generate_random_file ()#line:5696
	setting_cfg =open_setting_cfg ()#line:5697
	if setting_cfg ["settingdir"]==0 :#line:5698
		showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:5699
		filepathu =filedialog .askdirectory ()#line:5700
		path =get_directory_path (filepathu )#line:5701
		update_setting_cfg ("settingdir",path )#line:5702
	setting_cfg =open_setting_cfg ()#line:5703
	random_number =int (setting_cfg ["sidori"])#line:5704
	input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:5705
	day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:5706
	sid =random_number *2 +183576 #line:5707
	if input_number ==sid and day_end =="未过期":#line:5708
		usergroup ="用户组=1"#line:5709
		text .insert (END ,usergroup +"   有效期至：")#line:5710
		text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:5711
	else :#line:5712
		text .insert (END ,usergroup )#line:5713
	text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:5714
	peizhidir =str (setting_cfg ["settingdir"])+csdir .split ("pinggutools")[0 ][-1 ]#line:5715
	roox =Toplevel ()#line:5719
	tMain =threading .Thread (target =PROGRAM_showWelcome )#line:5720
	tMain .start ()#line:5721
	t1 =threading .Thread (target =PROGRAM_closeWelcome )#line:5722
	t1 .start ()#line:5723
	root .lift ()#line:5725
	root .attributes ("-topmost",True )#line:5726
	root .attributes ("-topmost",False )#line:5727
	root .mainloop ()#line:5731
	print ("done.")#line:5732
