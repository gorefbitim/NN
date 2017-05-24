SELECT * FROM (
  SELECT 
    date(committer.date) as committer_date,
    count(*) as date_count
  FROM `bigquery-public-data.github_repos.commits`
  WHERE committer.date > timestamp('2010-01-01')  AND
        committer.date < timestamp('2017-01-01')
  GROUP BY committer_date ) c
JOIN (
  SELECT
    -- Create a timestamp from the date components.
    date(timestamp(concat(year,"-",mo,"-",da))) as noaa_date,
    -- Replace numerical null values with 0s
    AVG(IF (temp=9999.9, 0, temp)) AS temperature,
    AVG(IF (visib=999.9, 0, visib)) AS visibility,
    AVG(IF (wdsp="999.9", 0, CAST(wdsp AS Float64))) AS wind_speed,
    AVG(IF (gust=999.9, 0, gust)) AS wind_gust,
    AVG(IF (prcp=99.99, 0, prcp)) AS precipitation,
    AVG(IF (sndp=999.9, 0, sndp)) AS snow_depth
  FROM
    `bigquery-public-data.noaa_gsod.gsod20*`
  WHERE
    CAST(YEAR AS INT64) > 2009 AND
    CAST(YEAR AS INT64) < 2017 AND
    (stn="725030" OR  -- La Guardia
     stn="744860")    -- JFK
  GROUP BY noaa_date) w
ON c.committer_date = w.noaa_date
ORDER BY c.committer_date
