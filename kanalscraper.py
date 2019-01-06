import urllib3
from bs4 import BeautifulSoup

class Channels(object):

	def __init__(self):
		self.http = urllib3.PoolManager()
		self.domain = 'https://eksisozluk.com'
		self.channels_url = 'https://eksisozluk.com/kanallar'
		self.channels = self.get_channels()

	def get_channels(self):
		r = self.http.request('GET', self.channels_url)
		soup = BeautifulSoup(r.data, "html.parser")
		arahtml = soup.find(id="channel-follow-list").find_all("li")

		kanal = []
		for knl in arahtml:
				with_hashtag = knl.find(class_="index-link").get_text()
				kanal.append({"name":with_hashtag[1:], "url":knl.find("a").get('href')})

		return kanal

	def get_topics(self):
		topicss = []
		for ch in self.channels:
			#print(ch["name"])
			#print(self.domain + ch["url"])
			listoftopics = []
			for page in range(1,5):
				r = self.http.request('GET', self.domain + ch["url"] + "?p=" + str(page))
				soup = BeautifulSoup(r.data, "html.parser")
				#Gets only list items topics as a list
				arahtml = soup.find(id="content-body").find_all("li")
				for tpc in arahtml:
					#Small tag ile sayfa sayısı belirtildiyse o tagı DOM'dan çıkarıyor
					if tpc.small: tpc.small.decompose()

					# Ignore the date after question mark(?)
					href = tpc.find("a").get("href")
					topic_href = href[:href.find("?day")]

					listoftopics.append({"topic_title":tpc.find("a").getText(), "topic_href":topic_href})
				
			topicss.append({"channel_name":ch["name"],"listoftopics":listoftopics})
		return topicss
			
