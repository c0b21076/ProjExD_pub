import pygame as pg
from pygame.locals import *
import random


#画面サイズの設定
WIDTH = 1200
HEIGHT = int(WIDTH * 0.7)

#色の設定
BLACK = (0,0,0)
RED = (255, 20, 40)
SKYBLUE = (0,50,150)
WHITE = (255, 255, 255)
GRAY = (200,200,200)

#フォントの設定
font_name = pg.font.match_font("hg正楷書体pro")

def draw_text(screen,text,size,x,y,color): #テキスト描画用の関数
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface,text_rect)

def sound():#C0B21128 西口響
    #音楽を呼び出す関数
    pg.mixer.init(frequency = 44100)    # 初期設定
    pg.mixer.music.load("sound/PerituneMaterial_Dream_and_Reality_inst_loop.mp3")     # 音楽ファイルの読み込み
    pg.mixer.music.play(1000)   # 音楽の再生回数
    return 0

class Background:#バックグラウンドクラス
    def __init__(self):
        #画像をロードしてtransformでサイズ調整（画面サイズに合わせる）
        self.image = pg.image.load('pic/pg_bg.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image,(WIDTH,HEIGHT))
        #画面のスクロール設定
        self.scroll = 0
        self.scroll_speed = 4
        self.x = 0
        self.y = 0
        #0と画面横サイズの二つをリストに入れておく
        self.imagesize = [0,WIDTH]

    def draw_BG(self,screen): #描画メソッド
        #for文で２つの位置に１枚づつバックグラウンドを描画する（描画するx位置は上で指定したimagesizeリスト）
        for i in range(2):      
            screen.blit(self.image,(self.scroll + self.imagesize[i], self.y))
        self.scroll -= self.scroll_speed
        #画像が端まで来たら初期位置に戻す
        if abs(self.scroll) > WIDTH:
            self.scroll = 0


class Plane(pg.sprite.Sprite):
    #インスタンス化時の初期位置を引数x、yに指定
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self) 
        
        #画像を空リストに格納していく
        self.idleimgs = []
        image = pg.image.load('pic/1.png').convert_alpha()         
        image = pg.transform.scale(image,(95,75))
        self.idleimgs.append(image)        

        #再開後の無敵状態の画像をリストに格納
        self.immortal_imgs = []                  
        image = pg.image.load('pic/0.png').convert_alpha()         
        image = pg.transform.scale(image,(95,75))
        self.immortal_imgs.append(image)

        #敵に接触時の画像をリストに格納していく
        self.deadimgs = []
        self.deadimg = pg.image.load('pic/1.png').convert_alpha()
        #１枚の画像を回転させながら８枚格納
        for i in range(8):
            self.deadimg = pg.transform.scale(self.deadimg,(95,75))
            self.deadimg = pg.transform.rotate(self.deadimg,90 * i)
            self.deadimgs.append(self.deadimg)

        #描画する画像を指定するための設定
        self.index = 0
        self.image = self.idleimgs[0]

        self.image.set_colorkey(SKYBLUE)
        #画像のrectサイズを取得
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        #radiusは当たり判定の設定に必要
        self.radius = 40
        
        #現在の状態をture,falseで管理
        self.IDLE = True
        self.SHOT = False
        self.DEAD = False
        self.IMMORTAL = False

        self.dy = 20
        #無敵時間の設定 
        self.immortal_timer = 60

        #残機画像関連（左上に表示される）
        self.plane_mini_img = pg.image.load('pic/2.png').convert_alpha()
        #サイズ調整で小さくする
        self.plane_mini_img = pg.transform.scale(self.plane_mini_img,(50,50))
        self.plane_mini_img.set_colorkey((0,0,0))
        self.lives = 3
          
    def draw_lives(self,screen,x,y): #残機描画用メソッド
        for i in range(self.lives):
            img_rect = self.plane_mini_img.get_rect()
            img_rect.x = x + 50 * i
            img_rect.y = y
            screen.blit(self.plane_mini_img,img_rect)

    def change_img(self,imglist): #状態に合わせて画像を描画するメソッド
        self.index += 1
        if self.index >= len(imglist):
            self.index = 0
        self.image = imglist[self.index]
    
    def create_bullet(self): #弾丸生成クラス呼び出しメソッド
        return Bullet(self.rect.center[0] + 20,self.rect.center[1] + 20)

    def update(self):
        #描画する画像を現在の状態から指定
        if self.IDLE:
            self.change_img(self.idleimgs)
        if self.DEAD:
            self.change_img(self.deadimgs)
        if self.immortal_timer < 60:
            self.change_img(self.immortal_imgs)
        
        #キー操作関連
        key = pg.key.get_pressed()
        if self.DEAD == False: #墜落している状態で無ければ以下の入力を受け付ける
            #上下左右の移動
            if key[pg.K_a]:
                self.rect.x -= 10
                if self.rect.x <= 0: 
                    self.rect.x = 0 

            if key[pg.K_d]: 
                self.rect.x += 10 
                if self.rect.x >= WIDTH - 75:
                    self.rect.x = WIDTH - 75

            if key[pg.K_w]:
                self.rect.y -= 10
                if self.rect.y <= 0: 
                    self.rect.y = 0 

            if key[pg.K_s]: 
                self.rect.y += 10 
                if self.rect.y >= HEIGHT - 75:
                    self.rect.y = HEIGHT - 75

        #墜落中の場合、斜め下に移動していく
        if self.DEAD:
            self.rect.x += 3
            self.rect.y += 10


