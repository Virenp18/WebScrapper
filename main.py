import requests,json
from bs4 import BeautifulSoup

url = "https://cricclubs.com/ScarboroughCA/viewScorecard.do?matchId=5253&clubId=1835"

r = requests.get(url)
htmlContent = r.content

soup = BeautifulSoup(htmlContent,'html.parser')
teamone_batting_array = []
# to get first team batting info type ballByBallTeam1 and for second type ballByBallTeam2 inside {"id" : "type here.."}
invaders_batting = soup.find("div", {"id": "ballByBallTeam2"})
if invaders_batting:
    tbody_tag = invaders_batting.find("tbody")
    if tbody_tag:
        all_batsmanscore = tbody_tag.findAll("tr")
        for abs in all_batsmanscore:
            valid_tr = abs.find('img')
            if valid_tr:
                player_detail = {}
                one_bat_all_anc = abs.findAll("a")
                player_name = one_bat_all_anc[0]
                player_detail["name"] = "".join(one_bat_all_anc[0].get_text().split())
                batting_fig = abs.find_all("th")
                player_detail["runs"] = "".join(batting_fig[2].get_text().split())       
                player_detail["balls"] = "".join(batting_fig[3].get_text().split())       
                player_detail["fours"] = "".join(batting_fig[4].get_text().split())      
                player_detail["six"] = "".join(batting_fig[5].get_text().split())    
                player_detail["sr"] = "".join(batting_fig[6].get_text().split())   
                teamone_batting_array.append(player_detail)

json_data = json.dumps(teamone_batting_array)
# get all the data in form of JSON
print(json_data)