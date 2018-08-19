# Traffic Sign Detection

[//]: # (Image References)
[image1]: ./project_images/overview.jpg
[image2]: ./project_images/all.jpg
[image3]: ./project_images/training.jpg

![alt text][image1] <br/>

See also: <https://github.com/jawilk/SDCND-P2-Traffic-Sign-Classifier>


## Final

## Training
For training the model a combination of own images and images from the german traffic sign dataset were used (see "Sources" below). The model was trained with 6 classes:
* 0 Background
* 1 50 km/h
* 2 Priority
* 3 Stop
* 4 Dangerous Curve Right
* 5 No Passing
* 
![alt text][image2] ![alt text][image3]

## Extraction of region proposals
A sliding window approach was used to extract regions of interest.

## Run


## Sources
* German Traffic Sign Dataset:
 J. Stallkamp, M. Schlipsing, J. Salmen, and C. Igel. The German Traffic Sign Recognition Benchmark: A multi-class classification competition. In Proceedings of the IEEE International Joint Conference on Neural Networks, pages 1453–1460. 2011.
 <http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset>
