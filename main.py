import random
from enum import Enum

class Card:

    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank

    def getCardNeat(self):
        return (self._suit.value, self._rank.value)

    def getSuit(self):
        return self._suit

    def getRankStr(self):
        return self._rank

    def isEqual(self, card):
        if self._suit == card._suit and self._rank == card._rank:
            return True
        else:
            return False

    def getSimpleCard(self):
        return self._suit.value[0] + self._rank.value

    def isCounter(self):
        if self._rank == Ranks.ACE or Ranks.TEN or Ranks.KING:
            return True
        else:
            return False

    def getRankNum(self):
        switcher = {
            'A' : 1,
            '10' : 2,
            'K' : 3,
            'Q' : 4,
            'J' : 5,
            '9' : 6
        }
        return switcher.get(self._rank.value)

def getRankNum(rank):
    if type(rank) is Ranks.ACE:
        rank = rank.value
    switcher = {
        'A' : 1,
        '10' : 2,
        'K' : 3,
        'Q' : 4,
        'J' : 5,
        '9' : 6
    }
    return switcher.get(rank)

class Ranks(Enum):
    ACE = 'A'
    TEN = '10'
    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    NINE = '9'

class Suits(Enum):
    SPADES = 's'
    CLUBS = 'c'
    DIAMONDS = 'd'
    HEARTS = 'h'


