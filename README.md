# pubgStatz

A Project where we collect and analyze data from PUBG Developer API

## To-Do:
### Iteration 1: 
- [x] Get The API-requests Working
- [x] Get single player data, match data and match telemetry data using the API
- [x] Get huge amount of data from different matches and different players
- [ ] Save the data to database and sort and categorize it so it can be accessed later easily
- [ ] Analyze data from the database 
- [x] Visualize analyzed data with some sick ass graphs (in the first iteration this should be done as easily as possible. No front-end, react, js or any other stuff.) This is actually quite easy with seaborn. Just give it some data in array format and it will show a graph. The hard part is to parse, manipulate  and get the data from the rawdata files.
- [ ] Profit ???

### Iteration 2: 
-




## Things and ideas to analyze:
Note: All these things has to be sorted by game mode and map (solo-fpp, duo-fpp, squad-fpp and sanhok, vikendi, erangel and miramar) 

* Correlation between rank, and distance between landing location and first circle position
* Correlation between rank, and distance between landing location and sixth circle position
* Correlation between rank, and distance between player position when fourth circle position appears
* Correlation between rank, and wheter the player is inside the safezone when different zones appear (e.g `isGame: 2.0, isInBlueZone: True`)
* Correlation between rank and landing time difference from first player landing time
* Correlation between rank and jump distance from the jump point
* *Correlation between rank and jump distance from the flight path (the flight path has to be calculated from the player position when starting flight and leaving the plane)*

___

* *Correlation between molotov throw amount and win% (will need player data or something else)*
* Correlation between molotov throw amount and kills
* Correlation between molotov throw amount and rank
* *Correlation between smoke throw amount and win% (will need player data or something else)*
* Correlation between smoke throw amount and rank
* Correlation between smoke throw amount and kills
* *Correlation between grenade throw amount and win% (will need player data or something else)*
* Correlation between grenade throw amount and rank
* Correlation between grenade throw amount and kills

___

* *Correlation between driving (distance?) in the first and second phase to rank (this has to be compared to others who dropped in the same location/ same distance)*
* *Correlation between driving (distance?) in the last phases to rank (this has to be compared to others who dropped in the same location/ same distance)*



