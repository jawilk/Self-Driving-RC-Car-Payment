# Self-Driving-RC-Car-Payment


[//]: # (Image References)
[image1]: ./project_images/overview.jpg
[image2]: ./project_images/overview_top.jpg
[image3]: ./project_images/overview_side.jpg
[image4]: ./project_images/overview_back.jpg
[image5]: ./project_images/project_structure_diagram.jpg

[gif1]: ./project_images/run_qr_2x.gif
[gif2]: ./project_images/whole_top_2x.gif
[gif3]: ./project_images/lane_traffic_sign.gif
[gif4]: ./project_images/barrier_moving_car.gif
[gif5]: ./project_images/payment.gif
[gif6]: ./project_images/track_overview_2x.gif


<https://youtu.be/0tvsjX1nmS0> - Full overview
<https://youtu.be/6oKXf77ebHk> - IOTA payment

![alt text][gif1] ![alt text][gif2]
![alt text][gif3]
![alt text][gif4]
![alt text][gif5]
<br/>
<br/>

This repository contains code for several autonomous car techniques applied to an RC-Car. It is splitted in a **"pipeline"** and a **"program"** part, respectively. The **"pipeline"** part contains the whole project as it was served to the PC, Arduino and Raspberry Pi. This code was able to drive the car around the track and contains the logic for connecting the different parts of the project. <br/>
However, since I assume the pipeline approach would **not** generalize well to other environment conditions, the **"program"** part contains standalone code for every **single** technique that was used in the original pipeline, without any connections in-between. 

Even if there are several different features, the main focus of this project was to make the car to pay for the barrier on its own, without human interaction. 

Further **code/explanations** can be found within the certain folders.
<br/>
<br/>

![alt text][image1] ![alt text][image2] ![alt text][image3]
![alt text][image4]


## Track overview <br/>
![alt text][gif6] 

![alt text][image5]
###### (Made with draw.io)


## Dependencies
**PC**
* python 3.5.5
* keras 2.2.0
* tensorflow 1.9.0
* opencv 3.2.0
* pyota 2.0.6
* zxing 0.9.3

**Raspberry Pi 3B**:
* keras 2.2.0
* tensorflow 1.9.0

## Sources
* A great help and inspiration was this project by Zheng Wang: <br/>
  <https://zhengludwig.wordpress.com/projects/self-driving-rc-car/> <br/>
  <https://github.com/hamuchiwa/AutoRCCar>

* <https://github.com/multunus/autonomous-rc-car>

* <https://github.com/AutoModelCar/AutoModelCarWiki/wiki>

* <https://custom-build-robots.com/raspberry-pi-roboter/autonom-fahrendes-raspberry-pi-ki-roboter-auto-elektronik-donkeycar/9775> (german)

* Krasheninnikov, Dmitrii. “AUTONOMOUS CONTROL OF A RC CAR WITH A CONVOLUTIONAL NEURAL NETWORK.”, 2017
<https://www.theseus.fi/bitstream/handle/10024/126220/Krasheninnikov_Dmitrii.pdf?sequence=1>
  
* Udacity Self-Driving Car Engineer Nanodegree (Part 1)

More sources can be found in the specific **"program"** sections.