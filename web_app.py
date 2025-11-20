import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance
import io

# --- 页面配置 ---
st.set_page_config(page_title="马尊专业修图", page_icon="📸", layout="wide")

# --- 隐藏默认菜单 CSS ---
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📸 Magic Studio Pro | 马尊专业影像工作台")
st.markdown("---")

# --- 侧边栏 ---
st.sidebar.title("🎛️ 调色控制台")
uploaded_file = st.sidebar.file_uploader("📂 上传高清图片", type=['jpg', 'png', 'jpeg'])

# --- 核心处理函数 ---
def apply_pro_beauty(img_cv, smooth, white, sharpen, saturate, bright):
    # 1. 智能磨皮 (双边滤波 - 保留边缘)
    # 参数映射：将 0-100 映射到算法参数
    d = 5 + int(smooth / 5)
    sigmaColor = smooth * 1.5
    sigmaSpace = 75
    img_smooth = cv2.bilateralFilter(img_cv, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
    
    # 2. 细节增强 (USM 锐化 - 让眼睛更有神)
    if sharpen > 0:
        gaussian = cv2.GaussianBlur(img_smooth, (0, 0), 3.0)
        img_smooth = cv2.addWeighted(img_smooth, 1.0 + sharpen/100.0, gaussian, -sharpen/100.0, 0)
    
    # 3. 转换颜色空间进行亮度/美白处理
    img_pil = Image.fromarray(cv2.cvtColor(img_smooth, cv2.COLOR_BGR2RGB))
    
    # 4. 美白 (提高亮度) & 亮度调节
    if white > 0 or bright != 0:
        enhancer = ImageEnhance.Brightness(img_pil)
        # 美白系数 + 整体亮度系数
        factor = 1.0 + (white / 200.0) + (bright / 100.0)
        img_pil = enhancer.enhance(factor)
    
    # 5. 气色红润 (提高饱和度)
    if saturate > 0:
        enhancer = ImageEnhance.Color(img_pil)
        img_pil = enhancer.enhance(1.0 + saturate / 100.0)
    
    return img_pil

# --- 主逻辑 ---
if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image.convert('RGB'))
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # 布局：分两栏
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🛠️ 参数调节")
        with st.expander("✨ 质感美颜 (Beauty)", expanded=True):
            val_smooth = st.slider("🧴 磨皮 (Dermabrasion)", 0, 100, 60)
            val_white = st.slider("💡 美白 (Whitening)", 0, 100, 30)
        
        with st.expander("🎨 色彩与光影 (Color)", expanded=True):
            val_saturate = st.slider("🌹 红润/饱和度", 0, 100, 20)
            val_bright = st.slider("☀️ 曝光补偿", -50, 50, 0)
            val_sharpen = st.slider("👁️ 清晰度/锐化", 0, 100, 30)
    
    # 实时处理
    result_img = apply_pro_beauty(img_cv, val_smooth, val_white, val_sharpen, val_saturate, val_bright)
    
    with col2:
        # 比较视图
        tab1, tab2 = st.tabs(["👀 效果预览", "🆚 原图对比"])
        with tab1:
            st.image(result_img, use_column_width=True)
        with tab2:
            c1, c2 = st.columns(2)
            c1.image(image, caption="原图", use_column_width=True)
            c2.image(result_img, caption="精修后", use_column_width=True)
    
    # 下载区
    st.markdown("---")
    buf = io.BytesIO()
    result_img.save(buf, format="PNG", quality=100)
    byte_im = buf.getvalue()
    
    btn_col1, btn_col2, _ = st.columns([1, 1, 3])
    with btn_col1:
        st.download_button(
            label="⬇️ 下载精修美照",
            data=byte_im,
            file_name="pro_beauty_result.png",
            mime="image/png",
            use_container_width=True
        )

else:
    st.info("👈 请在左侧上传照片，开始您的专业修图之旅！")