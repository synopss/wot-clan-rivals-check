import json
import math

import texttable
import urllib3
from tqdm import tqdm

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

        for results in data['data']['results']:
            player_previous_clan = ''
            for players in results['players']:
                url = 'https://api.worldoftanks.eu/wot/clans/accountinfo/?application_id' \
                      '=74613ef82f2d90e9c88a8449723936fe&account_id=' + players['uuid']
                data = get_data_response(url)

                if data['data'][players['uuid']] is not None:
                    player_clan = get_clan(data, players)
                    if player_previous_clan == '':
                        player_previous_clan = player_clan
                    if player_previous_clan != player_clan:
                        error_array = append_error_array(players['team_id'], results['title'], error_array)
                        break
                    player_previous_clan = player_clan
                else:
                    error_array = append_error_array(players['team_id'], results['title'], error_array)
                    break
            pbar.update(1)
        pbar.close()

        print_ending_message(error_array)
    else:
        print("This tournament doesn't exist")


def get_url(tournament_id, page_number):
    return 'https://worldoftanks.eu/tmsis/api/v1/tournament/teams/?filter[tournament_id]=' + str(tournament_id) + \
           ('&page[size]=' + str(page_number) if page_number is not None
            else '') + '&page[number]=1&filter[status]=confirmed'


def get_data_response(url):
    response = http.request('GET', url)
    return json.loads(response.data.decode('utf-8'))


def round_up(x):
    return int(math.ceil(x / 10.0)) * 10


def get_clan(data, players):
    return data['data'][players['uuid']]['clan']['tag']


def append_error_array(team_id, team_name, input_array):
    team_object = {'team_id': team_id, 'team_name': team_name}
    input_array.append(team_object)
    return input_array


def print_error_table(teams):
    table = texttable.Texttable()
    table.add_rows([["Team ID", "Team Name"]], True)
    table.set_cols_dtype(['t', 'i'])
    for i in teams:
        table.add_row([i['team_id'], i['team_name']])
    print(table.draw() + "\n")


def print_ending_message(error_array):
    if error_array is not None:
        print("Those teams don't meet the requirements: ")
        print_error_table(error_array)
    else:
        print('All teams meet the requirements')


if __name__ == "__main__":
    main()
