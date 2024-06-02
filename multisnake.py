""" Snake-Spiel aus dem Kurs "Programmieren lernen mit Python" von openHPI
    https://open.hpi.de/courses/pythonjunior2020
"""

import turtle
import random
import time



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
        for segment in self.segmente:
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
    def __init__(self, spielername, spielfeld: Spielfeld):
        self.feld = spielfeld   # nur Spieler mit der selben Spielfeldgröße können zusammenspielen
        self.essen = erstelle_turtle(0, 100, 0, "circle", "red")
        self.lokaler_spieler = Spieler(spielername, "orange")
        self.netzwerk_spieler = []

    def spiel_neustarten(self, spieler):
        # Kopf in der Mitte platzieren
        spieler.reset()
        # Ausgabe, dass Spielrunde vorbei ist
        print("Game Over")

    def checke_kollision_mit_segmenten(self, spieler):
        for segment in spieler.segmente:
            if segment.distance(spieler.kopf) < spielfeld.objekt:
                spiel.spiel_neustarten(spieler)

    def checke_kollision_mit_essen(self, spieler):
        if spieler.kopf.distance(self.essen) < spielfeld.objekt:
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

            # Schlange wachsen lassen
            neues_segment = turtle.Turtle()
            neues_segment.shape("square")
            neues_segment.color(spieler.farbe)
            neues_segment.speed(0)
            neues_segment.penup()

            spieler.segmente.append(neues_segment)

    def interpretiere_eingabe(self, x, y):
        if spielfeld.wurde_runter_geklickt(x, y):
            self.lokaler_spieler.nach_unten_ausrichten()
        elif spielfeld.wurde_rechts_geklickt(x, y):
            self.lokaler_spieler.nach_rechts_ausrichten()
        elif spielfeld.wurde_hoch_geklickt(x, y):
            self.lokaler_spieler.nach_oben_ausrichten()
        elif spielfeld.wurde_links_geklickt(x, y):
            self.lokaler_spieler.nach_links_ausrichten()

    def wiederhole_spiellogik(self):
        # Damit das Spiel bis zu einer Niederlage läuft, wird der folgende
        # Code von wiederhole_spiellogik() in einer Endlosschleife aufgerufen
        while True:
            self.checke_kollision_mit_essen(self.lokaler_spieler)
            self.checke_kollision_mit_fensterrand(self.lokaler_spieler)

            self.lokaler_spieler.koerper_bewegen()
            self.lokaler_spieler.kopf_bewegen()
            self.checke_kollision_mit_segmenten(self.lokaler_spieler)

            # schicke den stand des spiels
            # broadcast game status...

            # Position der verschiedenen Turtle-Elemente aktualisieren
            turtle.update()

            # time.sleep() unterbricht die Ausführung des weiteren
            # Codes für die angegebene Anzahl an Sekunden
            # An dieser Stelle verlangsamt sleep() das Spiel, damit die Schlange
            # nicht aus dem Bildschirm laufen kann, bevor man sie sehen kann.
            time.sleep(0.05)

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

spielername = 'Daniel' # input('Name eingeben:')
spielfeld = Spielfeld(920, 920)
spiel = Spiel(spielername, spielfeld)

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

# Turtle in der Mitte verbergen
turtle.hideturtle()

# Automatisches Aktualisieren der Turtle-Elemente ausschalten
turtle.tracer(False)

# Try-Except-Block fängt Beenden des Spiels ab
try:
    spiel.wiederhole_spiellogik()
except turtle.Terminator:
    print("Das Spiel wurde beendet.")
    # exit(0) beendet das Program sauber
    exit(0)
