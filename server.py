#! /usr/bin/python
# -- coding: utf-8 --
from random import *
import socket
import sys
import pymongo
from pymongo import MongoClient

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["po"]


HOST = ''  # 모든 ip 받음
PORT = 8888 # 포트 설정

#1. open Socket
s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ('Socket created')

#2. bind to a address and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind Failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
    sys.exit()

print ('Socket bind complete')

#3. Listen for incoming connections
s.listen(10)
print ('Socket now listening')

try:
    #keep talking with the client
    while 1:
        #4. Accept connection
        conn, addr = s.accept()
        print ('Connected with ' + addr[0] + ':' + str(addr[1]))
        
        #5. Read/Send
        # data라는 상태 메세지를 먼저 받는다
        data = conn.recv(1024).decode() # login, join, battle, save 중 하나를 client_server에서 받아옴
        if not data:
                break
        # data의 메세지가 login일 경우
        if data == "login":
            conn.send("ok") # client_server로 ok 값 보냄
            id = conn.recv(1024).decode()  # client_server에서 받은 id 값을 id 변수에 저장
            pw = conn.recv(1024).decode()  # client_server에서 받은 pw 값을 pw 변수에 저장
            # mycol = db collection person으로 설정
            mycol = mydb["person"]
            mydoc = mycol.find()
            # sendcol = db collection userinfo으로 설정
            sendcol = mydb["userinfo"]
            senddoc = sendcol.find({})
            polist = [] # 리스트 type

            # 로그인 한 아이디의 db의 정보를 변수들에 저장
            for i in senddoc:
                ITEM = i["ITEM"]
                pokemonNAME = i["pokemonNAME"]
                MAX_HP = i["MAX_HP"]
                MONEY = i["MONEY"]
                HP = i["HP"]
                user_id = i["id"]
                EXPERIENCE = i["EXPERIENCE"]
                ATK = i["ATK"]
                if user_id == id:
                    break
            # 문자열 형태로 바꿈
            ITEM = str(ITEM)
            pokemonNAME = str(pokemonNAME)
            MAX_HP = str(MAX_HP)
            MONEY = str(MONEY)
            HP = str(HP)
            user_id = str(user_id)
            EXPERIENCE = str(EXPERIENCE)
            ATK = str(ATK)
            print(pokemonNAME, MAX_HP, MONEY, ATK, HP, EXPERIENCE, ITEM, user_id)
            # 회원의 포켓몬 정보들을 한 번에 보내기 위해서 abc에 문자열 형태로 저장 - (를 쓴 이유 : split 조건을 만들기 위해서
            abc = pokemonNAME+"("+HP+"("+MAX_HP+"("+ATK+"("+EXPERIENCE+"("+ITEM+"("+MONEY+"("+user_id
            # 로그인 - 
            for i in mydoc:
                DB_id = i["id"] # 로그인한 id 값을 DB_id에 저장
                DB_pw = i["pw"] # 로그인한 pw 값을 DB_pw에 저장
                # 만약 내가 입력한 아이디가 db값에 있다면
                if mycol.find_one({'id' : id}):
                    # 만약 내가 입력한 비밀번호가 db값에 있다면
                    if mycol.find_one({'pw' : pw}):
                        print("로그인 성공") # 로그인 성공 출력
                        conn.send("ok") # client_server에 ok 값 전송
                        conn.send(abc) # 포켓몬 정보 값 전송
                        break
                else:            
                    conn.send("no") # 로그인 실패로 no 값 전송
        # data의 메세지가 join일 경우        
        if data == "join":
            conn.send("ok")
            id = conn.recv(1024).decode() # client_server에서 받은 id 값을 id 변수에 저장
            pw = conn.recv(1024).decode() # client_server에서 받은 pw 값을 pw 변수에 저장
            # print(id)
            # print(pw)
            # mycol = db collection person으로 설정
            mycol = mydb["person"]
            mydoc = mycol.find()
            # sendcol = db collection userinfo으로 설정
            sendcol = mydb["userinfo"]
            senddoc = sendcol.find()
            # client_server에서 받은 id 값이 person이라는 collection에 없는 값이라면
            if not(mycol.find_one({'id' : id})):
                mylist = [
                    {"id": id, "pw":pw}
                ]
                sendlist =[
                    {"id":id, "pokemonNAME":"pikachu", "HP":70, "ATK":20, "ITEM":5, "MONEY":1000, "EXPERIENCE":0, "MAX_HP":70}
                ]
                mycol.insert_many(mylist) # client_server에서 받은 값을 mylist에 저장후 person이라는 db에 insert
                sendcol.insert_many(sendlist) # client_server에서 받은 값을 sendlist에 저장후 userinfo라는 db에 insert
                conn.send("ok") # ok 값 전송
                print("회원가입 성공")
            else:            
                conn.send("no") # no 값 전송
                print("회원가입 실패")
        # data의 메세지가 battle일 경우
        # 야생 포켓몬 배틀
        if data == "battle":
            conn.send("ok")
            print('battle')
            mycol = mydb["pokemonList"] # mycol에 po라는 db에서 pokemonList라는 collection 지정
            mydoc = mycol.find() # mydoc = 
            i = randint(5,28) # i = 5 ~ 27번 사이의 랜덤 숫자를 저장
            a = mydoc[i] # a = pokemonList에서 랜덤 숫자 list방 지정
            list1 = []
            for key in a:
                list1.append(a[key]) # list1이라는 리스트에 a의 속성값을 차례대로 지정
            name = list1[2].encode("utf-8")
            print(name)
            HP = str(list1[0]) # float형 값을 string 값으로 바꿔서 HP라는 변수에 저장
            ATK = str(list1[3]) # float형 값을 string 값으로 바꿔서 ATK라는 변수에 저장
            print(name, HP, ATK)
            conn.send(name) # name값 client_server로 보내기
            conn.recv(1024).decode()
            conn.send(HP) # HP값 client_server로 보내기
            conn.recv(1024).decode()
            conn.send(ATK) # ATK값 client_server로 보내기
        # data의 메세지가 save일 경우
        if data == "save":
            print("save")
            # mycol = db collection userinfo으로 설정
            mycol = mydb["userinfo"]
            mydoc = mycol.find()
            conn.send("ok") # client_server로 ok 값을 보냄
            sum_info = conn.recv(1024).decode() # client_server에서 받은 sum_info 값을 sum_info 변수에 저장
            sum_info = sum_info.encode() # sum_info를 encode함
            sum_info = sum_info.split("(") # sum_info를 리스트 type으로 (단위로 잘라서 저장
            
            # user_id로 받은 id를 userinfo라는 db에서 찾아서 그 id의 속성 값들을 client_server에서 받은 값들로 update함
            mycol.update({ "id": sum_info[7] }, { "$set": {"pokemonNAME":sum_info[0],"ATK":sum_info[1], "HP":sum_info[2], "MONEY":sum_info[3], "EXPERIENCE":sum_info[4], "ITEM":sum_info[5], "MAX_HP":sum_info[6]}})

        conn.close()
    s.close()
except:
    print('Error occurred')
    s.close()