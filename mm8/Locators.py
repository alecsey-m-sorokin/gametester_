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

# bets = [
#     ('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25'), ('6', '25'), ('7', '25'),
#     ('8', '25'), ('9', '25'), ('10', '25'), ('15', '25'), ('20', '25'), ('25', '25'), ('30', '25'),
#     ('40', '25'), ('50', '25'), ('60', '25'), ('70', '25'), ('80', '25'), ('90', '25')
# ]

bets = [
    ('1', '25')
]


class APIdata_TwinWins:
    DOMAIN_tps = 'https://testpartnerservice.carhenge.space/setup/'
    DOMAIN = 'https://m-2932-mm8n-api.carhenge.space/'
    # DOMAIN = 'https://test-games-api.carhenge.space'

    gameURL = 'https://m-2932-mm8n-api.carhenge.space/'
    frontURL = 'https://review-feature-m-gwyldv.carhenge.space/'
    partnerURL = 'https://m-2932-partners-api.carhenge.space/'

    # gameURL = 'https://test-mm8n-api.carhenge.space/'
    # frontURL = 'https://stest.zhdun.space/'
    # partnerURL = 'https://test-partners-api.carhenge.space/'

    AuthorizationGame_Url = 'auth/AuthorizationGame'
    ResumeGame_Url = 'games/ResumeGame'
    GetSlotInfo_Url = 'games/GetSlotInfo'
    CreditDebit_Url = 'games/CreditDebit'
    GetAsyncResponse_Url = 'games/GetAsyncResponse'
    FreeSpin_Url = 'games/FreeSpin'
    GetMancalaQuestGameState_Url = 'bonus/GetMancalaQuestGameState'
    SelectCharacter_Url = 'bonus/SelectCharacter'
    MakeStep_Url = 'bonus/MakeStep'

    partnerID = '360'
    partnerID_rtp = '382'
    partnerID_rtp_90 = '476'
    partnerID_rtp_95 = '477'
    partnerID_rtp_96 = '478'
    partnerID_rtp_97 = '479'
    partnerID_rtp_120 = '480'

    start_users_rtp_90 = 20500  # 90%
    start_users_rtp_95 = 20300  # 95%
    start_users_rtp_120 = 20900  # 120%

    gameID = '21001'
    userID = '55555'
    currency = 'EUR'
    gameKey = 'TestKey'
    betSum = '1'
    cntLineBet = '25'
    TokenAsync = ''
    TokenAsync_2 = ''
    CardIndex = '2'
    mobile_platform = '&MobilePlatform=false'
    mm6_bonus = '&highfrequencybonus=true'

    fileName_fs = 'mm8/' + ''
    fileName_basic = 'mm8/' + 'test_mm8_basic_game.py'
    fileName_rtp = 'mm8/' + 'test_mm8_rtp.py'



# y1 = [method(x, point, data) for x in x1]