class Bullet(pg.sprite.Sprite): #弾丸クラス
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)

        #イメージを空のリストに格納
        self.bullet_images = []
        img = pg.image.load('pic/egg.png').convert_alpha()
        img = pg.transform.scale(img,(30,30))
        self.bullet_images.append(img)
        
         #描画する画像を指定するための設定
        self.index = 0
        self.image = self.bullet_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]        
           
    def update(self): #毎フレームの処理用メソッド
        self.rect.x += 40
        #位置が右端までいった場合の処理（killで自分自身をスプライトグループから削除する）
        if self.rect.x >= WIDTH:
            self.kill()
            

class Mob(pg.sprite.Sprite): #敵キャラ用クラス
    def __init__(self,x,y) -> None:
        pg.sprite.Sprite.__init__(self)
        
        self.images = []
        #サイズを３種類設定し、ランダムに設定するようにする
        self.imagesize = [(72,46),(144,92),(108,69)]
        random_num = random.choice(self.imagesize)
        #空のリストに画像を格納していく
        img = pg.image.load('pic/alien.gif').convert_alpha()
        img = pg.transform.scale(img,random_num)
        img = pg.transform.flip(img,180, 0)
        self.images.append(img)

        #描画する画像を指定するための設定
        self.index = 0
        self.image = self.images[0]
        self.image.set_colorkey(SKYBLUE)
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.radius = int(self.rect.x / 2)
        #初期配置をランダムに設定する
        self.dx = random.randint(1,15)
        self.dy = random.randint(-6,6)
        self.dy = 0
     
    def update(self): #毎フレームの処理用メソッド
        self.rect.x -= self.dx
        self.rect.y -= self.dy
        #move範囲
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.dy *= -1 

        if self.rect.right < 0:
            self.rect.x = WIDTH
        #画像インデックス送り
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[0]


