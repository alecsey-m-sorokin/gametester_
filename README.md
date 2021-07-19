# GameTester

автоматизация тестирования стратегий игры MM5 - Portal Master

регулярная игра
игра с фри спинами
игра с обменом сфер на скаттеры

параметры запуска файла starter.py

python.exe starter.py mm5 --strategy [fs, basic, replace] -- sessions [1..250] --rounds [1..250]

пример : 
python.exe starter.py mm5 --strategy replace -- sessions 2 --rounds 15

если в качестве параметра указать только mm5, то запустится базовый тест с параметрами сессии = 1 и раунда = 10
python.exe starter.py mm5

так же можно необязательные параметры использовать частично

starter.py mm6 --strategy rtp --sessions 1 --rounds 1 --rtp 120
