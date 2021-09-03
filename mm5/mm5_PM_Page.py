import hashlib
import json
import time
import unittest

import pytest
import requests

from Locators import APIdata_PortalMaster

A = APIdata_PortalMaster

def write_data_to_json_file(f, target_data):
    """
    : Функция записывает массив target_data в файл 'f' в формате JSON
    :output example : 'test 12-03-2021 14-57-37.json'
    :param f: test
    :param target_data: json.dumps(getAsyncResponse, indent=2)
    :example: write_data_to_json_file('test', getAsyncResponse)
    :www source: https://stackoverflow.com/questions/9170288/pretty-print-json-data-to-a-file-using-python
    """
    import datetime
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(json.dumps(target_data, indent=2))  # записываем файл
    file.close()  # закрываем файл


class Reddy:
    def __init__(self, toReddy=False, gameLine=''):
        self.toReddy = toReddy
        self.gameLine = gameLine
        self.token_bot = 'BGCcKgM79OMwRAJe-hWkZwpsRaIJ0-xx'
        self.id_bot = 72220000235

        if self.gameLine == 'mm5':
            self.reddy_id_chat = 324537
        if self.gameLine == 'mm6':
            self.reddy_id_chat = 323826
        if self.gameLine == 'mm7':
            self.reddy_id_chat = 324386
        else:
            pass

        return

    def send_message2reddy(self, text_bot):
        if self.toReddy:
            url = F"https://bot.reddy.team/bot{self.token_bot}/send?chat={self.reddy_id_chat}&msg={text_bot}"
            response = requests.get(url)
            print(f'Было отправлено сообщение в Reddy. HTTP: {response}')


class ScatterCrystalActionType:
    Trade = '0'
    Replace = '1'
    Finish = '2'

class LevelSphere:
    First = '1'
    Second = '2'

