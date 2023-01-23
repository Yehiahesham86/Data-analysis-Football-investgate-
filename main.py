# import modules
import pandas as pd
import matplotlib.pyplot as plt

# load dataset
df_match = pd.read_csv("F:/Data Analysis/2-Professional Level/Investigate a "
                       "Dataset/databases/Database_Soccer/Match.csv")

df_team = pd.read_csv("F:/Data Analysis/2-Professional Level/Investigate a "
                      "Dataset/databases/Database_Soccer/Team.csv")
#############################
######
# data cleaning
######
##############################
df_match.drop(columns={"goal", "shoton", "shotoff", "foulcommit", "card", "cross", "corner", "possession"},
              inplace=True)

df_match.drop_duplicates(inplace=True)
df_match["date"] = pd.to_datetime(df_match["date"])

num_match = len(df_match)
winner = []

for i in range(num_match):
    if df_match["home_team_goal"][i] > df_match["away_team_goal"][i]:
        winner.append("h")
    elif df_match["home_team_goal"][i] < df_match["away_team_goal"][i]:
        winner.append("a")
    else:
        winner.append("d")
pd.set_option('display.max_columns', None)
df_match["winner"] = winner


#####################################
#
# data analysis
#
######################################
def team_stat():
    print("Teams ID ", "real madrid : 8633 , barca : 8634 , man u : 10260 , man city : 8456 ,liverpool : 8650")
    team_id = int(input("Enter Team Id : "))
    team_name_search = df_team.query(f'team_api_id == {team_id}')
    team_name = team_name_search["team_long_name"].values[0]
    # what is team general stats ?
    win = df_match.query(
        f'((home_team_api_id == {team_id} )  and (winner == "h") ) or ((away_team_api_id == {team_id} )  and ('
        'winner == "a"))')

    lose = df_match.query(
        f'(away_team_api_id == {team_id}  and winner == "h") or (home_team_api_id == {team_id} and winner '
        '=="a" ) ')
    draw = df_match.query(f'(home_team_api_id == {team_id} or away_team_api_id == {team_id})  and (winner == "d")')
    all_match = df_match.query(f'home_team_api_id == {team_id} or  away_team_api_id == {team_id} ')

    win_p = round(len(win) / len(all_match) * 100)
    lose_p = round(len(lose) / len(all_match) * 100)
    draw_p = round(len(draw) / len(all_match) * 100)
    ###############################################
    ###################
    # is team (home or away) match effect the results?
    ##################
    ##########################################

    print("Team Name : {}".format(team_name))
    print("Win {}%  Lose {}%  Draw {}%".format(win_p, lose_p, draw_p))
    print("*" * 40)
    home_win = win.query(f'home_team_api_id == {team_id} and winner == "h"')
    away_win = win.query(f'away_team_api_id == {team_id} and winner == "a"')
    ########################
    home_lose = lose.query(f'home_team_api_id == {team_id} and winner == "a"')
    away_lose = lose.query(f'away_team_api_id == {team_id} and winner == "h"')
    ####################
    home_draw = draw.query(f'home_team_api_id == {team_id} and winner == "d"')
    away_draw = draw.query(f'away_team_api_id == {team_id} and winner == "d"')
    ####################
    all_points = len(all_match) * 3
    win_points = len(win) * 3 + len(draw)
    lose_points = len(lose) * 3 + len(draw) * 2

    print("{} win {} points from {} points".format(team_name, win_points, all_points))
    print("{} home win : ".format(team_name), round(len(home_win) / len(win) * 100), "%")
    print("{} away win : ".format(team_name), round(len(away_win) / len(win) * 100), "%")
    print("*" * 20)
    print("{} lose {} points from {} points".format(team_name, lose_points, all_points))
    print("{} home lose : ".format(team_name), round(len(home_lose) / len(lose) * 100), "%")
    print("{} away lose : ".format(team_name), round(len(away_lose) / len(lose) * 100), "%")
    print("*" * 20)
    print("{} home draw : ".format(team_name), round(len(home_draw) / len(draw) * 100), "%")
    print("{} away draw : ".format(team_name), round(len(away_draw) / len(draw) * 100), "%")

    # saving filtered data
    all_match.to_csv("C:/Users/Yehia/Desktop/team.csv", index=False)

    # load new data
    df_team_matches = pd.read_csv("C:/Users/Yehia/Desktop/team.csv")
    general = []
    for x in range(len(df_team_matches)):
        if df_team_matches["home_team_api_id"][x] == team_id and df_team_matches["winner"][x] == "h":
            general.append("W")
        elif df_team_matches["away_team_api_id"][x] == team_id and df_team_matches["winner"][x] == "a":
            general.append("W")
        elif df_team_matches["winner"][x] == "d":
            general.append("D")
        else:
            general.append("L")
    ########################################
    ##############
    # does team score more goals in home than away ?
    # does team conceded more goals in away than home?
    #############
    #########################################
    df_team_matches["general"] = general
    df_team_matches.to_csv("C:/Users/Yehia/Desktop/team.csv", index=False)
    goal_scored = 0
    goal_conceded = 0
    goal_scored_home = 0
    goal_scored_away = 0
    goal_conceded_home = 0
    goal_conceded_away = 0
    for z in range(len(df_team_matches)):
        if df_team_matches["home_team_api_id"][z] == team_id:
            goal_scored += df_team_matches["home_team_goal"][z]
            goal_conceded += df_team_matches["away_team_goal"][z]
            goal_scored_home += df_team_matches["home_team_goal"][z]
            goal_conceded_home += df_team_matches["away_team_goal"][z]
        else:
            goal_scored += df_team_matches["away_team_goal"][z]
            goal_conceded += df_team_matches["home_team_goal"][z]
            goal_scored_away += df_team_matches["away_team_goal"][z]
            goal_conceded_away += df_team_matches["home_team_goal"][z]

    print("*" * 40)
    print("ALL Goal Scored : {}".format(goal_scored))
    goal_scored_ratio = goal_scored / len(df_team_matches)
    print("Goal Scored Per Match : {}".format(round(goal_scored_ratio, 2)))
    print("*" * 20)
    print("ALL Goal Conceded : {}".format(goal_conceded))
    goal_conceded_ratio = goal_conceded / len(df_team_matches)
    print("Goal Conceded Per Match : {}".format(round(goal_conceded_ratio, 2)))
    print("*" * 20)
    print("ALL Goal Scored Home : {}".format(goal_scored_home))
    print("ALL Goal Conceded Home : {}".format(goal_conceded_home))
    print("*" * 20)
    print("ALL Goal Scored Away  : {}".format(goal_scored_away))
    print("ALL Goal Conceded Away : {}".format(goal_conceded_away))

    # data visualization & save image of it
    df_team_matches["general"].hist()
    plt.title(team_name)
    plt.xlabel('General Status')
    plt.ylabel('Matches')
    plt.grid(True)
    plt.savefig(f"{team_name}.png")
    plt.show()


def main():
    while True:
        team_stat()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
