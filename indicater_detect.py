import requests
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

def detection(path):
  model_name = "indicator-j3riv"
  version = 4
  api_key = "6GfuPFK2Ue4Fvh9EZiQJ"
  api_url = f"https://detect.roboflow.com/{model_name}/{version}?api_key={api_key}&format=json"
  image_path = path
  with open(image_path, "rb") as image_file:
      response = requests.post(api_url, files={"file": image_file})
  if response.status_code == 200:
      data = response.json()
      image = cv2.imread(image_path)
      if "predictions" in data and len(data["predictions"]) > 0:
          output_dir = "cropped_objects"
          os.makedirs(output_dir, exist_ok=True)
          for i, obj in enumerate(data["predictions"]):
              x, y, w, h = int(obj["x"]), int(obj["y"]), int(obj["width"]), int(obj["height"])
              label = obj["class"]
              confidence = obj["confidence"]
              x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
              x2, y2 = min(image.shape[1], x + w // 2), min(image.shape[0], y + h // 2)
              cropped_obj = image[y1:y2, x1:x2]
              cropped_filename = os.path.join(output_dir, f"{label}_{i}.jpg")
              cv2.imwrite(cropped_filename, cropped_obj)
              plt.figure()
              plt.imshow(cv2.cvtColor(cropped_obj, cv2.COLOR_BGR2RGB))
              plt.axis("off")
              plt.title(f"{label} ({confidence:.2f})")
              plt.show()

detection("img.jpg")
