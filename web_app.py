import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageDraw
import io
from rembg import remove

# --- 页面配置 ---
st.set_page_config(page_title="马尊影像工坊 Pro", page_icon="🎨", layout="wide")

# --- 高级 CSS 样式 (获奖级别设计) ---
premium_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* 全局样式 */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

/* 主容器 */
.main .block-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 2rem 3rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    margin-top: 2rem;
}

/* 隐藏默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 侧边栏样式 */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    border-right: none;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* 侧边栏标题 */
section[data-testid="stSidebar"] h1 {
    color: #fff;
    font-size: 1.5rem;
    font-weight: 700;
    text-align: center;
    padding: 1rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

section[data-testid="stSidebar"] h3 {
    color: #a0aec0;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1.5rem 0 0.5rem 0;
    padding-left: 0.5rem;
}

/* Radio 按钮样式 */
section[data-testid="stSidebar"] .stRadio > label {
    color: #cbd5e0;
    font-weight: 500;
}

section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.5rem;
}

section[data-testid="stSidebar"] .stRadio > div > label {
    background: rgba(255, 255, 255, 0.05);
    padding: 0.75rem 1rem;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    color: #e2e8f0;
}

section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateX(4px);
}

section[data-testid="stSidebar"] .stRadio > div > label[data-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
    color: white;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* 标题样式 */
h1 {
    color: #1a202c;
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    transition: all 0.3s ease;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(72, 187, 120, 0.6);
}

/* 滑块样式 */
.stSlider > div > div > div > div {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 文件上传器 */
.stFileUploader {
    border: 2px dashed #667eea;
    border-radius: 16px;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: #764ba2;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

/* 图片样式 */
img {
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* 输入框样式 */
.stTextInput > div > div > input {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 信息框 */
.stInfo {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-left: 4px solid #667eea;
    border-radius: 12px;
    padding: 1rem 1.5rem;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #667eea !important;
}

/* 选择框样式 */
.stSelectbox > div > div {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
}

.stSelectbox > div > div:hover {
    border-color: #667eea;
}

/* Radio 样式优化 */
.stRadio > div {
    gap: 0.75rem;
}

.stRadio > div > label {
    background: white;
    padding: 0.75rem 1.25rem;
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.stRadio > div > label:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.05);
}

.stRadio > div > label[data-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
    color: white;
    font-weight: 600;
}

/* Tab 样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    border: 2px solid #e2e8f0;
    font-weight: 600;
    color: #4a5568;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
    color: white;
}

/* 对比容器 */
.comparison-container {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}

.comparison-item {
    flex: 1;
    background: white;
    border-radius: 16px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.comparison-label {
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.5rem;
    font-size: 1rem;
}
</style>
"""
st.markdown(premium_css, unsafe_allow_html=True)

# --- 侧边栏导航 ---
st.sidebar.title("🎨 马尊影像工坊")
st.sidebar.markdown("### 🎯 功能导航")
app_mode = st.sidebar.radio("", [
    "✨ 智能美颜 (Beauty)",
    "🪄 AI 智能抠图 (Remove BG)",
    "🆔 证件照换底 (ID Photo)",
    "🎨 艺术滤镜 (Filters)",
    "📉 格式/压缩 (Converter)",
    "💧 水印管家 (Watermark)"
], label_visibility="collapsed")

# --- 公共函数 ---
def convert_image(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- 模块 1: 智能美颜 (升级版 - 带前后对比) ---
def app_beauty():
    st.title("✨ 专业级智能美颜")
    st.markdown("使用先进的双边滤波算法，打造自然真实的美颜效果")
    
    uploaded_file = st.file_uploader("📂 上传您的照片", type=['jpg', 'png', 'jpeg'], help="支持 JPG、PNG、JPEG 格式")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        img_cv = cv2.cvtColor(np.array(image.convert('RGB')), cv2.COLOR_RGB2BGR)
        
        st.markdown("---")
        st.subheader("🎛️ 美颜参数调节")
        
        c1, c2 = st.columns(2)
        with c1:
            smooth = st.slider("🧴 磨皮强度", 0, 100, 50, help="保留面部细节的同时平滑肌肤")
            white = st.slider("💡 美白提亮", 0, 100, 30, help="自然提升肤色亮度")
        with c2:
            sharpen = st.slider("👁️ 清晰锐化", 0, 100, 20, help="增强眼睛等关键部位的清晰度")
            saturate = st.slider("🌹 红润饱和", 0, 100, 20, help="增加气色，让肤色更健康")
        
        # 处理图片
        d = 5 + int(smooth/5)
        img_smooth = cv2.bilateralFilter(img_cv, d, smooth*2, 75)
        img_pil = Image.fromarray(cv2.cvtColor(img_smooth, cv2.COLOR_BGR2RGB))
        
        # 美白与调色
        if white > 0: 
            img_pil = ImageEnhance.Brightness(img_pil).enhance(1.0 + white/200.0)
        if saturate > 0: 
            img_pil = ImageEnhance.Color(img_pil).enhance(1.0 + saturate/100.0)
        
        # 前后对比展示
        st.markdown("---")
        st.subheader("👁️ 效果预览")
        
        tab1, tab2, tab3 = st.tabs(["🆚 前后对比", "📸 美颜后", "📷 原图"])
        
        with tab1:
            st.markdown("##### 拖动查看前后变化")
            col_before, col_after = st.columns(2)
            with col_before:
                st.markdown("**原图**")
                st.image(image, use_column_width=True)
            with col_after:
                st.markdown("**美颜后**")
                st.image(img_pil, use_column_width=True)
        
        with tab2:
            st.image(img_pil, caption="✨ 专业美颜效果", use_column_width=True)
        
        with tab3:
            st.image(image, caption="📷 原始照片", use_column_width=True)
        
        # 下载按钮
        st.markdown("---")
        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])
        with col_dl1:
            st.download_button(
                "⬇️ 下载美颜照片",
                convert_image(img_pil),
                "beauty_pro.png",
                "image/png",
                use_container_width=True
            )

# --- 模块 2: AI 抠图 ---
def app_remove_bg():
    st.title("🪄 AI 智能抠图")
    st.markdown("基于深度学习的智能主体识别，一键移除背景")
    
    uploaded_file = st.file_uploader("📂 上传图片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**原始图片**")
            st.image(image, use_column_width=True)
        
        if st.button("🚀 开始智能抠图", use_container_width=True):
            with st.spinner("🤖 AI 正在识别主体并移除背景..."):
                result = remove(image)
                with col2:
                    st.markdown("**抠图结果**")
                    st.image(result, use_column_width=True)
                
                st.success("✅ 抠图完成！")
                st.download_button(
                    "⬇️ 下载透明背景图",
                    convert_image(result),
                    "removed_bg.png",
                    "image/png",
                    use_container_width=True
                )

# --- 模块 3: 证件照换底 ---
def app_id_photo():
    st.title("🆔 证件照智能换底")
    st.markdown("AI 抠图 + 纯色背景，快速生成标准证件照")
    
    uploaded_file = st.file_uploader("📂 上传人像照片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="原始照片", use_column_width=True)
        
        color = st.radio("选择证件照底色", ["⚪ 白色", "🔴 红色", "🔵 蓝色"], horizontal=True)
        
        if st.button("🎨 生成证件照", use_container_width=True):
            with st.spinner("🤖 正在处理中..."):
                fg = remove(image)
                bg_color = (255, 255, 255) if "白" in color else (255, 0, 0) if "红" in color else (67, 142, 219)
                new_img = Image.new("RGB", fg.size, bg_color)
                new_img.paste(fg, (0, 0), fg)
                
                with col2:
                    st.image(new_img, caption=f"{color}底证件照", use_column_width=True)
                
                st.success("✅ 证件照生成完成！")
                st.download_button(
                    "⬇️ 下载证件照",
                    convert_image(new_img),
                    "id_photo.png",
                    "image/png",
                    use_container_width=True
                )

# --- 模块 4: 艺术滤镜 ---
def app_filters():
    st.title("🎨 创意艺术滤镜")
    st.markdown("专业级图像处理算法，打造独特艺术效果")
    
    uploaded_file = st.file_uploader("📂 上传图片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        option = st.selectbox("选择艺术滤镜", ["📝 素描风格", "🎞️ 经典黑白", "🌆 复古怀旧"])
        
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
            res = img_cv
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**原图**")
            st.image(image, use_column_width=True)
        with col2:
            st.markdown("**滤镜效果**")
            st.image(res, use_column_width=True)
        
        st.download_button(
            "⬇️ 下载艺术作品",
            convert_image(Image.fromarray(res)),
            "artistic_filter.png",
            "image/png",
            use_container_width=True
        )

# --- 模块 5: 格式转换 ---
def app_converter():
    st.title("📉 智能格式转换")
    st.markdown("支持多种格式互转，智能压缩优化")
    
    uploaded_file = st.file_uploader("📂 上传图片", type=['jpg', 'png', 'webp'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("原始尺寸", f"{image.size[0]} × {image.size[1]} px")
            st.image(image, use_column_width=True)
        
        to_format = st.selectbox("目标格式", ["PNG", "JPEG", "PDF"])
        
        if to_format == "JPEG":
            quality = st.slider("压缩质量", 10, 100, 85, help="质量越高，文件越大")
        
        if st.button("🔄 开始转换", use_container_width=True):
            buf = io.BytesIO()
            if to_format == "JPEG":
                image.convert('RGB').save(buf, format="JPEG", quality=quality)
            elif to_format == "PDF":
                image.convert('RGB').save(buf, format="PDF")
            else:
                image.save(buf, format="PNG")
            
            st.success(f"✅ 已转换为 {to_format} 格式！")
            st.download_button(
                f"⬇️ 下载 {to_format} 文件",
                buf.getvalue(),
                f"converted.{to_format.lower()}",
                use_container_width=True
            )

# --- 模块 6: 水印管家 ---
def app_watermark():
    st.title("💧 智能水印管家")
    st.markdown("为您的作品添加专属标识，保护版权")
    
    uploaded_file = st.file_uploader("📂 上传图片", type=['jpg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        if image.mode != 'RGBA':
            image = image.convert('RGB').convert('RGBA')
        
        col1, col2 = st.columns(2)
        with col1:
            text = st.text_input("水印文字", "© 马尊出品")
            opacity = st.slider("透明度", 0, 255, 128)
        with col2:
            font_size = st.slider("字体大小", 10, 100, 40)
        
        if st.button("💧 添加水印", use_container_width=True):
            txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            w, h = image.size
            position = (w - len(text) * font_size - 20, h - font_size - 20)
            draw.text(position, text, fill=(255, 255, 255, opacity))
            
            out = Image.alpha_composite(image, txt_layer)
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.markdown("**原图**")
                st.image(image, use_column_width=True)
            with col_res2:
                st.markdown("**添加水印后**")
                st.image(out, use_column_width=True)
            
            st.success("✅ 水印添加成功！")
            st.download_button(
                "⬇️ 下载带水印图片",
                convert_image(out),
                "watermarked.png",
                "image/png",
                use_container_width=True
            )

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
elif app_mode == "💧 水印管家 (Watermark)":
    app_watermark()