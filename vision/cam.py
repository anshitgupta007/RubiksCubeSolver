import cv2
import numpy as np
from src import util
from src import cube
# Define HSV ranges for Red, Green, Blue, White, Yellow, Orange
lower = [
     [136, 104, 111],    
     [58, 52, 62],  
    [96, 120, 35],   
     [0, 0, 240], 
    [21, 68, 90],   
    [7, 54, 100],


]

upper = [
    [180, 255, 255],   
    [83, 255, 255], 
    [140, 255, 255],     [179, 28, 255],     [34, 255, 255],  
    [22, 255, 255],

]

# Define facelet positions on the frame (adjust the positions as per your cube view)
facelet_positions = [(320, 100), (210, 100), (100, 100),
                     (320, 210), (210, 210),(100, 210) ,
                     (320, 320), (210, 320), (100, 320)]



def detect_color(hsv_frame, pos):
    """Detect the color at a specific position on the HSV frame."""
    x, y = pos
    roi = hsv_frame[y:y+50, x:x+50]
    #create a rectangle filled with green color at the roi
    
    
    avg_color = np.mean(roi, axis=(0, 1))
    avg_hsv = avg_color.astype(int)
    
    # Check each color range to find the matching color
    for i, (low, up) in enumerate(zip(lower, upper)):
        lower_bound = np.array(low)
        upper_bound = np.array(up)
        mask = cv2.inRange(roi, lower_bound, upper_bound)
        if cv2.countNonZero(mask) > 0:
            # Return the color corresponding to the index
            if i == 0:
                return 'R'  # Red
            elif i == 1:
                return 'G'  # Green
            elif i == 2:
                return 'B'  # Blue
            elif i == 3:
                return 'W'  # White
            elif i == 4:
                return 'Y'  # Yellow
            elif i == 5:
                return 'O'  # Orange
            
    
    return 'W'  # Default to white if no color is detected
def capturecube():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Storage for the final scanned cube string
    final_cube = ''
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for better alignment
        frame = cv2.flip(frame, 1)

        # Convert the frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # String to store detected colors for the current frame
        current_face = ''

        # Draw rectangles and detect colors
        for pos in facelet_positions:
            x, y = pos
            color_label = detect_color(hsv_frame, pos)
            current_face += color_label
            cv2.rectangle(frame, (x, y), (x+50, y+50), (255, 255, 255), 2)
            cv2.putText(frame, color_label, (x+5, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Display the frame with detected colors
        cv2.imshow('Rubik\'s Cube Face Detection', frame)

        # Capture the current face's colors when 's' is pressed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print(f"Captured face: {current_face}")
            
         
            final_cube += current_face
            
            if len(final_cube) == 54:
                print("All faces captured.")
                break

        # Exit the program when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting program.")
            break

    # Save the final cube string to a file
    cap.release()
    cv2.destroyAllWindows()

    return final_cube
def getcube():
    final_cube = capturecube()
    mycube = cube.generate()
    for i in range(6):
        for j in range(9):
            mycube[i][j] = util.char2num(final_cube[i * 9 + j])
    return mycube
