import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


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


# Go to the directory of the file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get local image path
# Should be a 28x28 greyscale image, represented as a 784-long 1d array
image_path = "./filtered_clothing_image.png"
input_image = to_28x28_greyscale(image_path)
save_greyscale_image(input_image)
print(input_image.shape)  # Should print (28, 28)

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


output_label = predict(SimpleCNN(), input_tensor)
print("Raw Output: ", output_label)
print("Predicted Label: ", torch.argmax(output_label).item())

# Convert the output to a label
# Labels 0 T-shirt/top, 1 Trouser, 2 Pullover, 3 Dress, 4 Coat, 5 Sandal, 6 Shirt, 7 Sneaker, 8 Bag, 9 Ankle boot
int_to_label = {
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot",
}

print("Predicted Label: ", int_to_label[torch.argmax(output_label).item()])
