# QR-Code Detection and Decoding

[//]: # (Image References)
[image1]: ./project_images/qr_img_barrier.jpg
[image2]: ./project_images/detected_qr_code.jpg


![alt text][image1] 

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
Car is waiting in front of barrier. Raspberry Pi camera is restarting with higher resolution, then streaming pictures to PC. PC receives images and starts searching for QR-Code. Making transaction after decoding barrier's address.
## Shortcomings
* Need reinitialization of Raspberry Pi camera with higher resolution, may try threading solution again
* Car needs to park in certain angle to be able to read qr-code
## Improvements
* Lower resolution decoding
* Moving camera to allow wider range scanning


## Sources
* <https://github.com/dlenski/python-zxing>


