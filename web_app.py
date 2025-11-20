import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

# --- 隐藏默认菜单的 CSS ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 标题与布局 ---
st.title("🎨 Magic Studio | 马尊图像魔术师")
st.markdown("---")

# --- 侧边栏：控制台 ---
st.sidebar.header("🎛️ 控制台")

# 1. 图片上传
uploaded_file = st.sidebar.file_uploader("上传图片 (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

# 2. 滤镜选择
filter_type = st.sidebar.radio(
    "✨ 选择魔法滤镜",
    ("🔴 原图", "📝 素描大师 (Sketch)", "🤖 赛博朋克 (Cyberpunk)", "🕶️ 模糊隐私 (Blur)", "✨ 智能美颜 (Pro Beauty)")
)

# --- 核心处理逻辑 ---
def process_image(image_input, filter_mode):
    # 将 PIL 图片转换为 OpenCV 格式 (RGB -> BGR)
    img_array = np.array(image_input.convert('RGB'))
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    if filter_mode == "🔴 原图":
        return img_cv

    elif filter_mode == "📝 素描大师 (Sketch)":
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        inv_gray = 255 - gray
        blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    elif filter_mode == "🤖 赛博朋克 (Cyberpunk)":
        # 增加对比度并检测边缘
        contrast = cv2.convertScaleAbs(img_cv, alpha=1.5, beta=10)
        edges = cv2.Canny(contrast, 100, 200)
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        # 将边缘叠加成霓虹色
        edges_color[:, :, 1] = 0 # 去掉绿色，变成紫红色调
        final = cv2.addWeighted(contrast, 0.8, edges_color, 0.4, 0)
        return final

    elif filter_mode == "🕶️ 模糊隐私 (Blur)":
        # 获取滑块参数
        blur_amount = st.sidebar.slider("调节模糊程度", 1, 100, 25)
        # 确保是奇数
        k_size = blur_amount if blur_amount % 2 == 1 else blur_amount + 1
        return cv2.GaussianBlur(img_cv, (k_size, k_size), 0)

    elif filter_mode == "✨ 智能美颜 (Pro Beauty)":
        # 获取美颜参数
        smooth_level = st.sidebar.slider("🧴 磨皮程度", 0, 50, 15)
        white_level = st.sidebar.slider("💡 美白程度", 0, 50, 10)
        
        # 1. 双边滤波磨皮 (保边去噪)
        # d: 邻域直径, sigmaColor: 颜色空间标准差, sigmaSpace: 坐标空间标准差
        img_smooth = cv2.bilateralFilter(img_cv, d=9, sigmaColor=smooth_level*2+10, sigmaSpace=75)
        
        # 2. 美白 (调整亮度/对比度)
        # alpha: 对比度 (1.0-3.0), beta: 亮度 (0-100)
        img_beauty = cv2.convertScaleAbs(img_smooth, alpha=1.0 + white_level/200.0, beta=white_level)
        
        return img_beauty

    return img_cv

# --- 主界面显示 ---
if uploaded_file is not None:
    # 打开图片
    image = Image.open(uploaded_file)
    
    # 处理图片
    result_cv = process_image(image, filter_type)
    
    # 将 OpenCV 格式转回 PIL 格式用于显示
    result_pil = Image.fromarray(cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB))

    # 分列显示：左边原图，右边效果图
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原始图像")
        st.image(image, use_column_width=True)
    with col2:
        st.subheader(f"魔法效果: {filter_type}")
        st.image(result_pil, use_column_width=True)

    # 下载按钮
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="⬇️ 下载魔法图片",
        data=byte_im,
        file_name="magic_result.png",
        mime="image/png"
    )

else:
    st.info("👈 请在左侧上传一张照片开始体验魔法！")