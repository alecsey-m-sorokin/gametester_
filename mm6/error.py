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
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--rtp', type=int, default=A.partnerID_rtp_120)
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
    rtp = A.partnerID_rtp_120


# def thread_function(ids):
#     print(f'\nuserId # {ids}')
#     regToken = api.tps(ids, rtp)
#     logging.info(f'Thread {ids}: starting')
#     time.sleep(2)
#     logging.info(f'Thread {ids}: finishing')

r = 0
i = 0

def fs2(ids):
    # return fs(ids)

    while True:
        try:
            return fs(ids)
        except Exception as e:
            print(f'/ userId # {ids} =================== Errrrrooooooooooooooooooorrrrrrr ===================', e)

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

    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))

    while r < sessions:  # выставляем количество раундов (сессий)
        fileName = 'logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
        log = Logger(fileName, toFile=False, toConsole=True)
        print2 = log.printml
        print2('\n')
        print2('round # %s' % str(r + 1))
        regToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2Mjg3MTY0MDQsImV4cCI6MTYyODcxODIwNCwiaXNzIjoiaHR0cDovL2lkZW50aXR5c2VydmVyLmNhcmhlbmdlLnNwYWNlIiwiY2xpZW50X2lkIjoiUGFydG5lclNlcnZpY2UiLCJTZXNzaW9uSWRlbnRpdHkiOiIyeWFyL2lUeDhqNzQ5dVBibkJybEZZSEhmSTM3TGpVRzNEWXZFWE93clUwSFVsRy9NOE1xeXQ5VktCbkpCTWZ4M0YzMXNBVDdtSit3WUdBd2lMWmRtRmk5VTZMRGw3N3l1cERRK25HTHptSm5uc05SUjZ6UjBLUGFNWkw3dGZPUHlpSU5qT0NmUWRFS3dtZENtUytkbDVWaUk1WjNyR2poL0pSd0NNNkNza25HOTNWT3g5VDgzSzRiTm5ZendaWFFUSHBMTjl4NTNJaWI0dFpuNXlOdDdXUnA2cCthTWZFM2F3RFE0SEVhaEhydHRYa2k2UFdmb2FNaFcrcW5jMHlKWVpGZ1grUGtISUk0L2N0eVI0YVg2bjlsT044Q3RXalBMVUVQYWxWa3hoTXQrVktGdVFJdGtGYmE0Sm1aemlISGxqS3YyZmgwUlYzUzZQTnlPWDNYekR4L0lYaWN0U1l1UmFhY01zTWpmTnpHRDF4V1UvVmV5d1lLTzZnZW9nVEpRYlBHcEkwK2xlZXVHL241Rk1uaUVzOWU1eTkzbHZMSHZlclpuaVUvYUF2UFU5WlNzYUpMSU9OTDAxanBFdk0wSGJSWUFwL2lLSy8xTEo5djVOYWpnbExOTjlsb3JtNi82UklqRXhHbVRybzdrYWFXcW9DOGtSZVMxWkIxTjVKYzN4R2hUUC92YTUxMmptNUNHdmpLeUVKOVJ2emRQcXVLV3RQWlo5OW1LYW41ZC9NTkR4U3podVJBbjgxSEhFc1VMUEdlVklrRWRhcjVUZ1NJL0NlbUw5bFNrWlVXVU5TbFhqK05tR2hhbWgxSXl1dkt4cXl2NU8wajNWWklWcG1jOHprbWRjWThTZ1VXZ2xGWm5EQ0RTdjhoLzMzNXRoZ1U1S093cmVqdW1IckIrSTdHZW54NENTOWxRZ1Y3RGI4VnNjWi9QYm9rRkNXVGU3Z3AvUzhTOFcvNjcrZDFnV3BQQlJBdUx1Yll5dFhsbGNTWWNydEVtQ2xVemdEcFRubVhTYnFXalZEVXo1Tld1blczdzE2aUZSVG05RGxBdlZZNzZnWkF6YmNDOWRIa2hyRWUvRnRRcFVxTDdOQW1OMXoraHY3WmpXMzlIQVMvTmU0aC9vMjJNTDNuNDZNSWZ3WmZDMURsRktlelNPZz0iLCJHYW1lSWQiOiIxOTAwMSIsIlNsb3RUeXBlIjoiMTkiLCJHYW1lU2VydmljZVVybCI6Imh0dHBzOi8vdGVzdC1tbTZuLWFwaS5jYXJoZW5nZS5zcGFjZS8iLCJHYW1lVXJsIjoiaHR0cHM6Ly9zdGVzdC56aGR1bi5zcGFjZS9tbTZuLyIsImp0aSI6IkRERkM3NjEwNUQ5ODI5NDk0RUFFRDEzOEUyNEQ5QUNEIiwiaWF0IjoxNjI4NzE2NDA0LCJzY29wZSI6WyJHZW5lcmF0ZUp3dFRva2VuIl19.y2iaHWqEFg9fhmiuXDLY7_aEMiDfSc5RwditoasNcZre1qcuehA5P5nmLH5glZMjCOfqCukElNv1ZnuYuB3jYnPpiK_tNIwdaDg6WA6R6nmIs2y3e93BhJdhDRaR1kOhoZxQRO-3526emDbIwNexI9CKUu9-wAjY9xTfgCEgAl0D7-77AShHaRNioq-iIbs_YJ4y50MUyU8mLUibY15uCU06YJnZsjDMIQwdA61n1KMUEOkQXzUZfgp4MRJVtFXY9eKxCpyJ58Nc_8NLaOdbUmR4Z29AHz-GDdW3p4rH7kcXo3KEQzVApiO3FQaIPg1JgW1JJlzRyVTPQ4MQTZz4GO5JwxbpCoLgoeuOe2HLZa3KRp6qaJgMtpTAoXhFeY9kL3Jm-bce27bVW_WNqN_txjgCAKsG4W_pBdRmyq6GX2y5vFYuML-QSbeZ4UZHVsTL3BgxhydubshvQ2f_tz1hYVgC0o1BTCI5i8nRCBm33CJnrUjoZByuIxsE_7QJFxeluHeiKqWOAzsdGxh5dDaWSJx64v6HYR8IBQl57jQXKEwNZL1wbalHuflHYsexjjnPr-zaBDdcg4hL9sB5bORHnfQffOMbq9r4nDjfsAdsxiElQlvG2xnXqUTptEizN9GPO06YaSv6Ew0Ed1k74T6P25x2BssNam3Q-OJnB7nEZrs'
        HH = '0814095ca80f5f8701b27c33490683bf'
        regToken = api.tps(ids, rtp)
        # logging.info(f'Thread {ids}: starting')
        # regToken = regToken[0]
        authorizationGame, balance, balanceReal, coin, currency, resultId, func = api.AuthorizationGame(regToken)
        print2(str(authorizationGame))
        balanceRealBefore = balanceReal
        func(balance, balanceReal, coin, currency, resultId)

        while i < rounds:  # выставляем количество спинов (вращений)
            print2(f'\nspin #  {str(i + 1)}  / session # {str(r + 1)}  / userId # {ids}')
            creditDebit, timeOut, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
            # creditDebit, timeOut, tokenAsync = api.CreditDebitError(regToken, HH, A.betSum, A.cntLineBet)
            getAsyncResponse, resultId, spinId, totalFreeSpinsCount, remainingFreeSpinsCount, printAR, bonusGameResult = api.GetAsyncResponse(regToken, timeOut, tokenAsync)
            print2(str(getAsyncResponse))
            printAR(coin)

            i = i + 1
            totalBets.append(getAsyncResponse["BetSum"])
            totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
            printAR(coin)

        r = r + 1

        print2('\n')
        print2('finished "Mancala Quest" session after %s spins' % i)
        print2('userId =', ids)
        i = 0


if __name__ == "__main__":

    setRTP = RTP(users, rtp)
    currentRTP = setRTP.setRTP()

    for i in range(len(currentRTP[1])):
        currentRTP[2][i] = threading.Thread(target=fs, args=(currentRTP[2][i],))
        currentRTP[2][i].start()
