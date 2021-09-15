import hashlib
import json
import time
import requests

from Locators import APIdata_mm4


A = APIdata_mm4


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


class API_CocoTiki:

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
        return response

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
        params_CreditDebit = {'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                              'BetSum': betSum}
        response_CreditDebit = requests.post(A.DOMAIN + '/games/CreditDebit',
                                             params={'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                                                     'BetSum': betSum}, json=params_CreditDebit, timeout=1, headers={'Connection': 'close'})
        response = response_CreditDebit.json()
        assert response_CreditDebit.status_code == 200
        print(response)
        tokenAsync = response["TokenAsync"]
        return tokenAsync

    @staticmethod
    def GetAsyncResponse(RegToken, TokenAsync):
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsync + A.gameKey).encode('utf-8')).hexdigest()
        params_GetAsyncResponse = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync}
        print(params_GetAsyncResponse)
        response_GetAsyncResponse = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                  params={'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync},
                                                  json=params_GetAsyncResponse, timeout=10, headers={'Connection': 'close'})
        response = response_GetAsyncResponse.json()
        assert response_GetAsyncResponse.status_code == 200
        i = 0
        while "Error" in response:
            assert i < 50, 'Превышено количество запросов'
            # if i > 50:
            #     break
            i += 1
            response_GetAsyncResponse = requests.post(A.DOMAIN + '/games/GetAsyncResponse',
                                                      params={'Hash': HASH, 'Token': RegToken,
                                                              'TokenAsync': TokenAsync}, json=params_GetAsyncResponse, headers={'Connection': 'close'})
            response = response_GetAsyncResponse.json()
            print(response)

        print(response)
        return response


    @staticmethod
    def AcceptBarWin(RegToken, ResultId, SpinId):
        BetLevel = A.betSum
        HASH = hashlib.md5(('AcceptBarWin/' + RegToken + ResultId + SpinId + BetLevel + A.gameKey).encode('utf-8')).hexdigest()
        params_AcceptBarWin = {'Hash': HASH, 'Token': RegToken,
                                'ResultId': ResultId, 'SpinId': SpinId, 'BetLevel': BetLevel}
        response_AcceptBarWin = requests.post(A.DOMAIN + '/bonus/AcceptBarWin',
                                               params={'Hash': HASH, 'Token': RegToken,
                                                       'ResultId': ResultId, 'SpinId': SpinId, 'BetLevel': BetLevel},
                                               json=params_AcceptBarWin, timeout=1,
                                               headers={'Connection': 'close'})
        response = response_AcceptBarWin.json()
        assert response_AcceptBarWin.status_code == 200
        tokenAsync = response["TokenAsync"]
        print(response)
        return tokenAsync

    @staticmethod
    def PickPearlGame(RegToken, ResultId, SpinId):
        BetLevel =A.betSum
        PerlNumber = '0'
        HASH = hashlib.md5(('PickPearlGame/' + RegToken + ResultId + SpinId + BetLevel + PerlNumber + A.gameKey).encode('utf-8')).hexdigest()
        print(f'PickPearlGame/ + {RegToken} + {ResultId} + {SpinId} + {BetLevel} + {PerlNumber} + {A.gameKey}')
        params_PickPearlGame = {'Hash': HASH, 'Token': RegToken, 'BetLevel': BetLevel, 'PerlNumber': PerlNumber,
                                'ResultId': ResultId, 'SpinId': SpinId, 'Finish': 'false', 'Info': 'false'}
        print(A.DOMAIN + '/bonus/PickPearlGame')
        print(params_PickPearlGame)
        response_PickPearlGame = requests.post(A.DOMAIN + '/bonus/PickPearlGame',
                                               params=params_PickPearlGame,
                                               json=params_PickPearlGame, timeout=1,
                                               headers={'Connection': 'close'})
        response = response_PickPearlGame.json()
        print(response)
        assert response_PickPearlGame.status_code == 200
        tokenAsync = response["TokenAsync"]
        print('HASH!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(HASH)
        return tokenAsync

    @staticmethod
    def FreeSpin(RegToken, ResultId, SpinId):
        HASH = hashlib.md5(('FreeSpin/' + RegToken + ResultId + SpinId + A.gameKey).encode('utf-8')).hexdigest()
        params_FreeSpin = {'Hash': HASH, 'Token': RegToken, 'ResultId': ResultId, 'SpinId': SpinId}
        response_FreeSpin = requests.post(A.DOMAIN + '/games/FreeSpin',
                                               params=params_FreeSpin,
                                               json=params_FreeSpin, timeout=1,
                                               headers={'Connection': 'close'})
        response = response_FreeSpin.json()
        assert response_FreeSpin.status_code == 200
        tokenAsync = response["TokenAsync"]
        print(response)
        return tokenAsync

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

