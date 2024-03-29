'''
Script voor de beurscrash/ inflatie borrel
Door Wieske

HOE TE GEBRUIKEN:
VOORBEREIDING
* Vul alle dranken in die je wil verkopen, in de vorm:
inventaris['{naam'] = drank(minprijs, maxprijs, startprijs, nrtotaal)   
elke drank begint op de aangegeven startprijs en zal nooit onder de minprijs of boven de maxprijs komen
wanneer een drank op is (dus nrtotaal - aantal verkocht <= 0) dan zal deze uit de lijst worden gehaald
* Test het script nog een keer (samen met Wieske)

TIJDENS DE BORREL:
* Run het script
* Verplaats de grafiek naar het beamerscherm
    (als dit niet meteen lukt kan je eerst een aantal aankopen invoeren)
* Wanneer je een (of meer) drankje(s) verkoopt vul je in:
 - {naam van het drankje} (moet wel in de drankinventaris staan)
 - {aantal dat je hebt verkocht}
 - {borrelsaldonaam} (moet wel op de saldolijst staan)
     Vul een streepje (-) in als niet met borrelsaldo wordt betaald
     Om een nieuwe naam in de borrelsaldolijst te zetten: 
         vul in op borrelsaldo van: toevoegen
     drankje niet echt verkopen, maar alleen prijs veranderen: 
         vul in op borrelsaldo van: crash
 
 -> Vervolgens worden de nieuwe prijzen automatisch berekend en wordt de plot geupdate

* Prijzen resetten naar de startprijs: 
    Vul in bij verkocht merk: reset

AAN HET EIND VAN DE BORREL:
* Programma stoppen:
    Vul in bij verkocht merk: break
Vervolgens worden opgeslagen in de map waar het script staat:
 - de grafiek (als png)
 - de prijshistorie (als csv); lijst met de prijzen van alle dranken voor alle tijden waarbij de prijs is veranderd
 - de borrellijst (als csv); lijst met borrelsaldonamen en uitgegeven bedrag
'''

# Imports
import random
import matplotlib.pyplot as plt
plt.ion()
import time
import pandas as pd

crash=False

# Class om een drankobject te kunnen maken
class drank:
    def __init__(self, minprijs, maxprijs, startprijs, koopprijs, nrtotaal, naam):
        self.minprijs = minprijs
        self.maxprijs = maxprijs
        self.startprijs = startprijs
        self.koopprijs = koopprijs
        self.nrtotaal = nrtotaal
        self.over = nrtotaal
        self.prijs = startprijs
        self.historie = [startprijs]
        self.naam = naam
    
    def veranderprijs(self, verkocht, verhoogmet=10, aantaldranken=10, crash=False, drank=None):
        self.verkocht = verkocht
        
        if verkocht > 0:
            if crash == False:
                # haal het aantal verkochte biertjes af van het totaal (tenzij crash)
                self.over -= verkocht
            # verhoog de prijs van de drank
            verhoging = verkocht * verhoogmet
        else:
            # verlaag de prijs van de drank 
            # (maar zorg dat gemiddelde prijs van alles ongeveer gelijk blijft)
            verhoging = verkocht * verhoogmet / (aantaldranken-1)
        
        # Verhoog de prijs met een random getal rond verhoging
        self.prijs += random.gauss(verhoging, verhoging)
        # Zorg dat prijs tussen minprijs en maxprijs zit:
        self.prijs = max(self.minprijs, min(self.prijs, self.maxprijs))
        # Eventueel nog iets afhankelijk van het aantal dat nog over is ?
        
        # Voeg de huidige prijs toe aan de historie lijst:
        self.historie.append(self.prijs)


# Maak de drankinventaris:
inventaris = {}
inv_oud = {}
# inventaris['naam'] = drank(minprijs, maxprijs, startprijs, koopprijs, nrtotaal, naam)
inventaris['ryu'] = drank(70, 120, 100, 99, 40,  'Ryujin')
inventaris['reale'] = drank(100, 170, 140, 150, 30, 'Del Borgo Reale')
inventaris['zweipac'] = drank(160, 250, 200, 224, 30,  'Kaapse Zweipac')
inventaris['hops'] = drank(240, 320, 270, 299, 30  ,'Fresh Hops')
inventaris['quad'] = drank(150, 230, 190, 209, 40 ,'Prearis Quadrupel')
inventaris['boudelo'] = drank(130, 200, 170, 179, 40 ,'Boudelo Tripel')
inventaris['zwijntje'] = drank(100, 165, 140, 149, 40 ,'Zwijntje')
inventaris['trio'] = drank(70, 120, 100, 99, 30 ,'Trio Extra Stout')
inventaris['callista'] = drank(260, 340, 300, 325, 30, 'My name is Callista')




