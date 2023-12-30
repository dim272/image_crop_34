# Image crop 34
Crops photos to the required aspect ratio and reduces the file size.

### The default aspect ratio for the new image is 3:4
To change the aspect ratio, new width and height values are calculated:  
**new width** = old width  
**new height** = old width + 33.33%  

The original image is cropped in the center with the new width and height values.  
When the width of the image is greater than the height, the image file is not cropped.

### To work, you need to create two folders:
'**input**' - copy the original images here, you can use subfolders.  
'**output**' - modified images will be saved here.