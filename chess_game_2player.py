# THE CHESS GAME!!
import pygame,sys
pygame.init()
pygame.display.set_caption("Chess")
size=85
enpaasant=False
class piece(pygame.sprite.Sprite):
    def __init__(self,txt,r,c):
        self.txt=txt
        self.r=r
        self.c=c
        self.prev=[r,c]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f"{self.txt}.png").convert_alpha(),(size,size))
        self.rect=self.image.get_rect(x=self.c*size+30, y=self.r*size+50)
    
    def move(self,r,c,board,pieces,castle=True):
        if board[r][c]!='':
            for i in pieces:
                if i.r==r and i.c==c:
                    pieces.remove(i)
                    break
        self.prev=[self.r,self.c,board[r][c]]
        board[self.r][self.c]=''
        self.r=r
        self.c=c
        board[self.r][self.c]=self.txt
        self.rect.x=self.c*size+30
        self.rect.y=self.r*size+50
        if(castle and self.txt=="w_k"):
            if(self.c-self.prev[1]==2):
                for i in pieces:
                    if (i.r,i.c)==(7,7):
                        i.move(7,5,board,pieces)
                        break
            elif(self.c-self.prev[1]==-2):
                for i in pieces:
                    if (i.r,i.c)==(7,0):
                        i.move(7,3,board,pieces)
                        break
        elif(castle and self.txt=="b_k"):
            if(self.c-self.prev[1]==2):
                for i in pieces:
                    if (i.r,i.c)==(0,7):
                        i.move(0,5,board,pieces)
                        break
            elif(self.c-self.prev[1]==-2):
                for i in pieces:
                    if (i.r,i.c)==(0,0):
                        i.move(0,3,board,pieces)
                        break
        self.enpaasant_move(board,pieces)
        
    def enpaasant_move(self,board,pieces):
        global enpaasant
        if(self.txt=="w_p" and self.r==2 and (self.c!=self.prev[1]) and self.prev[2]==''):
            for i in pieces:
                if i.r==3 and i.c==self.c:
                    pieces.remove(i)
                    board[3][i.c]=''
                    enpaasant=True
                    break
        elif(self.txt=="b_p" and self.r==5 and (self.c!=self.prev[1]) and self.prev[2]==''):
            for i in pieces:
                if i.r==4 and i.c==self.c:
                    pieces.remove(i)
                    board[4][i.c]=''
                    enpaasant=True
                    break
        else:
            enpaasant=False
            
    def backmove(self,board,pieces):
        global enpaasant
        if self.prev[2]!='':
            pieces.add(piece(self.prev[2],self.r,self.c))
        if(enpaasant):
            if self.txt=="w_p":
                pieces.add(piece("b_p",3,self.c))
                board[3][self.c]="b_p"
            else:
                pieces.add(piece("w_p",4,self.c))
                board[4][self.c]="w_p"
            enpaasant=False
        board[self.r][self.c]=self.prev[2]
        self.r=self.prev[0]
        self.c=self.prev[1]
        board[self.r][self.c]=self.txt
        self.rect.x=self.c*size+30
        self.rect.y=self.r*size+50
        
