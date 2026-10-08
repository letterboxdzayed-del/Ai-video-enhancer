import streamlit as st
import replicate
import os
import tempfile

st.set_page_config(page_title="AI Video Enhancer", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Quality Enhancer")
st.write("رفع جودة وتوضيح الفيديوهات بالذكاء الاصطناعي")

# القائمة الجانبية للمفتاح
st.sidebar.header("إعدادات الربط")
api_token = st.sidebar.text_input("أدخل Replicate API Token:", type="password")

if api_token:
    os.environ["REPLICATE_API_TOKEN"] = api_token

    st.subheader("رفع الفيديو")
    uploaded_video = st.file_uploader("اختر فيديو للتحسين (MP4 / MOV / AVI):", type=["mp4", "mov", "avi"])

    if uploaded_video is not None:
        # عرض الفيديو الأصلي
        st.video(uploaded_video)

        if st.button("بدء تحسين الفيديو 🚀"):
            with st.spinner("جاري رفع الفيديو ومعالجته على السيرفر... قد يستغرق ذلك دقيقة حسب حجم الفيديو"):
                try:
                    # حفظ الفيديو في ملف مؤقت لإرساله إلى Replicate
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                        tmp_file.write(uploaded_video.read())
                        tmp_video_path = tmp_file.name

                    # إرسال الفيديو لموديل رفع جودة الفيديوهات
                    with open(tmp_video_path, "rb") as video_file:
                        output = replicate.run(
                            "lucataco/video-upscaler:df010214878b30f81a700863004a4aa8e08dcd37c157f12e5e1a3bc4743b1778",
                            input={
                                "video": video_file,
                                "scale": 2  # تكبير الدقة ضعفَيْن
                            }
                        )

                    st.success("تمت معالجة الفيديو بنجاح!")
                    
                    # عرض الفيديو المعالج ورابط التحميل
                    st.video(output)
                    st.markdown(f"[📥 اضغط هنا لتحميل الفيديو المعدل]({output})")

                    # تنظيف الملف المؤقت
                    os.remove(tmp_video_path)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
else:
    st.warning("يرجى إدخال Replicate API Token في الشريط الجانبي للبدء.")
