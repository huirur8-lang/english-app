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

# 3. 核心单词数据库 (30天计划)
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

# 辅助函数：获取图片路径（增加更多容错性）
def get_img_path(day, word):
    base_path = f"assets/day{day}/{word}"
    # 尝试所有常见的扩展名
    for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]:
        if os.path.exists(base_path + ext):
            return base_path + ext
    return None

# 4. 头部
st.markdown("<h1 class='main-title'>🌟 灿灿学英语</h1>", unsafe_allow_html=True)
st.markdown("<p class='slogan'>每一天的进步，都是灿灿闪闪发光的小勋章！✨</p>", unsafe_allow_html=True)

# 生成日期列表
day_list = sorted(list(course_data.keys()), key=int)
day = st.selectbox("📅 选择今天的学习进度：", day_list, index=len(day_list)-1)
words_info = course_data[day]

tab1, tab2 = st.tabs(["📚 学习跟读", "🎮 挑战挑战"])

# 5. 学习模式
with tab1:
    for eng, info in words_info.items():
        img = get_img_path(day, eng)
        if img:
            st.image(img, width=280)
        else:
            st.info(f"💡 灿灿，快让妈妈在 assets/day{day}/ 文件夹下放一张 {eng} 的图片吧！")
        
        st.markdown(f"<h2 class='word-title'>{eng} <small>({info['chi']})</small></h2>", unsafe_allow_html=True)
        st.audio(f"https://dict.youdao.com/dictvoice?audio={eng}&type=2")
        
        st.markdown(f"<div class='sent-box'><p style='color:#FF4B4B; font-weight:bold;'>📖 句子跟读：</p><p style='font-size:1.2rem;'>{info['sent']}</p></div>", unsafe_allow_html=True)
        encoded_sent = urllib.parse.quote(info['sent'])
        st.audio(f"https://dict.youdao.com/dictvoice?audio={encoded_sent}&type=2")
        st.markdown("---")

# 6. 综合挑战模式 (滚雪球式复习)
with tab2:
    # A. 动态构建单词池
    all_past_words = {}
    current_day_int = int(day)
    for d_key, d_words in course_data.items():
        if int(d_key) <= current_day_int:
            for w, info in d_words.items():
                temp_info = info.copy()
                temp_info['belong_day'] = d_key
                all_past_words[w] = temp_info

    # B. 防崩溃逻辑
    if 'quiz_target' in st.session_state:
        if st.session_state.quiz_target not in all_past_words:
            if 'quiz_mode' in st.session_state: del st.session_state.quiz_mode

    # C. 初始化题目
    if 'quiz_mode' not in st.session_state or st.sidebar.button("♻️ 换一组题"):
        st.session_state.quiz_mode = random.choice(["listen", "speak"])
        st.session_state.quiz_target = random.choice(list(all_past_words.keys()))
        
        pool_size = min(len(all_past_words), 4)
        opts = random.sample(list(all_past_words.keys()), pool_size)
        if st.session_state.quiz_target not in opts:
            opts[0] = st.session_state.quiz_target
        random.shuffle(opts)
        
        st.session_state.quiz_options = opts
        st.session_state.quiz_answered = False

    target = st.session_state.quiz_target
    target_info = all_past_words[target]

    # D. 听音选图
    if st.session_state.quiz_mode == "listen":
        st.write(f"### 👂 听声音，选图片")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        
        col1, col2 = st.columns(2)
        for i, opt in enumerate(st.session_state.quiz_options):
            with col1 if i % 2 == 0 else col2:
                opt_day = all_past_words[opt]['belong_day']
                found_opt_img = get_img_path(opt_day, opt)

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

    # E. 看图说词
    else:
        st.write(f"### 🖼️ 看图说词")
        st.write("灿灿，大声说出这是什么？")
        
        target_day = target_info['belong_day']
        found_target_img = get_img_path(target_day, target)
        
        if found_target_img:
            st.image(found_target_img, width=300)
        else:
            st.warning(f"📸 缺少图片: {target}")
            
        if st.button("检查答案"):
            st.session_state.quiz_answered = True
            
    # F. 反馈区
    if st.session_state.get('quiz_answered'):
        st.info(f"答案是：{target} ({target_info['chi']})")
        st.audio(f"https://dict.youdao.com/dictvoice?audio={target}&type=2")
        if st.button("挑战下一题 ➡️"):
            if 'quiz_mode' in st.session_state: del st.session_state.quiz_mode
            st.rerun()
