import sys
import argparse
from subprocess import call
from subprocess import Popen
import os
from mm4.Locators import APIdata_mm4
from mm5.Locators import APIdata_PortalMaster
from mm6.Locators import APIdata_MancalaQuest
from mm7.Locators import APIdata_SpiritOtTheLake
from mm8.Locators import APIdata_TwinWins
from xspin.Locators import APIdata_xspin


A_mm4 = APIdata_mm4
A_mm5 = APIdata_PortalMaster
A_mm6 = APIdata_MancalaQuest
A_mm7 = APIdata_SpiritOtTheLake
A_mm8 = APIdata_TwinWins
A_xspin = APIdata_xspin

r = 0

def gameParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    mm4 = subparsers.add_parser('mm4')
    mm4.add_argument('--strategy', default='basic')
    mm4.add_argument('--sessions', type=int, default=1)
    mm4.add_argument('--rounds', type=int, default=10)
    mm4.add_argument('--rtp', type=int, default=A_mm4.partnerID)
    mm4.add_argument('--users', type=int, default=1)

    mm5 = subparsers.add_parser('mm5')
    mm5.add_argument('--strategy', default='basic')
    mm5.add_argument('--sessions', type=int, default=1)
    mm5.add_argument('--rounds', type=int, default=10)
    mm5.add_argument('--rtp', type=int, default=A_mm5.partnerID)
    mm5.add_argument('--users', type=int, default=3)

    mm6 = subparsers.add_parser('mm6')
    mm6.add_argument('--strategy', default='basic')
    mm6.add_argument('--sessions', type=int, default=1)
    mm6.add_argument('--rounds', type=int, default=10)
    mm6.add_argument('--rtp', type=int, default=A_mm6.partnerID)
    mm6.add_argument('--users', type=int, default=3)
    # mm6.add_argument('--userid', type=int, default=A.userID)

    mm7 = subparsers.add_parser('mm7')
    mm7.add_argument('--strategy', default='basic')
    mm7.add_argument('--sessions', type=int, default=1)
    mm7.add_argument('--rounds', type=int, default=10)
    mm7.add_argument('--rtp', type=int, default=A_mm7.partnerID)
    mm7.add_argument('--users', type=int, default=3)
    # mm6.add_argument('--userid', type=int, default=A.userID)

    mm8 = subparsers.add_parser('mm8')
    mm8.add_argument('--strategy', default='basic')
    mm8.add_argument('--sessions', type=int, default=1)
    mm8.add_argument('--rounds', type=int, default=10)
    mm8.add_argument('--rtp', type=int, default=A_mm8.partnerID)
    mm8.add_argument('--users', type=int, default=3)

    xspin = subparsers.add_parser('xspin')
    xspin.add_argument('--strategy', default='basic')
    xspin.add_argument('--sessions', type=int, default=1)
    xspin.add_argument('--rounds', type=int, default=1)
    xspin.add_argument('--rtp', type=int, default=A_xspin.partnerID)
    xspin.add_argument('--users', type=int, default=1)

    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])

if namespace.command == "mm4":
    print('using', sys.argv[0])
    print(namespace)
    print(f'command = {namespace.command}')
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    print(f'rtp (partnerId) = {namespace.rtp}')
    print(f'users = {namespace.users}')

    if namespace.strategy == 'fs':
        os.system(f'python {A_mm4.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A_mm4.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A_mm4.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp} --users {namespace.users}')

    else:
        print("Что-то пошло не так...")

elif namespace.command == "mm5":
    print('using', sys.argv[0])
    print(namespace)
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    
    if namespace.strategy == 'fs':
        os.system(f'python {A_mm5.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A_mm5.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'replace':
        os.system(f'python {A_mm5.fileName_replace} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A_mm5.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp} --users {namespace.users}')

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
    print(f'users = {namespace.users}')

    if namespace.strategy == 'fs':
        os.system(f'python {A_mm6.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A_mm6.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A_mm6.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp} --users {namespace.users}')

    else:
        print("Что-то пошло не так...")

elif namespace.command == "mm7":
    print('using', sys.argv[0])
    print(namespace)
    print(f'command = {namespace.command}')
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    print(f'rtp (partnerId) = {namespace.rtp}')
    print(f'users = {namespace.users}')

    if namespace.strategy == 'fs':
        os.system(f'python {A_mm7.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A_mm7.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A_mm7.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp} --users {namespace.users}')

    else:
        print("Что-то пошло не так...")

elif namespace.command == "mm8":
    print('using', sys.argv[0])
    print(namespace)
    print(f'command = {namespace.command}')
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    print(f'rtp (partnerId) = {namespace.rtp}')
    print(f'users = {namespace.users}')

    if namespace.strategy == 'fs':
        os.system(f'python {A_mm8.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A_mm8.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A_mm8.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp} --users {namespace.users}')

    else:
        print("Что-то пошло не так...")

elif namespace.command == "xspin":
    print('using', sys.argv[0])
    print(namespace)
    print(f'command = {namespace.command}')
    print(f'strategy = {namespace.strategy}')
    print(f'sessions = {namespace.sessions}')
    print(f'rounds = {namespace.rounds}')
    print(f'rtp (partnerId) = {namespace.rtp}')
    print(f'users = {namespace.users}')

    if namespace.strategy == 'fs':
        os.system(f'python {A_xspin.fileName_fs} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'basic':
        os.system(f'python {A_xspin.fileName_basic} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds}')

    elif namespace.strategy == 'rtp':
        os.system(f'python {A_xspin.fileName_rtp} --strategy {namespace.strategy} --sessions {namespace.sessions} --rounds {namespace.rounds} --rtp {namespace.rtp} --users {namespace.users}')

    else:
        print("Что-то пошло не так...")


else:
    print("Что-то пошло не так...")
    # call(["python", "main2.py"])
