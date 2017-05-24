# NN

# Files

SkyLine.ipynb    - analysis notebook
BigQuery.sql     - sql query used to prepare git and weather data from
                   google repo
commits_noaa.csv - data
nn_reg.py        - python functions code
requirements.txt - pip packages file
commit_tz.csv    - timezone commits data

# Assumption
(1) We discretize by date , and so the data is basically #commits/day ,
    or 360 / year
(2) We have both committer and author date - I decided to use committer
(3) People 'committed' as early as 1970, 1971, and all the way through 2100,
    and so I took only 2010-2016

# Data prep 
Data is the first figure is shown in thousands commits (x axis is days from
2010). We can see on general more commits with time (so we may hypothesize
positive correlation of #commits with the global warming :-)

Average is around 100k commits daily, so it would be nice to have an estimate
of ~20 or MSE~400 (a very low bar).

# Feature extraction
(A) derived from date: year, month, day, day_num, day_cos, day_sin, weekend
(B) took from NOAA (weather): temperature, visibility, wind_speed, wind_gust,
    precipitation, snow_depth from two points in New-Yord

# Model 
Neural network model using keras with TensorFlow.

# Results
(1) Correlation is unsuccessful: Results: 2249.43 (1556.20) MSE
(2) The data show a clear weekly period , with lowest number of commits every weekend.

# Limitations / Future 
(1) I used NY statios, a better correlation could use commiter geo location with
    weather data that is relevant to the lcoation. Although geolocation is not
    provided in BigQuery, it could be take from github (many commiter disclose
    their geolocation) or from commmit timezone data. I looked at the timezone
    data and was surprized to find that Israel time zone (+2) has more commits
    than CA (-7). To further understand this, I look at a few anecdotal commiter
    names and also their geolocation - turned out most from eastern Europe
    countries with timezone like Israel...
(2) It would be interesting to further explore if we also see lower commits
    on holidays.
