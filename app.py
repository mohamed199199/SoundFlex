import streamlit as st
import torch
import soundfile as sf
import numpy as np
import os
from pathlib import Path

st.set_page_config(page_title="محول الصوت - Voice Converter", layout="centered")

st.title("محول الصوت باستخدام الذكاء الصناعي")

st.markdown("""
- تحويل الصوت باستخدام نموذج مدرب (so-vits-svc).
- رفع النموذج بصيغة .pth أو .ckpt.
- دعم ملفات WAV فقط.
- استخدام Streamlit لواجهة سهلة وتفاعلية.
""")

# ===================== واجهة الاستخدام =====================

input_audio = st.file_uploader("ارفع ملف الصوت (WAV)", type=["wav"])
model_file = st.file_uploader("ارفع ملف النموذج (.pth أو .ckpt)", type=["pth", "ckpt"])

if st.button("ابدأ التحويل"):
    if input_audio is None or model_file is None:
        st.warning("من فضلك ارفع ملف صوت وملف نموذج أولاً.")
    else:
        input_path = "input.wav"
        output_path = "output.wav"
        model_path = "model.pth"

        # حفظ الملفات المرفوعة
        with open(input_path, "wb") as f:
            f.write(input_audio.read())
        with open(model_path, "wb") as f:
            f.write(model_file.read())

        # تشغيل كود التحويل (وهمي حالياً)
        st.info("جاري التحويل...")

        data, samplerate = sf.read(input_path)
        sf.write(output_path, data, samplerate)

        st.success("تم التحويل!")
        st.audio(output_path, format="audio/wav")

# ===================== ملاحظات تشغيل =====================

# لتشغيل التطبيق:
# 1. ثبتي المكتبات: pip install streamlit soundfile torch numpy
# 2. شغليه: streamlit run app.py
