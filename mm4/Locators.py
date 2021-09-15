class ErrorCodes:
    error_codes = [10, 11, 13, 49, 50, 51, 64, 100, 101, 102, 105, 108, 109, 110, 113, 114, 115, 116, 150, 151, 152,
                   200, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214]
    error_codes_messages = ['HashMismatch', 'RoundNotFound', 'AsyncResponseNotFound', 'GambleInfoNotFound',
                            'GambleCalculationError', 'InternalServiceError', 'MySQLRequestFailed', 'MongoSaveError',
                            'CachePartnerNotFound', 'RequestToPartnerFailed', 'PartnerError', 'WrongParamError',
                            'MongoUserSessionNotFound', 'MySQLRoundCreationError', 'PartnerBlocked', 'UserBlocked',
                            'CacheGameNotFound', 'InsufficientFunds', 'DemoUserNotFound', 'DemoUserCreateError',
                            'DemoUserUpdateError', 'GameBlocked', 'SpinslotInvalidMethod', 'GameEnded',
                            'UnavailableAction', 'JackpotError', 'GameNotFound', 'WrongBetSum',
                            'WrongLogic', 'NoAvailableFreeSpins', 'UserNotFound', 'TokenError']
    error_codes_dictionary = dict(zip(error_codes, error_codes_messages))


bets = [
    ('1', '25')
]


class APIdata_mm4:
    DOMAIN_tps = 'https://testpartnerservice.carhenge.space/setup/'

    DOMAIN = 'https://test-games-api.carhenge.space'
    gameURL = 'https://test-games-api.carhenge.space/'
    frontURL = 'https://stest.zhdun.space/'
    partnerURL = 'https://test-partners-api.carhenge.space/'

    # DOMAIN = "https://mg-1466-games-api.carhenge.space"
    # gameURL = 'https://mg-1466-games-api.carhenge.space/'
    # frontURL = 'https://stest.zhdun.space/'
    # partnerURL = 'https://mg-1466-partners-api.carhenge.space/'

    AuthorizationGame_Url = '/auth/AuthorizationGame'
    ResumeGame_Url = 'games/ResumeGame'
    GetSlotInfo_Url = '/games/GetSlotInfo'
    CreditDebit_Url = '/games/CreditDebit'
    GetAsyncResponse_Url = '/games/GetAsyncResponse'
    FreeSpin_Url = '/games/FreeSpin'

    partnerID = '360'
    partnerID_rtp = '382'
    partnerID_rtp_90 = '476'
    partnerID_rtp_95 = '477'
    partnerID_rtp_96 = '478'
    partnerID_rtp_97 = '479'
    partnerID_rtp_120 = '480'

    start_users_rtp_90 = 20500  # 90%
    # start_users_rtp_95 = 10500  # 95%
    start_users_rtp_95 = 20300  # 95%
    start_users_rtp_120 = 20900  # 120%

    gameID = '17001'
    userID = '160'
    currency = 'EUR'
    gameKey = 'TestKey'
    betSum = '1'
    cntLineBet = '5'
    TokenAsync_2 = ''
    CardIndex = '2'
    mobile_platform = '&MobilePlatform=false'





    fileName_basic = 'mm4/' + 'test_mm4_basic_game.py'
    fileName_rtp = 'mm4/' + 'test_mm4_rtp.py'