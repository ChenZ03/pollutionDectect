# pylint: disable=import-error
import os
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
import seaborn as sns
import plotly.express as px
from plotly import tools
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit import caching
import pandas as pd
pd.plotting.register_matplotlib_converters()

st.set_option('deprecation.showPyplotGlobalUse', False)

option = st.sidebar.selectbox(
    '', ['Project Overview', 'Project Demo', 'Linear Regression Prediction'])

if option == "Project Overview":
    from PIL import Image

    st.title('Project Title')
    st.write('Project Description')

    st.subheader('Problem Statement')
    st.write('Carbon emissions from car exhaust gases contain a great number of chemical substances that are detrimental not only to the human body, but also to environmental health. In a country with high car ownership like Malaysia, many environmentally harmful gases and substances are released into the surroundings on a daily basis. In the long term, this phenomenon leads to cases of climate change, particularly global warming. As seen in the graph below, the rate of carbon emission has seen a steady increase in the past 50 years.')
    st.write('')

    img = Image.open("assets/graph.png")
    st.image(img, width=600)

    st.subheader('Solution')
    st.write('1) A clear photo of incoming traffic is taken to monitor at regular intervals on Road X, preferably during the red light when cars are stationary so as to ease the process of analysis and object detection.')
    st.write('2) Traffic analysis is carried out by counting the number of vehicles at the time of the monitoring using FDK object_detection.')

    st.subheader('Future Improvements')
    st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu laoreet lacus, non euismod quam. Vivamus ac erat ut magna pretium iaculis. Pellentesque at lorem augue. Sed non orci non nisi suscipit tincidunt a nec tellus. Sed feugiat turpis nec felis accumsan, et malesuada elit consectetur. Nullam blandit luctus erat mattis ultrices. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum efficitur gravida velit, in lobortis sapien lacinia eget. Integer sagittis est turpis, eget aliquam risus pulvinar nec.')

    st.subheader('Our Team')
    st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu laoreet lacus, non euismod quam. Vivamus ac erat ut magna pretium iaculis. Pellentesque at lorem augue. Sed non orci non nisi suscipit tincidunt a nec tellus. Sed feugiat turpis nec felis accumsan, et malesuada elit consectetur. Nullam blandit luctus erat mattis ultrices. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum efficitur gravida velit, in lobortis sapien lacinia eget. Integer sagittis est turpis, eget aliquam risus pulvinar nec.')

    st.subheader('Appendix')
    st.text('https://www.geography.org.uk/teaching-resources/singapore-malaysia/Can-Malaysia-do-anything-about-its-air-pollution#:~:text=The%20first%20is%20air%20pollution,in%20all%20its%20major%20cities.')
    st.text('https://www.ucsusa.org/resources/cars-trucks-buses-and-air-pollution')
    st.text('https://www.researchgate.net/publication/317304216_Verification_Relationship_between_Vehicle_Data_and_Air_Pollution_Index_Using_Muti-linear_Regression_Modeling')
    st.text('https://www.researchgate.net/publication/286197080_Air_pollution_study_of_vehicles_emission_in_high_volume_traffic_Selangor_Malaysia_as_a_case_study')
    st.text('https://www.titlemax.com/resources/the-effect-of-your-cars-carbon-emission/')

elif option == "Project Demo":
    st.title('Project Demo')
    st.write('')

    st.echo()
    with st.echo():
        import torch
        from src.core.detect import Detector
        from src.core.utils import utils
        from PIL import Image
        import cv2

    st.echo()
    with st.echo():
        det = Detector(name="DemoDet")

    st.echo()
    with st.echo():
        img = Image.open("assets/highway.jpg")
        st.image(img, width=700)

    st.echo()
    with st.echo():
        img_cv = utils.pil_to_cv2(img)
        output = det.predict(img_cv)
        out_img = det.visualize(img_cv, output, figsize=(18, 18))
        cv2.imwrite('tempImage.jpg', out_img)
        st.image('tempImage.jpg', width=700)

    objects = getattr(output['instances'],'pred_classes')
    list = objects.tolist()
    dict = {
        "cars": 0,
        "bus": 0,
        "truck": 0,
        "motorcycle" : 0
    }
    dict["cars"] += list.count(2)
    dict["bus"] += list.count(5)
    dict["truck"] += list.count(7)
    dict["motorcycle"] += list.count(7)
    dict

elif option == "Linear Regression Prediction":
    st.title('Extra stuff')
    st.write('Coming Soon')
    st.write('')

    st.echo()
    with st.echo():
        filepath = "./assets/data.csv"
        raw_data = pd.read_csv(filepath)

        extracted_data = raw_data.loc[raw_data['Country Name'] == 'Malaysia']
        cleaned_data = extracted_data.dropna(axis=1).drop(
            columns=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'])
        data = cleaned_data.melt(var_name='Year', value_name='Value').sort_values(
            ['Year']).reset_index(drop=True)
        data['Year Index'] = data.index + 1
    
    st.echo()
    with st.echo():
        model = tf.keras.Sequential([
            layers.Dense(units=1)
        ])

        model.compile(
            optimizer=tf.optimizers.Adam(learning_rate=0.1),
            loss='mean_absolute_error'
        )

        history = model.fit(
            data['Year Index'], data['Value'],
            epochs=50
        )

        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch

    st.echo()
    with st.echo():
        x = tf.linspace(1, 70, 2)
        y = model.predict(x)

    st.echo()
    with st.echo():
        plt.plot(history.history['loss'], label='loss')
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.legend()
        plt.grid(True)
        st.pyplot(clear_figure=True)

    st.echo()
    with st.echo():
        plt.scatter(data['Year Index'], data['Value'], label='Data')
        plt.plot(x, y, color='m', label='Predictions')
        plt.xlabel('Year Index')
        plt.ylabel('Value')
        plt.title('Carbon Emissions')
        plt.legend()
        st.pyplot(clear_figure=True)
