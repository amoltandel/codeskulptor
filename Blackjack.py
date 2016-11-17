# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png?dl=1")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png?dl=1")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.current_hand = []  # create Hand object

    def __str__(self):
        str1 = '';
    # return a string representation of a hand
        for i in self.current_hand:
            str1 = str1 + i.suit + i.rank+' '
            
        return (str1)
    def add_card(self, card):
        self.current_hand.append(card)  # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        sum = 0;
        flag = False
        for i in self.current_hand:
            sum += VALUES[i.get_rank()]
            if (i.get_rank() =='A'):
                flag = True
        
        
        if (flag):
            if (sum+10 < 21):
                return(sum+10)
            
        return (sum)
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        c = 0
        for i in self.current_hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(i.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(i.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + (c * CARD_CENTER[0]), pos[1] + (CARD_CENTER[1])], CARD_SIZE)
            pos[0] += 40
            c +=1
        
# define deck class 
class Deck:
    def __init__(self):
        self.current_deck = []
        # create a Deck object
        for i in SUITS:
            for j in RANKS:
                card = Card(i, j)
                self.current_deck.append(card)
        
    def shuffle(self):
        # shuffle the deck 
        
        # use random.shuffle()
        random.shuffle(self.current_deck)
        
        
    def deal_card(self):
        # deal a card object from the deck
        temp = self.current_deck.pop(0)
        
        return temp
    
    def __str__(self):
        # return a string representing the deck
        s1 =  'Deck contains '
        for i in self.current_deck:
            s1 = s1 + str(i) + ' '
        
        return s1


deck = Deck()
player = Hand()
dealer = Hand()

#define event handlers for buttons
def deal():
    
    print "Deal:\n"
    global outcome, in_play
    global deck, score
    global busted, player, dealer
    # your code goes here
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    p = deck.deal_card()
    player.add_card(p)
    outcome = "Hit or Stand?"
    d = deck.deal_card()
    dealer.add_card(d)
    
    p = deck.deal_card()
    player.add_card(p)
    
    d = deck.deal_card()
    dealer.add_card(d)
    
    print "Dealer :"
    print dealer
    print "Player :"
    print player
    busted = False
    if(in_play):
        print "Player lost"
        score -=1
    
    in_play = True

busted = False
def hit(id = True):
    # replace with your code below
    print "Hit :\n"
    global player, deck, dealer, busted, score,in_play
    if id:
        temp = deck.deal_card()
        player.add_card(temp)
        if (player.get_value()>21):
            print "You have busted"
            score -= 1
            busted = True
            in_play = False
    else:
        dealer.add_card(deck.deal_card())
        
    print "Dealer :"
    print dealer
    print "Player :"
    print player
    
                
def stand():
    # replace with your code below
    print "Stand:\n"
    global dealer, deck, busted, score
    global in_play
    if busted:
        print "You have busted"
        in_play = False
        score -=1
    else:
        while (dealer.get_value() < 17):
            hit(False)
        
        if (dealer.get_value > 21):
            print "Dealer is busted"
            in_play = False
            score += 1
        elif(player.get_value() > dealer.get_value()):
            print "Player wins!"
            in_play = False
            score += 1
        else:
            print "Dealer wins!"
            score -=1
            in_play = False
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    print "Dealer :"
    print dealer
    print "Player :"
    print player
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player, dealer, score, outcome
    card = Card("S", "A")
    canvas.draw_text ("Black Jack",[270,50],30,"Red")
    canvas.draw_text ("Score : "+str(score),[470,50],30,"Red")
    canvas.draw_text(outcome, [270, 90],30 ,"Blue")
    dealer.draw(canvas,[100,100])
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [65 + CARD_CENTER[0], 100 + CARD_CENTER[1]], CARD_SIZE)
    else :
        dealer.draw(canvas,[100,100])
    player.draw(canvas,[100,300])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric