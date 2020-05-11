# -*- coding: utf-8 -*-
import datetime
import os
import time

import js2py
import requests
import execjs
import xlsxwriter
from gne import GeneralNewsExtractor
from pyppeteer import launch
import asyncio
import words_sort
import searchkey

class Toutiao:

    def __init__(self):
        self.url = 'https://www.toutiao.com/i'

    def get_pamas(self,max_time):
        with open('zzascp.js','r',encoding='utf8')as f:
            tt = f.read()
        et = execjs.compile(tt)
        as_cp = et.call('get_as_cp')
        _as = as_cp['as']
        cp = as_cp['cp']
        as_cp_url = f"https://www.toutiao.com/toutiao/api/pc/feed/?max_behot_time={max_time}2&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as={_as}&cp={cp}"
        _signature = requests.post('http://localhost:8000/post', data={'href': as_cp_url}).json()
        return as_cp_url,_signature

    def get_news(self,as_cp_url,_signature):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': "gr_user_id=ac6d5a38-05d0-450d-87a5-00c7c0d6bf1d; grwng_uid=ca65d884-05dd-4e7d-9d3d-d949a328bf4b; tt_webid=6783960477643900429; login_flag=64326e7e1dff2e8c0c23d67970d9649a; tt_webid=6783960477643900429; WEATHER_CITY=%E5%8C%97%E4%BA%AC; csrftoken=c426941a14d252cb771ae5401ce4f785; ttcid=b0dfc95097714e708788812b03d8f1b851; s_v_web_id=verify_k7lfbl1e_PVjXhPWz_q5ZG_4N94_8lSL_mxTjVc2kawRL; __tasessionId=v3sjz33zl1583833181436; SLARDAR_WEB_ID=4cd341cf-317d-4962-815d-09b2349e0c6e; tt_scid=65MJfOZ2rLLXjcRX.nxh781Ek0oPkGrNDKf8v.zP3EdtoOVF.eOvxo2-.1ZpYaFL7a46",
            'referer': 'https://www.toutiao.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',

        }
        url = as_cp_url + f'&_signature={_signature}'
        res = requests.get(url=url, headers=headers).json()
        return res
    def get_message(self,response):
        dalis = response['data']
        print(dalis)
        taglis = []
        titlelis = []
        groupidlis = []
        commentslis = []
        sourcelis = []
        responses = []
        for _ in dalis:
            if 'chinese_tag'and'comments_count' in _:
                responses.append(_)
            else:
                pass
        print(dalis)
        for a in responses:
            print(a)
            tag = a['tag']
            taglis.append(tag)
            title = a['title']
            titlelis.append(title)
            id = a['group_id']
            groupidlis.append(id)
            comment = a['comments_count']
            commentslis.append(comment)
            sources = a['source']
            sourcelis.append(sources)
        return taglis,titlelis,groupidlis,commentslis,sourcelis

    async def parse_new(self,id):
        browser = await launch(headless=False, args=['--disable-infobars'])
        page = await browser.newPage()
        ulls = self.url+id
        await page.goto(ulls)
        extractor = GeneralNewsExtractor()
        result = extractor.extract(await page.content())
        intab = '?/|\.><:*"'
        title = result['title']           #如果有intab字符,系统会报错(windows里有特殊用法)
        for s in intab:
            if s in title:
                title = title.replace(s, '')
        contend = result['content'].split('来源')[0]
        path = 'E:\\biyejinri\\result\\'+title+'.txt'
        if not os.path.exists(path):
            self.save_data("result/"+title+".txt",contend)
            self.sort_data(contend)
        await browser.close()
    def save_data(self,title,contend):
        with open(title,'w',encoding='utf-8')as fp:
            fp.write(contend)
    def sort_data(self,contend):
        with open('result/all.txt','a',encoding='utf-8')as fp:
            fp.write(contend)
    def save_xls(self,data_list):
        row = 1
        col = 0
        workbook = xlsxwriter.Workbook('{}.xlsx'.format(datetime.date.today()))

        cell_format = workbook.add_format({
            'border': 1,
            'text_wrap': 1
        })
        merge_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'text_wrap': 1
        })

        worksheet = workbook.add_worksheet("首页新闻")
        worksheet.write(0, 0, "tag", merge_format)
        worksheet.write(0, 1, "media_avatar_url", merge_format)
        worksheet.write(0, 2, "title", merge_format)
        worksheet.write(0, 3, "abstract", merge_format)
        worksheet.write(0, 4, "source_url", merge_format)
        worksheet.write(0, 5, "source", merge_format)
        worksheet.write(0, 6, "media_url", merge_format)

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 65)
        worksheet.set_column(2, 2, 70)
        worksheet.set_column(3, 3, 255)
        worksheet.set_column(4, 4, 30)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 75)
        datali = data_list['data']
        for data in datali:
            tag = data.get("tag")
            media_avatar_url = data.get("media_avatar_url")
            title = data.get("title")
            abstract = data.get("abstract")
            source_url = data.get("source_url")
            source = data.get("source")
            media_url = data.get("media_url")

            worksheet.write(row, col, tag, cell_format)
            worksheet.write(row, col + 1, media_avatar_url, cell_format)
            worksheet.write(row, col + 2, title, cell_format)
            worksheet.write(row, col + 3, abstract, cell_format)
            worksheet.write(row, col + 4, source_url, cell_format)
            worksheet.write(row, col + 5, source, cell_format)
            worksheet.write(row, col + 6, media_url, cell_format)

            row += 1

        workbook.close()
    async def auto_login(self,user,password):
        browser = await launch(headless=False, args=['--disable-infobars'])
        page = await browser.newPage()
        await page.goto('https://www.toutiao.com')
        await page.click('.login-button')
        frame = page.frames
        await asyncio.sleep(1)
        login = await frame[0].querySelector('#login-type-account > img')
        await asyncio.sleep(1)
        await login.click()
        await page.type('#user-name', user)
        await page.type('#password', password)
        await page.waitFor(1000)
        await page.click("#bytedance-login-submit")
        await asyncio.sleep(1)
        pageSouth = await page.content()
        if "请完成下列验证后继续:" in pageSouth:
            print('你需要验证验证码，然后输入 ok 继续')
            word = input('请输入ok：')
            if word == 'ok':
                await asyncio.sleep(3)
                sendmes = await frame[0].querySelector(
                    'body > div > div.bui-box.container > div.bui-left.index-content > div.ugcBox > div > ul > li:nth-child(2)')
                await asyncio.sleep(1)
                await sendmes.click()
                writ = input("请输入要发送的文章名字")
                await page.type(
                    'body > div:nth-child(1) > div.bui-box.container > div.bui-left.index-content > div.ugcBox > div > div > div > div > div.editor > div > div.editor-title > input',
                    writ.split('.')[0])

                with open(writ,'r',encoding='UTF-8')as f:
                    mess = f.read()
                await page.waitFor(1000)
                await page.type('body > div:nth-child(1) > div.bui-box.container > div.bui-left.index-content > div.ugcBox > div > div > div > div > div.editor > div > div.syl-wrapper > div > div.ProseMirror.placeholeder', mess)
                await asyncio.sleep(3)
                await page.click(".upload-publish")
        input()
        await browser.close()
    def sort_word(self,path):
        words_sort.begin_sort(path)
        with open(path, 'w')as f:
            f.write(" ")
    def search_key(self,timestamp,_signature):
        searchkey.begin_search(timestamp,_signature)
