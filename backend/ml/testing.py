from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import torchvision.transforms as T
import matplotlib.pyplot as plt
import torch.nn as nn
import os

processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
model = AutoModelForSemanticSegmentation.from_pretrained(
    "mattmdjaga/segformer_b2_clothes"
)

# url = "https://plus.unsplash.com/premium_photo-1673210886161-bfcc40f54d1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cGVyc29uJTIwc3RhbmRpbmd8ZW58MHx8MHx8&w=1000&q=80"

# image = Image.open(requests.get(url, stream=True).raw)

# Set image
image_location = "./test_imgs/"
image_name = "shirt.png"
image_path = os.path.join(image_location, image_name)

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
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check if the file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"The file {image_path} does not exist.")

# Handle image processing
with Image.open(image_path) as image:
    # image.show()
    inputs = processor(images=image, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0]
    int_tensor = pred_seg.int()
    print("\n\nImage type: ", int_tensor.type())
    print("\n\nImage shape: ", int_tensor.shape)
    print("\n\nImage: ", int_tensor)
    print("\n\nImage unique: ", int_tensor.unique())

    # processed_image = plt.imshow(pred_seg)
    # plt.axis("off")
    # processed_image.make_image()
    # plt.show()

    # Convert to PIL image
    transform_to_image = T.ToPILImage()
    with transform_to_image(int_tensor) as processed_image:
        processed_image.show()
        processed_image.save("processed_image.png")

with Image.open("processed_image.png") as image:
    transform_to_PIL = T.PILToTensor()

    reopened_tensor = transform_to_PIL(image)
    print("\n\nReopened tensor: ", reopened_tensor)
    print("\n\nReopened tensor type: ", reopened_tensor.type())
    print("\n\nReopened tensor shape: ", reopened_tensor.shape)
    print("\n\nReopened tensor unique: ", reopened_tensor.unique())
