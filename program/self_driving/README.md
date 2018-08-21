# Self driving

See also: <https://github.com/jawilk/SDCND-P3-Behavioral-Cloning>

[//]: # (Image References)
[image1]: ./project_images/overview.jpg


![alt text][image1] 


## Training
I collected a total of **17.503** images to train my model (with flipping **35.006**). I trained on resized, grayscaled images (320x160x1).<br/>
Labels were chosen as the following

Key | Label
--- | --- 
w   | 0
q   | 1
e   | 2

As mentioned before, the model was trained on flipped images as well. To achieve this, keys q<->e/labels 1<->2 need to be *swapped*, while w=0 must stay the same. This can be done with the function
> f(x) = |x - 3| % 3; x=label

After training (on AWS) for 20 epochs, the model achieved:

* Train acc: 0.9778
* Train loss: 0.0592
* Validation acc: 0.9649
* Validation loss: 0.1160

## Run
### Collecting process/Driving with PC
* Upload the sketch in "/arduino_car" to the Arduino on your car (Adjust desired **speed** of car in sketch)
* After powering up the Arduino on the car, wait till the HC-06 Bluetooth module starts blinking
* Connect the bluetooth of your PC with the Arduino (PW: 1234)
#### PC
First **create** directory key presses and their timestamps will be saved, it should be named **"time_press_release"**.<br/>

Open up a console
```python
python drive_car_pc.py
```
The PC should now connect to the Arduino and open up a tkinter window. Now you should be able to drive the car with this key presses:

Key | Action
--- | --- 
q   | forward left
w   | forward
e   | forward right
a   | backward left
s   | backward
d   | backward right
y   | wheels left
x   | wheels right
k   | STOP
0   | Speed state 0 (Adjust in ardunio sketch)
1   | Speed state 1 (Adjust in ardunio sketch)
2   | Speed state 2 (Adjust in ardunio sketch)
3   | Speed state 3 (Adjust in ardunio sketch)
4   | Speed state 4 (Adjust in ardunio sketch)

To stop driving and save the timestamped key presses, just close the tkinter window and approve the prompt.<br/>
The timestamped key presses should now be in the newly created directory.


#### Pi
First create directory where driving images will be saved
```
mkdir driving_frames
```
After the tkinter window opened, the bluetooth connection is established. Before pressing any keys, start **capture_driving_frames.py** on your Pi (SSH connection)
```python
python3 capture_driving_frames_pi.py
```
Now you can start driving/pressing keys, to stop capturing on the Pi press *Ctrl+c* to exit.<br/>
The saved frames should now be in the newly created directory. Copy the whole directory to your main PC.

### Creating consistent Training data (synchronizing images with key presses)
Now we should have 2 new directories

* *driving_frames* (containing all collected images with timestamp name)
* *time_press_release* (containing all timestamped key presse/releases

To match the frames with the corresponding key press, create a new directory **IMG**, then type inside a console
```
python connect_data.py
```
**Note:** Adjust the *range(1,y+1)* statement inside **connect_data.py** depending on how many runs(*y*) you recorded (e.g. *3 runs*, range(1,4)). This needs to be indicated within the folder name:<br/>
driving_frames_1
driving_frames_2
driving_frames_3
time_press_release_1
time_press_release_2
time_press_release_3<br/>

After executing **connect_data.py**, all driving_frame_X images should be saved inside the **IMG** directory.
> e_press_1532344802.89.jpg

Also a new **driving_data.txt** file should have been created, containing all the image names which are saved inside the **IMG** directory.<br/>
For finally training the model, only the **IMG** directory and the **driving_data.txt** are needed.<br/>

To train the model, open **driving_model_train.py** and start training. See **Training** section above.


### Driving
**Note:** Establish bluetooth connection between Pi and HC-06 module first.<br/> 
To test the trained model, move **driving_model.h5 + self_drive_pi.py** to your Pi and type
```
python3 self_drive_pi.py
```

## Sources
* <https://devblogs.nvidia.com/deep-learning-self-driving-cars/> 

* Opencv and pi camera
  <https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/>
  
* Source of Arduino code parts
  <https://www.instructables.com/id/Arduino-Bluetooth-RC-Car-Android-Controlled/>
  
* Serial Controller code
  <https://github.com/indrekots/rc-car-controller>
  
* Setting up Bluetooth on Pi
  <https://www.youtube.com/watch?v=sEmjcgbmoRM>