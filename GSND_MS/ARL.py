#!/usr/bin/env python
# coding: utf-8

# todo
# 1. 전처리 - nan 제거
# 2. K-means
    # 2.1. K-means 코드 수정
    # 2.2. K-means cluster 입력칸 수정 (spinbox 등)
# 3. 시간 걸리는 function (wordcloud...) 실행 전 샘플로 소요시간 계산 후 alert 띄워주기
# 10. SNA, 감정분석 등 기능 추가
# 96. 파일선택창에서 취소 선택시 에러 잡기
# 97. 메뉴-버전 OTA Update() 작성
# 98. workdir 삭제
# 99. '내용'.len < 15 처리 (Prepro)

# idea
# 1. 전처리과정에서 작성일자,일자,일시,작성일,등록일,date 등을 작성일자로 변경해주는 기능 추가

# Errorlog
# 1. 전처리 후 EDA 내 버튼 클릭시 화면 작아짐

import datetime, time, sys, os, re, urllib.request, bs4, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askopenfilenames
import tkinter.ttk as ttk
#pip install soynlp
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from soynlp.utils import DoublespaceLineCorpus
from konlpy.tag import Okt
from collections import Counter
#pip install wordcloud
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from git import Repo
import shutil

 # 환경 설정
plt.rc('font', family='Malgun Gothic') # matplotlib 한글 처리

title = '경상남도 민원분석 시스템'
flag_login = 0
username = ''
workdir = ''
resultdir = ''
filename = ''
filename_dateflag = ''
data_origin = pd.DataFrame()
rbt_value = 0
flag_prepro = 0

mainwindow = tk.Tk()
mainwindow.title(title)
mainwindow.geometry('800x600')
mainwindow.resizable(False, False)

 # 민원파일 로드 + 경로 설정