class Game(): #メイン処理のクラス
    def __init__(self) -> None:
        #pygameの初期化
        pg.init() 
        
        #クロック/FPS設定
        self.clock = pg.time.Clock()
        self.fps = 30       

        #画面設定
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption('戦え！こうかとん')
        #マウスのポインターを削除
        pg.mouse.set_visible(False)

        #BGインスタンス化
        self.BG = Background()

        #プレイヤーインスタンス化
        self.plane_group = pg.sprite.Group()
        self.plane = Plane(150,HEIGHT / 2)
        self.plane_group.add(self.plane)
        
        #弾丸関連インスタンス化
        self.bullet_group = pg.sprite.Group() 

        #敵キャラインスタンス化        
        self.mob_group = pg.sprite.Group()
        for i in range(10):
            self.mob = Mob(WIDTH * 2,random.randint(100,800))
            self.mob_group.add(self.mob)
           
        #スコア
        self.score = 0

        #フラグ
        self.game_clear = False #髙井智暉
        self.game_over = False
        self.game_start = True

    def game_start_screen(self): #スタート画面の描画用メソッド
        draw_text(self.screen,"戦えぃ！こうかとん", 100, WIDTH / 2, HEIGHT - 650, RED)
        draw_text(self.screen,"Press ENTER KEY TO START", 70, WIDTH / 2, HEIGHT - 500, BLACK)
        draw_text(self.screen,"Press ESCAPE KEY TO EXIT", 50, WIDTH / 2, HEIGHT - 400, BLACK)
        draw_text(self.screen,"BULLET: SPACE key", 50, WIDTH / 2, HEIGHT - 300, BLACK)
        draw_text(self.screen,"MOVE: WASD key", 50, WIDTH / 2, HEIGHT - 200, BLACK)

    #髙井智暉
    def game_clear_screen(self):
        draw_text(self.screen,"卵", 205, WIDTH / 2, HEIGHT / 4 - 50, GRAY)
        draw_text(self.screen,"殺", 205, WIDTH / 2, HEIGHT / 4 + 150, GRAY)
        draw_text(self.screen,"卵", 200, WIDTH / 2, HEIGHT / 4 - 50, WHITE)
        draw_text(self.screen,"殺", 200, WIDTH / 2, HEIGHT / 4 + 150, WHITE)
        draw_text(self.screen,"EGG EXECUTION", 50, WIDTH / 2, HEIGHT / 4 + 350, WHITE)
        draw_text(self.screen,"Press 9 KEY TO RESTART", 36, WIDTH / 2, int(HEIGHT * 0.8), BLACK)
        draw_text(self.screen,"Press ESCAPE KEY TO EXIT", 36, WIDTH / 2, int(HEIGHT * 0.85), BLACK)

    def game_over_screen(self): #GAMEOVER画面の描画用メソッド
        draw_text(self.screen,"死", 450, WIDTH / 2, HEIGHT / 2 - 300, RED)
        draw_text(self.screen,"DEATH", 50, WIDTH / 2, HEIGHT / 2 + 100, RED)
        draw_text(self.screen,"Press SPACE KEY TO RESTART", 36, WIDTH / 2, HEIGHT - 200, BLACK)    

    def main(self): #メインループ
        running = True
        t = 0
        sound()#音楽呼び出し
        #C0B21128 西口響
        while running:
            #敵キャラのインスタンス化
            t += 1
            if t % 100 == 0:
                if self.game_clear == False: #髙井智暉
                    for i in range(10):
                        self.mob = Mob(WIDTH,random.randint(100,800))
                        self.mob_group.add(self.mob)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                #キー入力の受付
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    if self.game_start:
                        if event.key == K_9:
                            self.game_start = False

                    #リスタート処理  gameover時　初期値に戻す
                    if event.key == pg.K_SPACE:
                        if self.plane.lives == 0:
                            #emptyでグループを空にする
                            self.mob_group.empty()
                            self.game_over = False
                            self.game_clear = False #髙井智暉
                            self.plane.IMMORTAL = False
                            self.plane.lives = 3
                            self.score = 0
                            #プレイヤーのインスタンス化
                            self.plane = Plane(150,HEIGHT / 2)
                            self.plane_group.add(self.plane) 
                    
                #弾丸発射キー操作
                if self.game_start == False and self.game_clear == False: #髙井智暉
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            if self.plane.DEAD == False:
                                self.plane.SHOT,self.plane.IDLE  = True,False
                                self.bullet_group.add(self.plane.create_bullet())
                    
                    #弾丸発射キーを放した時の処理
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_SPACE:
                            if self.plane.DEAD == False:             
                                self.plane.IDLE,self.plane.SHOT = True,False
                                self.bullet_READY = True
                    
                   
            #バックグラウンド表示
            self.BG.draw_BG(self.screen)
            if self.game_start:
                self.game_start_screen()
            #残機表示
            if self.game_start == False:
                self.plane.draw_lives(self.screen,50,70)
                
                #モブキャラ表示
                self.mob_group.draw(self.screen)

                #プレイヤー、弾丸表示
                self.plane_group.draw(self.screen)
                self.bullet_group.draw(self.screen)

                #各クラスアップデートメソッド実行
                self.plane_group.update()
                self.bullet_group.update()            
                self.mob_group.update()                      
                                                
                #プレイヤーとモブの接触時処理
                if self.plane.DEAD == False and self.plane.IMMORTAL == False:
                    mob1_collision =  pg.sprite.groupcollide(self.plane_group,self.mob_group,False,True)
                    for collision in mob1_collision:                
                        self.plane.DEAD = True
                        self.plane.IDLE, self.plane.SHOT, self.bullet_READY = False, False, False
                        self.plane.lives -= 1


                #プレイヤー死亡時処理
                if self.plane.DEAD == True:
                    if self.plane.rect.top >= HEIGHT:
                        if self.plane.lives == 0:
                            self.plane.kill()
                            self.game_over = True     
                        else:
                            self.plane.IDLE = True
                            self.plane.DEAD = False
                            self.plane.rect.x = 100
                            self.plane.rect.y = HEIGHT / 2
                            self.plane.IMMORTAL = True
                
                #モブキャラと弾丸のヒット時の処理
                mob1hits = pg.sprite.groupcollide(self.mob_group,self.bullet_group,True,True)
                if mob1hits:
                    self.score += 100  
                    #髙井智暉
                    if self.score >= 10000:
                        self.game_clear = True            

                #スコア表示              
                draw_text(self.screen, f'SCORE: {str(self.score)}', 50, WIDTH / 2, 100, BLACK)

                #GAMECLEAR
                #髙井智暉
                if self.game_clear:
                    self.plane.IMMORTAL = True
                    self.plane.kill()
                    self.mob.kill()
                    self.plane.immortal_timer += 1
                    self.game_clear_screen()
                
                #GAMEOVER　
                if self.game_over:
                    self.game_over_screen()
                
                #無敵時間カウンター  
                #髙井智暉
                if self.game_clear == False:
                    if self.plane.IMMORTAL:
                        self.plane.immortal_timer -= 1
                    if self.plane.immortal_timer <= 0:
                        self.plane.IMMORTAL = False
                        self.plane.immortal_timer = 60

            #FPS設定
            self.clock.tick(self.fps)
                
            pg.display.update()
        pg.quit()

game = Game()

game.main()