class API_PortalMaster:

    @staticmethod
    def tps(userID):
        params = {'gameURL': A.gameURL, 'frontURL': A.frontURL, 'partnerURL': A.partnerURL, 'partnerId': A.partnerID,
                  'gameID': A.gameID, 'userID': userID, 'currency': A.currency}
        response = requests.get(A.DOMAIN_tps, params=params, headers={'Connection': 'close'})
        # print(response)
        print(params)
        assert response.status_code == 200
        regToken = response.text.split("token=")[1].split("&")[0]
        print('game_%s_IframeUrl = ' % A.gameID, response.text)
        print('game_%s_regToken = ' % A.gameID, regToken)
        return regToken

    @staticmethod
    def testpartnerservice():
        params = {'gameURL': A.gameURL, 'frontURL': A.frontURL, 'partnerURL': A.partnerURL, 'partnerId': A.partnerID,
                  'gameID': A.gameID, 'userID': A.userID, 'currency': A.currency}
        response = requests.get(A.DOMAIN_tps, params=params, headers={'Connection': 'close'})
        # print(response)
        print(params)
        assert response.status_code == 200
        regToken = response.text.split("token=")[1].split("&")[0]
        print('game_%s_IframeUrl = ' % A.gameID, response.text)
        print('game_%s_regToken = ' % A.gameID, regToken)
        return regToken

    @staticmethod
    def AuthorizationGame(RegToken):
        """
        возвращает параметры: response, balance, balanceReal, coin, currency, printAG
        'response' =
        'balance' =
        'balanceReal' =
        'coin' =
        'currency' =
        'printAG' = function
         """
        HASH = hashlib.md5(('AuthorizationGame/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        params_AuthorizationGame = {'Hash': HASH, 'Token': RegToken, 'MobilePlatform': 'false'}
        response_AuthorizationGame = requests.post(A.DOMAIN + '/auth/AuthorizationGame',
                                                   params={'Hash': HASH, 'Token': RegToken,
                                                           'MobilePlatform': 'false'},
                                                   json=params_AuthorizationGame, headers={'Connection': 'close'})
        response = response_AuthorizationGame.json()
        assert response_AuthorizationGame.status_code == 200
        print(response)
        balance = response["Balance"]
        balanceReal = response["BalanceReal"]
        coin = response["Coin"]
        currency = response["Currency"]

        def printAG(*b):
            # print('\n')
            print("Balance = %s, Balance Real = %s, Coin = %s, Currency = %s" % b)
            print(
                '---------------------------------------------------------------------------------------------------------')

        return response, balance, balanceReal, coin, currency, printAG

    @staticmethod
    def GetSlotInfo(RegToken):
        HASH = hashlib.md5(('GetSlotInfo/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        params_GetSlotInfo = {'Hash': HASH, 'Token': RegToken}
        response_GetSlotInfo = requests.post(A.DOMAIN + '/games/GetSlotInfo',
                                             params={'Hash': HASH, 'Token': RegToken}, json=params_GetSlotInfo, headers={'Connection': 'close'})
        response = response_GetSlotInfo.json()
        assert response_GetSlotInfo.status_code == 200
        return response

    @staticmethod
    def CreditDebit(RegToken, betSum=A.betSum, cntLineBet=A.cntLineBet):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(('CreditDebit/' + RegToken + betSum + cntLineBet + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_CreditDebit = ', HASH)
        params_CreditDebit = {'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                              'BetSum': betSum}
        response_CreditDebit = requests.post(A.DOMAIN + '/games/CreditDebit',
                                             params={'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                                                     'BetSum': betSum}, json=params_CreditDebit, headers={'Connection': 'close'})
        response = response_CreditDebit.json()
        assert response_CreditDebit.status_code == 200
        tokenAsync = response["TokenAsync"]
        # print(response)
        print('CreditDebit_TokenAsync = ', response['TokenAsync'])
        # response_CreditDebit.close()
        return response, tokenAsync

    @staticmethod
    def GetAsyncResponse(RegToken, TokenAsync):
        """
        возвращает параметры: response, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace
        'response' =
        'ResultId' = jsonData.ResultId
        'SpinId' = jsonData.SpinResult.Id
        'scatterCrystalGame' =
        'spheres' =
        'spheresSpinId' =
        'scattersForReplace' =
         """
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsync + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponse = ', HASH)
        params_GetAsyncResponse = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync}
        response_GetAsyncResponse = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                  params={'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync},
                                                  json=params_GetAsyncResponse, headers={'Connection': 'close'})
        response = response_GetAsyncResponse.json()
        # print('GetAsyncResponse = ', response)
        assert response_GetAsyncResponse.status_code == 200
        while "Error" in response:
            time.sleep(500 / 1000)
            response_GetAsyncResponse = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                      params={'Hash': HASH, 'Token': RegToken,
                                                              'TokenAsync': TokenAsync}, json=params_GetAsyncResponse, headers={'Connection': 'close'})
            response = response_GetAsyncResponse.json()
        else:
            resultId = response['ResultId']
            spinId = response["SpinResult"]["Id"]
            print("Response =", response)
            print("ResultId =", resultId)
            print("SpinId =", spinId)
            if response["SpinResult"]["ScatterCrystalGame"]["Id"] is None:
                scatterCrystalGame = response["SpinResult"]["ScatterCrystalGame"]["Id"]
                spheres = 0
                spheresSpinId = 0
                scattersForReplace = 0
            else:
                scatterCrystalGame = response["SpinResult"]["ScatterCrystalGame"]["Id"]
                spheres = response["SpinResult"]["ScatterCrystalGame"]["Spheres"]
                spheresSpinId = response["SpinResult"]["ScatterCrystalGame"]["SpinId"]
                scattersForReplace = response["SpinResult"]["ScatterCrystalGame"]["ScattersForReplace"]

        def printAR(coin):
            betSum = response["BetSum"]
            totalWin = response["WinInfo"]["TotalWin"]
            balance = response["WinInfo"]["Balance"]
            balance_before_spin = (balance - totalWin + betSum) * coin
            balance_after_spin = balance * coin
            # print('\n')
            print("BetSum = %s, TotalWin = %s, BalanceBeforeSpin = %s, BalanceAfterSpin = %s" % (
                betSum, totalWin, balance_before_spin, balance_after_spin))
            print(
                '---------------------------------------------------------------------------------------------------------')

        # response_GetAsyncResponse.close()
        return response, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace, printAR

    @staticmethod
    def ScatterCrystalBonusGame(RegToken, ResultId, BonusGameId, SpinId, ActionType, ScatterPositionRow,
                                ScatterPositionColumn, LevelSphere, Info):
        """
        Trade : ActionType = 0
        Replace : ActionType = 1
        Finish : ActionType = 2
        For example when actionType is Finish, ScatterPosition.Row = 0, ScatterPosition.Column = 0, LevelSphere = 0 (-1)
         """
        HASH = hashlib.md5(
            ('ScatterCrystalBonusGame/' + RegToken + ResultId + SpinId + BonusGameId + ActionType +
             ScatterPositionRow + ScatterPositionColumn + LevelSphere + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_ScatterCrystalBonusGame = ', HASH)
        params_ScatterCrystalBonusGame = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                          "BonusGameId": BonusGameId, "SpinId": SpinId, "ActionType": ActionType,
                                          "ScatterPosition": {"Row": ScatterPositionRow,
                                                              "Column": ScatterPositionColumn},
                                          "LevelSphere": LevelSphere, "Info": Info}
        # print('params = ', params_ScatterCrystalBonusGame)
        response_ScatterCrystalBonusGame = requests.post(A.DOMAIN + '/bonus/ScatterCrystalBonusGame',
                                                         params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                                 "BonusGameId": BonusGameId, "SpinId": SpinId,
                                                                 "ActionType": ActionType,
                                                                 "ScatterPosition": {"Row": ScatterPositionRow,
                                                                                     "Column": ScatterPositionColumn},
                                                                 "LevelSphere": LevelSphere, "Info": Info},
                                                         json=params_ScatterCrystalBonusGame, headers={'Connection': 'close'})
        response = response_ScatterCrystalBonusGame.json()
        assert response_ScatterCrystalBonusGame.status_code == 200
        url = response_ScatterCrystalBonusGame.url
        # print("Response =", response)
        tokenAsyncScatter = response['TokenAsync']
        print('ScatterCrystalBonusGame_TokenAsync = ', tokenAsyncScatter)
        # response_ScatterCrystalBonusGame.close()
        return response, tokenAsyncScatter

    @staticmethod
    def GetAsyncResponse_Scatter(RegToken, TokenAsyncScatter):
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsyncScatter + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseScatter = ', HASH)
        params_GetAsyncResponse_Scatter = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsyncScatter}
        print('params = ', params_GetAsyncResponse_Scatter)
        response_GetAsyncResponse_Scatter = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                          params={'Hash': HASH, 'Token': RegToken,
                                                                  'TokenAsync': TokenAsyncScatter},
                                                          json=params_GetAsyncResponse_Scatter, headers={'Connection': 'close'})
        response = response_GetAsyncResponse_Scatter.json()
        print('GetAsyncResponse_Scatter = ', response)
        assert response_GetAsyncResponse_Scatter.status_code == 200
        while "Error" in response:
            # print('time waiting ...')
            # time.sleep(1)
            time.sleep(500 / 1000)
            response_GetAsyncResponse_Scatter = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                              params={'Hash': HASH, 'Token': RegToken,
                                                                      'TokenAsync': TokenAsyncScatter},
                                                              json=params_GetAsyncResponse_Scatter, headers={'Connection': 'close'})
            response = response_GetAsyncResponse_Scatter.json()
        else:
            print("Response =", response)
            freeSpinCount = response["FreeSpinCount"]
            print("FreeSpinCount = ", freeSpinCount)
            pass
        # response_GetAsyncResponse_Scatter.close()
        return response, freeSpinCount

    @staticmethod
    def FreeSpin(RegToken, ResultId, SpinId):
        """
        RegToken :
        ResultId :
        SpinId :
         """
        HASH = hashlib.md5(('FreeSpin/' + RegToken + ResultId + SpinId + A.gameKey).encode('utf-8')).hexdigest()
        print('\n')
        print('hash_FreeSpin = ', HASH)
        params_FreeSpin = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId, "SpinId": SpinId}
        print('params freeSpin= ', params_FreeSpin)
        response_FreeSpin = requests.post(A.DOMAIN + '/games/FreeSpin',
                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                  "SpinId": SpinId}, json=params_FreeSpin, headers={'Connection': 'close'})
        response = response_FreeSpin.json()
        assert response_FreeSpin.status_code == 200
        url = response_FreeSpin.url
        # print("Response =", response)
        tokenAsyncFreeSpin = response['TokenAsync']
        print('FreeSpin_TokenAsync = ', tokenAsyncFreeSpin)
        response_FreeSpin.close()
        return response, tokenAsyncFreeSpin

    @staticmethod
    def GetAsyncResponse_FreeSpin(RegToken, TokenAsyncFreeSpin):
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsyncFreeSpin + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseFreeSpin = ', HASH)
        params_GetAsyncResponse_FreeSpin = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsyncFreeSpin}
        print('params getAsyncResponse_FreeSpin= ', params_GetAsyncResponse_FreeSpin)
        response_GetAsyncResponse_FreeSpin = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                           params={'Hash': HASH, 'Token': RegToken,
                                                                   'TokenAsync': TokenAsyncFreeSpin},
                                                           json=params_GetAsyncResponse_FreeSpin, headers={'Connection': 'close'})
        response = response_GetAsyncResponse_FreeSpin.json()
        print('GetAsyncResponse_FreeSpin = ', response)
        assert response_GetAsyncResponse_FreeSpin.status_code == 200
        while "Error" in response:
            time.sleep(500 / 1000)
            response_GetAsyncResponse_FreeSpin = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                               params={'Hash': HASH, 'Token': RegToken,
                                                                       'TokenAsync': TokenAsyncFreeSpin},
                                                               json=params_GetAsyncResponse_FreeSpin, headers={'Connection': 'close'})
            response = response_GetAsyncResponse_FreeSpin.json()
        else:
            spinIdFs = response['SpinResult']['Id']
            print('spinIdFs = ', spinIdFs)
            print("Response =", response)
            freeSpinsCount = response["FreeSpinsCount"]
            print("FreeSpinsCount = ", freeSpinsCount)
        response_GetAsyncResponse_FreeSpin.close()
        return response, freeSpinsCount, spinIdFs
