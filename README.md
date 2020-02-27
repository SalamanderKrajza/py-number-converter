# NumberConverter
Założenia projektu:
1. Napisać aplikację Django - “liczby pisane słownie”
Przykład działania:
input: 10, output: “dziesięć”
input: 67, output: “sześćdziesiąt siedem”
input: 11234981, output: “jedenaście milionów dwieście trzydzieści cztery tysiące dziewięćset osiemdziesiąt jeden”

2. Aplikacja ma składać się z:
- formularza, w którym przekazana jest liczba całkowita
- widoku, który zwraca zapis słowny danej liczby
3. W pliku "functional_test.py" przygotować testy funkcjonalne
4. W pliku "number_converter_app\tests.py" przygotować testy jednostkowe


Dodatkowe uwagi:
1. Projekt został napisany w języku Python w wersji 3.7.4.
2. W pliku requirements.txt zawarto informacje o wszystkich zainstalowanych w środowisku virtualnym paczkach/bibliotekach.
3. Do poprawnego działania testów funkcjonalnych napisanych z wykorzystaniem Selenium niezbędna jest:
- Zainstalowana przeglądarka Firefox
- Plik geckodriver.exe dostępny pod adresem https://github.com/mozilla/geckodriver/releases dodany do "System's PATH Environmental Variable" w przypadku uruchamiania projektu na Windowsie