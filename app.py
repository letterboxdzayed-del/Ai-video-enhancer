import streamlit as st
import replicate
import os
import tempfile

# قراءة التوكن بأمان من إعدادات Streamlit Secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.set_page_config(
    page_title="Video Enhancer AI - Zayed",
    layout="centered"
)

# واجهة الفخامة السوداء والذهبية المخصصة (نفس الاستايل الأصلي)
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
.author-badge { display: inline-block; background: #121218; border: 1px solid #D4AF37; color: #F3E5AB; padding: 6px 24px; border-radius: 20px; font-size: 15px; font-weight: 800; direction: rtl; }

.stButton>button { background: linear-gradient(135deg, #D4AF37 0%, #996515 100%) !important; color: #000000 !important; font-size: 19px !important; font-weight: 900 !important; border-radius: 10px !important; border: 1px solid #FFE5B4 !important; padding: 14px 20px !important; width: 100% !important; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important; margin-top: 10px; }
section[data-testid="stFileUploadDropzone"] { background: #101015 !important; border: 2px dashed #D4AF37 !important; border-radius: 14px !important; }
section[data-testid="stFileUploadDropzone"] div { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# الهيدر بنفس الترتيب والاستايل
st.markdown("""
<div class="header-box">
    <div class="main-title">Video Enhancer AI - Zayed</div>
    <div class="sub-title">منصة توضيح وتنقيتها وترقية جودة الفيديوهات إلى 4K بالذكاء الاصطناعي مع الحفاظ على الألوان الطبيعية والوجوه</div>
    <div class="author-badge">تطوير: زايد العبادي</div>
</div>
""", unsafe_allow_html=True)

# رفع الفيديو مباشرة بدون خيارات الصور
uploaded_vid = st.file_uploader("اختر فيديو للرفع (MP4, MOV, AVI)", type=["mp4", "mov", "avi"], key="vid_up")

if uploaded_vid is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_vid.read())
    input_vid_path = tfile.name

    st.caption("الفيديو الأصلي:")
    st.video(input_vid_path)

    if st.button("بدء معالجة وترقية الجودة (Natural 4K)", key="btn_vid"):
        with st.spinner("جاري تحليل إطارات الفيديو، زيادة التحديد (Sharpness)، وترقية الجودة بدون تشويه الألوان..."):
            try:
                with open(input_vid_path, "rb") as video_file:
                    # استخدام نموذج متوازن يحافظ على الملامح والألوان الطبيعية
                    output = replicate.run(
                        "nightmareai/real-esrgan-video:b150937a077439000a40d58852877a940f90761e06ff4c3b6f0e30922e4c431d",
                        input={
                            "video": video_file,
                            "scale": 2,              # مضاعفة الأبعاد بذكاء لمنع التشويه
                            "face_enhance": False   # إيقاف التعديل الإجباري للوجوه لمنع تغيير ملامح الأشخاص
                        }
                    )
                st.success("تم تحسين الفيديو وترقية تفاصيله بنجاح!")
                st.video(output)
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الفيديو: {e}")
