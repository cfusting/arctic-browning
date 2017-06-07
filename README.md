# Arctic Browning
The 2015 Arctic Report Card <a href="#lc-1">[1]</a> showed an unusual downward trend in the Normalized Vegetation Index (NDVI) in the arctic circle and the northern reaches of Eurasia. NDVI is a measure of the earth's greenness, acting as a proxy for vegetative growth and primary productively. The cause of the recent browning trend is not known, although isolated field studies suggest extreme temperature and other events have had a significant impact <a href="#lc-2">[2]</a>. This is in contrast to the previous 30 years where an upward trend in vegetative growth and greenness has been observed. The plot below shows the aggregate trends over the Arctic, North America, and Eurasia.

![Arctic plot](https://cfusting.github.io/img/portfolio/arctic-trends.png)

On the left is the Max NDVI where the value represented is the maximum of the season. On the right is the Time Integrated NDVI (TI-NDVI) where the value represented is the sum of the NDVI over the growing season. TI-NDVI is a better indicator of overall vegetative growth as it takes the entire season into account and not just the maximum values.

## Methods
Data for the Arctic Circle is difficult to come by. However NASA launched two satellites (Aqua and Terra) around the turn of the century that provide daily coverage of the entire earth. From these satellites we can derive NDVI, Land Surface Temperature (LST), and Snow Cover. We will use LST and Snow Cover to predict TI-NDVI. We hope to find connections between the LST and Snow cover and the amount of vegetation growth (TI-NDVI) that was observed.

*Example: When temperature rises in mid winter, the snow melts and expose delicate shrubs. If the temperature then drops, the shrubs that were previously protected by the snow now die due due to exposure. When summer comes the dead shrubs fail to produce new leaves, which lowers the value of TI-NDVI. Because temperature had to rise and then fall for this event to occur, we call it "nonlinear".*

We hypothesize that the relationship between LST, Snow Cover, and TI-NDVI is nonlinear (as illustrated in the example). Although there are many methods in machine learning that can capture nonlinear relationships, we will use <a href="https://en.wikipedia.org/wiki/Symbolic_regression">Symbolic Regression</a>, an <a href="https://en.wikipedia.org/wiki/Evolutionary_algorithm">evolutionary algorithm</a>. Symbolic Regression is particularly good at finding nonlinear interactions between variables, in our case LST and snow cover. In addition the results are delivered as a mathematical equation which climate scientists can easily interpret. This is in contrast to other nonlinear machine learning methods such as <a href="https://en.wikipedia.org/wiki/Artificial_neural_network">Neural Networks</a> which although excellent at building nonlinear models, can be difficult to interpret.

## Results
This research is currently in progress.

### Literature Cited

1. Greenness 15. Arctic Program Available at: http://arctic.noaa.gov/Report-Card/Report-Card-2015/ArtMID/5037/ArticleID/221/Tundra-Greenness. (Accessed: 25th January 2017)<a name="lc-1"></a>
2. Bjerke, J. W. et al. Record-low primary productivity and high plant damage in the Nordic Arctic Region in 2012 caused by multiple weather events and pest outbreaks. Environ. Res. Lett. 9, 84006 (2014).<a name="lc-2"></a>

