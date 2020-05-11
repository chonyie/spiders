'''
	2. 豆瓣Top250数据提取  
		采集网址：https://movie.douban.com/top250 
		采集目标：剧情简介 电影名称 电影图片 电影评分  评价人数
		采集要求：
			* 必须使用正则表达式
			* 必须使用函数式编程
			* 数据必须保存到CSV文件 逗号
'''
import re, csv
import requests

headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
}


# 获取详情页网址
def get_list_url(url):
    '''
    url: 接受一个翻页的网址
    return: 详情页网址
    '''
    # 发出请求 得到响应
    response = requests.get(url, headers=headers)
    # 从响应中提取数据
    detail_urls = re.findall('<a href="(.*?)" class="">', response.text)
    # print(list(set(detail_urls)))
    return list(set(detail_urls)) # 去重

# 访问详情页 获取详情页中的数据
def get_detail_data(detail_url):
    '''
    detail_url: 详情页的网址
    return: data 返回数据 正则提取的数据
    '''
    # 进入详情页
    response = requests.get(detail_url, headers=headers).text
    # 提取数据
    # 电影标题
    title = re.search('name="title" value="(.*?)">', response).group(1)
    # 电影图片
    picture = re.search('<img class="media" src="(.*?)" />', response).group(1)
    # 电影评分
    score = re.search('"ratingValue": "(.*?)"', response).group(1)
    # 评价人数
    ratingCount = re.search('"ratingCount": "(\d+)"', response).group(1)
    # 电影简介
    try:
        summary = re.search('<span property="v:summary" class="">(.*?)</span>', response, flags=re.S).group(1).strip()
        summary = re.sub('<br />', '', summary)
        summary = re.sub('\s', '', summary)
    except:
        summary = ''

    # 返回数据 csv 数据中没有逗号
    # item = f'{title},{picture},{score},{ratingCount},{summary}' # 字符串
    # print(item)
    # return item
    # 返回数据 csv 数据有逗号
    item = [title, picture, score, ratingCount, summary] # 列表
    return item


# 保存数据
def save_to_csv(data):
    '''
    data: 接受提取出来的数据
    return: None 保存到文件中了
    '''
    # with open('Code/douban.csv', 'a', encoding='utf-8') as fp:
    #     print('正在写入数据......')
    #     fp.write(data+'\n')

    with open('Code/douban2.csv', 'a', encoding='utf-8', newline='') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow(data) # 列表

    # 单独写文件
    fp = open('Code/douban3.csv', 'a', encoding='utf-8', newline='')
    csv.writer(fp)
    csv_writer.writerow(data) # 列表
    fp.close()

if __name__ == "__main__":
    for page in range(0, 100):
        url = f'https://movie.douban.com/top250?start={page*25}&filter=' # 第三页
        detail_urls = get_list_url(url) # 详情页网址 返回是列表
        for detail_url in detail_urls:
            item = get_detail_data(detail_url) # 访问详情页 返回的数据
            # 写入数据的
            save_to_csv(item)