# Lane Detection

[//]: # (Image References)
[image1]: ./project_images/lane_example.jpg
[gif1]: ./project_images/lane.gif


![alt text][gif1] 

See also: <https://github.com/jawilk/SDCND-P4-Advanced-Lane-Lines>

## Run
Open a console, then run:
```python
python lane_new.py
```
Should yield this:
![alt text][image1] 


## Situation
Car in starting position, outline of the driving road during whole drive, including outer lanes.<br/>
**Note:** This was just used for visualization purpose only. No driving assistent is derived yet. The code was applied to the pictures collected by the driving car.
## Shortcomings
* No driving assistent yet
* Could fail under different light conditions
* Still not smooth lane at intersection

## Improvements
* Derive navigation for car as assistence for the self-driving process (i.e. keep car at the middle of the road etc.)
* Display road curvature
* Path planning
* Adviced parking in front of barrier (will enhance QR-code detection)