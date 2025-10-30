import pygame, sys, random #Thu vien Game
# Các module hỗ trợ đăng nhập, đăng kí, bảng xếp hạng
from login import init_db, login_user, get_user_high_score, update_user_high_score
from register import register_user
from leaderboard import get_top_leaderboard
from logout import logout_user  

# Các Hàm Của Game
# --------------------------------
# Vẽ sàn cho game
def draw_floor(): 
    screen.blit(floor,(floor_x_pos,650)) # vẽ sàn 1
    screen.blit(floor,(floor_x_pos + 432,650)) # vẽ sàn 2
    
# Tạo ống với khoảng trên dưới
def create_pipe():
    GAP_SIZE = 260  # khoảng trống giữa 2 ống
    GAP_CENTER_MIN = 250 # vị trí tâm khoảng trống tối thiểu
    GAP_CENTER_MAX = 550 # vị trí tâm khoảng trống tối đa
    gap_center_y = random.randint(GAP_CENTER_MIN, GAP_CENTER_MAX) # vị trí tâm khoảng trống ngẫu nhiên
    bottom_pipe = pipe_surface.get_rect(midtop=(500, gap_center_y + GAP_SIZE // 2)) # ống dưới
    top_pipe = pipe_surface.get_rect(midbottom=(500, gap_center_y - GAP_SIZE // 2)) # ống trên
    return bottom_pipe, top_pipe, gap_center_y # trả về cả tâm khoảng trống

# Di chuyển ống
def move_pipes(pipes): 
    for pipe in pipes: 
        pipe.centerx -= 5 
    return pipes

# vẽ ống và ống lật ngược
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600: # ống dưới
            screen.blit(pipe_surface,pipe) # vẽ ống dưới
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True) # lật ống trên
            screen.blit(flip_pipe,pipe) # vẽ ống trên

# tạo coin ngẫu nhiên
def create_coin(gap_center_y=None): 
    GAP_SIZE = 260 # khoảng trống giữa 2 ống
    if gap_center_y is None: # nếu không có vị trí tâm khoảng trống được cung cấp, tạo ngẫu nhiên
        GAP_CENTER_MIN = 250 # vị trí tâm khoảng trống tối thiểu
        GAP_CENTER_MAX = 550 # vị trí tâm khoảng trống tối đa
        gap_center_y = random.randint(GAP_CENTER_MIN, GAP_CENTER_MAX) # vị trí tâm khoảng trống ngẫu nhiên

    # Tính giới hạn an toàn để đặt coin trong khoảng trống
    coin_h = coin_surface.get_height() // 2 # bán chiều cao coin
    safe_offset = 20  # khoảng cách an toàn từ mép khoảng trống
    # Giới hạn y để đặt coin
    top_limit = gap_center_y - GAP_SIZE // 2 + coin_h + safe_offset # giới hạn trên
    bottom_limit = gap_center_y + GAP_SIZE // 2 - coin_h - safe_offset # giới hạn dưới

    # Bảo đảm giới hạn coin hợp lệ
    if top_limit > bottom_limit: 
        safe_y = gap_center_y # Nếu khoảng trống quá nhỏ (không khả dụng), đặt coin ở trung tâm
    else:
        safe_y = random.randint(top_limit, bottom_limit) # chọn y an toàn ngẫu nhiên trong giới hạn

    coin_rect = coin_surface.get_rect(center=(500, safe_y)) # đặt coin
    return coin_rect 

# Di chuyển coin
def move_coins(coins):
    for coin in coins:
        coin.centerx -= 5 # di chuyển coin về bên trái
    return coins

# Vẽ coin
def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_surface, coin) # vẽ coin
            
# Kiếm tra va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # nếu va chạm với ống
            hit_sound.play() # phát âm thanh va chạm
            return False  
    if bird_rect.top <= -75 or bird_rect.bottom >= 650: # nếu va chạm với trần hoặc sàn
        return False # thua
    return True

# kiểm tra va chạm với coin và thu thập
def check_coin_collision(coins):
    global score # điểm số
    collected_coins = [] # danh sách coin đã thu thập
    for coin in coins:
        if bird_rect.colliderect(coin): # nếu va chạm với coin
            collected_coins.append(coin) # thêm vào danh sách thu thập
            score += 1 # cộng 1 điểm
            score_sound.play() # phát âm thanh thu thập coin
    # Loại bỏ coin đã thu thập
    for coin in collected_coins:
        if coin in coins: # nếu coin vẫn trong danh sách
            coins.remove(coin) # xoá coin đã thu thập khỏi danh sách
    return coins

# xoay chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1) # xoay chim dựa trên vận tốc
    return new_bird

# đổi hình ảnh chim
def bird_animation():
    new_bird = bird_list[bird_index] # lấy hình chim mới từ danh sách
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery)) # giữ y hiện tại
    return new_bird, new_bird_rect # trả về chim mới và rect mới

