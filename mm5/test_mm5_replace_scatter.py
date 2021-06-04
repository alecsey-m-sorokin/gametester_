import argparse
import datetime
import sys
from datetime import timedelta
import time
import unittest
from random import randint

import pytest
from parameterized import parameterized
from locators import APIdata_PortalMaster, bets
from mm5_PM_Page import API_PortalMaster

A = APIdata_PortalMaster
api = API_PortalMaster
# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])

r = 0
i = 0
freeSpinsCount = 0
totalBets = []
totalWins = []
globalBets = []
globalWins = []
dt_start = time.time()

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
    print('round # %s' % str(r + 1))
    regToken = api.testpartnerservice()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency)

    while i < rounds:  # выставляем количество спинов (вращений)
        print('\n')
        print('spin # %s' % str(i + 1))
        creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)  # ставка ! CreditDebit # resultId = tokenAsync
        getAsyncResponse, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace, printAR = api.GetAsyncResponse(
            regToken, tokenAsync)  # асинхронный ответ ! GetAsyncResponse
        if getAsyncResponse["SpinResult"]["ScatterCrystalGame"]["Id"] is None:  # крутим барабан дальше, если нету бонуски
            print("ScatterCrystalGame =", scatterCrystalGame, '\n')
        else:
            print('\n')
            print("ScatterCrystalGame =", scatterCrystalGame)
            print("Spheres =", spheres)
            if spheres[0] > 0:  # тут проверяем, что есть хоть 1 сфера нижнего уровня
                actionType = '1'  # Replace : ActionType = 1
                levelSphere = '1'
            else:
                actionType = '2'  # Finish : ActionType = 2
                levelSphere = '0'
            print("SpheresSpinId =", spheresSpinId)
            print("ScattersForReplace =", scattersForReplace)
            if len(scattersForReplace) > 0:  # играем бонуску, когда есть 1 сфера 1 уровня и кристаллов > 0
                LR = randint(0, len(scattersForReplace) - 1)  # тут рандомно определяем, на какой Scatter менять сферу
                print("ScattersForReplace[%s] = " % LR, scattersForReplace[LR])
                scatterPositionRow = str(scattersForReplace[LR]["Row"])
                scatterPositionColumn = str(scattersForReplace[LR]["Column"])
                print("ScatterPositionRow = %s, ScatterPositionColumn = %s" % (scatterPositionRow, scatterPositionColumn))

                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=actionType,
                                                                                         ScatterPositionRow=scatterPositionRow,
                                                                                         ScatterPositionColumn=scatterPositionColumn,
                                                                                         LevelSphere=levelSphere,
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinsCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)  # асинхронный ответ ! GetAsyncResponse_Scatter
                print(getAsyncResponseScatter)

            else:  # завершаем бонуску, когда есть сфера, но нету кристалла
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=actionType,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere=levelSphere,
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinsCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)  # асинхронный ответ ! GetAsyncResponse_Scatter
                print(getAsyncResponseScatter)

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
        printAR(coin)

    r = r + 1

    print('finished Portal Master session after %s spins' % i)
    print('TotalWins in coins = ', totalWins)
    print(sum(totalWins))
    print('TotalBets in coins = ', totalBets)
    print(sum(totalBets))
    globalBets.append(sum(totalBets))
    totalWins.clear()
    totalBets.clear()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) / 125 * i), 2))
    print('GlobalWins in currency %s after %s spins = ' % (currency, i), globalWins)
    print("Balance =", balance)
    print("Balance Real =", balanceReal)
    i = 0

print('\n')
print('finished Portal Master after %s rounds' % r)
print('total bets = ', sum(globalBets) / 125)
print('total wins = ', round(sum(globalWins), 2))
print('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print('the end')


if __name__ == "__main__":
    unittest.main()
