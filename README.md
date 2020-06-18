# Slider input and a few other crazy ideas
Based on "Sliders for the Python mode of Processing" by Peter Farell https://github.com/hackingmath/python-sliders
Inspired by P5js.org sliders.
Also a simple way of getting data from Arduino/Firmata sensors/potentiometers.

##  
Put slider.py into the same folder as your sketch and import the Slider class at the top:
```python
from slider import Slider
```
Outside the setup function, create the slider object by giving it a range (here it's 0 to 20) and a default value for when it first runs (in this case, 6):
```python
slider1 = Slider(0,20,6)
```
Inside the setup function, give the slider a position:
```python
slider1.position(20,20)
```
In the draw function, assign the value of the slider to a variable:
```python
num = slider1.value()
```
You have the option of labeling the slider, too:
```python
slider1.label = "number"
```  

# TODO: Merge in inputs.py

### implement `.label`

## Explain or change:

### `Slider.create_defaults(Arduino)`
### `Slider.update_all()`
