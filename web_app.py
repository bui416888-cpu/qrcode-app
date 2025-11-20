import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# 设置页面配置 - 必须是第一个 Streamlit 命令
st.set_page_config(
    page_title="Magic Studio - 马尊图像魔术师",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 以实现科技感/赛博朋克风格
st.markdown("""
    <style>
    /* 全局背景和字体 */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #00e5ff !important;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
        font-weight: 700;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #00BCD4);
        color: white;
        border: none;
        border-radius: 5px;
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.4);
        transition: all 0.3s ease;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 188, 212, 0.6);
    }
    
    /* 文件上传组件 */
    .stFileUploader {
        border: 1px dashed #00e5ff;
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(0, 229, 255, 0.05);
    }
    
    /* 图片容器 */
    .image-container {
        border: 2px solid #30363d;
        border-radius: 10px;
        padding: 10px;
        background-color: #0d1117;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

def sketch_filter(img_array):
    """素描大师滤镜"""
    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    invert_img = cv2.bitwise_not(gray_img)
    blur_img = cv2.GaussianBlur(invert_img, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blur_img)
    sketch_img = cv2.divide(gray_img, inverted_blur, scale=256.0)
    return cv2.cvtColor(sketch_img, cv2.COLOR_GRAY2RGB)

def cyberpunk_filter(img_array):
    """赛博朋克滤镜"""
    # 增强对比度 (CLAHE)
    lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    
    # 增加饱和度和色调偏移 (简单的赛博朋克模拟)
    hsv = cv2.cvtColor(enhanced_img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 50) # 增加饱和度
    v = cv2.add(v, 20) # 增加亮度
    final_hsv = cv2.merge((h, s, v))
    final_img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
    
    return final_img

def blur_filter(img_array, ksize):
    """模糊隐私滤镜"""
    # 确保核大小是奇数
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(img_array, (ksize, ksize), 0)

def main():
    st.title("🔮 Magic Studio | 马尊图像魔术师")
    st.markdown("---")

    # --- 侧边栏：控制台 ---
    with st.sidebar:
        st.header("🎛️ 控制台")
        
        # 功能 1: 图片上传
        uploaded_file = st.file_uploader("上传图片 (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
        
        filter_type = "原图"
        blur_amount = 0
        
        if uploaded_file is not None:
            st.success("图片上传成功！")
            
            # 功能 2: 选滤镜
            st.subheader("🎨 选择魔法滤镜")
            filter_type = st.radio(
                "滤镜效果",
                ("原图", "素描大师 (Sketch)", "赛博朋克 (Cyberpunk)", "模糊隐私 (Blur)")
            )
            
            if filter_type == "模糊隐私 (Blur)":
                blur_amount = st.slider("调节模糊程度", min_value=1, max_value=100, value=25, step=2)

    # --- 主界面：实时画布 ---
    if uploaded_file is not None:
        # 读取图片
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        # 处理图片
        processed_img_array = img_array.copy()
        
        if filter_type == "素描大师 (Sketch)":
            processed_img_array = sketch_filter(img_array)
        elif filter_type == "赛博朋克 (Cyberpunk)":
            processed_img_array = cyberpunk_filter(img_array)
        elif filter_type == "模糊隐私 (Blur)":
            processed_img_array = blur_filter(img_array, blur_amount)
            
        processed_image = Image.fromarray(processed_img_array)

        # 功能 3: 对比模式
        st.subheader("👁️ 实时预览")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**原始图像**")
            st.image(image, use_column_width=True, caption="Original")
            
        with col2:
            st.markdown(f"**魔法效果: {filter_type}**")
            st.image(processed_image, use_column_width=True, caption="Magic Result")

        # 功能 4: 一键下载
        st.markdown("---")
        buf = io.BytesIO()
        # 根据原图格式保存，默认 PNG
        format_to_save = image.format if image.format else 'PNG'
        processed_image.save(buf, format=format_to_save)
        byte_im = buf.getvalue()
        
        st.download_button(
            label="⬇️ 下载魔法图片",
            data=byte_im,
            file_name=f"magic_studio_{filter_type}.{format_to_save.lower()}",
            mime=f"image/{format_to_save.lower()}"
        )
        
    else:
        # 欢迎界面
        st.info("👈 请在左侧控制台上传图片开始魔法之旅")
        st.markdown("""
        ### ✨ 功能介绍
        - **素描大师**: 一键生成艺术素描
        - **赛博朋克**: 赋予照片未来科技感
        - **模糊隐私**: 智能保护敏感信息
        """)

if __name__ == "__main__":
    main()