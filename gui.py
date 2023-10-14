import streamlit as st
from PIL import Image
import numpy as np
import io

animation_options = [
    None,
    'right', 'left',
    'up', 'down',
    'spin_clockwise', 'spin_counterclockwise',
    'zoomin', 'zoomout',
    'rotate_right', 'rotate_left',
    'rotate_up', 'rotate_down',
    'around_right', 'around_left',
    'zoomin_sinus_x', 'zoomout_sinus_y',
    'right_sinus_y', 'left_sinus_y',
    'live'
]

def create_tab_1_2(tab_key, image_size):
    imageLocation = st.empty()
    st.session_state[f"{tab_key}_text"] = st.text_input(
        "текст на баннере", 
        value="Название канала", 
        max_chars=50, 
        key=f"{tab_key}_text_input"
        )
    st.session_state[f"{tab_key}_prompt"] = st.text_input(
        "промпт для генерации баннера", 
        key=f"{tab_key}_prompt_text"
        )
    st.selectbox(
        "Анимация", 
        options=animation_options, 
        index=0, 
        key=f"{tab_key}_animation_selectbox"
        )
    
    init_image_upload = st.file_uploader(
        "Загрузи фото для стилизации (опционально)", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=False,
        key=f"{tab_key}_init_image_upload"
        )

    if init_image_upload is not None:
        st.session_state[f"{tab_key}_init_image"] = Image.open(
            io.BytesIO(init_image_upload.getvalue())
            )
    else: 
        st.session_state[f"{tab_key}_init_image"] = Image.fromarray(
            (np.random.random(size=image_size) * 255).astype(np.uint8)
            )

    imageLocation.image(
        st.session_state[f"{tab_key}_init_image"], 
        width=image_size[1]
        )

    user_image_upload = st.file_uploader(
        "Загрузи свое фото (опционально)", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=False,
        key=f"{tab_key}_user_image_upload"
        )
    if user_image_upload:
        st.session_state[f"{tab_key}_user_image"] = Image.open(
            io.BytesIO(user_image_upload.getvalue())
        )
    else: 
        st.session_state[f"{tab_key}_user_image"] = None

def create_tab_3(tab_key, image_size):
    imageLocation = st.empty()
    st.session_state[f"{tab_key}_text"] = st.text_input(
        "текст на баннере", 
        value="Название канала", 
        max_chars=50, 
        key=f"{tab_key}_text_input"
        )
    st.session_state[f"{tab_key}_prompt"] = st.text_input(
        "промпт для генерации баннера", 
        key=f"{tab_key}_prompt_text"
        )

    st.selectbox(
        "Анимация", 
        options=animation_options, 
        index=0, 
        key=f"{tab_key}_animation_selectbox"
        )
    
    init_image_upload = st.file_uploader(
        "Загрузи видео", 
        type=["mp4"], 
        accept_multiple_files=False,
        key=f"{tab_key}_init_image_upload"
        )

    if init_image_upload is not None:
        st.session_state[f"{tab_key}_init_image"] = Image.open(
            io.BytesIO(init_image_upload.getvalue())
            )
    else: 
        st.session_state[f"{tab_key}_init_image"] = Image.fromarray(
            (np.random.random(size=image_size) * 255).astype(np.uint8)
            )


    imageLocation.image(
        st.session_state[f"{tab_key}_init_image"], 
        width=image_size[1]
        )


user_data = dict()
tab1, tab2, tab3 = st.tabs(["Баннер 🌇", "Аватар 🗿", "Превью видео 🎥"])

with tab1:
    tab_key = "banner"
    st.title("Генерация Баннера 🌇")
    create_tab_1_2(tab_key, (400, 800, 3))
    st.button("Сгенерировать!", key=f"{tab_key}_generate_button", on_click=None)

with tab2:
    tab_key = "avatar"
    st.title("Генерация Аватара 🗿")
    create_tab_1_2(tab_key, (800, 800, 3))
    
    st.button("Сгенерировать!", key=f"{tab_key}_generate_button", on_click=None)

with tab3:
    tab_key = "preview"
    st.title("Генерация Превью видео 🎥")
    create_tab_3(tab_key, (400, 800, 3))
    st.button("Сгенерировать!", key=f"{tab_key}_generate_button", on_click=None)