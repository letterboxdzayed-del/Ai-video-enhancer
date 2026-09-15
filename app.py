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

# واجهة الفخامة السوداء والذهبية المخصصة مع لمسة زهرية لإهداء فاطمة
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

# الهيدر مع عبارة الإهداء لفاطمة
st.markdown("""
<div class="header-box">
    <div class="main-title">Video Enhancer AI - Zayed</div>
    <div class="sub-title">منصة توضيح وتنقيتها وترقية جودة الفيديوهات بالذكاء الاصطناعي مع الحفاظ على الألوان الطبيعية والوجوه</div>
    <div class="author-badge">تطوير: زايد العبادي | <span class="fatima-badge">فاطمة 🩷</span></div>
</div>
""", unsafe_allow_html=True)

# رفع الفيديو
uploaded_vid = st.file_uploader("اختر فيديو للرفع (MP4, MOV, AVI, WEBM)", type=["mp4", "mov", "avi", "webm"], key="vid_up")

if uploaded_vid is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_vid.getbuffer())
        input_vid_path = tfile.name

    st.caption("الفيديو الأصلي:")
    st.video(input_vid_path)

    if st.button("بدء المعالجة السريعة وترقية الجودة (Fast 4K)", key="btn_vid"):
        with st.spinner("جاري معالجة إطارات الفيديو بسرعة مع الحفاظ على الألوان والمظاهر الطبيعية..."):
            try:
                with open(input_vid_path, "rb") as video_file:
                    # تم استبدال الهاش القديم باسم النموذج الرسمي المباشر لتجنب خطأ 422
                    output = replicate.run(
                        "lucataco/real-esrgan-video:3e56ce4b57863bd03048b42bc09bdd4db20d427cca5fde9d8ae4dc60e1bb4775",
                        input={
                            "video_path": video_file,
                            "model": "RealESRGAN_x4plus",
                            "resolution": "HD"  # اختيار HD لضمان السرعة العالية وعدم إفساد ملامح الوجه والألوان
                        }
                    )
                st.success("تم تحسين الفيديو بنجاح!")
                st.video(output)
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الفيديو: {e}")
