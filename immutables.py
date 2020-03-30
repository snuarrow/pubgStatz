import os

gameModes = [
    'solo-fpp',
    'duo-fpp',
    'squad-fpp',
    'solo-tpp',
    'duo-tpp',
    'squad-tpp',
]

mapNames = {
  "Desert_Main": "Miramar",
  "DihorOtok_Main": "Vikendi",
  "Erangel_Main": "Erangel",
  "Baltic_Main": "Erangel (Remastered)",
  "Range_Main": "Camp Jackal",
  "Savage_Main": "Sanhok",
  "Summerland_Main": "Karakin"
}

try:
  db_host = os.environ['PUBGSTATZ_DB_HOST']
except KeyError:
  print('PUBGSTATZ_DB_HOST not exported, run export PUBGSTATZ_DB_HOST=<db host>')
  exit(1)
