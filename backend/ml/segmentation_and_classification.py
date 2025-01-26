from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import torchvision.transforms as T
import matplotlib.pyplot as plt
import torch.nn as nn
import os
import mplcursors
import torch
import torch.nn.functional as F
import numpy as np
import sys

# Input format
# python segmentation_and_classification.py [input_path] [output_path]
input_path = ""
output_path = ""
if len(sys.argv) == 3:
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    if os.path.exists(output_path):
        raise FileExistsError(f"The file {output_path} already exists.")
else:
    raise ValueError(
        "Invalid number of arguments. Please provide input and output paths."
    )

processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
model = AutoModelForSemanticSegmentation.from_pretrained(
    "mattmdjaga/segformer_b2_clothes"
)

# url = "https://plus.unsplash.com/premium_photo-1673210886161-bfcc40f54d1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cGVyc29uJTIwc3RhbmRpbmd8ZW58MHx8MHx8&w=1000&q=80"

# image = Image.open(requests.get(url, stream=True).raw)

# Set image
# image_location = "./test_imgs/"
# image_name = "jacket.jpg"
# image_path = os.path.join(image_location, image_name)
image_path = input_path

# Label switiching
# Labels: 0: "Background", 1: "Hat", 2: "Hair", 3: "Sunglasses", 4: "Upper-clothes", 5: "Skirt", 6: "Pants", 7: "Dress", 8: "Belt", 9: "Left-shoe", 10: "Right-shoe", 11: "Face", 12: "Left-leg", 13: "Right-leg", 14: "Left-arm", 15: "Right-arm", 16: "Bag", 17: "Scarf"
int_to_label = {
    0: "Background",
    1: "Hat",
    2: "Hair",
    3: "Sunglasses",
    4: "Upper-clothes",
    5: "Skirt",
    6: "Pants",
    7: "Dress",
    8: "Belt",
    9: "Left-shoe",
    10: "Right-shoe",
    11: "Face",
    12: "Left-leg",
    13: "Right-leg",
    14: "Left-arm",
    15: "Right-arm",
    16: "Bag",
    17: "Scarf",
}

# Go to the directory of the file
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check if the file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"The file {image_path} does not exist.")

# Handle image processing
with Image.open(image_path).convert("RGB") as original_image:
    # image.show()
    inputs = processor(images=original_image, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = nn.functional.interpolate(
        logits,
        size=original_image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    # Convert to int tensor and print tensor info
    pred_seg = upsampled_logits.argmax(dim=1)[0]
    int_tensor = pred_seg.int()
    # print("\n\nImage type: ", int_tensor.type())
    # print("\nImage shape: ", int_tensor.shape)
    # print("\nImage: ", int_tensor)
    # print("\nImage unique: ", int_tensor.unique())

    # Display the image

    # Display the image
    """ processed_image = plt.imshow(int_tensor)

    # Add interactive cursor
    cursor = mplcursors.cursor(processed_image, hover=True)

    # Define the annotation function
    @cursor.connect("add")
    def on_add(sel):
        x, y = int(sel.target[0]), int(sel.target[1])
        label = int_to_label.get(int(int_tensor[y, x]), "Unknown")
        sel.annotation.set(text=label)

    plt.show() """

    # Convert to PIL image
    transform_to_image = T.ToPILImage()
    with transform_to_image(int_tensor) as processed_image:
        # processed_image.show()
        processed_image.save("processed_image.png")

        # Open the clothing image and the filter image
        clothing_image = original_image.convert("RGBA")
        filter_image = processed_image.convert("L")

        # Create a new image with an alpha channel (transparency)
        output_image = Image.new("RGBA", clothing_image.size)

        # Iterate over each pixel
        for y in range(clothing_image.height):
            for x in range(clothing_image.width):
                # Get the pixel value from the filter image
                filter_pixel = filter_image.getpixel((x, y))

                # If the filter pixel is 0, make the output pixel transparent
                if filter_pixel in [0, 2, 11, 12, 13, 14, 15]:
                    output_image.putpixel((x, y), (0, 0, 0, 0))
                else:
                    # Otherwise, copy the pixel from the clothing image
                    output_image.putpixel((x, y), clothing_image.getpixel((x, y)))

        # Save the output image
        output_image.save(output_path)
        # print("Saved filtered image")

# === Classification ===

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")


# Takes a square image and returns a 28x28 greyscale image
def to_28x28_greyscale(image_path):
    # Open the image
    with Image.open(image_path).convert("RGBA") as image:
        # Convert to greyscale
        grey_image = image.convert("L")

        # Resize to 28x28
        resized_image = grey_image.resize((28, 28))

        # Convert to numpy array
        image_array = np.array(resized_image)

    return image_array


# Save a greyscale image to a file, to test
def save_greyscale_image(image_array, output_path="./greyscale_test_out.png"):
    # Convert the numpy array to a PIL image
    image = Image.fromarray(image_array.astype(np.uint8), mode="L")

    # Save the image
    image.save(output_path)


# Get local image path
# Should be a 28x28 greyscale image, represented as a 784-long 1d array
image_path = output_path
input_image = to_28x28_greyscale(image_path)
# save_greyscale_image(input_image)
# print(input_image.shape)  # Should print (28, 28)

# Convert to a tensor
input_tensor = torch.tensor(input_image, dtype=torch.float32).reshape(-1, 1, 28, 28)


class SimpleCNN(nn.Module):
    def __init__(self, conv1_out=32, conv2_out=64, fc1_out=128):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, conv1_out, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(conv1_out)
        self.conv2 = nn.Conv2d(conv1_out, conv2_out, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(conv2_out)
        self.fc1 = nn.Linear(conv2_out * 7 * 7, fc1_out)
        self.bn3 = nn.BatchNorm1d(fc1_out)
        self.fc2 = nn.Linear(fc1_out, 10)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)
        x = F.relu(self.bn3(self.fc1(x)))
        x = self.fc2(x)
        return x


def predict(model, data):
    model.to(device)
    data = data.to(device)
    model.eval()
    with torch.no_grad():
        output = model(data)
        return output


# Predict the label
output_tensor_unprocessed = predict(SimpleCNN(), input_tensor)
output_tensor = torch.cat(
    (output_tensor_unprocessed[:, :8], output_tensor_unprocessed[:, 8 + 1 :]), dim=1
)
# output_tensor = output_tensor_unprocessed
# print("Raw Output: ", output_tensor)
# print("Predicted Int Label: ", torch.argmax(output_tensor).item())

# Convert the output to a label
# Labels 0 T-shirt/top, 1 Trouser, 2 Pullover, 3 Dress, 4 Coat, 5 Sandal, 6 Shirt, 7 Sneaker, 8 Bag, 9 Ankle boot
int_to_label = {
    0: "Top",
    1: "Pants",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandals",
    6: "Shirt",
    7: "Shoes",
    8: "Boots",
}

# print("Predicted Label: ", int_to_label[torch.argmax(output_tensor).item()])
print(int_to_label[torch.argmax(output_tensor).item()])


""" with Image.open("processed_image.png") as image:
    transform_to_PIL = T.PILToTensor()

    reopened_tensor = transform_to_PIL(image)
    print("\n\nReopened tensor: ", reopened_tensor)
    print("\nReopened tensor type: ", reopened_tensor.type())
    print("\nReopened tensor shape: ", reopened_tensor.shape)
    print("\nReopened tensor unique: ", reopened_tensor.unique()) """
