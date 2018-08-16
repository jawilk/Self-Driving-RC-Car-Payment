# RC-Car-IOTA

[//]: # (Image References)
[image1]: ./project_images/overview_1.jpg
[gif1]: ./project_images/run_qr_2x.gif
[gif2]: ./project_images/whole_top_2x.gif
[gif3]: ./project_images/track_overview.gif


![alt text][gif1] ![alt text][gif2]
![alt text][image1] 


This git contains code for several autonomous car techniques applied to a RC-Car. It is splitted in a **"pipeline"** and a **"program"** part, respectively. The "pipeline" part contains the whole project as it was served to the PC, Arduino and Raspberry Pi. It was able to drive around the track and contains the logic for connecting the different parts of the project.
However, since I assume the pipeline approach would **not** generalize well to other environment conditions, the **"program"** part contains standalone code for every **single** technique which was used in the original pipeline, without any connection. 

Further **code/explanations** can be found within the certain folders.

**Track overview** <br/>
![alt text][gif3] 


## Dependencies
**PC**
* python 3.5.5
* keras 2.2.0
* tensorflow 1.9.0
* opencv 3.2.0
* pyota 2.0.6

**Raspberry Pi 3B**:
* keras 2.2.0
* tensorflow 1.9.0