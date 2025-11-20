import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io
from rembg import remove

# --- 页面配置 ---
st.set_page_config(page_title="马尊影像工坊", page_icon="🎨", layout="wide")

# --- 隐藏菜单 CSS ---
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 侧边栏导航 ---
st.sidebar.title("🎨 马尊影像工坊")
app_mode = st.sidebar.selectbox("选择功能模块", [
    "✨ 智能美颜 (Beauty)",
    "🪄 AI 智能抠图 (Remove BG)",
    "🆔 证件照换底 (ID Photo)",
    "🎨 艺术滤镜 (Filters)",
    "📉 格式/压缩 (Converter)",
    "💧 水印管家 (Watermark)"
])

# --- 公共函数 ---
def convert_image(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- 模块 1: 智能美颜 ---
def app_beauty():
    st.title("✨ 专业级智能美颜")
    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'png', 'jpeg'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        img_cv = cv2.cvtColor(np.array(image.convert('RGB')), cv2.COLOR_RGB2BGR)
        
        c1, c2 = st.columns(2)
        with c1:
            smooth = st.slider("🧴 磨皮", 0, 100, 50)
            white = st.slider("💡 美白", 0, 100, 30)
        with c2:
            sharpen = st.slider("👁️ 锐化", 0, 100, 20)
            saturate = st.slider("🌹 红润", 0, 100, 20)
        
        # 处理
        d = 5 + int(smooth/5)
        img_smooth = cv2.bilateralFilter(img_cv, d, smooth*2, 75)
        img_pil = Image.fromarray(cv2.cvtColor(img_smooth, cv2.COLOR_BGR2RGB))
        
        # 美白与锐化
        if white > 0: img_pil = ImageEnhance.Brightness(img_pil).enhance(1.0 + white/200.0)
        if saturate > 0: img_pil = ImageEnhance.Color(img_pil).enhance(1.0 + saturate/100.0)
        
        st.image(img_pil, caption="美颜后", use_column_width=True)
        st.download_button("⬇️ 下载美颜照", convert_image(img_pil), "beauty.png", "image/png")

# --- 模块 2: AI 抠图 ---
def app_remove_bg():
    st.title("🪄 AI 一键抠图")
    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="原图", width=300)
        if st.button("🚀 开始抠图"):
            with st.spinner("AI 正在识别主体..."):
                result = remove(image)
                st.image(result, caption="抠图结果 (透明背景)", use_column_width=True)
                st.download_button("⬇️ 下载PNG", convert_image(result), "rmbg.png", "image/png")

# --- 模块 3: 证件照换底 ---
def app_id_photo():
    st.title("🆔 证件照自动换底")
    uploaded_file = st.file_uploader("上传人像照片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        color = st.radio("选择底色", ["⚪ 白色", "🔴 红色", "� 蓝色"])
        
        if st.button("生成证件照"):
            with st.spinner("正在处理..."):
                fg = remove(image)
                bg_color = (255, 255, 255) if "白" in color else (255, 0, 0) if "红" in color else (67, 142, 219)
                new_img = Image.new("RGB", fg.size, bg_color)
                new_img.paste(fg, (0, 0), fg)
                st.image(new_img, caption=f"{color}底证件照", width=300)
                st.download_button("⬇️ 下载证件照", convert_image(new_img), "id_photo.png", "image/png")

# --- 模块 4: 艺术滤镜 ---
def app_filters():
    st.title("🎨 创意艺术滤镜")
    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        option = st.selectbox("选择滤镜", ["� 素描 (Sketch)", "🎞️ 黑白 (Grayscale)", "🌆 怀旧 (Sepia)"])
        
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        if "素描" in option:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            inv = 255 - gray
            blur = cv2.GaussianBlur(inv, (21, 21), 0)
            res = cv2.divide(gray, 255 - blur, scale=256.0)
            res = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB)
        elif "黑白" in option:
            res = cv2.cvtColor(cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
        else:
            res = img_cv  # 默认
            
        st.image(res, caption="滤镜效果", use_column_width=True)
        st.download_button("⬇️ 下载图片", convert_image(Image.fromarray(res)), "filter.png", "image/png")

# --- 模块 5: 格式转换 ---
def app_converter():
    st.title("📉 格式转换工厂")
    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'png', 'webp'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.write(f"原始尺寸: {image.size}")
        to_format = st.selectbox("转换为", ["PNG", "JPEG", "PDF"])
        quality = st.slider("压缩质量 (仅JPEG)", 10, 100, 80)
        
        if st.button("开始转换"):
            buf = io.BytesIO()
            if to_format == "JPEG":
                image = image.convert('RGB')
                image.save(buf, format="JPEG", quality=quality)
            elif to_format == "PDF":
                image = image.convert('RGB')
                image.save(buf, format="PDF")
            else:
                image.save(buf, format="PNG")
            
            st.download_button(f"⬇️ 下载 {to_format}", buf.getvalue(), f"new_image.{to_format.lower()}")

# --- 模块 6: 水印管家 ---
def app_watermark():
    st.title("💧 图片加水印")
    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGBA")
        text = st.text_input("水印文字", "马尊出品")
        opacity = st.slider("透明度", 0, 255, 128)
        
        if st.button("添加水印"):
            txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            # 简单处理：文字印在右下角
            w, h = image.size
            draw.text((w-150, h-50), text, fill=(255, 255, 255, opacity))
            out = Image.alpha_composite(image, txt_layer)
            st.image(out, caption="水印效果", use_column_width=True)
            st.download_button("⬇️ 下载", convert_image(out), "watermark.png", "image/png")

# --- 路由控制 ---
if app_mode == "✨ 智能美颜 (Beauty)":
    app_beauty()
elif app_mode == "🪄 AI 智能抠图 (Remove BG)":
    app_remove_bg()
elif app_mode == "🆔 证件照换底 (ID Photo)":
    app_id_photo()
elif app_mode == "🎨 艺术滤镜 (Filters)":
    app_filters()
elif app_mode == "📉 格式/压缩 (Converter)":
    app_converter()
elif app_mode == "� 水印管家 (Watermark)":
    app_watermark()