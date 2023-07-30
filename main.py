from bs4 import BeautifulSoup
import requests
import json

URL_TABLE = "https://www.premierleague.com/tables"
URL_STATS = "https://www.premierleague.com/stats"


def get_info_from_table_row(row):
    # print(row, "\n")
    team_name = row["data-filtered-table-row-name"]
    if " and " in team_name:  # Brighton & Hove Albion
        team_name = team_name.replace(" and ", " & ")
    if "Bournemouth" in team_name:
        team_name = "AFC Bournemouth"

    rank = row["data-position"]
    teams[team_name]["rank"] = int(rank)

    short_name = row.find("span", "league-table__team-name--short")
    teams[team_name]["short_name"] = short_name.text

    tds = row.find_all("td")
    hdr_numbers = {0: "skip", 1: "skip", 2: "played", 3: "won", 4: "draw", 5: "lost", 6: "goals_for", 7: "goals_against", 8: "goals_diff", 9: "points"}
    i = 0
    for td in tds:
        if i in range(2, 10):
            tag = hdr_numbers[i]
            teams[team_name][tag] = int(td.text)
            # print(i, td.text)
        i += 1

# -----------------------------------


PL_data = requests.get(URL_TABLE)
soup = BeautifulSoup(PL_data.content, 'html.parser')
# print(soup.title)

teams = {}

navigation = soup.find("nav", "clubNavigation")
lis = navigation.find_all("li")
for li in lis:
    name = li.find_all("span")[1]
    team = name.text.strip()
    teams[team] = {"short_name": "", "logo": "", "site": "", "rank": -1, "points": -1, "played": -1, "won": -1, "draw": -1, "lost": -1, "goals_for": -1, "goals_against": -1, "goals_diff": -1}
    site = li.find("a", "clubList__link")
    site_ref = site["href"].strip()
    site_lst = site_ref.split('?')
    teams[team]["site"] = site_lst[0]
    logo = li.find("img")
    teams[team]["logo"] = logo["src"]


PL_table = soup.find("tbody", "league-table__tbody")
table_teams = PL_table.find_all("tr")
for row in table_teams:
    if row.has_attr("data-filtered-table-row-name"):
        get_info_from_table_row(row)


for k, v in teams.items():
    print(f"{k} {v}")


with open('PL_table.txt', 'w') as file:
    file.write(json.dumps(teams))
