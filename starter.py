import sys
import argparse
from subprocess import call
from subprocess import Popen
import os
from mm6.Locators import APIdata_MancalaQuest

A = APIdata_MancalaQuest

fileName_fs = 'mm5/' + 'test_mm5_free_spins.py'
fileName_basic = 'mm5/' + 'test_mm5_basic_game.py'
fileName_replace = 'mm5/' + 'test_mm5_replace_scatter.py'

r = 0

def gameParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    mm5 = subparsers.add_parser('mm5')
    mm5.add_argument('--strategy', default='basic')
    mm5.add_argument('--sessions', type=int, default=1)
    mm5.add_argument('--rounds', type=int, default=10)

    mm6 = subparsers.add_parser('mm6')
    mm6.add_argument('--strategy', default='basic')
    mm6.add_argument('--sessions', type=int, default=1)
    mm6.add_argument('--rounds', type=int, default=10)
    mm6.add_argument('--rtp', type=int, default=A.partnerID)
    # mm6.add_argument('--userid', type=int, default=A.userID)

    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])


if namespace.command == "mm5":
    print('using', sys.argv[0])
    print(namespace)
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    
    if namespace.strategy == 'fs':
        os.system(f'python {fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'replace':
        os.system(f'python {fileName_replace} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    else:
        print("Что-то пошло не так...")

elif namespace.command == "mm6":
    print('using', sys.argv[0])
    print(namespace)
    print(f'command = {namespace.command}')
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    print(f'rtp (partnerId) = {namespace.rtp}')

    if namespace.strategy == 'fs':
        os.system(f'python {A.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp}')

    else:
        print("Что-то пошло не так...")

else:
    print("Что-то пошло не так...")
    # call(["python", "main2.py"])