def Load_File():
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        else:
            global filename, workdir, resultdir, filename_dateflag, flag_prepro
            flag_prepro = 0
            file = askopenfilenames(initialdir = 'c:/', filetypes = (('csv File', '*.csv'), ('All Files', '*.*')), title = '민원파일 선택')
            filename = file[0].split('/')[-1]
            workdir = file[0].split('/')[:-1] # 작업경로(민원파일 경로) 설정
            workdir = '/'.join(workdir) + '/'
            #os.chdir(workdir)
            os.makedirs('result', exist_ok = True)
            resultdir = os.getcwd() + '/result/'
            now = datetime.datetime.now()
            filename_dateflag = '[' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '] '
            
            mainwindow.title(title + '(' + username + ') ' + '- 작업중 (' + filename + ')')
            
            Load_Pandas()
            
            # preview (https://youtu.be/PgLjwl6Br0k)
            data_preview_frame = tk.LabelFrame(mainwindow, text = '데이터 미리보기 ({}행, {}열)'.format(data_origin.shape[0], data_origin.shape[1]))
            data_preview_frame.place(height = 300, width = 800, y = 5)
            
            data_preview = ttk.Treeview(data_preview_frame)
            data_preview.place(relheight = 1, relwidth = 1)
            
            scrolly = tk.Scrollbar(data_preview_frame, orient = 'vertical', command = data_preview.yview)
            scrollx = tk.Scrollbar(data_preview_frame, orient = 'horizontal', command = data_preview.xview)
            data_preview.configure(xscrollcommand = scrollx.set, yscrollcommand = scrolly.set)
            scrollx.pack(side = 'bottom', fill = 'x')
            scrolly.pack(side = 'right', fill = 'y')
            
            data_preview['column'] = list(data_origin.columns)
            data_preview['show'] = 'headings'
            for column in data_preview['columns']:
                data_preview.heading(column, text = column)
                
            data_origin['rows'] = data_origin.to_numpy().tolist()
            for row in data_origin['rows']:
                data_preview.insert('', 'end', values = row)        
            
            # analysis frame
            frame_analysis = ttk.Notebook(mainwindow, width = 787, height = 230)
            frame_analysis.place(x = 5, y = 320)
           
            frame_prepro = tk.Frame(mainwindow)
            frame_EDA = tk.Frame(mainwindow)
            frame_word = tk.Frame(mainwindow)
            frame_kmeans = tk.Frame(mainwindow)
            
            frame_analysis.add(frame_prepro, text = '데이터 전처리')
            frame_analysis.add(frame_EDA, text = 'EDA')
            frame_analysis.add(frame_word, text = '워드클라우드')
            frame_analysis.add(frame_kmeans, text = 'K-means')
            #prepro
            bt_test_prepro = tk.Button(frame_prepro, text = '데이터 전처리', overrelief = 'solid', command = lambda:Prepro())
            bt_test_prepro.place(x = 10, y = 10)
            #EDA
            bt_yearly = tk.Button(frame_EDA, text = '연간 민원건수 분석', overrelief = 'solid', command = lambda:Makegraph_Yearly(rbt_value))
            bt_yearly.place(x = 10, y = 10)
            bt_monthly = tk.Button(frame_EDA, text = '월간 민원건수 분석', overrelief = 'solid', command = lambda:Makegraph_Monthly(rbt_value))
            bt_monthly.place(x = 10, y = 40)
            bt_yearmonth = tk.Button(frame_EDA, text = '연간+월간 민원건수 분석', overrelief = 'solid', command = lambda:Makegraph_Yearmonth(rbt_value))
            bt_yearmonth.place(x = 10, y = 70)
            bt_daily = tk.Button(frame_EDA, text = '요일별 민원건수 분석', overrelief = 'solid', command = lambda:Makegraph_Daily(rbt_value))
            bt_daily.place(x = 10, y = 100)
            
            rbt_frame = tk.LabelFrame(frame_EDA, text = '그래프 형식')
            rbt_frame.place(height = 70, width = 120, x = 180, y = 5)
            #data_preview_frame = tk.LabelFrame(mainwindow, text = '데이터 미리보기 ({}행, {}열)'.format(data_origin.shape[0], data_origin.shape[1]))
            #data_preview_frame.place(height = 300, width = 800, y = 5)
            rbt_var = tk.IntVar()
            rbt_graphtype_0 = tk.Radiobutton(rbt_frame, text = '막대그래프', variable = rbt_var, value = 0, command = lambda:(Rbt_Check(rbt_var.get())))
            rbt_graphtype_0.select()
            rbt_graphtype_0.place(x = 5, y = 0)
            rbt_graphtype_1 = tk.Radiobutton(rbt_frame, text = '꺾은선그래프', variable = rbt_var, value = 1, command = lambda:(Rbt_Check(rbt_var.get())))
            rbt_graphtype_1.deselect()
            rbt_graphtype_1.place(x = 5, y = 20)
            #word
            target_word = tk.StringVar()
            combobox_column = ttk.Combobox(frame_word, text = '대상 열 선택', height = 15, textvariable = target_word)
            combobox_column['values'] = list(data_origin.columns)[:-1]
            combobox_column.place(x = 10, y = 10)
            
            bt_wordcloud_soynlp = tk.Button(frame_word, text = '워드클라우드(Soynlp)', overrelief = 'solid', command = lambda:Makegraph_Wordcloud_Soynlp(target_word.get()))
            bt_wordcloud_soynlp.place(x = 10, y = 40)
            bt_wordcloud_konlpy = tk.Button(frame_word, text = '워드클라우드(Konlpy)', overrelief = 'solid', command = lambda:Makegraph_Wordcloud_Konlpy(target_word.get()))
            bt_wordcloud_konlpy.place(x = 10, y = 70)
            
            #K-means
            target_Kmeans = tk.StringVar()
            cluster = tk.StringVar()
            
            combobox_column = ttk.Combobox(frame_kmeans, text = '대상 열 선택', height = 15, textvariable = target_Kmeans)
            combobox_column['values'] = list(data_origin.columns)[:-1]
            combobox_column.place(x = 10, y = 10)
            
            combobox_column = ttk.Combobox(frame_kmeans, text = '클러스터 수', height = 15, textvariable = cluster)
            combobox_column.place(x = 200, y = 10)
            
            bt_kmeans = tk.Button(frame_kmeans, text = 'K-means', overrelief = 'solid', command = lambda:Kmeans(target_Kmeans.get(), cluster.get()))
            bt_kmeans.place(x = 10, y = 40)
            
            
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n알 수 없는 오류가 발생했습니다.')
        
