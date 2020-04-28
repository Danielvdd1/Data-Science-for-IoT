# TV-uitzetter
Data Science for IoT project



# Introductie



# Project idee



# Bouw instructies
## Benodigdheden
### Hardware
Project onderdelen
* Raspberry pi 3B
* 5 volt voeding
* Radar sensor
* IR-ontvanger
* IR led
* Breadboard
* Breadboard draden
* Transistor
* 220Ω weerstand
* 10kΩ weerstand

Accessoires voor de Raspberry pi:
* Toetsenbord
* Muis
* HDMI-beeldscherm met kabel

### Software
* Raspbian besturingssysteem (Ook te installeren via NOOBS)
* Python (Is standaard geinstalleerd op Raspbian full versie)
* Thingspeak website


## Raspberry pi
Installeer een besturingssysteem. Dit doe je door een besturingssysteem op de sd kaart te zetten en deze in de Raspberry pi te steken.
Voor beginners adviseer ik om noobs te installeren. Hiermee kan je makkelijk verschillende besturingssystemen proberen. Kies bij dit project voor Raspbian.
Dit zijn instructies om noobs te installeren: https://thepi.io/how-to-install-noobs-on-the-raspberry-pi/

Als Raspbian geïnstalleerd is moeten het elektrische schema opgebouwd worden. Verbind de onderdelen zoals op de afbeelding hieronder is voorgedaan. Let op, controleer de pinnen van de infrarood ontvanger, hier is namelijk verschil in.
![Circuit](/Assets/Circuit.png)

## Thingspeak
Maak een account op [Thingspeak](https://thingspeak.com/) en klik op channels. Er zijn twee channels nodig. De eerste channel is voor de inkomende data met twee fields genaamd State en Movement. De tweede channel is voor de verwerkte data met een field die aan zal geven of de tv uit moet.  
![Channel1](/Assets/Channel1.png)
![Channel2](/Assets/Channel2.png)

## Python
Nu gaan we verder op de Raspberry pi. Kopieer de code van deze Github repository en sla dit op als een python bestand (.py) op de Raspberry pi. Of clone de hele Github repository door een nieuwe terminal te openen en dit commando uit te voeren: `git clone https://github.com/Danielvdd1/Data-Science-for-IoT.git`
Open het python bestand in de code folder in een tekst editor zoals nano en vul de 4 variabelen in genaamd writeAPIkey, writeChannelID, readAPIkey en readChannelID. Deze informatie kun je vinden in Teamspeak in de bijbehorende channels. De Channel id staat bij ‘Channel settings’ en de read of write API keys staan bij het kopje ‘API Keys’.
De write API key en channel moeten de waarde hebben van de channel van de Incomming data. En de read API key en channel moeten de waarde hebben van de channel van de Outgoing data.

Als de sensoren goed zijn aangesloten en de Teamspeak channels goed zijn ingesteld kan de python code aangezet worden en zal de eerste data naar Teamspeak verzonden kunnen worden.

## Matlab analysis
Matlab Analysis is een app op Teamspeak waarmee de data in de channels verwerkt kan worden. Open Matlab Analysis op Teamspeak > Apps > MATLAB Analysis. Maak een nieuwe lege code aan en copieer de code hieronder in Matlab Analysis.
```lang-matlab
Github markdown
Code hier
```
Vul de 4 variabelen in genaamd readAPIKey, readChannelID, writeAPIKey en writeChannelID.
De readAPIKey en readChannelID moeten de waarde hebben van de channel van de Incomming data. En de writeAPIKey en writeChannelID moeten de waarde hebben van de channel van de Outgoing data.
Klik op ‘Sava and Run’ om de code uit te voeren. Deze code wordt dan helaas maar 1 keer uitgevoerd. Om deze code constant uit te voeren en dus up-to-date te houden moeten we TimeControle gebruiken. Dit is een app op Teamspeak die acties uit kan voeren op ingestelde tijdstippen. Ook kan deze app acties herhalen.
De makkelijkste manier om dit in te stellen is om bij de Matlab Analysis code omlaag te scrollen naar ‘Schedule Actions’ en op ‘TimeControl’ te klikken. Dit brengt je meteen naar een pagina om TimeControl in te stellen op de MatlabAnalysis code.
Stel deze Timecontrol in zoals op de afbeelding hieronder.
![TimeControl](/Assets/TimeControl.png)

Als alle stappen goed zijn opgevolgd 
