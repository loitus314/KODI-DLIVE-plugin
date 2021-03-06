import graphql


def dq_get_user_info(uname):
	client = graphql.GraphQLClient('https://graphigo.prd.dlive.tv/')

	if uname == "":
		uname = "winsomehax"

	result = client.execute(
		''' query { user(username: "''' + uname + '''") { following { totalCount list { displayname username 
		livestream { thumbnailUrl title } pastBroadcasts { list { title length thumbnailUrl playbackUrl } } } } } 
		} ''')

	if result["data"]["user"] is None:
		result = None

	return result


def dq_get_all_live_streams(after):
	client = graphql.GraphQLClient('https://graphigo.prd.dlive.tv/')

	result = client.execute(
		'''query { livestreams (input: {showNSFW: true, order: TRENDING, after: "'''+after+'''"}) { pageInfo { startCursor, endCursor, 
		hasNextPage, hasPreviousPage} list { id, permlink, ageRestriction, thumbnailUrl, disableAlert, title, 
		createdAt, totalReward, watchingCount, creator {username, displayname}, view } } }''')

	return result


def all_live_streams():
	result = []

	after_cursor = "0"
	next_page = True

	while next_page:
		r = dq_get_all_live_streams(after_cursor)
		next_page= r["data"]["livestreams"]["pageInfo"]["hasNextPage"]
		after_cursor = r["data"]["livestreams"]["pageInfo"]["endCursor"]

		for u in r["data"]["livestreams"]["list"]:
			result.append((u["title"], 'https://live.prd.dlive.tv/hls/live/' + u["creator"]["username"] + '.m3u8',
						   u["thumbnailUrl"], u["creator"]["displayname"]))

	return result


def following_live_streams(uname):
	r = dq_get_user_info(uname)
	result = []

	for u in r["data"]["user"]["following"]["list"]:
		if u["livestream"] is not None:
			result.append(
				(u["livestream"]["title"], 'https://live.prd.dlive.tv/hls/live/' + u["username"] + '.m3u8',
				 u["livestream"]["thumbnailUrl"], u["displayname"]))

	return result


def following(uname):
	r = dq_get_user_info(uname)
	result = []

	for u in r["data"]["user"]["following"]["list"]:
		result.append((u["displayname"], u["username"]))

	return result


def replays(username, uname):
	r = dq_get_user_info(uname)
	result = []

	for u in r["data"]["user"]["following"]["list"]:
		if username == u["username"]:
			for s in u["pastBroadcasts"]["list"]:
				result.append((s["title"], s["length"], s["thumbnailUrl"], s["playbackUrl"]))

	return result