def sha256(acc):
    try:
        return hashlib.sha256(acc.encode()).hexdigest()
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n로그인 중 오류가 발생했습니다.')

def Login(pleasebequiet = 1):
    server_login = 'https://github.com/SoongFish/GSND_MS/blob/master/LDB.acc'
    list_acc = list()
    
    global flag_login, username
    if flag_login == 0 or flag_login == None or flag_login == '':
        flag_login = simpledialog.askstring('인증', '사용자 코드를 입력하세요.', parent = mainwindow)
        
        if flag_login == 0 or flag_login == None or flag_login == '' or len(flag_login) > 20:
            flag_login = 0
            return
        else:
            try:
                mainwindow.title(title + ' @ 로그인 서버 연결중...')
                db_acc = urllib.request.urlopen(server_login)
            except Exception as e:
                Log(desc = e)
                messagebox.showerror('계정', str(e) + '\n로그인 서버에 연결할 수 없습니다.')
                mainwindow.title(title)
                flag_login = 0
                return
            
            db_acc_obj = bs4.BeautifulSoup(db_acc, 'html.parser')
            
            sep = db_acc_obj.findAll('td', {'class' : 'blob-code'})
            mainwindow.title(title + ' @ 로그인중...')
            
            for index in range(len(sep)):
                list_acc.append(sep[index].text)
            
            if sha256(flag_login) in list_acc:
                username = flag_login
                mainwindow.title(title + '(' + username + ') ')
            else:
                messagebox.showwarning('계정', '사용자 정보가 존재하지 않습니다!') 
                flag_login = 0
                mainwindow.title(title)
                return
    else:
        if pleasebequiet != 1:
            messagebox.showwarning('계정', '이미 로그인 되어있습니다!') 
            return
    
def Logout():
    try:
        global flag_login, flag_prepro, username, rbt_value
        if flag_login == 0 or flag_login == None or flag_login == '':
            messagebox.showwarning('계정', '먼저 로그인하세요!')
        else:
            messagebox.showinfo('계정', '로그아웃이 완료되었습니다.')
            for widget in mainwindow.winfo_children(): # 화면 클리어
                widget.destroy()
            Make_Menu()
            flag_login = flag_prepro = rbt_value = 0
            username = ''
            mainwindow.title(title)
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n로그아웃 중 오류가 발생했습니다.')

def Quit():
	mainwindow.quit()
    
def Rbt_Check(rbt_val):
    global rbt_value
    rbt_value = rbt_val
    
 # 작업 데이터 로드
def Load_Pandas():
    global data_origin
    data_origin = pd.read_csv(workdir + filename, encoding = 'cp949') # 도지사에게바란다
    #data_origin = pd.read_csv(workdir + filename, encoding = 'utf-8') # 국민신문고

 # 데이터 전처리
