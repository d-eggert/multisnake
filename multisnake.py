""" Snake-Spiel aus dem Kurs "Programmieren lernen mit Python" von openHPI
    https://open.hpi.de/courses/pythonjunior2020
"""

import turtle
import random
import time


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


def nach_unten_ausrichten():
    if kopf.direction != "up":
        kopf.direction = "down"


def nach_rechts_ausrichten():
    if kopf.direction != "left":
        kopf.direction = "right"


def nach_links_ausrichten():
    if kopf.direction != "right":
        kopf.direction = "left"


def nach_oben_ausrichten():
    if kopf.direction != "down":
        kopf.direction = "up"


def interpretiere_eingabe(x, y):
    if 150 <= x <= 170 and -190 <= y <= -170:
        nach_unten_ausrichten()
    elif 170 <= x <= 190 and -170 <= y <= -150:
        nach_rechts_ausrichten()
    elif 150 <= x <= 170 and -150 <= y <= -130:
        nach_oben_ausrichten()
    elif 130 <= x <= 150 and -170 <= y <= -150:
        nach_links_ausrichten()


def kopf_bewegen():
    if kopf.direction == "down":
        y = kopf.ycor()
        kopf.sety(y - 20)

    elif kopf.direction == "right":
        x = kopf.xcor()
        kopf.setx(x + 20)

    elif kopf.direction == "left":
        x = kopf.xcor()
        kopf.setx(x - 20)

    elif kopf.direction == "up":
        y = kopf.ycor()
        kopf.sety(y + 20)


def koerper_bewegen():
    for index in range(len(segmente) - 1, 0, -1):
        # Bewege segmente[index] an segmente[index - 1]
        segmente[index].setx(segmente[index - 1].xcor())
        segmente[index].sety(segmente[index - 1].ycor())

    # Überprüfe, ob Schlange nicht nur aus Kopf besteht
    if len(segmente) > 0:
        # Wenn, dann bewege erstes Segment zum Kopf
        segmente[0].setx(kopf.xcor())
        segmente[0].sety(kopf.ycor())


def segmente_entfernen():
    # Verstecke und entferne Segmente
    for segment in segmente:
        segment.hideturtle()
        del segment
    segmente.clear()


def spiel_neustarten():
    # Kopf in der Mitte platzieren
    kopf.setx(0)
    kopf.sety(0)
    # Richtung auf "stop" setzen
    kopf.direction = "stop"
    segmente_entfernen()
    # Ausgabe, dass Spielrunde vorbei ist
    print("Game Over")


def checke_kollision_mit_fensterrand():
    if kopf.xcor() > 190 or kopf.xcor() < -190 or kopf.ycor() > 190 or kopf.ycor() < -190:
        spiel_neustarten()


def checke_kollision_mit_segmenten():
    for segment in segmente:
        if segment.distance(kopf) < 20:
            spiel_neustarten()


def checke_kollision_mit_essen():
    if kopf.distance(essen) < 20:
        # Essen an neue Position bewegen
        x = 140
        y = -140

        while x >= 140 and y <= -140:
            x = random.randint(-9, 9) * 20
            y = random.randint(-9, 9) * 20

        essen.setx(x)
        essen.sety(y)

        # Schlange wachsen lassen
        neues_segment = turtle.Turtle()
        neues_segment.shape("square")
        neues_segment.color("yellow")
        neues_segment.speed(0)
        neues_segment.penup()

        segmente.append(neues_segment)

def wiederhole_spiellogik():
    # Damit das Spiel bis zu einer Niederlage läuft, wird der folgende
    # Code von wiederhole_spiellogik() in einer Endlosschleife aufgerufen
    while True:
        checke_kollision_mit_essen()
        checke_kollision_mit_fensterrand()

        koerper_bewegen()
        kopf_bewegen()
        checke_kollision_mit_segmenten()

        # Position der verschiedenen Turtle-Elemente aktualisieren
        turtle.update()

        # time.sleep() unterbricht die Ausführung des weiteren
        # Codes für die angegebene Anzahl an Sekunden
        # An dieser Stelle verlangsamt sleep() das Spiel, damit die Schlange
        # nicht aus dem Bildschirm laufen kann, bevor man sie sehen kann.
        time.sleep(0.15)


spielername = input('Name eingeben:')

# Auf dem Spielfeld sichtbare Elemente definieren
rechts = erstelle_turtle(180, -160, 0)
unten = erstelle_turtle(160, -180, 90)
oben = erstelle_turtle(160, -140, -90)
links = erstelle_turtle(140, -160, 180)

essen = erstelle_turtle(0, 100, 0, "circle", "red")
kopf = erstelle_turtle(0, 0, 0, "square", "black")
segmente = []

# Spielbereich (das sich öffnende Fenster beim Ausführen dieser Datei) definieren
spielbereich = turtle.Screen()
spielbereich.title(f'Mein Snake-Spiel ({spielername})')
spielbereich.setup(width=1024, height=1024)

# Drücken der Pfeiltasten zur Richtungssteuerung registrieren
spielbereich.onkeypress(nach_oben_ausrichten, "Up")
spielbereich.onkeypress(nach_links_ausrichten, "Left")
spielbereich.onkeypress(nach_unten_ausrichten, "Down")
spielbereich.onkeypress(nach_rechts_ausrichten, "Right")
spielbereich.listen(0)

# Registrierung der Richtungssteuerung über das Anklicken der grünen Dreiecke
turtle.onscreenclick(interpretiere_eingabe)

# Turtle in der Mitte verbergen
turtle.hideturtle()

# Automatisches Aktualisieren der Turtle-Elemente ausschalten
turtle.tracer(False)

# Try-Except-Block fängt Beenden des Spiels ab
try:
    wiederhole_spiellogik()
except turtle.Terminator:
    print("Das Spiel wurde beendet.")
    # exit(0) beendet das Program sauber
    exit(0)
