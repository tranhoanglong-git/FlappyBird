import pygame, sys, random
from login import init_db, login_user, get_user_high_score, update_user_high_score
from register import register_user
from leaderboard import get_top_leaderboard
from logout import logout_user  

# Tạo hàm cho game

# Vẽ sàn cho game
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos + 432,650))
    
# tạo ống với khoảng trên dưới
def create_pipe():
    GAP_SIZE = 260  
    GAP_CENTER_MIN = 250
    GAP_CENTER_MAX = 550
    gap_center_y = random.randint(GAP_CENTER_MIN, GAP_CENTER_MAX)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, gap_center_y + GAP_SIZE // 2))
    top_pipe = pipe_surface.get_rect(midbottom=(500, gap_center_y - GAP_SIZE // 2))
    return bottom_pipe, top_pipe

# di chuyển ống
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# vẽ ống và ống lật ngược
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

# tạo coin ngẫu nhiên
def create_coin():
    # Tạo coin ở vị trí an toàn giữa ống trên và ống dưới
    GAP_SIZE = 260  
    GAP_CENTER_MIN = 250
    GAP_CENTER_MAX = 550
    gap_center_y = random.randint(GAP_CENTER_MIN, GAP_CENTER_MAX)
    
    # Tính toán vị trí an toàn cho coin
    # Coin sẽ xuất hiện ở giữa khoảng trống, cách ống ít nhất 400 pixel
    safe_margin = 400
    top_pipe_bottom = gap_center_y - GAP_SIZE // 2
    bottom_pipe_top = gap_center_y + GAP_SIZE // 2
    
    # Đảm bảo coin ở giữa khoảng trống an toàn
    safe_y = gap_center_y  # Vị trí trung tâm của khoảng trống
    coin_rect = coin_surface.get_rect(center=(500, safe_y))
    return coin_rect

# di chuyển coin
def move_coins(coins):
    for coin in coins:
        coin.centerx -= 5
    return coins

# vẽ coin
def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_surface, coin)
            
# kiếm tra va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

# kiểm tra va chạm với coin và thu thập
def check_coin_collision(coins):
    global score
    collected_coins = []
    for coin in coins:
        if bird_rect.colliderect(coin):
            collected_coins.append(coin)
            score += 1
            score_sound.play()
    # Loại bỏ coin đã thu thập
    for coin in collected_coins:
        if coin in coins:
            coins.remove(coin)
    return coins

# xoay chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird

# đổi hình ảnh chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

# hiển thị điểm số hiện tại và điểm cao
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    
        high_score_surface = game_font.render(f'High Score: {int(high_score )}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)

# cập nhật điểm cao nhất nếu điểm hiện tại lớn hơn.
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
       
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)
small_font = pygame.font.Font('04B_19.ttf',20)

# PHẦN 2: HÀM HỖ TRỢ GIAO DIỆN (UI)
def draw_text(surface, text, font, color, center):
    # Vẽ một dòng chữ ra màn hình tại vị trí center
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=center)
    surface.blit(txt, rect)
    return rect

def draw_button(surface, text, center, size=(240, 50)):
    # Vẽ button đơn giản; trả về True nếu chuột đang bấm trái trên button
    w, h = size
    rect = pygame.Rect(0, 0, w, h)
    rect.center = center
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
    hovered = rect.collidepoint(mouse_pos)
    color = (70, 130, 180) if hovered else (50, 90, 140)
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, (255,255,255), rect, width=2, border_radius=10)
    draw_text(surface, text, small_font, (255,255,255), rect.center)
    clicked = hovered and mouse_pressed[0]
    return clicked

class TextInput:
    # Ô nhập liệu cực gọn cho username/password
    def __init__(self, placeholder='', is_password=False, width=300, height=50):
        self.text = ''
        self.placeholder = placeholder
        self.is_password = is_password
        self.rect = pygame.Rect(0, 0, width, height)
        self.active = False

    def set_center(self, center):
        self.rect.center = center

    def handle_event(self, event):
        # Bắt sự kiện: click để focus, gõ phím để nhập/xoá, Enter/Tab để điều hướng
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return 'submit'
            elif event.key == pygame.K_TAB:
                return 'tab'
            else:
                if len(self.text) < 24 and event.unicode and 32 <= ord(event.unicode) <= 126:
                    self.text += event.unicode
        return None

    def draw(self, surface):
        # Vẽ khung input; nếu là password thì hiển thị dấu *
        pygame.draw.rect(surface, (30,30,30), self.rect, border_radius=8)
        pygame.draw.rect(surface, (255,255,255), self.rect, width=2, border_radius=8)
        display_text = ('*' * len(self.text)) if (self.is_password and self.text) else (self.text or self.placeholder)
        color = (255,255,255) if self.text else (150,150,150)
        draw_text(surface, display_text, small_font, color, self.rect.center)

