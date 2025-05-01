# ===================== تثبيت المكتبات =====================
# لازم تثبتي دول قبل التشغيل:
# pip install streamlit pyngrok soundfile torch numpy

import streamlit as st
from pyngrok import ngrok
import torch
import numpy as np
import soundfile as sf
import os
import tempfile
import subprocess

# ===================== دالة تحويل الصوت (باستخدام so-vits-svc) =====================
def advanced_voice_processing(uploaded_wav):
    # حفظ الملف المؤقت
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
        tmp_input.write(uploaded_wav.read())
        input_path = tmp_input.name

    # مسار النموذج المدرب المفترض
    model_path = "uploaded_model.pth"
    output_path = input_path.replace(".wav", "_converted.wav")

    # أمر التحويل (لازم يكون عندك inference_main.py في نفس المجلد)
    command = [
        "python3", "inference_main.py",
        "--input_wav", input_path,
        "--output_wav", output_path,
        "--model_path", model_path
    ]

    try:
        subprocess.run(command, check=True)
        return output_path
    except Exception as e:
        st.error(f"فشل في التحويل: {e}")
        return None

# ===================== واجهة Streamlit =====================
st.set_page_config(page_title="تحويل الصوت بين بنت وولد", layout="centered")
st.title("تطبيق تحويل الصوت بين بنت وولد")

# خانة 1: رفع وتحويل الصوت
st.header("1. رفع وتحوير الصوت")
tfile = st.file_uploader("ارفع عينة صوتية (WAV)", type=["wav"])

# خانة 2: رفع النموذج
st.header("2. رفع نموذج التحويل")
model_file = st.file_uploader("ارفع ملف النموذج المدرب (.pth أو .ckpt)", type=["pth", "ckpt"])
if model_file:
    with open("uploaded_model.pth", "wb") as f:
        f.write(model_file.read())
    st.success("تم رفع النموذج بنجاح")

# خانة 3: تنفيذ التحويل
if tfile and os.path.exists("uploaded_model.pth"):
    st.info("جاري التحويل، برجاء الانتظار...")
    converted_path = advanced_voice_processing(tfile)

    if converted_path:
        st.success("تم التحويل بنجاح")

        st.subheader("الاستماع للصوت الأصلي")
        tfile.seek(0)
        st.audio(tfile, format="audio/wav")

        st.subheader("الاستماع للصوت المحول")
        st.audio(converted_path, format="audio/wav")

        with open(converted_path, "rb") as f:
            st.download_button("تحميل الصوت المحول", f, file_name="converted.wav")
    else:
        st.error("حصلت مشكلة أثناء التحويل")

# ===================== تفاصيل إضافية =====================
with st.expander("تفاصيل المشروع"):
    st.markdown("""
    - تحويل الصوت باستخدام نموذج مدرب (so-vits-svc).
    - رفع النموذج بصيغة .pth أو .ckpt.
    - دعم ملفات WAV فقط.
    - استخدام Streamlit لواجهة سهلة وتفاعلية.
    - متوافق مع ngrok لمشاركة التطبيق أونلاين.
    """)

# ===================== رابط ngrok =====================
try:
    public_url = ngrok.connect(8501)
    st.markdown(f"**رابط التطبيق أونلاين:** [اضغط هنا]({public_url})")
except:
    st.warning("تعذر إنشاء رابط ngrok. تأكد إن ngrok متثبت بشكل صحيح.")

# ===================== ملاحظات تشغيل =====================
# لتشغيل التطبيق:
# 1. ثبتي المكتبات: pip install streamlit pyngrok soundfile torch numpy
# 2. شغليه: streamlit run app.py
