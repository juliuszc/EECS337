import json
import random
import re
from titlecase import titlecase
from tfidf import *
import numpy
import sys
from alchemyapi import *
from operator import itemgetter
import pprint

def removeRT(tweet):
    ''' Removes the RT @handle: rom the tweet.
        Input: string (Tweet)
        Output: string (Tweet without RT)'''
    t = re.split('RT\s\@\S+\:\s', tweet,1)
    if len(t)>1:
        return removeRT(t[len(t)-1]) # this recursiveness is necessary to remove the case of multiple RTs
    else:
        return t[0]

def winners(tweets):
    g = re.compile('.+.+\sgoes\sto.+.+')
    h = re.compile('.+.+wins.+.+for.+.+')
    winners={}
    awards={}
    output=[]
    i = 0
    for t in tweets:
        if h.match(t):
            words = re.split('wins',t)
            person = words[0].lstrip().rstrip()
            person = re.split('\.', person)[0] # ignore punctuation
            person = re.split('\!', person)[0]
            if '"' in person:
                person = re.split('"', person)[1]
            if person=='' or person[0]=='#':
                continue
            if person in winners.keys():
                winners[person]+=1
            else:
                winners[person]=1
            award = re.split('for\s',words[1])
            for phrase in award:
                p = phrase.lower().lstrip().rstrip()
                if re.match('^best', p):
                    if person in awards.keys():
                        if p in awards[person].keys():
                            awards[person][p].append(i)
                        else:
                            awards[person][p] = [i]
                    else:
                        awards[person] = {}
                        awards[person][p]=[i]
        elif g.match(t):
            words = re.split('\sgoes\sto',t)
            if re.match('^best',words[0].lower().lstrip()):
                category = words[0].lower().lstrip().rstrip()
                who = re.split('\sfor\s',words[1])
                person = who[0].lstrip()
                person = re.split('\s#', person)[0]
                if '"' in person:
                    person = re.split('"', person)[1]
                person = re.split('\.', person)[0]
                person = re.split('\!', person)[0]
                what = ''
                if len(who) > 1:
                    what = who[1].lstrip().rstrip()
                    what = re.split('http', what)[0]
                    what = re.split('#', what)[0]
                    if '"' in what:
                        what = re.split('"', what)[1]
                    what = re.split('\.', what)[0]
                if person in winners.keys():
                    winners[person]+=1
                else:
                    winners[person]=1
                if person in awards.keys():
                    if category in awards[person].keys():
                        awards[person][category].append(i)
                    else:
                        awards[person][category] = [i]
                else:
                    awards[person] = {}
                    awards[person][category]=[i]
        i += 1


    for key in winners:
        category = ''
        if winners[key] > 10:
            #print key+': '+str(winners[key])
            if key in awards:
                maxLen = 0
                for a in awards[key]:
                    l = len(awards[key][a])
                    if l > maxLen:
                        maxLen = l
                        category = a
                        categoryKey = a
            category = category.split('. ', 1)[0] #removes trailing links. award names do not take two sentences.
            if '."' in category:#if clause handles award names ending with quotes ex. "django unchained." 
                category = category.split('."',1)[0]
                category += str('."')
            category = category.split('#',1)[0] #removes any hashtags remaining
            if category != '' and key != '':
                output.append({'winner': key, 'category': titlecase(category), 'max': max(awards[key][categoryKey]), 'min': min(awards[key][categoryKey]), 'ave': numpy.mean(awards[key][categoryKey]), 'positions': awards[key][categoryKey], 'median': numpy.median(awards[key][categoryKey])})
    return output

def getNominees(tweets):
    nominee = re.compile('.+.+should\shave\swon.+.+')
    # should of won
    # should've won
    # robbed
    g = re.compile('.+.+\sgoes\sto.+.+')
    h = re.compile('.+.+wins.+.+for.+.+')
    flag = False
    listing = []
    ret = {}
    for t in tweets:
        if nominee.match(t):
            name = re.split('should\shave\swon',t)[0]
            name = re.split('[?.,!]', name)
            name = name[len(name)-1].lstrip().rstrip()
            if 'but' in name:
                name = re.split('but\s', name)
                name = name[len(name)-1].lstrip().rstrip()
            if len(name)<=3:
                continue
            if "@" in name:
                continue
            upper = 0
            wordcount = 1
            for l in name:
                if l.isupper():
                    upper += 1
                if l == " ":
                    wordcount += 1
            if float(upper)/float(wordcount) < .5 or float(upper)/float(len(name))>.3:
                continue
            listing.append(name)
        elif h.match(t) and len(listing) > 0:
            award = re.split('for\s',t)
            for phrase in award:
                p = phrase.lower().lstrip().rstrip()
                if re.match('^best', p):
                    if len(p.split(" ")) > 6:
                        continue
                    if "#" in p:
                        continue
                    #print p + "\n"
                    for persona in listing:
                        if p not in ret.keys():
                            ret[p] = []
                        if persona not in ret[p]:
                            ret[p].append(persona)
                    listing = []
        elif g.match(t) and len(listing) > 0:
            words = re.split('\sgoes\sto',t)
            if re.match('^best',words[0].lower().lstrip()):
                category = words[0].lower().lstrip().rstrip()
                if len(category.split(" ")) > 6:
                    continue
                if "#" in category:
                    continue
                #print category + "\n"
                for persona in listing:
                    if category not in ret.keys():
                        ret[category] = []
                    if persona not in ret[category]:
                        ret[category].append(persona)
                listing = []
    return ret