# hiển thị điểm số hiện tại và điểm cao
def score_display(game_state):
    if game_state == 'main game': # hiển thị điểm khi chơi
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) # điểm hiện tại khi chơi
        score_rect = score_surface.get_rect(center = (216,100)) # vị trí điểm khi chơi
        screen.blit(score_surface,score_rect) # vẽ điểm
    if game_state == 'game_over': # hiển thị điểm khi thua
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255)) # điểm hiện tại khi thua
        score_rect = score_surface.get_rect(center = (216,100)) # vị trí điểm khi thua
        screen.blit(score_surface,score_rect) # vẽ điểm
    
        high_score_surface = game_font.render(f'High Score: {int(high_score )}',True,(255,255,255)) # điểm cao 
        high_score_rect = high_score_surface.get_rect(center = (216,630)) # vị trí điểm cao 
        screen.blit(high_score_surface,high_score_rect) # vẽ điểm cao 

# cập nhật điểm cao nhất nếu điểm hiện tại lớn hơn.
def update_score(score, high_score):
    if score > high_score: # nếu điểm hiện tại lớn hơn điểm cao
        high_score = score # cập nhật điểm cao
    return high_score # trả về điểm cao
       
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512) # Cấu hình âm thanh
pygame.init() # Khởi động pygame
pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((432,768)) # Kích thước màn hình game 
clock = pygame.time.Clock() # Đồng hồ để kiểm soát FPS
game_font = pygame.font.Font('04B_19.ttf',40) # Font chính
small_font = pygame.font.Font('04B_19.ttf',20) # Font chứ nhỏ

# HÀM HỖ TRỢ GIAO DIỆN (UI)
def draw_text(surface, text, font, color, center): 
   # Vẽ một dòng chữ ra màn hình tại vị trí center
    txt = font.render(text, True, color) # tạo bề mặt chữ
    rect = txt.get_rect(center=center) # lấy rect chữ
    surface.blit(txt, rect) # vẽ chữ lên
    return rect # trả về rect chữ

def draw_button(surface, text, center, size=(240, 50)): 
    # Vẽ button đơn giản; trả về True nếu chuột đang bấm trái trên button
    w, h = size # kích thước button
    rect = pygame.Rect(0, 0, w, h) # tạo rect button
    rect.center = center # đặt vị trí button
    mouse_pos = pygame.mouse.get_pos() # vị trí chuột
    mouse_pressed = pygame.mouse.get_pressed(num_buttons=3) # trạng thái bấm chuột
    hovered = rect.collidepoint(mouse_pos) # kiểm tra hover 
    color = (70, 130, 180) if hovered else (50, 90, 140) # màu button
    pygame.draw.rect(surface, color, rect, border_radius=10) # vẽ button
    pygame.draw.rect(surface, (255,255,255), rect, width=2, border_radius=10) # viền button
    draw_text(surface, text, small_font, (255,255,255), rect.center) # vẽ chữ button
    clicked = hovered and mouse_pressed[0] # kiểm tra click
    return clicked 

