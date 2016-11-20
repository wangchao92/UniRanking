#encoding=utf8
import requests
from bs4 import BeautifulSoup

Default_Header = {
	'Host': 'www.zinch.cn',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2'
}

data = {
    'name': 'chao.wang92@gmail.com',
    'pass': 'wc@921008'
}

_session = requests.session()
_session.headers.update(Default_Header)
loginsoup = BeautifulSoup(_session.get('http://www.zinch.cn/account').content, 'html.parser')
form_data = loginsoup.select("form[action^=/account] input")
data.update({inp["name"]: inp["value"] for inp in form_data if inp["name"] not in data})
_session.post('http://www.zinch.cn/account#!/account', data=data, headers=Default_Header)
uniRanking = {}
uniIdName = {}
years = ['2015', '2016', '2017']

def getPage(year, pageIdx):
	if year == '2017':
		pageUrl = 'http://www.zinch.cn/top/university/367583/2017/367589/367848?page=' + pageIdx
	else:
		pageUrl = 'http://www.zinch.cn/top/university/world/usnews' + year + '?page=' + pageIdx
	soup = BeautifulSoup(_session.get(pageUrl).content, 'html.parser')
	uniDiv = soup.find('div', attrs = {'class': 'school-rank-detail-page-body'})
	uniList = uniDiv.find('ul').findAll('li')
	if year not in uniRanking:
		uniRanking[year] = {}
	for uni in uniList:
		rank = uni.find('div', attrs = {'class': 'rank-right-top-left'})
		name = uni.find('div', attrs = {'class': 'rank-right-top-right-name'}).find('div', attrs = {'class': 'rank-right-top-right-name-en'}).string.strip()
		uniRanking[year][uni['id']] = rank.string
		if uni['id'] not in uniIdName:
			uniIdName[uni['id']] = name

def getAcendingUni():
	for id in uniIdName.keys():
		if uniIsBetterNow(id):
			print uniIdName[id], uniRanking['2017'][id]

def uniIsBetterNow(id):
	for i in range(len(years) - 1, 0, -1):
		rankNow = uniRanking[years[i]].get(id)
		rankBefore = uniRanking[years[i - 1]].get(id)
		if rankNow is None or rankBefore is None:
			return False
		elif int(rankNow) > int(rankBefore):
			return False
	return True

if __name__ == '__main__':
	for year in years:
		for i in range(1, 10):
			getPage(year, str(i))
	getAcendingUni()