# BIẾN TRẠNG THÁI GAME

gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
current_user = None
screen_state = 'menu' # menu | login | register | leaderboard | game
auth_message = ''
username_input = None
password_input = None
focus = 'user'
passed_pipes = set()  # Theo dõi các ống đã bay qua

init_db()  # Đảm bảo DB sẵn sàng trước khi dùng

# Chèn hình nền (background)
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Chèn sàn (floor) để tạo cảm giác chuyển động mặt đất
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Chèn chim (3 khung hình cánh)
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))

# Tạo timer cho chim (đổi khung cánh mỗi 200ms)
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)

# Chèn ống (cặp ống trên/dưới)
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Chèn coin
coin_surface = pygame.image.load('assets/coin.png').convert_alpha()
coin_surface = pygame.transform.scale(coin_surface, (50, 50))  # Tăng kích thước coin
coin_list = []

# Tạo timer sinh ống mới mỗi 1700ms
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1700) 

# Ảnh hiển thị ở trạng thái game over
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message1.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,350))

# Âm thanh: vỗ cánh, va chạm, đạt điểm
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')


# VÒNG LẶP CHÍNH CUA
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Input cho gameplay (chỉ xử lý khi đang ở màn hình 'game')
        if screen_state == 'game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement =- 7
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active==False:
                    game_active = True
                    pipe_list.clear()
                    coin_list.clear()
                    bird_rect.center = (100,384)
                    bird_movement = 0
                    score = 0
                    passed_pipes.clear()
            if event.type == spawnpipe:
                pipe_list.extend(create_pipe())
                # Tạo coin cùng lúc với ống (50% cơ hội)
                if random.random() < 0.5:
                    coin_list.append(create_coin())
            if event.type == birdflap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird, bird_rect = bird_animation()
        # Input cho form đăng nhập/đăng kí
        if screen_state in ('login', 'register'):
            if username_input and password_input:
                action = username_input.handle_event(event)
                if action == 'tab':
                    focus = 'pass'
                if action == 'submit':
                    focus = 'pass'
                action2 = password_input.handle_event(event)
                if action2 == 'tab':
                    focus = 'user'
                if action2 == 'submit':
                    pass
        
    screen.blit(bg,(0,0))  

    # VẼ CÁC MÀN HÌNH 
    if screen_state == 'menu':
        # Màn hình MENU chính: Play / Đăng nhập / Đăng kí / Bảng xếp hạng
        draw_text(screen, 'FLAPPY BIRD', game_font, (255,255,255), (216, 150))
        if current_user:
            draw_text(screen, f'Hello {current_user}', small_font, (255,255,0), (216, 210))
        play_clicked = draw_button(screen, 'PLAY GAME', (216, 320))
        # Ẩn LOGIN/REGISTER khi đã đăng nhập; thêm LOG OUT
        logout_clicked = False
        if current_user:
            login_clicked = False
            register_clicked = False
            lb_clicked = draw_button(screen, 'LEADERBOARD', (216, 385))
            logout_clicked = draw_button(screen, 'LOG OUT', (216, 450))
        else:
            login_clicked = draw_button(screen, 'LOGIN', (216, 385))
            register_clicked = draw_button(screen, 'REGISTER', (216, 450))
            lb_clicked = draw_button(screen, 'LEADERBOARD', (216, 515))
        if play_clicked:
            # Reset trạng thái game và chuyển sang màn hình game
            pipe_list.clear()
            coin_list.clear()
            bird_rect.center = (100,384)
            bird_movement = 0
            score = 0
            passed_pipes.clear()
            game_active = True
            high_score = get_user_high_score(current_user) if current_user else 0
            screen_state = 'game'
        elif login_clicked:
            # Chuẩn bị 2 ô nhập liệu (username/password) cho màn hình đăng nhập
            username_input = TextInput('username')
            password_input = TextInput('password', is_password=True)
            username_input.set_center((216, 320))
            password_input.set_center((216, 390))
            focus = 'user'
            auth_message = ''
            screen_state = 'login'
        elif register_clicked:
            # Chuẩn bị ô nhập liệu cho màn hình đăng kí
            username_input = TextInput('username')
            password_input = TextInput('password', is_password=True)
            username_input.set_center((216, 320))
            password_input.set_center((216, 390))
            focus = 'user'
            auth_message = ''
            screen_state = 'register'
        elif lb_clicked:
            screen_state = 'leaderboard'
        elif logout_clicked:
            # Đăng xuất: xoá người dùng hiện tại, reset high_score trên màn hình
            logout_data = logout_user()
            current_user = logout_data['current_user']
            high_score = logout_data['high_score']
            auth_message = logout_data['auth_message']

    elif screen_state == 'login':
        # Màn hình ĐĂNG NHẬP
        draw_text(screen, 'Login', game_font, (255,255,255), (216, 150))
        if username_input and password_input:
            username_input.active = (focus == 'user')
            password_input.active = (focus == 'pass')
            username_input.draw(screen)
            password_input.draw(screen)
        ok_clicked = draw_button(screen, 'CONFIRM', (216, 450))
        back_clicked = draw_button(screen, 'MENU', (216, 520))
        draw_text(screen, auth_message, small_font, (255,200,200), (216, 250))
        if ok_clicked and username_input and password_input:
            # Thử đăng nhập -> thành công: về menu; thất bại: hiện thông báo
            if login_user(username_input.text, password_input.text):
                current_user = username_input.text
                high_score = get_user_high_score(current_user)
                auth_message = 'Login successful'
                screen_state = 'menu'
            else:
                auth_message = 'Incorrect username or password'
        if back_clicked:
            screen_state = 'menu'

    elif screen_state == 'register':
        # Màn hình ĐĂNG KÍ
        draw_text(screen, 'REGISTER', game_font, (255,255,255), (216, 150))
        if username_input and password_input:
            username_input.active = (focus == 'user')
            password_input.active = (focus == 'pass')
            username_input.draw(screen)
            password_input.draw(screen)
        ok_clicked = draw_button(screen, 'CREATE ACCOUNT', (216, 450))
        back_clicked = draw_button(screen, 'MENU', (216, 520))
        draw_text(screen, auth_message, small_font, (255,200,200), (216, 250))
        if ok_clicked and username_input and password_input:
            # Thử đăng kí -> thành công: tự đăng nhập, về menu
            ok, msg = register_user(username_input.text, password_input.text)
            auth_message = msg
            if ok:
                current_user = username_input.text
                high_score = 0
                screen_state = 'menu'
        if back_clicked:
            screen_state = 'menu'

    elif screen_state == 'leaderboard':
        # Màn hình BẢNG XẾP HẠNG (Top high score)
        draw_text(screen, 'Leaderboard', game_font, (255,255,255), (216, 110))
        rows = get_top_leaderboard(8)
        y = 180
        rank = 1
        for name, hs in rows:
            draw_text(screen, f"{rank}. {name} - {int(hs)}", small_font, (255,255,255), (216, y))
            y += 45
            rank += 1
        back_clicked = draw_button(screen, 'MENU', (216, 600))
        if back_clicked:
            screen_state = 'menu'

    elif screen_state == 'game':
        # Màn hình GAMEPLAY (chơi game)
        if game_active:
            bird_movement += gravity
            rotated_bird = rotate_bird(bird)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_active = check_collision(pipe_list)
            pipe_list = move_pipes(pipe_list)
            draw_pipe(pipe_list)
            
            # Xử lý coin
            coin_list = move_coins(coin_list)
            draw_coins(coin_list)
            coin_list = check_coin_collision(coin_list)
            
            # Kiểm tra và cộng điểm khi bay qua ống
            # Chỉ kiểm tra ống dưới (bottom pipe) để tránh cộng điểm 2 lần cho 1 cặp ống
            for i, pipe in enumerate(pipe_list):
                # Chỉ kiểm tra ống dưới (có bottom >= 600)
                if pipe.bottom >= 600:  # Đây là ống dưới
                    pipe_id = id(pipe)
                    if pipe_id not in passed_pipes and bird_rect.centerx > pipe.centerx:
                        passed_pipes.add(pipe_id)
                        score += 1
                        score_sound.play()
            
            score_display('main game')
        else:
            # Trạng thái thua: hiển thị bảng điểm, cập nhật high score nếu có user
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')
            if current_user:
                update_user_high_score(current_user, score)
            replay = draw_button(screen, 'PLAY AGAIN', (216, 500))
            to_menu = draw_button(screen, 'MENU', (216, 560))
            if replay:
                pipe_list.clear()
                coin_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
                passed_pipes.clear()
                game_active = True
            if to_menu:
                screen_state = 'menu'

    # Sàn (scroll vô hạn)
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:   
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
