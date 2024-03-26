import io
import base64
import cv2
import numpy as np
import streamlit
from PIL import Image
from filters import *


# image download link
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format='JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


# title
streamlit.title("Artistic Image Filters")

# image upload
uploaded_file = streamlit.file_uploader('Choose an image file:', type=['png', 'jpg'])

if uploaded_file is not None:
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    input_col, output_col = streamlit.columns(2)
    with input_col:
        streamlit.header('Original')
        streamlit.image(img, channels='BRG', use_column_width=True)

    streamlit.header('Filter Options')
    option = streamlit.selectbox('Select a filter:',
                                  ('None',
                                   'Black and White',
                                   'Sepia / Vintage',
                                   'Vignette Effect',
                                   'Pencil Sketch',
                                   ))

    col1, col2, col3, col4 = streamlit.columns(4)
    with col1:
        streamlit.caption('Black and White')
        streamlit.image('filter_bw.jpg')
    with col2:
        streamlit.caption('Sepia / Vintage')
        streamlit.image('filter_sepia.jpg')
    with col3:
        streamlit.caption('Vignette Effect')
        streamlit.image('filter_vignette.jpg')
    with col4:
        streamlit.caption('Pencil Sketch')
        streamlit.image('filter_pencil_sketch.jpg')

    # flag for showing output image
    output_flag = 1
    color = 'BRG'

    if option == 'None':
        output_flag = 0
    elif option == 'Black and White':
        output = bw_filter(img)
        color = 'GRAY'
    elif option == 'Sepia / Vintage':
        output = sepia(img)
    elif option == 'Vignette Effect':
        level = streamlit.slider('level', 1, 6, 3)
        output = vignette(img, level)
    elif option == 'Pencil Sketch':
        ksize = streamlit.slider('Blur Kernel Size', 1, 11, 5, step=2)
        output = pencil_sketch(img, ksize)
        color = 'GRAY'

    with output_col:
        if output_flag == 1:
            streamlit.header('Output')
            streamlit.image(output, channels=color)

            if color == 'BGR':
                result = Image.fromarray(output[:,:,::-1])
            else:
                result = Image.fromarray((output))

            streamlit.markdown(get_image_download_link(result, 'output.png', 'Download '+'Output'), unsafe_allow_html=True)



