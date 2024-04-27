import requests,json
from bs4 import BeautifulSoup


def batting_scorecard():
    print("Welcome to batting Scorecard..")
    get_match_url = input("Kindly provide the match link: ")
    if get_match_url:
        if(is_valid_url(get_match_url)):
            print('Choose the option from the following:')
            print('1. Type "1" for selecting Team 1')
            print('2. Type "2" for selecting Team 2')
            team_mapping = {
                '1': "ballByBallTeam1",
                '2' : "ballByBallTeam2"
            }
            team_select_ipt = input("chose the Option (1/2): ")

            if team_select_ipt in team_mapping:
                team_selected = team_mapping[team_select_ipt]
            else:
                print("Invalid choice")

            print("Getting Scorecard....")
            requested_json = batting_scorecard_teamwise(get_match_url,team_selected)
            print(requested_json)
        else:
            print("no a valid URL!")
    else:
        print("No Url Found!")

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
def batting_scorecard_teamwise(url,team):
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
    return json_data

function_mapping = {
    '1': batting_scorecard
}
# main function
def main():
    print('Welcome to the Invaders Analytics.')
    print('Choose the option from the following:')
    print('1. Batting Scorecard of a Match')
    print('2. Exit')

    user_input = input("Enter your choice (1/2): ")
    if user_input in function_mapping:
        function_mapping[user_input]()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()