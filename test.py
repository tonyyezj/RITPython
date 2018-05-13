import requests

url = 'http://localhost:9999/v1/'

############ CHANGE THE API KEY BEFORE RUNNING.
headers = {
    'X-API-KEY': 'WM1RI9PV',
    'Content-Type':'application/json'
}

def getTop4News(): 
	params = {
		'limit': 4 # counting backwards from the most recent news item
	}

	resp = requests.get(url + 'news', params = params, headers=headers)
	if resp.status_code != 200:
	    # This means something went wrong.
	    print('Error in fetching news')

	# Array of news item objects
	# Ordered by most recent to least recent.
	newsArray = resp.json()
	return newsArray

def getTimeElapsedSeconds():
	# Get Time Elapsed
	resp = requests.get(url + 'case', headers=headers)
	if resp.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('GET /case/ {}'.format(resp.status_code))

	caseDetails = resp.json()
	# Case is 0 to 450 ticks. Each tick = 4 seconds
	# So we need to multiply by 4.
	curTick = caseDetails['tick']
	elapsed = curTick*4
	return elapsed

#Get RT100 Spot Index
def getPricePath():
	getHistoryUrl = 'securities/history?ticker=RT100&period=1&limit=300'
	resp = requests.get(url + getHistoryUrl, headers=headers)
	if resp.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('GET /securities/ {}'.format(resp.status_code))
	historyArray = resp.json()
	return historyArray


newsArray = getTop4News()
for news in newsArray:
    print('{}\n{}'.format(news['headline'], news['body']))

print('Seconds elapsed: {}\n'.format(getTimeElapsedSeconds()))

historyArray = getPricePath()
for datapt in historyArray:
    print('Tick: {} Price: {}\n'.format(datapt['tick'], datapt['open']))

#example object for datapt:
# [
#   {
#     "tick": 11,
#     "open": 4.12,
#     "high": 4.21,
#     "low": 4.1,
#     "close": 4.15
#   }
# ]