# Maak figuur aan:
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
plots = []
for i, drank in enumerate(inventaris):
    lines, = ax.plot([],[])
    plots.append(lines)
ax.set_ylim(0, 340)
plt.xlabel('Tijd')
plt.ylabel('Prijs in cent')

# Maak functie die checkt of een string (x) geconverteerd kan worden naar int
def is_int(x):
    try:
        int(x)
    except ValueError:
        return False
    return True

# Maak een aantal start variabelen aan
hoogsteprijs = 0
tijd = [time.time()]
borrellijst = []

# Script om continue verkochte dranken in te vullen:
while True:
    # Vraag welk merk er is verkocht:
    merk = input('Verkocht merk: ')
    if merk == 'break':
        # Stop het programma (slaat alle resultaten op)
        break    
    if merk == 'reset':
        # Reset alle prijzen naar de startprijs
        for drank in inventaris:
            inventaris[drank].prijs = inventaris[drank].startprijs
        merk = input('Verkocht merk: ')
    # Check of het merk in de inventaris zit:        
    while merk not in inventaris:
        print('Vul een van de aanwezige merken in:')
        print(inventaris.keys())
        merk = input('Verkocht merk: ')
    
    correct = False
    while correct == False:
        # Vraag hoeveel van dit merk verkocht zijn:
        aantal = input('Aantal: ')
        # Check of er een getal (integer) is ingevoerd:
        if is_int(aantal) == False:
            print('Vul een geheel getal in.')
        else: 
            aantal = int(aantal)
            aantalover = inventaris[merk].over
            if aantalover < aantal:
                print('Er zijn nog maar {} over van {}'.format(aantalover, merk))
            else:
                correct = True
    
    # Check de prijs die betaald moet worden:
    verkoopprijs = (inventaris[merk].prijs * aantal)/100
    print('Verkoopprijs is: €{:.2f}'.format(verkoopprijs))
    print('\n')
    winst = ((inventaris[merk].koopprijs - inventaris[merk].prijs) * aantal)/100


    
    
    # Update de prijs en print de nieuwe prijs voor alle dranken en update plot
    print('\n-----------------------------------------------------------------')
    print('Huidige prijzen: \n')
    tijd.append(time.time())
    drankop = False
    # Voor alle dranken in de inventaris:
    for j, drank in enumerate(inventaris):
        # Update de prijzen:
        if drank == merk: 
            inventaris[drank].veranderprijs(aantal, aantaldranken=len(inventaris), crash=crash, drank=drank)
        else:
            inventaris[drank].veranderprijs(-aantal, aantaldranken=len(inventaris), crash=crash, drank=drank)
        
        # Print de prijzen:
        prijs = inventaris[drank].prijs
        naam = inventaris[drank].naam
        label = '{}: €{:.2f}'.format(naam, prijs/100)
        print(label)
        if prijs > hoogsteprijs:
            hoogsteprijs = prijs
        
        # Verwijder uit inventaris als drank op is:
        if inventaris[drank].over <= 0:
            print(drank, 'is op en wordt hierna verwijderd uit de lijst')
            drankop = drank
            label = '{}: op'.format(drank)
            nr = j
        
        # Update plot met prijzen:
        plots[j].set_xdata(tijd)
        plots[j].set_ydata(inventaris[drank].historie)
        plots[j].set_label(label)
        
    
    if drankop != False:
        val = inventaris.pop(drankop, None)
        inv_oud[drankop] = val
        print(drankop, 'is verwijderd')
        del plots[nr]
    
    # Rescale en update figuur:
    ax.set_xlim(tijd[0], tijd[-1])
    ax.get_xaxis().set_ticks([])
    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
    fig.canvas.draw()
    fig.canvas.flush_events()
    print('\n')
# Wanneer het programma is gestopt (met break):
# Sla de borrellijst op
borrellijst = pd.DataFrame(data=borrellijst, columns=['Naam', 'Prijs', 'Winst'])
borrellijst = borrellijst.groupby(['Naam']).sum()
borrellijst = borrellijst.sort_index()
borrellijst.to_csv('borrellijst.csv')

# Sla grafiek op
plt.savefig('borrelgrafiek.png')

# Sla de prijshistorie van alle dranken op
prijshistorie = pd.DataFrame()
prijshistorie['Tijd'] = [time.strftime('%H:%M:%S', time.gmtime(t)) for t in tijd]
for drank in inventaris:
    prijshistorie[drank] = inventaris[drank].historie
for drank in inv_oud:
    prijshistorie[drank] = pd.Series(inv_oud[drank].historie)
prijshistorie.to_csv('borrelprijshistorie.csv')
