# pubgStatz

A Project where we collect and analyze data from PUBG Developer API

## Usage:
* Install docker and docker-compose
* navigate into db/ and: docker-compose up  <- this starts postgres database in container which is accessable via localhost:5432
* open +1 terminal and connect to database: psql -h localhost -p 5432 -U pubgstatz pubgstatz
* db default password is 'pubgstatz'
* open +1 terminal and navigate into project root
* python3 main.py --populate --players=1 --root-player=JantevaVarsi    <- this populates db with all of defined players matches
* python3 main.py --plot --plot-target=karakin_landings --cache    <- caches results from db into json file
* python3 main.py --plot --plot-target=karakin_landings     <- plots landing heatmap

## To-Do:
### Iteration 1: 
- [x] Get The API-requests Working
- [x] Get single player data, match data and match telemetry data using the API
- [ ] Get huge amount of data from different matches and different players
- [ ] Save the data to database and sort and categorize it so it can be accessed later
- [ ] Analyze data from the database (in the first iteration this should be done as easily as possible. No front-end, react, js or any other stuff.)

### Iteration 2: 
-




## Things and ideas to analyze:
Note: All these things has to be sorted by game mode and map (solo-fpp, duo-fpp, squad-fpp and sanhok, vikendi, erangel and miramar) 
* Correlation between rank, landing location and first circle position
* Correlation between rank, landing location and sixth circle position
* Correlation between rank and jump time vs start time
* Correlation between rank and jump distance from the jump point
* Correlation between rank and jump distance from the flight path
* Correlation between molotov usage and win%
* Correlation between molotov usage and k/d
* Correlation between smoke usage and win%
* Correlation between smoke usage and k/d
* Correlation between driving (distance?) in the first and second phase to rank and win%
* Correlation between driving (distance?) in the last phases to rank and win%



