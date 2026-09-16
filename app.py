import streamlit as st
import cv2
import numpy as np
import imageio
import imageio_ffmpeg as ffmpeg
import subprocess
import os

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
.sub-title { font-size: 15px; color: #e2e8f0; margin-bottom: 15px; direction: rtl; font-weight: 600; }
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
    <div class="sub-title">محرك التوضيح الذكي مع موازنة بشرة الوجوه وتعميم الانتقالات</div>
    <div class="author-badge">تطوير: زايد العبادي | <span class="fatima-badge">فاطمة 🩷</span></div>
</div>
""", unsafe_allow_html=True)

uploaded_vid = st.file_uploader("اختر فيديو للرفع (حتى 500 ميغابايت)", type=["mp4", "mov", "avi", "webm"], key="vid_up")

if uploaded_vid is not None:
    input_path = "temp_input.mp4"
    video_only_path = "temp_no_audio.mp4"
    final_output_path = "output_enhanced_1080p.mp4"

    with open(input_path, "wb") as f:
        f.write(uploaded_vid.getbuffer())

    st.caption("الفيديو الأصلي:")
    st.video(input_path)

    if st.button("بدء المعالجة والتعديل الاحترافي", key="btn_vid"):
        with st.spinner("جاري المعالجة... 🤍 (أستغفر الله العظيم - سبحان الله وبحمده - لا إله إلا الله) ✨"):
            try:
                reader = imageio.get_reader(input_path)
                meta = reader.get_meta_data()
                fps = int(meta.get('fps', 30))

                writer = imageio.get_writer(
                    video_only_path,
                    fps=fps,
                    codec='libx264',
                    ffmpeg_params=['-crf', '18', '-preset', 'fast'],
                    pixelformat='yuv420p'
                )

                prev_valid_frame = None

                for frame in reader:
                    # 1. إصلاح الرمشة الرمادية بين الانتقالات (Fix Gray Flash/Glitch)
                    gray_test = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    mean_val = np.mean(gray_test)
                    std_val = np.std(gray_test)

                    # إذا كان الفريم باهت/رمادي جداً ومفاجئ (Glitch Frame)
                    if std_val < 8 and (30 < mean_val < 100) and prev_valid_frame is not None:
                        frame = prev_valid_frame.copy()
                    else:
                        prev_valid_frame = frame.copy()

                    # 2. تحويل HSV لمعالجة درجة ألوان البشرة secara خاص
                    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
                    h, s, v = cv2.split(hsv)

                    # تحديد نطاق درجات لون البشرة (Skin Tone Detection Mask)
                    skin_mask = (h >= 0) & (h <= 25) & (s >= 30) & (s <= 180)
                    skin_mask = skin_mask.astype(np.float32)
                    skin_mask = cv2.GaussianBlur(skin_mask, (7, 7), 0)

                    # تخفيض ذكي وتكيفي للتشبع على المناطق الخاصة بالبشرة فقط
                    s_skin_reduced = s * 0.82  # تقليل نسبة التشبع الزائدة على الوجه
                    s = s * (1.0 - skin_mask * 0.28) + s_skin_reduced * (skin_mask * 0.28)
                    s = np.clip(s, 0, 255)

                    # 3. تحسين الإضاءة والتباين بشكل ناعم
                    v_uint8 = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                    clahe = cv2.createCLAHE(clipLimit=1.1, tileGridSize=(8, 8))
                    v_enhanced = clahe.apply(v_uint8).astype(np.float32)

                    # إعادة تجميع القنوات
                    hsv_enhanced = cv2.merge([h, s, v_enhanced]).astype(np.uint8)
                    rgb_enhanced = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2RGB)

                    # 4. الشاربينغ (Sharpness) كما هو بدون تغيير بناءً على طلبك
                    gray = cv2.cvtColor(rgb_enhanced, cv2.COLOR_RGB2GRAY)
                    edges = cv2.Canny(gray, 50, 150).astype(np.float32) / 255.0
                    edges = cv2.GaussianBlur(edges, (3, 3), 0)

                    gaussian = cv2.GaussianBlur(rgb_enhanced, (0, 0), 2.0)
                    sharpened_full = cv2.addWeighted(rgb_enhanced, 1.4, gaussian, -0.4, 0)

                    edges_3ch = cv2.merge([edges, edges, edges])
                    final_frame = (sharpened_full * edges_3ch + rgb_enhanced * (1.0 - edges_3ch)).astype(np.uint8)

                    writer.append_data(final_frame)

                writer.close()
                reader.close()

                # تصدير بـ 1080p
                ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
                cmd = [
                    ffmpeg_exe, '-y',
                    '-i', video_only_path,
                    '-i', input_path,
                    '-vf', "scale='if(gt(ih,iw),-2,1080)':'if(gt(ih,iw),1080,-2)'",
                    '-c:v', 'libx264',
                    '-crf', '18',
                    '-preset', 'fast',
                    '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac',
                    '-map', '0:v:0',
                    '-map', '1:a:0?',
                    final_output_path
                ]
                
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                display_path = final_output_path if os.path.exists(final_output_path) and os.path.getsize(final_output_path) > 0 else video_only_path

                st.success("تم ضبط تشبع الوجوه وإلغاء الرمشة بين الانتقالات بنجاح!")
                
                with open(display_path, "rb") as vid_file:
                    st.video(vid_file.read(), format="video/mp4")

            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
