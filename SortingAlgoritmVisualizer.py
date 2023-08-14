import numpy as np
import imageio

# Set up the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Function to check if array is sorted
def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

# Function to draw the stacks and create a frame
def draw_stacks_frame(arr, color):
    stack_width = WINDOW_WIDTH // len(arr)
    frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    for i, height in enumerate(arr):
        frame[WINDOW_HEIGHT - height : WINDOW_HEIGHT, i * stack_width : (i + 1) * stack_width] = color

    return frame

def pigeonhole_sort(arr, writer):
    # size of range of values in the list (ie, number of pigeonholes we need)
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1

    # list of pigeonholes
    holes = [0] * size

    # populate the pigeonholes
    for x in arr:
        holes[x - min_val] += 1

    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + min_val
            i += 1
            writer.append_data(draw_stacks_frame(arr, WHITE))
    
    if is_sorted(arr):
        for _ in arr:
            writer.append_data(draw_stacks_frame(arr, GREEN))

    return arr

def visualize_sorting(arr):
    # Convert frames to a video using imageio (write incrementally)
    with imageio.get_writer("pigeonhole_sort_visualization.mp4", mode="I", fps=30, macro_block_size=None) as writer:
        pigeonhole_sort(arr, writer)


if __name__ == "__main__":
    input_list = (np.random.permutation(300) + 1).tolist()
    print(input_list)
    visualize_sorting(input_list)
