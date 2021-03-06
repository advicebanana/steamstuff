from bs4 import BeautifulSoup
import sys

if len(sys.argv)<=1:
	print "Usage: " + __file__ + " arg1 [arg2 [...]]\n"
	exit

def steam3ID264 ( id3 ):
# https://developer.valvesoftware.com/wiki/SteamID
# assuming public universe and an "individual" type account:
 return str(1 << 52 | 1 << 56 | 1 << 32 | id3)

def parsehistory( soup ):
	result = []
	
	group = soup.find('a',{'class':['groupadmin_header_name','hoverunderline']}).get('href').rpartition('/')[2]
	for event in soup.findAll(lambda ev: ev.name=="div" and (ev.get('class') == ['historyItem'] or ev.get('class') == ['historyItemb'])):
		type = event.find('span','historyShort').contents[0]
		date = event.find('span','historyDate').contents[0]
		try:
			who = event.find('a',{'class':'whiteLink'})['data-miniprofile']
			who64 = steam3ID264(long(who))
			whoURL = event.find('a',{'class':'whiteLink'})['href']
			# who64 = "[url=https://steamrep.com/profiles/{}]{}[/url]".format(str(who64),str(who64))
		except (IndexError, TypeError) as e:
			who="-"
			who64="-"
			whoURL="-"
		try:
			actor = event.findAll('a',{'class':'whiteLink'})[1]['data-miniprofile']
			actor64 = steam3ID264(long(actor))
			actorURL = event.find('a',{'class':'whiteLink'})['href']
			# actor64 = "[url=https://steamrep.com/profiles/{}]{}[/url]".format(str(actor64),str(actor64))
		except IndexError:
			actor = "-"
			actor64 = "-"
			actorURL = "-"
		
		who = "-" if who=="-" else "[U:1:{}]".format(who)
		actor = "-" if actor=="-" else "[U:1:{}]".format(actor)
		print "{};{};{};{};{};{};{};{};{}".format(type,date,who,who64,whoURL,actor,actor64,actorURL,group)
	return []
	
data=[]
# print "event;time;user;user_id64;actor;actor_id64;group"
for fh in sys.argv[1:]:
	soup = BeautifulSoup(open(fh,'r'))
	data = data + parsehistory(soup)