def Prepro():
    try:
        global data_origin, flag_prepro
        
        #data_origin = data_origin[data_origin['내용'].str.len() > 15] # '내용' 15글자 이상만 추출 (왜안되지?)
        #data_origin = data_origin.drop([data_origin['내용'].str.len() > 15], axis = 0) # '내용' 15글자 이상만 추출 (왜안되지??)
        
        data_origin['작성일시'] = pd.to_datetime(data_origin['작성일시']) # 작성일시 날짜화
        data_origin = data_origin.sort_values(by = ['작성일시'], ascending = True) # 작성일시 기준으로 정렬
        
        flag_prepro = 1
        
        messagebox.showinfo('작업', '데이터 전처리가 완료되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('경고', str(e) + ' 열을 찾을 수 없습니다.')
        #mainwindow.title(title)
        #flag_login = 0
        #return
 # 연도별 민원 빈도 그래프 작성 (코드 개선필요)
def Makegraph_Yearly(graphtype): #graphtype - 0:bar / 1:plot
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        elif flag_prepro == 0:
            messagebox.showwarning('주의', '데이터 전처리 후 실행해주세요.')
            return
        else:
            (cnt2018, cnt2019, cnt2020) = (0, 0, 0)
            for i in range(len(data_origin['작성일시'])):
               if data_origin.loc[i, '작성일시'].year == 2018: cnt2018 += 1
               elif data_origin.loc[i, '작성일시'].year == 2019: cnt2019 += 1
               else: cnt2020 += 1
                       
            plt.clf() # plt figure 초기화
            plt.style.use('ggplot')
            plt.title('연도별 민원 빈도')
            if graphtype:
                plt.plot(['2018', '2019', '2020'], [cnt2018, cnt2019, cnt2020])
                plt.savefig(resultdir + filename_dateflag + '연도별 민원 빈도_꺾은선.png', dpi = 200)
            else:
                plt.bar(['2018', '2019', '2020'], [cnt2018, cnt2019, cnt2020])
                plt.savefig(resultdir + filename_dateflag + '연도별 민원 빈도_막대.png', dpi = 200)
            #plt.show() 
        messagebox.showinfo('작업', '연간 민원건수 분석이 완료되었습니다.\n\nresult폴더에 결과물이 저장되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n작업 중 오류가 발생했습니다.')
        
 # 월별 민원 빈도 그래프 작성 (코드 개선필요)
def Makegraph_Monthly(graphtype): #graphtype - 0:bar / 1:plot
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        elif flag_prepro == 0:
            messagebox.showwarning('주의', '데이터 전처리 후 실행해주세요.')
            return
        else:
            (cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9, cnt10, cnt11, cnt12) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            for i in range(len(data_origin['작성일시'])):
                if data_origin.loc[i, '작성일시'].month == 1: cnt1 += 1
                elif data_origin.loc[i, '작성일시'].month == 2: cnt2 += 1
                elif data_origin.loc[i, '작성일시'].month == 3: cnt3 += 1
                elif data_origin.loc[i, '작성일시'].month == 4: cnt4 += 1
                elif data_origin.loc[i, '작성일시'].month == 5: cnt5 += 1
                elif data_origin.loc[i, '작성일시'].month == 6: cnt6 += 1
                elif data_origin.loc[i, '작성일시'].month == 7: cnt7 += 1
                elif data_origin.loc[i, '작성일시'].month == 8: cnt8 += 1
                elif data_origin.loc[i, '작성일시'].month == 9: cnt9 += 1
                elif data_origin.loc[i, '작성일시'].month == 10: cnt10 += 1
                elif data_origin.loc[i, '작성일시'].month == 11: cnt11 += 1
                else: cnt12 += 1
                       
            plt.clf()
            plt.style.use('ggplot')
            plt.title('월별 민원 빈도')
            if graphtype:
                plt.plot(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], [cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9, cnt10, cnt11, cnt12])
                plt.savefig(resultdir + filename_dateflag + '월별 민원 빈도_꺾은선.png', dpi = 200)
            else:
                plt.bar(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], [cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9, cnt10, cnt11, cnt12])
                plt.savefig(resultdir + filename_dateflag + '월별 민원 빈도_막대.png', dpi = 200)
            #plt.show()
        messagebox.showinfo('작업', '월간 민원건수 분석이 완료되었습니다.\n\nresult폴더에 결과물이 저장되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n작업 중 오류가 발생했습니다.')
        
 # 요일별 민원 빈도 그래프 작성 (코드 개선필요)
