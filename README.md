# surfs_up

## Overview
The purpose of this analysis is to collect Temperature trends and information in Oahu for a surf and ice cream shop business. Two specific months, June and December, are observed in order to determine if the business will be sustainable year-round.

## Results
The images below display the Temperature Statistics for June and December:

![June Temperature Statistics](Resources/June_Stats.png)

![December Temperature Statistics](Resources/Dec_Stats.png)

- The Count for June and December are both quite high, which makes the analysis more accurate.
- June has a mean temperature of 74.9, whereas December has a mean temperature of 71.0. Although December has a slightly colder mean temperature, it's not colder by much, and is still appropriate for our purposes. 
- Both June and December have appropriate maximum temperatures, however the minimum temperature in December may not be appropriate for our purposes. 

## Summary
In summary, it seems that both June and December have temperatures suitable for our purposes. Therefore it can be concluded that a surf and ice cream business is suitable year-round.

Below are some queries that one could perform to gather more weather data for the June and December months:

rain_june=session.query(Measurement.date, Measurement.prcp).filter(extract("month", Measurement.date)==6).all()

rain_december=session.query(Measurement.date, Measurement.prcp).filter(extract("month", Measurement.date)==12).all()

The two queries above will return the precipitation scores for June and December. 