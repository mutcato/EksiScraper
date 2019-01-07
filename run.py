from database import Database
from kanalscraper import Channels

db = Database()
ch = Channels()
sql_insert_kanal = "INSERT INTO kanallar (kanal_name) VALUES (%s)"
sql_insert_topic = "INSERT INTO basliklar (baslik_name,kanal_id) VALUES (%s,%s)"
sql_kanal_check = "SELECT * FROM kanallar WHERE kanal_name=%s" #Checks if the kanal has inserted already
sql_topic_check = "SELECT * FROM basliklar WHERE baslik_name=%s AND kanal_id=%s" #Checks if the baslik has inserted already

topics = ch.get_topics()

for by_channel in topics:
    for by_topic in by_channel["listoftopics"]:
        #Has it inserted aldeady
        channel_obj = db.query_select(sql_kanal_check, [by_channel["channel_name"]])
        print(channel_obj)
        if channel_obj:
            topic_obj = db.query_select(sql_topic_check, [by_topic["topic_title"],channel_obj[0]["id"]])
            #if the topic_obj is empty
            if topic_obj:
                print("TOPICMEVCUT")
            else:
                channel_id = channel_obj[0]["id"]
                db.query_insert(sql_insert_topic, [by_topic["topic_title"], channel_id])
                print(" inserted")
        else:
            topic_obj = db.query_select(sql_topic_check, [by_topic["topic_title"]])
            #if the topic_obj is empty
            if topic_obj:
                print("TOPICMEVCUT2")
            else:
                channel_id = db.query_insert(sql_insert_kanal, [by_channel["channel_name"]])
                db.query_insert(sql_insert_topic, [by_topic["topic_title"], channel_id])
                print("Not inserted")    
