#!/bin/python

'![zones](/DopeTrope/assets/images/2017-04-16-Deep-Q-Learning-For-Self-Driving-Cars/02-zones.png "The closer a car gets to the agent the more punishment it recieves. Only a collision will cause the run to end (this is know as a terminal state)")'

<center><img src="/DopeTrope/assets/images/2017-04-16-Deep-Q-Learning-For-Self-Driving-Cars/01-sim.png" alt="simulator">  
<br><span class="caption"><em>Screen shot of the PyGame Simulator. The red car is agent, it is the goal of the agent to place the orange dot in one of the lanes, the car is programmed to track the dot with a simple PID loop. The lines fanning out infront of the car are simulating LiDAR beams. The colour of the LiDAR lines indicates how close another car is. Finally the gray cars are TERRIBLE drivers, programmed to randomly change lanes with zero regard for agent's wellbeing.</em></span></center>
