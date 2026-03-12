import streamlit as st
import random
import os
import requests # 仅用于有道语音接口
import urllib.parse

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(
    page_title="灿灿学英语",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed" # 默认收起侧边栏，聚焦内容
)

# ==========================================
# 2. 界面美化 CSS
# ==========================================
st.markdown("""
    <style>
    /* 隐藏顶部导航和底部水印 */
    header, #MainMenu, footer {visibility: hidden;}
    /* 限制内容最大宽度，更像手机 APP */
    .block-container {padding-top: 1.5rem; max-width: 500px;}
    
    /* 音频播放器样式 */
    .stAudio {width: 100%; margin-bottom: 15px;}
    
    /* 标题和口号样式 */
    .main-title {text-align: center; color: #FF4B4B; font-size: 2.2rem; margin-bottom: 5px; font-weight: 800;}
    .slogan {text-align: center; color: #666; font-size: 1rem; margin-bottom: 10px;}
    
    /* 单词标题样式 */
    .word-title {text-align: center; color: #1E1E1E; margin-top: 10px; font-size: 2.5rem; font-weight: 800;}
    
    /* 句子跟读框样式 */
    .sent-box {
        background-color: #FFF4F4;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #FFCACA;
        margin: 15px 0;
        box-shadow: 2px 2px 10px rgba(255,75,75,0.05);
    }
    
    /* 全局按钮样式美化 */
    div.stButton > button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        height: 3.8em;
        background-color: #f0f2f6;
        border: 2px solid #d1d5db;
        transition: all 0.3s;
        font-size: 1.1rem;
    }
    div.stButton > button:hover {
        background-color: #FF4B4B;
        color: white;
        border-color: #FF4B4B;
        transform: scale(1.02);
    }

    /* 统计勋章区域样式 */
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 核心配置与【完整】单词数据库
# ==========================================

# 占位图地址 (当本地找不到图时显示)
PLACEHOLDER_IMG = "https://via.placeholder.com/500x350?text=Learning+English+Together"

# 完整的 30 天单词库
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
    },
    "4": {
        "cat": {"chi": "猫", "sent": "The cat is sleeping."},
        "dog": {"chi": "狗", "sent": "I like my dog."},
        "duck": {"chi": "鸭子", "sent": "The duck can swim."},
        "pig": {"chi": "猪", "sent": "The pig is fat."},
        "cow": {"chi": "奶牛", "sent": "The cow gives milk."},
        "horse": {"chi": "马", "sent": "He can ride a horse."},
        "sheep": {"chi": "绵羊", "sent": "I see a white sheep."},
        "rabbit": {"chi": "兔子", "sent": "The rabbit has long ears."}
    },
    "5": {
        "lion": {"chi": "狮子", "sent": "The lion is the king."},
        "tiger": {"chi": "老虎", "sent": "The tiger is very strong."},
        "panda": {"chi": "熊猫", "sent": "I love the cute panda."},
        "monkey": {"chi": "猴子", "sent": "The monkey likes bananas."},
        "elephant": {"chi": "大象", "sent": "The elephant has a long nose."},
        "bear": {"chi": "熊", "sent": "The brown bear is big."},
        "snake": {"chi": "蛇", "sent": "The snake is very long."},
        "bird": {"chi": "鸟", "sent": "The bird can fly high."}
    },
    "6": {
        "apple": {"chi": "苹果", "sent": "An apple a day."},
        "banana": {"chi": "香蕉", "sent": "I want a yellow banana."},
        "pear": {"chi": "梨", "sent": "The pear is sweet."},
        "grape": {"chi": "葡萄", "sent": "I like purple grapes."},
        "melon": {"chi": "瓜", "sent": "This melon is very big."},
        "strawberry": {"chi": "草莓", "sent": "Strawberry is my favorite."},
        "peach": {"chi": "桃子", "sent": "The peach is soft."},
        "lemon": {"chi": "柠檬", "sent": "The lemon is sour."}
    },
    "7": {
        "milk": {"chi": "牛奶", "sent": "Drink your milk."},
        "egg": {"chi": "鸡蛋", "sent": "I eat an egg every day."},
        "bread": {"chi": "面包", "sent": "The bread is fresh."},
        "rice": {"chi": "米饭", "sent": "I want some white rice."},
        "cake": {"chi": "蛋糕", "sent": "Happy birthday cake!"},
        "juice": {"chi": "果汁", "sent": "I like orange juice."},
        "water": {"chi": "水", "sent": "Can I have some water?"},
        "ice cream": {"chi": "冰淇淋", "sent": "I like cold ice cream."}
    },
    "8": {
        "tomato": {"chi": "西红柿", "sent": "Tomato is red."},
        "potato": {"chi": "土豆", "sent": "I like potato chips."},
        "carrot": {"chi": "胡萝卜", "sent": "Rabbit likes carrot."},
        "onion": {"chi": "洋葱", "sent": "Onion makes me cry."},
        "corn": {"chi": "玉米", "sent": "The corn is yellow."},
        "bean": {"chi": "豆子", "sent": "Green bean is good."},
        "cabbage": {"chi": "卷心菜", "sent": "Eat your cabbage."},
        "pumpkin": {"chi": "南瓜", "sent": "The pumpkin is orange."}
    },
    "9": {
        "one": {"chi": "一", "sent": "I have one nose."},
        "two": {"chi": "二", "sent": "I have two eyes."},
        "three": {"chi": "三", "sent": "Three little pigs."},
        "four": {"chi": "四", "sent": "A car has four wheels."},
        "five": {"chi": "五", "sent": "I have five fingers."},
        "six": {"chi": "六", "sent": "There are six apples."},
        "seven": {"chi": "七", "sent": "Seven days a week."},
        "eight": {"chi": "八", "sent": "An octopus has eight legs."}
    },
    "10": {
        "nine": {"chi": "九", "sent": "I see nine birds."},
        "ten": {"chi": "十", "sent": "Ten little Indians."},
        "eleven": {"chi": "十一", "sent": "Eleven comes after ten."},
        "twelve": {"chi": "十二", "sent": "A clock has twelve numbers."},
        "thirteen": {"chi": "十三", "sent": "I am thirteen today."},
        "fourteen": {"chi": "十四", "sent": "Fourteen red roses."},
        "fifteen": {"chi": "十五", "sent": "Fifteen minutes left."},
        "sixteen": {"chi": "十六", "sent": "She is sixteen years old."}
    },
    "11": {
        "father": {"chi": "父亲", "sent": "I love my father."},
        "mother": {"chi": "母亲", "sent": "My mother is beautiful."},
        "brother": {"chi": "兄弟", "sent": "He is my big brother."},
        "sister": {"chi": "姐妹", "sent": "I have a little sister."},
        "grandpa": {"chi": "爷爷", "sent": "My grandpa is kind."},
        "grandma": {"chi": "奶奶", "sent": "Grandma makes cookies."},
        "uncle": {"chi": "叔叔", "sent": "My uncle is tall."},
        "aunt": {"chi": "阿姨", "sent": "My aunt is nice."}
    },
    "12": {
        "home": {"chi": "家", "sent": "Go home now."},
        "room": {"chi": "房间", "sent": "Clean your room."},
        "window": {"chi": "窗户", "sent": "Open the window."},
        "door": {"chi": "门", "sent": "Close the door."},
        "bed": {"chi": "床", "sent": "Go to bed early."},
        "lamp": {"chi": "灯", "sent": "Turn on the lamp."},
        "floor": {"chi": "地板", "sent": "Sit on the floor."},
        "wall": {"chi": "墙", "sent": "The wall is white."}
    },
    "13": {
        "cup": {"chi": "杯子", "sent": "A cup of tea."},
        "plate": {"chi": "盘子", "sent": "Put it on the plate."},
        "bowl": {"chi": "碗", "sent": "A bowl of rice."},
        "fork": {"chi": "叉子", "sent": "I eat with a fork."},
        "spoon": {"chi": "勺子", "sent": "Use a spoon for soup."},
        "knife": {"chi": "刀", "sent": "The knife is sharp."},
        "pot": {"chi": "锅", "sent": "The pot is hot."},
        "fridge": {"chi": "冰箱", "sent": "Milk is in the fridge."}
    },
    "14": {
        "shirt": {"chi": "衬衫", "sent": "My shirt is white."},
        "coat": {"chi": "外套", "sent": "Put on your coat."},
        "dress": {"chi": "连衣裙", "sent": "The red dress is nice."},
        "skirt": {"chi": "短裙", "sent": "I like your skirt."},
        "pants": {"chi": "裤子", "sent": "My pants are blue."},
        "shoes": {"chi": "鞋子", "sent": "Clean your shoes."},
        "hat": {"chi": "帽子", "sent": "A yellow hat."},
        "socks": {"chi": "袜子", "sent": "Where are my socks?"}
    },
    "15": {
        "sun": {"chi": "太阳", "sent": "The sun is hot."},
        "rain": {"chi": "雨", "sent": "I like the rain."},
        "snow": {"chi": "雪", "sent": "I see white snow."},
        "wind": {"chi": "风", "sent": "The wind is strong."},
        "cloud": {"chi": "云", "sent": "A white cloud."},
        "cold": {"chi": "冷", "sent": "It is cold today."},
        "hot": {"chi": "热", "sent": "The water is hot."},
        "warm": {"chi": "温暖", "sent": "The sun is warm."}
    },
    "16": {
        "sky": {"chi": "天空", "sent": "The sky is blue."},
        "star": {"chi": "星星", "sent": "Twinkle little star."},
        "moon": {"chi": "月亮", "sent": "The moon is round."},
        "sea": {"chi": "大海", "sent": "The sea is deep."},
        "river": {"chi": "河流", "sent": "The river is long."},
        "lake": {"chi": "湖泊", "sent": "The lake is quiet."},
        "mountain": {"chi": "高山", "sent": "The mountain is high."},
        "tree": {"chi": "树木", "sent": "The tree is green."}
    },
    "17": {
        "run": {"chi": "跑", "sent": "I can run fast."},
        "jump": {"chi": "跳", "sent": "Jump like a rabbit."},
        "walk": {"chi": "走", "sent": "Walk to school."},
        "sit": {"chi": "坐", "sent": "Sit down, please."},
        "stand": {"chi": "站", "sent": "Stand up, please."},
        "sleep": {"chi": "睡觉", "sent": "Go to sleep."},
        "eat": {"chi": "吃", "sent": "Eat your food."},
        "drink": {"chi": "喝", "sent": "Drink some water."}
    },
    "18": {
        "read": {"chi": "读", "sent": "Read a book."},
        "write": {"chi": "写", "sent": "Write your name."},
        "draw": {"chi": "画", "sent": "Draw a flower."},
        "sing": {"chi": "唱", "sent": "Sing a song."},
        "dance": {"chi": "跳舞", "sent": "I like to dance."},
        "play": {"chi": "玩", "sent": "Let's play together."},
        "swim": {"chi": "游泳", "sent": "I can swim."},
        "fly": {"chi": "飞", "sent": "Birds can fly."}
    },
    "19": {
        "happy": {"chi": "开心", "sent": "I am so happy."},
        "sad": {"chi": "伤心", "sent": "Don't be sad."},
        "angry": {"chi": "生气", "sent": "The man is angry."},
        "tired": {"chi": "累", "sent": "I am very tired."},
        "hungry": {"chi": "饿", "sent": "I am hungry now."},
        "thirsty": {"chi": "渴", "sent": "I am thirsty."},
        "brave": {"chi": "勇敢", "sent": "You are very brave."},
        "shy": {"chi": "害羞", "sent": "The girl is shy."}
    },
    "20": {
        "circle": {"chi": "圆形", "sent": "It is a circle."},
        "square": {"chi": "正方形", "sent": "Draw a square."},
        "heart": {"chi": "心形", "sent": "A pink heart."},
        "star": {"chi": "星形", "sent": "A yellow star."},
        "line": {"chi": "线", "sent": "Draw a line."},
        "dot": {"chi": "点", "sent": "Follow the dots."},
        "big": {"chi": "大", "sent": "The elephant is big."},
        "small": {"chi": "小", "sent": "The ant is small."}
    },
    "21": {
        "in": {"chi": "在...里", "sent": "It is in the box."},
        "on": {"chi": "在...上", "sent": "It is on the desk."},
        "under": {"chi": "在...下", "sent": "It is under the chair."},
        "near": {"chi": "在...旁", "sent": "The cat is near me."},
        "behind": {"chi": "在...后", "sent": "Who is behind you?"},
        "front": {"chi": "在...前", "sent": "In front of the house."},
        "left": {"chi": "左", "sent": "Turn left here."},
        "right": {"chi": "右", "sent": "Turn right here."}
    },
    "22": {
        "car": {"chi": "小汽车", "sent": "My car is red."},
        "bus": {"chi": "大巴", "sent": "Wait for the bus."},
        "bike": {"chi": "自行车", "sent": "Ride your bike."},
        "plane": {"chi": "飞机", "sent": "The plane is high."},
        "boat": {"chi": "船", "sent": "A small boat."},
        "train": {"chi": "火车", "sent": "The train is fast."},
        "taxi": {"chi": "出租车", "sent": "Call a taxi."},
        "truck": {"chi": "卡车", "sent": "A big truck."}
    },
    "23": {
        "teacher": {"chi": "老师", "sent": "I love my teacher."},
        "doctor": {"chi": "医生", "sent": "Go to see a doctor."},
        "nurse": {"chi": "护士", "sent": "The nurse is kind."},
        "pilot": {"chi": "飞行员", "sent": "He is a pilot."},
        "cook": {"chi": "厨师", "sent": "My father is a cook."},
        "driver": {"chi": "司机", "sent": "The bus driver."},
        "worker": {"chi": "工人", "sent": "A hard worker."},
        "farmer": {"chi": "农民", "sent": "The farmer is busy."}
    },
    "24": {
        "ball": {"chi": "球", "sent": "Play with the ball."},
        "football": {"chi": "足球", "sent": "I like football."},
        "basket": {"chi": "篮子", "sent": "A fruit basket."},
        "tennis": {"chi": "网球", "sent": "Play tennis today."},
        "game": {"chi": "游戏", "sent": "Let's play a game."},
        "race": {"chi": "比赛", "sent": "Win the race."},
        "win": {"chi": "赢", "sent": "I want to win."},
        "fast": {"chi": "快", "sent": "He runs fast."}
    },
    "25": {
        "school": {"chi": "学校", "sent": "Go to school."},
        "park": {"chi": "公园", "sent": "Play in the park."},
        "zoo": {"chi": "动物园", "sent": "Go to the zoo."},
        "farm": {"chi": "农场", "sent": "Live on a farm."},
        "shop": {"chi": "商店", "sent": "Go to the shop."},
        "bank": {"chi": "银行", "sent": "The bank is near."},
        "hospital": {"chi": "医院", "sent": "He is in hospital."},
        "garden": {"chi": "花园", "sent": "The garden is pretty."}
    },
    "26": {
        "day": {"chi": "白天", "sent": "A sunny day."},
        "night": {"chi": "夜晚", "sent": "Good night."},
        "morning": {"chi": "早晨", "sent": "Good morning."},
        "evening": {"chi": "晚上", "sent": "In the evening."},
        "today": {"chi": "今天", "sent": "It is hot today."},
        "week": {"chi": "周", "sent": "A week has 7 days."},
        "month": {"chi": "月", "sent": "What month is it?"},
        "year": {"chi": "年", "sent": "Happy New Year!"}
    },
    "27": {
        "look": {"chi": "看", "sent": "Look at me."},
        "listen": {"chi": "听", "sent": "Listen to music."},
        "smell": {"chi": "闻", "sent": "Smell the flower."},
        "taste": {"chi": "尝", "sent": "Taste the cake."},
        "touch": {"chi": "摸", "sent": "Touch your nose."},
        "soft": {"chi": "软", "sent": "The bed is soft."},
        "hard": {"chi": "硬", "sent": "The stone is hard."},
        "loud": {"chi": "大声", "sent": "Don't be loud."}
    },
    "28": {
        "good": {"chi": "好", "sent": "You are a good boy."},
        "bad": {"chi": "坏", "sent": "The egg is bad."},
        "long": {"chi": "长", "sent": "The pencil is long."},
        "short": {"chi": "短", "sent": "It is too short."},
        "tall": {"chi": "高", "sent": "The tree is tall."},
        "thin": {"chi": "瘦", "sent": "The girl is thin."},
        "fat": {"chi": "胖", "sent": "The pig is fat."},
        "new": {"chi": "新", "sent": "I have a new bag."}
    },
    "29": {
        "old": {"chi": "老/旧", "sent": "An old man."},
        "young": {"chi": "年轻", "sent": "You are very young."},
        "beautiful": {"chi": "漂亮", "sent": "You are beautiful."},
        "cute": {"chi": "可爱", "sent": "The baby is cute."},
        "funny": {"chi": "逗趣", "sent": "A funny story."},
        "clean": {"chi": "干净", "sent": "Clean your hands."},
        "dirty": {"chi": "脏", "sent": "The shoes are dirty."},
        "quiet": {"chi": "安静", "sent": "Be quiet, please."}
    },
    "30": {
        "bee": {"chi": "蜜蜂", "sent": "The bee likes flowers."},
        "ant": {"chi": "蚂蚁", "sent": "The ant is small."},
        "frog": {"chi": "青蛙", "sent": "The frog can jump."},
        "fish": {"chi": "鱼", "sent": "The fish can swim."},
        "turtle": {"chi": "乌龟", "sent": "The turtle is slow."},
        "fly": {"chi": "苍蝇", "sent": "A fly is here."},
        "spider": {"chi": "蜘蛛", "sent": "Spider has 8 legs."},
        "worm": {"chi": "虫子", "sent": "The bird eats worm."}
    }
}


# ==========================================
# 4. 纯本地搜图函数
# ==========================================
def get_local_image(day, word):
    """
    只在本地 assets/dayX/ 文件夹下查找文件名为 word 的图片。
    妈妈精选，品质保证。
    """
    # 允许的图片后缀
    valid_extensions = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
    base_path = f"assets/day{day}/{word}"
    
    # 尝试查找本地文件
    for ext in valid_extensions:
        full_local_path = base_path + ext
        if os.path.exists(full_local_path):
            # Streamlit 可以直接读取本地路径
            return full_local_path
    
    # 如果找不到，返回占位图
    return PLACEHOLDER_IMG


# ==========================================
# 5. 页面头部 & 学习进度选择 (优化排版)
# ==========================================
st.markdown("<h1 class='main-title'>🌟 灿灿学英语</h1>", unsafe_allow_html=True)
st.markdown("<p class='slogan'>每一天的进步，都是灿灿闪闪发光的小勋章！✨</p>", unsafe_allow_html=True)

# 1. 生成日期列表
day_list = sorted(list(course_data.keys()), key=int)

# 2. 先让灿灿选择天数 (确保在最上方，操作方便)
day = st.selectbox("📅 灿灿，今天我们要学习第几天？", day_list, index=0) 

# 3. 计算勋章逻辑：当前天数 * 8
current_day_int = int(day)
all_learned_words_count = current_day_int * 8

# 4. 显示勋章区域
st.markdown(f"""
<div class='stats-container'>
    <div style='font-size: 0.8rem; opacity: 0.9;'>✨ 灿灿超棒！到今天为止你已经获得了</div>
    <div style='font-size: 2.2rem; font-weight: 800; margin: 5px 0;'>{all_learned_words_count}</div>
    <div style='font-size: 0.9rem; font-weight: bold;'>枚英语小勋章啦！🎉</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. 模式切换
# ==========================================
words_info = course_data[day]
words_info = course_data[day]

# 使用 Tabs 切换模式
tab1, tab2 = st.tabs(["📚 学习跟读", "🎮 综合挑战"])


# ==========================================
# 7. 学习模式 (Tab 1)
# ==========================================
with tab1:
    for eng, info in words_info.items():
        # --- 修改：只使用本地搜图 ---
        img_src = get_local_image(day, eng)
        
        # 展示图片，加宽一点
        st.image(img_src, use_container_width=True)
        
        # 展示单词和翻译
        st.markdown(f"<h2 class='word-title'>{eng}</h2><p style='text-align:center; color:#666; font-size:1.2rem; margin-top:-10px;'>({info['chi']})</p>", unsafe_allow_html=True)
        
        # 单词读音
        st.audio(f"https://dict.youdao.com/dictvoice?audio={eng}&type=2")
        
        # 句子跟读
        st.markdown(f"<div class='sent-box'><p style='color:#FF4B4B; font-weight:bold; margin-bottom:5px;'>📖 句子跟读：</p><p style='font-size:1.3rem; line-height:1.4;'>{info['sent']}</p></div>", unsafe_allow_html=True)
        
        # 句子读音 (需要编码 URL)
        encoded_sent = urllib.parse.quote(info['sent'])
        st.audio(f"https://dict.youdao.com/dictvoice?audio={encoded_sent}&type=2")
        
        # 分割线
        st.markdown("<br><hr style='border:1px dashed #FFCACA;'><br>", unsafe_allow_html=True)


# ==========================================
# 8. 综合挑战模式 (Tab 2)
# ==========================================
with tab2:
    st.markdown("### 🏆 看看灿灿记住了多少？")
    st.write("这里会随机抽取今天和以前学过的单词来挑战哦！")
    st.markdown("---")

    # 1. 构建适合当前进度的“已学单词库”
    all_past_words = {}
    current_day_int = int(day)
    for d_key, d_words in course_data.items():
        if int(d_key) <= current_day_int:
            for w, info in d_words.items():
                temp_info = info.copy()
                temp_info['belong_day'] = d_key
                all_past_words[w] = temp_info

    # 如果库是空的（比如第1天），加个保护
    if not all_past_words:
        st.warning("灿灿，先去『学习跟读』模式学几个单词再来挑战吧！💪")
        st.stop()

    # 2. 初始化 Session State (题目缓存)
    if 'quiz_target' in st.session_state:
        if st.session_state.quiz_target not in all_past_words:
            if 'quiz_mode' in st.session_state: del st.session_state.quiz_mode

    if 'quiz_mode' not in st.session_state or st.sidebar.button("♻️ 换一组题"):
        # 随机题目模式：听声音选图 vs 看图说词
        st.session_state.quiz_mode = random.choice(["listen", "speak"])
        
        # 随机目标单词
        st.session_state.quiz_target = random.choice(list(all_past_words.keys()))
        
        # 生成干扰项 (共4个选项)
        pool_size = min(len(all_past_words), 4)
        opts = random.sample(list(all_past_words.keys()), pool_size)
        # 确保目标单词在选项中
        if st.session_state.quiz_target not in opts:
            opts[0] = st.session_state.quiz_target
        random.shuffle(opts)
        
        st.session_state.quiz_options = opts
        st.session_state.quiz_answered = False


    target = st.session_state.quiz_target
    target_info = all_past_words[target]


    # --- 挑战模式 A: 听声音，选图片 ---
    if st.session_state.quiz_mode == "listen":
        st.markdown(f"#### 👂 第一关：听声音，选图片")
        st.write("点击小喇叭，听听看是哪个单词，然后选出正确的图片：")
        
        # 播放目标单词声音
        col_audio, _ = st.columns([1, 2])
        with col_audio:
            st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 展示4张图片供选择
        col1, col2 = st.columns(2)
        for i, opt in enumerate(st.session_state.quiz_options):
            with col1 if i % 2 == 0 else col2:
                opt_day = all_past_words[opt]['belong_day']
                # --- 修改：只使用本地搜图 ---
                found_opt_img = get_local_image(opt_day, opt)
                st.image(found_opt_img, use_container_width=True)
                
                # 选项按钮
                if st.button(f"选这个", key=f"sel_{opt}"):
                    if opt == target:
                        st.success("灿灿真棒！答对了！🎉")
                        st.balloons()
                        st.session_state.quiz_answered = True
                    else:
                        st.error("哎呀，选错了，再听一遍试试看？")


    # --- 挑战模式 B: 看图说词 ---
    else:
        st.markdown(f"#### 🖼️ 第二关：看图说词")
        st.write("灿灿，大声说出这是什么？（说完点击检查答案）")
        st.markdown("<br>", unsafe_allow_html=True)
        
        target_day = target_info['belong_day']
        # --- 修改：只使用本地搜图展示目标 ---
        found_target_img = get_local_image(target_day, target)
        st.image(found_target_img, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 检查答案按钮
        if st.button("检查答案"):
            st.session_state.quiz_answered = True
            
    # 3. 答题完成后的展示
    if st.session_state.get('quiz_answered'):
        st.markdown("---")
        st.markdown(f"**答案是：** <span style='font-size:1.5rem; color:#FF4B4B; font-weight:bold;'>{target}</span> ({target_info['chi']})", unsafe_allow_html=True)
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        st.write(f"📖 句子：{target_info['sent']}")
        
        # 挑战下一题
        if st.button("挑战下一题 ➡️"):
            # 清除 Session State，强制重新生成题目
            if 'quiz_mode' in st.session_state: del st.session_state.quiz_mode
            st.rerun()
