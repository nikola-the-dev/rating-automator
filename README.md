# Rating Automator

#### Video Demo:  

https://youtu.be/JBX-pXBih3I
    
#### Description:

Python script that helps to calculate item popularity rate based on Google Analytics report file (you can find this report in `GA4` open `Reports`, then `Engagement`, and finally `Pages and screens`, and then you can download report as `CSV` file)

## Table of Contents

*   [Key features](#key-features)
*   [How to use](#how-to-use)
*   [Interface](#interface)
    *   [GA4 analytics file](#ga4-analytics-file)
    *   [Name of result file](#name-of-result-file)
    *   [Weights of metrics](#weights-of-metrics)
    *   [Name of columns in result file](#name-of-columns-in-result-file)
    *   [Regular expression](#regular-expression)
    *   [Feed](#feed)
    *   [Feed file columns mapping](#feed-file-columns-mapping)


## Key features

* There is possible configure almost any parameter through the menu even the name of the resulting file
* All settings are saved, except for the analytics path file (it is assumed that the analytics file is changes from launch to launch)
* The path to the analytics file can be set not only with the help of menu, but there is also possible to specify it as an argument
* Reveal `CSV` file(s) from the local folder during selecting one for analytics or feed. Also, if some local file was previously selected for analytics, for example, then do not show it when selecting a feed file and vice versa
* There are possible to set weights for analytics metrics in order to calculate popularity/rating final value (Number of Views - Number of Users - Views/User Rate - Average Time - Number of Events - Key Events)
* Also there are possible to set column/header names in the resulting file
* The ability to set a regular expression in order to filter the feed or select the developed default regex are provided 
* If user leaves the regex field empty, then all valuable analytics data will be taken (table headers will be skipped)
* Feed not limited only by a local `CSV` files, there is also possible to set a link to the `XML` file of Google Feed for Merchant Center as the source for feed data
* If the feed is specified as a `CSV` file, then appears preview of this file with ability to map column namber with required attributes as `SKU` and item link. Also, another required step appears in the menu
* Long data values ​​are compressed when printing the settings summary table, or, in the case of a regex, printed below the table

## How to use

You can set path to analytics file as an argument:
```
python project.py analytics.csv
```

This field is required but there is not necessary to set it here you can always do it later by using menu.

So you can call it without specifying argument:
```
python project.py
```

Also you can call short version with argument (especially if you set all settings previously and you need only to receive result file from analytics file):
```
python run.py analytics.csv
```

## Interface

You can set almost every option on settings, preview of menu you can find below:
```
/ $ python project.py analytics.csv

════════════════════════════════════════════════════════════════════════════════
RATING AUTOMATOR
════════════════════════════════════════════════════════════════════════════════

Settings:
╒═══════╤═══════════════════════════════════════════════════╤═══════════════════════════════╕
│   Key │ Name                                              │ Value                         │
╞═══════╪═══════════════════════════════════════════════════╪═══════════════════════════════╡
│     1 │ (Required) GA4 analytics file (.csv)              │ analytics.csv                 │
├───────┼───────────────────────────────────────────────────┼───────────────────────────────┤
│     2 │ Name of result file                               │ result.csv                    │
├───────┼───────────────────────────────────────────────────┼───────────────────────────────┤
│     3 │ Weights of metrics (Views - Users -               │ 0-5-5-10-20-30                │
│       │ Views/User_Rate - Avg.Time - Events - Key_Events) │                               │
├───────┼───────────────────────────────────────────────────┼───────────────────────────────┤
│     4 │ Name of columns in result file (2 columns)        │ Артикул & Популярность        │
├───────┼───────────────────────────────────────────────────┼───────────────────────────────┤
│     5 │ Regular expression for filtering aliases in       │ You can find current regex    │
│       │ analytics file                                    │ pattern below the table (*)   │
├───────┼───────────────────────────────────────────────────┼───────────────────────────────┤
│     6 │ (Required) Feed with all items (.csv file or link │ https://dream...feed?langId=3 │
│       │ to Google Merchant Center .xml file)              │                               │
╘═══════╧═══════════════════════════════════════════════════╧═══════════════════════════════╛
(*) 5. Full regex:
^.*-([a-z]{1,7}[0-9]{1,9}[a-z]{1,9}(([0-9]{1,5}[a-z]{1,5}[0-9]?)|(-l))?|[a-z]{3,4}-[0-9]{3,6}|[0-9]{4,7}-[a-z]{1,4}|[a-z]{2}[0-9]{2,3}-[a-z]{2}-[0-9]{1,3})$

To change any setting parameter, enter the appropriate Key number from the table,
or enter 9 to start calculations and generate the final file

Input: 
```

If all required fields are filled you can type `9` and hit `Enter`-button on the keyboard and it start calculates and forms result file that you can upload to your site later


### GA4 analytics file

You can always set/edit analytics file. In order to do this you need to type `1` next to the `Input:` prompt and hit `Enter`-button on the keyboard.
You will get next window:

```
Input: 1

────────────────────────────────────────────────────────────────────────────────
1. (REQUIRED) GA4 ANALYTICS FILE (.CSV):
────────────────────────────────────────────────────────────────────────────────

We found some file(s) in the current folder:
1. feed.csv
2. analytics.csv

Select one by entering file's key number or enter file path
Type 0 to cancel

Input: 
```

Here you can select files that located in the current folder (type the key-number of the file and hit `Enter`-button on the keyboard), enter path to the file by your own or cancel and return to the previous menu by typing `0` and hitting `Enter` on the keyboard.

### Name of result file

It is not necessary but you can set the name of result file by typing `2` next to the `Input:` prompt and hit `Enter`-button on the keyboard.
You will get next window:

```
Input: 2

────────────────────────────────────────────────────────────────────────────────
2. NAME OF RESULT FILE:
────────────────────────────────────────────────────────────────────────────────
Type 0 to cancel

Input: 
```

Here you can enter new name with/without extension `CSV` or you can enter `0` and hit `Enter`-button on the keyboard in order to return to the previous menu.

### Weights of metrics

Google Analytics report `CSV` file contains a lot of metrics (`GA4` -> `Reports` -> `Engagement` -> `Pages and screens`):
* Number of Views
* Number of Active Users
* Views per User Rate
* Average Time
* Number of Events
* Key Events

In order to calculate final rate value it:
1. Calculates average value for each of metrics mentioned above
2. For current page it takes current value of metric and divide it by average value of metric and multiply it by metric weight
3. This repeats for each metric and then sum all of these received values
4. Received sum then divide by the sum of all weights and myltiply by 100

There are next weight values by default:
* Number of Views = `0` (it doesn't matter because there is another metric below - Views per User Rate)
* Number of Active Users = `5` (it's not so important metric so we give it that weight)
* Views per User Rate = `5` (actually it calculates as `Number of Views / Number of Active Users`)
* Average Time = `10` (this one is much important than previous two)
* Number of Events = `20` (it show number of events that performed by users: scrolls, zooming image, switching tabs etc.)
* Key Events = `30` (the most important metric)

But you can set weights of this metric by your own just typing `3` and hitting `Enter`-button on the keyboard from the main menu:

```
Input: 3

────────────────────────────────────────────────────────────────────────────────
3. WEIGHTS OF METRICS:
────────────────────────────────────────────────────────────────────────────────
Views: 10
Users: 5
Views per User Rate: 1
Avg. Time: 30
Events: 40
Key Events: 45
```

### Name of columns in result file

You can set column headers in result file by typing `4` and hitting `Enter`-button on the keyboard or you can type `0` and hit `Enter`-button on the keyboard in order to return to previous menu

```
Input: 4

────────────────────────────────────────────────────────────────────────────────
4. NAME OF COLUMNS IN RESULT FILE (2 COLUMNS):
────────────────────────────────────────────────────────────────────────────────
Type 0 to cancel

ID: SKU
Rate: Popularity
```


### Regular expression

By default it uses next regular expression:
```
^.*-([a-z]{1,7}[0-9]{1,9}[a-z]{1,9}(([0-9]{1,5}[a-z]{1,5}[0-9]?)|(-l))?|[a-z]{3,4}-[0-9]{3,6}|[0-9]{4,7}-[a-z]{1,4}|[a-z]{2}[0-9]{2,3}-[a-z]{2}-[0-9]{1,3})$
```

Or you can design regular expression on your own in order to exclude some unwanted pages during calculating rate

You can test your own regular expression by using [https://regex101.com](https://regex101.com)

Or you can leave input prompt empty and script will not use any regex for filtering and take into account all valuable data (excluding table headers)

For editing regular expression you need to type `5` and hit `Enter`-button on the keyboard

If you want to restore default value you need to type `d` and hit `Enter`-button on the keyboard


```
Input: 5

────────────────────────────────────────────────────────────────────────────────
5. REGULAR EXPRESSION FOR FILTERING ALIASES IN ANALYTICS FILE:
────────────────────────────────────────────────────────────────────────────────

You can use default regular expression:
^.*-([a-z]{1,7}[0-9]{1,9}[a-z]{1,9}(([0-9]{1,5}[a-z]{1,5}[0-9]?)|(-l))?|[a-z]{3,4}-[0-9]{3,6}|[0-9]{4,7}-[a-z]{1,4}|[a-z]{2}[0-9]{2,3}-[a-z]{2}-[0-9]{1,3})$
...or you can enter any regex on your own.

To use default regex - enter 'd'
If you do not want to use any regex - leave input empty (in this case it takes into account whole data from analytics file except headers).

Type 0 to cancel

Input: 
```

### Feed

This is required step, here you can set not only `CSV` file but also link to `XML` file that you are use as a Google Feed for Merchant Center

It scans current folder for `CSV` files excluding analytics file and you can select one by typing its number and hitting `Enter`-button on the keyboard

Or you can paste link to `XML` file

Or you can type `0` and hit `Enter`-button on the keyboard in order to return to previous menu

```
Input: 6

────────────────────────────────────────────────────────────────────────────────
6. (REQUIRED) FEED WITH ALL ITEMS:
────────────────────────────────────────────────────────────────────────────────

We found some file(s) in the current folder:
1. feed.csv

Select one by entering file's key number, enter path to csv feed file or enter url to xml of google feed for merchant center
Type 0 to cancel

Input:
```

### Feed file columns mapping

This option appears if you select some `CSV` file on [previous step](#feed)

It prints table preview of selected file with numbers for selecting in the header 

Here you need map in which columns locates SKU values and which contains page url values

```
────────────────────────────────────────────────────────────────────────────────
7. (REQUIRED) FEED FILE COLUMNS MAPPING:
────────────────────────────────────────────────────────────────────────────────

Feed file preview:
╒═══════════╤═══════════════════════════════╤══════════╤═══════════════════════════════╤═══════════════════════════════╕
│ 1         │ 2                             │ 3        │ 4                             │ 5                             │
│ ID        │ Item title                    │ Price    │ Image URL                     │ Final URL                     │
╞═══════════╪═══════════════════════════════╪══════════╪═══════════════════════════════╪═══════════════════════════════╡
│ DGR-41613 │ Каблучка. Sia...кул DGR-41613 │ 1850 UAH │ https://somes...7b9d5f571.jpg │ https://somes...so-dgr-41613/ │
├───────────┼───────────────────────────────┼──────────┼───────────────────────────────┼───────────────────────────────┤
│ DGE-4163  │ Сережки гвозд...икул DGE-4163 │ 750 UAH  │ https://somes...eb9623531.jpg │ https://somes...rgi-dge-4163/ │
├───────────┼───────────────────────────────┼──────────┼───────────────────────────────┼───────────────────────────────┤
│ ...       │ ...                           │ ...      │ ...                           │ ...                           │
╘═══════════╧═══════════════════════════════╧══════════╧═══════════════════════════════╧═══════════════════════════════╛

Enter the table column number that corresponds to the value.
Type 0 to cancel

SKU: 1
Alias: 5
```
