BEDIENUNGSANLEITUNG 

---INSTALLATION----
- gehe in die Eingabeaufforderung
- gebe ein <pip install monke2>
- um das Paket in ein Python Notebook einzubinden gebe ein <import monke> 

- Am besten wird dieses Paket mit VS Code genutzt, falls man Plots und Tabellen ausdrucken will,
 da diese Paket es ermöglicht, Tabellen und Plots mit geringem Aufwand in einer LaTeX Datei zu verpacken und dies eine
Hilfestellung. Da man LaTeX mit VS Code nutzen kann, wird hiermit der Arbeitsaufwand minimiert.


----Geraden-Fits----

- Als erstes muss ein Objekt linear_fit() definiert werden 
- anschließend muss der y-Fehler mit set_y_error() definiert werden
- mit der funktion make_fit() kann ein Geraden-Fit erstellt werden

Beispiel code:
----------------------------------
from monke.fit import linear_fit

myfit = linear_fit()
myfit.set_y_error(y_err)
result = myfit.make_fit(x, y)

ax = myfit.plot()

# ax.set_axisbelow(True)     
# ax.grid()
# Diese zwei Zeilen fügen ein Grid hinzu
----------------------------------

--Variablen--
Variablen gehören alle zum Objekt linear_fit()
Beispiel (änderen den Wert der Variable var):
-----------------------
myift = linear_fit()
myfit.var = 1
----------------------
Dieses Schema gilt für alle Variablen:

- detail: (boolean), bei True werden extra-infos ausgegeben, bei False nicht
- m_round: (integer), gibt an, auf welche Nachkommastelle die Steigung m gerundet wird
- n_round: (integer), gibt an, auf welche Nachkommastelle der Achsenabschnitt n gerundet wird
- textloc: (string), bestimme, in welche Ecke der Infokasten des Graphen gesetzt wird. 
    -verfügbare Optionen: 'upper right', 'upper left', 'lower right', 'lower left'
- plotsize: (tupel), bestimme die Größe des Diagramms
- errbar: (5d List [marker, caps, eline, markerwidth, shape]), 5 Parameter die das Aussehen der Fehlerbalken ändern
    - MARKER: (float), ändere die Größe der marker der Fehlerbalken
    - CAPS: (float), ändere die Länge der oberen und unteren Striche der Fehlerbalken
    - ELINE: (float), ändere die Dicke der Fehlerbalken
    - MARKERWIDTH: (float), ändere die Dicke der oberen und unteren Striche der Fehlerbalken
    - SHAPE: (string), ändere die Form der Fehlerbalken
        - 's' für Quadrat
        - 'o' für Kreis
        - 'd' für Raute
        - 'x' für x
        - 'v' für Dreieck
- ANCH: (float), ändere die Größe der Infobox
- legendsize (float): Größe der Legende 
- legend_label (string-Liste): Element 0 ist der Legendentext für die Fit-Gerade, Element 1 für die Messwerte
- style: (string oder string-Liste), ändert den Style des Diagramms
- size: (float), ändert die Schriftgrößen im Diagramm
- colors: (4d list [string, stringt, string, string]), ändert die Farben im Diagramm
    - 0: Fehlerbalken
    - 1: Fit-Geraden
    - 2: Fehlerkurven
    - 3: Füllraum
- xlim und ylim: (tupel), setzt die Grenzen der x- oder y-Achse
- xticks und yticks (array oder list): beschriftet die jeweilige achse mit Zahlen 
- xrotation und yrotation (float zwischen 0 - 90): rotiert die Achsenbeschriftung
- dpi (integer): ändert die Qualität des Plots (je höher desto besser)

--Funktionen--
Funktionen gehören zum Objekt linear_fit()

- set_y_error(yerr,var=True): setze den y-Fehler. yerr kann ein Array oder eine Zahl sein. Wenn var==True, dann wird
     varianzgewichtet gerechnet
- set_x_error(xerr): setze den x-Fehler. wird automatisch varianzgewichtet
- make_fit(x_vals,y_vals, r=2, hide=False, name ) berechnet die Fit-Gerade mit Fehlern. r beschreibt die Nachkommastelle, auf die gerundet wird. hide versteckt die Ergebnisausgabe.
    diese Funktion gibt ein Dictionary wieder. Wichtige Einträge aus dem dict: 'm' und 'merr' sind Steigung und dessen Fehler,
    'n' und 'nerr' sind Achsenabschnitt und dessen Fehler. 'name' ist der Name der bei der Infoanzeige ausgegeben wird und bei der Multiplot Funktion in der Legende gebraucht wird.
- plot(title='title',xlabel='x_Achse',ylabel='y_achse',err=True,legend = True, infos=False, name='', scale = 0.7, grid = False): 
    bei err=True werden Fehlerbalken eingefügt, name ist der Name der Datei (nur wenn einer angegeben wird, wird die Datei gespeichert);
    mit legend=True kann man die Legende anmachen; mit infos=True kann man steigung und achsenabschnitt anzeigen lassen.
    Falls die Datei gespeichert wird, wird sie automatisch in einer LaTeX-Datei abespeichert. Mit <scale> lässt sich die Größe ändern.
    Bei <grid = True> wird im plot ein Grid in den Hintergrund eingefügt.
