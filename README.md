# virtual-steering-wheel

This is a basic virtual steering wheel project that I have developed to play Forza Horizon 5 with my phone. 
It is merely a prototype and I will be updating it regularly.

## How to install:
First Install the dependencies:
<code> pip install -r requirements.txt </code>

If you get error while installing vgamepad, you have to install **Visual Studio C++ Build Tools for Windows** first. Then re install the dependencies with the command above. 

## How to use:
Open the directory in Terminal and simply run `python server.py`.
Then use your **Android** Phone and open the server link on a browser. 
Make sure to use **HTTPS** as Javascript can not read `deviceorientation` event without secure connection. 


# Note for advanced users
If you want to work on this project, please make yourself at home. Together we can achieve greatness. I have to do a lot of tweaking on ths project to get the desired feel. Feel free to help.

## TO DO:

- Add vibrartion
- Smoothen Input 
- Figure out another way to fix input lag
- Setup deadzone settings and a sweet spot for steering 