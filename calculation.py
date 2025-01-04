from pathlib import Path

import cv2
import numpy as np
import torch
from flask import current_app, jsonify

from aws_s3 import upload_to_s3
from postprocess import draw_lines, draw_texts, make_color, make_line
from preparation import load_image
from preprocess import image_to_tensor

basedir = Path(__name__).parent


def detection(image, scale, threshold=0.9):
    dict_results = {}
    # load labels
    labels = current_app.config["LABELS"]
    # load image
    image = load_image(image, scale)
    # convert the image to tensor
    image_tensor = image_to_tensor(image)
    # load the pretrained model
    try:
        model = torch.load("model.pt")
    except FileNotFoundError:
        return jsonify("The model is not found"), 404

    # switch the model to inference mode
    model = model.eval()
    # inference
    output = model([image_tensor])[0]

    result_image = np.array(image.copy())
    # add borders and labels detected by pretrained model on the image
    for i, (box, label, score) in enumerate(
        zip(output["boxes"], output["labels"], output["scores"])
    ):
        # if score is above threshold
        if score >= threshold:
            # decide border color randomly
            color = make_color(labels)
            # make border
            line = make_line(result_image)
            # positions of the border of the detected image and the border of the text label
            c1 = int(box[0]), int(box[1])
            c2 = int(box[2]), int(box[3])
            # add border on the image
            draw_lines(c1, c2, result_image, line, color)
            # add text label on the image
            draw_texts(
                result_image,
                line,
                c1,
                color,
                labels[label] + f"{i}: {round(100*score.item())}%",
            )
            # create a dictionary of detected labels and scores
            dict_results[labels[label] + f"{i}"] = round(100 * score.item())
    # If you are trying at a local environment, uncomment the following two lines (lines 63 - 64).
    # Instead, comment out lines 66 and 68.
    # imagedir = str(basedir / "tmp.jpg")
    # cv2.imwrite(imagedir, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    # save detected image
    cv2.imwrite("/tmp/tmp.jpg", cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    # upload image to S3
    upload_to_s3("/tmp/tmp.jpg", "detector-app-api-tmp", "tmp.jpg")
    return jsonify(dict_results), 200
