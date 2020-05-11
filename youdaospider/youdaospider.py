import random
import time
import hashlib

import requests

url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

headers = {
    "Cookie": '_ga=GA1.2.37083754.1581260484; OUTFOX_SEARCH_USER_ID_NCOO=122841041.90469362; OUTFOX_SEARCH_USER_ID="82816029@10.108.160.18"; JSESSIONID=aaarRYY4OhNgo96yPMIbx; ___rl__test__cookies=1582202548824',
    "Host": "fanyi.youdao.com",
    "Origin": "http://fanyi.youdao.com",
    "Referer": "http://fanyi.youdao.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
}

""" JavaScript 加密实现的逻辑
var r = function(e) {
    var t = n.md5(navigator.appVersion)
      , r = "" + (new Date).getTime()
      , i = r + parseInt(10 * Math.random(), 10);
    return {
        ts: r,
        bv: t,
        salt: i,
        sign: n.md5("fanyideskweb" + e + i + "Nw(nmmbP%A-r6U3EUn]Aj")
    }
};
number + python
"""

ua = "5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"


def func(e):
    t = hashlib.md5(ua.encode('utf-8')).hexdigest()
    r = str(int(time.time() * 1000))
    i = r + str(random.randint(0, 10))
    return {
        'ts': r,
        'bv': t,
        'salt': i,
        'sign': hashlib.md5(("fanyideskweb" + e + i + "Nw(nmmbP%A-r6U3EUn]Aj").encode('utf-8')).hexdigest()
    }


def get_data(word):
    r = func(word)
    return {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": r['salt'],
        "sign": r['sign'],
        "ts": r['ts'],
        "bv": r['bv'],
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }


response = requests.post(url, headers=headers, data=get_data('你好'))
print(response.json())
