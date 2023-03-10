import random
from enum import Enum

class Card:

    def __init__(self, suit, rank, player=False):
        self._suit = suit
        self._rank = rank
        self._player = player
        self._cardFront
        self._cardBack

        for card in CardSVGs:
            if self._suit.name in card:
                if self._rank.name in card:
                    self._cardFront = card
                    break

    def printCardFront(self):
        img = mpimg.imread(self._cardFront)
        imgplot = plt.imshow(img)
        plt.show()

    def setPlayer(self, player):
        self._player = player

    def getPlayer(self):
        return self._player

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
        return self._suit.value + self._rank.value

    def isCounter(self):
        if self._rank == Ranks.ACE or self._rank == Ranks.TEN or self._rank == Ranks.KING:
            return True
        else:
            return False

    def getRankNum(self):
        switcher = {
            Ranks.ACE: 6,
            Ranks.TEN: 5,
            Ranks.KING: 4,
            Ranks.QUEEN: 3,
            Ranks.JACK: 2,
            Ranks.NINE: 1
        }
        return switcher.get(self._rank)

def getRankNum(rank):
    switcher = {
        Ranks.ACE : 6,
        Ranks.TEN : 5,
        Ranks.KING : 4,
        Ranks.QUEEN : 3,
        Ranks.JACK : 2,
        Ranks.NINE : 1
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
    SPADES = 'S'
    CLUBS = 'C'
    DIAMONDS = 'D'
    HEARTS = 'H'

class CardSVGs(Enum):
    CLUBS_ACE = 'CLUB-1-ACE.svg'
    CLUBS_NINE = 'CLUB-9-NINE.svg'
    CLUBS_TEN = 'CLUB-10-TEN.svg'
    CLUBS_JACK = 'CLUB-11-JACK.svg'
    CLUBS_QUEEN = 'CLUB-12-QUEEN.svg'
    CLUBS_KING = 'CLUB-13-KING.svg'
    DIAMONDS_ACE = 'DIAMOND-1-ACE.svg'
    DIAMONDS_NINE = 'DIAMOND-9-NINE.svg'
    DIAMONDS_TEN = 'DIAMOND-10-TEN.svg'
    DIAMONDS_JACK = 'DIAMOND-11-JACK.svg'
    DIAMONDS_QUEEN = 'DIAMOND-12-QUEEN.svg'
    DIAMONDS_KING = 'DIAMOND-13-KING.svg'
    HEARTS_ACE = 'HEART-1-ACE.svg'
    HEARTS_NINE = 'HEART-9-NINE.svg'
    HEARTS_TEN = 'HEART-10-TEN.svg'
    HEARTS_JACK = 'HEART-11-JACK.svg'
    HEARTS_QUEEN = 'HEART-12-QUEEN.svg'
    HEARTS_KING = 'HEART-13-KING.svg'
    SPADES_ACE = 'SPADES-1-ACE.svg'
    SPADES_NINE = 'SPADES-9-NINE.svg'
    SPADES_TEN = 'SPADES-10-TEN.svg'
    SPADES_JACK = 'SPADES-11-JACK.svg'
    SPADES_QUEEN = 'SPADES-12-QUEEN.svg'
    SPADES_KING = 'SPADES-13-KING.svg'

class NoNumberBid(Enum):
    PASS = 'pass'
    BID_OR_BUNCH = "bid or bunch"

def getSuitEnum(str):
    for suit in Suits:
        if str == suit.value:
            return suit

def getRankEnum(str):
    for rank in Ranks:
        if str == rank.value:
            return rank

class Deck:

    def __init__(self):
        self._deck = []
        for suit in Suits:
            for rank in Ranks:
                self._deck.append(Card(suit, rank))
                self._deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self._deck)

    def takeTopCard(self):
        top = self._deck[len(self._deck)-1]
        self._deck.remove(top)
        return top

