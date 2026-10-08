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
            with st.spinner("جاري معالجة الفيديو بالذكاء الاصطناعي... قد يستغرق العمل من 1 إلى 3 دقائق"):
                try:
                    # حفظ الفيديو في ملف مؤقت
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                        tmp_file.write(uploaded_video.read())
                        tmp_video_path = tmp_file.name

                    # استخدام موديل Real-ESRGAN الرسمي والمعتمد للفيديوهات على Replicate
                    with open(tmp_video_path, "rb") as video_file:
                        output = replicate.run(
                            "lucataco/real-esrgan-video:e28238703271d43a6d713c7ee83a5472f1025539d8c0b299a73898b31a31e843",
                            input={
                                "video": video_file,
                                "fps": 0  # للحفاظ على عدد الفريمات الأصلي للفيديو
                            }
                        )

                    st.success("تمت معالجة الفيديو بنجاح!")
                    st.video(output)
                    st.markdown(f"[📥 اضغط هنا لتحميل الفيديو المعدل]({output})")

                    # حذف الملف المؤقت
                    os.remove(tmp_video_path)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
else:
    st.warning("يرجى إدخال Replicate API Token للبدء.")
