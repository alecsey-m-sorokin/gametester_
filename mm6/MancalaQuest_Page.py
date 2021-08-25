import hashlib
import json
import time
import unittest
import pytest
import requests
from Locators import APIdata_MancalaQuest, ErrorCodes

A = APIdata_MancalaQuest
E = ErrorCodes


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


def print2file(f, target_data):
    import datetime
    # dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(target_data)  # записываем файл
    file.write('\n')
    file.close()  # закрываем файл


def findall(v, k):
    """
    : рекурсивный поиск - найти конкретное значение JSON по ключу
    :param v: где ищем
    :param k: что ищем
    :return: results = findall(data, "WinStateInfo")
    with open('c:/testing/response2.json') as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)
    """
    if type(v) == type({}):
        for k1 in v:
            if k1 == k:
                print(v[k1])
                return v[k1]
            result = findall(v[k1], k)
            if result is not None:
                return result

    if type(v) == type([]):
        for k1 in v:
            result = findall(k1, k)
            if result is not None:
                return result


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


class Logger(object):

    def __init__(self, fileName='', toFile=False, toConsole=False):
        self.fileName = fileName
        self.toFile = toFile
        self.toConsole = toConsole
        return

    def printml(self, *args):
        aa = []
        toprint = ''
        for v in args:
            aa.append(str(v))
            toprint = toprint + str(v) + ' '
        if self.toFile and self.toConsole:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
                print(aa[a])
                # print('\n')
            f.close()
        elif self.toFile:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
            f.close()
        elif self.toConsole:
            for a in range(len(aa)):
                print(aa[a])
        else:
            pass
        return


class RTP:

    def __init__(self, userCount=0, currentRTP=0):
        self.userCount = userCount
        self.currentRTP = currentRTP

        if self.currentRTP == 90:
            self.start_users_rtp = A.start_users_rtp_90
        if self.currentRTP == 95:
            self.start_users_rtp = A.start_users_rtp_95
        if self.currentRTP == 120:
            self.start_users_rtp = A.start_users_rtp_120
        else:
            self.start_users_rtp = A.start_users_rtp_95

        return

    def setRTP(self):
        rtp_user_count = self.userCount
        rtp_user_range = range(self.start_users_rtp, self.start_users_rtp + rtp_user_count)
        rtp_user_list = []

        for xxx in range(len(rtp_user_range)):
            rtp_user_list.append(rtp_user_range[xxx])

        return rtp_user_count, rtp_user_range, rtp_user_list