class Player:

    def __init__(self, name=""):
        self._name = name
        self._hand = []
        self._bid = ""
        self._meld = 0

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

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

    def printHandFront(self):
        for card in self._hand:
            card.printCardFront()

    def sorting(self, card):
        key = card.getSimpleCard()
        return key[0] + str(card.getRankNum())

    def sortHand(self):
        self._hand.sort(key=self.sorting, reverse=True)

    def askBid(self, currentBid, first):
        if self.getBid() == NoNumberBid.PASS:
            return
        bid = input(self.getName() + ", enter bid:")
        bid = bid.lower()
        for b in NoNumberBid:
            if b.value == bid:
                bid = b
        if bid == NoNumberBid.PASS:
            self._bid = bid
        elif bid == NoNumberBid.BID_OR_BUNCH:
            if first is True and currentBid == 240:
                self._bid = bid
            else:
                print(self.getName() + ", enter appropriate bid")
                self.askBid(currentBid, first)
                return
        else:
            try:
                bid = int(bid)
            except ValueError:
                print(self.getName() + ", enter integer bid")
                self.askBid(currentBid, first)
                return
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

    def askTrick(self, trickRound, trump):
        leadingTrick = trickRound.isLeadingCard()

        trickSimple = input(self.getName() + ", play trick:").upper()
        trick = Card(getSuitEnum(trickSimple[0]), getRankEnum(trickSimple[1:]), self)
        for card in self._hand:
            if card.isEqual(trick):
                if leadingTrick:
                    return card
                else:
                    firstSuit = trickRound.getFirstCard().getSuit()
                    winner = trickRound.getWinningCard(trump)
                if not self.outOfSuit(firstSuit):
                    winner = trickRound.getWinningCard(trump, True)
                    if trick.getSuit() != firstSuit:
                        print(self.getName() + ", enter card in suit")
                        return
                    elif self.canBeat(firstSuit, winner.getRankNum()):
                        if trick.getRankNum() > winner.getRankNum():
                            return card
                        else:
                            print(self.getName() + ", enter appropriate card. You must win the trick if you can.")
                            return
                    else:
                        return card
                elif not self.outOfSuit(trump):
                    if winner.getSuit() != trump:
                        if trick.getSuit() == trump:
                            return card
                        else:
                            print(self.getName() + ", enter trump card. You must win the trick if you can.")
                            return
                    elif self.canBeat(winner.getSuit(), winner.getRankNum()):
                        if trick.getSuit() == trump and trick.getRankNum() > winner.getRankNum():
                            return card
                        else:
                            print(self.getName() + ", enter trump card. You must win the trick if you can.")
                            return
                    else:
                        return card
                else:
                    return card
        print(self.getName() + ", enter trick card from hand")
        return

    def getBid(self):
        return self._bid

    def getMeld(self):
        return self._meld

    def scoreGroups(self, group, score, doubleScore):
        tempHand = self.getSimpleHand()
        if set(group).issubset(tempHand):
            for card in group:
                tempHand.remove(card)
            if set(group).issubset(tempHand):
                self._meld += doubleScore
            else:
                self._meld += score

    def scoreHand(self, trump):
        fiveNinesNoMeldCheck = False
        if trump is None:
            fiveNinesNoMeldCheck = True

        acesAround = []
        kingsAround = []
        queensAround = []
        jacksAround = []
        for s in Suits:
            acesAround.append(s.value + 'A')
            kingsAround.append(s.value + 'K')
            queensAround.append(s.value + 'Q')
            jacksAround.append(s.value + 'J')

        pinochle = [Suits.SPADES.value + "Q", Suits.DIAMONDS.value + "J"]

        self.scoreGroups(acesAround, 100, 1000)
        self.scoreGroups(kingsAround, 80, 800)
        self.scoreGroups(queensAround, 60, 600)
        self.scoreGroups(jacksAround, 40, 400)

        self.scoreGroups(pinochle, 40, 300)

        for suit in Suits:
            if not fiveNinesNoMeldCheck and suit != trump:
                marriage = [suit.value + "K", suit.value + "Q"]
                self.scoreGroups(marriage, 20, 40)
            else:
                marriage = [suit.value + "K", suit.value + "Q"]
                self.scoreGroups(marriage, 20, 40)

        if not fiveNinesNoMeldCheck:
            run = [trump.value + "A", trump.value + "10", trump.value + "K", trump.value + "Q", trump.value + "J"]
            royalMarriage = [trump.value + "K", trump.value + "Q"]
            royalHalfMarriageA = [trump.value + "A", trump.value + "10", trump.value + "K", trump.value + "K", trump.value + "Q", trump.value + "J"]
            royalHalfMarriageB = [trump.value + "A", trump.value + "10", trump.value + "K", trump.value + "Q", trump.value + "Q", trump.value + "J"]
            nine = [trump.value + "9"]

            if set(run).issubset(self.getSimpleHand()):
                self.scoreGroups(run, 150, 1500)
                if set(royalHalfMarriageA).issubset(self.getSimpleHand()):
                    self._meld += 20
                if set(royalHalfMarriageB).issubset(self.getSimpleHand()):
                    self._meld += 20
            elif set(royalMarriage).issubset(self.getSimpleHand()):
                self.scoreGroups(royalMarriage, 40, 80)

            self.scoreGroups(nine, 10, 20)
            print(self.getName() + "'s meld: " + str(self._meld))

    def loadMeldPoints(self):
        tempMeld = self._meld
        self._meld = 0
        return tempMeld

    def is5NinesNoMeld(self):
        nines = 0
        for card in self._hand:
            if card.getRankNum() == 1:
                nines += 1
        if nines < 5:
            return False
        else:
            self.scoreHand(None)
            if self._meld == 0:
                return True
            else:
                return False

