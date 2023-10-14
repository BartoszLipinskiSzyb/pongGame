# Gra Pong
Gra Pong to okienkowa aplikacja napisana w pyQt i pygame, która odwzorowuje jedną z pierwszych gier wideo.
# Instalacja
 - Pobierz lub zklonuj przy pomocy Git repozytorium:
> git clone https://github.com/BartoszLipinskiSzyb/pongGame
 - Zainstaluj potrzebne moduły, np. przy pomocy PIP:
> pip install pyqt5  
> pip install pygame
 - Uruchom plik *main.py* przy pomocy interpretera Pythona (zalecana wersja: 3.11):
> cd pongGame  
> python main.py
# Jak grać
Po uruchomieniu pojawia się okienko z przyciskiem *Graj* oraz *Ustawienia*
 - Przycisk *Graj* otwiera nowe okno z grą
	 - Gracz 1 używa klawiszy *arrow up* oraz *arrow down* do poruszania się
	 - Gracz 2 używa klawiszy *W* oraz *S* do poruszania się
	 - Celem gry jest odbijanie piłki oraz doprowadzenie przeciwnika do nie odbicia piłki
 - Przycisk *Ustawienia* otwiera nowe okno z ustawieniami
	 - *fps*: ilość klatek na sekundę podczas gry
	 - *width*: szerokość ekranu podczas gry
	 - *height*: wysokość ekranu podczas gry
	 - *fullscreen*: False - gra uruchomi się w okienku o rozmiarach zdefiniowanych przez *width* i *height*, True - uruchomi grę w okienku o wymiarach wyświetlacza urządzenia
	 - *cursorVisible*: widoczność kursora na okienku gry
	 - *ballSpeed*: prędkość piłki
	 - *boardSpeed*: prędkość paletek
	 - *speedUp*: True - automatycznie przyspiesza grę w momentach kiedy długo trzeba czekać na piłkę
	 - Przycisk *Zapisz* waliduje i zapisuje do pliku *settings.json* wartości z formularza
	 - Przycisk *Zapisz i wyjdź* waliduje i zapisuje do pliku *settings.json* wartości z formularza, a następnie zamyka okienko ustawień
# Funkcjonalności
## Prędkości niezależne od liczby klatek na sekundę
Co klatkę liczony jest odstęp czasowy od poprzedniej klatki  - jest on uwzględnianych w obliczeniach pozycji
## Zmiana trybu pełnoekranowego podczas gry
Wystarczy nacisnąć klawisz F11
## Odbijanie piłki od paletek oraz brzegów
Sposób obliczania pozycji niepozwalający na przenikanie piłki przez ściany
## Liczenie punktów
Punkty są zdobywane kiedy przeciwny gracz nie da rady odbić piłki i przeleci ona za jego paletkę. Po osiągnięciu 10 punktów gra kończy się i wynik wyświetlany jest w okienku startowym
## Podkręcanie piłki
Jeśli piłka zostanie odbita od paletki będącej w ruchu, to *podkręci się* i zmieni kąt pod którym się porusza. Wektor prędkości piłki jest normalizowany, dzięki czemu jej szybkość pozostaje stała

