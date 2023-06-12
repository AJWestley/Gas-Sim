# Gas-Sim
A 2D simulation of ideal and non-ideal gasses.

## The Physics
The simulation uses kinetic gas theory and models the gas as a collection of balls (circles in 2D) all zipping around and filling their container. 
These collisions are all elastic and the circular shape of the particles made the collisions fairly simple to compute.

## The Programming
The most notable feature of this simulation is its use of a spatial hashmap for collision detection. I found that, before I implemented this, 
the simualation could only handle under 300 particles before it starts slowing down, but now the program can handle about 10 times as many with 
no significant performance hits.