class TextInput:
    # Ô nhập liệu cho username/password
    def __init__(self, placeholder='', is_password=False, width=300, height=50): # khởi tạo ô nhập liệu
        self.text = '' # văn bản nhập liệu
        self.placeholder = placeholder # văn bản gợi ý
        self.is_password = is_password # có phải là mật khẩu
        self.rect = pygame.Rect(0, 0, width, height) # rect ô nhập liệu
        self.active = False # trạng thái focus

    def set_center(self, center): 
        self.rect.center = center # đặt vị trí center cho ô nhập liệu  

    def handle_event(self, event):
        # Bắt sự kiện: click để focus, gõ phím để nhập/xoá, Enter/Tab để điều hướng
        if event.type == pygame.MOUSEBUTTONDOWN: # kiểm tra click chuột
            self.active = self.rect.collidepoint(event.pos) # kiểm tra click vào ô
        if event.type == pygame.KEYDOWN and self.active: # kiểm tra gõ phím khi ô được focus
            if event.key == pygame.K_BACKSPACE: # nhấn Backspace
                self.text = self.text[:-1] # xoá ký tự cuối
            elif event.key == pygame.K_RETURN: # nhấn Enter
                return 'submit' # trả về submit
            elif event.key == pygame.K_TAB: # nhấn Tab
                return 'tab' # trả về tab 
            else:
                if len(self.text) < 24 and event.unicode and 32 <= ord(event.unicode) <= 126: # giới hạn ký tự
                    self.text += event.unicode # thêm ký tự mới
        return None

    def draw(self, surface):
        # Vẽ khung input; nếu là password thì hiển thị dấu *
        bg_color = (50,50,70) if self.active else (30,30,30)  # màu nền sẽ sáng hơn khi focus
        border_color = (100,149,237) if self.active else (255,255,255)  # màu viền xanh khi focus
        border_width = 3 if self.active else 2  # viền dày hơn khi focus
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8) # vẽ nền
        pygame.draw.rect(surface, border_color, self.rect, width=border_width, border_radius=8) # vẽ viền
        display_text = ('*' * len(self.text)) if (self.is_password and self.text) else (self.text or self.placeholder) # hiển thị dấu * nếu là password
        color = (255,255,255) if self.text else (150,150,150) # màu chữ 
        draw_text(surface, display_text, small_font, color, self.rect.center) # vẽ chữ

# BIẾN TRẠNG THÁI GAME
gravity = 0.25 # trọng lực game 
bird_movement = 0 # vận tốc chim
game_active = False # trạng thái game
score = 0 # điểm số ban đầu
high_score = 0 # điểm cao 
current_user = None # người dùng hiện tại
screen_state = 'menu' # menu | login | register | leaderboard | game
auth_message = '' # thông báo xác thực
username_input = None # ô nhập username
password_input = None # ô nhập password
focus = 'user' # ô đang focus
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
bird_index = 0 # chỉ số khung hình chim hiện tại
bird = bird_list[bird_index] # hình chim hiện tại
bird_rect = bird.get_rect(center = (100,384)) # vị trí ban đầu của chim

# Tạo timer cho chim (đổi khung cánh mỗi 200ms)
birdflap = pygame.USEREVENT + 1 
pygame.time.set_timer(birdflap,200) 

# Chèn ống (cặp ống trên/dưới)
pipe_surface = pygame.image.load('assets/pipe-green.png').convert() 
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] 

# Chèn coin
coin_surface = pygame.image.load('assets/coin.png').convert_alpha()
coin_surface = pygame.transform.scale(coin_surface, (50, 50))  # kích thước coin
coin_list = []

# Tạo timer sinh ống mới mỗi 1700ms
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1700) 

# Ảnh hiển thị ở trạng thái game over
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message1.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,350)) # vị trí ảnh game over

