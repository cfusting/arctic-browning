# Arctic Browning
The 2015 Arctic Report Card[1] showed an unusual downward trend in the Normalized Vegetation Index (NDVI) in the arctic circle and the northern reaches of Eurasia. NDVI is a measure of the earth's greenness and is thus a proxy for vegetative growth and primary productively. Most plots of NDVI span from brown (no vegetation) to green (lots of vegetation). This can be miss-leading, as brown is an indication of "not green" and not the color brown. For example bare rock and water are considered "brown".
The cause of the recent downward trend is not know, although isolated field studies suggests extreme temperature and other events have had a significant impact[2]. This is in contrast to the previous 30 years where an upward trend has been observed. The following plot illustrates the greening and browning trends from 1982 to 2014 over the arctic circle. 

![Arctic NDVI](https://cfusting.github.io/img/portfolio/arcticbrowning-orig.png)

On the left is the Max NDVI where the value represented is the maximum of the season. On the right is the Time Integrated NDVI (TI-NDVI) where the value represented is the sum of the NDVI over the growing season. TI-NDVI is a better indicator of overall vegetative growth as it takes the entire season into account and not just the maximum values. The plot below shows the trends over the arctic, North America, and Eurasia.

![Arctic plot](https://cfusting.github.io/img/portfolio/arctic-trends.png)

Again Max NDVI is on the left and TI-NDVI on the right.

The goal of this research understand what is causing the arctic to brown.

## Methods
Data in the Arctic Circle is difficult to come by. However NASA launched two satellites (Aqua and Terra) around the turn of the century that provide daily coverage of the entire earth. From these satellites we can derive NDVI, Land Surface Temperature, and Snow Cover. We will use Temperature and Snow Cover and predictors for the TI-NDVI (the sum of the NDVI over the growing season discussed previously). What we're hoping to find is some link between the temperature and snow cover during different points in time leading up to the end of the growing season, and the amount of vegetation growth (TI-NDVI) that was observed. For example we might find that when the temperature rises in mid winter, melts the snow cover and exposed delicate shrubs, and then drops to rapidly, shrubs that were previously protected by the snow are now die due to the extreme cold.

We hypothesize that the relationship between temperature, snow cover, and TI-NDVI is not linear; that is to say that the temperature simply going up or down doesn't mean the TI-NDVI value goes up or down with it. The example previously given is an example of a non-linear relationship. Because of this we will use [evolutionary methods](https://en.wikipedia.org/wiki/Symbolic_regression) to build a non-linear model. 

## Results
This research is currently in progress.

Literature Cited

1. Greenness 15. Arctic Program Available at: http://arctic.noaa.gov/Report-Card/Report-Card-2015/ArtMID/5037/ArticleID/221/Tundra-Greenness. (Accessed: 25th January 2017)
2. Bjerke, J. W. et al. Record-low primary productivity and high plant damage in the Nordic Arctic Region in 2012 caused by multiple weather events and pest outbreaks. Environ. Res. Lett. 9, 84006 (2014).

