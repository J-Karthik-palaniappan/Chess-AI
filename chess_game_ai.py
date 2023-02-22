# THE CHESS GAME!!
import pygame,sys
import random
pygame.init()
pygame.display.set_caption("Chess")
size=100

class environment:
    def __init__(self):
        self.moves=[]
        self.castle=[1,1,1,1]
        self.enpassantable=None
        self.board = [['' for i in range(8)]for j in range(8)]
        self.board[0] = ['b_r','b_kn','b_b','b_q','b_k','b_b','b_kn','b_r']
        self.board[1] = ['b_p','b_p','b_p','b_p','b_p','b_p','b_p','b_p']
        self.board[7] = ['w_r','w_kn','w_b','w_q','w_k','w_b','w_kn','w_r']
        self.board[6] = ['w_p','w_p','w_p','w_p','w_p','w_p','w_p','w_p']
        self.pieces=pygame.sprite.Group()
        for i in range(8):
            self.pieces.add(Piece(self.board[0][i],0,i))
            self.pieces.add(Piece(self.board[7][i],7,i))
            self.pieces.add(Piece(self.board[1][i],1,i))
            self.pieces.add(Piece(self.board[6][i],6,i))
            
    def movements(self,i,attack=False): # main code where every piece's movements are calculated
        redbox=[]
        if(i.txt=="w_kn" or i.txt=="b_kn"): #knight's movement
            for j in [(2,1),(1,2),(-2,1),(1,-2),(2,-1),(-1,2),(-2,-1),(-1,-2)]:
                if(0<=i.r+j[0]<8 and 0<=i.c+j[1]<8 and (self.board[i.r+j[0]][i.c+j[1]]==''or self.board[i.r+j[0]][i.c+j[1]][0]!=i.txt[0])):
                    redbox.append((i.r+j[0],i.c+j[1]))
                    
        elif(i.txt=="b_k" or i.txt=="w_k"): #king's movement
            for j in [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
                if(0<=i.r+j[0]<8 and 0<=i.c+j[1]<8 and (self.board[i.r+j[0]][i.c+j[1]]=='' or self.board[i.r+j[0]][i.c+j[1]][0]!=i.txt[0])):
                    redbox.append((i.r+j[0],i.c+j[1]))
            if not attack: #casteling
                if(i.txt[0]=="w"):
                    if(self.castle[0]==1 and self.board[7][3]==self.board[7][2]==self.board[7][1]==''):
                        redbox.append((i.r,i.c-2))
                    if(self.castle[1]==1 and self.board[7][5]==self.board[7][6]==''):
                        redbox.append((i.r,i.c+2))
                else:
                    if(self.castle[2]==1 and self.board[0][3]==self.board[0][2]==self.board[0][1]==''):
                        redbox.append((i.r,i.c-2))
                    if(self.castle[3]==1 and self.board[0][5]==self.board[0][6]==''):
                        redbox.append((i.r,i.c+2))
            
        elif(i.txt=="w_p"): #white pawn's movement
            if(0<=i.r-1<8 and 0<=i.c+1<8 and (attack or (self.board[i.r-1][i.c+1]!='' and self.board[i.r-1][i.c+1][0]=='b') or (i.r==3 and self.enpassantable and self.enpassantable.c-1==i.c))):
                redbox.append((i.r-1,i.c+1))
            if(0<=i.r-1<8 and 0<=i.c-1<8 and (attack or (self.board[i.r-1][i.c-1]!='' and self.board[i.r-1][i.c-1][0]=='b') or (i.r==3 and self.enpassantable and self.enpassantable.c+1==i.c))):
                redbox.append((i.r-1,i.c-1))
            if not attack: #front moving pawn does not attack anyone
                if(self.board[i.r-1][i.c]==''):
                    redbox.append((i.r-1,i.c))
                if(i.r==6 and self.board[i.r-1][i.c]=='' and self.board[i.r-2][i.c]==''):
                    redbox.append((i.r-2,i.c))
            
        elif(i.txt=="b_p"): #black pawn's movement
            if(0<=i.r+1<8 and 0<=i.c+1<8 and (attack or (self.board[i.r+1][i.c+1]!='' and self.board[i.r+1][i.c+1][0]=='w') or (i.r==4 and self.enpassantable and self.enpassantable.c-1==i.c))):
                redbox.append((i.r+1,i.c+1))
            if(0<=i.r+1<8 and 0<=i.c-1<8 and (attack or (self.board[i.r+1][i.c-1]!='' and self.board[i.r+1][i.c-1][0]=='w') or (i.r==4 and self.enpassantable and self.enpassantable.c+1==i.c))):
                redbox.append((i.r+1,i.c-1))
            if not attack: #front moving pawn does not attack anyone
                if(self.board[i.r+1][i.c]==''):
                    redbox.append((i.r+1,i.c))
                if(i.r==1 and self.board[i.r+1][i.c]=='' and self.board[i.r+2][i.c]==''):
                    redbox.append((i.r+2,i.c))
            
        else: #Queen rook and bishop's movement
            if(i.txt=="w_q" or i.txt=="b_q"): l=[[-1,0],[1,0],[0,1],[0,-1],[-1,1],[1,-1],[1,1],[-1,-1]]
            elif(i.txt=="w_r" or i.txt=="b_r"): l=[[-1,0],[1,0],[0,1],[0,-1]]
            else: l=[[-1,1],[1,-1],[1,1],[-1,-1]]
            for j in l:
                while(0<=i.r+j[0]<8 and 0<=i.c+j[1]<8):
                    if(self.board[i.r+j[0]][i.c+j[1]]!='' and self.board[i.r+j[0]][i.c+j[1]][0]!=i.txt[0]):
                        redbox.append((i.r+j[0],i.c+j[1]))
                        break
                    if(self.board[i.r+j[0]][i.c+j[1]]!=''):break
                    redbox.append((i.r+j[0],i.c+j[1]))
                    if(j[0]!=0):j[0]+=j[0]//abs(j[0])
                    if(j[1]!=0):j[1]+=j[1]//abs(j[1])
                    
        if not attack:
            c= "w" if(i.txt[0]=='b') else "b" # checking if playing a move will lead to check thus enabling pinning and block check movements
            for j in redbox.copy():
                self.move(i,j[0],j[1])
                if(self.getcheck(c)):
                    redbox.remove(j)
                self.remove()
                
            if i.txt[2:]=="k": #checking if king is passing through attack while castling
                if(((i.r,i.c-2) in redbox) and ((i.r,i.c-1) not in redbox)):
                    redbox.remove((i.r,i.c-2))
                if(((i.r,i.c+2) in redbox) and ((i.r,i.c+1) not in redbox)):
                    redbox.remove((i.r,i.c+2))
                
        return redbox
    
    def all_attack(self,colour): #all the possible attacks of a side are covered
        attack_list=[]
        for i in self.pieces:
            if(i.txt[0]==colour):
                attack_list+=self.movements(i,attack=True)
                    
        return attack_list
    
    def getcheck(self,colour): #check if king is in check
        attack=self.all_attack(colour)
        for i in self.pieces:
            if ((i.txt=="b_k" and colour=="w") or (i.txt=="w_k" and colour=="b")):
                if((i.r,i.c) in attack):
                    return True
        return False
                
    def move(self,piece,r,c): #the moves are played and stored
        rem=''
        if(r>7 or c>7):return
        if self.board[r][c]!='': #normal piece is attacked
            for i in self.pieces:
                if i.r==r and i.c==c:
                    self.pieces.remove(i)
                    rem=i
                    break
        elif(piece.txt[2]=='p' and piece.c!=c and self.board[r][c]==''): #enpassent move is played
            self.pieces.remove(self.enpassantable)
            rem=self.enpassantable
            self.board[rem.r][rem.c]=''
        
        self.moves.append({"piece":piece,"pos":(piece.r,piece.c),"removed":rem})
        self.board[piece.r][piece.c]=''
        self.board[r][c]=piece.txt
        
        self.enpassantable=None
        if(piece.txt=="w_r" and piece.c==0):self.castle[0]-=1 # castling conditions
        elif(piece.txt=="w_r" and piece.c==7):self.castle[1]-=1
        elif(piece.txt=="b_r" and piece.c==0):self.castle[2]-=1
        elif(piece.txt=="b_r" and piece.c==7):self.castle[3]-=1
        elif(piece.txt=="w_k"):
            self.castle[0]-=1
            self.castle[1]-=1
        elif(piece.txt=="b_k"):
            self.castle[2]-=1
            self.castle[3]-=1
        elif(piece.txt[2]=="p" and abs(r-piece.r)==2): #enpassant conditions(every double moving pawn)
            self.enpassantable=piece
            self.moves[-1]["enpassant_store"]=piece
        
        if(piece.txt[2:]=="k" and abs(piece.c-c)==2): #the king is castling(rook position changing)
            cold = 0 if(piece.c>c) else 7
            cnew = 3 if(piece.c>c) else 5
            r1 = 7 if(piece.txt[0]=='w') else 0
            for i in self.pieces:
                if (i.r,i.c) == (r1,cold):
                    self.board[r1][cold]=''
                    self.board[r1][cnew]=i.txt
                    i.c=cnew
                    self.moves[-1]["castled"]=(i,cold)
                    break
        
        piece.r=r
        piece.c=c
        
    def remove(self):
        if self.moves==[]:return
        old=self.moves.pop()
        p=old["removed"]
        if(p!=''):
            self.pieces.add(p)
            self.board[p.r][p.c]=p.txt
        
        if(old.get("castled")): #castling rook back to place
            p1,c1=old["castled"]
            self.board[p1.r][c1]=p1.txt
            self.board[p1.r][p1.c]=''
            p1.c=c1
        
        self.enpassantable=None #enpassant backstoring
        if(self.moves and self.moves[-1].get("enpassant_store")):
            self.enpassantable=self.moves[-1]["enpassant_store"]
            
        r=old["pos"][0]
        c=old["pos"][1]
        p1=old["piece"]
        
        if(p1.txt=="w_r" and c==0):self.castle[0]+=1 # castling conditions
        elif(p1.txt=="w_r" and c==7):self.castle[1]+=1
        elif(p1.txt=="b_r" and c==0):self.castle[2]+=1
        elif(p1.txt=="b_r" and c==7):self.castle[3]+=1
        elif(p1.txt=="w_k"):
            self.castle[0]+=1
            self.castle[1]+=1
        elif(p1.txt=="b_k"):
            self.castle[2]+=1
            self.castle[3]+=1
        
        self.board[r][c]=p1.txt
        if(self.board[p1.r][p1.c]==p1.txt): self.board[p1.r][p1.c]=''
        p1.r=r
        p1.c=c
        
class AI:
    def __init__(self,env,colour):
        self.colour=colour
        self.env=env
        self.pawn_map = [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
        ]

        self.knight_map = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
        ]

        self.bishop_map = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
        ]

        self.rook_map = [
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
        ]

        self.queen_map = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
        ]
        
    def get_move(self):
        move = None
        score = -99999
        for i in self.available_moves(self.colour):
            self.env.move(i[0],i[1],i[2])
            s1 = self.alphabeta(2,-9999,9999,True)
            
            print(i[0].txt,":",s1,":",i[1],i[2])
            
            self.env.remove()
            if(s1>score):
                score=s1
                move=i
        print("final score:",score,move[0].txt,move[1],move[2])
        return move[0],move[1],move[2]
    
    def alphabeta(self,depth,a,b,maximize):
        if depth==0:
            return self.evaluate()
        if (maximize):
            best_score = -99999
            for i in self.available_moves('b' if self.colour=='w' else 'w'):
                self.env.move(i[0],i[1],i[2])
                best_score = max(best_score, self.alphabeta(depth-1, a, b, False))
                a = max(a, best_score)
                self.env.remove()
                if (b <= a):
                    break
            return best_score
        else:
            best_score = 99999
            for i in self.available_moves(self.colour):
                self.env.move(i[0],i[1],i[2])
                best_score = min(best_score, self.alphabeta(depth-1, a, b, True))
                b = min(b, best_score)
                self.env.remove()
                if (b <= a):
                    break
            return best_score
        
    def available_moves(self,colour):
        m=[]
        for i in self.env.pieces:
            if(i.txt[0]==colour):
                m1=self.env.movements(i)
                if(m1!=[]):
                    for j in m1:
                        m.append((i,j[0],j[1]))
        return m
    
    def evaluate(self):
        sign = lambda x:1 if x==self.colour else -1
        score=0    
        for i in self.env.pieces:
            s = sign(i.txt[0])
            if i.txt[2:]=="p":
                score+=(100*s)
                score+=(self.pawn_map[i.r][i.c]*s)
            elif i.txt[2:]=="kn":
                score+=(320*s)
                score+=(self.knight_map[i.r][i.c]*s)
            elif i.txt[2:]=="b":
                score+=(330*s)
                score+=(self.bishop_map[i.r][i.c]*s)
            elif i.txt[2:]=="r":
                score+=(500*s)
                score+=(self.knight_map[i.r][i.c]*s)
            elif i.txt[2:]=="q":
                score+=(900*s)
                score+=(self.queen_map[i.r][i.c]*s)
                
        return score
            
