import imageio.v3 as iio
import streamlit as st
from PIL import Image
import numpy as np
import cv2
import io

# from generate import (
#     generate_avatar, 
#     generate_preview, 
#     generate_banner,
#     detector, 
#     decoder, 
#     controlnet, 
#     prior
# )

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
        

if __name__ == "__main__":
    user_data = dict()
    tab1, tab2, tab3 = st.tabs(["Баннер 🌇", "Аватар 🗿", "Превью видео 🎥"])

    with tab1:
        tab_key = "banner"
        st.title("Генерация Баннера 🌇")

        st.session_state[f"{tab_key}_imageLocation"] = st.empty()
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
                (np.random.random(size=(800, 800, 3)) * 255).astype(np.uint8)
                )

        st.session_state[f"{tab_key}_imageLocation"].image(
            st.session_state[f"{tab_key}_init_image"], 
            width=800
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
        
        if st.button(label="Сгенерировать!", key=f"{tab_key}_button"):
            # image = generate_avatar(
            #     decoder, controlnet, prior, 
            #     st.session_state["preview_prompt"], 
            #     st.session_state["preview_text"], 
            #     st.session_state["preview_init_image"], 
            #     st.session_state["preview_user_image_upload"], 
            #     st.session_state["preview_animation_selectbox"], 
            # )
            image = Image.fromarray(np.ones((800, 800, 3), dtype=np.uint8) * np.random.randint(0, 255)) 
            st.session_state[f"{tab_key}_imageLocation"].image(image)

    with tab2:
        tab_key = "avatar"
        st.title("Генерация Аватара 🗿")
        

        st.session_state[f"{tab_key}_imageLocation"] = st.empty()
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
                (np.random.random(size=(800, 800, 3)) * 255).astype(np.uint8)
                )

        st.session_state[f"{tab_key}_imageLocation"].image(
            st.session_state[f"{tab_key}_init_image"], 
            width=800
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
        
        if st.button(label="Сгенерировать!", key=f"{tab_key}_button"):
    
            # image = generate_avatar(
            #     decoder, controlnet, prior, 
            #     st.session_state[f"{tab_key}_prompt"], 
            #     st.session_state[f"{tab_key}_text"], 
            #     st.session_state[f"{tab_key}_init_image"], 
            #     st.session_state[f"{tab_key}_user_image_upload"], 
            #     st.session_state[f"{tab_key}_animation_selectbox"], 
            # )
            image = Image.fromarray(np.ones((800, 800, 3), dtype=np.uint8) * np.random.randint(0, 255))
            st.session_state[f"{tab_key}_imageLocation"].image(image)
            

    with tab3:
        tab_key = "preview"
        st.session_state[f"{tab_key}_imageLocation"] = st.empty()
        st.title("Генерация Превью видео 🎥")
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
            if init_video_upload is not None: # run only when user uploads video
                vid = init_video_upload.name
                with open(vid, mode='wb') as f:
                    f.write(init_video_upload.read()) # save video to disk
                    
                vidcap = cv2.VideoCapture(vid) # load video from disk
                cur_frame = 0
                success = True
                max_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

                while success:
                    success, frame = vidcap.read() # get next frame from video
                    if cur_frame <= max_frames//2 and success: # only analyze every n=300 frames
                        if cur_frame != max_frames//2: 
                            continue
                        pil_img = Image.fromarray(frame[:, :, ::-1]) # convert opencv frame (with type()==numpy) into PIL Image
                        st.session_state[f"{tab_key}_init_image"] = pil_img
                        imageLocation.image(pil_img)
                    cur_frame += 1

        if st.button(label="Сгенерировать!", key=f"{tab_key}_button"):
            # image = generate_avatar(
            #     decoder, controlnet, prior, 
            #     st.session_state[f"{tab_key}_prompt"], 
            #     st.session_state[f"{tab_key}_text"], 
            #     st.session_state[f"{tab_key}_init_image"], 
            #     st.session_state[f"{tab_key}_animation_selectbox"], 
            # )
            image = Image.fromarray(np.ones((800, 800, 3), dtype=np.uint8) * np.random.randint(0, 255))
            st.session_state[f"{tab_key}_imageLocation"].image(image)
