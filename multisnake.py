""" Snake-Spiel aus dem Kurs "Programmieren lernen mit Python" von openHPI
    https://open.hpi.de/courses/pythonjunior2020
"""

import turtle
import random
import time
import json
from game_broadcaster import GameBroadcaster


class Spielfeld:
    def __init__(self, breite=400, hoehe=400, objekt=20):
        self.breite = breite
        self.hoehe = hoehe
        self.objekt = objekt
        self.rand = 20
        self.min_x = -breite/2
        self.max_x = breite/2
        self.min_y = -hoehe/2
        self.max_y = hoehe/2
        self.puffer = self.rand/2

    def serialize(self) -> str:
        return json.dumps({'breite': self.breite,
                           'hoehe': self.hoehe,
                           'objekt': self.objekt})

    def erstelle_schaltflaechen(self):
        self.nach_rechts = erstelle_turtle(spielfeld.max_x - spielfeld.rand, spielfeld.min_y + spielfeld.objekt + spielfeld.rand,
                                 0)
        self.nach_unten = erstelle_turtle(spielfeld.max_x - spielfeld.rand - spielfeld.objekt, spielfeld.min_y + spielfeld.rand,
                                90)
        self.nach_oben = erstelle_turtle(spielfeld.max_x - spielfeld.rand - spielfeld.objekt,
                               spielfeld.min_y + spielfeld.rand + 2 * spielfeld.objekt, -90)
        self.nach_links = erstelle_turtle(spielfeld.max_x - spielfeld.rand - 2 * spielfeld.objekt,
                                spielfeld.min_y + spielfeld.rand + spielfeld.objekt, 180)

    def wurde_geklickt(self, t: turtle.Turtle, x, y):
        o2 = self.objekt/2
        return (t.xcor()-o2) <= x <= (t.xcor()+o2) and (t.ycor()-o2) <= y <= (t.ycor()+o2)
    def wurde_runter_geklickt(self, x, y):
        return self.wurde_geklickt(self.nach_unten, x, y)

    def wurde_hoch_geklickt(self, x, y):
        return self.wurde_geklickt(self.nach_oben, x, y)

    def wurde_rechts_geklickt(self, x, y):
        return self.wurde_geklickt(self.nach_rechts, x, y)

    def wurde_links_geklickt(self, x, y):
        return self.wurde_geklickt(self.nach_links, x, y)


    def random_x_pos(self):
        pos_idx = self.breite / self.objekt / 2 - 1
        return random.randint(-pos_idx, pos_idx) * self.objekt

    def random_y_pos(self):
        pos_idx = self.hoehe / self.objekt / 2 - 1
        return random.randint(-pos_idx, pos_idx) * self.objekt


class Spieler:
    def __init__(self, name, farbe):
        self.name = name
        self.farbe = farbe
        self.kopf = erstelle_turtle(0, 0, 0, "square", "black")
        self.segmente = []

    def wachsen(self):
        neues_segment = turtle.Turtle()
        neues_segment.shape("square")
        neues_segment.color(self.farbe)
        neues_segment.speed(0)
        neues_segment.penup()

        self.segmente.append(neues_segment)

    def serialize(self) -> str:
        return json.dumps({'name': self.name,
                           'farbe': self.farbe,
                           'kopf': serialize_turtle(self.kopf),
                           'segmente': [serialize_turtle(t) for t in self.segmente]})

    def nach_unten_ausrichten(self):
        if self.kopf.direction != "up":
            self.kopf.direction = "down"

    def nach_rechts_ausrichten(self):
        if self.kopf.direction != "left":
            self.kopf.direction = "right"

    def nach_links_ausrichten(self):
        if self.kopf.direction != "right":
            self.kopf.direction = "left"

    def nach_oben_ausrichten(self):
        if self.kopf.direction != "down":
            self.kopf.direction = "up"

    def kopf_bewegen(self):
        if self.kopf.direction == "down":
            y = self.kopf.ycor()
            self.kopf.sety(y - 20)

        elif self.kopf.direction == "right":
            x = self.kopf.xcor()
            self.kopf.setx(x + 20)

        elif self.kopf.direction == "left":
            x = self.kopf.xcor()
            self.kopf.setx(x - 20)

        elif self.kopf.direction == "up":
            y = self.kopf.ycor()
            self.kopf.sety(y + 20)

    def koerper_bewegen(self):
        for index in range(len(self.segmente) - 1, 0, -1):
            # Bewege segmente[index] an segmente[index - 1]
            self.segmente[index].setx(self.segmente[index - 1].xcor())
            self.segmente[index].sety(self.segmente[index - 1].ycor())

        # Überprüfe, ob Schlange nicht nur aus Kopf besteht
        if len(self.segmente) > 0:
            # Wenn, dann bewege erstes Segment zum Kopf
            self.segmente[0].setx(self.kopf.xcor())
            self.segmente[0].sety(self.kopf.ycor())

    def segmente_entfernen(self):
        # Verstecke und entferne Segmente
        while len(self.segmente) > 0:
            segment = self.segmente.pop()
            segment.hideturtle()
            del segment
        self.segmente.clear()

    def reset(self):
        self.kopf.setx(0)
        self.kopf.sety(0)
        # Richtung auf "stop" setzen
        self.kopf.direction = "stop"
        self.segmente_entfernen()