class Piece(pygame.sprite.Sprite): #pygame sprite (all pieces)
    def __init__(self,txt,r,c):
        pygame.sprite.Sprite.__init__(self)
        self.txt=txt
        self.r=r
        self.c=c
        self.image = pygame.transform.scale(pygame.image.load(self.txt+".png").convert_alpha(),(size,size))
        self.rect=self.image.get_rect(x=self.c*size+30, y=self.r*size+50)
        
    def update(self,flip=False): #updating piece position
        if not flip:
            self.rect.x=self.c*size+30
            self.rect.y=self.r*size+50
        else:
            self.rect.x=(7-self.c)*size+30
            self.rect.y=(7-self.r)*size+50

class game:
    def __init__(self):
        self.clock=pygame.time.Clock()
        self.screen=pygame.display.set_mode((size*8+60,size*8+100))
        self.started=False
        self.env=environment()
        self.colour='b'
        self.chance=0
        self.flip=False
        self.redbox=[]
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.started:
                    self.clicked() #sensing any click made by the user
                if event.type==pygame.KEYDOWN: #click z for remove
                    if event.key==pygame.K_z:
                        self.env.remove()
                        self.env.remove()
                        self.redbox=[]
                
            #==========>drawing the board
            self.screen.fill("black")
            self.draw_board() 
            if not self.started:
                self.select_mode()
            else:
                #==========>drawing the redbox
                a=self.redbox[1:]
                if self.flip: a=[(7-i[0],7-i[1]) for i in a]
                for i in a:
                    s = pygame.Surface((size,size))
                    s.set_alpha(128) 
                    s.fill((255,0,0))
                    self.screen.blit(s, (i[1]*size+30,i[0]*size+50))
                    
                #==========>AI move
                if((self.chance==0 and self.colour=='w') or (self.chance==1 and self.colour=='b')):
                    p,r,c=self.AI.get_move()
                    self.env.move(p,r,c)
                    self.chance=(self.chance+1)%2
                    
                #==========>drawing pieces
                self.env.pieces.update(self.flip) #updating pieces position
                self.env.pieces.draw(self.screen) #drawing
                
            pygame.display.update()
            self.clock.tick(15)
            
    def clicked(self):
        #==========>mouse position
        pos=pygame.mouse.get_pos()
        mr=(pos[1]-30)//size
        mc=(pos[0]-50)//size
        if self.flip :#if the board is flipped, positions are also flipped
            mr=7-mr
            mc=7-mc
        if (mr,mc) in self.redbox[2:]:
            #==========>Player move is played
            p=self.redbox[0]
            self.env.move(p,mr,mc) #moving piece
            self.chance=(self.chance+1)%2 #changing chance
                
        #==========>updating redbox
        self.redbox=[]
        for i in self.env.pieces:
            if(i.rect.collidepoint(pos)):
                
                if(i.txt[0]==self.colour):return #the player cannot click on opponents colour
                
                self.redbox.append(i) #the redbox contains the piece clicked, its position and its possible moves
                self.redbox.append((i.r,i.c))
                self.redbox+=self.env.movements(i)
            
    def select_mode(self):
        white=pygame.Rect(2.75*size,3*size,3*size,size)
        black=pygame.Rect(2.75*size,5*size,3*size,size)
        rand=pygame.Rect(2.75*size,7*size,3*size,size)
        font=pygame.font.Font(r'C:\Users\JAYANKONDAN\anaconda3\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\DejaVuSerif.ttf',int(size*2/3))
        pygame.draw.rect(self.screen,'yellow',white)
        pygame.draw.rect(self.screen,'yellow',black)
        pygame.draw.rect(self.screen,'yellow',rand)
        txt1=font.render('White',False,'black')
        txt2=font.render('Black',False,'black')
        txt3=font.render('Random',False,'black')
        self.screen.blit(txt1, txt1.get_rect(center=(4.25*size,3.5*size)))
        self.screen.blit(txt2, txt2.get_rect(center=(4.25*size,5.5*size)))
        self.screen.blit(txt3, txt3.get_rect(center=(4.25*size,7.5*size)))
        font1=pygame.font.Font(r'C:\Users\JAYANKONDAN\anaconda3\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\DejaVuSerif-Bold.ttf',size*2)
        txt4=font1.render('Chess',False,'brown')
        self.screen.blit(txt4, txt4.get_rect(center=(4.25*size,1.5*size)))
        if True in pygame.mouse.get_pressed():
            pos=pygame.mouse.get_pos()
            self.started=True
            if white.collidepoint(pos):
                print("All the best white!!")
                self.colour='b'
            elif black.collidepoint(pos):
                print("All the best black!!")
                self.colour='w'
                self.flip=True
            elif rand.collidepoint(pos):
                print("rand!!")
                self.colour=random.choice(['w','b'])
                if(self.colour=='w'): self.flip=True
            else:
                self.started=False
        self.AI=AI(self.env,self.colour)
                
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 1:
                    pygame.draw.rect(self.screen,'#769656',pygame.Rect(i*size+30,j*size+50,size,size))
                else:
                    pygame.draw.rect(self.screen,'#eeeed2',pygame.Rect(i*size+30,j*size+50,size,size))
                    
g=game()
g.run()