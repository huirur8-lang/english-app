import streamlit as st
import random
import os

# 页面基础配置
st.set_page_config(page_title="英语天天练", page_icon="🎨")

# 隐藏多余组件的 CSS 样式
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

# 30天全主题单词数据库
course_data = {
    "1": {"pencil": "铅笔", "pen": "钢笔", "book": "书", "bag": "书包", "ruler": "尺子", "eraser": "橡皮", "desk": "书桌", "chair": "椅子"},
    "2": {"eye": "眼睛", "ear": "耳朵", "nose": "鼻子", "mouth": "嘴巴", "face": "脸", "hand": "手", "arm": "胳膊", "leg": "腿"},
}

# 侧边栏
day = st.sidebar.selectbox("📅 选择学习进度", list(course_data.keys()))
words = course_data[day]

tab1, tab2 = st.tabs(["📚 学习模式", "🎮 听音选图"])

# --- 1. 学习模式 ---
with tab1:
    st.info(f"第 {day} 天：点击喇叭跟读单词")
    for eng, chi in words.items():
        col_img, col_txt, col_audio = st.columns([1, 2, 1])
        
        # 自动寻找 assets/day1/ 文件夹下的图片
        img_path = f"assets/day{day}/{eng}.png"
        
        with col_img:
            if os.path.exists(img_path):
                st.image(img_path, width=80)
            else:
                st.write("🖼️") # 如果图片还没传，显示占位符
                
        with col_txt:
            st.subheader(eng)
            st.write(f"({chi})")
            
        with col_audio:
            audio_url = f"https://dict.youdao.com/dictvoice?audio={eng}&type=2"
            st.audio(audio_url)

# --- 2. 听音选图挑战 ---
with tab2:
    st.warning("听声音，选出正确的图片！")
    
    # 随机出一道题
    if 'target' not in st.session_state or st.sidebar.button("♻️ 换一题"):
        st.session_state.target = random.choice(list(words.keys()))
        # 随机选4个选项
        opts = random.sample(list(words.keys()), 4)
        if st.session_state.target not in opts:
            opts[0] = st.session_state.target
        random.shuffle(opts)
        st.session_state.options = opts

    target = st.session_state.target
    st.write("### 请听题：")
    st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")

    # 显示图片选项供孩子点击
    cols = st.columns(2) # 手机端建议分两列，图片大一点
    for i, opt in enumerate(st.session_state.options):
        with cols[i % 2]:
            opt_img = f"assets/day{day}/{opt}.png"
            if os.path.exists(opt_img):
                st.image(opt_img, use_column_width=True)
            if st.button(f"点这里选", key=f"btn_{opt}"):
                if opt == target:
                    st.success(f"太棒了！答对了！")
                    st.balloons()
                else:
                    st.error(f"再试一次哦！")
