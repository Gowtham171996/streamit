# https://huggingface.co/spaces/Vishaltiwari2019/Object-Detection-with-NLP/blob/main/app.py

import random,collections
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image,ImageDraw
import requests
import streamlit as st
import pandas as pd

from headerfooter import footer,Disclaimer,JobSearch,Getlogo

def DetectImage(image):
    # you can specify the revision tag if you don't want the timm dependency
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.8)[0]

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
        )
    return model,results

def plot_results(model,img, results):
    img = ImageDraw.Draw(image)
    detected_objects = []
    for i, (score, label, box) in enumerate(zip(results["scores"], results["labels"], results["boxes"])):
        box = [round(i, 2) for i in box.tolist()]
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        img.rectangle(box, outline=color, width=3)
        label_text = f"{model.config.id2label[label.item()]}: {round(score.item(), 2)}"
        # Larger and bolder font
        img.text((box[0], box[1]), label_text, fill=color,)
        detected_objects.append(model.config.id2label[label.item()])

    return image, detected_objects
    #return image, ', '.join(detected_objects)
    

st.set_page_config(page_title = "Generic Object Detection",
                    layout='centered',
                    initial_sidebar_state = "collapsed")


col1, col2 = st.columns([60,40],gap="medium",vertical_alignment="bottom")
with st.container(border=True):
    with col1:
        st.header("Generic Object Detection")
    with col2:    
        if st.button("Home",use_container_width=True):
            st.switch_page("Home.py")

st.write("---")

with st.container(border=True):

    on = st.toggle("Toggle to input Custom Image URL or Select a image from dropdown")
    if on:
        input_URL = st.text_input('''Enter the URL to Image in JPEG format:''',"https://walk21.com/wp-content/uploads/2021/03/berlin-800x800.jpg")
    else:
        input_URL = st.selectbox(
            "Select an image:",
            (
            "https://www.berlin.de/binaries/asset/image_assets/8322030/ratio_2_1/1726134278/972x486/",
            "https://images.squarespace-cdn.com/content/v1/60e7a1a3e172013cc845137c/10c9f18e-a2c2-49b1-bab7-9bafd669c299/pexels-brett-sayles-1467807.jpg",
            "https://walk21.com/wp-content/uploads/2021/03/berlin-800x800.jpg"),
        )
    

    image = Image.open(requests.get(input_URL, stream=True).raw)

    submit = st.button("Generate",use_container_width=True)
    
    
    if submit:
        st.caption("Please scroll down to see results.")
        with st.container(border=True):
            st.subheader("Original Image")
            st.image(image)
        st.write("---")
        with st.container(border=True):
            st.subheader("Object Detected Image")
            with st.spinner("Running the model... just few seconds more...."):
                model,results = DetectImage(image)
                bboximage,detectedobjects = plot_results(model,image, results)
                st.image(bboximage)
                
                detectedobjects = collections.Counter(detectedobjects)
                df = pd.DataFrame.from_dict(detectedobjects, orient='index').reset_index()
                df = df.rename(columns={'index':'Category', 0:'count'})
                st.table(df)
        

Disclaimer()

st.markdown(footer,unsafe_allow_html=True)
#Getlogo()
JobSearch()