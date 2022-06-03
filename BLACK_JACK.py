# black jack

import sys
import os
import time
import random
import math

# все виды карт
soc_vis = ['♥', '♦', '♠', '♣']
soc_nam = ['hearts', 'diamonds', 'spades', 'clubs']
voc = list(range(2, 11)) + ['J', 'Q', 'K', 'A']

posres = ['y', 'Y', 'yes']
negres = ['n', 'N', 'no']


def begin(tn=6):
    t = 0
    while True:
        if t > 4:
            print("Aight I'm done, you've lost your blackjack privileges for today.")
            print("Please try again later.")
            return 0
            break

        print("How many people will be joining today?")
        print("Maximum of", tn, "players.")
        try:
            x = int(input())
        except ValueError:
            print("Must be a number.")
            t += 1
            time.sleep(3)
            continue
        else:
            if 1 <= x <= tn:
                return x
            else:
                print("Please be reasonable, must be between 1 and", tn)
                t += 1
                time.sleep(3)
                continue


# function to create deck
def create_deck(x):
    deck = {}
    z = 1
    for i in range(x):
        for n in voc:
            for m in soc_vis:
                deck[z] = (str(n) + m)
                z += 1
    return deck


# устанавливает количество игроков (а также колоды)
tpd = begin()
if tpd < 1:
    sys.exit()

# количество игроков для именования по умолчанию в будущем
pc = tpd

# словарь колоды, карты выбираются случайным образом из списка и относятся к картам здесь
a_deck = create_deck(tpd)

# количество карт в колоде
ld = len(a_deck.keys())
# список со всеми оставшимися картами в колоде
carlis = list(range(1, (ld + 1)))

#когда длина колоды становится меньше этой точки, колода переделывается
reshuf = ld / 2

# список выбывших, на случай, если кто-то захочет вернуться со своими фишками
leli = []
# класс игрока для отслеживания карт, ставок и фишек


class Player:

    def __init__(self, name):
        self.name = name
        self.chips = 1000
        self.bet = 0
        self.cards = []
        self.cv = 0
        self.qtr = 0

    def place_bet(self, amt):
        self.chips -= amt
        self.bet += amt

    def give_card(self, c):
        self.cards.append(a_deck[c])

    def find_cv(self):
        self.cv = 0
        a = 0
        for c in self.cards:
            try:
                b = int(c[0:-1])
            except ValueError:
                if c[0] in ["J", "Q", "K"]:
                    self.cv += 10
                if c[0] == "A":
                    self.cv += 1
                    a += 1
            else:
                self.cv += b
        if a > 0:
            if self.cv <= 11:
                self.cv = (self.cv, self.cv + 10)

    # ws = 1 if won, 0 if lost
    def end_turn(self, ws):

        if ws == 1:
            self.chips += 2 * self.bet
            print(self.name, "has won with:", self.cv, "vs the dealers", dealer.cv, '\n', "New chips count:",
                  self.chips)
        elif ws == 2:
            self.chips += math.ceil(2.5 * self.bet)
            print(self.name, "has won with: blackjack", '\n', "New chips count:", self.chips)
        elif ws == 0:
            self.chips += self.bet
            print(self.name, "has pushed with:", self.cv, "vs the dealers", dealer.cv, '\n', "New chips count:",
                  self.chips)
        elif ws == -1:
            print(self.name, "has lost with:", self.cv, "vs the dealers", dealer.cv, '\n', "New chips count:",
                  self.chips)
        self.bet = 0
        self.cards = []
        self.cv = 0


dealer = Player('Dealer')


# function for asking yes or no questions, 3 tries
def yn_askr():
    t = 0
    while True:
        if t > 4:
            return "nr"
        i = input()
        if i in posres:
            return "y"
        elif i in negres:
            return "n"
        else:
            print("I did not get that, please respond yes or no.")
            time.sleep(1)
            t += 1
            continue


# функция создания игрока, 3 попытки или заданное имя по умолчанию
def play_n(x):
    t = 0
    while True:
        if t > 3:
            print("Exceeded number of tries, given default name Player " + str(x))
            time.sleep(1)
            return "Player " + str(x)
        print("Player " + str(x) + ", insert name:")
        z = input()
        time.sleep(.5)
        print("You have chosen the name " + str(z) + ", is this correct?")
        q = yn_askr()
        if q == "y":
            return str(z)
        elif q == "n":
            t += 1
            continue
        elif q == "nr":
            print("Exceeded number of tries, given default name Player " + str(x))
            time.sleep(1)
            return "Player " + str(x)
# список игроков для объектов класса


pl = []
for a in range(tpd):
    pl.append(Player(play_n(a + 1)))
    time.sleep(.5)
    print(pl[a].name + ' you have been given 1000 chips.')
    time.sleep(1.5)