# Âm thanh của game: vỗ cánh, va chạm, đạt điểm
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# VÒNG LẶP CHÍNH CUA
while True:
    for event in pygame.event.get(): # lặp qua các sự kiện của game
        if event.type == pygame.QUIT: # nếu nhấn nút đóng cửa sổ
            pygame.quit() # thoát pygame
            sys.exit() # thoát chương trình
        # Input cho gameplay (chỉ xử lý khi đang ở màn hình 'game')
        if screen_state == 'game': # chỉ xử lý khi đang chơi game
            if event.type == pygame.KEYDOWN: # kiểm tra nhấn phím 
                if event.key == pygame.K_SPACE and game_active: # nhấn Space khi đang chơi
                    bird_movement = 0 # đặt vận tốc chim về 0
                    bird_movement =- 7 # tạo lực nâng cho chim
                    flap_sound.play() # phát âm thanh vỗ cánh
                if event.key == pygame.K_SPACE and game_active==False: # nhấn Space khi thua
                    game_active = True # bắt đầu lại game
                    pipe_list.clear() # xoá ống
                    coin_list.clear() # xoá coin 
                    bird_rect.center = (100,384) # đặt lại vị trí chim
                    bird_movement = 0 # đặt vận tốc chim về 0 
                    score = 0 # đặt lại điểm số 
                    passed_pipes.clear() # đặt lại ống đã qua 
            if event.type == spawnpipe: # khi đến thời điểm sinh ống mới
                # Tạo 2 ống và nhận về vị trí tâm khoảng trống (gap_center_y)
                bottom_pipe, top_pipe, gap_center_y = create_pipe() # tạo ống
                pipe_list.extend((bottom_pipe, top_pipe)) # thêm ống vào danh sách
                # Tạo coin cùng lúc với ống (50% cơ hội) và đặt coin trong khoảng trống
                if random.random() < 0.5: # 50% cơ hội tạo coin
                    coin_list.append(create_coin(gap_center_y)) # tạo coin và thêm vào danh sách
            if event.type == birdflap: # khi đến thời điểm đổi khung cánh chim
                if bird_index < 2: # nếu chưa phải khung cuối
                    bird_index += 1  # tăng chỉ số khung hình
                else:
                    bird_index = 0 # quay lại khung đầu
                bird, bird_rect = bird_animation() # cập nhật hình và rect chim
        # Input cho form đăng nhập/đăng kí
        if screen_state in ('login', 'register'): # chỉ xử lý khi ở màn hình đăng nhập/đăng kí
            if username_input and password_input: # nếu có ô nhập liệu
                action = username_input.handle_event(event) # xử lý sự kiện cho ô username
                if action == 'tab': # chuyển focus sang ô password
                    focus = 'pass' # chuyển focus sang password
                if action == 'submit': # nếu nhấn Enter
                    focus = 'pass' # chuyển focus sang password
                action2 = password_input.handle_event(event) # xử lý sự kiện cho ô password
                if action2 == 'tab': # chuyển focus sang ô username
                    focus = 'user' # chuyển focus sang username
                if action2 == 'submit': # nếu nhấn Enter
                    pass
        
    screen.blit(bg,(0,0))  # vẽ nền

    # VẼ CÁC MÀN HÌNH 
    if screen_state == 'menu':
        # Màn hình MENU chính: Play / Đăng nhập / Đăng kí / Bảng xếp hạng
        draw_text(screen, 'FLAPPY BIRD', game_font, (255,255,255), (216, 150)) # tiêu đề trang menu
        if current_user:
            draw_text(screen, f'Hello {current_user}', small_font, (255,255,0), (216, 210)) # chào người dùng đã đăng nhập
        play_clicked = draw_button(screen, 'PLAY GAME', (216, 320)) # nút chơi game ở trang menu
        # Ẩn LOGIN/REGISTER khi đã đăng nhập; thêm LOG OUT
        logout_clicked = False # khởi tạo biến logout_clicked
        if current_user:
            login_clicked = False # ẩn nút login ở trang menu khi login
            register_clicked = False # ẩn nút register ở trang menu khi login
            lb_clicked = draw_button(screen, 'LEADERBOARD', (216, 385)) # nút bảng xếp hạng ở trang menu khi login
            logout_clicked = draw_button(screen, 'LOG OUT', (216, 450)) # nút đăng xuất ở trang menu khi login
        else:
            login_clicked = draw_button(screen, 'LOGIN', (216, 385)) # nút đăng nhập ở menu
            register_clicked = draw_button(screen, 'REGISTER', (216, 450)) # nút đăng kí ở menu
            lb_clicked = draw_button(screen, 'LEADERBOARD', (216, 515)) # nút bảng xếp hạng ở menu
        if play_clicked: # nếu nhấn nút chơi game
            # Reset trạng thái game và chuyển sang màn hình game
            pipe_list.clear() # xoá ống
            coin_list.clear() # xoá coin
            bird_rect.center = (100,384) # đặt lại vị trí chim
            bird_movement = 0 # đặt vận tốc chim về 0
            score = 0 # đặt lại điểm số
            passed_pipes.clear() # đặt lại ống đã qua
            game_active = True # bắt đầu game
            high_score = get_user_high_score(current_user) if current_user else 0 # lấy điểm cao của người dùng hiện tại
            screen_state = 'game' # chuyển sang màn hình game
        elif lb_clicked: # nếu nhấn nút bảng xếp hạng
            screen_state = 'leaderboard'  # chuyển sang màn hình leaderboard 
        elif login_clicked: # nếu nhấn nút đăng nhập
            # Chuẩn bị 2 ô nhập liệu (username/password) cho màn hình đăng nhập
            username_input = TextInput('username') # ô nhập username 
            password_input = TextInput('password', is_password=True) # ô nhập password
            username_input.set_center((216, 320)) # đặt vị trí ô username ở màn hình đăng nhập
            password_input.set_center((216, 390)) # đặt vị trí ô password ở màn hình đăng nhập
            focus = 'user' # đặt focus ban đầu vào ô username 
            auth_message = '' # xoá thông báo xác thực
            screen_state = 'login' # chuyển sang màn hình đăng nhập 
        elif register_clicked: # nếu nhấn nút đăng kí
            # Chuẩn bị ô nhập liệu cho màn hình đăng kí
            username_input = TextInput('username') # ô nhập username
            password_input = TextInput('password', is_password=True) # ô nhập password
            username_input.set_center((216, 320)) # đặt vị trí ô username ở man hình đăng kí
            password_input.set_center((216, 390)) # đặt vị trí ô password ở màn hình đăng kí
            focus = 'user' # đặt focus ban đầu vào ô username 
            auth_message = ''
            screen_state = 'register' # chuyển sang màn hình đăng kí
        elif logout_clicked: # nếu nhấn nút đăng xuất
            # Đăng xuất: xoá người dùng hiện tại, reset high_score trên màn hình
            logout_data = logout_user() # gọi hàm đăng xuất
            current_user = logout_data['current_user'] # lấy người dùng hiện tại (None)
            high_score = logout_data['high_score'] # đặt lại điểm cao
            auth_message = logout_data['auth_message'] # thông báo xác thực

    elif screen_state == 'login': # nếu đang ở màn hình đăng nhập
        # Màn hình ĐĂNG NHẬP
        draw_text(screen, 'Login', game_font, (255,255,255), (216, 150)) # tiêu đề ở trang đăng nhập
        if username_input and password_input: 
            username_input.active = (focus == 'user') # đặt trạng thái active cho ô username
            password_input.active = (focus == 'pass') # đặt trạng thái active cho ô password
            username_input.draw(screen) # vẽ ô username
            password_input.draw(screen) # vẽ ô password
        ok_clicked = draw_button(screen, 'CONFIRM', (216, 450)) # nút xác nhận ở trang đăng nhập
        back_clicked = draw_button(screen, 'MENU', (216, 580))  # nút quay lại menu ở trang đăng nhập
        draw_text(screen, auth_message, small_font, (255,200,200), (216, 250)) # thông báo xác thực ở trang đăng nhập
        if ok_clicked and username_input and password_input: # nếu nhấn nút xác nhận 
            # Thử đăng nhập -> thành công: về menu; thất bại: hiện thông báo
            if login_user(username_input.text, password_input.text):
                current_user = username_input.text # đặt người dùng hiện tại
                high_score = get_user_high_score(current_user)  # lấy điểm cao người dùng
                auth_message = 'Login successful' # thông báo thành công
                screen_state = 'menu' # về menu
            else:
                auth_message = 'Incorrect' # thông báo thất bại
        if back_clicked:
            screen_state = 'menu' # về menu

    elif screen_state == 'register':
        # Màn hình ĐĂNG KÍ
        draw_text(screen, 'REGISTER', game_font, (255,255,255), (216, 150)) # tiêu đề
        if username_input and password_input:
            username_input.active = (focus == 'user') # đặt trạng thái active cho ô username
            password_input.active = (focus == 'pass') # đặt trạng thái active cho ô password
            username_input.draw(screen) # vẽ ô username
            password_input.draw(screen) # vẽ ô password
        ok_clicked = draw_button(screen, 'CREATE ACCOUNT', (216, 450))         # nút tạo tài khoản ở trang đăng kí
        back_clicked = draw_button(screen, 'MENU', (216, 580))                 # nút quay lại menu ở trang đăng kí
        draw_text(screen, auth_message, small_font, (255,200,200), (216, 250)) # thông báo xác thực
        if ok_clicked and username_input and password_input:
            # Thử đăng kí -> thành công: tự đăng nhập, về menu
            ok, msg = register_user(username_input.text, password_input.text) # gọi hàm đăng kí 
            auth_message = msg  # thông báo xác thực
            if ok:
                current_user = username_input.text # đặt người dùng hiện tại
                high_score = 0 # điểm cao mới
                screen_state = 'menu' # về menu
        if back_clicked:
            screen_state = 'menu' # về menu

    elif screen_state == 'leaderboard': 
        # Màn hình BẢNG XẾP HẠNG (Top high score)
        draw_text(screen, 'Leaderboard', game_font, (255,255,255), (216, 110)) # tiêu đề
        rows = get_top_leaderboard(8) # lấy 8 người có điểm cao nhất
        y = 180   # vị trí y bắt đầu vẽ
        rank = 1  # xếp hạng bắt đầu từ 1
        # Tính toán căn giữa bảng xếp hạng
        max_name_len = max((len(str(name)) for name, _ in rows), default=0)
        max_score_len = max((len(str(int(hs))) for _, hs in rows), default=0)
        table_width = 320  # chiều rộng bảng xếp hạng
        x_start = (432 - table_width) // 2  # căn giữa theo chiều ngang màn hình 432px
        name_col = x_start + 40
        score_col = x_start + table_width - 80
        for name, hs in rows:
            # Định dạng: hạng. tên (căn trái)    điểm (căn phải)
            rank_str = f"{rank}."
            name_str = str(name)
            score_str = str(int(hs))
            # Vẽ thứ hạng
            txt_rank = small_font.render(rank_str, True, (255,255,255))
            rect_rank = txt_rank.get_rect()
            rect_rank.topleft = (x_start, y)
            screen.blit(txt_rank, rect_rank)
            # Vẽ tên (căn trái)
            txt_name = small_font.render(name_str, True, (255,255,255))
            rect_name = txt_name.get_rect()
            rect_name.topleft = (name_col, y)
            screen.blit(txt_name, rect_name)
            # Vẽ điểm (căn phải)
            txt_score = small_font.render(score_str, True, (255,255,255))
            rect_score = txt_score.get_rect()
            rect_score.top = y
            rect_score.right = score_col + 60
            screen.blit(txt_score, rect_score)
            y += 45
            rank += 1
        back_clicked = draw_button(screen, 'MENU', (216, 600)) # nút quay lại menu
        if back_clicked:
            screen_state = 'menu' # về menu

    elif screen_state == 'game': 
        # Màn hình GAMEPLAY (chơi game)
        if game_active:
            bird_movement += gravity # áp dụng trọng lực cho chim
            rotated_bird = rotate_bird(bird) # xoay chim dựa trên vận tốc
            bird_rect.centery += bird_movement # cập nhật vị trí chim theo vận tốc
            screen.blit(rotated_bird,bird_rect) # vẽ chim
            game_active = check_collision(pipe_list) # kiểm tra va chạm với ống/sàn/trần
            pipe_list = move_pipes(pipe_list)   # di chuyển ống
            draw_pipe(pipe_list) # vẽ ống
            
            # Xử lý coin
            coin_list = move_coins(coin_list)           # di chuyển coin
            draw_coins(coin_list)                       # vẽ coin
            coin_list = check_coin_collision(coin_list) # kiểm tra va chạm với coin
            
            # Kiểm tra và cộng điểm khi bay qua ống
            # Chỉ kiểm tra ống dưới (bottom pipe) để tránh cộng điểm 2 lần cho 1 cặp ống
            for i, pipe in enumerate(pipe_list):
                # Chỉ kiểm tra ống dưới (có bottom >= 600)
                if pipe.bottom >= 600:  # Đây là ống dưới
                    pipe_id = id(pipe) # lấy id duy nhất của ống
                    if pipe_id not in passed_pipes and bird_rect.centerx > pipe.centerx: # nếu chưa qua ống này và chim đã bay qua
                        passed_pipes.add(pipe_id) # đánh dấu ống đã qua
                        score += 1 # cộng điểm
                        score_sound.play() # phát âm thanh đạt điểm
            
            score_display('main game')
        else:
            # Trạng thái thua: hiển thị bảng điểm, cập nhật high score nếu có user
            screen.blit(game_over_surface,game_over_rect) # vẽ ảnh game over
            high_score = update_score(score, high_score) # cập nhật điểm cao
            score_display('game_over') # hiển thị điểm số
            if current_user: 
                update_user_high_score(current_user, score) # cập nhật điểm cao người dùng trong DB
            replay = draw_button(screen, 'PLAY AGAIN', (216, 500)) # nút chơi lại
            to_menu = draw_button(screen, 'MENU', (216, 560)) # nút về menu
            if replay:
                pipe_list.clear() # xoá ống
                coin_list.clear() # xoá coin
                bird_rect.center = (100,384) # đặt lại vị trí chim
                bird_movement = 0 # đặt vận tốc chim về 0
                score = 0 # đặt lại điểm số
                passed_pipes.clear() # đặt lại ống đã qua
                game_active = True # bắt đầu lại game
            if to_menu: 
                screen_state = 'menu' # về menu

    # Sàn (scroll vô hạn)
    floor_x_pos -= 1 # di chuyển sàn về bên trái
    draw_floor() # vẽ sàn
    if floor_x_pos <= -432:   
        floor_x_pos = 0 # đặt lại vị trí sàn để tạo hiệu ứng vô hạn

    pygame.display.update() # cập nhật màn hình
    clock.tick(100) # giới hạn FPS
