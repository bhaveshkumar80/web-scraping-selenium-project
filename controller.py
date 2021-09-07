import os
import json
import pandas as pd


import Kaufen_Anlageobjekte
import Kaufen_Grundstuck
import Kaufen_Haus
import Kaufen_Wohnungen
import Mieten_Wohnungen
from conversion import convert


def Run():
    Kaufen_Anlageobjekte.KA()
    convert('Kaufen_Anlageobjekte.json')

    Kaufen_Grundstuck.KG()
    convert('Kaufen_Grundstuck.json')

    Kaufen_Haus.KH()
    convert('Kaufen_Haus.json')

    Kaufen_Wohnungen.KW()
    convert('Kaufen_Wohnungen.json')

    Mieten_Wohnungen.MW()
    convert('Mieten_Wohnungen.json')


Run()
