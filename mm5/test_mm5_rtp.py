import concurrent.futures
import threading
import logging
from datetime import timedelta
import time
import unittest
import argparse
import datetime
import sys

from Locators import APIdata_PortalMaster, bets
from mm5_PM_Page import API_PortalMaster, ScatterCrystalActionType, LevelSphere, Logger, RTP

A = APIdata_PortalMaster
api = API_PortalMaster


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=5)
    parser.add_argument('--rtp', type=int, default=A.partnerID_rtp_95)
    parser.add_argument('--users', type=int, default=1)
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


r = 0
i = 0

def fs2(ids):
    while True:
        try:
            return fs(ids)
        except Exception as e:
            print(f'spin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {ids} =================== Errrrrooooooooooooooooooorrrrrrr ===================', e)


def fs(ids):
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

    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))

    while r < sessions:  # выставляем количество раундов (сессий)
        print('\n')
        print('session # %s' % str(r + 1))
        # regToken = api.testpartnerservice()
        regToken = api.tps(ids)
        authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
        balanceRealBefore = balanceReal
        func(balance, balanceReal, coin, currency)

        while i < rounds:  # выставляем количество спинов (вращений)
            fileName = 'logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
            log = Logger(fileName, toFile=False, toConsole=True)
            print2 = log.printml
            print2(f'\nspin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {ids}')
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

        print2('finished Portal Master session after %s spins' % i)
        print2(totalWins)
        print2(sum(totalWins))
        print2(totalBets)
        print2(sum(totalBets))
        globalBets.append(sum(totalBets))
        totalWins.clear()
        totalBets.clear()
        authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
        globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) * coin * i), 2))
        print2('global wins = ', globalWins)
        print2("Balance =", balance)
        print2("Balance Real =", balanceReal)
        print2('userId =', ids)
        i = 0

    print2('\n')
    print2('finished Portal Master after %s sessions' % r)
    print2('total bets = ', sum(globalBets) * coin)
    print2('total wins = ', round(sum(globalWins), 2))
    print2('global wins = ', globalWins)
    print2('free spins collected by player in all (%s) sessions: ' % r, FS_collected_count)
    print2('real free spins collected by player in all (%s) sessions: ' % r, FS_collected_real_count)
    print2('%s win in each free spins round: ' % currency, FS_collected_winnings)
    print2('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
    print2('the end')


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    setRTP = RTP(users, rtp)
    currentRTP = setRTP.setRTP()

    for i in range(len(currentRTP[1])):
        currentRTP[2][i] = threading.Thread(target=fs2, args=(currentRTP[2][i],))
        currentRTP[2][i].start()
        time.sleep(1)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     executor.map(fs, range(4))
