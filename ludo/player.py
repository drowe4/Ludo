from random import randint

class Player:

    def __init__(self, b, player_id): 
        self.player_id = player_id
        self.pieces = [Piece(player_id, i, b) for i in range(4)]


    def play(self, rolls):
        for roll in rolls:
            piece = self.pieces[randint(0,3)] # TODO: Choose the piece to be moved. It's randomized right now.
            if piece.in_prison():
                if roll == 6:
                    piece.move(1)
            else:
                piece.move(1)
                     
    def get_player_id(self):
        return self.player_id
    
    

class Step:
    
    
    def __init__(self, val=None):
        self.val = val
        self.next = None
    
    def look_forward(self, n):
        if n <= 0:
            return True
        elif not self.next:
            return False
        
        return self.next.look_forward(n-1)
    
    def journey(self):
        p = []
        s = self
        while s:
            p.append(s)
            s = s.next
        return p
        
    def __repr__(self):
        return self.val.__repr__()
    
	
class Piece:


    def __init__(self, owner_id, piece_id, b):
        self.owner_id = owner_id
        self.piece_id = piece_id
        self.board = b
        self.path = self.generate_path(b.player_count)
		
    def generate_path(self, player_count):
        i = 2 + self.owner_id * 13
        step = Step(self.board.board[0][self.owner_id][self.piece_id])
        step.val.contents = self
        start = step
        
        j = 2
        while j < (player_count) * 13:
            step.next = Step(self.board.board[1][i])
            step = step.next
            j += 1
            i = (i + 1) % ((player_count) * 13)
            
        j = 0
        while j < 5:
            step.next = Step(self.board.board[2][self.owner_id][j])
            step = step.next
            j += 1
        return start
        
    def in_prison(self):
        return self.path.val == self.board.board[0][self.owner_id][self.piece_id]
        
    def move(self, steps):
        start = self.path
        piece = self.path.val
        if self.path.look_forward(steps):
            for i in range(steps):
                self.path = self.path.next
        start.val.contents = self.__repr__()
        self.path.val.contents = piece
        
    def __repr__(self):
        return "({};{})".format(self.owner_id, self.piece_id)

    def __repr__1(self):
        return "'blah'"

		
class Die:


    def __init__(self, sides=6):
        self.sides = 6
        
    def get_rolls(self):
        rolls = []
        i = 0
        goes = 1
        while i < 3 and goes > 0:
            roll = randint(1,self.sides)
            rolls.append(roll)
            if roll == 6:
                goes += 1
            goes -= 1
            i += 1
        return rolls
        
        
class Board:


    def __init__(self, player_count):
        self.player_count = player_count
        self.board = self.make_board(player_count)

    def make_board(self, players):
        b = [[[Square("start_square") for i in range(4)] for j in range(players)]]
        
        b.append([Square("general_square") for i in range(13) for j in range(players)])

        b.append([[Square("end_squares") for i in range(5)] for j in range(players)])
        
        return b

    def display(self):
        for i in self.board:
            print (i)


class Square:


    def __init__(self, contents):
        self.contents = contents
        
    def __repr__(self):
        return self.contents.__repr__()
