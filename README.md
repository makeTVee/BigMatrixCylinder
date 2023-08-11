# BigMatrixCylinder

The BigMatrixCylinder is a large LED cylinder with 1680 addressable LEDs (84x20 matrix) showing beautiful animations and allowing up to 4 people playing games like Tetris against each other. In party mode, it shows audio triggered animations and is controlled via ArtNet. It's powered by either a Raspberry Pi, a Teensy 4, a PixelBlaze. The cylinder has a diameter of 90cm and a height of 70cm.

![image](https://github.com/makeTVee/BigMatrixCylinder/assets/18531000/c600e6b2-864a-4ea3-a0e9-51fce3c3d0de)

## Custom Animations

Easiest way of preparing custom animations are GIF files or picture slideshows. GIFs can be streched to the matrix size, but best results will be generated with native 21:5 aspect ratio (84x20 pixel). Currently, GIFs are played with fixed transition time between the frames, but overall speed can be changed.

## Custom Games
Simple example of a 4-player snake game in the example_game folder. Requires pygame lib.
