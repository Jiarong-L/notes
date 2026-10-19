import turtle
import random
import time


class Block(turtle.Turtle):              # A single turtle to be added or deleted
    def __init__(self):
        super().__init__()
        self.penup()
        self.ht()
        self.shape('square')
        self.shapesize(4, 4, 8)

    def show_block(self,pos,val):
        self.goto(pos)
        self.color('Cornsilk')
        self.stamp()
        self.color('Black')
        self.text_val = val
        self.write('{}'.format(self.text_val),align='center',font = 30)


class Game(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.ht()
        self.shape('square')
        self.shapesize(4, 4, 8)
        self.all_pos = [(-150+100*i,50-100*j) for i in range(4) for j in range(4)]

        self.avail_pos_idx = [i for i in range(len(self.all_pos))]          # index of all_pos
        self.block_pos_idx = []                                             # index of all_pos, for shown blocks
        self.block = []                                                     # a list of shown blocks turtles

        self.show_background()
        self.emerge_block()

        self.max_score = 2              # init as 2, increase by merging
        
    
    def show_background(self): 
        for pos in self.all_pos:
            self.goto(pos)
            self.color('Moccasin') 
            self.stamp()

    def add_block(self,pos_idx,text_val): 
        temp_block = Block()
        temp_block.show_block(self.all_pos[pos_idx],text_val)
        self.block.append(temp_block)
        self.block_pos_idx.append(pos_idx)        
        self.avail_pos_idx.remove(pos_idx)

    def remove_block(self, pos_idx):   ##pos_idx = self.all_pos.index(pos)
        temp_block = self.block[self.block_pos_idx.index(pos_idx)]
        temp_block.clear()

        self.avail_pos_idx.append(pos_idx)
        self.block_pos_idx.remove(pos_idx)
        self.block.remove(temp_block)

    def move_block(self,from_pos_idx,to_pos_idx):               # A single move with 3 possible reaults
        from_text_val = self.block[self.block_pos_idx.index(from_pos_idx)].text_val
        return_val = 1                                          # move but not merge
        if to_pos_idx in self.avail_pos_idx:
            to_text_val = from_text_val
        else:
            temp_text_val = self.block[self.block_pos_idx.index(to_pos_idx)].text_val
            if temp_text_val != from_text_val:
                to_text_val = -1
                return 0                                        # cannot move
            else:
                to_text_val = from_text_val + temp_text_val
                self.remove_block(to_pos_idx)
                return_val = 2                                  # merge

        self.remove_block(from_pos_idx)
        self.add_block(to_pos_idx,to_text_val)
        self.max_score = max(self.max_score,to_text_val)
        return return_val

    def emerge_block(self):                         # Random new block
        text_val = 2
        pos_idx = random.choice(self.avail_pos_idx)
        self.add_block(pos_idx,text_val)
        return 1

    def to_direction(self, direction):                                      # An act, see notes
        ordered_pos_idx = [i for i in self.block_pos_idx]

        if direction in ['Up','Left']:
            ordered_pos_idx.sort()
            update_sig = -1
        elif direction in ['Down','Right']:  
            ordered_pos_idx.sort(reverse = True)   
            update_sig = 1         

        for temp_idx in ordered_pos_idx:

            if direction in ['Up','Down']:
                min_E = (temp_idx // 4 ) * 4
                max_E = (temp_idx // 4 ) * 4 +3
                update_scale = update_sig * 1
            elif direction in ['Left','Right']:
                min_E = 0
                max_E = 15
                update_scale = update_sig * 4

            can_move = 1
            temp_to_idx = temp_idx + update_scale
            temp_from_idx = temp_idx
            while ( (temp_to_idx >= min_E)  & (temp_to_idx <= max_E)  & (can_move == 1) ):      # 1. within (min_E,max_E)    
                can_move = self.move_block(temp_from_idx,temp_to_idx)                           # 2. if merged / cannot move; stop
                # time.sleep(0.2)
                temp_from_idx = temp_to_idx
                temp_to_idx = temp_to_idx + update_scale

        self.win_lose()                                                       # check win/lose by every act

        if set(ordered_pos_idx) != set(self.block_pos_idx):                 # if some position change, add new block
            self.emerge_block()


    def Up(self):
        self.to_direction('Up')
    def Down(self):
        self.to_direction('Down')
    def Left(self):
        self.to_direction('Left')           
    def Right(self):
        self.to_direction('Right')

    def win_lose(self):
        self.goto((0,200))
        self.color('Red')
        if self.max_score >= 2048:
            self.write('Win',align='center',font = 80)
        else:
            if self.avail_pos_idx == []:
                check_lose = True
                for temp_pos_idx in [ (i+4*j) for i in range(4-1) for j in range(4-1)]:
                    t_val = self.block[self.block_pos_idx.index(temp_pos_idx)].text_val

                    if t_val == self.block[self.block_pos_idx.index(temp_pos_idx +1 )].text_val:
                        check_lose = False
                    elif t_val == self.block[self.block_pos_idx.index(temp_pos_idx +4 )].text_val:
                        check_lose = False
                    
                if check_lose == True:
                    self.write('You Lose',align='center',font = 80)


ms = turtle.Screen()
ms.setup(430,630)
ms.bgcolor('FloralWhite')
ms.title('2048')
ms.tracer(0)

bg = Game()

ms.listen()
ms.onkey(bg.Up, 'Up')
ms.onkey(bg.Down, 'Down')
ms.onkey(bg.Left, 'Left')
ms.onkey(bg.Right, 'Right')

while True:
    ms.update()

ms.mainloop()