- add_plot(x, y,label='',colors=['tab:green','tab:purple','tab:orange']) fügt zusätzliche Plots hinzu. x und y können 2d- Arrays oder Listen sein, um mehrere Plots
 	einzufügen. mit label kann man die Namen in der Legende bestimmen, mit colors die Farben. MUSS im code VOR der plot()-Funktion stehen, damit es hinzugefügt werden kann.
- function_label(error_mode = 'plus-minus') Bei der Legende kann für das Label des Geraden-Fits die Funktion f = mx + n 
    ausgegeben werden. error_mode = 'plus-minus', 'parenthesis' oder 'scientific', dies kann jedoch ignoriert werden.


----------------Multiplot-----------------
die Funktion multiplot() ermöglicht es einem, mehrere Geraden-Fits in einen Plot einzufügen.
Beispielcode für zwei Fits:
----------------------------------
# x,y und err sind Arrays mit den Messwerten
from monke.fit import linear_fit
import monke.fit as fit

fit1 = linear_fit()
fit1.set_y_error(err)
result1 = fit1.make_fit(x1,y1)

fit2 = linear_fit()
fit2.set_y_error(err)
result2 = fit2.make_fit(x2,y2)

results = [result1, result2]
ax = fit.multiplot(results)

# ax.set_axisbelow(True)     
# ax.grid()
# Diese zwei Zeilen fügen ein Grid hinzu
----------------------------------
multiplot(result, title = 'Titel', xlabel = 'x-Achse', ylabel = 'y-Achse', color = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange', 'tab:cyan'] , name = None, scale = 0.7, figsize = (7, 5.5), fontsize = 16, legendsize = 11, xrotation = 0, yrotation = 0, 
             custom = False, errbar = [7,5,1,1], symbols = ['x', 'o', 'v'], linestyle = '-'):
        
- result ist eine Liste mit allen dictionaries, die von der Funktion make_fit() ausgegeben werden (siehe Beispiel). 
- title, xlabel, ylabel sind die für den Plot entsprechenden Beschriftungen.
- color ist ein Array von Farben, die für die Geraden genutzt werden.
- wenn für name ein string-Wert eingegeben wird, dann wird mit diesen Namen die Datei gespeichert und in die LaTeX-Datei eingefügt
- scale ist die relative Größe in der LaTeX-Datei
- figsize sind die Dimensionen des Plots
- fontsize bestimmt die Schriftgröße
- legendsize bestimt die Größe der Legende
- x- und yroation lässt die Beschriftungen um den eingegebenen Winkel rotieren
- bei custom == True lassen sich die Größen der einzelnen Schrift-Elemente manuell einstellen
- errbar funktioniert wie bei der plot()-Funktion von <linear_fit()>
- symbols ist ein Array mit den Symbolen der Fehlerbalen. Möglich sind 's', 'o', 'd', 'x' und 'v'
- linestyle besimmt den Stil der Geraden (durchgezogene Linie, gestrichelt usw.)


-- Liste aller Konstanten --
-----------------------------------------
c   # Lichtgeschwindigkeit
q   # Elementarladung
mu0 # Magnetische Feldkonstante
e0  # Elektrische Feldkonstante
kc  # Coulomb-Konstante
h   # Planckes Wirkungsquantum
G   # Gravitationskonstante
m_planck  # Planck Masse
l_planck  # Planck Länge
t_planck  # Planck Zeit
T_planck  # Planck Temperatur
kb    # Boltzmann Konstante
sb    # Stefan Boltzmann Konstante
me    # Elektronenmasse
lc    # Compton Wellenlänge
re    # klassischer Elektronenradius
R_inf # Rydberg konstante
R_c   # Rydberg Frequenz
N_A   # Avogadro Konstante
F     # Faraday Konstante
R     # Gaskonstante
Vm0   # Molares Volumen eines idealen Gases
g     # Erdbeschleunigung
u     # atomare Masseneinheit
-----------------------------------------

------Plots------

<monke.plots> enthält einige Funktionen, die einem Aufgaben mit dem Modul matplotplib.pyplot erleichtern

--Funktionen--
- errorbar(ax, x_val,y_val,y_err,x_err=[0],errbar=[7,5,1,1,'x'],color='tab:red',line='',label='Daten'):
    macht dasgleiche wie pyplot.errbar, jedoch sind die Fehlerbalken visuell angepasst, um einem Arbeit zu ersparen.
    die variable <errbar> funktioniert analog zur gleichen Variable beim Geraden-Fit.
- style(): 
    passt den standard stil von pyplot an
- legend(ax):
    entfernt bei der Legende zuätzliche Fehlerbalken. ax ist das plot objekt von Pyplot (z.B aus <fig, ax = pyplot.subplots()>)
- savefig(name, dpi=300, scale = 0.7):
    hat dieselbe Funktion wie pyplot.savefig, nur das hiermit der gespeicherte Plot automatisch in der LaTeX-Datei abgespeichert


