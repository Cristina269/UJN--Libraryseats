# -*- coding:utf-8 -*-
from hashlib import md5
import requests
import time
import datetime
import json



name=''

seatid=''    #座位号
yh=''     #账号
mm=''          #密码


print(name)




start_time_mon = int(16) * 60
# 周一预约的时间
end_time_mon = int(22) * 60  #
# 周一预约的时间
start_time_normal = int(9) * 60
# 正常预约的时间
end_time_normal = int(22) * 60  #
# 正常预约的时间



ttt=0  #(休息时间)


def get_bind_nocode(yh, mm):
    s = requests.session()
    url = 'https://seat.ujn.edu.cn/libseat-ibeacon/doLogin'
    headers = {
        'Host': 'seat.ujn.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Content-Length': '31',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://seat.ujn.edu.cn',
        'Referer': 'http://seat.ujn.edu.cn/remote/static/bindHandler',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    }
    data2 = {'account':yh,'password':mm,'linkSign':'currentBook','type':'currentBook'}
    session = requests.Session()
    maxTryNum = 20
    for tries in range(maxTryNum):
        try:
            data2 = {'account': yh, 'password': mm, 'linkSign': 'currentBook', 'type': 'currentBook'}
            session = requests.Session()
            maxTryNum = 20
            session = requests.Session()
            s = session.post(url, headers=headers, data=data2)
            cookie_jar = s.cookies
            cookie = requests.utils.dict_from_cookiejar(cookie_jar)
            cookie=str(cookie)
            cookie=cookie.replace("'", '')
            cookie = cookie.replace("{", '')
            cookie = cookie.replace("}", '')
            cookie = cookie.replace(":", '=')
            #print(cookie)
            return cookie
        except:
            if tries < (maxTryNum - 1):
                continue



def book(seatid, cookie):
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    date = tomorrow
    day = datetime.datetime.now()
    day = day.weekday()
    if day == 0:
        start = start_time_mon
        end = end_time_mon
    else:
        start = start_time_normal
        end = end_time_normal
    url = 'http://seat.ujn.edu.cn/libseat-ibeacon/saveBook?seatId=' + str(seatid) + '&date=' + str(
        date) + '&start=' + str(start) + '&end=' + str(end) + '&type=1'
    headers = {
        'Host': 'seat.ujn.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Cookie': cookie

    }
    maxTryNum = 20
    for tries in range(maxTryNum):
        try:
            r = requests.get(url=url, headers=headers)
            #print(r.text)
            succ = r.text.find('success')
            fail = r.text.find('已有1个')
            wrong = r.text.find('系统可预约时间')
            yiyou = r.text.find('预约失败，请尽快选择其他时段或座位')
            shichang = r.text.find('非法时长')
            if succ != -1:                                                      #成功返回 1  已经被抢返回2  不在时间内3   预约时长错误4    已经有座位5           
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '成功', '', riqi, shijian)
                status = 1
                return status
            elif fail != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '已经有座位', '', riqi, shijian)
                status = 5
                return status
            elif wrong != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '不在预约时间内', '', riqi, shijian)
                status = 3
                return status
            elif yiyou != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '已经被抢', '', riqi, shijian)
                status = 2
                return status
            elif shichang != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '时长不对', '', riqi, shijian)
                status = 4
                return status
            else:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                status = 3
                print(name, '失效', '', riqi, shijian)
                return status
        except:
            if tries < (maxTryNum - 1):
                time.sleep(2)            #删掉
                continue



def get_cookie():
    stat = 0
    while stat == 0:
        cookie = get_bind_nocode(yh, mm)  # 获取account
        num=1
        if num == 1:
            #print(cookie)
            return cookie
            stat = 1
        else:
            stat = 0
    # return cookie


def differ():  # 时间差
    h = int(time.strftime("%H", time.localtime())) * 3600
    m = int(time.strftime("%M", time.localtime())) * 60
    s = int(time.strftime("%S", time.localtime()))
    differ = 25198 - h - m - s
    if differ < 0:
        differ = 0
    else:
        differ = differ
    return differ
    # return differ