class Deck:

    def __init__(self):
        #ranks = [Ranks.ACE, Ranks.TEN, Ranks.KING, Ranks.QUEEN, Ranks.JACK, Ranks.NINE]
        self._suits = [Suits.SPADES, Suits.CLUBS, Suits.DIAMONDS, Suits.HEARTS]
        self._deck = []
        for suit in self._suits:
            for rank in Ranks:
                self._deck.append(Card(suit, rank))
                self._deck.append(Card(suit, rank))

    def getSuits(self):
        return self._suits

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
        self._meld = 0

    def getName(self):
        return self._name

    def getCardFromSimple(self, simpleCard):
        for card in self._hand:
            if card.getSimpleCard() == simpleCard:
                return card

    def resetBid(self):
        self._bid = ""

    def fillHand(self, card):
        self._hand.append(card)
        self.sortHand()

    def isInHand(self, card):
        for c in self._hand:
            if c == card:
                return True
        return False

    def removeCard(self, card):
        self._hand.remove(card)

    def getHand(self):
        return self._hand

    def getSimpleHand(self):
        simpleHand = []
        for card in self._hand:
            simpleHand.append(card.getSimpleCard())
        return simpleHand

    def sorting(self, card):
        key = card.getSimpleCard()
        return key[0] + str(card.getRankNum())

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
                return
        else:
            try:
                int(bid)
            except ValueError:
                print(self.getName() + ", enter integer bid")
                self.askBid(currentBid, first)
                return
            bid = int(bid)
            if bid % 10 != 0:
                print(self.getName() + ", enter appropriate integer bid")
                self.askBid(currentBid, first)
                return
            if bid <= currentBid:
                print(self.getName() + ", enter larger bid")
                self.askBid(currentBid, first)
                return
            self._bid = bid

    def outOfSuit(self, suit):
        for card in self._hand:
            if card.getSuit() == suit:
                return False
        return True

    def canBeat(self, suit, rank):
        for card in self._hand:
            if card.getSuit() == suit:
                if card.getRankNum() > rank:
                    return True
        return False

    def askTrick(self, currentTricks, winRank, winSuit, trump):
        if currentTricks == []:
            leadingTrick = True
        else:
            leadingTrick = False
            firstSuit,firstRank = currentTricks[0]
        trickSimple = input(self.getName() + ", play trick:")

        trick = Card(trickSimple, (trickSimple[1:]))
        print("hi")
        for card in self._hand:
            if card.getSimpleCard() == trick:
                print("1")
                if leadingTrick:
                    return trick
                if not self.outOfSuit(firstSuit):
                    print("2")
                    if self.canBeat(winRank):
                        print("3")
                        if trick[0] == firstSuit[0] and trick[1:] > winRank:
                            return trick
                        else:
                            print(self.getName() + ", enter appropriate trick")
                            self.askTrick(currentTricks, winRank, winSuit, trump)
                            return
                    else:
                        return trick
                elif not self.outOfSuit(trump):
                    if trick[0] == trump and trick[1:] > winRank or winSuit != trump[0]:
                        return trick
                    else:
                        print(self.getName() + ", enter appropriate trick")
                        self.askTrick(currentTricks, winRank, winSuit, trump)
                        return
                else:
                    return trick
        print(self.getName() + ", enter appropriate trick")
        self.askTrick(currentTricks, winRank, winSuit, trump)
        return

    def getBid(self):
        return self._bid

    def scoreGroups(self, group, score, doubleScore):
        tempHand = self.getSimpleHand()
        if set(group).issubset(tempHand):
            tempHand = set(tempHand) - set(group)
            if set(group).issubset(tempHand):
                self._meld += doubleScore
            else:
                self._meld += score

    def scoreHand(self, trump):
        acesAround = ["hA", "sA", "dA", "cA"]
        kingsAround = ["hK", "sK", "dK", "cK"]
        queensAround = ["hQ", "sQ", "dQ", "cQ"]
        jacksAround = ["hJ", "sJ", "dJ", "cJ"]

        run = [trump[0] + "A", trump[0] + "10", trump[0] + "K", trump[0] + "Q", trump[0] + "J"]
        royalMarriage = [trump[0] + "K", trump[0] + "Q"]
        royalHalfMarriageA = [trump[0] + "A", trump[0] + "10", trump[0] + "K", trump[0] + "K", trump[0] + "Q", trump[0] + "J"]
        royalHalfMarriageB = [trump[0] + "A", trump[0] + "10", trump[0] + "K", trump[0] + "Q", trump[0] + "Q", trump[0] + "J"]
        nine = [trump[0] + "9"]

        pinochle = ["sQ", "dJ"]

        ranks = ["A", "10", "K", "Q", "J", "9"]
        suits = ["hearts", "spades", "diamonds", "clubs"]

        self.scoreGroups(acesAround, 100, 1000)
        self.scoreGroups(kingsAround, 80, 800)
        self.scoreGroups(queensAround, 60, 600)
        self.scoreGroups(jacksAround, 40, 400)

        if set(run).issubset(self.getSimpleHand()):
            self.scoreGroups(run, 150, 1500)
            if set(royalHalfMarriageA).issubset(self.getSimpleHand()):
                self._meld += 20
            if set(royalHalfMarriageB).issubset(self.getSimpleHand()):
                self._meld += 20
        elif set(royalMarriage).issubset(self.getSimpleHand()):
            self.scoreGroups(royalMarriage, 40, 80)

        self.scoreGroups(nine, 10, 20)
        self.scoreGroups(pinochle, 40, 300)

        for suit in suits:
            if suit != trump:
                marriage = [suit[0] + "K", suit[0] + "Q"]
                self.scoreGroups(marriage, 20, 40)

        print(self.getName() + "'s meld: " + str(self._meld))

class Team:

    def __init__(self, player1, player2):
        self._p1 = player1
        self._p2 = player2
        self._score = 0

    def getPartners(self):
        return [self._p1, self._p2]

    def getPartner1(self):
        return self._p1

    def getPartner2(self):
        return self._p2

    def getPartnerOf(self, player):
        if player == self._p1:
            return self._p2
        else:
            return self._p1

    def addScore(self, score):
        self._score += score

    def getScore(self):
        return self._score

class Game:

    def __init__(self, players):
        self._p1 = Player(players[0])
        self._p2 = Player(players[1])
        self._p3 = Player(players[2])
        self._p4 = Player(players[3])
        self._allPlayers = [self._p1, self._p2, self._p3, self._p4]
        self._team1 = Team(self._p1, self._p3)
        self._team2 = Team(self._p2, self._p4)
        self._allTeams = [self._team1, self._team2]

    def getAllPlayers(self):
        return self._allPlayers

    def getPlayers(self, number): #number is 1-4
        return self._allPlayers[number - 1]

    def getAllTeams(self):
        return self._allTeams

    def getTeams(self, number): # number is 1-2
        return self._allTeams[number-1]

