import streamlit as st
import random
import os

# 1. 页面配置
st.set_page_config(page_title="英语天天练", page_icon="🎨", layout="centered")

# 2. 界面美化 CSS
st.markdown("""
    <style>
    header, #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 1rem; max-width: 500px;}
    .stAudio {width: 100%;}
    div.stButton > button {
        width: 100%; border-radius: 15px; font-weight: bold; height: 3.5em;
    }
    .sentence-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 增强版数据库（加入金句）
course_data = {
    "1": {
        "pencil": {"chi": "铅笔", "sent": "I have a pencil."},
        "pen": {"chi": "钢笔", "sent": "This is a pen."},
        "book": {"chi": "书", "sent": "Open your book."},
        "bag": {"chi": "书包", "sent": "My bag is green."},
        "ruler": {"chi": "尺子", "sent": "Show me your ruler."},
        "eraser": {"chi": "橡皮", "sent": "I need an eraser."},
        "desk": {"chi": "书桌", "sent": "It is on the desk."},
        "chair": {"chi": "椅子", "sent": "Sit on the chair."}
    },
    "2": {
        "eye": {"chi": "眼睛", "sent": "Look into my eyes."},
        "ear": {"chi": "耳朵", "sent": "I hear with my ears."},
        "nose": {"chi": "鼻子", "sent": "Touch your nose."},
        "mouth": {"chi": "嘴巴", "sent": "Open your mouth."},
        "face": {"chi": "脸", "sent": "Wash your face."},
        "hand": {"chi": "手", "sent": "Clap your hands."},
        "arm": {"chi": "胳膊", "sent": "This is my arm."},
        "leg": {"chi": "腿", "sent": "My legs are long."}
    }
}

# 顶部导航
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌟 英语天天练</h1>", unsafe_allow_html=True)
day = st.selectbox("📅 选择学习进度：", list(course_data.keys()), index=0)
words_info = course_data[day]
words_list = list(words_info.keys())

tab1, tab2 = st.tabs(["📚 学习 & 跟读", "🎮 综合挑战"])

# --- 学习 & 跟读模式 ---
with tab1:
    for eng, info in words_info.items():
        img_path = f"assets/day{day}/{eng}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=280)
        
        st.markdown(f"<h2 style='text-align: center;'>{eng} <small style='color:gray;'>({info['chi']})</small></h2>", unsafe_allow_html=True)
        
        # 单词发音
        st.audio(f"https://dict.youdao.com/dictvoice?audio={eng}&type=2")
        
        # 每日金句
        st.markdown(f"""<div class='sentence-box'>
            <p style='margin-bottom:5px;'><b>📖 金句阅读：</b></p>
            <p style='font-size:1.2rem;'>{info['sent']}</p>
        </div>""", unsafe_allow_html=True)
        st.audio(f"https://dict.youdao.com/dictvoice?audio={info['sent'].replace(' ', '%20')}&type=2")
        
        # 跟读录音功能 (Streamlit 官方原生录音组件)
        st.write("🎤 听一听，自己试着读一遍：")
        st.audio_input(key=f"rec_{eng}")
        
        st.markdown("---")

# --- 综合挑战模式 ---
with tab2:
    # 初始化题目类型：0-听音选图，1-看图说词
    if 'quiz_type' not in st.session_state or st.sidebar.button("♻️ 换一题"):
        st.session_state.quiz_type = random.choice([0, 1])
        st.session_state.quiz_word = random.choice(words_list)
        st.session_state.quiz_options = random.sample(words_list, min(4, len(words_list)))
        if st.session_state.quiz_word not in st.session_state.quiz_options:
            st.session_state.quiz_options[0] = st.session_state.quiz_word
        random.shuffle(st.session_state.quiz_options)
        st.session_state.answered = False

    target = st.session_state.quiz_word
    
    # 题型 1：听音选图
    if st.session_state.quiz_type == 0:
        st.markdown("### 📢 题型：听音选图")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        cols = st.columns(2)
        for i, opt in enumerate(st.session_state.quiz_options):
            with cols[i % 2]:
                opt_img = f"assets/day{day}/{opt}.png"
                if os.path.exists(opt_img): st.image(opt_img, use_column_width=True)
                if st.button("选这个", key=f"btn_{opt}"):
                    if opt == target:
                        st.success("太棒了！答对了！")
                        st.balloons()
                        st.session_state.answered = True
                    else:
                        st.error("再听听看？")

    # 题型 2：看图说词
    else:
        st.markdown("### 🖼️ 题型：看图说词")
        st.write("这是什么？大声说出来！")
        img_path = f"assets/day{day}/{target}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=300)
        
        st.write("🎤 录下你的回答：")
        st.audio_input(key="quiz_rec")
        
        if st.button("显示答案"):
            st.info(f"正确答案是：{target} ({words_info[target]['chi']})")
            st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
            st.session_state.answered = True

    if st.session_state.get('answered'):
        if st.button("下一题 ➡️"):
            del st.session_state.quiz_type
            st.rerun()
