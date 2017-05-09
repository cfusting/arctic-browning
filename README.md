# Arctic Browning
The 2015 Arctic Report Card [[1]](#lc-1)</a> showed an unusual downward trend in the Normalized Vegetation Index (NDVI) in the arctic circle and the northern reaches of Eurasia. NDVI is a measure of the earth's greenness and is thus a proxy for vegetative growth and primary productively. The cause of the recent downward trend is not know, although isolated field studies suggests extreme temperature and other events have had a significant impact [[2]](#lc-2). This is in contrast to the previous 30 years where an upward trend in vegetative growth has been observed. The plot below shows the aggregate trends over the arctic, North America, and Eurasia.

![Arctic plot](https://cfusting.github.io/img/portfolio/arctic-trends.png)


On the left is the Max NDVI where the value represented is the maximum of the season. On the right is the Time Integrated NDVI (TI-NDVI) where the value represented is the sum of the NDVI over the growing season. TI-NDVI is a better indicator of overall vegetative growth as it takes the entire season into account and not just the maximum values.

## Methods
Data in the Arctic Circle is difficult to come by. However NASA launched two satellites (Aqua and Terra) around the turn of the century that provide daily coverage of the entire earth. From these satellites we can derive NDVI, Land Surface Temperature (LST), and Snow Cover. We will use LST and Snow Cover to predict TI-NDVI (the sum of the NDVI over the growing season discussed previously). What we're hoping to find is some link between the LST and snow cover and the amount of vegetation growth (TI-NDVI) that was observed.

*Example: When temperature rises in mid winter the snow melts and exposed delicate shrubs. If it then drops the shrubs that were previously protected by the snow now die due due to exposure. When summer comes the dead shrubs fail to produce new leaves and thus raise the value of TI-NDVI. Because temperature had to rise and then fall for this event to occur, we call it "non-linear".*

We hypothesize that the relationship between LST, snow cover, and TI-NDVI is non linear (as illustrated in the example). Although there are many methods in machine learning that can capture non-linear relationships, we will use [Symbolic Regression](https://en.wikipedia.org/wiki/Symbolic_regression), an [evolutionary algorithm](https://en.wikipedia.org/wiki/Evolutionary_algorithm). Symbolic Regression is particularly good at finding non-linear interactions between variables, in our case LST and snow cover. In addition the results are delivered as a mathematical equation which climate scientists can easily interpret. This is in contrast to other non-linear machine learning methods such as [Neural Networks](https://en.wikipedia.org/wiki/Artificial_neural_network) which although excellent at building non-linear models, can be difficult to interpret.
## Results
This research is currently in progress.

Literature Cited

<a name="lc-1"></a>1. Greenness 15. Arctic Program Available at: http://arctic.noaa.gov/Report-Card/Report-Card-2015/ArtMID/5037/ArticleID/221/Tundra-Greenness. (Accessed: 25th January 2017)
<a name="lc-2"></a>2. Bjerke, J. W. et al. Record-low primary productivity and high plant damage in the Nordic Arctic Region in 2012 caused by multiple weather events and pest outbreaks. Environ. Res. Lett. 9, 84006 (2014).