class Team:

    def __init__(self, player1, player2, name):
        self._p1 = player1
        self._p2 = player2
        self._name = name
        self._score = 0
        self._roundScore = 0

    def isOnTeam(self, player):
        if player == self._p1 or player == self._p2:
            return True
        else:
            return False

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

    def addScore(self, score, newRound=False):
        if not newRound:
            self._roundScore += score
        else:
            self._score += score

    def getScore(self):
        return self._score

    def getRoundScore(self):
        return self._roundScore

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

class Game:

    def __init__(self, players=['', '', '', '']):
        self._p1 = Player(players[0])
        self._p2 = Player(players[1])
        self._p3 = Player(players[2])
        self._p4 = Player(players[3])
        self._allPlayers = [self._p1, self._p2, self._p3, self._p4]
        self._team1 = Team(self._p1, self._p3, "Team 1")
        self._team2 = Team(self._p2, self._p4, "Team 2")
        self._allTeams = [self._team1, self._team2]
        self._gameOver = False

    def askTeamNames(self):
        for team in self._allTeams:
            players = ""
            for player in team.getPartners():
                players += player.getName() + " and "
            players = players.removesuffix(' and ')
            name = input(players + " team name: ")
            team.setName(name)

    def askPlayerNames(self):
        for player in self._allPlayers:
            name = input("Player " + str(self._allPlayers.index(player) + 1) + " name: ")
            player.setName(name)

    def getAllPlayers(self):
        return self._allPlayers

    def getPlayers(self, number): #number is 1-4
        return self._allPlayers[number - 1]

    def getAllTeams(self):
        return self._allTeams

    def getTeams(self, number): # number is 1-2
        return self._allTeams[number-1]

    def showScores(self):
        print("Scores")
        print(self._team1.getName() + ": " + str(self._team1.getScore()))
        print(self._team2.getName() + ": " + str(self._team2.getScore()))

    def gameOver(self):
        self._gameOver = True

    def isGameOver(self):
        return self._gameOver

    def playRound(self):
        round = PinochleRound(self)
        round.deal()
        round.showAllHands()
        round.bidding()
        round.passingCards()
        round.scoreMeld()
        round.trickPlaying()
        round.finishRound()


class Tricks:

    def __init__(self):
        self._cardsPlayed = []
        self._winningcard = None
        self._leadingCard = True

    def playCard(self, card):
        self._cardsPlayed.append(card)
        self._leadingCard = False

    def isLeadingCard(self):
        return self._leadingCard

    def isDone(self):
        if len(self._cardsPlayed) >= 4:
            return True
        else:
            return False

    def getFirstCard(self):
        if not self._leadingCard:
            return self._cardsPlayed[0]
        else:
            return None

    def getWinningCard(self, trump, ignoreTrump=False):
        winRank = 0
        winSuit = self._cardsPlayed[0].getSuit()
        winningCard = None
        for card in self._cardsPlayed:
            if card.getSuit() == winSuit:
                if card.getRankNum() > winRank:
                    winRank = card.getRankNum()
                    winningCard = card
            elif card.getSuit() == trump:
                if not ignoreTrump:
                    winSuit = trump
                    winRank = card.getRankNum()
                    winningCard = card
        return winningCard

    def getCounters(self):
        counters = 0
        for card in self._cardsPlayed:
            if card.isCounter():
                counters += 10
        return counters


