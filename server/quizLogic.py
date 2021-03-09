import json
#Player: stores info about a twitch user
class Player:
    def __init__(self, username):
        self.username = username
        self.userID = 0

    def getUserName(self):
        pass

    def getUserID(self):
        pass

#Lobby: Obj to Store players in a game lobby + add/delete players
class Lobby:
    def __init__(self):
        #key:value = username:playerInstance
        self.lobby = {}

    # Adds player to dictionary of players in lobby
    def addPlayer(self, username):
        #checks if user not allready in lobby (want code here as will be useful to check whenever adding new players)
        if (not(username in self.lobby)):
            self.lobby[username] = Player(username)
            print(username + " has joined the lobby")

    # Removes player from lobby (e.g. incorrect answer)
    def removePlayer(self, player):
        pass

    #returns true if player in lobby
    def playerInLobby(self, username):
        if (username in self.lobby):
            return True
        return False

    def getLobby(self):
        return self.lobby

#stores one instance of a question 
class Question:

    def __init__(self, questionString, optionTuple, correctAnswer):
        self.questionDict = {"question":questionString,
                            "optionA": optionTuple[0],
                            "optionB": optionTuple[1],
                            "optionC": optionTuple[2],
                            "optionD": optionTuple[3],
                            "correctAnswer": correctAnswer}
        
    def getQuestionString(self):
        return self.questionDict["question"]

    def getOptions(self):
        return self.questionDict["optionA"] + " " + self.questionDict["optionB"] + " " + self.questionDict["optionC"] + " " + self.questionDict["optionD"]

    def getCorrectAnswer(self):
        return self.questionDict["correctAnswer"]

    def getQuestionDict(self):
        return self.questionDict

#stores set of questions + ability to iterate throught the questions
class Questions:
    def __init__(self):
        self.questionList = []
        self.questionCount = 0

    def testPopuateQuestions(self):
        self.questionList.append(Question("what is the capital of England", ("London", "Manchester", "England", "Brighton"), 'A'))
        self.questionList.append(Question("what is the capital of London", ("London", "Manchester", "England", "Brighton"), 'C'))
        self.questionList.append(("Where is London", ("London", "Manchester", "England", "Brighton"), 'A'))

    #gets next question from list of questions
    def getNextQuestion(self):
        nextQuestion = self.questionList[self.questionCount]
        self.questionCount += 1
        return nextQuestion

    def lastQuestion(self):
        if self.questionCount >= len(self.questionList)-1 :
            return true
        return false


#deals with game logic + dealing with twitch messages
class QuizLogic:
    def __init__(self):
        #stores current game state e.g. players joining/answer question/doing nothing
        #can check this var whenever msg comes in to determine what to do with it
        self.gameState = "join" 
        self.gameLobby = Lobby()
        self.winnerLobby = Lobby()
        self.currentQuestion = None
        self.callb = None
        self.socket_id = None

    def makeReturnMessage(self,command,message):
        m = {
            "command": command,
            "socketid": self.socket_id,
            "payload": message
        }
        x = json.dumps(m)
        return x

    def setSocketCallback(self, callback, socketID):
        self.callb = callback
        self.socket_id = socketID

    def sendSocketMessage(self, command, message):
        if self.callb:
            #message["socketid"] =  self.socket_id
            x = self.makeReturnMessage(command,message)
            self.callb(x, self.socket_id)

    #params: message (message from chat collected by twitchbot)
    #process: called whenever message sent in chat, processes message into game logic
    #returns: json storing info e.g. {join, name : username}
    def recieveCommand(self, username, message):
        rs = None

        #if players currently joining state
        if self.gameState == "join":
            #USING REGULAR EXPRESSION IN FUTURE
            if message == "join":
                # add player to lobby (checks done in lobby)
                self.gameLobby.addPlayer(username)
                #self.sendSocketMessage("join", {"name" : username})
                rs = self.makeReturnMessage("join", {"name" : username})

            elif message == "start":
                self.startGame()
        elif self.gameState == "answers":
            #if correct answer for current question AND player is still in the lobby
            if message == self.currentQuestion.getCorrectAnswer() and self.gameLobby.playerInLobby(username):
                #add to next round lobby
                self.winnerLobby.addPlayer(username)
                print("Correct Answer!!")
                print(self.winnerLobby.getLobby())
            else:
                print("incorrect!!")

        return rs

    def recieveWebSocketCommand(self, data):
        rs = None
        if data['command'] == 'start':
            rs = self.startGame()
        return rs

    #called when first start game
    def startGame(self):
        self.gameState = "answers"

        questions = Questions()
        questions.testPopuateQuestions()
        self.currentQuestion = questions.getNextQuestion()

        print(self.currentQuestion.getQuestionString())
        print(self.currentQuestion.getOptions())

        return self.makeReturnMessage("question", self.currentQuestion.getQuestionDict())


        #enter main question loop sequence

    def questionSequence(self):
        pass


