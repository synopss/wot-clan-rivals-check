# World of Tanks Clan Rival Check
This script is able to check every single confirmed teams registered to play a World of Tanks tournament

## Requirements
To work properly, this script needs you to install those libs:
- texttable
- urllib3
- tqdm

Made in Python 3.9

## Utilisation
```
python main.py
```
Then you will need to enter the tournament ID then wait the end of the process.
If there are teams which don't meet the requirements, this table will show up, filled with problematic teams and the problematic players:

```
+------------+-------------------+-------------------+
|  Team ID   |     Team Name     |     Nicknames     |
+============+===================+===================+
| 1234567894 | Team 1            | nick1,nick2,nick3 |
+------------+-------------------+-------------------+
| 2131659894 | Team 2            | nick4,nick2,nick7 |
+------------+-------------------+-------------------+
| 7563249852 | Team 3            | nick8,nick5,nick1 |
+------------+-------------------+-------------------+
| 1324987324 | Team 4            | nick2,nick3       |
+------------+-------------------+-------------------+
| 7563219783 | Team 5            | nick9,nick2       |
+------------+-------------------+-------------------+
| 3295465231 | Team 6            | nick3             |
+------------+-------------------+-------------------+
```

## Team requirements
A team has to have all its players within the same clan to be accepted
