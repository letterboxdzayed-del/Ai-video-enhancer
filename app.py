import streamlit as st
import cv2
import numpy as np
import tempfile
import subprocess
import os

st.set_page_config(
    page_title="Video Enhancer AI - Zayed",
    layout="centered"
)

# تصميم الواجهة باللونين الأسود والذهبي مع لمسة وردية مخصصة لإهداء فاطمة
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
    <div class="sub-title">محرك معالجة وتنعيم الملامح، معالجة الإضاءة التكيفية، ورفع حدة الفيديوهات المتقدم</div>
    <div class="author-badge">تطوير: زايد العبادي | <span class="fatima-badge">فاطمة 🩷</span></div>
</div>
""", unsafe_allow_html=True)

uploaded_vid = st.file_uploader("اختر فيديو للرفع (MP4, MOV, AVI, WEBM)", type=["mp4", "mov", "avi", "webm"], key="vid_up")

def enhance_frame_advanced(frame):
    # 1. تنعيم البشرة والوجوه مع الحفاظ على الحدود الحادة
    smoothed = cv2.bilateralFilter(frame, d=7, sigmaColor=50, sigmaSpace=50)

    # 2. تحويل الصورة إلى الفضاء LAB للتحكم بالإضاءة والتباين
    lab = cv2.cvtColor(smoothed, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # 3. تطبيق موازن التباين التكيّفي (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    # إعادة دمج القنوات الملونة
    limg = cv2.merge((cl, a, b))
    enhanced_color = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # 4. معالجة التحديد والحدة المتقدمة (Unsharp Masking)
    gaussian_33 = cv2.GaussianBlur(enhanced_color, (0, 0), 2.0)
    final_frame = cv2.addWeighted(enhanced_color, 1.6, gaussian_33, -0.6, 0)

    return final_frame

def process_video_with_audio(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    temp_no_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_no_audio, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        enhanced = enhance_frame_advanced(frame)
        out.write(enhanced)

    cap.release()
    out.release()

    # دمج الصوت الأصلي مع الفيديو المحسّن عبر ffmpeg
    try:
        cmd = [
            'ffmpeg', '-y',
            '-i', temp_no_audio,
            '-i', input_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0?',
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except Exception:
        # في حال عدم وجود مسار صوتي بالأساس يتم حفظ الفيديو المحسن فقط
        if os.path.exists(temp_no_audio):
            os.replace(temp_no_audio, output_path)

if uploaded_vid is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_vid.getbuffer())
        input_vid_path = tfile.name

    st.caption("الفيديو الأصلي:")
    st.video(input_vid_path)

    if st.button("بدء المعالجة الذكية والتوضيح القوي", key="btn_vid"):
        with st.spinner("جاري تنعيم الوجوه، موازنة التباين، ورفع حدة الإطارات مع الحفاظ على الصوت..."):
            try:
                output_vid_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                process_video_with_audio(input_vid_path, output_vid_path)
                
                st.success("تم تحسين وتوضيح الفيديو بنجاح!")
                st.video(output_vid_path)
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

