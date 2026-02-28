import streamlit as st
import random
import os
import urllib.parse

# 1. 页面基础配置
st.set_page_config(page_title="灿灿学英语", page_icon="⭐", layout="centered")

# 2. 界面美化 CSS
st.markdown("""
    <style>
    header, #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 1.5rem; max-width: 500px;}
    .stAudio {width: 100%;}
    .main-title {text-align: center; color: #FF4B4B; font-size: 2.2rem; margin-bottom: 5px;}
    .slogan {text-align: center; color: #666; font-size: 1rem; margin-bottom: 20px;}
    .word-title {text-align: center; color: #1E1E1E; margin-top: 10px;}
    .sent-box {background-color: #FFF4F4; padding: 15px; border-radius: 15px; border: 1px solid #FFCACA; margin: 10px 0;}
    div.stButton > button {width: 100%; border-radius: 15px; font-weight: bold; height: 3.5em; background-color: #f0f2f6;}
    </style>
    """, unsafe_allow_html=True)

# 3. 单词数据库 (保持不变)
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
    },
    "3": {
        "red": {"chi": "红色", "sent": "The apple is red."},
        "blue": {"chi": "蓝色", "sent": "The sky is blue."},
        "yellow": {"chi": "黄色", "sent": "The sun is yellow."},
        "green": {"chi": "绿色", "sent": "I see green grass."},
        "black": {"chi": "黑色", "sent": "The cat is black."},
        "white": {"chi": "白色", "sent": "I like white clouds."},
        "orange": {"chi": "橙色", "sent": "I like the orange."},
        "pink": {"chi": "粉色", "sent": "It is a pink heart."}
    }
}

# 辅助函数：获取图片路径（处理大小写和后缀）
def get_img_path(day, word):
    base_path = f"assets/day{day}/{word}"
    for ext in [".png", ".jpg", ".PNG", ".JPG"]:
        if os.path.exists(base_path + ext):
            return base_path + ext
    return None

# 4. 头部
st.markdown("<h1 class='main-title'>🌟 灿灿学英语</h1>", unsafe_allow_html=True)
st.markdown("<p class='slogan'>每一天的进步，都是灿灿闪闪发光的小勋章！✨</p>", unsafe_allow_html=True)

day = st.selectbox("📅 选择今天的学习进度：", list(course_data.keys()), index=len(list(course_data.keys()))-1)
words_info = course_data[day]

tab1, tab2 = st.tabs(["📚 学习跟读", "🎮 挑战挑战"])

# 5. 学习模式
with tab1:
    for eng, info in words_info.items():
        img = get_img_path(day, eng)
        if img:
            st.image(img, width=280)
        
        st.markdown(f"<h2 class='word-title'>{eng} <small>({info['chi']})</small></h2>", unsafe_allow_html=True)
        st.audio(f"https://dict.youdao.com/dictvoice?audio={eng}&type=2")
        
        st.markdown(f"<div class='sent-box'><p style='color:#FF4B4B; font-weight:bold;'>📖 句子跟读：</p><p style='font-size:1.2rem;'>{info['sent']}</p></div>", unsafe_allow_html=True)
        # 修复音频编码问题
        encoded_sent = urllib.parse.quote(info['sent'])
        st.audio(f"https://dict.youdao.com/dictvoice?audio={encoded_sent}&type=2")
        st.markdown("---")

# 6. 综合挑战模式
with tab2:
    if 'quiz_mode' not in st.session_state or st.sidebar.button("♻️ 换一组题"):
        st.session_state.quiz_mode = random.choice(["listen", "speak"])
        st.session_state.quiz_target = random.choice(list(words_info.keys()))
        opts = random.sample(list(words_info.keys()), 4)
        if st.session_state.quiz_target not in opts: opts[0] = st.session_state.quiz_target
        random.shuffle(opts)
        st.session_state.quiz_options = opts
        st.session_state.quiz_answered = False

    target = st.session_state.quiz_target

    if st.session_state.quiz_mode == "listen":
        st.write("### 👂 听声音，选图片")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        col1, col2 = st.columns(2)
        for i, opt in enumerate(st.session_state.quiz_options):
            with col1 if i % 2 == 0 else col2:
                o_img = get_img_path(day, opt)
                if o_img:
                    st.image(o_img, use_container_width=True)
                else:
                    st.button(f"🖼️ 缺少图片: {opt}", disabled=True)
                
                if st.button(f"选这个", key=f"sel_{opt}"):
                    if opt == target:
                        st.success("灿灿真棒！答对了！🎉")
                        st.balloons()
                        st.session_state.quiz_answered = True
                    else:
                        st.error("再听一遍试试看？")
    else:
        st.write("### 🖼️ 看图说词")
        t_img = get_img_path(day, target)
        if t_img:
            st.image(t_img, width=300)
        if st.button("检查答案"):
            st.session_state.quiz_answered = True
            
    if st.session_state.get('quiz_answered'):
        st.info(f"答案是：{target} ({words_info[target]['chi']})")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        if st.button("挑战下一题 ➡️"):
            del st.session_state.quiz_mode
            st.rerun()
