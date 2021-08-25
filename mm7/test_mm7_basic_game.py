import argparse
import datetime
import sys
from datetime import timedelta
import time
import unittest
from random import randint
import pytest
import requests
from parameterized import parameterized
from Locators import bets, APIdata_SpiritOtTheLake
from SpiritOfTheLake_Page import API_SpiritOfTheLake, Logger, Reddy

A = APIdata_SpiritOtTheLake
api = API_SpiritOfTheLake

# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])

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
dt_start_2 = datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S")
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

def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=3)
    # parser.add_argument('--userid', type=int, default=A.userID)
    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])
sessions = namespace.sessions
rounds = namespace.rounds


global fileName
dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))

while r < sessions:  # set the number of rounds (sessions)
    fileName = 'logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
    log = Logger(fileName, toFile=False, toConsole=True)
    print2 = log.printml
    print2('\n')
    print2(f'\nround # %s' % str(r + 1))
    regToken = api.testpartnerservice()
    regToken = regToken[0]
    authorizationGame, balance, balanceReal, coin, currency, resultId, func = api.AuthorizationGame(regToken)
    print2(str(authorizationGame))
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency, resultId)

    if resultId is not None:  # if ResumeGame
        resumeGame, timeOut, tokenAsyncResumeGame = api.ResumeGame(regToken, resultId)
        getAsyncResponse, resultId, spinId, totalFreeSpinsCount, remainingFreeSpinsCount, printAR, bonusGameResult = api.GetAsyncResponse(regToken, timeOut, tokenAsyncResumeGame)

        if totalFreeSpinsCount:
            freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
            getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, timeOut, tokenAsyncFreeSpin)
            print2(f'\n----- Spirit of the Lake {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
            globalWinsFS.clear()
            globalWinsFS.append(getAsyncResponse["WinInfo"]["CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
            globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2('globalWinsFS = ', globalWinsFS)
            while remainingFreeSpinsCount > 0:
                freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, timeOut, tokenAsyncFreeSpin)
                print2(f'\n----- Spirit of the Lake {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
                print2(str(getAsyncResponseFreeSpin))
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('globalWinsFS = ', globalWinsFS)

            print2('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), totalFreeSpinsCount))
            print2('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) * coin, currency, totalFreeSpinsCount))
            if not bonusGameResult:
                FS_WILD_collected_winnings.append(sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов WILD
            else:
                FS_BONUS_collected_winnings.append(sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов BONUS
        else:
            pass

    else:
        pass

    while i < rounds:  # set the number of spins
        print2(f'\nspin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {A.userID}')
        creditDebit, timeOut, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
        getAsyncResponse, resultId, spinId, totalFreeSpinsCount, remainingFreeSpinsCount, printAR, bonusGameResult = api.GetAsyncResponse(regToken, timeOut, tokenAsync)
        # # print2(str(getAsyncResponse))
        # # printAR(coin)
        # if bonusGameResult:
        #     fsLabel = 'BONUS GAME`s'
        #     print2('! you WIN !')
        #     print2(bonusGameResult)
        #     # FS_BONUS_collected_count.append(bonusGameResult["FreeSpinCount"])
        #     FS_BONUS_collected_count.append(totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок от BONUS game
        #     FS_BONUS_collected.append(bonusGameResult)
        # elif not bonusGameResult and totalFreeSpinsCount:
        #     FS_WILD_collected_count.append(totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок от WILD символов
        #     fsLabel = 'WILD`s'
        #
        if totalFreeSpinsCount:
            """
            тут начинаются Фри спины, полученные в результате того, что дерево с цветами выросло
            """
            freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
            getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, timeOut, tokenAsyncFreeSpin)
            print2(f'\n----- Spirit of the Lake {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
            print2(str(getAsyncResponseFreeSpin))
            globalWinsFS.clear()
            # FS_collected_count.append(totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок
            globalWinsFS.append(getAsyncResponse["WinInfo"]["CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
            globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2('globalWinsFS = ', globalWinsFS)
            while remainingFreeSpinsCount > 0:
                freeSpin, timeOut, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, timeOut, tokenAsyncFreeSpin)
                print2(f'\n----- Spirit of the Lake {fsLabel} free spin # {str(totalFreeSpinsCount - remainingFreeSpinsCount)}')
                print2(str(getAsyncResponseFreeSpin))
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('globalWinsFS = ', globalWinsFS)

            print2('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), totalFreeSpinsCount))
            print2('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) * coin, currency, totalFreeSpinsCount))
            if not bonusGameResult:
                FS_WILD_collected_winnings.append(sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов WILD
            else:
                FS_BONUS_collected_winnings.append(sum(globalWinsFS) * coin)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов BONUS

        else:
            pass

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
        printAR(coin)

    r = r + 1

    print2('\n')
    print2(f'finished "Spirit OfThe Lake" session after {i} spins')
    print2(f'totalWins = {totalWins}')
    print2(f'sum totalWins = {sum(totalWins)}')
    print2(f'totalBets = {totalBets}')
    print2(f'sum totalBets = {sum(totalBets)}')
    globalBets.append(sum(totalBets))
    totalWins.clear()
    totalBets.clear()
    authorizationGame, balance, balanceReal, coin, currency, remainingFreeSpinsCount, func = api.AuthorizationGame(regToken)
    globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) * coin * i), 2))
    print2(f'globalWins = {globalWins}')
    print2(f'sum globalWins = {round(sum(globalWins), 2)}')
    print2(f'Balance = {balance}')
    print2(f'Balance Real = {balanceReal}')
    i = 0

print2('\n')
print2(f'finished "Spirit Of The Lake" after {r} rounds')
print2(f'total bets = {sum(globalBets) * coin}')
print2(f'total wins = {round(sum(globalWins), 2)}')
print2(f'free spins collected by player in all ({r}) sessions: \n{FS_WILD_collected_count}')
# print2('BONUS GAME free spins collected by player in all (%s) sessions: ' % r, FS_BONUS_collected_count)
print2(f'{currency} win in each free spins round: \n{FS_WILD_collected_winnings}')
# print2('%s win in each BONUS free spins round: ' % currency, FS_BONUS_collected_winnings)
# print2('Bonus collected: ', FS_BONUS_collected)
print2('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print2(f'start time = {dt_start_2}')
print2(f'end time = {datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S")}')
print2('the end')


token_bot = 'BGCcKgM79OMwRAJe-hWkZwpsRaIJ0-xx'
id_bot = 72220000235
id_chat = 324386
text_bot = f'Тест закончен \n Количество сессий = {sessions} \n Количество спинов = {rounds} \n' \
           f' Общая сумма ставок = {sum(globalBets) * coin} \n Общая сумма выигрыша = {round(sum(globalWins), 2)}'

def send_message(text):
    url = F"https://bot.reddy.team/bot{token_bot}/send?chat={id_chat}&msg={text_bot}"
    response = requests.get(url)
    print(response)
    print('Сообщение отправлено')


send_message(text_bot)


if __name__ == "__main__":
    unittest.main()
