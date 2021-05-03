# RaspBerryPi_Pong...

## Requirements
* MQTT topics
    - /player1
    - /player2

    Coördinaten paddles van server naar client
    Initieël sturen we alle coördinaten en nadien enkel Y0 en Y1 omdat we enkel naar boven en onder bewegen
    - /playerX/server/x0
    - /playerX/server/y0
    - /playerX/server/x1
    - /playerX/server/y1

    Coördinaten paddles van client naar server
    Wordt gans het spel naar server gestuurd
    - /playerX/client/up  Zal een boolean zijn -> True is naar boven gaan en False is niet bewegen
    - /playerX/client/down  Zal een boolean zijn -> True is naar onder gaan en False is niet bewegen
    - /playerX/client/fast  Zal een boolean zijn -> True is sneller bewegen en False is default speed
    - /playerX/client/

    Coördinaten bal
    Wordt gans het spel verstuurd naar client
    - /bal/x0
    - /bal/y0
    - /bal/x1
    - /bal/y1



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


## Thomas Kramp
* Collison detectie op bewegende objecten
    * met integratie collision klasse (bol + colision.py) van Robbe