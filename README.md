# RaspBerryPi_Pong...

## Requirements
* MQTT topics

    Coördinaten paddles van server naar client
    Initieël sturen we alle coördinaten en nadien enkel Y omdat we enkel naar boven en onder bewegen
    We sturen dit door met deze syntax: [x0,y0,x1,y1]
    - /playerX/server/coords

    Beweging van speler van client naar server
    Wordt gans het spel naar server gestuurd
    - /playerX/client/up  Zal een boolean zijn -> True is naar boven gaan en False is niet bewegen
    - /playerX/client/down  Zal een boolean zijn -> True is naar onder gaan en False is niet bewegen
    - /playerX/client/fast  Zal een boolean zijn -> True is sneller bewegen en False is default speed

    Startsignaal van server naar client
    - /server/start

    Startsignaal van client naar server
    - /client/start

    Startsignaal van nieuw spel binnen +- 4 seconden van server naar client.
    De server zal om de 1 seconden versturen en dit 6x naar /server/startnext. De payload maakt niet uit
    - /server/startnext

    Punten van client
    - /playerx/points

    Coördinaten bal
    Wordt gans het spel verstuurd naar client
        We sturen dit door met deze syntax: [x0,y0,x1,y1]
    - /bal/coords

    Config variabelen
    - Aantal botsingen
        - /tics
    - Aantal rondes
        - /rounds

    Select player initialisatie 
    We gaan eerst van client uit een puls geven naar topic
    - /client/player 
    met de payload '1'
    De server zal hierop "True" of "False" op antwoorden op topic
    - /server/player
    a.d.h.v. een boolean die hij intern heeft ofdat er al een speler 1 zich heeft aangemeld.
    Als de client 'True' krijgt, dan is hij speler1.
    Als de client 'False' krijgt, dan stuurt hij een '2' op topic
    - /client/server
    De server zal weer kijken of er ene player2 zich al heeft aangemeld. Zo niet, dan zal deze client een 'True' ontvangen op topic
    - /server/player
    Wanneer de client een 'False' krijgt, dan kan deze client enkel en alleen maar kijken.

    De speler uitkiezen
    Wanneer deze topic een True uitstuurt, dan zal player 1 Links zijn en player 2 Rechts.
    Wanneer deze topic een False uitstuurt, dan zal player 1 Recht zijn en player 2 Links.
    - /server/selectplayer


# Week 1 (26/4 2/5)
## Robbe Elsermans
* experimenteren met tkInter
* 2 padels onafhankelijk van elkaar laten bewegen via mouse input
    * we kunnen kiezen a.d.h.v. 1 variabele of de linkse of de rechtse bruikbaar is
    * padels kunnen niet uit het scherm gaan
* Een beetje OOP toegepast in de paddels.ph
* begin bol laten bewegen
* Bol laten bewegen + collision op eender welk object + OOP
* probeersel MQTT met full duplex 

## Thomas Kramp
* experimenteren met tkInter
* Paddle laten bewegen via key input + OOP
* Een bal laten bewegen dat niet buiten de kader kwam.
* Collison detectie op bewegende objecten
    * met integratie collision klasse (bol + colision.py) van Robbe


# Week 2 (3/5 9/5)
## Robbe Elsermans
* Start aan Client Console voor player0
* Aanpassing klassens om enken van server afhankelijk te zijn
* Maak de grafische interface 
    * toevoeging bol + paddle
    * toevoeging drukknoppen
    * toevoeging leds
* maak testopgeving op in Node-Red om mqtt berichten te simuleren
* Configureer de 'on_message' MQTT handler.
    * De paddles laten bewegen a.d.h.v. de gekregen waarde van de server op topic /player1/coords & /player2/coords
    * De bol laten bewegen a.d.h.v. de gekregen waarde van de server op topic /bal/coords
    * De start knop laten verdwijnen wanneer de client het start signaal verkrijgt van de server op topic /server/start
    * De gele led laten pinken op de topic /server/startnext die 6x zal versturen (de led zal hierdoor 3x aangaan)
* Begin uitwerking van select player 
    * De client bij opstart allemaal onder dezelfde een '1' sturen op topic /client/player
    * De logica die bij 'Requirements' staat uitwerken
* dubbele gebruikte code opschonen
* De client zijn naam veranderen als de speler geselecteerd is a.d.h.v. 'playerSelector'
* opkuis van code ga ik later pas doen

## Thomas Kramp
* Collison detectie op bewegende objecten
    * met integratie collision klasse (bol + colision.py) van Robbe

# Week 3 (10/5 16/5)
## Robbe Elsermans

## Thomas Kramp
* Game server aanmaken
    * Aparte paddle en ball classe voor server aanmaken
    * MQTT publishes en subsrcibes maken op basis van de client side
    * 