def Makegraph_Daily(graphtype): #graphtype - 0:bar / 1:plot
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        elif flag_prepro == 0:
            messagebox.showwarning('주의', '데이터 전처리 후 실행해주세요.')
            return
        else:
            (cntd1, cntd2, cntd3, cntd4, cntd5, cntd6, cntd7) = (0, 0, 0, 0, 0, 0, 0)
            for i in range(len(data_origin['작성일시'])):
                if data_origin.loc[i, '작성일시'].weekday() == 0: cntd1 += 1
                elif data_origin.loc[i, '작성일시'].weekday() == 1: cntd2 += 1
                elif data_origin.loc[i, '작성일시'].weekday() == 2: cntd3 += 1
                elif data_origin.loc[i, '작성일시'].weekday() == 3: cntd4 += 1
                elif data_origin.loc[i, '작성일시'].weekday() == 4: cntd5 += 1
                elif data_origin.loc[i, '작성일시'].weekday() == 5: cntd6 += 1
                else: cntd7 += 1
               
            plt.clf()
            plt.style.use('ggplot')
            plt.title('요일별 민원 빈도')
            if graphtype:
                plt.plot(['월', '화', '수', '목', '금', '토', '일'], [cntd1, cntd2, cntd3, cntd4, cntd5, cntd6, cntd7])
                plt.savefig(resultdir + filename_dateflag + '요일별 민원 빈도_꺾은선.png', dpi = 200)
            else:
                plt.bar(['월', '화', '수', '목', '금', '토', '일'], [cntd1, cntd2, cntd3, cntd4, cntd5, cntd6, cntd7])
                plt.savefig(resultdir + filename_dateflag + '요일별 민원 빈도_막대.png', dpi = 200)
            #plt.show()
        messagebox.showinfo('작업', '요일별 민원건수 분석이 완료되었습니다.\n\nresult폴더에 결과물이 저장되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n작업 중 오류가 발생했습니다.')

 # 연도+월별 민원 빈도 그래프 작성 (코드 개선필요)
def Makegraph_Yearmonth(graphtype): #graphtype - 0:bar / 1:plot
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        elif flag_prepro == 0:
            messagebox.showwarning('주의', '데이터 전처리 후 실행해주세요.')
            return
        else:
            cnt = 0
            tmp_yymm = ''
            list_yymm = list()
            list_yymm_cnt = list()

            for i in data_origin['작성일시']:
               if tmp_yymm != str(i.year) + '-' + str(i.month): 
                   if cnt > 1: list_yymm_cnt.append(cnt)
                   cnt = 1
                   tmp_yymm = str(i.year) + '-' + str(i.month)
                   list_yymm.append(tmp_yymm)
               else:
                   cnt += 1
            list_yymm_cnt.append(cnt)

            plt.clf()
            plt.style.use('ggplot')
            plt.figure(figsize = (len(list_yymm)*0.6, 10)) # grid size 가변화
            plt.title('연도+월별 민원 빈도')
            if graphtype:
                plt.plot(list_yymm, list_yymm_cnt)
                plt.xticks(rotation = 45, ha = 'right') # x축 라벨 회전
                plt.savefig(resultdir + filename_dateflag + '연도+월별 민원 빈도_꺾은선.png', dpi = 200)
            else:
                plt.bar(list_yymm, list_yymm_cnt)
                plt.xticks(rotation = 45, ha = 'right') # x축 라벨 회전
                plt.savefig(resultdir + filename_dateflag + '연도+월별 민원 빈도_막대.png', dpi = 200)
            #plt.show() 
        messagebox.showinfo('작업', '연간+월간 민원건수 분석이 완료되었습니다.\n\nresult폴더에 결과물이 저장되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n작업 중 오류가 발생했습니다.')

 # 처리상황 파이차트


 # 답변소요기간 계산
# todo
# 기준을 작성일시로 할지 수정일시로 할지?
# 답변소요기간 표시형식 바꾸기
# NaT 처리
def Reply():
    data_origin['답변일자'] = pd.to_datetime(data_origin['답변일자']) # 답변일자 날짜화

    for i in range(len(data_origin)):
        data_origin.loc[i, '답변소요기간'] = data_origin.loc[i, '답변일자'] - data_origin.loc[i, '작성일시']


 # 처리부서별 최소, 최대, 평균 답변소요기간 (어렵네)
#data_origin.groupby('담당부서').apply(lambda x : data_origin['답변소요기간'])


 # 워드클라우드 (https://blog.naver.com/jjuna91/222108733922)
 # todo
 # stopwords 목록 추가(공무원, 행정, 민원 ...) / 삭제(경남, 김해 ...) 
 # 워드클라우드 모양 https://blog.naver.com/nilsine11202/221834254905
