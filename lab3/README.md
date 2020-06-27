Zadanie na 5

INSTRUKCJA:
    1. Uruchamiamy program (poleceniem: python LZW.py [plik do zakodowania] [rodzaj kodowania])
    2. Możlie kodowanie:
        'eg' : kodowanie eliasa gamma
        'ed' : kodowanie eliasa delta
        'eo' : kodowanie eliasa omega
        'fb' : kodowanie fibonacciego
        ''   : jakiekolwiek inne oznaczenie lub jego brak oznaczenia powoduje użycie kodowania eliasa omega

    3. Na standardowym wyjsciu otrzymujemy statystyki dotyczące kompresji, dodatkowo w pliku encoded.bin znajduje sie jego zdekompresowana wersja,
    a w decoded.bin jego zdekompresowana wersja. 

PRZYKLADOWE URUCHOMIENIE:
    python LZW.py test.txt eg