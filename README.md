![Banner](/readme/aircatbanner.gif)
# airCat v0.1
>airCat is a text-based airline simulation game made in Python where players can become "pilots-cats" and
start virtual flights directly from streamer's Twitch chat using commands starting with '#'. The players can accumulate
flight hours and get to higher ranks as they keep flying for the virtual company.

>airCat é um jogo de simulação de companhia aérea baseado em texto feito em Python onde os jogadores podem
se tornar "gatos-pilotos" e iniciar voos virtuais diretamente do chat da Twitch. Os jogadores podem acumular horas e 
atingir ranks mais altos conforme voam pela companhia virtual.

You can either use the code as a template for your project or play the game on my Twitch channel's chat while i'm live!

Você pode tanto usar esse código como modelo para seu projeto como jogar durante minhas lives na Twitch!

[Twitch Channel](https://twitch.tv/elicktengan)

## How to play 

If is your first time playing the game, start by just sending *#newcat* to register as a new pilot. If everything's
OK, you will receive a confirmation message on the chat and can start your flight by using #catfly! 

After starting a flight, your place will be defined as "Sky" and you can't start a new flight before finishing the
current one. For this first version of the game, there is only two routes available (Campinas -> Rio, Rio <- Campinas)
that takes 1 hour and 15 minutes to finish. Everytime you start a flight, it defines the route based on your last's
flight destiny (that is your current location).

During flight, you can use *#catfly* again to check time remaining, our use *#catstatus*, to show your game profile, 
containing your pilot ID number, rank, real-time updated flight hours and location. 

## Como jogar

Se for sua primeira vez jogando, comece enviando *#newcat* no chat para se registrar como um novo gato-piloto. Se tudo 
estiver OK, você receberá uma mensagem de confirmação no chat e poderá iniciar seu voo usando *#catfly*!

Depois de iniciar um voo, seu local será definido como "Sky" e você não poderá iniciar um novo voo antes de terminar o
atual. Nessa primeira versão do jogo, só existem duas rotas disponíveis (Campinas -> Rio, Rio <- Campinas), que levam 
1 hora e 15 minutos para terminar. Sempre que você inicia um voo, o jogo define sua rota com base no destino do último vôo
(que é sua localização atual).

Durante o voo, você pode usar *#catfly* novamente para verificar o tempo de voo restante. Você também pode usar *#catstatus* 
a qualquer momento para mostrar seu perfil, contendo número de identificação do piloto, rank, localização e horas de voo 
atualizadas em tempo real.


## Rank System - Sistema de Ranks

Rank | Hours
------|------
Kitty V|0
Kitty IV|1
Kitty III|5
Kitty II|10
Kitty I|15
Trainee Cat IV|20
Trainee Cat III|25
Trainee Cat II|30
Trainee Cat I|35
Copilot Cat IV|40
Copilot Cat III|50
Copilot Cat II|60
Copilot Cat I|70
Private Pilot Cat IV|100
Private Pilot Cat III|125
Private Pilot Cat II|150
Private Pilot Cat I|175
Commercial Pilot Cat IV|200
Commercial Pilot Cat III|250
Commercial Pilot Cat II|300
Commercial Pilot Cat I|350
Feline Flight Instructor|500
Master of Air Cat|1000
GrandMaster of Air Cat|2500
Radiant Cat|5000

## Dev Info

Libraries used: [aiomysql](https://github.com/aio-libs/aiomysql) [asyncio](https://github.com/python/asyncio) [twitchio](https://github.com/TwitchIO/TwitchIO)

Data stored into MySQL database.
Code uses async modules to access twitch's chat and executes SQL queries, so it's kinda *fast*, even using MySQL database.
Uses Python 3.9.
Free to use under MIT License.

Código com comentários em inglês, se você não entender algo pode entrar em contato comigo pelas redes sociais ou pelo Github. Sinta-se livre pra dar um
git clone e usar o código como quiser.
