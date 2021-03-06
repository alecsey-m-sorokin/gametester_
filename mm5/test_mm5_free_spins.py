import argparse
import datetime
import sys
from datetime import timedelta
import time
import unittest
from random import randint
# from parameterized import parameterized
from Locators import APIdata_PortalMaster, bets
from mm5_PM_Page import API_PortalMaster, ScatterCrystalActionType, LevelSphere, Logger, Reddy

A = APIdata_PortalMaster
api = API_PortalMaster


# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])

def goto(linenum):
    global line
    line = linenum


r = 0
i = 0
currency = ''
freeSpinCount = 0
freeSpinsCount = 0
totalBets = []
totalWins = []
globalBets = []
globalWins = []
FS_collected_count = []
FS_collected_real_count = []
FS_collected_winnings = []
globalWinsFS = []
dt_start = time.time()
dt_start_2 = datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S")

FS_collected_count.clear()
FS_collected_real_count.clear()
FS_collected_winnings.clear()


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=3)
    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])
strategy = namespace.strategy
sessions = namespace.sessions
rounds = namespace.rounds

print('\nusing', sys.argv[0])

dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))

while r < sessions:  # выставляем количество раундов (сессий)
    fileName = 'logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
    log = Logger(fileName, toFile=False, toConsole=True)
    print2 = log.printml
    print2('\n')
    print2('session # %s' % str(r + 1))
    regToken = api.testpartnerservice()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency)

    while i < rounds:  # выставляем количество спинов (вращений)
        print2(f'\nspin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {A.userID}')
        creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
        getAsyncResponse, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace, printAR = api.GetAsyncResponse(regToken, tokenAsync)
        trade_low_actionType = 0
        trade_mid_actionType = 0
        if getAsyncResponse["SpinResult"]["ScatterCrystalGame"]["Id"] is None:
            print2(f'ScatterCrystalGame = {scatterCrystalGame} \n')
        else:
            print2('\n')
            print2(getAsyncResponse)
            print2(f'ScatterCrystalGame = {scatterCrystalGame}')
            print2(f'Spheres = {spheres}')
            print2(f'SpheresSpinId = {spheresSpinId}')
            print2(f'ScattersForReplace = {scattersForReplace}')

            if spheres[0] == 3:  # тут проверяем, что есть 3 сферы 1 уровня и меняем 3 сферы на 1 сферу 2 уровня
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=ScatterCrystalActionType.Trade,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere=LevelSphere.First,
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)
                print2(getAsyncResponseScatter)

            if spheres[1] == 2:  # тут проверяем, что есть 2 сферы среднего уровня и меняем 2 сферы на 1 сферу высшего уровня
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=ScatterCrystalActionType.Trade,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere=LevelSphere.Second,
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)
                print2(getAsyncResponseScatter)

            else:  # Finish : ActionType = 2
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=ScatterCrystalActionType.Finish,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere='0',
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)
                print2(getAsyncResponseScatter)

        if freeSpinCount > 0:
            freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
            getAsyncResponseFreeSpin, fS, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
            status = getAsyncResponseFreeSpin["WinInfo"]["FreeSpin"]
            globalWinsFS.clear()
            FS_collected_count.append(freeSpinCount)  # сюда помещаем значения freeSpinCount, которые получает Игрок
            FS_collected_real_count.append(fS)  # сюда помещаем значения freeSpinsCount, реальное значение фри спинов
            globalWinsFS.append(getAsyncResponse["WinInfo"]["CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
            globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2(f'Current freeSpin win = {getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"]}')
            print2(f'globalWinsFS = {globalWinsFS}')
            while status:
                freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                getAsyncResponseFreeSpin, fS, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
                status = getAsyncResponseFreeSpin["WinInfo"]["FreeSpin"]
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2(f'Current freeSpin win = {getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"]}')
                print2(f'globalWinsFS = {globalWinsFS}')
            print2(f'Player got {sum(globalWinsFS)} Coins in {freeSpinCount} freeSpins')
            print2(f'Player got {sum(globalWinsFS) * coin} {currency} in {freeSpinCount} freeSpins')
            FS_collected_winnings.append(sum(globalWinsFS) / 100)  # тут сохраняем сколько игрок выиграл в CURRENCY за freeSpinCount фри спинов
            freeSpinCount = 0

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
        printAR(coin)

    r = r + 1

    print2(f'finished "Portal Master" session after {i} spins')
    print2(f'totalWins = {totalWins}')
    print2(f'sum totalWins = {sum(totalWins)}')
    print2(f'totalBets = {totalBets}')
    print2(f'sum totalBets = {sum(totalBets)}')
    globalBets.append(sum(totalBets))
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) * coin * i), 2))
    print2(f'globalWins = {globalWins}')
    print2(f'sum globalWins = {round(sum(globalWins), 2)}')
    print2(f'Balance = {balance}')
    print2(f'Balance Real = {balanceReal}')
    print2(f'userId = {A.userID}')
    i = 0

    text_bot_1 = f'finished "Portal Master" session after {rounds} spins \n UserId = {A.userID} \n totalWins = {totalWins} \n sum totalWins = {sum(totalWins)} \n ' \
                 f'totalBets = {totalBets} \n sum totalBets = {sum(totalBets)} \n globalWins = {globalWins} \n ' \
                 f'sum globalWins = {round(sum(globalWins), 2)} \n Balance = {balance} \n Balance Real = {balanceReal}'

    totalWins.clear()
    totalBets.clear()


print2('\n')
print2(f'finished "Portal Master" after {r} rounds')
print2(f'total bets = {sum(globalBets) * coin}')
print2(f'total wins = {round(sum(globalWins), 2)}')
print2(f'free spins collected by player in all ({r}) sessions: \n{FS_collected_count}')
print2('real free spins collected by player in all (%s) sessions: ' % r, FS_collected_real_count)
print2(f'{currency} win in each free spins round: \n{FS_collected_winnings}')
print2('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print2(f'start time = {dt_start_2}')
print2(f'end time = {datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S")}')
print2('the end')

text_bot_2 = f'finished "Portal Master" after {sessions} sessions with {rounds} rounds\n UserId = {A.userID} \n total bets = {sum(globalBets) * coin} \n globalWins = {globalWins} \n ' \
             f'total wins = {round(sum(globalWins), 2)} \n free spins collected by player in all ({sessions}) sessions: \n {FS_collected_count} \n' \
             f'{currency} win in each free spins round: \n{FS_collected_winnings} \n balance real before {balanceReal + (sum(globalBets) * coin) - round(sum(globalWins), 2)} \n ' \
             f'balance real after {balanceReal} \n Execution took: {timedelta(seconds=round(time.time() - dt_start))} \n start time = {dt_start_2} \n ' \
             f'end time = {datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S")} \n the end'

text_bot = f'Тест закончен \n UserId = {A.userID} \n Количество сессий = {sessions} \n Количество спинов = {rounds} \n' \
           f' Общая сумма ставок = {sum(globalBets) * coin} \n Общая сумма выигрыша = {round(sum(globalWins), 2)}'


Reddy(toReddy=True, gameLine='mm5').send_message2reddy(text_bot_2)


if __name__ == "__main__":
    unittest.main()