class Spiel:
    def __init__(self, spielername, spielfeld: Spielfeld, fps=20):
        self.feld = spielfeld   # nur Spieler mit der selben Spielfeldgröße können zusammenspielen
        self.fps = fps
        self.essen = erstelle_turtle(0, 100, 0, "circle", "red")
        self.netzwerk_essen = {}
        self.lokaler_spieler = Spieler(spielername, "orange")
        self.netzwerk_spieler = {}
        self.netzwerk_spieler_letzter_kontakt = {}
        self.netzwerk_spieler_timeout = 5 # 5 sekunden

    def verschiebe_essen(self):
        # Essen an neue Position bewegen
        steuerfelder_x = spielfeld.max_x - spielfeld.rand - 2 * spielfeld.objekt
        steuerfelder_y = spielfeld.min_y + spielfeld.rand + 2 * spielfeld.objekt
        x = steuerfelder_x
        y = steuerfelder_y

        while x >= steuerfelder_x and y <= steuerfelder_y:
            x = spielfeld.random_x_pos()
            y = spielfeld.random_y_pos()

        self.essen.setx(x)
        self.essen.sety(y)

    def serialize(self) -> str:
        return json.dumps({
            "feld": self.feld.serialize(),
            "fps": self.fps,
            "essen": serialize_turtle(self.essen),
            "spieler": self.lokaler_spieler.serialize()
        })

    def deserialize(self, data, sender):
        # print(f'received game data from {sender}: {data}')
        # speichere letzten kontakt zu netzwerk spieler
        self.netzwerk_spieler_letzter_kontakt[sender] = time.time()

        # deserialisiere daten
        data = json.loads(data)
        # checke kompatibilität
        if self.ist_kompatibel(data):
            # spiel daten sind kompatibel - deserialisiere
            # essen
            ed = json.loads(data['essen'])
            if sender in self.netzwerk_essen:
                # aktualisiere
                essen: turtle.Turtle = self.netzwerk_essen[sender]
                essen.setx(ed['x'])
                essen.sety(ed['y'])
            else:
                # erstelle neues essens turtle - immer grün
                self.netzwerk_essen[sender] = erstelle_turtle(ed['x'], ed['y'], 0, ed['shape'], 'green')

            # spieler
            sd = json.loads(data['spieler'])
            if sender not in self.netzwerk_spieler:
                self.netzwerk_spieler[sender] = Spieler(sd['name'], sd['farbe'])

            spieler = self.netzwerk_spieler[sender]
            # aktualisiere
            kopf = json.loads(sd['kopf'])
            spieler.kopf.setx(kopf['x'])
            spieler.kopf.sety(kopf['y'])
            seg = sd['segmente']
            while len(seg) < len(spieler.segmente):
                # zu viele segmente - entferne
                s: turtle.Turtle = spieler.segmente.pop()
                s.hideturtle()
                del s

            while len(seg) > len(spieler.segmente):
                # zu wenige segmente - hinzufuegen
                spieler.segmente.append(erstelle_turtle(0, 0, 0, 'square', 'cyan'))#sd['farbe']))

            # aktualisiere segment positionen
            for i in range(len(spieler.segmente)):
                seg_i = json.loads(seg[i])
                s: turtle.Turtle = spieler.segmente[i]
                s.setx(seg_i['x'])
                s.sety(seg_i['y'])


    def ist_kompatibel(self, spieldaten) -> bool:
        # deserialisiere spielfeld daten
        feld_daten = json.loads(spieldaten['feld'])

        return (spieldaten['fps'] == self.fps and feld_daten['breite'] == self.feld.breite and
                feld_daten['hoehe'] == self.feld.hoehe and feld_daten['objekt'] == self.feld.objekt)

    def spiel_neustarten(self, spieler):
        # Ausgabe, dass Spielrunde vorbei ist
        print(f'Game Over, Punkte: {len(spieler.segmente)}')
        if len(self.netzwerk_spieler) > 0:
            print('Punkte der anderen Spieler:')
            for spieler in self.netzwerk_spieler.values():
                print(f'{spieler[1].name} ({spieler[0]}): {len(spieler[1].segmente)}')


        # lokalen spieler zurücksetzen
        spieler.reset()

        while len(self.netzwerk_essen) > 0:
            essen = self.netzwerk_essen.pop()
            essen[1].hideturtle()
            del essen
        self.netzwerk_essen.clear()

        self.verschiebe_essen()


    def checke_kollision_mit_segmenten(self):
        # checke kollision mit eigenen segmenten
        for segment in self.lokaler_spieler.segmente:
            if segment.distance(self.lokaler_spieler.kopf) < self.feld.objekt:
                self.spiel_neustarten(self.lokaler_spieler)

        # checke kollision mit anderen spielern
        for spieler in self.netzwerk_spieler.values():
            for segment in spieler.segmente:
                if segment.distance(self.lokaler_spieler.kopf) < self.feld.objekt:
                    self.spiel_neustarten(self.lokaler_spieler)

    def checke_kollision_mit_essen(self):
        # checke lokaler spieler und netzwerk essen
        for essen in self.netzwerk_essen.values():
            if self.lokaler_spieler.kopf.distance(essen) < self.feld.objekt:
                self.lokaler_spieler.wachsen()

        # checke lokaler spieler und lokales essen
        if self.lokaler_spieler.kopf.distance(self.essen) < self.feld.objekt:
            self.verschiebe_essen()
            self.lokaler_spieler.wachsen()

        # checke netzwerk spieler und lokales essen
        for spieler in self.netzwerk_spieler.values():
            if spieler.kopf.distance(self.essen) < self.feld.objekt:
                self.verschiebe_essen()

    def interpretiere_eingabe(self, x, y):
        if spielfeld.wurde_runter_geklickt(x, y):
            self.lokaler_spieler.nach_unten_ausrichten()
        elif spielfeld.wurde_rechts_geklickt(x, y):
            self.lokaler_spieler.nach_rechts_ausrichten()
        elif spielfeld.wurde_hoch_geklickt(x, y):
            self.lokaler_spieler.nach_oben_ausrichten()
        elif spielfeld.wurde_links_geklickt(x, y):
            self.lokaler_spieler.nach_links_ausrichten()

    def entferne_inaktive_netzwerkspieler(self):
        now = time.time()
        for (sender, letzter_kontakt) in self.netzwerk_spieler_letzter_kontakt.items():
            if now - letzter_kontakt > self.netzwerk_spieler_timeout and sender in self.netzwerk_essen:
                if sender in self.netzwerk_essen:
                    sender[1].hideturtule()
                    del self.netzwerk_essen[sender]
                if sender in self.netzwerk_spieler:
                    sender[1].reset()
                    del self.netzwerk_spieler[sender]


    def wiederhole_spiellogik(self):
        # Damit das Spiel bis zu einer Niederlage läuft, wird der folgende
        # Code von wiederhole_spiellogik() in einer Endlosschleife aufgerufen
        single_loop_time = 1/self.fps
        update_time = 0.05  # time reserved to update the turtle objects at the end

        while True:
            loop_finish_time = time.time() + single_loop_time

            self.checke_kollision_mit_essen()
            self.checke_kollision_mit_fensterrand(self.lokaler_spieler)

            self.lokaler_spieler.koerper_bewegen()
            self.lokaler_spieler.kopf_bewegen()
            self.checke_kollision_mit_segmenten()

            # broadcast serialized game status
            gb.broadcast_game(self.serialize())

            # receive game status broadcasted by other players
            while time.time() < loop_finish_time - update_time:
                data, sender = gb.receive_game_broadcasts()
                if data is None:
                    time.sleep(0.01)
                else:
                    # deserialize data
                    self.deserialize(data, sender)

            self.entferne_inaktive_netzwerkspieler()

            # Position der verschiedenen Turtle-Elemente aktualisieren
            turtle.update()


    def checke_kollision_mit_fensterrand(self, spieler: Spieler):
        if (spieler.kopf.xcor() > spielfeld.max_x-spielfeld.rand/2
                or spieler.kopf.xcor() < spielfeld.min_x+spielfeld.rand/2
                or spieler.kopf.ycor() > spielfeld.max_y-spielfeld.rand/2
                or spieler.kopf.ycor() < spielfeld.min_y+spielfeld.rand/2):
            spiel.spiel_neustarten(spieler)

