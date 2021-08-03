import argparse
import datetime
import sys
from datetime import timedelta
import time
import unittest
import threading
import logging
from random import randint
import pytest
from parameterized import parameterized
from Locators import bets, APIdata_MancalaQuest
from MancalaQuest_Page import API_MancalaQuest, Logger, RTP

A = APIdata_MancalaQuest
api = API_MancalaQuest


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=200)
    parser.add_argument('--rounds', type=int, default=200)
    parser.add_argument('--rtp', type=int, default=A.partnerID_rtp_95)
    parser.add_argument('--users', type=int, default=50)
    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])
sessions = namespace.sessions
rounds = namespace.rounds
rtp = namespace.rtp
users = namespace.users

if namespace.rtp == 90:
    rtp = A.partnerID_rtp_90
elif namespace.rtp == 95:
    rtp = A.partnerID_rtp_95
elif namespace.rtp == 96:
    rtp = A.partnerID_rtp_96
elif namespace.rtp == 97:
    rtp = A.partnerID_rtp_97
elif namespace.rtp == 120:
    rtp = A.partnerID_rtp_120
else:
    rtp = A.partnerID_rtp_95


def thread_function(ids):
    print(f'\nuserId # {ids}')
    regToken = api.tps(ids, rtp)
    logging.info(f'Thread {ids}: starting')
    time.sleep(2)
    logging.info(f'Thread {ids}: finishing')

r = 0
i = 0

def fs2(ids):
    while True:
        try:
            return fs(ids)
        except Exception as e:
            # print(f'spin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {ids} =================== Errrrrooooooooooooooooooorrrrrrr ===================', e)
            print('=================== Errrrrooooooooooooooooooorrrrrrr ===================', e)
            time.sleep(1)

# global fileName


