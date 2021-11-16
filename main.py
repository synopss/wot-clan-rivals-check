import json
import math

import texttable
import urllib3
from tqdm import tqdm
from collections import Counter

http = urllib3.PoolManager()


def main():
    tournament_id = input('Enter the tournament ID: ')
    check_teams(tournament_id)


def check_teams(tournament_id):
    data = get_data_response(get_url(tournament_id, None))

    total_count = data['data']['total_count']
    page_number = round_up(total_count)

    data = get_data_response(get_url(tournament_id, page_number))
    if data['status'] != 'error' or tournament_id is not None:
        pbar = tqdm(total=total_count, ncols=100, unit='teams', desc='Processing: ')
        error_array = []

        for team in data['data']['results']:
            team_id = 0
            players = []
            for player in team['players']:
                url = 'https://api.worldoftanks.eu/wot/clans/accountinfo/?application_id' \
                      '=74613ef82f2d90e9c88a8449723936fe&account_id=' + player['uuid']
                data = get_data_response(url)

                players.append({'player': player['nickname'], 'clan': get_clan_from_data(data, player)})
                team_id = player['team_id']

            problematic_players = get_problematic_players(players)
            if problematic_players[0] != []:
                error_array.append({'team_id': team_id, 'team_name': team['title'], 'nicknames': ','.join(problematic_players[0])})

            pbar.update(1)
        pbar.close()

        print_ending_message(error_array)
    else:
        print('This tournament doesn\'t exist')


def get_url(tournament_id, page_number):
    return 'https://worldoftanks.eu/tmsis/api/v1/tournament/teams/?filter[tournament_id]=' + str(tournament_id) + \
           ('&page[size]=' + str(page_number) if page_number is not None
            else '') + '&page[number]=1&filter[status]=confirmed'


def get_data_response(url):
    response = http.request('GET', url)
    return json.loads(response.data.decode('utf-8'))


def round_up(x):
    return int(math.ceil(x / 10.0)) * 10


def get_clan_from_data(data, player):
    if data['data'][player['uuid']] is not None:
        return data['data'][player['uuid']]['clan']['tag']
    return 'No clan'


def get_problematic_players(players):
    clan_counts = Counter(p['clan'] for p in players)
    clan_from_team = clan_counts.most_common(1)[0][0]
    return [p['player'] for p in players if p['clan'] != clan_from_team], clan_from_team


def append_error_array(team_id, team_name, nicknames, input_array):
    team_object = {'team_id': team_id, 'team_name': team_name, 'nicknames': nicknames}
    input_array.append(team_object)
    return input_array


def print_error_table(teams):
    table = texttable.Texttable()
    table.add_rows([['Team ID', 'Team Name', 'Nicknames']], True)
    table.set_cols_dtype(['i', 't', 't'])
    for t in teams:
        table.add_row([t['team_id'], t['team_name'], t['nicknames']])
    print(table.draw() + '\n')


def print_ending_message(error_array):
    if error_array is not None:
        teams_count = len(error_array)
        if teams_count == 1:
            print('This team doesn\'t meet the requirements: ')
        elif teams_count > 1:
            print(f'Those {teams_count} teams don\'t meet the requirements: ')
        print_error_table(error_array)
    else:
        print('All teams meet the requirements')


if __name__ == '__main__':
    main()
