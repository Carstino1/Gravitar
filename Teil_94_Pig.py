import random


def würfeln(sp,pkt,zug=0):
  while True:
    wurf = random.randint(1, 6)
    zug = zug+wurf if wurf > 1 else 0
    print(f'Spieler {sp}: {wurf} gewürfelt, Punkte Zug = {zug:<2}, Punkte Gesamt = {pkt+zug} (Max = {max(punkte)})')
    if zug and input('Weiterwürfeln im Zug? (j/n) ').lower() == 'j': continue
    return zug


def rangliste(punkte):
  for p, s in sorted([(-p, s) for s, p in enumerate(punkte,start=1)]):
    print(f'Spieler {s} mit {-p} Punkten')
  print()    


MA_SP, MA_PKT = 9,50
anz_spieler = int(input(f'Wieviele Spieler (2-{MA_SP}) '))
punkte = [0]*anz_spieler

while max(punkte) < MA_PKT:
  for i, p in enumerate(punkte):
    punkte[i] += würfeln(i+1, p)
    rangliste(punkte)