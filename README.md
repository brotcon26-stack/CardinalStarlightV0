# Cardinal Aerospace Starlight Software

When I bought the Starlight flight computer a few months ago, I intended to edit the software minimally to switch the thrust vectoring servo outputs to deploy parachutes, while using the existing logic and event triggers. I planned to map the pyrotechnic channels to the servo channels. 

I  was unable to do this due to a large number of issues that I ran into, and ended up deciding to just rewrite the main.py file from scratch. The open software that came with the board included good libraries for all of the onboard sensors, allowing me to just poll the sensors for data and use that for my logic.

The files in the src folder are the ones that are actually used in flight. I wrote all of these modules besides the 'starlight' module, which was written by the creator of the board.

Although this went through a large number of revisions, I did not start version controlling the software until much more recently, after the software was relatively mature.

The code is quite reliable at this point, but I have a large number of ideas for improvements. I intend to write a version 2 software in the near future from the ground up to implement these improvements.
