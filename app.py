import streamlit as st
import replicate
import os
import tempfile

st.set_page_config(page_title="AI Video Enhancer", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Quality Enhancer")
st.write("رفع جودة وتوضيح الفيديوهات بالذكاء الاصطناعي")

# 1. قراءة التوكن تلقائياً من Secrets أو من الشريط الجانبي
api_token = st.secrets.get("REPLICATE_API_TOKEN", "")
user_token = st.sidebar.text_input("Replicate API Token:", value=api_token, type="password")

if user_token:
    api_token = user_token

# 2. التشغيل عند توفر التوكن
if api_token:
    os.environ["REPLICATE_API_TOKEN"] = api_token

    st.subheader("رفع الفيديو")
    uploaded_video = st.file_uploader("اختر فيديو للتحسين (MP4 / MOV / AVI):", type=["mp4", "mov", "avi"])

    if uploaded_video is not None:
        st.video(uploaded_video)

        if st.button("بدء تحسين الفيديو 🚀"):
            with st.spinner("جاري جلب أحدث نسخة من الموديل ومعالجة الفيديو على السيرفر..."):
                try:
                    # حفظ الفيديو في ملف مؤقت
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                        tmp_file.write(uploaded_video.read())
                        tmp_video_path = tmp_file.name

                    # جلب أحدث نسخة معتمدة تلقائياً لمنع أخطاء 404 و 422
                    model = replicate.models.get("lucataco/video-upscaler")
                    latest_version = model.latest_version.id

                    with open(tmp_video_path, "rb") as video_file:
                        output = replicate.run(
                            f"lucataco/video-upscaler:{latest_version}",
                            input={
                                "video": video_file,
                                "scale": 2
                            }
                        )

                    st.success("تمت معالجة الفيديو بنجاح!")
                    st.video(output)
                    st.markdown(f"[📥 اضغط هنا لتحميل الفيديو المعدل]({output})")

                    os.remove(tmp_video_path)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
else:
    st.warning("يرجى إدخال Replicate API Token للبدء.")
