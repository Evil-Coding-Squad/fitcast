from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import torchvision.transforms as T
import matplotlib.pyplot as plt
import torch.nn as nn
import os
import mplcursors

processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
model = AutoModelForSemanticSegmentation.from_pretrained(
    "mattmdjaga/segformer_b2_clothes"
)

# url = "https://plus.unsplash.com/premium_photo-1673210886161-bfcc40f54d1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cGVyc29uJTIwc3RhbmRpbmd8ZW58MHx8MHx8&w=1000&q=80"

# image = Image.open(requests.get(url, stream=True).raw)

# Set image
image_location = "./test_imgs/"
image_name = "top.png"
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
        output_image.save("filtered_clothing_image.png")
        print("Saved filtered image")

""" with Image.open("processed_image.png") as image:
    transform_to_PIL = T.PILToTensor()

    reopened_tensor = transform_to_PIL(image)
    print("\n\nReopened tensor: ", reopened_tensor)
    print("\nReopened tensor type: ", reopened_tensor.type())
    print("\nReopened tensor shape: ", reopened_tensor.shape)
    print("\nReopened tensor unique: ", reopened_tensor.unique()) """
