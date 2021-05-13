# Clan Rival Check
This script is able to check every single confirmed teams registered to play a World of Tanks tournament

## Requirements
To work properly, this script needs you to install those libs:
- texttable
- urllib3
- tqdm

## Utilisation
```
python main.py
```
Then you will need to enter the tournament ID then wait the end of the process.
If there are teams which don't meet the requirements, this table will show up, filled with problematic teams :

```
+------------+-------------------+
|  Team ID   |     Team Name     |
+============+===================+
| 1234567894 | Team 1            |
+------------+-------------------+
| 2131659894 | Team 2            |
+------------+-------------------+
| 7563249852 | Team 3            |
+------------+-------------------+
| 1324987324 | Team 4            |
+------------+-------------------+
| 7563219783 | Team 5            |
+------------+-------------------+
| 3295465231 | Team 6            |
+------------+-------------------+
```

## Team requirements
A team has to have all its players within the same clan to be accepted
