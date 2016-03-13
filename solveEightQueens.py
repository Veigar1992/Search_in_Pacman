import random
import copy
from optparse import OptionParser

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        solutionCounter = 0
        lectureCase = [[]]
        if lectureExample:
            lectureCase = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "q", ".", ".", ".", "."],
            ["q", ".", ".", ".", "q", ".", ".", "."],
            [".", "q", ".", ".", ".", "q", ".", "q"],
            [".", ".", "q", ".", ".", ".", "q", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ]
        for i in range(0,numberOfRuns):
            if self.search(Board(lectureCase), verbose).getNumberOfAttacks() == 0:
                solutionCounter+=1
        print "Solved:",solutionCounter,"/",numberOfRuns

    def search(self, board, verbose):
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print "iteration ",i
                print newBoard.toString()
                print newBoard.getCostBoard().toString()
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks) = newBoard.getBetterBoard()
            i+=1
#            if currentNumberOfAttacks <= newNumberOfAttacks:
            if newNumberOfAttacks == 0 or currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray
        self.queueAttack = [0]*8
#        print self.squareArray
    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [["." for i in range(0,8)] for j in range(0,8)]
        for i in range(0,8):
            tmpSquareArray[random.randint(0,7)][i] = "q"
        return tmpSquareArray
          
    def toString(self):
        s = ""
        for i in range(0,8):
            for j in range(0,8):
                s += str(self.squareArray[i][j]) + " "
            s += "\n"
        return s + "# attacks: "+str(self.getNumberOfAttacks())

    def getCostBoard(self):
        costBoard = copy.deepcopy(self)
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        #TODO: put your code here...
#        tmpBoard = copy.deepcopy(self)
        tmpBoard = self
        costBoard = tmpBoard.getCostBoard().squareArray
        minAttackNum = 1000000
#        tmpBoard.queueAttack = [8,7,6,5,4,3,2,1]
#        print "costBoard: \n", costBoard
        for r in range(0,8):
            for c in range(0,8):
                if costBoard[r][c] == "q": continue
                if costBoard[r][c] < minAttackNum:
                    minAttackNum = costBoard[r][c]
        maxAttacjNum = 0
        moveQueue = -1
        while True:
            for i in range(0,8):
                if tmpBoard.queueAttack[i] > maxAttacjNum:
                    moveQueue = i
                    maxAttacjNum = tmpBoard.queueAttack[i]
#            print moveQueue, maxAttacjNum, tmpBoard.queueAttack
            for i in range(0,8):
                if costBoard[i][moveQueue] == minAttackNum:
                    pos = 0
                    for k in range(0,8):
                        if costBoard[k][moveQueue]=="q":
                            pos = k
                    tmpBoard.squareArray[pos][moveQueue] = "."
                    tmpBoard.squareArray[i][moveQueue] = "q"
#                    print tmpBoard.squareArray
#                    print "#attack: ", minAttackNum
                    return (tmpBoard, minAttackNum)
            tmpBoard.queueAttack[moveQueue] = -1
            maxAttacjNum = -1
        return (tmpBoard, minAttackNum)

    def getNumberOfAttacks(self):
        #TODO: put your code here...
        self.queueAttack = [0]*8
        queuePos = []
        attackNum = 0
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    queuePos.append((r,c))
                if len(queuePos) == 8:
                    break
        for i in range(0,8):
            for j in range(i+1,8):
                qx, qy = queuePos[i], queuePos[j]
                if qx[0]== qy[0] or qx[1] == qy[1] or \
                        abs(qx[0]-qy[0]) == abs(qx[1]-qy[1]):
                            attackNum+=1
                            self.queueAttack[i] += 1
                            self.queueAttack[j] += 1
#        print queuePos
#        print "attack: " , attackNum
        return attackNum

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(0)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)