if __name__ == '__main__':
    # while True:
    tt = Toutiao()
    max_time = int(time.time())
    pam = tt.get_pamas(max_time)  #url +sign
    print(pam)
    sel = input("请选择以下三个选择:1获取首页热点新闻 2自动登录并发布文章 3获取关键字文章")
    if sel == '1':
        while True:
            time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
            if time_now == "09:41:30":
                timelis = []
                timelis.append(max_time)
                pams = tt.get_pamas(max_time)
                print(timelis)
                newses = tt.get_news(*pams)  # respones.json
                print(newses),
                mss = tt.get_message(newses)
                for i in mss[2]:
                    asyncio.get_event_loop().run_until_complete(tt.parse_new(i))
                time.sleep(1)
                xlss = tt.save_xls(newses)
                nexttime = newses['next']
                timelis.append(nexttime['max_behot_time'])
                time.sleep(5)
                print(timelis)
                sot = tt.sort_word('result/all.txt')
            elif time_now == "12:30:00":
                timelis = []
                timelis.append(max_time)
                pams = tt.get_pamas(max_time)
                print(timelis)
                newses = tt.get_news(*pams)    #respones.json
                print(newses),
                mss = tt.get_message(newses)
                for i in mss[2]:
                    asyncio.get_event_loop().run_until_complete(tt.parse_new(i))
                time.sleep(1)
                xlss = tt.save_xls(newses)
                nexttime = newses['next']
                timelis.append(nexttime['max_behot_time'])
                time.sleep(5)
                print(timelis)


                sot = tt.sort_word('result/all.txt')
            elif time_now == "21:00:00":
                timelis = []
                timelis.append(max_time)
                pams = tt.get_pamas(max_time)
                print(timelis)
                newses = tt.get_news(*pams)    #respones.json
                print(newses),
                mss = tt.get_message(newses)
                for i in mss[2]:
                    asyncio.get_event_loop().run_until_complete(tt.parse_new(i))
                time.sleep(1)
                xlss = tt.save_xls(newses)
                nexttime = newses['next']
                timelis.append(nexttime['max_behot_time'])
                time.sleep(5)
                print(timelis)


                sot = tt.sort_word('result/all.txt')
    elif sel == '2':
        user = input("请输入账号")
        password = input("请输入密码")
        userr = asyncio.get_event_loop().run_until_complete(tt.auto_login(user,password))
    elif sel == '3':
        searchs = tt.search_key(max_time,pam[1])