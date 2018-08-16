# RC-Car-IOTA

[//]: # (Image References)
[image1]: ./project_images/overview.jpg


![alt text][image1] 


This git contains code ... . It is splitted in a "pipeline" and a "program" part, respectively. The "pipeline" part contains the whole project as it was served to the PC, Arduino and Raspberry Pi. It was able to drive around the track and contains the logic for connection the different parts of the project.
However, since I assume the standalone pipeline would not generalise well to other environment conditions, the "program" part contains single programs which are part of the pipeline, without any connection.


## Dependecies
**PC**
* python 3.5.5
* keras 2.2.0
* tensorflow 1.9.0
* opencv 3.2.0
* pyota 2.0.6

**Raspberry Pi 3B**:
* keras 2.2.0
* tensorflow 1.9.0


Repositority structure:
* Pipeline