#!/usr/bin/python3

"""CSV loader."""

import csv
from datetime import datetime
from os import path

from pytz import timezone

from modules.logs import CVFILOG


NAME_DEP = {
    "01": "01 - Ain",
    "02": "02 - Aisne",
    "03": "03 - Allier",
    "04": "04 - Alpes-de-Haute-Provence",
    "05": "05 - Hautes-Alpes",
    "06": "06 - Alpes-Maritimes",
    "07": "07 - Ardèche",
    "08": "08 - Ardennes",
    "09": "09 - Ariège",
    "10": "10 - Aube",
    "11": "11 - Aude",
    "12": "12 - Aveyron",
    "13": "13 - Bouches-du-Rhône",
    "14": "14 - Calvados",
    "15": "15 - Cantal",
    "16": "16 - Charente",
    "17": "17 - Charente-Maritime",
    "18": "18 - Cher",
    "19": "19 - Corrèze",
    "2A": "2A - Corse-du-Sud",
    "2B": "2B - Haute-Corse",
    "21": "21 - Côte-d'Or",
    "22": "22 - Côtes d'Armor",
    "23": "23 - Creuse",
    "24": "24 - Dordogne",
    "25": "25 - Doubs",
    "26": "26 - Drôme",
    "27": "27 - Eure",
    "28": "28 - Eure-et-Loir",
    "29": "29 - Finistère",
    "30": "30 - Gard",
    "31": "31 - Haute-Garonne",
    "32": "32 - Gers",
    "33": "33 - Gironde",
    "34": "34 - Hérault",
    "35": "35 - Ille-et-Vilaine",
    "36": "36 - Indre",
    "37": "37 - Indre-et-Loire",
    "38": "38 - Isère",
    "39": "39 - Jura",
    "40": "40 - Landes",
    "41": "41 - Loir-et-Cher",
    "42": "42 - Loire",
    "43": "43 - Haute-Loire",
    "44": "44 - Loire-Atlantique",
    "45": "45 - Loiret",
    "46": "46 - Lot",
    "47": "47 - Lot-et-Garonne",
    "48": "48 - Lozère",
    "49": "49 - Maine-et-Loire",
    "50": "50 - Manche",
    "51": "51 - Marne",
    "52": "52 - Haute-Marne",
    "53": "53 - Mayenne",
    "54": "54 - Meurthe-et-Moselle",
    "55": "55 - Meuse",
    "56": "56 - Morbihan",
    "57": "57 - Moselle",
    "58": "58 - Nièvre",
    "59": "59 - Nord",
    "60": "60 - Oise",
    "61": "61 - Orne",
    "62": "62 - Pas-de-Calais",
    "63": "63 - Puy-de-Dôme",
    "64": "64 - Pyrénées-Atlantiques",
    "65": "65 - Hautes-Pyrénées",
    "66": "66 - Pyrénées-Orientales",
    "67": "67 - Bas-Rhin",
    "68": "68 - Haut-Rhin",
    "69": "69 - Rhône",
    "70": "70 - Haute-Saône",
    "71": "71 - Saône-et-Loire",
    "72": "72 - Sarthe",
    "73": "73 - Savoie",
    "74": "74 - Haute-Savoie",
    "75": "75 - Paris",
    "76": "76 - Seine-Maritime",
    "77": "77 - Seine-et-Marne",
    "78": "78 - Yvelines",
    "79": "79 - Deux-Sèvres",
    "80": "80 - Somme",
    "81": "81 - Tarn",
    "82": "82 - Tarn-et-Garonne",
    "83": "83 - Var",
    "84": "84 - Vaucluse",
    "85": "85 - Vandée",
    "86": "86 - Vienne",
    "87": "87 - Haute-Vienne",
    "88": "88 - Vosges",
    "89": "89 - Yonne",
    "90": "90 - Territoire de Belfort",
    "91": "91 - Essonne",
    "92": "92 - Hauts-de-Seine",
    "93": "93 - Seine-St-Denis",
    "94": "94 - Val-de-Marne",
    "95": "95 - Val-D'Oise",
    "971": "971 - Guadeloupe",
    "972": "972 - Martinique",
    "973": "973 - Guyane",
    "974": "974 - La Réunion",
    "976": "976 - Mayotte"}
