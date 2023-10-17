import cv2
import numpy as np
import triangle
import matplotlib.pyplot as plt
import json

def process_image(input_path, output_path):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 220, 240)
    kernel = np.ones((5,5),np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    points = []
    segments = []
    segment_start = 0
    for i, contour in enumerate(contours):
        if hierarchy[0][i][2] == -1:
            epsilon = 0.001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
            
            for j in range(len(approx) - 1):
                segments.append([segment_start + j, segment_start + j + 1])
            segments.append([segment_start + len(approx) - 1, segment_start])
            
            segment_start += len(approx)
            points.extend(approx)

    cv2.imwrite(output_path, image)
    
    vertex_array = np.vstack(points).astype(np.float32)
    vertex_dict = {'vertices': vertex_array, 'segments': segments}
    tri_data = triangle.triangulate(vertex_dict, 'pa800')
    triangles = tri_data['triangles']
    triangle_points = []
    for tri in triangles:
        triangle_points.append([tri_data['vertices'][tri[0]], tri_data['vertices'][tri[1]], tri_data['vertices'][tri[2]]])

    return tri_data, triangle_points

def visualize_triangles(image_path, tri_data):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    plt.imshow(img)
    plt.triplot(tri_data['vertices'][:,0], tri_data['vertices'][:,1], tri_data['triangles'], color='b')
    plt.show()
    
def triangles_to_json(triangle_points, image):
    data = {
        "resolution": list(image.shape[1::-1]),
        "background": [0.5, 0.5, 0.5], 
        "objects": []
    }

    for points in triangle_points:
        obj = {
            "type": "triangle",
            "p0": list(map(int, points[0])),
            "p1": list(map(int, points[1])),
            "p2": list(map(int, points[2])),
            "color": [0.9, 0.9, 0.3],  
            "alpha": 1.0  
        }
        data["objects"].append(obj)

    return data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    input_path = 'bear.jpg'
    output_path = 'drawContours.jpg'
    
    tri_data, triangle_points = process_image(input_path, output_path)
    visualize_triangles(input_path, tri_data)
    image = cv2.imread(input_path)
    json_data = triangles_to_json(triangle_points, image)
    save_to_json(json_data, 'triangles.json')

if __name__ == "__main__":
    main()