# erstelle_turtle() verkürzt die Schreibarbeit für
# die Erstellung der verschiedenen Turtles im Spiel.
#
# Den letzten zwei Parametern von erstelle_turtle() wurden sogenannte
# Standardwerte hinzugefügt. Standardwerte (auch: default values) werden
# für die jeweiligen Parameter beim Aufruf der Funktion automatisch
# eingesetzt, wenn der Funktion nicht explizit Argumente für diese Parameter
# mitgegeben werden. Da die Steuerungsdreiecke die Mehrheit der
# Turtle-Elemente darstellen, wurden eine Dreiecksform und eine grüne
# Füllfarbe als Standardwerte für die Parameter shape und color gewählt.
def erstelle_turtle(x, y, rotationswinkel, shape="triangle", color="green"):
    element = turtle.Turtle()
    element.speed(0)  # Keine Animation, Turtle "springt" zum Zielpunkt
    element.shape(shape)
    element.color(color)
    element.right(rotationswinkel)  # Nur für grüne Steuerungsdreiecke relevant
    element.penup()
    element.goto(x, y)

    # Nur für Kopf relevant; "direction" ist nicht aus Turtle,
    # sondern eine Variable von uns, die wir "element" dynamisch zuweisen
    element.direction = "stop"

    return element

def serialize_turtle(t: turtle.Turtle) -> str:
    return json.dumps({'x': t.xcor(),
                       'y': t.ycor(),
                       'color': t.color(),
                       'shape': t.shape()})

