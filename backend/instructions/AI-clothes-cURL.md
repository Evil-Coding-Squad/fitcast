# AI Clothes Request

### Instructions

1. With Go installed, open a command line and enter the `backend` folder.
2. To install Python dependencies

   1. Create a new environment with `python3 -m venv env`
   2. Activate the environment with `source env/bin/activate`
   3. Run `pip install --requirement ./requirements.txt`.

3. Run `go run .` to activate the API server on your device.
4. Run the following request with Postman, using the import function, or with the command line. Make sure to replace `<your image of clothing path here>` with the path your the image you want to send.

```
curl --location 'http://localhost:8080/api/ai/segment' \
--form 'image=@"<your image of clothing path here>"
```

4. The API will take a moment to process the response, and then will return a classification of the clothing type in the "Predicted-Label" header. The raw data of the image file will also be returned in the body. **Note**: I recommend using Postman for this since it automatically displays the received image.

---

### Example

Click on this video link to see an example of the request in action:
[![Watch the video](https://img.youtube.com/vi/2X0Uqy2o3dI/maxresdefault.jpg)](https://youtu.be/2X0Uqy2o3dI)

---

##### Author: Kai Turanski