def fs(ids):
    r = 0
    i = 0
    freeSpinCount = 0
    freeSpinsCount = 0
    totalBets = []
    totalWins = []
    globalBets = []
    globalWins = []
    globalWinsFS = []
    dt_start = time.time()
    fsLabel = ''

    FS_WILD_collected_count = []
    FS_BONUS_collected_count = []
    FS_BONUS_collected = []
    FS_WILD_collected_winnings = []
    FS_BONUS_collected_winnings = []

    FS_WILD_collected_count.clear()
    FS_BONUS_collected_count.clear()
    FS_WILD_collected_winnings.clear()
    FS_BONUS_collected_winnings.clear()
    FS_BONUS_collected.clear()

    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))

    while r < sessions:  # выставляем количество раундов (сессий)
        fileName = 'logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
        log = Logger(fileName, toFile=False, toConsole=True)
        print2 = log.printml
        print2('\n')
        print2('round # %s' % str(r + 1))
        regToken = api.tps(ids, rtp)
        # logging.info(f'Thread {ids}: starting')
        # regToken = regToken[0]
        authorizationGame, balance, balanceReal, coin, currency, resultId, func = api.AuthorizationGame(regToken)
        print2(str(authorizationGame))
        balanceRealBefore = balanceReal
        func(balance, balanceReal, coin, currency, resultId)

        if resultId is not None:
            resumeGame, timeOut, tokenAsyncResumeGame = api.ResumeGame(regToken, resultId)
            getAsyncResponse, resultId, spinId, totalFreeSpinsCount, remainingFreeSpinsCount, printAR, bonusGameResult = api.GetAsyncResponse(
                regToken, timeOut, tokenAsyncResumeGame)

            if totalFreeSpinsCount:
                freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
                getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(
                    regToken, timeOut, tokenAsyncFreeSpin)
                print2(
                    f'\n----- Mancala Quest {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
                globalWinsFS.clear()
                globalWinsFS.append(getAsyncResponse["WinInfo"][
                                        "CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('globalWinsFS = ', globalWinsFS)
                while remainingFreeSpinsCount > 0:
                    freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                    getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(
                        regToken, timeOut, tokenAsyncFreeSpin)
                    print2(
                        f'\n----- Mancala Quest {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
                    print2(str(getAsyncResponseFreeSpin))
                    globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                    print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                    print2('globalWinsFS = ', globalWinsFS)

                print2('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), totalFreeSpinsCount))
                print2('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) * coin, currency, totalFreeSpinsCount))
                if not bonusGameResult:
                    FS_WILD_collected_winnings.append(
                        sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов WILD
                else:
                    FS_BONUS_collected_winnings.append(
                        sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов BONUS
            else:
                pass

        else:
            pass

        while i < rounds:  # выставляем количество спинов (вращений)
            print2(f'\nspin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {ids}')
            creditDebit, timeOut, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
            getAsyncResponse, resultId, spinId, totalFreeSpinsCount, remainingFreeSpinsCount, printAR, bonusGameResult = api.GetAsyncResponse(
                regToken, timeOut, tokenAsync)
            print2(str(getAsyncResponse))
            printAR(coin)
            if bonusGameResult:
                fsLabel = 'BONUS GAME`s'
                print2('! you WIN !')
                print2(bonusGameResult)
            elif not bonusGameResult and totalFreeSpinsCount:
                FS_WILD_collected_count.append(
                    totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок от WILD символов
                fsLabel = 'WILD`s'

            if totalFreeSpinsCount:
                """
                тут начинаются Фри спины, полученные в результате выпадения Wild- символов слева и справа
                """
                freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
                getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(
                    regToken, timeOut, tokenAsyncFreeSpin)
                print2(
                    f'\n----- Mancala Quest {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
                print2(str(getAsyncResponseFreeSpin))
                globalWinsFS.clear()
                # FS_collected_count.append(totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок
                globalWinsFS.append(getAsyncResponse["WinInfo"][
                                        "CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('globalWinsFS = ', globalWinsFS)
                while remainingFreeSpinsCount > 0:
                    freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                    getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(
                        regToken, timeOut, tokenAsyncFreeSpin)
                    print2(
                        f'\n----- Mancala Quest {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
                    print2(str(getAsyncResponseFreeSpin))
                    globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                    print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                    print2('globalWinsFS = ', globalWinsFS)

                print2('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), totalFreeSpinsCount))
                print2('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) * coin, currency, totalFreeSpinsCount))
                # FS_collected_winnings.append(sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов
                if not bonusGameResult:
                    FS_WILD_collected_winnings.append(
                        sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов WILD
                else:
                    FS_BONUS_collected_winnings.append(
                        sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов BONUS

            else:
                pass

            i = i + 1
            totalBets.append(getAsyncResponse["BetSum"])
            totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
            printAR(coin)

        r = r + 1

        print2('\n')
        print2('finished "Mancala Quest" session after %s spins' % i)
        print2('totalWins ', totalWins)
        print2('sum totalWins ', sum(totalWins))
        print2('totalBets ', totalBets)
        print2('sum totalBets ', sum(totalBets))
        globalBets.append(sum(totalBets))
        totalWins.clear()
        totalBets.clear()
        authorizationGame, balance, balanceReal, coin, currency, resultId, func = api.AuthorizationGame(regToken)
        globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) * coin * i), 2))
        print2('globalWins', globalWins)
        print2('sum globalWins ', round(sum(globalWins), 2))
        print2("Balance =", balance)
        print2("Balance Real =", balanceReal)
        print2('userId =', ids)
        i = 0

    print2('\n')
    print2('finished Mancala Quest after %s rounds' % r)
    print2('total bets = ', sum(globalBets) * coin)
    print2('total wins = ', round(sum(globalWins), 2))
    print2('WILD free spins collected by player in all (%s) sessions: ' % r, FS_WILD_collected_count)
    print2('BONUS GAME free spins collected by player in all (%s) sessions: ' % r, FS_BONUS_collected_count)
    print2('%s win in each WILD`s free spins round: ' % currency, FS_WILD_collected_winnings)
    print2('%s win in each BONUS free spins round: ' % currency, FS_BONUS_collected_winnings)
    print2('Bonus collected: ', FS_BONUS_collected)

    print2('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
    print2('the end')
    # logging.info(f'Thread {ids}: finishing')


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    setRTP = RTP(users, rtp)
    currentRTP = setRTP.setRTP()

    for i in range(len(currentRTP[1])):
        currentRTP[2][i] = threading.Thread(target=fs2, args=(currentRTP[2][i],))
        currentRTP[2][i].start()
