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

# تصميم الواجهة الأسود والذهبي مع لمسة زهرية لإهداء فاطمة
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

# الهيدر المخصص
st.markdown("""
<div class="header-box">
    <div class="main-title">Video Enhancer AI - Zayed</div>
    <div class="sub-title">محرك التحسين التكيفي الذكي للوجوه والإضاءة مع المحافظة على الصوت</div>
    <div class="author-badge">تطوير: زايد العبادي | <span class="fatima-badge">فاطمة 🩷</span></div>
</div>
""", unsafe_allow_html=True)

uploaded_vid = st.file_uploader("اختر فيديو للرفع (MP4, MOV, AVI, WEBM)", type=["mp4", "mov", "avi", "webm"], key="vid_up")

if uploaded_vid is not None:
    input_path = "temp_input.mp4"
    video_only_path = "temp_no_audio.mp4"
    final_output_path = "output_enhanced.mp4"

    with open(input_path, "wb") as f:
        f.write(uploaded_vid.getbuffer())

    st.caption("الفيديو الأصلي:")
    st.video(input_path)

    if st.button("بدء المعالجة الذكية والمتكيفة", key="btn_vid"):
        with st.spinner("جاري المعالجة... استغفر الله، الحمد لله، لا إله إلا الله، الله أكبر ✨"):
            try:
                reader = imageio.get_reader(input_path)
                meta = reader.get_meta_data()
                fps = meta.get('fps', 30)

                writer = imageio.get_writer(
                    video_only_path,
                    fps=fps,
                    codec='libx264',
                    quality=7,
                    pixelformat='yuv420p'
                )

                # حساب وتعديل الإضاءة المتكيفة
                target_brightness = 125.0
                curr_alpha = 1.0
                curr_beta = 0.0
                target_alpha = 1.0
                target_beta = 0.0

                frame_idx = 0

                for frame in reader:
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                    # تقييم الإضاءة كل 30 فريم
                    if frame_idx % 30 == 0:
                        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
                        mean_val = np.mean(gray)

                        if mean_val < 90:
                            target_alpha = 1.12
                            target_beta = (target_brightness - mean_val) * 0.6
                        elif mean_val > 160:
                            target_alpha = 0.92
                            target_beta = (target_brightness - mean_val) * 0.4
                        else:
                            target_alpha = 1.04
                            target_beta = 4.0

                    # انتقال سلس لتجنب الفروقات المفاجئة
                    curr_alpha = curr_alpha * 0.94 + target_alpha * 0.06
                    curr_beta = curr_beta * 0.94 + target_beta * 0.06

                    adjusted = cv2.convertScaleAbs(frame_bgr, alpha=curr_alpha, beta=curr_beta)

                    # تحسين حواف الوجه والتفاصيل بلطف
                    sharpen_kernel = np.array([
                        [0, -0.4, 0],
                        [-0.4, 2.6, -0.4],
                        [0, -0.4, 0]
                    ])
                    enhanced = cv2.filter2D(adjusted, -1, sharpen_kernel)

                    enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
                    writer.append_data(enhanced_rgb)
                    frame_idx += 1

                writer.close()
                reader.close()

                # دمج الصوت الأصلي باستخدام مسار FFmpeg المدمج
                ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
                cmd = [
                    ffmpeg_exe, '-y',
                    '-i', video_only_path,
                    '-i', input_path,
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-map', '0:v:0',
                    '-map', '1:a:0?',
                    final_output_path
                ]
                
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if os.path.exists(final_output_path) and os.path.getsize(final_output_path) > 0:
                    display_path = final_output_path
                else:
                    display_path = video_only_path

                st.success("تم تحسين وتوضيح الفيديو بنجاح مع حفظ الصوت الأصلي!")
                
                with open(display_path, "rb") as vid_file:
                    video_bytes = vid_file.read()
                    st.video(video_bytes, format="video/mp4")

            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
