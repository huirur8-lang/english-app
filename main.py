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
    # --- A. 动态构建复习池：包含当前天及之前所有天的单词 ---
    all_past_words = {}
    current_day_int = int(day)
    for d_key, d_words in course_data.items():
        if int(d_key) <= current_day_int:
            # 整合单词，并记录它属于哪一天（用于定位图片路径）
            for w, info in d_words.items():
                temp_info = info.copy()
                temp_info['belong_day'] = d_key
                all_past_words[w] = temp_info

    # --- B. 【修复 KeyError 报错】防崩溃逻辑 ---
    # 如果切换天数导致缓存里的单词不在现在的单词池中，就强制清除题目状态
    if 'quiz_target' in st.session_state:
        if st.session_state.quiz_target not in all_past_words:
            if 'quiz_mode' in st.session_state:
                del st.session_state.quiz_mode

    # --- C. 初始化挑战题目 ---
    if 'quiz_mode' not in st.session_state or st.sidebar.button("♻️ 换一组题"):
        st.session_state.quiz_mode = random.choice(["listen", "speak"])
        # 从汇总后的“滚雪球”单词池里随机选一个
        st.session_state.quiz_target = random.choice(list(all_past_words.keys()))
        
        # 确保选项数量不超过单词池总数
        pool_size = min(len(all_past_words), 4)
        opts = random.sample(list(all_past_words.keys()), pool_size)
        if st.session_state.quiz_target not in opts:
            opts[0] = st.session_state.quiz_target
        random.shuffle(opts)
        
        st.session_state.quiz_options = opts
        st.session_state.quiz_answered = False

    # 获取当前题目信息
    target = st.session_state.quiz_target
    target_info = all_past_words[target]
    target_day = target_info['belong_day']

    # --- D. 听音选图模式 ---
    if st.session_state.quiz_mode == "listen":
        st.write(f"### 👂 听声音，选图片 (来自第 {target_day} 课)")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        
        col1, col2 = st.columns(2)
        for i, opt in enumerate(st.session_state.quiz_options):
            with col1 if i % 2 == 0 else col2:
                # 核心优化：根据单词原本所属的文件夹查找图片
                opt_day = all_past_words[opt]['belong_day']
                
                # 自动尝试多种图片后缀，解决截图里显示“缺少图片”的问题
                found_opt_img = None
                for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
                    test_path = f"assets/day{opt_day}/{opt}{ext}"
                    if os.path.exists(test_path):
                        found_opt_img = test_path
                        break

                if found_opt_img:
                    st.image(found_opt_img, use_container_width=True)
                else:
                    st.warning(f"📸 缺少图片: {opt}")
                
                if st.button(f"选这个", key=f"sel_{opt}"):
                    if opt == target:
                        st.success("灿灿真棒！答对了！🎉")
                        st.balloons()
                        st.session_state.quiz_answered = True
                    else:
                        st.error("再听一遍试试看？")

    # --- E. 看图说词模式 ---
    else:
        st.write(f"### 🖼️ 看图说词 (来自第 {target_day} 课)")
        st.write("灿灿，大声说出这是什么？")
        
        # 同样进行后缀自动匹配
        found_target_img = None
        for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
            test_path = f"assets/day{target_day}/{target}{ext}"
            if os.path.exists(test_path):
                found_target_img = test_path
                break
            
        if found_target_img:
            st.image(found_target_img, width=300)
        else:
            st.warning(f"📸 缺少图片: {target}")
            
        if st.button("检查答案"):
            st.session_state.quiz_answered = True
            
    # --- F. 答题反馈区 ---
    if st.session_state.get('quiz_answered'):
        st.info(f"答案是：{target} ({target_info['chi']})")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        if st.button("挑战下一题 ➡️"):
            if 'quiz_mode' in st.session_state:
                del st.session_state.quiz_mode
            st.rerun()
