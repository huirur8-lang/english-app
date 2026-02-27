import streamlit as st
import random
import os

# 1. 页面配置：设置网页标题和图标
st.set_page_config(page_title="英语天天练", page_icon="🎨", layout="centered")

# 2. 界面美化：用 CSS 样式隐藏 Streamlit 的默认横幅、页脚，并调整间距
st.markdown("""
    <style>
    /* 隐藏顶部横幅、菜单和页脚 */
    header, #MainMenu, footer {visibility: hidden;}
    /* 减少页面顶部的空白 */
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    /* 强制所有内容（图片、文字、音频）居中显示 */
    .stMarkdown, .stImage, .stAudio {text-align: center; display: flex; justify-content: center; align-items: center;}
    /* 让音频播放器铺满其所在容器的宽度 */
    audio {width: 100%;}
    </style>
    """, unsafe_allow_html=True)

# 3. 单词数据库 (你可以继续在这里添加新的日期和单词)
course_data = {
    "1": {"pencil": "铅笔", "pen": "钢笔", "book": "书", "bag": "书包", "ruler": "尺子", "eraser": "橡皮", "desk": "书桌", "chair": "椅子"},
    "2": {"eye": "眼睛", "ear": "耳朵", "nose": "鼻子", "mouth": "嘴巴", "face": "脸", "hand": "手", "arm": "胳膊", "leg": "腿"},
}

# 侧边栏：选择日期
st.sidebar.markdown("### 📅 学习进度")
day = st.sidebar.selectbox("选择今天学习哪一天：", list(course_data.keys()))
words = course_data[day]

# 界面主区：用 Tabs 区分学习和听写
tab1, tab2 = st.tabs(["📚 学习模式", "✍️ 听写挑战"])

# --- 学习模式 ---
with tab1:
    st.markdown(f"**今天学习第 {day} 天的内容。** \n\n看图片，大声念出单词，点击喇叭听发音哦！")
    st.markdown("---") # 分割线
    
    for eng, chi in words.items():
        # 为每个单词创建一个居中的容器
        with st.container():
            # 动态生成图片路径，例如 assets/day1/pencil.png
            img_path = f"assets/day{day}/{eng}.png"
            
            # 1. 显示图片
            if os.path.exists(img_path):
                # ★★★ 关键修改：把图片宽度改为 250，这样在手机上就够大了 ★★★
                # ★★★ use_column_width=True 可以让图片自适应，但为了精确控制大小，我们用 width ★★★
                st.image(img_path, width=250)
            else:
                # 如果图片不存在，显示一个占位图标，提醒你需要上传图片
                st.info(f"🖼️ 正在等待上传 {eng} 的图片...")
            
            # 2. 显示英文单词（加大字号）
            st.markdown(f"## **{eng}**")
            
            # 3. 显示中文含义
            st.markdown(f"({chi})")
            
            # 4. 显示音频播放器
            # 直接调用有道词典的真人发音接口
            audio_url = f"https://dict.youdao.com/dictvoice?audio={eng}&type=2"
            st.audio(audio_url)
            
            # 单词之间的分割线
            st.markdown("---")

# --- 听写挑战 ---
with tab2:
    st.markdown("**听写模式：在手机上打出你听到的单词拼写。**")
    
    # 初始化听写题目
    if 'test_words' not in st.session_state or st.sidebar.button("🔀 打乱顺序重新开始"):
        items = list(words.items())
        random.shuffle(items) # 打乱单词顺序
        st.session_state.test_words = items
        st.session_state.current_index = 0
        st.session_state.score = 0
    
    if st.session_state.current_index < len(st.session_state.test_words):
        eng, chi = st.session_state.test_words[st.session_state.current_index]
        
        st.write(f"### 请听写：**{chi}**")
        
        # 播放单词读音
        audio_url = f"https://dict.youdao.com/dictvoice?audio={eng}&type=2"
        st.audio(audio_url)
        
        # 使用表单以便按回车键提交
        with st.form(key=f"form_{eng}"):
            user_input = st.text_input("在这里输入拼写：", key=f"input_{eng}").strip().lower()
            submit_button = st.form_submit_button(label="提交拼写")
        
        # 处理用户提交的拼写
        if submit_button:
            if user_input == eng:
                st.success(f"太棒了！ {eng} 拼写正确！✅")
                st.session_state.score += 1
            else:
                st.error(f"记错了哦，正确拼写是: **{eng}**")
            
            # 自动跳转到下一个单词
            st.session_state.current_index += 1
            # 强制页面重新运行以更新内容
            st.experimental_rerun()
            
    else:
        # 完成所有听写后的评分页面
        st.balloons() # 庆祝气球
        st.metric("今日得分", f"{st.session_state.score} / {len(words)}")
        st.success("今日听写完成！你是最棒的！🌟")
