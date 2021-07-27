import argparse
import json
import sys

from mm6.Locators import RTP, APIdata_MancalaQuest
from mm6.MancalaQuest_Page import API_MancalaQuest


def findall(v, k):
    if type(v) == type({}):
        for k1 in v:
            if k1 == k:
                print(v[k1])
                return v[k1]
            result = findall(v[k1], k)
            if result is not None:
                return result

    if type(v) == type([]):
        for k1 in v:
            result = findall(k1, k)
            if result is not None:
                return result

with open('c:/testing/response2.json') as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

    results = findall(data, "WinStateInfo")
    if results is not None:
        print('bonus game is is finished')
        print(type(results))
        print(f'{results["WinState"]} {results["FreeSpinCount"]} {results["Multiplier"]}')
    else:
        print('bonus game is not finished yet ...')


if 'WinStateInfo' in data_str:
    print('OK')
    print(data_str)
    print(data['SpinResult']['UserSavedState']['StepPlayerContracts'])
    print(data['SpinResult']['UserSavedState']['StepOpponentContracts'])
else:
    print('not OK')

# print(json.dumps(data, indent=2))


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--rtp', type=int, default=A.partnerID_rtp_120)
    parser.add_argument('--users', type=int, default=3)
    return parser


A = APIdata_MancalaQuest
api = API_MancalaQuest

gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])
sessions = namespace.sessions
rounds = namespace.rounds
rtp = namespace.rtp
users = namespace.users

setRTP = RTP(users, rtp)
currentRTP = setRTP.setRTP()

print(currentRTP)
