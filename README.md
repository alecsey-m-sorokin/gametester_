# GameTester

автоматизация тестирования стратегий игр :
MM5 - Portal Master
MM6 - Mancala Quest

All dependencies are in the requirements.txt file 
```sh
pip install -r requirements.txt
```

регулярная игра
игра с фри спинами
игра с обменом сфер на скаттеры

параметры запуска файла starter.py
```sh
python.exe starter.py mm5 --strategy [fs, basic, replace] -- sessions [1..250] --rounds [1..250]
```
пример : 
```sh
python.exe starter.py mm5 --strategy replace -- sessions 2 --rounds 15
```
если в качестве параметра указать только mm5, то запустится базовый тест с параметрами сессии = 1 и раунда = 10
python.exe starter.py mm5

так же можно необязательные параметры использовать частично

starter.py mm6 --strategy rtp --sessions 1 --rounds 1 --rtp 120