class API_MancalaQuest:

    @staticmethod
    def tps(userID, rtp):
        params = {'gameURL': A.gameURL, 'frontURL': A.frontURL, 'partnerURL': A.partnerURL,
                  'partnerId': rtp,
                  'gameID': A.gameID, 'userID': userID, 'currency': A.currency}
        response = requests.get(A.DOMAIN_tps, params=params, headers={'Connection': 'close'})
        # print(response)
        print('params = ', params)
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
        print('params = ', params)
        assert response.status_code == 200
        print('response status code =', response.status_code)
        print('url = ', response.url)
        regToken = response.text.split("token=")[1].split("&")[0]
        iFrameUrl = response.text
        print('game_%s_IframeUrl = ' % A.gameID, response.text)
        print('game_%s_regToken = ' % A.gameID, regToken)
        return regToken, iFrameUrl

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
        print('hash_AuthorizationGame = ', HASH)
        params_AuthorizationGame = {'Hash': HASH, 'Token': RegToken, 'MobilePlatform': 'false'}
        response_AuthorizationGame = requests.post(A.gameURL + A.AuthorizationGame_Url,
                                                   params={'Hash': HASH, 'Token': RegToken,
                                                           'MobilePlatform': 'false'},
                                                   json=params_AuthorizationGame, headers={'Connection': 'close'})
        print('response_AuthorizationGame = ', response_AuthorizationGame)
        response = response_AuthorizationGame.json()
        assert response_AuthorizationGame.status_code == 200
        print("Response =", response)
        # url = response_AuthorizationGame.url
        balance = response["Balance"]
        balanceReal = response["BalanceReal"]
        coin = response["Coin"]
        currency = response["Currency"]
        resultId = response["ResultId"]
        print('ResultId = ', resultId)

        def printAG(*b):
            # print('\n')
            print("Balance = %s, Balance Real = %s, Coin = %s, Currency = %s, ResultId = %s" % b)
            print('--------------------------------------------------------------------------------------------------')

        return response, balance, balanceReal, coin, currency, resultId, printAG

    @staticmethod
    def ResumeGame(RegToken, ResultId):
        """
        возвращает параметры: response, timeOut, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(('ResumeGame/' + RegToken + ResultId + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_ResumeGame = ', HASH)
        params_ResumeGame = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId}
        response_ResumeGame = requests.post(A.gameURL + A.ResumeGame_Url,
                                            params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId},
                                            json=params_ResumeGame,
                                            headers={'Connection': 'close'})
        response = response_ResumeGame.json()
        print('params_ResumeGame = ', params_ResumeGame)
        print('response = ', response)
        assert response_ResumeGame.status_code == 200
        timeOut = response["Timeout"]
        tokenAsyncResumeGame = response["TokenAsync"]
        print('ResumeGame_TokenAsync = ', response['TokenAsync'])
        # response_ResumeGame.close()
        return response, timeOut, tokenAsyncResumeGame

    @staticmethod
    def GetSlotInfo(RegToken):
        HASH = hashlib.md5(('GetSlotInfo/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        params_GetSlotInfo = {'Hash': HASH, 'Token': RegToken}
        response_GetSlotInfo = requests.post(A.gameURL + A.GetSlotInfo_Url,
                                             params={'Hash': HASH, 'Token': RegToken}, json=params_GetSlotInfo,
                                             headers={'Connection': 'close'})
        response = response_GetSlotInfo.json()
        assert response_GetSlotInfo.status_code == 200
        return response

    @staticmethod
    def CreditDebitError(RegToken, HH, betSum=A.betSum, cntLineBet=A.cntLineBet):
        """
        возвращает параметры: response, timeOut, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(('CreditDebit/' + RegToken + betSum + cntLineBet + A.gameKey).encode('utf-8')).hexdigest()
        print('--- CreditDebit : ---------------------------------------------------------------------------------------')
        print('hash_CreditDebit = ', HH)
        params_CreditDebit = {'Hash': HH, 'Token': RegToken, 'CntLineBet': cntLineBet, 'BetSum': betSum}
        print('params = ', params_CreditDebit)

        with open('c:/testing/cd_bad.json') as json_file:
            try:
                response = json.load(json_file)
                print('response = ', response)
            except Exception as e:
                print('Exception = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! credit debit = ', e)
                while e:
                    try:
                        print('1')
                        with open('c:/testing/cd_bad.json') as json_file:
                            response = json.load(json_file)
                    except Exception as zzz:
                        print('Exception = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! credit debit bad json = ', zzz)
                else:
                    print('False')

        print('=====')
        # try:
        #     if len(response) == 2:
        #         print('response CD ok= ', response)
        #     else:
        #         while len(response) != 2:
        #             with open('c:/testing/cd_ok.json') as json_file:
        #                 response = json.load(json_file)
        # except Exception as e:
        #     print('Exception = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! credit debit == ', e)
        #
        timeOut = response["Timeout"]
        tokenAsync = response["TokenAsync"]
        print(f'CreditDebit_TimeOut : {timeOut} / CreditDebit_TokenAsync : {tokenAsync}')
        # return response
        return response, timeOut, tokenAsync

    @staticmethod
    def CreditDebit(RegToken, betSum=A.betSum, cntLineBet=A.cntLineBet):
        """
        возвращает параметры: response, timeOut, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(('CreditDebit/' + RegToken + betSum + cntLineBet + A.gameKey).encode('utf-8')).hexdigest()
        print('--- CreditDebit : ---------------------------------------------------------------------------------------')
        print('hash_CreditDebit = ', HASH)
        params_CreditDebit = {'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet, 'BetSum': betSum}
        print('params = ', params_CreditDebit)
        # response = {}
        response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
                                             params={'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                                                     'BetSum': betSum}, json=params_CreditDebit,
                                             headers={'Connection': 'close'})

        # while response_CreditDebit.status_code != 200:
        #     print('BAD response CreditDebit = ', response_CreditDebit)
        #     print('BAD response CreditDebit status code = ', response_CreditDebit.status_code)
        #     print('trying to make CreditDebit request ...')
        #     response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
        #                                          params={'Hash': HASH, 'Token': RegToken,
        #                                                  'CntLineBet': cntLineBet,
        #                                                  'BetSum': betSum}, json=params_CreditDebit,
        #                                          headers={'Connection': 'close'})
        # else:
        #     response = response_CreditDebit.json()
        #     if not response["Timeout"] and not response["TokenAsync"]:
        #         print('Empty JSON')
        #     else:
        #         response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
        #                                              params={'Hash': HASH, 'Token': RegToken,
        #                                                      'CntLineBet': cntLineBet,
        #                                                      'BetSum': betSum}, json=params_CreditDebit,
        #                                              headers={'Connection': 'close'})
        #         response = response_CreditDebit.json()

        while response_CreditDebit.status_code != 200:
            print('trying to make CreditDebit request ...')
            response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
                                                     params={'Hash': HASH, 'Token': RegToken,
                                                             'CntLineBet': cntLineBet,
                                                             'BetSum': betSum}, json=params_CreditDebit,
                                                     headers={'Connection': 'close'})
        else:
            try:
                response = response_CreditDebit.json()
            except Exception as e:
                print('Exception = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! credit debit bad json = ', e)
                while e:
                    try:
                        response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
                                                             params={'Hash': HASH, 'Token': RegToken,
                                                                     'CntLineBet': cntLineBet,
                                                                     'BetSum': betSum}, json=params_CreditDebit,
                                                             headers={'Connection': 'close'})
                        response = response_CreditDebit.json()
                    except Exception as ee:
                        print('Exception = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! credit debit bad json = ', ee)
                else:
                    pass

        print('response = ', response)

        # while response_CreditDebit.status_code != 200:
        #     print('BAD response CreditDebit = ', response_CreditDebit)
        #     print('BAD response CreditDebit status code = ', response_CreditDebit.status_code)
        #     response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
        #                                          params={'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
        #                                                  'BetSum': betSum}, json=params_CreditDebit,
        #                                          headers={'Connection': 'close'})
        # else:
        #     response = response_CreditDebit.json()
        #     try:
        #         if len(response) == 2:
        #             print('response CD ok= ', response)
        #             print('Response_CreditDebit.status = ', response_CreditDebit.status_code)
        #         else:
        #             while len(response) != 2:
        #                 response_CreditDebit = requests.post(A.gameURL + A.CreditDebit_Url,
        #                                                  params={'Hash': HASH, 'Token': RegToken,
        #                                                          'CntLineBet': cntLineBet,
        #                                                          'BetSum': betSum}, json=params_CreditDebit,
        #                                                  headers={'Connection': 'close'})
        #                 response = response_CreditDebit.json()
        #     except Exception as e:
        #         print('Exception = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! credit debit = ', e)
        #         # print2file('CreditDebit error.txt', response_CreditDebit)

        assert response_CreditDebit.status_code == 200
        timeOut = response["Timeout"]
        tokenAsync = response["TokenAsync"]
        print(f'CreditDebit_TimeOut : {timeOut} / CreditDebit_TokenAsync : {tokenAsync}')
        response_CreditDebit.close()
        return response, timeOut, tokenAsync

    @staticmethod
    def GetAsyncResponse(RegToken, TimeOut, TokenAsync):
        """
        возвращает параметры: response, resultId, spinId, StonesNumber, OAKLines, printAR, oak_l
        'response' =
        'ResultId' = jsonData.ResultId
        'SpinId' = jsonData.SpinResult.Id
        'StonesNumber' =
        'OAKLines' =
        'printAR' =
        'oak_l' =
         """
        HASH = hashlib.md5(('GetAsyncResponse/' + RegToken + TokenAsync + A.gameKey).encode('utf-8')).hexdigest()
        print(
            '--- GetAsyncResponse : ----------------------------------------------------------------------------------')
        print('hash_GetAsyncResponse = ', HASH)
        params_GetAsyncResponse = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync}
        print('params = ', params_GetAsyncResponse)
        response_GetAsyncResponse = requests.post(A.gameURL + A.GetAsyncResponse_Url,
                                                  params={'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync},
                                                  json=params_GetAsyncResponse,
                                                  headers={'Connection': 'close'})
        # print('url = ', response_GetAsyncResponse.url)
        response = response_GetAsyncResponse.json()
        # print('GetAsyncResponse = ', response)
        assert response_GetAsyncResponse.status_code == 200
        while "Error" in response:
            if response["Error"] == 13:
                print('GetAsyncResponse = ', response)
                print(f'sleeping ... {TimeOut} ms')
                time.sleep(TimeOut / 1000)
                response_GetAsyncResponse = requests.post(A.gameURL + A.GetAsyncResponse_Url,
                                                          params={'Hash': HASH, 'Token': RegToken,
                                                                  'TokenAsync': TokenAsync},
                                                          json=params_GetAsyncResponse,
                                                          headers={'Connection': 'close'})
                response = response_GetAsyncResponse.json()
            else:
                for key in E.error_codes_dictionary:
                    if response["Error"] == key:
                        print(f'\nScript error: {E.error_codes_dictionary[key]} = {key}', )
                        exit()
        else:
            resultId = response['ResultId']
            spinId = response["SpinResult"]["Id"]
            if response["GameFreeSpins"]:
                totalFreeSpinsCount = response["GameFreeSpins"][0]["TotalFreeSpinsCount"]
                remainingFreeSpinsCount = response["GameFreeSpins"][0]["RemainingFreeSpinsCount"]
            else:
                totalFreeSpinsCount = 0
                remainingFreeSpinsCount = 0
            print("Response =", response)
            print("ResultId =", resultId)
            print("SpinId =", spinId)
            print("TotalFreeSpinsCount =", totalFreeSpinsCount)
            print("RemainingFreeSpinsCount =", remainingFreeSpinsCount)
            bonusGameResult = {}
            if 'UserSavedState' not in response["SpinResult"]:
                print('no MASK bonus game ...')
                FreeSpinCount = 0
                Multiplier = 0
                WinState = 0
            else:
                print('MASK bonus game !')
                bonusGameResult = findall(response, "WinStateInfo")
                if bonusGameResult is not None:
                    print('bonus game is finished !')
                    print(
                        f'{bonusGameResult["WinState"]} {bonusGameResult["FreeSpinCount"]} {bonusGameResult["Multiplier"]}')
                    FreeSpinCount = bonusGameResult["WinState"]
                    Multiplier = bonusGameResult["FreeSpinCount"]
                    WinState = bonusGameResult["Multiplier"]
                else:
                    print('bonus game is not finished yet ...')

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
            response_GetAsyncResponse.close()

        return response, resultId, spinId, totalFreeSpinsCount, remainingFreeSpinsCount, printAR, bonusGameResult

    @staticmethod
    def GetMancalaQuestGameState(RegToken, ResultId, BonusGameId, SpinId):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(
            ('GetMancalaQuestGameState/' + RegToken + SpinId + BonusGameId + ResultId + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_GetMancalaQuestGameState = ', HASH)
        params_GetMancalaQuestGameState = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                           "BonusGameId": BonusGameId, "SpinId": SpinId}
        response_GetMancalaQuestGameState = requests.post(A.gameURL + '/bonus/GetMancalaQuestGameState',
                                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                                  "BonusGameId": BonusGameId, "SpinId": SpinId},
                                                          json=params_GetMancalaQuestGameState, timeout=1,
                                                          headers={'Connection': 'close'})
        response = response_GetMancalaQuestGameState.json()
        assert response_GetMancalaQuestGameState.status_code == 200
        print(response)
        tokenAsyncGetMancalaQuestGameState = response["TokenAsync"]
        print('GetMancalaQuestGameState_TokenAsync = ', response['TokenAsync'])
        # response_GetMancalaQuestGameState.close()
        return response, tokenAsyncGetMancalaQuestGameState

    @staticmethod
    def GetAsyncResponse_QuestGameState(RegToken, TokenAsyncGetMancalaQuestGameState):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + TokenAsyncGetMancalaQuestGameState + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_GetAsyncResponseQuestGameState = ', HASH)
        params_GetAsyncResponse_QuestGameState = {'Hash': HASH, 'Token': RegToken,
                                                  'TokenAsync': TokenAsyncGetMancalaQuestGameState}
        response_GetAsyncResponse_QuestGameState = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                 params={'Hash': HASH, 'Token': RegToken,
                                                                         'TokenAsync': TokenAsyncGetMancalaQuestGameState},
                                                                 json=params_GetAsyncResponse_QuestGameState, timeout=1,
                                                                 headers={'Connection': 'close'})
        response = response_GetAsyncResponse_QuestGameState.json()
        assert response_GetAsyncResponse_QuestGameState.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_QuestGameState = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                     params={'Hash': HASH, 'Token': RegToken,
                                                                             'TokenAsync': TokenAsyncGetMancalaQuestGameState},
                                                                     json=params_GetAsyncResponse_QuestGameState,
                                                                     timeout=1,
                                                                     headers={'Connection': 'close'})
            response = response_GetAsyncResponse_QuestGameState.json()
        else:
            print('params = ', params_GetAsyncResponse_QuestGameState)
            print("Response =", response)
            ActiveCharacterIndex = response["ActiveCharacterIndex"]
            CharacterIndex = response["CharacterIndex"]
            Cups = response["Cups"]
        # response_GetAsyncResponse_QuestGameState.close()
        return response, ActiveCharacterIndex, CharacterIndex, Cups

    @staticmethod
    def SelectCharacter(RegToken, ResultId, BonusGameId, SpinId, CharacterId):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(
            ('SelectCharacter/' + RegToken + CharacterId + BonusGameId + ResultId + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_SelectCharacter = ', HASH)
        params_SelectCharacter = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                  "BonusGameId": BonusGameId, "SpinId": SpinId, "CharacterId": CharacterId}
        response_SelectCharacter = requests.post(A.gameURL + '/bonus/SelectCharacter',
                                                 params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                         "BonusGameId": BonusGameId, "SpinId": SpinId,
                                                         "CharacterId": CharacterId},
                                                 json=params_SelectCharacter, timeout=1,
                                                 headers={'Connection': 'close'})
        response = response_SelectCharacter.json()
        url = response_SelectCharacter.url
        # print('url = ', url)
        print('params = ', params_SelectCharacter)
        print('response = ', response)
        assert response_SelectCharacter.status_code == 200
        tokenAsyncSelectCharacter = response["TokenAsync"]
        # print(response)
        print('SelectCharacter_TokenAsync = ', response['TokenAsync'])
        # response_SelectCharacter.close()
        return response, tokenAsyncSelectCharacter

    @staticmethod
    def GetAsyncResponse_SelectCharacter(RegToken, tokenAsyncSelectCharacter):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + tokenAsyncSelectCharacter + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseSelectCharacter = ', HASH)
        params_GetAsyncResponse_SelectCharacter = {'Hash': HASH, 'Token': RegToken,
                                                   'TokenAsync': tokenAsyncSelectCharacter}
        response_GetAsyncResponse_SelectCharacter = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                  params={'Hash': HASH, 'Token': RegToken,
                                                                          'TokenAsync': tokenAsyncSelectCharacter},
                                                                  json=params_GetAsyncResponse_SelectCharacter,
                                                                  timeout=1,
                                                                  headers={'Connection': 'close'})
        response = response_GetAsyncResponse_SelectCharacter.json()
        # print('GetAsyncResponse_SelectCharacter = ', response)
        assert response_GetAsyncResponse_SelectCharacter.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_SelectCharacter = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                      params={'Hash': HASH, 'Token': RegToken,
                                                                              'TokenAsync': tokenAsyncSelectCharacter},
                                                                      json=params_GetAsyncResponse_SelectCharacter,
                                                                      timeout=1, headers={'Connection': 'close'})
            response = response_GetAsyncResponse_SelectCharacter.json()
        else:
            print('params = ', params_GetAsyncResponse_SelectCharacter)
            print("response =", response)
            Character = response["Character"]
            print("Character = ", Character)
        # response_GetAsyncResponse_SelectCharacter.close()
        return response, Character

    @staticmethod
    def MakeStep(RegToken, ResultId, BonusGameId, SpinId):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(
            ('MakeStep/' + RegToken + SpinId + BonusGameId + ResultId + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_MakeStep = ', HASH)
        params_MakeStep = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                           "BonusGameId": BonusGameId, "SpinId": SpinId}
        response_MakeStep = requests.post(A.gameURL + '/bonus/MakeStep',
                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                  "BonusGameId": BonusGameId, "SpinId": SpinId},
                                          json=params_MakeStep, timeout=1,
                                          headers={'Connection': 'close'})
        response = response_MakeStep.json()
        print('params_MakeStep = ', params_MakeStep)
        print('response = ', response)
        assert response_MakeStep.status_code == 200
        tokenAsyncMakeStep = response["TokenAsync"]
        print('MakeStep_TokenAsync = ', response['TokenAsync'])
        # response_MakeStep.close()
        return response, tokenAsyncMakeStep

    @staticmethod
    def GetAsyncResponse_MakeStep(RegToken, tokenAsyncMakeStep):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + tokenAsyncMakeStep + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseMakeStep = ', HASH)
        params_GetAsyncResponse_MakeStep = {'Hash': HASH, 'Token': RegToken,
                                            'TokenAsync': tokenAsyncMakeStep}
        response_GetAsyncResponse_MakeStep = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                           params={'Hash': HASH, 'Token': RegToken,
                                                                   'TokenAsync': tokenAsyncMakeStep},
                                                           json=params_GetAsyncResponse_MakeStep,
                                                           timeout=1,
                                                           headers={'Connection': 'close'})
        response = response_GetAsyncResponse_MakeStep.json()
        # print('GetAsyncResponse_SelectCharacter = ', response)
        assert response_GetAsyncResponse_MakeStep.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_MakeStep = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                               params={'Hash': HASH, 'Token': RegToken,
                                                                       'TokenAsync': tokenAsyncMakeStep},
                                                               json=params_GetAsyncResponse_MakeStep,
                                                               timeout=1, headers={'Connection': 'close'})
            response = response_GetAsyncResponse_MakeStep.json()
        else:
            if "WinStateInfo" not in response:
                FreeSpinCount = 0
                Multiplier = 0
            else:
                FreeSpinCount = response["WinStateInfo"]["FreeSpinCount"]
                Multiplier = response["WinStateInfo"]["Multiplier"]
            print('params_GetAsyncResponse_MakeStep = ', params_GetAsyncResponse_MakeStep)
            print("Response =", response)
            print('FreeSpinCount = ', FreeSpinCount)
            print('Multiplier = ', Multiplier)
            ActiveCharacterIndex = response["ActiveCharacterIndex"]
            # CupIndex = response["CupIndex"]
            # Cups = response["Cups"]
            # Steals = response["Steals"]
            # print("ActiveCharacterIndex = ", ActiveCharacterIndex)
            # print("CupIndex = ", CupIndex)
            # print("Cups = ", Cups)
            # print("Steals = ", Steals)
        # response_GetAsyncResponse_SelectCharacter.close()
        return response, ActiveCharacterIndex, FreeSpinCount, Multiplier

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
        response_FreeSpin = requests.post(A.gameURL + A.FreeSpin_Url,
                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                  "SpinId": SpinId}, json=params_FreeSpin,
                                          headers={'Connection': 'close'})
        response = response_FreeSpin.json()
        print("Response =", response_FreeSpin)
        assert response_FreeSpin.status_code == 200
        url = response_FreeSpin.url
        print("Response =", response)
        timeOut = response["Timeout"]
        tokenAsyncFreeSpin = response["TokenAsync"]
        print(f'FreeSpins_TimeOut : {timeOut} / FreeSpins_TokenAsync : {tokenAsyncFreeSpin}')
        response_FreeSpin.close()
        return response, timeOut, tokenAsyncFreeSpin

    @staticmethod
    def GetAsyncResponse_FreeSpin(RegToken, TimeOut, TokenAsyncFreeSpin):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + TokenAsyncFreeSpin + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseFreeSpin = ', HASH)
        params_GetAsyncResponse_FreeSpin = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsyncFreeSpin}
        print('params getAsyncResponse_FreeSpin= ', params_GetAsyncResponse_FreeSpin)
        response_GetAsyncResponse_FreeSpin = requests.post(A.gameURL + A.GetAsyncResponse_Url,
                                                           params={'Hash': HASH, 'Token': RegToken,
                                                                   'TokenAsync': TokenAsyncFreeSpin},
                                                           json=params_GetAsyncResponse_FreeSpin,
                                                           headers={'Connection': 'close'})
        response = response_GetAsyncResponse_FreeSpin.json()
        print('GetAsyncResponse_FreeSpin = ', response)
        assert response_GetAsyncResponse_FreeSpin.status_code == 200

        while "Error" in response:
            if response["Error"] == 13:
                print('GetAsyncResponse = ', response)
                print(f'sleeping ... {TimeOut} ms')
                time.sleep(TimeOut / 1000)
                print('GetAsyncResponse = ', response)
                response_GetAsyncResponse_FreeSpin = requests.post(A.gameURL + A.GetAsyncResponse_Url,
                                                                   params={'Hash': HASH, 'Token': RegToken,
                                                                           'TokenAsync': TokenAsyncFreeSpin},
                                                                   json=params_GetAsyncResponse_FreeSpin,
                                                                   headers={'Connection': 'close'})
                response = response_GetAsyncResponse_FreeSpin.json()
            else:
                for key in E.error_codes_dictionary:
                    if response["Error"] == key:
                        print(f'\nScript error: {E.error_codes_dictionary[key]} = {key}', )
                        exit()

        else:
            spinIdFs = response['SpinResult']['Id']
            print('spinIdFs = ', spinIdFs)
            print("Response =", response)
            if response["GameFreeSpins"]:
                remainingFreeSpinsCount = response["GameFreeSpins"][0]["RemainingFreeSpinsCount"]
                totalFreeSpinsCount = response["GameFreeSpins"][0]["TotalFreeSpinsCount"]
                print("remainingFreeSpinsCount = ", remainingFreeSpinsCount)
                print("totalFreeSpinsCount = ", totalFreeSpinsCount)
            else:
                totalFreeSpinsCount = 0
                remainingFreeSpinsCount = 0
        response_GetAsyncResponse_FreeSpin.close()
        return response, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs
