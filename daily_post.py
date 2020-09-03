import praw, datetime, time, requests, sys

########################
######## config ########
########################
username=""
password=""

#something to identify yourself to reddit (e.g. "groestlcoin info updater v1.0 by /u/example")
useragent=""

#time to sleep in seconds after a network error:
time_to_sleep=60

subreddit_to_post=""
########################
###### end config ######
########################

nl="\n\n"

def main(useragent, username, password):
	#login:
	r = praw.Reddit(client_id='',
			client_secret='',
			username=username,
			password=password,
			user_agent=useragent)

	#get current time:
	currTime=datetime.datetime.now()

	#create title and description:
	title=createTitleSkeleton(currTime)
	description=createDescriptionSkeleton(currTime)

	#add data to description:
	description+=getData()

	#attempt to submit post
	print "Attempting to submit post to /r/" + subreddit_to_post
	try:
		post=r.subreddit(subreddit_to_post).submit(title=title, selftext=description)
	except praw.exceptions.APIException as e:
		if "SUBREDDIT_NOTALLOWED" in str(e):
			print "You do not have permission to post in /r/" + subreddit_to_post + ", exiting..."
		elif "SUBREDDIT_NOEXIST" in str(e):
			print "/r/" + subreddit_to_post + " does not exist, exiting..."
		else:
			print e
		sys.exit()
	print "Success! View at https://reddit.com/" + post.id

def createTitleSkeleton(currTime):
	title="Groestlcoin Network Status Update " + currTime.strftime('%A, %B %d, %Y')
	return title

def createDescriptionSkeleton(currTime):
	description="###Status of the Groestlcoin network as of " + currTime.strftime('%A, %B %d, %Y') + " at " + currTime.strftime('%H:%M:%S') + " EST:"
	return description

def getData():
	print "Beginning to obtain network data..."
	description=nl

	#get and format data:
	totalBtc=float("%.8f" % float(requests.get('http://chainz.cryptoid.info/grs/api.dws?q=totalcoins')))
	block_count=int(requests.get('http://chainz.cryptoid.info/grs/api.dws?q=getblockcount'))
	difficulty=float(requests.get('http://chainz.cryptoid.info/grs/api.dws?q=getdifficulty'))
	hashrate_day=float(requests.get('http://chainz.cryptoid.info/grs/api.dws?q=hashrate'))
	price=float(requests.get('https://chainz.cryptoid.info/grs/api.dws?q=ticker.usd'))

	#adding commas to data
	totalBtc=str("{:,f}".format(totalBtc))
	block_count=str("{:,d}".format(block_count))
	difficulty=str("{:,f}".format(difficulty))
	hashrate_day=str("{:,f}".format(hashrate_day))
	#one can only hope this is necessary...
	priceUSD=str("{:,.2f}".format(price))

	#adding data to description:
	description+="**Total groestlcoins:** " + totalBtc + nl
	description+="**Height:** " + block_count + nl
	description+="**Difficulty:** " + difficulty + nl

	description+="######Statistics for the past 24 hours:" + nl
	description+="**Estimated hashrate:** " + hashrate_day + " gh/s" + nl
	description+="**Current price:** US$" + priceUSD + nl

	description+="*Data provided by [cryptoid](https://chainz.cryptoid.info/).*" + nl

	description+="***" + nl

	description+="^^I ^^am ^^a ^^bot. **[^^Message ^^my ^^creator](https://www.reddit.com/message/compose?to=jackielove4u) ^^| [^^Source ^^code](https://github.com/Groestlcoin/crypto_bot)"

	return description

if __name__=="__main__":
	main(useragent, username, password)