def get_history(cookie):  # 获取当天预约状态 return 当天所有status和当天开始时间
    cancel = 'CANCEL'
    ing = 'CHECK_IN'
    ok = 'COMPLETE'
    miss = 'MISS'
    stop = 'STOP'
    xiayige = 'RESERVE'
    url = 'http://seat.ujn.edu.cn/libseat-ibeacon/getUserBookHistory'
    headers = {
        'Host': 'seat.ujn.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Cookie': cookie
    }
    r = requests.get(url=url, headers=headers)
    result = json.loads(r.text)
    items = result['params']['history']  #
    len1 = int(len(items))
    date = int(time.strftime('%d', time.localtime(time.time())))
    for i in range(len1):
        id = items[i]['id']
        date2 = items[i]['date']
        num = date2.find('-', 5)
        ri = int(date2[num + 1:])
        # print(ri,date)
        if ri == date:
            status = items[i]['stat']  # 座位状态
            status = status.strip()
            b_time = items[i]['begin']  # 座位开始时间
            # print(status==xiayige)
            if status == ing or status == cancel or status == ok or status == miss or status == stop:
                b_time = 0
                return b_time
                # 返回一个数据表示没有待签到
            elif status == xiayige:
                # print(id,b_time)
                return id, b_time
    # return id, b_time


def compare(b_time):  # 比较当前时间和预约开始的时间
    if b_time != 0:
        h1 = int(time.strftime("%H", time.localtime())) * 3600
        m1 = int(time.strftime("%M", time.localtime())) * 60
        s1 = int(time.strftime("%S", time.localtime()))
        h, m = b_time.strip().split(':')
        miao = int(h) * 3600 + int(m) * 60
        #print(miao)
        timecha = int(miao - h1 - m1 - s1)
        if timecha < 120:  # 距离预约时间小于120s
            return 0
        else:
            wait_time = int(miao) - h - m
            return wait_time

    # return 1 0


def cancel(cookie, id):
    url = 'http://seat.ujn.edu.cn/libseat-ibeacon/cancleBook?bookId=' + str(id)
    headers = {
        'Host': 'seat.ujn.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Cookie': cookie
    }
    r = requests.get(url=url, headers=headers)
    print(r.text)


def test_cookie(cookie):  # return一个正常的cookie
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    url = 'http://seat.ujn.edu.cn/libseat-ibeacon/loadStartTime?seatId=22141&date=' + str(tomorrow)
    #print(tomorrow, url)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Cookie': cookie,
        'DNT': '1',
        'Host': 'seat.ujn.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://seat.ujn.edu.cn/libseat-ibeacon/seatdetail?linkSign=activitySeat&roomId=40&date=2021-03-11&buildId=2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }
    r = requests.get(url=url, headers=headers)
    #print(r.text)
    #print(len(r.text))
    if len(r.text) < 2000:
        return cookie
    else:
        cookie = get_bind_nocode(yh, mm)
        return cookie
    # 报废



def start_book(cookie,  seatid):
    shijian = time.strftime("%H:%M:%S", time.localtime())
    print('\r', name, '现在：', shijian, end='    ')
    status = book(seatid, cookie)
    return status


def book_aftercheck(seatid, cookie):
    date = datetime.date.today()
    start = (int(time.strftime("%H", time.localtime())) + 1)*60
    #print(start)
    end = int(22) * 60
    url = 'http://seat.ujn.edu.cn/libseat-ibeacon/saveBook?seatId=' + str(seatid) + '&date=' + str(
        date) + '&start=' + str(start) + '&end=' + str(end) + '&type=1'
    headers = {
        'Host': 'seat.ujn.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Cookie': cookie
    }
    maxTryNum = 20
    for tries in range(maxTryNum):
        try:
            r = requests.get(url=url, headers=headers)
            succ = r.text.find('success')
            fail = r.text.find('已有1个')
            wrong = r.text.find('系统可预约时间')
            yiyou = r.text.find('预约失败，请尽快选择其他时段或座位')
            if succ != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '成功', '', riqi, shijian)
                status = 1
                return status
            elif fail != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '已经有座位', '', riqi, shijian)
                status = 0
                return status
            elif wrong != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '不在预约时间内', '', riqi, shijian)
                status = 0
                return status
            elif yiyou != -1:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                print(name, '已经被抢', '', riqi, shijian)
                status = 0
                return status
            else:
                shijian = time.strftime("%H:%M:%S", time.localtime())
                riqi = time.strftime("%Y-%m-%d", time.localtime())
                status = 0
                print(name, '失效', '', riqi, shijian)
                return status
        except:
            if tries < (maxTryNum - 1):
                continue