LAT_DEP = {
    "01": "46.1061500835",
    "02": "49.5524137158",
    "03": "46.3993644498",
    "04": "44.0908723554",
    "05": "44.6744954225",
    "06": "43.9477022711",
    "07": "44.748161488",
    "08": "49.610898748",
    "09": "42.9322144767",
    "10": "48.3182253913",
    "11": "43.1012521113",
    "12": "44.277717255",
    "13": "43.5436905217",
    "14": "49.0966958599",
    "15": "45.0180519173",
    "16": "45.7166708711",
    "17": "45.7703624625",
    "18": "47.0631160847",
    "19": "45.3655110046",
    "2A": "41.8839751228",
    "2B": "42.3789860605",
    "21": "47.4148513561",
    "22": "48.4435359708",
    "23": "46.0861690765",
    "24": "45.1273768173",
    "25": "47.1651371592",
    "26": "44.6743762083",
    "27": "49.1073075931",
    "28": "48.3896168991",
    "29": "48.3017361102",
    "30": "43.9938436911",
    "31": "43.3574229585",
    "32": "43.6837953357",
    "33": "44.8572445351",
    "34": "43.5777973112",
    "35": "48.1812360423",
    "36": "46.8018622942",
    "37": "47.2310354675",
    "38": "45.2694421656",
    "39": "46.7337108015",
    "40": "43.965937453",
    "41": "47.6176924713",
    "42": "45.7272583786",
    "43": "45.135004008",
    "44": "47.3753590043",
    "45": "47.8813399374",
    "46": "44.6269246895",
    "47": "44.3674227861",
    "48": "44.5294508592",
    "49": "47.3952383531",
    "50": "49.0858024109",
    "51": "48.9405334413",
    "52": "48.1022459554",
    "53": "48.1320145418",
    "54": "48.7916600767",
    "55": "48.9990933177",
    "56": "47.8426011958",
    "57": "49.0221937323",
    "58": "47.1016983299",
    "59": "50.4501366141",
    "60": "49.3993972661",
    "61": "48.6109514041",
    "62": "50.4986573015",
    "63": "45.7334187796",
    "64": "43.2765512642",
    "65": "43.0586379729",
    "66": "42.6040161713",
    "67": "48.6601653977",
    "68": "47.8564873154",
    "69": "45.8705575392",
    "70": "47.6428660146",
    "71": "46.6422857602",
    "72": "47.9885256718",
    "73": "45.4607199042",
    "74": "46.0352614624",
    "75": "48.8626304852",
    "76": "49.6545398173",
    "77": "48.6142332217",
    "78": "48.821484306",
    "79": "46.5207504336",
    "80": "49.9733253681",
    "81": "43.7799765873",
    "82": "44.0801227297",
    "83": "43.4690059217",
    "84": "43.9851237661",
    "85": "46.6729533879",
    "86": "46.5546778015",
    "87": "45.8830768403",
    "88": "48.1963376541",
    "89": "47.8490198002",
    "90": "47.6278946489",
    "91": "48.5270354108",
    "92": "48.8365843138",
    "93": "48.9023234526",
    "94": "48.7837401836",
    "95": "49.0803858577",
    "971": "16.266812",
    "972": "14.667264",
    "973": "4.075111",
    "974": "-21.117282",
    "976": "-12.817226"}
