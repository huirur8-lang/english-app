import streamlit as st
import random

# 配置
st.set_page_config(page_title="二年级英语每日练", page_icon="🎒")
st.title("🎒 二年级英语：30天挑战")

# 30天全主题单词数据库
course_data = {
    "1": {"pencil": "铅笔", "pen": "钢笔", "book": "书", "bag": "书包", "ruler": "尺子", "eraser": "橡皮", "desk": "书桌", "chair": "椅子"},
    "2": {"eye": "眼睛", "ear": "耳朵", "nose": "鼻子", "mouth": "嘴巴", "face": "脸", "hand": "手", "arm": "胳膊", "leg": "腿"},
    "3": {"red": "红色", "blue": "蓝色", "yellow": "黄色", "green": "绿色", "black": "黑色", "white": "白色", "orange": "橙色", "pink": "粉色"},
    "4": {"one": "一", "two": "二", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七", "eight": "八"},
    "5": {"nine": "九", "ten": "十", "big": "大的", "small": "小的", "long": "长的", "short": "短的", "tall": "高的", "fat": "胖的"},
    "6": {"father": "父亲", "mother": "母亲", "brother": "兄弟", "sister": "姐妹", "grandpa": "爷爷", "grandma": "奶奶", "baby": "婴儿", "family": "家庭"},
    "7": {"apple": "苹果", "banana": "香蕉", "pear": "梨", "orange": "橘子", "grape": "葡萄", "peach": "桃子", "melon": "瓜", "lemon": "柠檬"},
    "8": {"cat": "小猫", "dog": "小狗", "bird": "小鸟", "fish": "小鱼", "rabbit": "兔子", "duck": "鸭子", "pig": "小猪", "bear": "熊"},
    "9": {"monkey": "猴子", "tiger": "老虎", "lion": "狮子", "elephant": "大象", "panda": "熊猫", "snake": "蛇", "horse": "马", "cow": "母牛"},
    "10": {"egg": "鸡蛋", "milk": "牛奶", "bread": "面包", "cake": "蛋糕", "rice": "米饭", "water": "水", "juice": "果汁", "tea": "茶"},
    "11": {"sun": "太阳", "moon": "月亮", "star": "星星", "sky": "天空", "cloud": "云", "rain": "雨", "snow": "雪", "wind": "风"},
    "12": {"tree": "树", "flower": "花", "grass": "草", "leaf": "树叶", "park": "公园", "zoo": "动物园", "lake": "湖泊", "river": "河流"},
    "13": {"run": "跑", "jump": "跳", "walk": "走", "swim": "游泳", "dance": "跳舞", "sing": "唱歌", "fly": "飞", "climb": "爬"},
    "14": {"read": "读", "write": "写", "draw": "画", "play": "玩", "sleep": "睡", "eat": "吃", "drink": "喝", "sit": "坐"},
    "15": {"happy": "高兴的", "sad": "伤心的", "angry": "生气的", "tired": "累的", "hot": "热的", "cold": "冷的", "good": "好的", "bad": "坏的"},
    "16": {"head": "头", "hair": "头发", "shoulder": "肩膀", "knee": "膝盖", "toe": "脚趾", "finger": "手指", "foot": "脚", "body": "身体"},
    "17": {"bed": "床", "door": "门", "window": "窗户", "box": "盒子", "cup": "杯子", "key": "钥匙", "clock": "闹钟", "lamp": "台灯"},
    "18": {"shirt": "衬衫", "coat": "大衣", "dress": "连衣裙", "skirt": "短裙", "pants": "裤子", "shoe": "鞋子", "sock": "袜子", "hat": "帽子"},
    "19": {"plane": "飞机", "car": "小汽车", "bus": "公交车", "bike": "自行车", "boat": "小船", "train": "火车", "truck": "卡车", "ship": "轮船"},
    "20": {"teacher": "老师", "student": "学生", "doctor": "医生", "nurse": "护士", "worker": "工人", "driver": "司机", "cook": "厨师", "farmer": "农民"},
    "21": {"bread": "面包", "cookie": "曲奇", "candy": "糖果", "pizza": "比萨", "soup": "汤", "meat": "肉", "chicken": "鸡肉", "ice": "冰"},
    "22": {"morning": "早上", "afternoon": "下午", "evening": "晚上", "night": "夜里", "today": "今天", "now": "现在", "time": "时间", "year": "年"},
    "23": {"home": "家", "school": "学校", "room": "房间", "class": "班级", "shop": "商店", "farm": "农场", "street": "街道", "city": "城市"},
    "24": {"on": "在上面", "under": "在下面", "in": "在里面", "near": "在附近", "behind": "在后面", "left": "左边", "right": "右边", "here": "这里"},
    "25": {"spring": "春天", "summer": "夏天", "autumn": "秋天", "winter": "冬天", "warm": "温暖的", "cool": "凉爽的", "sunny": "晴朗的", "windy": "有风的"},
    "26": {"tomato": "西红柿", "potato": "土豆", "carrot": "胡萝卜", "onion": "洋葱", "corn": "玉米", "bean": "豆子", "fruit": "水果", "food": "食物"},
    "27": {"shirt": "衬衫", "jeans": "牛仔裤", "shorts": "短裤", "sweater": "毛衣", "jacket": "夹克", "scarf": "围巾", "gloves": "手套", "watch": "手表"},
    "28": {"ball": "球", "doll": "娃娃", "kite": "风筝", "balloon": "气球", "toy": "玩具", "game": "游戏", "robot": "机器人", "card": "卡片"},
    "29": {"Monday": "周一", "Tuesday": "周二", "Wednesday": "周三", "Thursday": "周四", "Friday": "周五", "Saturday": "周六", "Sunday": "周日", "week": "星期"},
    "30": {"hello": "你好", "thanks": "谢谢", "sorry": "对不起", "please": "请", "friend": "朋友", "name": "名字", "English": "英语", "China": "中国"}
}

# 侧边栏选择进度
day = st.sidebar.selectbox("📅 选择学习进度", list(course_data.keys()))
words = course_data[day]

# 界面主区
tab1, tab2 = st.tabs(["📚 学习模式", "✍️ 听写挑战"])

with tab1:
    st.info(f"今天学习第 {day} 天的内容。点击小喇叭跟读哦！")
    for eng, chi in words.items():
        col1, col2 = st.columns([4, 1])
        col1.write(f"### {eng} \n ({chi})")
        if col2.button(f"🔊", key=f"btn_{eng}"):
            # 兼容手机浏览器的网页朗读
            # 强化版发音脚本
            st.components.v1.html(f"""
                <script>
                window.speechSynthesis.cancel(); 
                var msg = new SpeechSynthesisUtterance('{eng}');
                msg.lang = 'en-US';
                msg.rate = 0.8; 
                window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

with tab2:
    st.warning("听写模式：拼写正确后会自动显示下一个。")
    # 初始化题目顺序
    if 'test_words' not in st.session_state or st.sidebar.button("🔀 重新打乱顺序"):
        items = list(words.items())
        random.shuffle(items)
        st.session_state.test_words = items

    score = 0
    for eng, chi in st.session_state.test_words:
        st.write(f"---")
        st.write(f"**请拼写：{chi}**")
        user_input = st.text_input(f"在这里输入 {chi} 的拼写", key=f"q_{eng}").strip().lower()
        
        if user_input == eng:
            st.success(f"太棒了！ {eng} ✅")
            score += 1
        elif user_input != "":
            st.error(f"记错了哦，正确拼写是: **{eng}**")

    if st.button("🏁 完成挑战，查看总分"):
        st.balloons()
        st.metric("今日得分", f"{score} / {len(words)}")
