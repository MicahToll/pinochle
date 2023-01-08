import random

class Card:

    def __init__(self, suit, rank, order):
        self._suit = suit
        self._rank = rank
        self._order = order #H=0, S=1, D=2, C=3

    def getSortOrder(self):
        return self._order

    def getCard(self):
        return (self._suit, self._rank)

class Deck:

    def __init__(self):
        ranks = ["A", "10", "K", "Q", "J", "9"]
        suits = ["hearts", "spades", "diamonds", "clubs"]
        self._deck = []
        for suit in suits:
            for rank in ranks:
                order = suits.index(suit)*10 + ranks.index(rank)
                self._deck.append(Card(suit, rank, order))
                self._deck.append(Card(suit, rank, order))

    def shuffle(self):
        random.shuffle(self._deck)

    def takeTopCard(self):
        top = self._deck[len(self._deck)-1]
        self._deck.remove(top)
        return top

class Player:

    def __init__(self, name):
        self._name = name
        self._hand = []
        self._bid = ""

    def getName(self):
        return self._name

    def fillHand(self, card):
        self._hand.append(card)
        self.sortHand()

    def getHand(self):
        return self._hand

    def sorting(self, card):
        return card.getSortOrder()

    def sortHand(self):
        self._hand.sort(key=self.sorting)

    def askBid(self, currentBid, first):
        if self.getBid() == "Pass":
            return
        bid = input(self.getName() + ", enter bid:")
        if bid == "Pass":
            self._bid = "Pass"
        elif bid == "Bid or Bunch":
            if first is True and currentBid == 240:
                self._bid = "Bid or Bunch"
            else:
                print(self.getName() + ", enter appropriate bid")
                self.askBid(currentBid, first)
        else:
            try:
                int(bid)
            except ValueError:
                print(self.getName() + ", enter integer bid")
                self.askBid(currentBid, first)
            bid = int(bid)
            if bid % 10 != 0:
                print(self.getName() + ", enter appropriate integer bid")
                self.askBid(currentBid, first)
            if bid <= currentBid:
                print(self.getName() + ", enter larger bid")
                self.askBid(currentBid, first)
            self._bid = bid

    def getBid(self):
        return self._bid

class Team:

    def __init__(self, player1, player2):
        self._p1 = player1
        self._p2 = player2

class Pinochle:

    def __init__(self, players):
        self._p1 = Player(players[0])
        self._p2 = Player(players[1])
        self._p3 = Player(players[2])
        self._p4 = Player(players[3])
        self._allPlayers = [self._p1, self._p2, self._p3, self._p4]
        self._team1 = Team(self._p1, self._p2)
        self._team2 = Team(self._p3, self._p4)
        self._deck = Deck()
        self._deck.shuffle()

    def deal(self):
        for index in range(12):
            for player in self._allPlayers:
                player.fillHand(self._deck.takeTopCard())

    def getPlayer(self, playerName):
        for player in self._allPlayers:
            if player.getName() == playerName:
                return player

    def showHand(self, playerName):
        player = self.getPlayer(playerName)
        for card in player.getHand():
            print(card.getCard())

    def bidding(self):
        passed = 0
        currentBid = 240
        biddingPlayers = self._allPlayers
        first = True
        while passed < 3:
            for player in biddingPlayers.copy():
                player.askBid(currentBid, first)
                if player.getBid() == "Pass":
                    passed += 1
                    if passed == 4 and first == True:
                        break
                    biddingPlayers.remove(player)
                    if passed >= 3 and first == False:
                        break
                else:
                    if type(player.getBid()) is int:
                        currentBid = player.getBid()
            else:
                first = False
                continue
            break

        finalBid = biddingPlayers[0].getBid()
        if finalBid == "Pass":
            print("No bids, reshuffle?")
        else:
            print("Final bid: " + str(finalBid) + ", " + biddingPlayers[0].getName())


if __name__ == '__main__':
    players = ["Lizzy", "Micah", "Dad", "Mom"]
    myGame = Pinochle(players)
    myGame.deal()
    myGame.showHand("Lizzy")
    myGame.bidding()

