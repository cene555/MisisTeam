import imageio.v3 as iio
import streamlit as st
from PIL import Image
import numpy as np
import cv2
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

def generate_image(prompt, text, user_image, image_size=(768, 768)):
    return Image.open("test.jpg").resize(image_size)

def generate_video():
    return Image.open("test.mp4")

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
    
    init_video_upload = st.file_uploader(
        "Загрузи видео", 
        type=["mp4"], 
        accept_multiple_files=False,
        key=f"{tab_key}_init_image_upload"
        )

    frame_skip = 1 # display every 300 frames

    if init_video_upload is not None: # run only when user uploads video
        # vid = init_video_upload.name
        # with open(vid, mode='wb') as f:
        #     f.write(init_video_upload.read()) # save video to disk

        # st.markdown(f"""
        # ### Files
        # - {vid}
        # """,
        # unsafe_allow_html=True) # display file name

        # vidcap = cv2.VideoCapture(vid) # load video from disk
        # cur_frame = 0
        # success = True

        # while success:
        #     success, frame = vidcap.read() # get next frame from video
        #     if cur_frame % frame_skip == 0: # only analyze every n=300 frames
        #         print('frame: {}'.format(cur_frame)) 
        #         st.session_state[f"{tab_key}_init_image"] = Image.fromarray(frame) # convert opencv frame (with type()==numpy) into PIL Image
        #         imageLocation.image(
        #             st.session_state[f"{tab_key}_init_image"], 
        #             width=image_size[1]
        #         )
        #     cur_frame += 1

        # read a single frame
        metadata = iio.immeta(init_video_upload.name, exclude_applied=False)
        max_frames = int(metadata["fps"] * metadata["duration"])
        
        if max_frames >= 1000: 
            frame_idx = 1000
        else: 
            frame_idx = max_frames // 2
        print("\n\n\n", frame_idx, "\n\n\n\n")
        st.write(max_frames)
        st.session_state[f"{tab_key}_init_image"] = iio.imread(
            init_video_upload.name,
            index=frame_idx,
            plugin="pyav",
        )
        imageLocation.image(
                st.session_state[f"{tab_key}_init_image"], 
                width=image_size[1]
        )

    st.button("Сгенерировать!", key=f"{tab_key}_generate_button", on_click=None)

user_data = dict()
tab1, tab2, tab3 = st.tabs(["Баннер 🌇", "Аватар 🗿", "Превью видео 🎥"])

with tab1:
    tab_key = "banner"
    st.title("Генерация Баннера 🌇")
    create_tab_1_2(tab_key, (400, 800, 3))

with tab2:
    tab_key = "avatar"
    st.title("Генерация Аватара 🗿")
    create_tab_1_2(tab_key, (800, 800, 3))
    
with tab3:
    tab_key = "preview"
    st.title("Генерация Превью видео 🎥")
    create_tab_3(tab_key, (400, 800, 3))