class maingame:
    def __init__(self):
        self.screen=pygame.display.set_mode((size*8+60,size*8+100))
        self.clock=pygame.time.Clock()
        self.setup()
        self.redbox=[]
        self.chance=0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked()
            self.screen.fill("black")
            self.draw_board()
            self.pieces.draw(self.screen)
            pygame.display.update()
            self.clock.tick(15)
            
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 1:
                    pygame.draw.rect(self.screen,'#769656',pygame.Rect(i*size+30,j*size+50,size,size))
                else:
                    pygame.draw.rect(self.screen,'#eeeed2',pygame.Rect(i*size+30,j*size+50,size,size))
        for i in self.redbox[1:]:
            s = pygame.Surface((size,size))
            s.set_alpha(128) 
            s.fill((255,0,0))
            self.screen.blit(s, (i[1]*size+30,i[0]*size+50))

    def clicked(self):
        pos=pygame.mouse.get_pos()
        mr=(pos[1]-30)//size
        mc=(pos[0]-50)//size
        if (mr,mc) in self.redbox[2:]:
            p=self.redbox[0]
            p.move(mr,mc,self.board,self.pieces)
            self.enpassant=[]
            if(self.getcheck(p.txt[0])):
                print("CHECK")
                if(self.checkmate(p.txt[0])):
                    print(f"CHECK MATE {p.txt[0]} won")
            if(p.txt=="w_k"):
                self.w_l_c=False
                self.w_r_c=False
            elif(p.txt=="b_k"):
                self.b_l_c=False
                self.b_r_c=False
            elif(p.txt=="w_r"):
                if(p.prev[:2]==[7,0]):self.w_l_c=False
                elif(p.prev[:2]==[7,7]):self.w_r_c=False
            elif(p.txt=="b_r"):
                if(p.prev[:2]==[0,0]):self.b_l_c=False
                elif(p.prev[:2]==[0,7]):self.b_r_c=False
            self.redbox=[]
            self.chance=(self.chance+1)%2
            if((p.txt=="w_p" and p.r==0) or (p.txt=="b_p" and p.r==7)):
                self.promote(p)
            elif((p.txt=="w_p" and p.r-p.prev[0]==-2) or (p.txt=="b_p" and p.r-p.prev[0]==2)):
                self.enpassant.append(p)
            return
        
        self.redbox=[]
        for i in self.pieces:
            if(i.rect.collidepoint(pos)):
                
                if(self.chance==0 and i.txt[0]=="b"):return
                elif(self.chance==1 and i.txt[0]=="w"):return
                
                self.redbox.append(i)
                self.redbox.append((i.r,i.c))
                self.redbox+=self.getbox(i)
                                
                if(i.txt=="w_p"):
                    if(0<=i.r-1<8 and 0<=i.c+1<8 and self.board[i.r-1][i.c+1]!='' and self.board[i.r-1][i.c+1][0]=='b'):
                        self.redbox.append((i.r-1,i.c+1))
                    if(0<=i.r-1<8 and 0<=i.c-1<8 and self.board[i.r-1][i.c-1]!='' and self.board[i.r-1][i.c-1][0]=='b'):
                        self.redbox.append((i.r-1,i.c-1))
                    if(self.board[i.r-1][i.c]==''):
                        self.redbox.append((i.r-1,i.c))
                    if(i.r==6 and self.board[i.r-1][i.c]=='' and self.board[i.r-2][i.c]==''):
                        self.redbox.append((i.r-2,i.c))
                    if(i.r==3):
                        for j in self.enpassant:
                            if(j.c==i.c+1):self.redbox.append((i.r-1,i.c+1))
                            elif(j.c==i.c-1):self.redbox.append((i.r-1,i.c-1))
                elif(i.txt=="b_p"):
                    if(0<=i.r+1<8 and 0<=i.c+1<8 and self.board[i.r+1][i.c+1]!='' and self.board[i.r+1][i.c+1][0]=='w'):
                        self.redbox.append((i.r+1,i.c+1))
                    if(0<=i.r+1<8 and 0<=i.c-1<8 and self.board[i.r+1][i.c-1]!='' and self.board[i.r+1][i.c-1][0]=='w'):
                        self.redbox.append((i.r+1,i.c-1))
                    if(self.board[i.r+1][i.c]==''):
                        self.redbox.append((i.r+1,i.c))
                    if(i.r==1 and self.board[i.r+1][i.c]=='' and self.board[i.r+2][i.c]==''):
                        self.redbox.append((i.r+2,i.c))
                    if(i.r==4):
                        for j in self.enpassant:
                            if(j.c==i.c+1):self.redbox.append((i.r+1,i.c+1))
                            elif(j.c==i.c-1):self.redbox.append((i.r+1,i.c-1))
                elif(i.txt=="w_k" or i.txt=="b_k"):
                    if i.txt[0]=="w":
                        attack = self.attackbox("b")
                        self.redbox=[x for x in self.redbox if x not in attack]
                        if(self.w_l_c and self.board[7][3]==self.board[7][2]==self.board[7][1]=='' and all(x not in attack for x in ((7,4),(7,3),(7,2),(7,1)))):self.redbox.append((i.r,i.c-2))
                        if(self.w_r_c and self.board[7][5]==self.board[7][6]=='' and all(x not in attack for x in ((7,4),(7,5),(7,6)))):self.redbox.append((i.r,i.c+2))
                    else:
                        attack = self.attackbox("w")
                        self.redbox=[x for x in self.redbox if x not in attack]
                        if(self.b_l_c and self.board[0][3]==self.board[0][2]==self.board[0][1]=='' and all(x not in attack for x in ((0,4),(0,3),(0,2),(0,1)))):self.redbox.append((i.r,i.c-2))
                        if(self.b_r_c and self.board[0][5]==self.board[0][6]=='' and all(x not in attack for x in ((0,4),(0,5),(0,6)))):self.redbox.append((i.r,i.c+2))
                    #if(len(self.redbox)==1):self.redbox.insert(1,(i.r,i.c))
                break
            
        if(self.redbox==[]): return
        if(self.redbox[0].txt[0]=="w"):c="b"
        else:c="w"
        arr=self.redbox[2:]
        for i in arr:
            self.redbox[0].move(i[0],i[1],self.board,self.pieces,False)
            if(self.getcheck(c)):
                self.redbox.remove(i)
            self.redbox[0].backmove(self.board,self.pieces)
                
    def checkmate(self,colour):
        for i in self.pieces:
            if(i.txt[0]==colour):continue
            a=self.getbox(i)
            if i.txt=="w_p":
                if(0<=i.r-1<8 and 0<=i.c+1<8):a.append((i.r-1,i.c+1))
                if(0<=i.r-1<8 and 0<=i.c-1<8):a.append((i.r-1,i.c-1))
            elif i.txt=="b_p":
                if(0<=i.r+1<8 and 0<=i.c+1<8):a.append((i.r+1,i.c+1))
                if(0<=i.r+1<8 and 0<=i.c-1<8):a.append((i.r+1,i.c-1))
            for j in a:
                i.move(j[0],j[1],self.board,self.pieces,False)
                g=self.getcheck(colour)
                i.backmove(self.board,self.pieces)
                if not g:
                    return False
        return True
                
    def getcheck(self,colour):
        attack = self.attackbox(colour)
        check=False
        for i in self.pieces:
            if ((i.txt=="b_k" and colour=="w") or (i.txt=="w_k" and colour=="b")):
                if((i.r,i.c) in attack):
                    check=True
                break
        return check
            
    def attackbox(self,colour):
        attack=[]
        for j in self.pieces:
            if j.txt!='' and j.txt[0]==colour:
                attack+=self.getbox(j)
                if j.txt=="w_p":
                    if(0<=j.r-1<8 and 0<=j.c+1<8):
                        attack.append((j.r-1,j.c+1))
                    if(0<=j.r-1<8 and 0<=j.c-1<8):
                        attack.append((j.r-1,j.c-1))
                elif j.txt=="b_p":
                    if(0<=j.r+1<8 and 0<=j.c+1<8):
                        attack.append((j.r+1,j.c+1))
                    if(0<=j.r+1<8 and 0<=j.c-1<8):
                        attack.append((j.r+1,j.c-1))
        return attack
    
    def promote(self,p):
        box=pygame.Surface((size,size*4))
        img = lambda x: pygame.transform.scale(pygame.image.load(f"{x}.png").convert_alpha(),(size,size))
        box.fill("white")
        box.blit(img(f"{p.txt[0]}_q"),(0,0))
        box.blit(img(f"{p.txt[0]}_r"),(0,size))
        box.blit(img(f"{p.txt[0]}_b"),(0,size*2))
        box.blit(img(f"{p.txt[0]}_kn"),(0,size*3))
        rect=box.get_rect(x=(p.c+1)*size+30,y=p.r*size+50)
        if(p.txt[0]=="b"):rect.y-=size*3
        self.draw_board()
        self.pieces.draw(self.screen)
        self.screen.blit(box, rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos=pygame.mouse.get_pos()
                    mr=(pos[1]-30)//size
                    mc=(pos[0]-50)//size
                    if(rect.collidepoint(pos)):
                        self.pieces.remove(p)
                        if(p.txt[0]=="w"):
                            if((mr,mc)==(p.r,p.c+1)):
                                self.pieces.add(piece("w_q",p.r,p.c))
                                self.board[p.r][p.c]="w_q"
                            elif((mr,mc)==(p.r+1,p.c+1)):
                                self.pieces.add(piece("w_r",p.r,p.c))
                                self.board[p.r][p.c]="w_r"
                            elif((mr,mc)==(p.r+2,p.c+1)):
                                self.pieces.add(piece("w_b",p.r,p.c))
                                self.board[p.r][p.c]="w_b"
                            else:
                                self.pieces.add(piece("w_kn",p.r,p.c))
                                self.board[p.r][p.c]="w_kn"
                        else:
                            if((mr,mc)==(p.r,p.c+1)):
                                self.pieces.add(piece("b_kn",p.r,p.c))
                                self.board[p.r][p.c]="b_kn"
                            elif((mr,mc)==(p.r-1,p.c+1)):
                                self.pieces.add(piece("b_b",p.r,p.c))
                                self.board[p.r][p.c]="b_b"
                            elif((mr,mc)==(p.r-2,p.c+1)):
                                self.pieces.add(piece("b_r",p.r,p.c))
                                self.board[p.r][p.c]="b_r"
                            else:
                                self.pieces.add(piece("b_q",p.r,p.c))
                                self.board[p.r][p.c]="b_q"
                        return
                self.clock.tick(15)
            
    def getbox(self,i):
        redbox=[]
        if(i.txt=="w_kn" or i.txt=="b_kn"):
            for j in [(2,1),(1,2),(-2,1),(1,-2),(2,-1),(-1,2),(-2,-1),(-1,-2)]:
                if(0<=i.r+j[0]<8 and 0<=i.c+j[1]<8 and (self.board[i.r+j[0]][i.c+j[1]]==''or self.board[i.r+j[0]][i.c+j[1]][0]!=i.txt[0])):
                    redbox.append((i.r+j[0],i.c+j[1]))
                    
        elif(i.txt=="b_k" or i.txt=="w_k"):
            for j in [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
                if(0<=i.r+j[0]<8 and 0<=i.c+j[1]<8 and (self.board[i.r+j[0]][i.c+j[1]]=='' or self.board[i.r+j[0]][i.c+j[1]][0]!=i.txt[0])):
                    redbox.append((i.r+j[0],i.c+j[1]))
                    
        elif(i.txt!="b_p" and i.txt!="w_p"):
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
        return redbox
            
    def setup(self):
        self.board = [['' for i in range(8)]for j in range(8)]
        self.board[0] = ['b_r','b_kn','b_b','b_q','b_k','b_b','b_kn','b_r']
        self.board[1] = ['b_p','b_p','b_p','b_p','b_p','b_p','b_p','b_p']
        self.board[7] = ['w_r','w_kn','w_b','w_q','w_k','w_b','w_kn','w_r']
        self.board[6] = ['w_p','w_p','w_p','w_p','w_p','w_p','w_p','w_p']
        self.pieces=pygame.sprite.Group()
        for i in range(8):
            self.pieces.add(piece(self.board[0][i],0,i))
            self.pieces.add(piece(self.board[7][i],7,i))
            self.pieces.add(piece(self.board[1][i],1,i))
            self.pieces.add(piece(self.board[6][i],6,i))
        self.w_l_c=True
        self.w_r_c=True
        self.b_l_c=True
        self.b_r_c=True
        self.enpassant=[]
        
m=maingame()
m.run()