-------functions-----------

<monke.functions> bietet weitere nützliche Funktionen wie LaTeX, Tabellen erstellen, wo Messwerte automatisch gerundet werden.

--Funktionen--

- roundup(x,r=2):
    rundet die eingegebenen Werte automatisch auf (nützlich für Mess-Unsicherheiten), <r> ist die gewünschte Nachkommastelle.
    Dies Funktioniert mit float und int zahlen sowie mit Arrays.
- varianz_xy(x, y):
    berechnet die xy Varianz zweier Arrays
- varianz_x(x): 
    berechnet die Varianz eines Arrays
- gcd(a, b):
    Größter gemeinsamer Teiler zweier Zahlen
- gcd_array(array):
    Größter gemeinsamer Teiler eines Arrays
- error_round(x, xerr, error_mode = 'plus-minus', get_float = False):
    bei eingabe zweier Arrays (erstes für Messwerte und zweites für die Unsicherheiten) werden zwei String-Listen ausgegeben mit den gerundeten Werten.
    Die Unsicherheiten Werden auf erste (oder zweite) signifikante Stelle gerundet und die Ausgabe der Messwerte dementsprechend angepasst.
    - error_mode = 'plus-minus': Ausgabe von zwei einzelnen Arrays (bei <get_float = True> werden float-Listen ausgegeben)
    - error_mode = 'parenthesis': Ausgabe eines einzlen Arrays, wo bei den Messwerten die Fehler in Klammern stehen. (Bsp.: Zahl = 1.03(2) = 1.03 +- 0.02)
    - error_mode = 'scientific': Ausdgabe zweier Arrays, das erste ist gleich wie bei 'parenthesis', nur im wissenschaftlichen Format (0.03(2) = 3(2)e-2) 
        	das Zweite arrays gibt einem die jeweilige Potenz an
- make_table(array,header ='',align = '', caption = None, latex=True, transpose = False, error_mode = 'plus-minus'):
    erstellt eine LaTeX Tabelle, die automatisch in eine LaTeX-Datei gepackt wird. 
    - array: ist eine Liste mit allen Arrays, die in die Tabelle eingefügt werden sollen. wenn ein Element in der Liste selbst eine Liste bestehend aus 
        zwei Arrays ist, wird angenommen, dass diese einer Messreihen mit ihren Unsicherheiten entsprechen. Diese werden automatisch gerundet wie bei 
        der Funktion <error_round>
    - header: eine Liste der Überschriften der jeweiligen Spalte
    - wenn <transpose = True>: die gesamte Tabelle wird transponiert
    - error_mode = ändert das Format, wie Messwerte mit ihren Unsicherheiten ausgegeben werden (siehe bei Funktion <error_round>)
- round_align(list):
    falls in einem Array die Elemente unterschiedlich viele Nachkommastellen haben, werden alle auf die gleiche Anzahl von Nachkommastellem gerundet
- create_tex():
    SEHR WICHTIG!: Damit man eine LaTeX-fähige Datei erstellen kann, MUSS diese Funktion vor jeglicher Tabelle oder Plot in den Code eingefügt werden.
    Jedes mal, wenn man einer latex-datei erstellen will, müssen alle Zellen eines Jupyternotebooks hintereinander ausgeführt werden.
    Werden einzelne Zellen mehrfach hintereinander ausgeführt, werden diese mehrfach in die LaTeX-Datei eingefügt, ohne die alten Einträge zu löschen.
- display_value(name, value, value_err, unit, display_style = 'plus-minus'):
    ermöglicht eine einfache und übersichtliche Ausgabe von einer beim Versuch bestimmten Größe.
    <name> und <unit> sind string für den Name und die Einheit der bestimmten Größe

-- Griechische Buchstaben für eine Python strings --

unicode	character	
\u03B1	α	 \u0391	Α
\u03B2	β	 \u0392	Β
\u03B3	γ	 \u0393	Γ
\u03B4	δ    \u0394	Δ
\u03B5	ε    \u0395	Ε	
\u03B6	ζ    \u0396	Ζ	
\u03B7	η    \u0397	Η  	
\u03B8	θ    \u0398	Θ
\u03B9	ι    \u0399	Ι
\u03BA	κ	 \u039A	Κ
\u03BB	λ	 \u039B	Λ
\u03BC	μ	 \u039C	Μ
\u03BD	ν	 \u039D	Ν
\u03BE	ξ	 \u039E	Ξ
\u03BF	ο	 \u039F	Ο
\u03C0	π	 \u03A0	Π
\u03C1	ρ	 \u03A1	Ρ
\u03C2	ς	 \u03A3	Σ
\u03C3	σ	 \u03A4	Τ
\u03C4	τ    \u03A5	Υ
\u03C5	υ	 \u03A6	Φ
\u03C6	φ	 \u03A7	Χ
\u03C7	χ	 \u03A8	Ψ
\u03C8	ψ	 \u03A9	Ω
\u03C9	ω	 \u03F4	ϴ