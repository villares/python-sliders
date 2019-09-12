# Slider input and a few other crazy ideas
Based on "Sliders for the Python mode of Processing" by Peter Farell https://github.com/hackingmath/python-sliders
Inspired by P5js.org sliders.
Also a simple way of getting data from Arduino/Firmata sensors/potentiometers.

##  
Put slider.py into the same folder as your sketch and import the Slider class at the top:</p>
<code>from slider import Slider</code>
<p>Outside the setup function, create the slider object by giving it a range (here it's 0 to 20) and a default value for when it first runs (in this case, 6):</p>
<code>slider1 = Slider(0,20,6)</code>
<p>Inside the setup function, give the slider a position:</p>
<code>slider1.position(20,20)</code>
<p>In the draw function, assign the value of the slider to a variable:</p>
<code>num = slider1.value()</code>
<p>You have the option of labeling the slider, too:</p>
<code>slider1.label = "number"</code>

# TODO: Merge in inputs.py
## Explain or change:
### Slider.create_defaults(Arduino)
### Slider.update_all()
