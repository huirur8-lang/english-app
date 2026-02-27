import streamlit as st
import random
import os

# 1. 页面基础配置
st.set_page_config(page_title="英语天天练", page_icon="🎨", layout="centered")

# 2. 界面美化 CSS (进一步优化按钮样式)
st.markdown("""
    <style>
    header, #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 1rem; max-width: 500px;}
    
    .stMarkdown, .stImage, .stAudio {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    
    /* 挑战模式的大按钮样式 */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3em;
        font-size: 1.1rem;
        border: 2px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 单词数据库 (这里仅展示前几天，你可以继续保留你原来的完整库)
course_data = {
    "1": {"pencil": "铅笔", "pen": "钢笔", "book": "书", "bag": "书包", "ruler": "尺子", "eraser": "橡皮", "desk": "书桌", "chair": "椅子"},
    "2": {"eye": "眼睛", "ear": "耳朵", "nose": "鼻子", "mouth": "嘴巴", "face": "脸", "hand": "手", "arm": "胳膊", "leg": "腿"},
}

# --- 4. 进度选择 ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌟 英语天天练</h1>", unsafe_allow_html=True)
day = st.selectbox("📅 选择今天学习哪一天：", list(course_data.keys()), index=0)
words = course_data[day]

st.markdown("---")

tab1, tab2 = st.tabs(["📚 学习模式", "🎮 挑战模式"])

# --- 5. 学习模式 ---
with tab1:
    for eng, chi in words.items():
        img_path = f"assets/day{day}/{eng}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=280)
        
        st.markdown(f"<h2 style='text-align: center;'>{eng}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>({chi})</p>", unsafe_allow_html=True)
        
        audio_url = f"https://dict.youdao.com/dictvoice?audio={eng}&type=2"
        st.audio(audio_url)
        st.markdown("<br>", unsafe_allow_html=True)

# --- 6. 挑战模式 (优化版：听音选图) ---
with tab2:
    # 逻辑初始化
    if 'quiz_word' not in st.session_state or st.session_state.get('last_day') != day:
        st.session_state.last_day = day
        target = random.choice(list(words.keys()))
        options = random.sample(list(words.keys()), 4)
        if target not in options: options[0] = target
        random.shuffle(options)
        
        st.session_state.quiz_word = target
        st.session_state.quiz_options = options
        st.session_state.answered = False

    st.markdown("<h3 style='text-align: center;'>👂 听听这是哪个？</h3>", unsafe_allow_html=True)
    st.audio(f"https://dict.youdao.com/dictvoice?audio={st.session_state.quiz_word}&type=2")

    # 布局：2x2 图片墙
    col1, col2 = st.columns(2)
    for i, opt in enumerate(st.session_state.quiz_options):
        with col1 if i % 2 == 0 else col2:
            opt_img = f"assets/day{day}/{opt}.png"
            if os.path.exists(opt_img):
                st.image(opt_img, use_column_width=True)
            
            # 按钮只显示序号或简单的“选我”
            if st.button(f"选择图片 {i+1}", key=f"btn_{opt}"):
                if opt == st.session_state.quiz_word:
                    st.success("✨ 答对了！太棒了！")
                    st.balloons()
                    st.session_state.answered = True
                else:
                    st.error("❌ 不对哦，再听听看")

    if st.session_state.get('answered'):
        st.markdown("---")
        if st.button("🌟 下一题 ➡️"):
            del st.session_state.quiz_word
            st.rerun()
