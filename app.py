import streamlit as st
import replicate
import os
import tempfile

# حقن التوكين الجديد والنظيف الخاص بك مباشرة داخل بيئة التشغيل
os.environ["REPLICATE_API_TOKEN"] = "r8_aeg9IioLuMuqlrzz9gkd7ZaN5gNIJrf28z5CV"

st.set_page_config(
    page_title="Enhancer AI - Zayed",
    layout="centered"
)

# واجهة الفخامة السوداء والذهبية المخصصة
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

div[data-testid="stRadio"] > div { display: flex !important; flex-direction: row-reverse !important; background: #101015 !important; padding: 8px !important; border-radius: 12px !important; border: 1px solid #282830 !important; gap: 8px !important; margin-bottom: 20px !important; }
div[data-testid="stRadio"] label { flex: 1 !important; text-align: center !important; color: #ffffff !important; background-color: #1a1a22 !important; padding: 12px 8px !important; border-radius: 8px !important; font-weight: 800 !important; font-size: 15px !important; cursor: pointer !important; border: 1px solid #2d2d38 !important; }
div[data-testid="stRadio"] label > div:first-child { display: none !important; }
div[data-testid="stRadio"] label[data-checked="true"] { background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important; color: #000000 !important; font-weight: 900 !important; border: 1px solid #FFF8DC !important; box-shadow: 0 2px 10px rgba(212, 175, 55, 0.3) !important; }
.stButton>button { background: linear-gradient(135deg, #D4AF37 0%, #996515 100%) !important; color: #000000 !important; font-size: 19px !important; font-weight: 900 !important; border-radius: 10px !important; border: 1px solid #FFE5B4 !important; padding: 14px 20px !important; width: 100% !important; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important; }
section[data-testid="stFileUploadDropzone"] { background: #101015 !important; border: 2px dashed #D4AF37 !important; border-radius: 14px !important; }
section[data-testid="stFileUploadDropzone"] div { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <div class="main-title">Enhancer AI - Zayed</div>
    <div class="sub-title">منصة توضيح الوجوه وتحسين الصور والفيديو بالذكاء الاصطناعي بدقة فائقة</div>
    <div class="author-badge">تطوير: زايد العبادي</div>
</div>
""", unsafe_allow_html=True)

main_mode = st.radio(
    "اختر نوع الملف",
    ["تحسين الصور (AI)", "تحسين الفيديوهات (AI)"],
    horizontal=True,
    label_visibility="collapsed"
)

# ----------------- [ تحسين الصور ] -----------------
if main_mode == "تحسين الصور (AI)":
    uploaded_img = st.file_uploader("اختر صورة للرفع", type=["jpg", "jpeg", "png", "webp"], key="img_up")

    if uploaded_img is not None:
        st.image(uploaded_img, caption="الصورة الأصلية", use_container_width=True)

        if st.button("بدء تحسين الجودة والوجوه بـ AI", key="btn_img"):
            with st.spinner("جاري معالجة الصورة وإعادة رسم التفاصيل والوجوه بدقة خرافية..."):
                try:
                    output = replicate.run(
                        "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db788775d71320b54",
                        input={
                            "image": uploaded_img,
                            "upscale": 4,
                            "face_upsample": True,
                            "codeformer_fidelity": 0.8
                        }
                    )
                    st.success("تم التحسين بدقة مذهلة بنجاح!")
                    st.image(output, caption="الصورة بعد تحسين AI", use_container_width=True)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")

# ----------------- [ تحسين الفيديوهات ] -----------------
else:
    uploaded_vid = st.file_uploader("اختر فيديو للرفع", type=["mp4", "mov", "avi"], key="vid_up")

    if uploaded_vid is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_vid.read())
        input_vid_path = tfile.name

        st.video(input_vid_path)

        if st.button("بدء تحسين الفيديو بـ AI", key="btn_vid"):
            with st.spinner("جاري رفع الجودة وتصفية إطارات الفيديو بالذكاء الاصطناعي... يرجى الانتظار"):
                try:
                    with open(input_vid_path, "rb") as video_file:
                        output = replicate.run(
                            "lucataco/real-esrgan-video:3e56ce4b57863bd03048b42bc09bdd4db20d427cca5fde9d8ae4dc60e1bb4775",
                            input={
                                "model": "RealESRGAN_x4plus",
                                "resolution": "UHD",
                                "video_path": video_file
                            }
                        )
                    st.success("تم تحسين الفيديو بجودة فائقة بنجاح!")
                    st.video(output)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء معالجة الفيديو: {e}")