def getHosts(tweets):
    h = re.compile('.+.+\shosts\s.+.+')
    n = re.compile('.+.+\snext\s.+.+')
    votes = {}
    for t in tweets:
        if h.match(t) and not n.match(t):
            tokens = tokenizer.tokenize(t)
            bi_tokens = bigrams(tokens)
            for b in bi_tokens:
                #if isupper(b[0][0]) and isupper(b[1][0]):
                if b[0][0].isupper() and b[1][0].isupper():
                    bJoined = b[0] + ' ' + b[1]
                    if bJoined in votes.keys():
                        votes[bJoined] += 1
                    else:
                        votes[bJoined] = 1
    avg = numpy.mean(votes.values())
    s = numpy.std(votes.values())
    cutoff = avg + 2*s
    hosts = []
    for v in votes:
        if votes[v] >= cutoff and not (('Golden' in v) or ('Globes' in v)):
            hosts.append(v)
    return hosts


# Imperatives Begin Here
alchemy = AlchemyAPI()
with open('goldenglobes.json', 'r') as f:
    tweets = map(json.loads, f)
tweets = sorted(tweets, key=itemgetter('created_at')) 
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(tweets)
cleanTweets = []
for t in tweets:
    cleanTweets.append(removeRT(t['text']))


# 1. Find the names of the hosts
hosts = getHosts(cleanTweets)
print "HOSTS:"
for h in hosts:
	print h
# 2. For each award, find the name of the winner.
results = winners(cleanTweets)
print "\n\nWINNERS:"
for a in results:
    print a['category'].upper() + ": " + a['winner']
# 4. For each award, try to find the nominees
print "\n\nOTHER NOMINEES:\n"
nominees = getNominees(cleanTweets)
for n in nominees:
    print n.upper()
    for person in nominees[n]:
        print person
    print "\n"

# Probably going to completely junk this code
# The tweets where it talks about presenters don't seem to have any real correlation to the locations of the award that they are presenting.
# Because they are announced beforehand, though, it is acceptable to parse them from another online source, like Wikipedia
query = ''
entities = []
matches = []
matchNumber = []
i = 0

presenters={}
for a in results:
    start = a['min']
    category = a['category']
    query = ''
    i = 0
    possibilities = []
    while(True):
        query += cleanTweets[start - i].encode('utf-8') + ' '
        query += cleanTweets[start + i].encode('utf-8') + ' '
        i += 1
        if sys.getsizeof(query)>25000:
            break
    response = alchemy.entities('text',query,{})
    if response['status'] == 'OK':
        entities = response['entities']
    else:
        continue
    for e in entities:
    	if e['type'] == 'Person':
    		possibilities.append(e['text'])
    if len(possibilities) > 0:
    	presenters[category] = []
    	for p in possibilities:
    		if p in a['winner'] or a['winner'] in p:
    			continue
    		if p in hosts:
    			continue
    		if 'golden' in p.lower() or 'globes' in p.lower():
    			continue
    		presenters[category].append(p)
    		if len(presenters[category]) > 1:
    			break
print "\n\nPRESENTERS\n"
for p in presenters:
	print p.upper()
	for who in presenters[p]:
		print titlecase(who)
	print "\n"

# Analysis of best and worst dressed
wearing = re.compile('.+.+wearing.+.+')
query = ''
wearingTweets = []
reactions = []
response = None
for t in cleanTweets:
	if wearing.match(t):
		query += t.encode('utf-8') + ' '
		wearingTweets.append(t)
		if sys.getsizeof(query) > 50000:
			response = alchemy.entities('text',query,{'sentiment': 1, 'showSourceText': 1})
			query = ''
			if response['status'] == 'OK':
				reactions.extend(response['entities'])
response = alchemy.entities('text',query,{'sentiment': 1, 'showSourceText': 1})
if response['status'] == 'OK':
	reactions.extend(response['entities'])
for r in reactions:
	if 'score' in r['sentiment'].keys():
		r['score'] = float(r['sentiment']['score'])
	else:
		r['score'] = 0
rankedRxn = sorted(reactions, key=itemgetter('score')) 
#pprint.pprint(rankedRxn)
i = 0
j = 0
best = {}
worst = {}
while j < 5:
	r = rankedRxn[i]
	if 'disambiguated' not in r.keys():
		i += 1
		continue
	d = r['disambiguated']
	if 'subType' not in d.keys():
		i += 1
		continue
	if r['type'] == 'Person' and len(d['subType']) > 3:
		worst[r['text']] = []
		j += 1
	i += 1
i = 1
j = 0
while j < 5:
	r = rankedRxn[-i]
	if 'disambiguated' not in r.keys():
		i += 1
		continue
	d = r['disambiguated']
	if 'subType' not in d.keys():
		i += 1
		continue
	if r['type'] == 'Person' and len(d['subType']) > 3:
	    best[r['text']] = []
	    j += 1
	i += 1
for t in wearingTweets:
	for p in worst:
		if p.lower() in t.lower():
			worst[p].append(t)
	for p in best:
		if p.lower() in t.lower():
			best[p].append(t)
print "BEST DRESSED PER TWITTER REACTION"
i = 1
for p in best:
	bestTweets = list(set(best[p]))
	bestTweets = random.sample(bestTweets,1)
	print str(i) + ". " + p
	for t in bestTweets:
		print "   \"" + bestTweets[0] + "\""
	i += 1
print "WORST DRESSED PER TWITTER REACTION"
i = 1
for p in worst:
	worstTweets = list(set(worst[p]))
	worstTweets = random.sample(worstTweets,1)
	print str(i) + ". " + p
	print "   \"" + worstTweets[0] + "\""
	i += 1
