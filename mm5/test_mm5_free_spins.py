import argparse
import datetime
import sys
from datetime import timedelta
import time
import unittest
from random import randint
# from parameterized import parameterized
from locators import APIdata_PortalMaster, bets
from mm5_PM_Page import API_PortalMaster, ScatterCrystalActionType, LevelSphere

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

FS_collected_count.clear()
FS_collected_real_count.clear()
FS_collected_winnings.clear()


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=10)
    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])
strategy = namespace.strategy
sessions = namespace.sessions
rounds = namespace.rounds

print('\nusing', sys.argv[0])

while r < sessions:  # выставляем количество раундов (сессий)
    print('\n')
    print('session # %s' % str(r + 1))
    regToken = api.testpartnerservice()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency)

    while i < rounds:  # выставляем количество спинов (вращений)
        print('\n')
        print('spin # %s' % str(i + 1), ' / session # %s' % str(r + 1), ' / userId # %s' % A.userID)
        creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum,
                                                  A.cntLineBet)  # ставка ! CreditDebit # resultId = tokenAsync
        getAsyncResponse, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace, printAR = api.GetAsyncResponse(
            regToken, tokenAsync)  # асинхронный ответ ! GetAsyncResponse
        trade_low_actionType = 0
        trade_mid_actionType = 0
        if getAsyncResponse["SpinResult"]["ScatterCrystalGame"]["Id"] is None:
            print("ScatterCrystalGame =", scatterCrystalGame, '\n')
        else:
            print('\n')
            print(getAsyncResponse)
            print("ScatterCrystalGame =", scatterCrystalGame)
            print("Spheres =", spheres)
            print("SpheresSpinId =", spheresSpinId)
            print("ScattersForReplace =", scattersForReplace)

            if spheres[0] == 3:  # тут проверяем, что есть 3 сферы 1 уровня и меняем 3 сферы на 1 сферу 2 уровня
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=ScatterCrystalActionType.Trade,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere=LevelSphere.First,
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)
                print(getAsyncResponseScatter)

            if spheres[
                1] == 2:  # тут проверяем, что есть 2 сферы среднего уровня и меняем 2 сферы на 1 сферу высшего уровня
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=ScatterCrystalActionType.Trade,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere=LevelSphere.Second,
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)
                print(getAsyncResponseScatter)

            else:  # Finish : ActionType = 2
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=ScatterCrystalActionType.Finish,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere='0',
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)
                print(getAsyncResponseScatter)

        if freeSpinCount > 0:
            freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
            getAsyncResponseFreeSpin, fS, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
            status = getAsyncResponseFreeSpin["WinInfo"]["FreeSpin"]
            globalWinsFS.clear()
            FS_collected_count.append(freeSpinCount)  # сюда помещаем значения freeSpinCount, которые получает Игрок
            FS_collected_real_count.append(fS)  # сюда помещаем значения freeSpinsCount, реальное значение фри спинов
            globalWinsFS.append(getAsyncResponse["WinInfo"][
                                    "CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
            globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print('globalWinsFS = ', globalWinsFS)
            while status:
                freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                getAsyncResponseFreeSpin, fS, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
                status = getAsyncResponseFreeSpin["WinInfo"]["FreeSpin"]
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print('globalWinsFS = ', globalWinsFS)
            print('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), freeSpinCount))
            print('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) / 100, currency, freeSpinCount))
            FS_collected_winnings.append(
                sum(globalWinsFS) / 100)  # тут сохраняем сколько игрок выиграл в CURRENCY за freeSpinCount фри спинов
            freeSpinCount = 0

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
        printAR(coin)

    r = r + 1

    print('finished Portal Master session after %s spins' % i)
    print(totalWins)
    print(sum(totalWins))
    print(totalBets)
    print(sum(totalBets))
    globalBets.append(sum(totalBets))
    totalWins.clear()
    totalBets.clear()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) / 100 * i), 2))
    print('global wins = ', globalWins)
    print("Balance =", balance)
    print("Balance Real =", balanceReal)
    print('userId =', A.userID)
    i = 0

print('\n')
print('finished Portal Master after %s sessions' % r)
print('total bets = ', sum(globalBets) / 100)
print('total wins = ', round(sum(globalWins), 2))
print('global wins = ', globalWins)
print('free spins collected by player in all (%s) sessions: ' % r, FS_collected_count)
print('real free spins collected by player in all (%s) sessions: ' % r, FS_collected_real_count)
print('%s win in each free spins round: ' % currency, FS_collected_winnings)
print('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print('the end')

if __name__ == "__main__":
    unittest.main()
