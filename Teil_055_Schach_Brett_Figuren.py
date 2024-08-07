import pygame as pg
import chessdotcom as chess
import Teil_55_Schach_Zuggenerator as zuggen


def sz2xy(sz):
  return sz[0]*FELD, sz[1]*FELD

def xy2sz(xy):
  return xy[0]//FELD, xy[1]//FELD

def zeichneBrett(BRETT):
  for sz, feld in BRETT.items():
    farbe = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(screen, farbe, (*sz2xy(sz), FELD, FELD))

def fen2position(fen):
  position, s, z, rochaderecht = {}, 0, 0, ['','']
  figurenstellung, zugrecht, rochaderechte, enpassant, zug50, zugnr = fen.split()
  for char in figurenstellung:
    if char.isalpha():
      position[(s,z)] = char
      s += 1
    elif char.isnumeric():
      s += int(char)
    else:
      s, z = 0, z + 1
  for char in rochaderechte:
    if char == '-': break
    rochaderecht[char.isupper()] += char    
      
  return position, zugrecht, rochaderecht

def ladeFiguren():
  bilder = {}
  fig2datei = dict(r='br', n='bn', b='bb', q='bq', k='bk', p='bp',
                   R='wr', N='wn', B='wb', Q='wq', K='wk', P='wp')
  for fig, datei in fig2datei.items():
    bild = pg.image.load(f'Teil_49_Figuren/{datei}.png')
    bilder[fig] = pg.transform.smoothscale(bild, (FELD, FELD))
  return bilder  

def zeichneFiguren(p):
  for sz, fig in p.items():
    screen.blit(FIGUREN[fig], sz2xy(sz))

def zeichneZielfelder(zielfelder):
  for ziel in zielfelder:
    x, y = sz2xy(ziel)
    pg.draw.circle(screen, pg.Color('bisque4'), (x+50, y+50), 10)





pg.init()
BREITE, HÖHE = 800,800
FELD = BREITE // 8
FPS = 40
screen = pg.display.set_mode((BREITE, HÖHE))
FIGUREN = ladeFiguren()
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
#fen = chess.get_random_daily_puzzle().json['fen']
position,zugrecht,rochaderecht = fen2position(fen)
weiss = zugrecht == 'w'
print(f'{"Weiss" if weiss else "Schwarz"} ist am Zug')
züge, königspos = zuggen.zugGenerator(weiss, position, rochaderecht)
spieler = [False, True]

  

weitermachen = True
clock = pg.time.Clock()
drag = zugwechsel = spielende = False

while weitermachen:
  if spielende: break
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    elif ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
      von = xy2sz(pg.mouse.get_pos())
      if von in {z[1] for z in züge}:
        fig = position.pop(von)
        drag = FIGUREN[fig]
        zielfelder = {z[2] for z in züge if z[1] == von}
    elif ereignis.type == pg.MOUSEBUTTONUP and drag:
      zu = xy2sz(pg.mouse.get_pos())
      if zu in zielfelder:
        zug = [z for z in züge if z[1] == von and z[2] == zu][0]
        position[von] = fig
        zuggen.zug_ausführen(zug, position, königspos)
        zugwechsel = True
      else:
        position[von] = fig  
      drag = None
      
           
  screen.fill((0,0,0))
  zeichneBrett(zuggen.BRETT)
  zeichneFiguren(position)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
    zeichneZielfelder(zielfelder)
  pg.display.flip()

  if zugwechsel:
    weiss = not weiss
    züge, königspos = zuggen.zugGenerator(weiss, position, rochaderecht)
    if not züge:
      print(f'{"Weiss" if weiss else "Schwarz"} ist ', end='')
      if zuggen.imSchach(weiss, position, königspos[weiss]):
        print('Matt')
      else:
        print('Patt')
      zugwechsel = False
      spielende = True
    elif spieler[weiss]:
      beste_bewertung, bester_zug = zuggen.minimax(0, -999999, 999999, weiss, position, rochaderecht)
      zuggen.zug_ausführen(bester_zug, position, königspos)
    else:
      zugwechsel = False        
  
pg.quit()