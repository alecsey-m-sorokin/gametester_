import concurrent.futures
import threading
import logging
from datetime import timedelta
import time
import unittest

from Locators import APIdata_PortalMaster, bets
from mm5_PM_Page import API_PortalMaster, ScatterCrystalActionType, LevelSphere

A = APIdata_PortalMaster
api = API_PortalMaster

a = range(1500, 1700)
aa = []

for num in range(len(a)):
    aa.append(a[num])

def thread_function(ids):
    print('\n')
    print('userId # %s' % ids)
    regToken = api.tps(ids)
    logging.info("Thread %s: starting", ids)
    time.sleep(2)
    logging.info("Thread %s: finishing", ids)


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

    FS_collected_count.clear()
    FS_collected_real_count.clear()
    FS_collected_winnings.clear()

    while r < 20:  # выставляем количество раундов (сессий)
        print('\n')
        print('session # %s' % str(r + 1))
        # regToken = api.testpartnerservice()
        regToken = api.tps(ids)
        authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
        balanceRealBefore = balanceReal
        func(balance, balanceReal, coin, currency)

        while i < 50:  # выставляем количество спинов (вращений)
            print('\n')
            print('spin # %s' % str(i + 1), ' / session # %s' % str(r + 1), ' / userId # %s' % ids)
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

                if spheres[1] == 2:  # тут проверяем, что есть 2 сферы среднего уровня и меняем 2 сферы на 1 сферу высшего уровня
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
                FS_collected_real_count.append(
                    fS)  # сюда помещаем значения freeSpinsCount, реальное значение фри спинов
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
        globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) * coin * i), 2))
        print('global wins = ', globalWins)
        print("Balance =", balance)
        print("Balance Real =", balanceReal)
        print('userId =', ids)
        i = 0

    print('\n')
    print('finished Portal Master after %s sessions' % r)
    print('total bets = ', sum(globalBets) * coin)
    print('total wins = ', round(sum(globalWins), 2))
    print('global wins = ', globalWins)
    print('free spins collected by player in all (%s) sessions: ' % r, FS_collected_count)
    print('real free spins collected by player in all (%s) sessions: ' % r, FS_collected_real_count)
    print('%s win in each free spins round: ' % currency, FS_collected_winnings)
    print('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
    print('the end')


# for i in range(len(a)):
#     a[i] = threading.Thread(target=fs, args=(a[i],))
#     a[i].start()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    for i in range(len(a)):
        aa[i] = threading.Thread(target=fs2, args=(aa[i],))
        aa[i].start()
        time.sleep(1)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     executor.map(fs, range(4))