# спрашивает каждого игрока, будут ли они делать ставки в этом раунде, тайм-аут после 3 попыток
# возвращает список всех игроков, участвующих в раунде
def bet_ask():
    inround = []
    quit_list = []
    for i in pl:
        t = 0
        while True:
            if t > 3:
                print("Sorry, maximum allowed attempts passed.")
                time.sleep(2)
                break

            ooc = 0
            if i.chips == 0:
                print(i.name, "you are out of chips, would you like to continue?")
                huh = yn_askr()
                if huh == "y":
                    print("500 chips have been added to your account.")
                    i.chips = 500
                    time.sleep(1.5)
                else:
                    quit_list.append(i)
                    print("You are leaving, please wait until the end of the round to cash out.")
                    time.sleep(1.5)
                    break

            print(i.name + ", you have " + str(i.chips) + " chips, would you like to buy in this round?")
            x = input()
            if x in posres:
                bet_amt_ask(i)
                if i.bet > 0:
                    i.qtr = 0
                    inround.append(i)
                break
            elif x in negres:
                i.qtr += 1
                if i.qtr > 3:
                    print("You have skipped out on three rounds in a row, would you like to quit?")
                    q = yn_askr()
                    if q in ["y", "nr"]:
                        print("Are you sure?")
                        z = yn_askr()
                        if z in ["y", "nr"]:
                            quit_list.append(i)
                            print("You are leaving, please wait until the end of the round to cash out")
                            time.sleep(1.5)
                        elif z == "n":
                            i.qtr = 0
                    elif q == "n":
                        i.qtr = 0
                break
            else:
                print("I didn't get that, please respond yes or no.")
                time.sleep(2)
                t += 1
                continue
        if len(pl) > 1:
            if pl.index(i) == (len(pl) - 1):
                print("Return computer to first player.")
                time.sleep(2)
            else:
                print("Please pass computer to next player.")
                time.sleep(2)


    if len(inround) > 0:
        for i in range(4):

            a = 'All bets are in, please wait while I deal the cards'
            for j in range(4):

                print(a + j * '.')
                time.sleep(.25)
    else:
        print("No bets were placed, removing top " + str((tpd + 1) * 2) + " cards from deck.")
        time.sleep(2)

    return (inround, quit_list)


# спрашивает игрока, сколько он будет ставить в этом раунде, тайм-аут после 3 попыток
def bet_amt_ask(pers):
    u = 0
    while True:
        if u > 4:
            print("Sorry, maximum allowed attempts passed.")
            time.sleep(2)
            break
        print(pers.name + ", how much would you like to bet?")
        try:
            x = int(input())
        except ValueError:
            print("Must be a number.")
            u += 1
            time.sleep(1)
            continue
        else:
            if x > 0:
                if x <= pers.chips:
                    print("You are betting " + str(x) + " chips.")
                    pers.place_bet(x)
                    time.sleep(1)
                    break
                else:
                    print('Sorry, you are betting too much, you only have ' + str(pers.chips) + ' chips.')
                    time.sleep(2)
                    u += .5
                    continue
            else:
                print('Must be a positive number.')
                time.sleep(2)
                u += 1
                continue


# проверяем, находится ли колода ниже середины, «перетасовывает» (путем воссоздания списка)
def deck_check():
    global carlis
    if len(carlis) < reshuf:
        carlis = list(range(1, (ld + 1)))
        for i in range(4):
            a = 'Deck is low, please wait while I reshuffle the deck'
            for j in range(4):
                os.system('clear')
                print(a + j * '.')
                time.sleep(.25)


# удаляет данный список игроков
def rmvplr(qtlst):
    global tpd
    for qt in range(len(qtlst)):
        print(qtlst[qt].name, "you have ended the game with", qtlst[qt].chips, "chips.")
        leli.append(qtlst[qt])
        pl.remove(qtlst[qt])
        tpd -= 1
        time.sleep(2)


# переделывать колоду после ухода игрока
def rmde(ntpd):
    print("Please wait as deck is readjusted for new player count.")
    global tpd
    global a_deck
    global ld
    global carlis
    global reshuf
    time.sleep(2)
    tpd = ntpd
    a_deck = create_deck(ntpd)
    ld = len(a_deck.keys())
    carlis = list(range(1, (ld + 1)))
    reshuf = ld / 2


# печатает карты и значение для всех в игре во время раунда
def bj_intrface(tr):
    print("Dealer has", *dealer.cards)
    if isinstance(dealer.cv, tuple):
        print("Worth " + str(dealer.cv[0]) + " or " + str(dealer.cv[1]), '\n', '\n')
    else:
        print("Worth " + str(dealer.cv), '\n', '\n')
    for p in tr:
        print(p.name, "has", *p.cards)
        if isinstance(p.cv, tuple):
            print("Worth " + str(p.cv[0]) + " or " + str(p.cv[1]), '\n', '\n')
        else:
            print("Worth " + str(p.cv), '\n', '\n')


