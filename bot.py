import asyncio, discord, random, threading, os
from time import localtime, strftime

app = discord.Client()
token = "NjI3NTEyNTEwMzg3NDUzOTU1.XZEJgQ.t8LXVqRyhBfgGS583K88ZeizZC0"
game_list = ["타르코프에서 삥뜯기기",
                 "엉덩이로 이름쓰기",
                 "태와 레식",
                 "거울과 가위바위보",
                 "리그 오브 레전드"]

async def fun_changeGame():
    current_game = game_list[random.randint(0, len(game_list)-1)]
    game = discord.Game(current_game)
    await discord.Client.change_presence(app, status=discord.Status.online, activity=game)

from discord.ext import commands

# 봇이 구동되었을 떄 동작되는 코드
@app.event
async def on_ready():
    print(strftime("%Y-%m-%d %H:%M:%S ", localtime())+ app.user.name, "봇 가동.")
    current_game = game_list[random.randint(0, len(game_list) - 1)]
    game = discord.Game(current_game)
    await discord.Client.change_presence(app, status=discord.Status.online, activity=game)

# 봇이 새로운 메시지를 수신
@app.event
async def on_message(message) :
    if message.author.bot:
        return None;

    if message.content == "!도움" or message.content == "!help" or message.content == "!기능" or message.content == "!규태" or message.content == "!명령어":
        await message.channel.send("```사용가능한 명령어 모음입니다.\n\n"
                                   "!주사위 [number_생략가능]   !랜덤 [number_생략가능]\n"
                                   "!가위바위보\n"
                                   "!한일 [검색어]\n"
                                   "!일한 [검색어]\n"
                                   "!한영 [검색어]\n"
                                   "!영한 [검색어]\n"
                                   "!실검     !실시간검색어\n"
                                   "!헛소리    !어록\n"
                                   "!헛소리추가 [헛소리]\n"
                                   "!어록추가 [헛소리]\n"
                                   "!게임변경 [게임이름]"
                                   "\n\n기능 추가중입니다. 아이디어 환영"
                                   "```")

    def get_random(range):
        random_number = random.randint(1, range)
        dice_subtext = ''
        if(message.author.id == 277067626541350925):
            random_number = range
            dice_subtext += "꼽으면 너도 규태하던가~"
        elif (random_number <= range * 0.2):
            dice_subtext += "발로굴려도 이거보단 낫겠군요."
        elif (random_number <= range * 0.4):
            dice_subtext += "최악은 면했어요."
        elif (random_number <= range * 0.6):
            dice_subtext += "나쁘지 않아요!"
        elif (random_number <= range * 0.8):
            dice_subtext += "어디 한번 덤벼보시지!"
        elif (random_number <= range and range < 100):
            dice_subtext += "전설의 " + user + " !"
        elif (range >= 100):
            dice_subtext += "사기치지마 이 닭대가리야!"
        return (user + "는 " + str(random_number) + "(이)가 나왔습니다. " + dice_subtext)

    if message.content.startswith("!주사위") or message.content.startswith("!랜덤") or message.content.startswith("!random") or message.content.startswith("!dice"):
        try :
            user = discord.Client.get_user(app, message.author.id).name
            range = int(message.content.split(' ', maxsplit=2)[1])
            await message.channel.send(get_random(range))
            return
        except IndexError :
            await message.channel.send(get_random(100))
        except ValueError :
            await message.channel.send("올바르지 않은 형식입니다.")

    if message.content == "!가위바위보":
        value = random.randint(1,3)
        user =  discord.Client.get_user(app, message.author.id).name
        if (value == 1): #가위
            await message.channel.send(user + "는 가위를 냈습니다.")
        elif (value == 2):
            await message.channel.send(user + "는 바위를 냈습니다.")
        else:
            await message.channel.send(user + "는 보자기를 냈습니다.")
        
    if message.content.startswith("!한일 ") or message.content.startswith("!일한 ") or message.content.startswith("!한영 ") or message.content.startswith("!영한 "):
        try :
            from googletrans import Translator
            texts = message.content.split(' ')
            idx = 0
            query = ''
            for text in texts :
                if(idx>0):
                    query += text + " "
                idx+=1

            translator = Translator()
            if(message.content.startswith("!한일")) :
                tr_results = translator.translate(query, src='ko', dest='ja')
            elif(message.content.startswith("!일한")) :
                tr_results = translator.translate(query, src='ja', dest='ko')
            elif(message.content.startswith("!한영")) :
                tr_results = translator.translate(query, src='ko', dest='en')
            elif(message.content.startswith("!영한")) :
                tr_results = translator.translate(query, src='en', dest='ko')
            await message.channel.send(tr_results.text)
            return

        except IndexError :
            await message.channel.send("번역할 글을 넣어주세요.")
        except ValueError :
            await message.channel.send("오류가 발생했어요.")

    if (message.content == "!실검" or message.content == "!실시간검색어"):
        from bs4 import BeautifulSoup
        import requests

        url = ("http://www.naver.com")
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        silgum_result = current_time + " 실시간 검색어입니다.\n"
        silgum_idx=1

        for tag in soup.select('span[class=ah_k]'):
            silgum_result += str(silgum_idx) + ". " + tag.text + "\n"
            silgum_idx += 1
            if(silgum_idx > 10):
                break;

        await message.channel.send(silgum_result)

    if (message.content == "!헛소리" or message.content == "!어록"):
        # f = open("C:\\Users\\HanSeokJun\\Desktop\\gyubot\\venv\\uhrok.txt", 'r')
        f = open(os.getcwd()+"uhrok.txt", 'r')
        list = []
        while True:
            line = f.readline()
            if not line: break;
            list.append(line)
        rand_num = random.randint(0,len(list)-1)
        f.close()
        await message.channel.send(list[rand_num])

    if (message.content.startswith("!헛소리추가") or message.content.startswith("!어록추가")):
        add_uhrok = message.content.split(' ')
        idx = 0
        if(len(add_uhrok)<2):
            await message.channel.send("추가할 헛소리를 뒤에 입력해주세요.")
            return
        uhrok = " ".join(add_uhrok[1:])
        # f = open("C:\\Users\\HanSeokJun\\Desktop\\gyubot\\venv\\uhrok.txt", 'a')
        f = open(os.getcwd()+"uhrok.txt", 'a')
        f.write(uhrok + "\n")
        f.close()
        await message.channel.send("어록에 [" + uhrok + "]이(가) 추가되었습니다.")

    if (message.content.startswith("!음악") or message.content.startswith("!music")):
        music_name = message.content.split(" ")[1]
        user = message.author
        try:
            voice_channel = user.voice.channel
        except:
            await message.channel.send('유저가 속한 채널이 없습니다.')
            return
        channel = None
        #only play music if user is in a voice chanel
        if voice_channel != None:
            channel = voice_channel.name
            await message.channel.send(channel + " 채널에 접속합니다.")
            music_file = ''
            if(music_name == "포켓몬"):
                music_file = 'rocketdan.mp3'
            await voice_channel.connect()
            #music = discord.FFmpegPCMAudio.is_opus(os.getcwd()+"\\music\\"+music_file)
            player = discord.FFmpegPCMAudio.is_opus("C:\\Users\\HanSeokJun\\Desktop\\gyubot\\music\\"+music_file)
            # 오류
            vc = discord.VoiceClient(state=discord.VoiceState.channel.loo ,timeout=60, channel=voice_channel).loop=False
            vc.play(self=vc,source = player)

            #await vc.play(self=vc,source = music)

            #voice.play(os.getcwd()+"\\music\\"+music_file, after=lambda: print('play ' + music_file))
            # 음악 플레이중에 ㅇㅇ
            # disconnet after the player has finished
            player.stop()
            await vc.disconnet()

    if (message.content == "!물어"):
        bite_num = random.randint(1,5)
        if(bite_num == 1):
            await message.channel.send("멍! 크아아아앙!")
        elif(bite_num == 2):
            await message.channel.send("멍멍 으르르르 컹컹!!")
        elif(bite_num == 3):
            await message.channel.send("멍멍 냐옹 멍멍멍")
        elif(bite_num == 4):
            await message.channel.send("나는 나보다 약한자의 말은 듣지 않는다.")
        elif(bite_num == 5):
            await message.channel.send("멍멍멍멍멍멍멍멍멍멍멍멍멍멍멍멍~~")

    if (message.content.startswith('💼 🐟')):
        user = discord.Client.get_user(app, message.author.id).name
        brief_fish = ''
        fish_case = random.randint(1, 5)
        if(fish_case == 1) :
            brief_fish = user + "는 신이난 모양이에요"
        elif(fish_case == 2) :
            brief_fish = user + ", 집 빨리가니까 좋냐?"
        elif(fish_case == 3) :
            brief_fish = user + "가 기분이 좋아보이네요."
        elif(fish_case == 4) :
            brief_fish = user + ", 어쩌라구요."
        elif(fish_case == 5) :
            brief_fish = user + "가 과제가 많았으면 좋겠네요."

        await message.channel.send(brief_fish)

    if (message.content.startswith("!게임변경")):
        change_subtext = message.content.split(' ')
        if(len(change_subtext)>1):
            change_subtext = " ".join(change_subtext[1:])
            await discord.Client.change_presence(app, status=discord.Status.online, activity=discord.Game(change_subtext))
            return
        current_game = game_list[random.randint(0, len(game_list) - 1)]
        game = discord.Game(current_game)
        await discord.Client.change_presence(app, status=discord.Status.online, activity=game)

access_token = os.environ["BOT_TOKEN"]
app.run(access_token)