def Makegraph_Wordcloud_Soynlp(target):
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        #elif flag_prepro == 0:
            #messagebox.showwarning('주의', '데이터 전처리 후 실행해주세요.')
            #return
        else:
            data_wordcloud_soynlp = pd.DataFrame(data_origin[target], columns = ['contents'])
            data_wordcloud_soynlp['contents'] = data_origin[target].apply(lambda x: re.sub('[^가-힣]',' ', x))

            word_extractor = WordExtractor(min_frequency = 10, # 가변화하기 (ex. data_origin.len() 비례)
                             min_cohesion_forward = 0.05,
                             min_right_branching_entropy = 0.0)
            word_extractor.train(data_wordcloud_soynlp['contents'].values)
            words = word_extractor.extract()

            cohesion_score = {word:score.cohesion_forward for word, score in words.items()}
            tokenizer = LTokenizer(scores = cohesion_score)
            data_wordcloud_soynlp['tokenizer'] = data_wordcloud_soynlp['contents'].apply(lambda x: tokenizer.tokenize(x, remove_r = True))

            words = list()
            for i in data_wordcloud_soynlp['tokenizer'].values:
                for j in i:
                    words.append(j)

            count_soynlp = Counter(words)
            words_dict_soynlp = dict(count_soynlp.most_common())

            csv_stopwords = pd.read_csv(workdir + 'stopwords.csv', encoding = 'cp949', skiprows = 0) # with open 변경
            stopwords = list()
            for i in csv_stopwords.values:
                for j in i:
                    stopwords.append(j)

            for word in stopwords:
                words_dict_soynlp.pop(word, None)

            wordcloud = WordCloud(font_path = workdir + 'NanumGothic.ttf', width = 500, height = 500, background_color = 'white').generate_from_frequencies(words_dict_soynlp)

            plt.clf()
            plt.figure(figsize = (20, 20))
            plt.imshow(wordcloud)
            plt.axis('off')
            #plt.show()
            plt.savefig(resultdir + filename_dateflag + target + ' - wordcloud_soynlp.png', dpi = 100)
            
        messagebox.showinfo('작업', '워드클라우드(Soynlp) 생성이 완료되었습니다.\n\nresult폴더에 결과물이 저장되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('경고', str(e) + ' 열을 찾을 수 없습니다.')
        
def Makegraph_Wordcloud_Konlpy(target):
    try:
        if flag_login == 0 or flag_login == None or flag_login == '':
            Login()
        #elif flag_prepro == 0:
            #messagebox.showwarning('주의', '데이터 전처리 후 실행해주세요.')
            #return
        else:
            data_wordcloud_konlpy = pd.DataFrame(data_origin[target], columns = ['contents'])
            data_wordcloud_konlpy['contents'] = data_origin[target].apply(lambda x: re.sub('[^가-힣]',' ', x))
            
            morphs = list()
            filtered = list()
            
            for data in data_wordcloud_konlpy['contents']: # 형태소 분석
                morphs.append(Okt().pos(data))
            
            for element in morphs: # 형태소 필터
                for word, tag in element:
                    if tag in ['Noun']: # 사용자 선택 추가 (CheckButton = 명사/형용사/부사/동사... -> bit operation)
                        filtered.append(word)
            
            count_konlpy = Counter(filtered)
            words_dict_konlpy = dict(count_konlpy.most_common())
            
            csv_stopwords = pd.read_csv(workdir + 'stopwords.csv', encoding = 'cp949', skiprows = 0) # with open 변경
            stopwords = list()
            for i in csv_stopwords.values:
                for j in i:
                    stopwords.append(j)

            for word in stopwords:
                words_dict_konlpy.pop(word, None)
            
            wordcloud = WordCloud(font_path = workdir + 'NanumGothic.ttf', width = 500, height = 500, background_color = 'white').generate_from_frequencies(words_dict_konlpy)
            
            plt.clf()
            plt.figure(figsize = (20, 20))
            plt.imshow(wordcloud)
            plt.axis('off')
            #plt.show()
            plt.savefig(resultdir + filename_dateflag + target + ' - wordcloud_konlpy.png', dpi = 100)
            
        messagebox.showinfo('작업', '워드클라우드(Konlpy) 생성이 완료되었습니다.\n\nresult폴더에 결과물이 저장되었습니다.')
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('경고', str(e) + ' 열을 찾을 수 없습니다.')

 #K-means
def Kmeans(target, cluster):
    vectorizer = TfidfVectorizer()
    result = vectorizer.fit_transform(data_origin[target])

    data_points = data_origin[target].values
    Kmeans = KMeans(n_clusters = int(cluster), init = 'k-means++', max_iter = 100).fit(result)

    data_origin['cluster_result'] = 0
    for i in range(len(data_origin[target])):
        data_origin.iloc[i, -1] = Kmeans.labels_[i]

    #data_origin['s1_labels'] = pd.DataFrame.from_records(Kmeans.labels_)
    data_origin[[target, 'cluster_result']].to_csv('result/Kmeans.csv', encoding = 'cp949', index = False)

 # Menubar
def Make_Menu():
    menubar = tk.Menu(mainwindow)

    menu_1 = tk.Menu(menubar, tearoff = 0)
    menu_1.add_command(label = '민원파일 열기', command = Load_File)
    menu_1.add_separator()
    menu_1.add_command(label = '종료', command = Quit)
    menubar.add_cascade(label = '파일', menu = menu_1)

    menu_2 = tk.Menu(menubar, tearoff = 0)
    menu_2.add_command(label = '로그인', command = lambda:Login(pleasebequiet = 0))
    menu_2.add_separator()
    menu_2.add_command(label = '로그아웃', command = Logout)
    menubar.add_cascade(label = '계정', menu = menu_2)

    menu_3 = tk.Menu(menubar, tearoff = 0)
    menu_3.add_command(label = 'About', command = About)
    menu_3.add_command(label = '버전/업데이트', command = Version)
    menubar.add_cascade(label = '정보', menu = menu_3)

    mainwindow.config(menu = menubar)
    
def About():
    messagebox.showinfo('정보', '민원분석 시스템\n\n경상남도청 정보빅데이터담당관실 인턴, 2020')
    
def Version():
    version = '1.1.0.1'
    server_version = 'https://github.com/SoongFish/GSND_MS/blob/master/version'
    
    try:
        mainwindow.title(title + ' @ 업데이트 서버 연결중...')
        db_version = urllib.request.urlopen(server_version)
    except Exception as e:
        Log(desc = e)
        messagebox.showerror('오류', str(e) + '\n업데이트 서버에 연결할 수 없습니다.')
        mainwindow.title(title)
        return
        
    db_version_obj = bs4.BeautifulSoup(db_version, 'html.parser')
    sep = db_version_obj.find('td', {'class' : 'blob-code'})
    
    mainwindow.title(title + ' @ 업데이트 확인중...')
    if sep.text == version:
        messagebox.showinfo('버전', '민원분석 시스템 ' + version + '\n\n최신버전입니다.')
    else:
        update = messagebox.askquestion('버전', '민원분석 시스템 ' + version + '\n\n업데이트가 존재합니다. (' + sep.text + ')\n업데이트 하시겠습니까?')
        if update == 'yes':
            Update()
            mainwindow.title(title)
        else:
            mainwindow.title(title)
            return
            
def Update():
    wherenewcode = 'https://github.com/SoongFish/GSND_MS.git'
    if os.path.isdir(os.getcwd() + '/updates'):
        shutil.rmtree(os.getcwd() + '/updates')
    else:
        os.makedirs('/updates', mode = 777, exist_ok = True)
        Repo.clone_from(wherenewcode, os.getcwd() + '/updates')
    
    os.system("dir")
    
def Log(desc = ''):
    try:
        os.makedirs('log', mode = 777, exist_ok = True)
        with open('log/' + 'log.log', 'a') as logdata:
            logfuncname = sys._getframe().f_back.f_code.co_name
            logtime = time.strftime('%c', time.localtime(time.time()))
            logdata.write('[{}] {} ##funcname: {} ##workdir: {} ##filename: {} ##desc: {}\n'.format(username, logtime, logfuncname, workdir, filename, desc))
    except Exception as e:
        messagebox.showerror('오류', str(e) + '\n로그 시스템에 오류가 발생했습니다.')

 # main
mainwindow.tk.call('wm', 'iconphoto', mainwindow._w, tk.PhotoImage(file = 'icon.png'))
Make_Menu()
mainwindow.mainloop()