def main_cancel():
    #new 检测是否失约并自动取消用 ，好像一直没用
    while 1:
        shijian = int(time.strftime("%H%M", time.localtime()))
        time.sleep(0.1)
        while shijian != 730:
            cookie = get_cookie()
            try:
                id, b_time = get_history(cookie)
                status = compare(b_time)
                if status == 0:
                    #status==0表明距离失约不到两分钟
                    print('正在取消当前预约')
                    cancel(cookie, id)
                    # 开始新的预约
                    day = datetime.datetime.now()
                    day = day.weekday()
                    # 排除周二
                    if day == 1:
                        pass
                    else:
                        time.sleep(20)
                        print('正在预约一个小时后的座位')
                        # 开始新的预约
                        #cookie = get_cookie()
                        book_aftercheck(seatid, cookie)
                else:
                    time.sleep(status-70)
                    #返回数值说明大于两分钟
            except:
                # 表示没有待签到
                id = get_history(cookie)
                print('正常')
                time.sleep(3000)


'''def only():                                                  #第一次0    成功返回 1  已经被抢返回2  不在时间内3   预约时长错误4    已经有座位5
    shijian = time.strftime("%H%M%S", time.localtime())
    status = 0
    counter=0
    t = 0
    time.sleep(0.1)
    shijian = time.strftime("%H%M", time.localtime())
    while t!=30:
        if status == 0 and counter==0:
            print('第一次预约')
            cookie = get_cookie()
            #time.sleep(0.1)
            timecha2 = differ()
            time.sleep(timecha2)       #等到659
            status = start_book(cookie, seatid)
            shijian = time.strftime("%H%M", time.localtime())
            counter=counter+1
            t=t+1
        elif status==0 and counter!=0:      #莫名其妙失败 or 未到时间
            print('第',t,'次')
            status = start_book(cookie, seatid)
            shijian = time.strftime("%H%M", time.localtime())
            time.sleep(ttt)
            t=t+1
        elif status==2:         #座位被抢
            t==30
        elif status==3:         #cookie失效
            print('第',t,'次')
            cookie=test_cookie(cookie)
            print('cookie失效')
            time.sleep(0)
            status = start_book(cookie,  seatid)
            t=t+1'''


def only():
    shijian = time.strftime("%H%M%S", time.localtime())
    while int(shijian) != 65959:
        print('-----------------------------------')
        cookie = get_cookie()
        status=book(seatid, cookie)
        if status==2 or status==1 or status==5:
            break
        else:
            pass

def main():
    #早上预约用
    while 1:
        shijian = time.strftime("%H%M", time.localtime())
        status = 0
        t = 0
        time.sleep(0.1)
        while int(shijian) == 659:
            # 等号改成   !=   实验是否能用
            time.sleep(0.1)
            shijian = time.strftime("%H%M", time.localtime())
            while status == 0 and t != 2:
                cookie = get_cookie()
                #print(cookie)
                time.sleep(0.1)
                timecha2 = differ()
                status = start_book(cookie, timecha2, seatid)
                shijian = time.strftime("%H%M", time.localtime())
                t = t + 1

def main_crazy():
    while 1:
        shijian = time.strftime("%H%M%S", time.localtime())
        status = 0
        counter=0
        t = 0
        time.sleep(0.1)
        while int(shijian) != 659:
            # 等号改成   !=   实验是否能用
            shijian = time.strftime("%H%M", time.localtime())
            while 1:
                if status == 0 and counter==0:
                    print('第一次预约')
                    cookie = get_cookie()
                    #time.sleep(0.1)
                    timecha2 = differ()
                    time.sleep(timecha2)       #等到659
                    status = start_book(cookie, seatid)
                    shijian = time.strftime("%H%M", time.localtime())
                    counter=counter+1
                elif status==0 and counter!=0:      #莫名其妙失败 or 未到时间
                    status = start_book(cookie, seatid)
                    shijian = time.strftime("%H%M", time.localtime())
                    time.sleep(ttt)
                elif status==2:         #座位被抢
                    time.sleep(0.1)
                    break
                elif status==3:         #cookie失效
                    cookie=test_cookie(cookie)
                    print('cookie失效')
                    time.sleep(0)
                    status = start_book(cookie,  seatid)
#main()

while 1:
    time.sleep(0.1)
    only()