def zeichne_rand():
    # gehe in linke untere ecke
    turtle.penup()
    turtle.setx(spielfeld.min_x + spielfeld.rand / 2)
    turtle.sety(spielfeld.min_y + spielfeld.rand / 2)
    # zeichne rand
    turtle.pendown()
    turtle.forward(spielfeld.breite - spielfeld.rand)
    turtle.left(90)
    turtle.forward(spielfeld.hoehe - spielfeld.rand)
    turtle.left(90)
    turtle.forward(spielfeld.breite - spielfeld.rand)
    turtle.left(90)
    turtle.forward(spielfeld.hoehe - spielfeld.rand)


# Automatisches Aktualisieren der Turtle-Elemente ausschalten
turtle.tracer(False)

spielername = 'Daniel' # input('Name eingeben:')
spielfeld = Spielfeld(920, 920)
spiel = Spiel(spielername, spielfeld, 8)
gb = GameBroadcaster()

# Auf dem Spielfeld sichtbare Elemente definieren
spielfeld.erstelle_schaltflaechen()

# Spielbereich (das sich öffnende Fenster beim Ausführen dieser Datei) definieren
spielbereich = turtle.Screen()
spielbereich.title(f'Mein Snake-Spiel ({spielername})')
spielbereich.setup(width=spielfeld.breite+spielfeld.rand, height=spielfeld.hoehe+spielfeld.rand)

# Drücken der Pfeiltasten zur Richtungssteuerung registrieren
spielbereich.onkeypress(spiel.lokaler_spieler.nach_oben_ausrichten, "Up")
spielbereich.onkeypress(spiel.lokaler_spieler.nach_links_ausrichten, "Left")
spielbereich.onkeypress(spiel.lokaler_spieler.nach_unten_ausrichten, "Down")
spielbereich.onkeypress(spiel.lokaler_spieler.nach_rechts_ausrichten, "Right")
spielbereich.listen(0)

# Registrierung der Richtungssteuerung über das Anklicken der grünen Dreiecke
turtle.onscreenclick(spiel.interpretiere_eingabe)

zeichne_rand()

# Turtle in der Mitte verbergen
turtle.hideturtle()



# Try-Except-Block fängt Beenden des Spiels ab
try:
    spiel.wiederhole_spiellogik()
except turtle.Terminator:
    print("Das Spiel wurde beendet.")
    # exit(0) beendet das Program sauber
    exit(0)
