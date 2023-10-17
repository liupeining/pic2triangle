# pic2triangle
Welcome to the Image Triangulation Tool -- **img2triangle**! This utility takes in an image and processes it to identify boundaries and further triangulates the segmented image to create an artistic representation. The output is saved as a JSON file, which can be rendered using a suitable renderer.

## Features
1. Image Boundary Detection.
2. Triangular partitioning of the image regions.
3. Visualization of the triangulated image.
4. Exporting the triangles' data as JSON.

## How to use it
### Environment Setup
Before you start, ensure you have the following python libraries dependencies installed:
* OpenCV (cv2)
* NumPy (numpy)
* Triangle (triangle)
* Matplotlib (matplotlib)

You can install all these libraries using pip:
```
pip install opencv-python numpy triangle matplotlib
```
### Execution Steps
To activate the tool, run the Python script as follows:
```
python img2triangle.py
```

## Systematic Breakdown
### Input Image
Start by designing your own graphic image. This could be an image you've created using a digital drawing tool on your PC, an artwork on your iPad, or even a hand-drawn sketch that you've scanned.
![input example](bear.jpg)

### Boundary Detection Phase
The tool utilizes OpenCV's robust functions to detect image boundaries, thereby outlining major image segments.
* Edge Detection: The OpenCV library's Canny function serves to detect edges within the source image.
* Contour Identification: Edges that have been detected are accentuated using dilation. Post dilation, contours are isolated from these boundaries.
* Polygonal Simplification: The approxPolyDP function simplifies each contour into polygonal shapes, permitting the representation of intricate designs as rudimentary polygons.
![Boundary Detection output](/example/drawContours_exp.jpg)

### Triangulation Process
The previously identified boundaries are processed further to produce a triangular partitioning of the image. 
* Triangulation Operation: With the Triangle library, the tool methodically partitions the identified regions into triangles.
![Triangulation Process](/example/triangulation_exp.png)

### Visualization via JSON
The derived triangular data is transcribed into a JSON file. This JSON file can then be processed by various renderers to visualize the triangulated design.
* JSON Compilation: All triangular data is documented in a systematic JSON format, which enhances usability across different applications.
![Render Result](/example/triangulation_exp.png)