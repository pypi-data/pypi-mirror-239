import requests
import time
import re
from bs4 import BeautifulSoup

class Cricbuzz():
	def __init__(self):
		pass

	def crawl_url(self,url):
		try:
			r = requests.get(url).json()
			return r
		except Exception:
			raise

	def players_mapping(self,mid):
		url = "https://www.cricbuzz.com/live-cricket-scores/75549/sl-vs-afg-30th-match-icc-cricket-world-cup-2023" + mid
		match = self.crawl_url(url)
		players = match.get('players')
		d = {}
		for p in players:
			d[int(p['id'])] = p['name']
		t = {}
		t[int(match.get('team1').get('id'))] = match.get('team1').get('name')
		t[int(match.get('team2').get('id'))] = match.get('team2').get('name')
		return d,t

	def matchinfo(self,mid):
		d = {}
		d['id'] = mid
		url = "https://www.cricbuzz.com/live-cricket-scores/75549/sl-vs-afg-30th-match-icc-cricket-world-cup-2023" + mid
		match = self.crawl_url(url)

		d['srs'] = match.get('series_name')
		d['mnum'] = match.get('header',).get('match_desc')
		d['type'] = match.get('header').get('type')
		d['mchstate'] = match.get('header').get('state')
		d['status'] = match.get('header').get('status')
		d['venue_name'] = match.get('venue').get('name')
		d['venue_location'] = match.get('venue').get('location')
		d['toss'] = match.get('header').get('toss')
		d['official'] = match.get('official')
		d['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(match.get('header').get('start_time'))))


		#squads
		p_map,_ = self.players_mapping(mid)
		team1 = {}
		team1['name'] = match.get('team1').get('name')
		t1_s = match.get('team1').get('squad')
		if t1_s is None:
			t1_s = []
		team1['squad'] = [ p_map[id] for id in t1_s]
		t1_s_b = match.get('team1').get('squad_bench')
		if t1_s_b is None:
			t1_s_b = []
		team1['squad_bench'] =	[ p_map[id] for id in t1_s_b]
		team2 = {}
		team2['name'] = match.get('team2').get('name')
		t2_s = match.get('team2').get('squad')
		if t2_s is None:
			t2_s = []
		team2['squad'] = [ p_map[id] for id in t2_s]
		t2_s_b = match.get('team2').get('squad_bench')
		if t2_s_b is None:
			t2_s_b = []
		team2['squad_bench'] =	[ p_map[id] for id in t2_s_b]
		d['team1'] = team1
		d['team2'] = team2
		return d

	def matches(self):

		url = "https://m.cricbuzz.com"

		# Send an HTTP request to the URL and get the content
		response = requests.get(url)

		if response.status_code == 200:
			# Parse the HTML content using BeautifulSoup
			soup = BeautifulSoup(response.text, 'html.parser')

			# Find all anchor elements with a "href" attribute containing match IDs and names
			match_links = soup.find_all("a", href=re.compile(r"/cricket-commentary/(\d+)/([^/]+)-[^/]+-[^/]+-\d+"))

			# Extract and print the match names and match IDs
			for link in match_links:
				match_url = link["href"]
				match_name = re.search(r"/cricket-commentary/(\d+)/([^/]+)-[^/]+-[^/]+-\d+", match_url).group(2)
				match_id = re.search(r"/cricket-commentary/(\d+)/([^/]+)-[^/]+-[^/]+-\d+", match_url).group(1)
				print(f"Match Name: {match_name}, Match ID: {match_id}")

		else:
			print("Request failed with status code:", response.status_code)

	def summary(self,mid):
		# Define the URL
		url = "https://m.cricbuzz.com/cricket-commentary/{mid}"

		# Send an HTTP request to the URL and get the content
		response = requests.get(url)

		if response.status_code == 200:
			# Parse the HTML content using BeautifulSoup
			soup = BeautifulSoup(response.text, 'html.parser')

			# Find the specific h3 element that contains the desired header value
			result = soup.find("h3", class_="ui-li-heading")
			score = soup.find("div", class_="col-xs-9 col-lg-9 dis-inline")

			if result or score:
				# Extract and print the desired header value
				result_text = result.get_text(strip=True)
				score_text = score.get_text(strip=True)
				print("Result of the Match:")
				print(result_text)
				print(score_text)
			else:
				print("Header not found on the page.")
		else:
			print("Request failed with status code:", response.status_code)


	def find_match(self,id):
		url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
		crawled_content = self.crawl_url(url)
		matches = crawled_content['matches']

		for match in matches:
			if match['match_id'] == id:
				return match
		return None

	def livescore(self,mid):
		data = {}
		try:
			comm = self.find_match(mid)
			if comm is None:
				return data
			batting = comm.get('bat_team')
			if batting is None:
				return data
			bowling = comm.get('bow_team')
			batsman = comm.get('batsman')
			bowler = comm.get('bowler')

			team_map = {}
			team_map[comm["team1"]["id"]] = comm["team1"]["name"]
			team_map[comm["team2"]["id"]] = comm["team2"]["name"]

			if batsman is None:
				batsman = []
			if bowler is None:
				bowler = []
			d = {}
			d['team'] = team_map[batting.get('id')]
			d['score'] = []
			d['batsman'] = []
			for player in batsman:
				d['batsman'].append({'name':player['name'],'runs': player['r'],'balls':player['b'],'fours':player['4s'],'six':player['6s']})
			binngs = batting.get('innings')
			if binngs is None:
				binngs = []
			for inng in binngs:
				d['score'].append({'inning_num':inng['id'], 'runs': inng['score'],'wickets':inng['wkts'],'overs':inng['overs'],'declare':inng.get('decl')})
			data['batting'] = d
			d = {}
			d['team'] = team_map[bowling.get('id')]
			d['score'] = []
			d['bowler'] = []
			for player in bowler:
				d['bowler'].append({'name':player['name'],'overs':player['o'],'maidens':player['m'],'runs':player['r'],'wickets':player['w']})
			bwinngs = bowling.get('innings')
			if bwinngs is None:
				bwinngs = []
			for inng in bwinngs:
				d['score'].append({'inning_num':inng['id'], 'runs': inng['score'],'wickets':inng['wkts'],'overs':inng['overs'],'declare':inng.get('decl')})
			data['bowling'] = d
			return data
		except Exception:
			raise

	def commentary(self,mid):
		data = {}
		try:
			url =  "http://mapps.cricbuzz.com/cbzios/match/" + mid + "/commentary"
			comm = self.crawl_url(url).get('comm_lines')
			d = []
			for c in comm:
				if "comm" in c:
					d.append({"comm":c.get("comm"),"over":c.get("o_no")})
			data['commentary'] = d
			return data
		except Exception:
			raise

	def scorecard(self,mid):
		try:
			url = "http://mapps.cricbuzz.com/cbzios/match/" +  mid + "/scorecard.json"
			scard = self.crawl_url(url)
			p_map,t_map = self.players_mapping(mid)

			innings = scard.get('Innings')
			data = {}
			d = []
			card = {}
			for inng in innings:
				card['batteam'] = inng.get('bat_team_name')
				card['runs'] = inng.get('score')
				card['wickets'] = inng.get('wkts')
				card['overs'] = inng.get('ovr')
				card['inng_num'] = inng.get('innings_id')
				extras = inng.get("extras")
				card["extras"] = {"total":extras.get("t"),"byes":extras.get("b"),"lbyes":extras.get("lb"),"wides":extras.get("wd"),"nballs":extras.get("nb"),"penalty":extras.get("p")}
				batplayers = inng.get('batsmen')
				if batplayers is None:
					batplayers = []
				batsman = []
				bowlers = []
				fow = []
				for player in batplayers:
					status = player.get('out_desc')
					p_name = p_map[int(player.get('id'))]
					batsman.append({'name':p_name,'runs': player['r'],'balls':player['b'],'fours':player['4s'],'six':player['6s'],'dismissal':status})
				card['batcard'] = batsman
				card['bowlteam'] = t_map[int(inng.get("bowl_team_id"))]
				bowlplayers = inng.get('bowlers')
				if bowlplayers is None:
					bowlplayers = []
				for player in bowlplayers:
					p_name = p_map[int(player.get('id'))]
					bowlers.append({'name':p_name,'overs':player['o'],'maidens':player['m'],'runs':player['r'],'wickets':player['w'],'wides':player['wd'],'nballs':player['n']})
				card['bowlcard'] = bowlers
				fall_wickets = inng.get("fow")
				if fall_wickets is None:
					fall_wickets = []
				for p in fall_wickets:
					p_name = p_map[int(p.get('id'))]
					fow.append({"name":p_name,"wkt_num":p.get("wkt_nbr"),"score":p.get("score"),"overs":p.get("over")})
				card["fall_wickets"] = fow
				d.append(card.copy())
			data['scorecard'] = d
			return data
		except Exception:
			raise

	def fullcommentary(self,mid):
		data = {}
		try:
			url =  "https://www.cricbuzz.com/match-api/"+mid+"/commentary-full.json"
			comm = self.crawl_url(url).get('comm_lines')
			d = []
			for c in comm:
				if "comm" in c:
					d.append({"comm":c.get("comm"),"over":c.get("o_no")})
			data['fullcommentary'] = d
			return data
		except Exception:
			raise
	def players(self,mid):
		data = {}
		try:
			url =  "https://www.cricbuzz.com/match-api/"+mid+"/commentary.json"
			players = self.crawl_url(url).get('players')
			d = []
			for c in players:
				if "player" in c:
					d.append({"id":c.get("id"),"f_name":c.get("f_name"),"name":c.get("name"),"bat_style":c.get("bat_style"),"bowl_style":c.get("bowl_style")})
			data['players'] = d
			return data
		except Exception:
			raise
