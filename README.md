# 'Blue Marbles' - Earth Like World Generator 

This project utilises Perlin noise to generate unique earth like worlds of a random size, inspired by the famous 'Blue Marble' image taken on Apollo 17. [https://en.wikipedia.org/wiki/The_Blue_Marble]

In fact, the project makes use of two Perlin noise generators:
 1) To generate terrain and ice caps. Different noise values are assigned various colours to simulate elevation levels.
 2) To generate planet cloud coverage. 
 
Each generated planet has its own unique landmass and ice caps, along with unique cloud coverage and atmosphere. 

Shadows, simulating the dark side of the earth will appear over the planet with a chance of >= .66 percent. 


## Running The Program

### Prerequisites

Language:
```
Python 3.7 
```

Python Packages: 
```
noise
pycairo
```

### Installing

I have included a 'setup.sh' bash script that sets up the environment and runs the program, outputting a timestamped png image. This will work if running on a Unix based OS. 

The script does the following:
1) Creates a Python virtual environment
2) Activates the environment
3) Upgrades pip
4) Installs required packages to the environment
5) Runs the program, generating a world 

To run clone this project, cd into the root of the cloned folder and run: 
```
sh setup.sh 
```

### Running After Installation 

Activate the created virtual environment 

```
source ./venv/bin/activate
```

Run the main file

```
python main.py
``` 

## Custom Options

#### Custom Image Width & Height
Alter main.py and set custom values for WIDTH and HEIGHT 

#### Switch Border On / Off

By default the image is drawn with a white border to frame the image. 

To disable, alter main.py and set:
```
DRAW_BORDER = False
``` 

There are a few options the user can tinker with to customise the generated world.

#### Ice Age Mode 

By default ice age mode is switched off. Enabling ice age mode will generate an earth like planet in the midst of an ice age, with normal terrain is replaced by snow and ice. 

To enable, alter main.py and set:
```
ICE_AGE = True
``` 

#### Cloud Opacity 

Defaulted to 3.

To increase cloud opacity, alter main.py and set CLOUD_STRENGTH to a higher value than the default.

To reduce cloud visibility set lower. 

#### Ice Cap Length 

Defaulted to 0.7.

To make ice caps more prominent raise the ice cap strength, to reduce, lower the value.

To alter, edit main.py and set ICE_CAP_STRENGTH to your custom value.