class PinochleRound:

    def __init__(self, game):
        self._allPlayers = game.getAllPlayers()
        self._team1 = game.getTeams(1)
        self._team2 = game.getTeams(2)
        self._deck = Deck()
        self._deck.shuffle()
        self._trump = False
        self._finalBid = 0
        self._tookBid = False
        self._shootMoon = False
        self._game = game

    def deal(self):
        for index in range(12):
            for player in self._allPlayers:
                card = self._deck.takeTopCard()
                player.fillHand(card)
                card.setPlayer(player)

    def dealRigged(self):
        for index in range(12):
            for player in self._allPlayers:
                if self._allPlayers.index(player) == 3:
                    card = Card(Suits.SPADES, Ranks.NINE, player)
                else:
                    card = self._deck.takeTopCard()
                player.fillHand(card)
                card.setPlayer(player)

    def reshuffle(self):
        for player in self._allPlayers:
            hand = player.getHand().copy()
            for index in range(len(hand)):
                player.removeCard(hand[index])
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

    def getOtherTeam(self, player):
        if player in self._team1.getPartners():
            return self._team2
        else:
            return self._team1

    def addScore(self, score, player):
        team = self.getTeam(player)
     #   if team == self.getTeam(self._tookBid):
     #       self._biddersScore += score
        team.addScore(score)

    def showHand(self, player):
        print(player.getName() + "'s hand:")
        #for card in player.getHand():
            #print(card.getCardNeat())
        player.printCardFront()

    def showAllHands(self):
        for player in self._allPlayers:
            self.showHand(player)

    def check5NinesNoMeld(self):
        for player in self._allPlayers:
            if player.is5NinesNoMeld():
                while True:
                    answer = input(player.getName() + ", do you want to throw with 5 nines no meld?").upper()
                    if answer == "YES":
                        print(player.getName() + " had 5 nines no meld. Reshuffling and dealing")
                        self.reshuffle()
                        self.deal()
                        self.showAllHands()
                        self.check5NinesNoMeld()
                        break
                    elif answer == "NO":
                        return
                    else:
                        print("Answer with yes or no")

    def bidding(self):
        self.check5NinesNoMeld()
        passed = 0
        currentBid = 240
        for player in self._allPlayers:
            player.resetBid()
        biddingPlayers = self._allPlayers.copy()
        first = True
        while passed < 3:
            for player in biddingPlayers.copy():
                player.askBid(currentBid, first)
                if player.getBid() == NoNumberBid.PASS:
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
        if finalBid == NoNumberBid.PASS:
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
                trump = trump.upper()
                for suit in Suits:
                    if trump == suit.name:
                        self._trump = suit
                if self._trump in list(Suits):
                    break

    def pass4Cards(self, playerPassing):
        recieving = self.getTeam(playerPassing).getPartnerOf(playerPassing)
        counter = 1
        self.showHand(playerPassing)
        message = playerPassing.getName() + ", pass card " + str(counter) + ":"
        while counter < 5:
            cardToPassSimple = input(message).upper()
            cardToPass = playerPassing.getCardFromSimple(cardToPassSimple)
            if playerPassing.isInHand(cardToPass):
                recieving.fillHand(cardToPass)
                playerPassing.removeCard(cardToPass)
                counter += 1
                message = playerPassing.getName() + ", pass card " + str(counter) + ":"
            else:
                message = 'Card not in hand. ' + playerPassing.getName() + ", pass card " + str(counter) + ":"

    def passingCards(self):
        player = self._tookBid
        team = self.getTeam(player)
        partner = team.getPartnerOf(player)

        self.pass4Cards(partner)
        self.pass4Cards(player)

    def scoreMeld(self):
        for player in self._allPlayers:
            player.scoreHand(self._trump)

        self.askShootMoon()

        if not self.canMakeBid() and not self._shootMoon:
            self.throwIn()
            return

        for player in self._allPlayers:
            if self._shootMoon:
                if self.getTeam(player) != self.getTeam(self._tookBid):
                    self.addScore(player.loadMeldPoints(), player)
            else:
                self.addScore(player.loadMeldPoints(), player)

    def canMakeBid(self):
        meld = self._tookBid.getMeld() + self.getTeam(self._tookBid).getPartnerOf(self._tookBid).getMeld()
        if meld + 250 < self._finalBid:
            return False
        else:
            return True

    def askShootMoon(self):
        while True:
            answer = input(self._tookBid.getName() + ", do you want to shoot the moon?").upper()
            if answer == "YES":
                print(self._tookBid.getName() + " is shooting the moon")
                self._shootMoon = True
                return
            elif answer == "NO":
                self._shootMoon = False
                return
            else:
                print("Answer with yes or no")

    def getNextPlayer(self, currentPlayer):
        for player in self._allPlayers:
            if player == currentPlayer:
                index = self._allPlayers.index(player)
                return self._allPlayers[(index +  1)%4]

    def trickPlaying(self):
        nextPlayer = self._tookBid
        round = 1
        trickCards = Tricks()
        while round < 13:
            for player in self._allPlayers:
                if trickCards.isDone():
                    counters = trickCards.getCounters()
                    if round == 12:
                        counters += 10
                    winCard = trickCards.getWinningCard(self._trump)
                    self.addScore(counters, winCard.getPlayer())
                    self._game.showScores()
                    trickCards = Tricks()
                    nextPlayer = winCard.getPlayer()
                    round += 1
                    break
                if player == nextPlayer:
                    self.showHand(player)
                    trick = None
                    while trick is None:
                        trick = player.askTrick(trickCards, self._trump)
                    player.removeCard(trick)
                    trickCards.playCard(trick)
                    nextPlayer = self.getNextPlayer(player)

    def madeBid(self):
        if self._shootMoon:
            self._finalBid = 250

        if self.getTeam(self._tookBid).getRoundScore() >= self._finalBid:
            return True
        else:
            if self._shootMoon:
                self._finalBid = 500
            return False

    def finishRound(self):
        biddingTeam = self.getTeam(self._tookBid)
        otherTeam = self.getOtherTeam(self._tookBid)
        print(biddingTeam.getName(), " bid: ", self._finalBid)

        if self.madeBid():
            score = biddingTeam.getRoundScore()
            if self._shootMoon:
                score = 500
            biddingTeam.addScore(score, True)
            print(biddingTeam.getName(), "made bid!")
            print(biddingTeam.getName(), "scored:", score)
        else:
            biddingTeam.addScore(-self._finalBid, True)
            print(biddingTeam.getName(), "did not make the bid! :(")
            print(biddingTeam.getName(), "scored:", -self._finalBid)

        score = otherTeam.getRoundScore()
        otherTeam.addScore(score, True)
        print(otherTeam.getName(), " scored: ", score)

        winner = self.winner()
        if winner is not Null:
            print(winner.getName(), " wins!!")
            self._game.showScores()

    def winner(self): #Null is no winner yet
        t1Score = self._team1.getScore()
        t2Score = self._team2.getScore()

        if t1Score < 1500 and t1Score > -1500 and t2Score < 1500 and t2Score > -1500:
            return Null
        elif t1Score >= 1500 and t2Score < t1Score:
            return self._team1
        elif t2Score >= 1500 and t1Score < t2Score:
            return self._team2
        elif t1Score <= -1500 and t2Score > t1Score:
            return self._team2
        elif t2Score <= -1500 and t1Score > t2Score:
            return self._team1
        else:
            return Null


if __name__ == '__main__':
    players = ["Lizzy", "Micah", "Dad", "Mom"]
    myGame = Game(players)
    myGame.showScores()
  #  myGame.askPlayerNames()
  #  myGame.askTeamNames()
    myGame.playRound()

