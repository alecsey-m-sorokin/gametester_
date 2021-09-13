import argparse
import sys
import datetime
from datetime import timedelta
import time
import threading
import logging
import requests
from random import randint
from Locators import APIdata_xspin, bets
from xspin_Crazy_Scientist_Page import API_CrazyScientist, Logger, RTP

A = APIdata_xspin
api = API_CrazyScientist


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', default=['basic'])
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=7)
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


def fs2(ids):
    # return fs(ids)

    while True:
        try:
            return fs(ids)
        except Exception as e:
            print(f'/ userId # {ids} =================== Errrrrooooooooooooooooooorrrrrrr ===================', e)


def fs(ids):
    r = 0
    i = 0
    global_count_spin = 0
    GlobalTotalBets = 0
    GlobalTotalWins = 0
    GlobalTotalWinsFS = 0
    GlobalTotalWinsBG = 0
    spinWinsFS = 0
    freeSpinsCount = 0
    totalBets = 0
    totalWins = 0
    totalWinsFS = 0
    totalWinsBG = 0
    dt_start = time.time()
    ResultId_Update = ''


    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    # set the number of rounds (sessions)
    while r < sessions:
        fileName = 'xspin/logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
        log = Logger(fileName, toFile=False, toConsole=True)
        print2 = log.printml
        print2('\n')
        print2('round # %s' % str(r + 1))
        regToken = api.tps(ids, rtp)
        authorizationGame = api.AuthorizationGame(regToken)
        resultId = authorizationGame["ResultId"]
        winsBG_for_update = 0
        updatedCurrentSpin = 0

        if resultId is not None:
            print2('Восстанаваливаем игру')
            resumeGame, timeOut, tokenAsyncResumeGame = api.ResumeGame(regToken, resultId)
            getAsyncResponse = api.GetAsyncResponse(
                regToken, tokenAsyncResumeGame)
            updatedSpinResult = getAsyncResponse['UpdatedSpinResult']

            ResultId = getAsyncResponse["ResultId"]
            ResultId_Update = getAsyncResponse["ResultId"]

            print2('Игру восстановили, проверяем на бонусную игру')
            # check if there is a bonus game
            if getAsyncResponse["SpinResult"]["DiceGame"] is not None:
                Info = "true"
                SpinId = getAsyncResponse["SpinResult"]["Id"]
                BonusGameId = getAsyncResponse["SpinResult"]["DiceGame"]["Id"]
                if updatedSpinResult is not None and updatedSpinResult["DiceGame"] is None:
                    print2('начисление выигрыша за updated spin после бонусной игры')
                    print2('\n')
                    updatedCurrentSpin = updatedSpinResult["WinCoins"]
                    print2(f'updatedSpinResult = {updatedSpinResult}')

                tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                print2("Bonus game started")
                if getAsyncResponse["SelectedSector"] is not None:
                    print2("Select Card in bonus game")
                    tokenAsync = api.SelectCardBonusGame(regToken, ResultId, SpinId, BonusGameId)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                while getAsyncResponse["ThrowsLeft"] > 0:
                    Info = "false"
                    tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    # check there is in the bonus game, the card game
                    if getAsyncResponse["SelectedSector"]["WinType"] == 7:
                        print2("Select Card in bonus game")
                        tokenAsync = api.SelectCardBonusGame(regToken, ResultId, SpinId, BonusGameId)
                        getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                # logger
                if getAsyncResponse["ThrowsLeft"] <= 0:
                    totalWinsBG += getAsyncResponse["WinInfo"]["CurrentSpinWin"] + updatedCurrentSpin
                    winsBG_for_update = getAsyncResponse["WinInfo"]["CurrentSpinWin"]
                    print2(f'Bonus game winnings = {getAsyncResponse["WinInfo"]["CurrentSpinWin"] + updatedCurrentSpin}')
            print2('Игру восстановили, проверяем на бонусную после стрелки')

            if updatedSpinResult is not None and updatedSpinResult["DiceGame"] is not None:
                print2('Бонусная игра запустилась после стрелки!!!!!!!!!!!!!!!')
                Info = "true"
                ResultId = ResultId_Update
                SpinId = updatedSpinResult["Id"]
                BonusGameId = updatedSpinResult["DiceGame"]["Id"]

                tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                print2("Bonus game started")

                while getAsyncResponse["ThrowsLeft"] > 0:
                    Info = "false"
                    tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    # check there is in the bonus game, the card game
                    if getAsyncResponse["SelectedSector"]["WinType"] == 7:
                        print2("Select Card in bonus game")
                        tokenAsync = api.SelectCardBonusGame(regToken, ResultId, SpinId, BonusGameId)
                        getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    # logger
                    if getAsyncResponse["ThrowsLeft"] <= 0:
                        totalWinsBG = totalWinsBG + getAsyncResponse["WinInfo"]["CurrentSpinWin"] - winsBG_for_update
                        winsBG_for_update = 0
                        print2(f'Bonus game winnings = {getAsyncResponse["WinInfo"]["CurrentSpinWin"]}')
            # check for FreeSpins and run after resume Game
            print2('Игру восстановили, проверяем на фриспины')
            if getAsyncResponse["FreeSpinsCount"] > 0:
                print2('Игру восстановили, запускаем фриспины')
                ResultId = getAsyncResponse["ResultId"]
                SpinId = getAsyncResponse["SpinResult"]["Id"]

                while getAsyncResponse["FreeSpinsCount"] > 0:
                    print2('запускаем фриспины после Resume Game')
                    print2(getAsyncResponse["FreeSpinsCount"])

                    tokenAsync = api.FreeSpin(regToken, ResultId, SpinId)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                    SpinId = getAsyncResponse["SpinResult"]["Id"]
                    # logger
                    if getAsyncResponse["UpdatedSpinResult"] is not None:
                        totalWinsFS += getAsyncResponse["UpdatedSpinResult"]["WinCoins"]
                        spinWinsFS += getAsyncResponse["UpdatedSpinResult"]["WinCoins"]
                    totalWinsFS += getAsyncResponse["WinInfo"]["CurrentSpinWin"]
                    spinWinsFS += getAsyncResponse["WinInfo"]["CurrentSpinWin"]
                    print2(f'Free Spin = {spinWinsFS}')
                print2(f'The amount of winnings for free spins = {spinWinsFS}')
                spinWinsFS = 0





        # set the number of spins (spins)
        while i < rounds:
            print2('\n')
            print2('spin # %s' % str(i + 1))
            tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
            getAsyncResponse = api.GetAsyncResponse(
                regToken, tokenAsync)
            totalBets += getAsyncResponse["BetSum"]
            updatedSpinResult = getAsyncResponse['UpdatedSpinResult']
            ResultId_Update = getAsyncResponse["ResultId"]
            updatedCurrentSpin = 0



            # check if there is a bonus game
            if getAsyncResponse["SpinResult"]["DiceGame"] is not None:
                Info = "true"
                ResultId = getAsyncResponse["ResultId"]
                SpinId = getAsyncResponse["SpinResult"]["Id"]
                BonusGameId = getAsyncResponse["SpinResult"]["DiceGame"]["Id"]
                if updatedSpinResult is not None and updatedSpinResult["DiceGame"] is None:
                    print2('начисление выигрыша за updated spin после бонусной игры')
                    print2('\n')
                    updatedCurrentSpin = updatedSpinResult["WinCoins"]
                    print2(f'updatedSpinResult = {updatedSpinResult}')

                tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                print2("Bonus game started")



                while getAsyncResponse["ThrowsLeft"] > 0:
                    Info = "false"
                    tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    # check there is in the bonus game, the card game
                    if getAsyncResponse["SelectedSector"]["WinType"] == 7:
                        print2("Select Card in bonus game")
                        tokenAsync = api.SelectCardBonusGame(regToken, ResultId, SpinId, BonusGameId)
                        getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    #logger
                    if getAsyncResponse["ThrowsLeft"] <= 0:
                        totalWinsBG += getAsyncResponse["WinInfo"]["CurrentSpinWin"] + updatedCurrentSpin
                        winsBG_for_update = getAsyncResponse["WinInfo"]["CurrentSpinWin"]
                        print2(f'Bonus game winnings = {getAsyncResponse["WinInfo"]["CurrentSpinWin"] + updatedCurrentSpin}')

            if updatedSpinResult is not None and updatedSpinResult["DiceGame"] is not None:
                print2('Бонусная игра запустилась после стрелки!!!!!!!!!!!!!!!')
                Info = "true"
                ResultId = ResultId_Update
                SpinId = updatedSpinResult["Id"]
                BonusGameId = updatedSpinResult["DiceGame"]["Id"]

                tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                print2("Bonus game started")

                while getAsyncResponse["ThrowsLeft"] > 0:
                    Info = "false"
                    tokenAsync = api.DiceBonusGame(regToken, ResultId, SpinId, BonusGameId, Info)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    # check there is in the bonus game, the card game
                    if getAsyncResponse["SelectedSector"]["WinType"] == 7:
                        print2("Select Card in bonus game")
                        tokenAsync = api.SelectCardBonusGame(regToken, ResultId, SpinId, BonusGameId)
                        getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                    # logger
                    if getAsyncResponse["ThrowsLeft"] <= 0:
                        print2('\n')
                        print2(f'winsBG_for_update = {winsBG_for_update}')
                        print2('\n')
                        totalWinsBG = totalWinsBG + getAsyncResponse["WinInfo"]["CurrentSpinWin"] - winsBG_for_update
                        winsBG_for_update = 0
                        print2(f'Bonus game winnings = {getAsyncResponse["WinInfo"]["CurrentSpinWin"]}')


            # check for FreeSpins and run with a 50% probability
            if "UpdatedSpinResult" in getAsyncResponse and \
                    getAsyncResponse["LooseChainLength"] >= 4 and randint(1, 10) > 5\
                    and getAsyncResponse["UpdatedSpinResult"] is None:
                ResultId = getAsyncResponse["ResultId"]
                SpinId = getAsyncResponse["SpinResult"]["Id"]
                BonusGameId = getAsyncResponse["SpinResult"]["StartFreeSpinBonusGame"]["Id"]

                tokenAsync = api.StartFreeSpinBonusGame(regToken, ResultId, SpinId, BonusGameId)
                getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)

                while getAsyncResponse["FreeSpinsCount"] > 0:
                    print2(f' Количетсво фриспинов = {getAsyncResponse["FreeSpinsCount"]}')
                    tokenAsync = api.FreeSpin(regToken, ResultId, SpinId)
                    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)
                    SpinId = getAsyncResponse["SpinResult"]["Id"]
                    #logger
                    if getAsyncResponse["UpdatedSpinResult"] is not None:
                        totalWinsFS += getAsyncResponse["UpdatedSpinResult"]["WinCoins"]
                        spinWinsFS += getAsyncResponse["UpdatedSpinResult"]["WinCoins"]
                    totalWinsFS += getAsyncResponse["WinInfo"]["CurrentSpinWin"]
                    spinWinsFS += getAsyncResponse["WinInfo"]["CurrentSpinWin"]
                    print2(f'Free Spin = {spinWinsFS}')
                print2(f'The amount of winnings for free spins = {spinWinsFS}')
                spinWinsFS = 0


            else:
                totalWins += getAsyncResponse["WinInfo"]["TotalWin"]
                print2(f'Win for spin {getAsyncResponse["WinInfo"]["TotalWin"]}')
                print2(f'Total winnings {totalWins + totalWinsBG + totalWinsFS}')

            i = i + 1
        print2('\n')
        print2('finished Crazy Scientist session after %s spins' % i)
        global_count_spin += i
        i = 0
        GlobalTotalBets += totalBets
        totalWins = totalWins + totalWinsBG + totalWinsFS
        GlobalTotalWins += totalWins
        GlobalTotalWinsFS += totalWinsFS
        GlobalTotalWinsBG += totalWinsBG


        print2(f'Total Bets = {totalBets}')
        totalBets = 0
        print2(f'Total Wins = {totalWins}')
        totalWins = 0
        print2(f'Total Wins in free spins = {totalWinsFS}')
        totalWinsFS = 0
        print2(f'Total Wins in Bonus Game = {totalWinsBG}')
        totalWinsBG = 0
        print2('the end session')


        r = r + 1


    print2('\n')
    print2(f'finished Crazy Scientist after {r} rounds and {global_count_spin} sessions')
    print2('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
    print2(f'Total Bets = {GlobalTotalBets}')
    print2(f'Total Wins = {GlobalTotalWins}')
    print2(f'Total Wins in free spins = {GlobalTotalWinsFS}')
    print2(f'Total Wins in Bonus Game = {GlobalTotalWinsBG}')
    print2('the end session')

    token_bot = 'A7IyBs7bnC7BtH4xGPEp9Q5mkMj6QOoR'
    id_bot = 72220000233
    id_chat = 322776
    text_bot = f'Тест закончен \n Количество сессий = {r} \n Количество спинов = {global_count_spin} \n' \
               f' Общая сумма ставок = {GlobalTotalBets} \n Общая сумма выигрыша = {GlobalTotalWins} \n' \
               f'RTP = {GlobalTotalWins/GlobalTotalBets * 100}'

    def send_message(text):
        url = F"https://bot.reddy.team/bot{token_bot}/send?chat={id_chat}&msg={text_bot}"
        response = requests.get(url)
        print2(response)
        print2('Сообщение отправлено')
    send_message(text_bot)



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    setRTP = RTP(users, rtp)
    currentRTP = setRTP.setRTP()

    for i in range(len(currentRTP[1])):
        currentRTP[2][i] = threading.Thread(target=fs, args=(currentRTP[2][i],))
        currentRTP[2][i].start()

