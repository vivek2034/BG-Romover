
from PIL import Image
import numpy as np

def remove_background(input_path, output_path):
    # Dummy background remover: convert white to transparent
    image = Image.open(input_path).convert("RGBA")
    data = np.array(image)

    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    mask = (r > 240) & (g > 240) & (b > 240)
    data[mask] = [255, 255, 255, 0]

    result = Image.fromarray(data)
    result.save(output_path)
