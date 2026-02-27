import streamlit as st
import random
import os

# 1. 页面基础配置
st.set_page_config(page_title="英语天天练", page_icon="🎨", layout="centered")

# 2. 界面美化 CSS (让手机端体验更像 APP)
st.markdown("""
    <style>
    /* 隐藏所有多余的菜单 */
    header, #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 1rem; max-width: 500px;}
    
    /* 所有的文字和图片强制居中 */
    .stMarkdown, .stImage, .stAudio {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    
    /* 让按钮更适合孩子点击 */
    div.stButton > button {
        width: 100%;
        border-radius: 20px;
        border: 2px solid #FF4B4B;
        background-color: white;
        color: #FF4B4B;
        font-weight: bold;
        height: 3em;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 30天全主题单词数据库 (保持不变)
course_data = {
    "1": {"pencil": "铅笔", "pen": "钢笔", "book": "书", "bag": "书包", "ruler": "尺子", "eraser": "橡皮", "desk": "书桌", "chair": "椅子"},
    "2": {"eye": "眼睛", "ear": "耳朵", "nose": "鼻子", "mouth": "嘴巴", "face": "脸", "hand": "手", "arm": "胳膊", "leg": "腿"},
    "3": {"red": "红色", "blue": "蓝色", "yellow": "黄色", "green": "绿色", "black": "黑色", "white": "白色", "orange": "橙色", "pink": "粉色"},
    # 后续天数代码保持原样...
}

# --- 4. 顶部进度选择 (从侧边栏移到主页面) ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌟 英语天天练</h1>", unsafe_allow_html=True)
day = st.selectbox("📅 请选择学习进度：", list(course_data.keys()), index=0)
words = course_data[day]

st.markdown("---")

# 5. 模式选择标签
tab1, tab2 = st.tabs(["📚 学习模式", "🎮 挑战模式"])

# --- 学习模式 ---
with tab1:
    st.markdown(f"<p style='text-align: center;'>今天我们要学习 <b>{len(words)}</b> 个新单词</p>", unsafe_allow_html=True)
    
    for eng, chi in words.items():
        with st.container():
            # 图片路径
            img_path = f"assets/day{day}/{eng}.png"
            
            # 显示大图
            if os.path.exists(img_path):
                st.image(img_path, width=280)
            else:
                st.info(f"正在准备 {eng} 的图片...")
            
            # 单词和翻译
            st.markdown(f"<h2 style='text-align: center; margin-bottom: 0;'>{eng}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: gray;'>({chi})</p>", unsafe_allow_html=True)
            
            # 音频
            audio_url = f"https://dict.youdao.com/dictvoice?audio={eng}&type=2"
            st.audio(audio_url)
            st.markdown("<br>", unsafe_allow_html=True)

# --- 挑战模式 (听音选图) ---
with tab2:
    # 如果换了天数，自动刷新题目
    if 'current_day' not in st.session_state or st.session_state.current_day != day:
        st.session_state.current_day = day
        if 'quiz_word' in st.session_state: del st.session_state.quiz_word

    if 'quiz_word' not in st.session_state:
        target = random.choice(list(words.keys()))
        options = random.sample(list(words.keys()), 4)
        if target not in options:
            options[0] = target
        random.shuffle(options)
        
        st.session_state.quiz_word = target
        st.session_state.quiz_options = options
        st.session_state.answered = False

    st.write("### 📢 听声音，选图片：")
    st.audio(f"https://dict.youdao.com/dictvoice?audio={st.session_state.quiz_word}&type=2")

    # 2x2 图片矩阵
    col1, col2 = st.columns(2)
    for i, opt in enumerate(st.session_state.quiz_options):
        with col1 if i % 2 == 0 else col2:
            opt_img = f"assets/day{day}/{opt}.png"
            if os.path.exists(opt_img):
                st.image(opt_img, use_column_width=True)
            if st.button(f"这是 {opt} 吗？", key=f"btn_{opt}"):
                if opt == st.session_state.quiz_word:
                    st.success("太棒了！🎉")
                    st.balloons()
                    st.session_state.answered = True
                else:
                    st.error("再试一次哦 ❌")

    if st.session_state.get('answered'):
        if st.button("下一题 ➡️"):
            del st.session_state.quiz_word
            st.rerun()
