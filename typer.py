import pygame
import pygame.locals
typed_strings = 0

def upload_info(filename:str="data.txt"):
    '''
    Принимает на вход строку filename
    Не возвращает ничего
    Задает глобальную переменную typed_strings.
    '''
    global typed_strings 
    try:
        with open(filename,encoding='utf-8', mode="r") as data:
            try:
                typed_strings = int(data.readline())
            except:
                typed_strings = 0
    except FileNotFoundError:
        typed_strings = 0        


def save_info(filename:str="data.txt"):
    '''
    Принимает на вход строку filename
    Не возвращает ничего
    Записывает в файл информацию.
    '''
    global typed_strings 
    try:
        data = open(filename, encoding='utf-8', mode="r")
        all_data = data.readlines()
        data.close()
        if all_data[0][:-1:].isdigit():
            all_data[0] = str(typed_strings) + '\n'
        else:
            all_data.insert(0, str(typed_strings) + '\n')
        

        data = open(filename, encoding='utf-8', mode="w")
        data.write(''.join(all_data))
        data.close()
    except:
        pass

def choose_string(filename:str="data.txt", string_number:int=1)->str:
    '''
    Принимает на вход строку filename и целое значение string_number.
    Возвращает строку состоящую не только из чисел с номером string_number
    Если файла не существует, либо строки с таким номером не существует - возвращает "-1".
    '''
    try:
        with open(filename,encoding='utf-8', mode="r") as data:
            
            count = 0
            for line in data:
                if not line.isdigit():
                    count += 1
                if count == string_number:
                    if line[-1] == '\n':
                        return line[:-1:]
                    else:
                        return line
            return None
    except:
        return None


def display_text(text:str, max_x, typed_letters, font, screen, color=(0,0,0), color_ok = (0, 152, 50), 
                 x:int=10, y:int=10):
    '''
    Принимает текст, максимальную длинну текста, количество напечатанных букв,
    шрифт, экран, опционально - цвет, цвет напечатанного и верхний левый угол текста.

    Печатает текст на экран.
    '''

    words = text.split()
    len_space = font.size(' ')[0]
    min_x = x

    count = 0
    srf2 = None
    for word in words:
        if count + len(word) < typed_letters:
            srf = font.render(word, True, color_ok)
        else: 
            srf = font.render(word, True, color)

            if count < typed_letters:
                srf2 = font.render(word[:typed_letters - count:], True, color_ok)
            else:
                srf2 = None
            
        size = srf.get_size()
        if x + size[0] > max_x:
            x = min_x
            y += size[1] + 1
        screen.blit(srf, (x, y))
        if srf2 is not None:
            screen.blit(srf2, (x, y))

        x += size[0] + len_space
        count += len(word) + 1



def draw_graphic(data, screen, x=10, y=500, delta_x = 5):
    '''
    Функция получает значения в точках и экран на котором рисуется график. Опционально - координаты
    левого нижнего угла
    Рисукт график на заданном экране.
    '''
    point=pygame.surface.Surface((5,5))

    pointb=pygame.surface.Surface((5,3))
    pointb.fill((0, 0, 0))

    for i in data:
        if i > 200:
            point.fill((117, 21, 30))
            if i > 500:
                i = 500
        elif i > 100:
            point.fill((255, 204, 0))
        else:
            point.fill((80, 200, 120))
        
        screen.blit(point, (x, y - i/5))
        screen.blit(pointb, (x, y))
        x += delta_x
    


def UI():
    '''
    Главная функция с циклом Pygame
    '''
    upload_info()

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((240,248,255))

    max_x = screen.get_size()[0]

    font = pygame.font.SysFont(None, 20)
    typed_letters = 0
    global typed_strings
    is_typing_started = False
    running = True
    FPS = 30
    clock = pygame.time.Clock()
    string = None
    
    pygame.display.flip()

    letters_pressing_time = []
    letter_time = 0

    while running:
        screen.fill((240,248,255))
        
        if not is_typing_started and typed_strings == 0:
            screen.blit(font.render("Нажмите enter чтобы начать", True, (0, 0, 0)), (10, 10))
        elif not is_typing_started:
            screen.blit(font.render("Нажмите enter чтобы продолжить", True, (0, 0, 0)), (10, 10))
            draw_graphic(letters_pressing_time, screen)
        elif string is None:
            string = choose_string(string_number=typed_strings + 1)
        elif string == "-1":
            screen.blit(font.render("Конец файла.", True, (0, 0, 0)), (10, 10))
            draw_graphic(letters_pressing_time, screen)
        else:
            display_text(string, max_x, typed_letters, font, screen)
            


        events = pygame.event.get()
        for event in events:
            if string is not None and string != "-1":
                if event.type == pygame.KEYDOWN:
                    if is_typing_started:
                        if typed_letters < len(string) and event.unicode == string[typed_letters]:
                            typed_letters += 1
                            letters_pressing_time.append(letter_time)
                            letter_time = 0
                        
                        if typed_letters >= len(string):
                            typed_letters = 0
                            typed_strings += 1
                            is_typing_started = False
                            string = None


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    is_typing_started = True
                    letter_time = 0
                    letters_pressing_time = []

            if event.type == pygame.locals.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)
        letter_time += 100/30
    

    save_info()
    pygame.quit()



if __name__ == "__main__":
    UI()