import tweepy
from tkinter import *
import csv
import pandas as pd
import praw
import datetime
from datetime import datetime

def both_search():
	s_word = e1.get()
	if s_word == "" :
		l1.configure(text = "No Keyword Entered")
	else :
		twitter_search()
		reddit_search()
		l1.configure(text = "Twitter and Reddit Data Generated")
		 
def twitter_search():
	s_word = e1.get()
	if s_word == "" :
		l1.configure(text = "No Keyword Entered")
	else:
		#twitter keys
		twitter_keys = open('twitter_keys.txt', 'r')
	
		consumer_key = twitter_keys.readline().rstrip()	
		consumer_secret = twitter_keys.readline().rstrip()
		access_token = twitter_keys.readline().rstrip()
		access_token_secret = twitter_keys.readline().rstrip()
		twitter_keys.close()

		#twitter authorization
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth,wait_on_rate_limit=True)
		
		#twitter data file
		csvFile1 = open('twitter_data.csv', 'w')
		csvWriter1 = csv.writer(csvFile1)

		#Data collection from twitter
		for tweet in tweepy.Cursor(api.search,q='#'+s_word, count=100, tweet_mode="extended", since=
"2019-11-27").items(1000):
			csvWriter1.writerow([tweet.user.name, tweet.user.screen_name, tweet.created_at, tweet.full_text, tweet.favorite_count, tweet.retweet_count])
		l1.configure(text = "Twitter Data Generated")

def reddit_search():
	s_word = e1.get()
	if s_word == "" :
		l1.configure(text = "No Keyword Entered")
	else:
		#reddit keys
		reddit_keys = open('Reddit_keys.txt', 'r')
		CLIENT_ID = reddit_keys.readline().rstrip()
		CLIENT_SECRET = reddit_keys.readline().rstrip()
		USERNAME = reddit_keys.readline().rstrip()
		PASS = reddit_keys.readline().rstrip()
		USER_AGENT  = reddit_keys.readline().rstrip()
		reddit_keys.close()
	
	
		#reddit authorization
		reddit = praw.Reddit(client_id = CLIENT_ID,
			     client_secret = CLIENT_SECRET,
			     username = USERNAME,
			     password = PASS,
			     user_agent = USER_AGENT)
	
		#reddit data file
		csvFile2 = open('reddit_data.csv', 'w')
		csvWriter2 = csv.writer(csvFile2)
		
		#Data collection from reddit
		subreddit = reddit.subreddit('all').search(s_word,time_filter='day',limit=1000)
		for submission in subreddit:
			csvWriter2.writerow([submission.author, datetime.utcfromtimestamp(submission.created_utc), submission.title, submission.score, submission.num_comments, submission.url])
		l1.configure(text = "Reddit Data Generated")


master = Tk()
master.title("OSINT Software")
master.geometry('450x450')
master.configure(background = 'deep sky blue')
val = IntVar()
val.set("1")
Label(master, text="Enter a keyword", font = 'Arial 16 bold', fg='white', bg='deep sky blue').place(height=30,width=200,x=125,y=50)
e1 = Entry(master, font = 'Arial 14', fg = 'deep sky blue', justify = CENTER, border=0)
e1.place(height=30,width=250,x=100,y=100)
Button(master, text='Search Twitter', font = 'Arial 14 bold', bg='white', fg='deep sky blue',  command=twitter_search, border=0, activebackground = 'dodger blue', activeforeground = 'ghost white').place(height=30,width=150,x=150,y=150)
Button(master, text='Search Reddit', font = 'Arial 14 bold', bg='white', fg='deep sky blue',  command=reddit_search, border=0, activebackground = 'dodger blue', activeforeground = 'ghost white').place(height=30,width=150,x=150,y=200)
Button(master, text='Search Both', font = 'Arial 14 bold', bg='white', fg='deep sky blue',  command=both_search, border=0, activebackground = 'dodger blue', activeforeground = 'ghost white').place(height=30,width=150,x=150,y=250)
Button(master,text='Quit', font = 'Arial 14 bold', bg='white', fg='deep sky blue', command=master.quit, border=0, activebackground = 'dodger blue', activeforeground = 'ghost white').place(height=30,width=150,x=150,y=300)
l1 = Label(master, text="", font = 'Arial 16 bold', fg='white', bg='deep sky blue')
l1.place(height=30,width=350,x=50,y=350)
master.mainloop()