# функция играть
def play_round():
    deck_check()
    ba = bet_ask()
    tr = ba[0]
    wl = []
    bwl = []
    tl = []
    ll = []
    if len(tr) == 0:
        for i in range((tpd + 1) * 2):
            carlis.pop(random.randrange(len(carlis)))

    else:
        dc = carlis.pop(random.randrange(len(carlis)))
        dealer.give_card(dc)
        dealer.find_cv()

        for p in tr:
            c1 = carlis.pop(random.randrange(len(carlis)))
            c2 = carlis.pop(random.randrange(len(carlis)))
            p.give_card(c1)
            p.give_card(c2)
            p.find_cv()
            if isinstance(p.cv, tuple):
                if p.cv[1] == 21:
                    p.cv = "bj"

        time.sleep(2)

        for plr in tr:
            while True:
                if len(plr.cards) > 2:
                    print('Received card', plr.cards[-1], ', you are now at', plr.cv, '\n\n')
                bj_intrface(tr)

                if isinstance(plr.cv, tuple):
                    plr.cv = plr.cv[1]
                if plr.cv == "bj":
                    print(plr.name + ", you have blackjack!\n \n")
                    time.sleep(2)
                    break
                elif plr.cv > 21:
                    print(plr.name + ", you bust!\n \n")
                    time.sleep(2)
                    break
                elif plr.cv == 21:
                    print(plr.name + ", you have 21!\n \n")
                    time.sleep(2)
                    break

                print(plr.name + ", would you like to hit?\n \n")
                yn = yn_askr()
                if yn == "y":
                    c3 = carlis.pop(random.randrange(len(carlis)))
                    plr.give_card(c3)
                    plr.find_cv()
                    print('Received card', a_deck[c3], ', you are now at', plr.cv, '\n\n')
                    time.sleep(1)
                    continue
                else:
                    print('Pass Computer to next player.\n \n')
                    time.sleep(2)
                    break

        while True:
            if isinstance(dealer.cv, tuple):
                if dealer.cv[1] < 17:
                    dc1 = carlis.pop(random.randrange(len(carlis)))
                    dealer.give_card(dc1)
                    dealer.find_cv()
                    bj_intrface(tr)
                    time.sleep(2)
                    continue
                else:
                    dealer.cv = dealer.cv[1]
                    time.sleep(2)
                    break
            else:
                if dealer.cv < 17:
                    dc1 = carlis.pop(random.randrange(len(carlis)))
                    dealer.give_card(dc1)
                    dealer.find_cv()
                    bj_intrface(tr)
                    time.sleep(2)
                    continue
                else:
                    time.sleep(2)
                    break

        for al in tr:
            if isinstance(al.cv, tuple):
                al.cv = al.cv[1]
            if al.cv == "bj":
                if dealer.cv != 21:
                    bwl.append(al)
                else:
                    tl.append(al)
            elif al.cv <= 21:
                if dealer.cv == al.cv:
                    tl.append(al)
                elif dealer.cv < al.cv:
                    wl.append(al)
                elif dealer.cv > 21:
                    wl.append(al)
                else:
                    ll.append(al)
            else:
                ll.append(al)

    for b in bwl:
        b.end_turn(2)
    for a in wl:
        a.end_turn(1)
    for c in tl:
        c.end_turn(0)
    for d in ll:
        d.end_turn(-1)

    dealer.end_turn("d")

    if len(ba[1]) > 0:
        print("Player has decided to leave, will anyone else be joining?\n \n")
        global pc
        ask = yn_askr()
        if ask == "y":
            e = len(pl) - len(ba[1])
            ntpd = begin((8 - e))
            if ntpd >= 1:
                for i in range(ntpd):
                    pc += 1
                    pl.append(Player(play_n(pc)))
                    time.sleep(.5)
                    print(pl[-1].name + ' you have been given 1000 chips.\n \n')
                    time.sleep(1.5)
        rmvplr(ba[1])
        if len(pl) < 1:
            print("All players have left, game is over.\n \n")
            time.sleep(5)
            sys.exit()
        else:
            rmde(len(pl))

    print('The round has ended, would you like to continue playing?\n \n')
    q = yn_askr()
    if q == "y":
        play_round()
    elif q == "n":
        print("Are you sure? \nThe game will finish and all players will cash out.\n \n")
        print("Hint: Individual players can leave if they skip 3 betting rounds in a row.\n \n")
        z = yn_askr()
        if z in ["y", "nr"]:
            ql = []
            for i in pl:
                ql.append(i)
            rmvplr(ql)
            time.sleep(2)
            sys.exit()
        elif z == "n":
            play_round()


print("Game is set up, shall we begin?")
ok = yn_askr()
if ok == "y":
    play_round()
else:
    print("OK, write play_round() when you're ready to begin.\n \n")

# добавить статистику в конце игры
