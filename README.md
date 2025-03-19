# Spaceship Game
#### Video Demo: https://youtu.be/Wx8swCm7Gxk?si=wc8RcVXpopGOIrpO
#### Description:

#### My project is a game, inspired by Galaga, where you use your arrow keys and the Z key to destroy incoming asteroids before they hit you.

#### Let's start with the obvious ones, my project.py is where all code from any other files is executed, it's where the main game loop happens, where the switching of states happens, it's where the whole game takes place. And, of course, the test_project.py are the tests for some functions in project.py

#### custom_timer.py is a timer implementation I came up with, because the only thing raylib gives you for timers is the amount of time that's passed since the window's opened. I made a timer by snapshotting the time that the timer starts with a variable and subtracting the actual time that's passed by that snapshot. When the number that results from that equation is the time that I want, we call any function we may want to trigger after the timer is done.

#### laser.py is a file for the laser class that are instanced when the player pushes "z". It's a simple class that has a drawing and updating function. The drawing function is pretty self-explanatory, it just calls the drawing function for raylib and puts in any values. The update function makes the laser go up by a set speed and multiplies that by deltatime (the time elapsed since the last frame), to maintain movement consistency even when we're at 40 FPS or 4000 FPS.

#### menu_stuff.py is just an abstraction for drawing an empty rectangle and some text with raylib. It was getting tiring doing the same thing with raylib, having verbose functions, so I wrapped it all into a class I can draw the rectangle AND the text with.

#### meteor.py is similar to laser.py, but instead of going up, it's going down by a set speed, and there's also a random x direction and speed left and right that you go by. Whenever a meteor and a laser collide they both dissapear. Whenever a meteor and the player collides, the game over state is triggered.

#### settings.py is just some setup for the game, as well as importing all libraries that are to be used in project.py and any python files that will be in the project. If I needed a new package, I'd import it in settings.py.

#### ship.py is a class to make the ship. I'd argue I didn't need this class, but I wanted to learn more about OOP, so I did it just to learn. You move with the arrow keys, and the direction is decided by an integer that gets calculated depending on what arrow key is pressed.

#### sprites.py is a rarely used sprite class. I think I only used it for the ship class and then promptly forgot about it. I suppose I didn't need it for any other class.

#### stars.py is a file to draw a star and decide it's scale and position. These are used for the background, I loaded a list of them at the beginning of the window opening and then draw their random position and scale every frame. This random scale and position isn't recalculated every frame, which is why I put it in a class, to only do randint and other functions like that once.

## That's it! Thank you so much CS50 staff for making this course free for anyone to do and making it so darn good. You've inspired me to want to do programming as my job in the future, and I appreciate that a lot. This was CS50P!