class PinochleRound:

    def __init__(self, game):
        self._allPlayers = game.getAllPlayers()
        self._team1 = game.getTeams(1)
        self._team2 = game.getTeams(2)
        self._deck = Deck()
        self._deck.shuffle()
        self._trump = False
        self._finalBid = False
        self._tookBid = False

    def deal(self):
        for index in range(12):
            for player in self._allPlayers:
                player.fillHand(self._deck.takeTopCard())

    def reshuffle(self):
        for player in self._allPlayers:
            for card in player.getHand():
                player.removeCard(card)
        self._deck = Deck()
        self._deck.shuffle()

    def getPlayer(self, playerName):
        for player in self._allPlayers:
            if player.getName() == playerName:
                return player

    def getTeam(self, player):
        if player in self._team1.getPartners():
            return self._team1
        else:
            return self._team2

    def addScore(self, score, player):
        team = self.getTeam(player)
        team.addScore(score)

    def showHand(self, playerName):
        player = self.getPlayer(playerName)
        print(playerName + "'s hand:")
        for card in player.getHand():
            print(card.getCardNeat())

    def bidding(self):
        passed = 0
        currentBid = 240
        for player in self._allPlayers:
            player.resetBid()
        biddingPlayers = self._allPlayers.copy()
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
            self.reshuffle()
            self.deal()
            self.bidding()
            return
        else:
            self._finalBid = finalBid
            self._tookBid = biddingPlayers[0]
            print("Final bid: " + str(finalBid) + ", " + biddingPlayers[0].getName())
            while True:
                trump = input(biddingPlayers[0].getName() + ", enter trump suit:")
                for suit in Suits:
                    if trump == suit.name:
                        self._trump = suit
                if self._trump in self._deck.getSuits():
                    break

    def pass4Cards(self, passing):
        recieving = self.getTeam(passing).getPartnerOf(passing)
        counter = 1
        message = passing.getName() + ", pass card " + str(counter) + ":"
        while counter < 5:
            cardToPassSimple = input(message)
            cardToPass = passing.getCardFromSimple(cardToPassSimple)
            if passing.isInHand(cardToPass):
                recieving.fillHand(cardToPass)
                passing.removeCard(cardToPass)
                counter += 1
                message = passing.getName() + ", pass card " + str(counter) + ":"
            else:
                message = 'Card not in hand. ' + passing.getName() + ", pass card " + str(counter) + ":"

    def passingCards(self):
        player = self._tookBid
        team = self.getTeam(player)
        partner = team.getPartnerOf(player)

        self.pass4Cards(partner)

        self.showHand("Dad")
        self.showHand("Lizzy")

        self.pass4Cards(player)

    def scoreMeld(self):
        for player in self._allPlayers:
            player.scoreHand(self._trump)

    def getNextPlayer(self, currentPlayer):
        for player in self._allPlayers:
            if player == currentPlayer:
                index = self._allPlayers.index(player)
                return self._allPlayers[(index +  1)%4]

    def trickPlaying(self):
        nextPlayer = self._tookBid
        round = 1
        trickCards = []
        winRank,winSuit,winPlayer = [0, 0, False]  # rank, suit, player
        while round < 13:
            for player in self._allPlayers:
                if player == nextPlayer:
                    trick = player.askTrick(trickCards, winRank, winSuit, self._trump)
                    if int(trick[1:]) > int(winRank):
                        winRank,winSuit,winPlayer = [trick[1:], trick[0], player]
                if len(trickCards) == 4:
                    counters = 0
                    for card,player in trickCards:
                        if card.isCounter():
                            counters += 10
                    self.addScore(counters, winPlayer)
                    trickCards = []
                    print(len(trickCards))
                    nextPlayer = winPlayer
                    round += 1



if __name__ == '__main__':
    for suit in Suits:
        print(suit.name)
    players = ["Lizzy", "Micah", "Dad", "Mom"]
    myGame = Game(players)
    round = PinochleRound(myGame)
    round.deal()
    round.showHand("Lizzy")
    round.showHand("Dad")
    round.showHand("Micah")
    round.showHand("Mom")
    round.bidding()
  #  round.passingCards()
    round.scoreMeld()
    round.trickPlaying()