LON_DEP = {
    "01": "5.32551470817",
    "02": "3.56557185412",
    "03": "3.1654172286",
    "04": "6.23590323452",
    "05": "6.23085847467",
    "06": "7.12430252381",
    "07": "4.41397525518",
    "08": "4.61820857627",
    "09": "1.51243170827",
    "10": "4.14937893854",
    "11": "2.3863195178",
    "12": "2.70931526263",
    "13": "5.07329988936",
    "14": "-0.379270597736",
    "15": "2.6624257459",
    "16": "0.196450542402",
    "17": "-0.701151604065",
    "18": "2.50571113255",
    "19": "1.87090523159",
    "2A": "8.97997119242",
    "2B": "9.23567141765",
    "21": "4.81194710404",
    "22": "-2.85882396738",
    "23": "2.02430101436",
    "24": "0.712740186269",
    "25": "6.36768229649",
    "26": "5.16582168009",
    "27": "1.00532238081",
    "28": "1.37569716428",
    "29": "-4.03428132272",
    "30": "4.17905217935",
    "31": "1.21425495972",
    "32": "0.477177140595",
    "33": "-0.57369678116",
    "34": "3.34800607563",
    "35": "-1.64589552684",
    "36": "1.55801304217",
    "37": "0.686650122405",
    "38": "5.60195085024",
    "39": "5.70313863162",
    "40": "-0.822038920542",
    "41": "1.41960449512",
    "42": "4.15060346621",
    "43": "3.82064144653",
    "44": "-1.71598291146",
    "45": "2.30587611938",
    "46": "1.59005920617",
    "47": "0.470227995175",
    "48": "3.48086881176",
    "49": "-0.553551118702",
    "50": "-1.33862320377",
    "51": "4.24555140178",
    "52": "5.18945345266",
    "53": "-0.660149410464",
    "54": "6.16801224152",
    "55": "5.37408151001",
    "56": "-2.85850436809",
    "57": "6.66814664402",
    "58": "3.51951300252",
    "59": "3.19335565357",
    "60": "2.4291033299",
    "61": "0.107175122984",
    "62": "2.28398463259",
    "63": "3.14276506265",
    "64": "-0.758975468791",
    "65": "0.177947425719",
    "66": "2.51579255516",
    "67": "7.56876364377",
    "68": "7.27311359047",
    "69": "4.64214055868",
    "70": "6.07108033539",
    "71": "4.53104899924",
    "72": "0.200030493539",
    "73": "6.44362178612",
    "74": "6.43415213",
    "75": "2.33629344655",
    "76": "1.04295071603",
    "77": "2.96159846336",
    "78": "1.82843694709",
    "79": "-0.323592605264",
    "80": "2.29150476832",
    "81": "2.19017910647",
    "82": "1.2899145835",
    "83": "6.17637273437",
    "84": "5.16506865588",
    "85": "-1.29188591019",
    "86": "0.506618351155",
    "87": "1.22078165066",
    "88": "6.38201358618",
    "89": "3.5878018416",
    "90": "6.92965534221",
    "91": "2.27017712838",
    "92": "2.23913599058",
    "93": "2.4837276939",
    "94": "2.45463530415",
    "95": "2.15488070885",
    "971": " -61.563250",
    "972": " -61.011036",
    "973": " -53.129967",
    "974": " 55.536225",
    "976": " 45.159895"}


def load_csv(file_path, point_hour, measurement, limit=None):
    """Load CSV file to list."""
    TAGS = ['hosp', 'rea', 'rad', 'dc']

    if not path.isfile(file_path):
        CVFILOG.error('File not exist: ' + file_path)
        return None

    inputfile = open(file_path, 'r')

    data_points = []
    count = 0
    reader = csv.DictReader(inputfile, delimiter=';')
    for row in reader:
        if row['sexe'] == '0' and row['dep'] != '' and row['dep'] != 'NA':
            dt_src = datetime.strptime(
                row['jour'] + ' ' + point_hour,
                '%d/%m/%Y %H:%M:%S' if '/' in row['jour']
                else '%Y-%m-%d %H:%M:%S')
            dt_loc = datetime.isoformat(
                timezone('Europe/Paris').localize(dt_src))

            fields = {}
            row_dict = {
                key: value for (key, value) in row.items() if key in TAGS}
            for val in row_dict:
                try:
                    fields[val] = int(row[val])
                except ValueError:
                    fields[val] = 0

            data_points.append({
                'measurement': measurement,
                'time': dt_loc,
                'fields': fields,
                'tags': {
                    'code': row['dep'],
                    'dep': NAME_DEP[row['dep']],
                    'latitude': LAT_DEP[row['dep']],
                    'longitude': LON_DEP[row['dep']]
                }
            })

        count += 1
        if limit is not None and count > limit:
            break

    inputfile.close()
    return data_points
