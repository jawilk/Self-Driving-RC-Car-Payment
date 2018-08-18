# QR-Code Detection, Decoding and Displaying

[//]: # (Image References)
[image1]: ./project_images/qr_img_barrier.jpg
[image2]: ./project_images/detected_qr_code.jpg


![alt text][image1] 

This folder contains for qr-code detection and encoding as well as for displaying the qr-code.
## Run
Original image dimensions are **2048x1236**.
Open a console, then run:
```python
python qr_detection.py 1 # arg 0 for no display
```
Should yield this:<br/>
![alt text][image2] <br/>
> The address is: GXHCZXIPIQWYGYUUUOYKL9DUEAJGLINGMMOJADZDNPHHSRJOJLMPLKBMFXSQPAPVDUFHLBGOBO9TBCQHAMZSMEIPHC

## Situation
**(i)**
Car is waiting in front of barrier. Raspberry Pi camera is restarting with higher resolution, then streaming pictures to PC. PC receives images and starts searching for QR-Code. Making transaction after decoding barrier's address.<br/>
<br/>
**(ii)**
Car has arrived at the barrier. Barrier motion detection of the car has detected that the car isn't moving anymore, barrier ultra sonic sensor has detected an obstacle. PC is displaying QR-Code on second screen device (phone).
## Shortcomings
* Need reinitialization of Raspberry Pi camera with higher resolution, may try threading solution again
* Car needs to park in certain angle to be able to read qr-code
## Improvements
* Lower resolution decoding
* Moving camera to allow wider range scanning


## Sources
* <https://github.com/dlenski/python-zxing>


