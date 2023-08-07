# Example Snake game
If you want to write a game for the cylinder, this snake game is a good starting point. The matrix has 4 wireless gamepads for 4 players. In this simulation, you can either use gamepads or the keyboard for game control. During events, there are always some spare gamepads available for testing.

## Overall structrue
The matrix has 84x20 pixels. Pygame lib is used for simulation. If you start the game, you will see 4 worm and 4 apples on the gameboard.

![image](https://github.com/makeTVee/BigMatrixCylinder/assets/18531000/3c87d8c4-69cc-4569-bf73-179914cd8065)

In the example the four worms are running independently.

## Controller
Good introduction to pygame joystick events: 
https://www.pygame.org/docs/ref/joystick.html

The controller is a simple SNES gamepad.
![image](https://github.com/makeTVee/BigMatrixCylinder/assets/18531000/75ec01f1-1e12-43b6-b77d-a1c54df0b9b7)

## Display matrix

Draw a Pixel at coordinates x,y with color from predefined colorset 
```
drawPixel(x,y,color)
```

Draw a Pixel at coordinates x,y with RGB color
```
drawPixelRgb(x,y,r,g,b)
```
