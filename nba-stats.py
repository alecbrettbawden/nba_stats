import requests
import csv

class NBAStats():

    # season formated in YYYY-YY in alignment with query parameter format
    def __init__(self, season):
        self.season = season
        self.stats_endpoint = 'https://stats.nba.com/stats/leaguedashplayerstats'
        self.player_index_endpoint = 'https://stats.nba.com/stats/playerindex'

        # Headers required by nba.com to be part of the request. User-Agent is parsed and managed by nba.com
        self.headers = {
            'Accept': '*/*',
            'Referer': 'https://www.nba.com/',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
        }

        # Query parameters required for the leaguedashplayerstats endpoint to receive 200 response for GET request
        self.stats_params = {
            'College': '',
            'Conference': '',
            'Country': '',
            'DateFrom': '',
            'DateTo': '',
            'Division': '',
            'DraftPick': '',
            'DraftYear': '',
            'GameScope': '',
            'GameSegment': '',
            'Height': '',
            'LastNGames': '0',
            'LeagueID': '00',
            'Location': '',
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': 'PerGame',
            'Period': '0',
            'PlayerExperience': '',
            'PlayerPosition': '',
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': '2021-22',
            'SeasonSegment': '',
            'SeasonType': 'Regular Season',
            'ShotClockRange': '',
            'StarterBench': '',
            'TeamID': '0',
            'TwoWay': '0',
            'VSConference': '',
            'VSDivision': '',
            'Weight': ''
        }

        
        # Query parameters required for the playerindex endpoint to receive 200 response for GET request
        self.player_params = {
            'College': '',
            'Country': '',
            'DraftPick': '',
            'DraftRound': '',
            'DraftYear': '',
            'Height': '',
            'Historical': '1',
            'LeagueID': '00',
            'Season': '2021-22',
            'SeasonType': 'Regular Season',
            'TeamID': '0',
            'Weight': ''
        }

    def get_season_stats(self):
        self.stats_params['Season'] = self.season
        res = requests.request('GET', self.stats_endpoint, headers=self.headers, params=self.stats_params, timeout=30)
        res = res.json()['resultSets'][0]
        columns = res['headers']
        self.season_data = [dict(zip(columns, row)) for row in res['rowSet']]
        
        return self.season_data

    def get_player_indexes(self):
        self.player_params['Season'] = self.season
        res = requests.request('GET', self.player_index_endpoint, headers=self.headers, params=self.player_params, timeout=30)
        res = res.json()['resultSets'][0]
        columns = res['headers']
        self.player_indexes = [dict(zip(columns, row)) for row in res['rowSet']]

        return self.player_indexes

    def get_third_mp_player(self):
        for player in self.season_data:
            player['MP'] = int(player['GP']*player['MIN'])
        self.season_data = sorted(self.season_data, key = lambda i: i['MP'], reverse=True)
        res = self.season_data[2]['PLAYER_NAME']

        return res
    
    def get_highest_ast_team(self):
        teams = {}
        for player in self.season_data:
            assists = player['GP']*player['AST']
            teams[player['TEAM_ABBREVIATION']] = int(teams[player['TEAM_ABBREVIATION']]+assists) if player['TEAM_ABBREVIATION'] in teams.keys() else assists
        res = max(teams, key=teams.get)

        return res
            
    def get_players_over_certain_points(self, points=750):
        if 'TOTAL_POINTS' not in self.season_data: self._get_players_total_points()
        teams = {}
        for player in self.season_data:      
            if player['TOTAL_POINTS'] >= points:
                teams[player['TEAM_ABBREVIATION']] = teams[player['TEAM_ABBREVIATION']]+1 if player['TEAM_ABBREVIATION'] in teams.keys() else 1
        res = max(teams, key=teams.get)

        return res
    
    def get_player_point_percentage(self):
        if 'TOTAL_POINTS' not in self.season_data: self._get_players_total_points()
        self.season_data = sorted(self.season_data, key = lambda i: i['TOTAL_POINTS'], reverse=True)
        teams = {}
        for player in self.season_data:
            if player['TEAM_ABBREVIATION'] in teams.keys():
                teams[player['TEAM_ABBREVIATION']][0] = teams[player['TEAM_ABBREVIATION']][0]+player['TOTAL_POINTS']
                teams[player['TEAM_ABBREVIATION']].append((player['PLAYER_NAME'], player['TOTAL_POINTS']))
            else:
                teams[player['TEAM_ABBREVIATION']] = [player['TOTAL_POINTS'], (player['PLAYER_NAME'], player['TOTAL_POINTS'])]
        for k, v in teams.items():
            percentage = round(v[1][1] / v[0],2)
            teams[k] = (v[1][0], percentage)
        res = sorted(teams.items(), key = lambda i: i[1][1], reverse=True)[0]
        
        return res

    def get_player_FG3_PCT_difference(self, min_FG3A=20):
        if not hasattr(self, 'average_FG3_PCT'): self._calculate_average_3PP(min_FG3A)
        if not hasattr(self, 'player_indexes'): self.get_player_indexes()

        player_index_dict = { player['PERSON_ID']: player for player in self.player_indexes}
        player_stats_dict = { player['PLAYER_ID']: player for player in self.season_data}

        pos_dict = {}
        for k, v in player_stats_dict.items():
            if player_index_dict[k]['POSITION'] in pos_dict.keys():
                if int(v['FG3A']*v['GP']) >= min_FG3A and abs(v['FG3_PCT'] - self.average_FG3_PCT) > pos_dict[player_index_dict[k]['POSITION']][1]:
                    pos_dict[player_index_dict[k]['POSITION']] = [v['PLAYER_NAME'], abs(v['FG3_PCT'] - self.average_FG3_PCT)]
            else:
                pos_dict[player_index_dict[k]['POSITION']] = [v['PLAYER_NAME'], abs(v['FG3_PCT'] - self.average_FG3_PCT)]
        res = pos_dict
        
        return res

    def data_to_csv(self, dictionary, csv_name):
        keys = dictionary[0].keys()

        with open(csv_name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(csv_name)


    # HELPER FUNCTION
    def _get_players_total_points(self):
        for player in self.season_data:
            player['TOTAL_POINTS'] = int(player['PTS']*player['GP'])
    
    def _calculate_average_3PP(self, min_FG3A):
        total_FG3_PCT = 0
        count_players = 0
        for player in self.season_data: 
            if int(player['FG3A']*player['GP']) >= min_FG3A:
                total_FG3_PCT += player['FG3_PCT']
                count_players += 1
        
        self.average_FG3_PCT = total_FG3_PCT/count_players
        print('average 3pt: ', self.average_FG3_PCT)

            


stats = NBAStats('2015-16')
stats.get_season_stats()
print('1. Third Most Minutes: ', stats.get_third_mp_player())
print('2. Highest Assist Team: ', stats.get_highest_ast_team())
print('3. Most Players Over 750: ', stats.get_players_over_certain_points())
print('4. Highest Percentage Points of Team: ', stats.get_player_point_percentage())
print('5. Furthest From Average 3 Point Percentage by Position: ', stats.get_player_FG3_PCT_difference())