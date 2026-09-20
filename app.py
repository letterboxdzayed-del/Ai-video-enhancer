import streamlit as st
import cv2
import numpy as np
import imageio_ffmpeg as ffmpeg
import subprocess
import os
import time

st.set_page_config(
    page_title="Video Enhancer AI - Zayed",
    layout="centered"
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;800;900&display=swap" rel="stylesheet">

<style>
* { font-family: 'Cairo', sans-serif !important; }
.stApp { background-color: #08080c !important; color: #ffffff !important; }
.header-box { text-align: center; padding: 25px 10px 15px 10px; border-bottom: 1px solid rgba(212, 175, 55, 0.3); margin-bottom: 25px; }
.main-title { font-size: 32px; font-weight: 900; color: #D4AF37; text-shadow: 0 0 12px rgba(212, 175, 55, 0.3); margin-bottom: 6px; direction: ltr; }
.sub-title { font-size: 16px; color: #e2e8f0; margin-bottom: 15px; direction: rtl; font-weight: 600; }
.author-badge { display: inline-block; background: #121218; border: 1px solid #D4AF37; color: #F3E5AB; padding: 6px 20px; border-radius: 20px; font-size: 15px; font-weight: 800; direction: rtl; }
.fatima-badge { color: #ff69b4; text-shadow: 0 0 8px rgba(255, 105, 180, 0.4); font-weight: 900; }

.stButton>button { background: linear-gradient(135deg, #D4AF37 0%, #996515 100%) !important; color: #000000 !important; font-size: 19px !important; font-weight: 900 !important; border-radius: 10px !important; border: 1px solid #FFE5B4 !important; padding: 14px 20px !important; width: 100% !important; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important; margin-top: 10px; }
section[data-testid="stFileUploadDropzone"] { background: #101015 !important; border: 2px dashed #D4AF37 !important; border-radius: 14px !important; }
section[data-testid="stFileUploadDropzone"] div { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <div class="main-title">Video Enhancer AI - Zayed</div>
    <div class="sub-title">تحسين جودة الفيديوهات</div>
    <div class="author-badge">تطوير: زايد العبادي | <span class="fatima-badge">فاطمة 🩷</span></div>
</div>
""", unsafe_allow_html=True)

uploaded_vid = st.file_uploader("اختر فيديو للرفع (حتى 500 ميغابايت)", type=["mp4", "mov", "avi", "webm"], key="vid_up")

if uploaded_vid is not None:
    input_path = "temp_input.mp4"
    processed_temp_path = "temp_processed.mp4"
    final_output_path = "output_enhanced_1080p.mp4"

    for temp_f in [input_path, processed_temp_path, final_output_path]:
        if os.path.exists(temp_f):
            try:
                os.remove(temp_f)
            except:
                pass

    with open(input_path, "wb") as f:
        f.write(uploaded_vid.getbuffer())

    st.caption("الفيديو الأصلي:")
    st.video(input_path)

    if st.button("بدء المعالجة ⚡", key="btn_vid"):
        start_time = time.time()
        with st.spinner("أستغفر الله العظيم - سبحان الله وبحمده - لا إله إلا الله ✨"):
            try:
                cap = cv2.VideoCapture(input_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps == 0 or np.isnan(fps):
                    fps = 30.0

                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(processed_temp_path, fourcc, fps, (width, height))

                # تحسين تباين موجه ومناسب
                clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # 1. تعزيز التباين والألوان في مساحة LAB
                    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                    l, a, b = cv2.split(lab)
                    l_enhanced = clahe.apply(l)
                    lab_enhanced = cv2.merge([l_enhanced, a, b])
                    rgb_frame = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

                    # 2. قياس مستوى التوضيح تلقائياً برياضيات سريعة
                    laplacian_var = cv2.Laplacian(l_enhanced, cv2.CV_64F).var()

                    if laplacian_var < 100:
                        sharp_amount = 1.45
                    elif laplacian_var < 300:
                        sharp_amount = 1.25
                    else:
                        sharp_amount = 1.10

                    # 3. توضيح حاد بدون استهلاك كبير للمعالج
                    blur = cv2.GaussianBlur(rgb_frame, (0, 0), 2.0)
                    sharpened = cv2.addWeighted(rgb_frame, sharp_amount, blur, -(sharp_amount - 1.0), 0)

                    # 4. قناع إضاءة سريع لحماية المناطق شديدة الظلمة والأسود من النويز
                    dark_mask = (l_enhanced > 30).astype(np.uint8)
                    dark_mask_3ch = cv2.merge([dark_mask, dark_mask, dark_mask])

                    final_frame = np.where(dark_mask_3ch == 1, sharpened, rgb_frame)

                    out.write(final_frame)

                cap.release()
                out.release()

                # دمج الصوت ورفع الدقة عبر FFmpeg بريسيت سريع جداً
                ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
                cmd = [
                    ffmpeg_exe, '-y',
                    '-i', processed_temp_path,
                    '-i', input_path,
                    '-vf', "scale='if(gt(ih,iw),-2,1080)':'if(gt(ih,iw),1080,-2)'",
                    '-c:v', 'libx264',
                    '-crf', '17',
                    '-preset', 'ultrafast',
                    '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac',
                    '-map', '0:v:0',
                    '-map', '1:a:0?',
                    final_output_path
                ]
                
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                display_path = final_output_path if os.path.exists(final_output_path) and os.path.getsize(final_output_path) > 0 else processed_temp_path

                elapsed_seconds = int(time.time() - start_time)
                mins = elapsed_seconds // 60
                secs = elapsed_seconds % 60
                
                time_str = f"{mins} min and {secs} sec" if mins > 0 else f"{secs} sec"
                st.success(f"Worked for {time_str}")
                
                with open(display_path, "rb") as vid_file:
                    st.video(vid_file.read(), format="video/mp4")

            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
