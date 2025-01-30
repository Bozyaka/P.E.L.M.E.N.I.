import os
import sys
import random
import math
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print(f"Файл с изображением '{fullname}' не найден")
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def change_size(self, w, h):
        self.state = pygame.Rect(0, 0, w, h)

    def apply(self, target, mod=1):
        if mod == 1:
            return target.rect.move(self.state.topleft)
        else:
            return target.rect.move(self.state.x * mod, self.state.y * mod)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + size[0] / 2, -t + size[1] / 2

    l = min(0, l)
    l = max(-(camera.width - size[0]), l)
    t = max(-(camera.height - size[1]), t)
    t = min(0, t)
    return pygame.Rect(l, t, w, h)


class EventBlock(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, file):
        super().__init__(ev_block)
        self.image = pygame.Surface([x2 - x1, y2 - y1])
        pygame.draw.rect(self.image, (0, 0, 0), (x1, y1, x2 - x1, y2 - y1))
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.file = [j.split('; ') for j in open(file, encoding="utf-8-sig").readlines()]
        # print(self.file)
        self.wait_time = 0
        self.wait = 0
        self.iterator = 0
        self.moving_objects = []

    def update(self):
        # print(self.wait, self.wait_time)
        if not dialog:
            if self.wait == self.wait_time:
                if pygame.sprite.spritecollideany(self, spike) or self.iterator != 0:
                    # print(spiike.rect)
                    # print(self.file)
                    self.do_event()
            else:
                self.wait += 1
        for j in self.moving_objects:
            random_objects_slovar[j[0]].rect.x += j[1]
            random_objects_slovar[j[0]].rect.y += j[2]

    def do_event(self):
        while True:
            # print(self.file[self.iterator])
            command = self.file[self.iterator][0].strip()
            # print(command)
            if command == 'wait':
                self.wait_time = int(self.file[self.iterator][1])
                self.wait = 0
                self.iterator += 1
                break
            elif command == 'ctrl':
                self.ctrl(int(self.file[self.iterator][1]))
            elif command == 'load_room':
                for i in ev_block:
                    i.rect.topleft = 10000, 10000
                    i.kill()
                for i in enemies:
                    i.kill()
                for i in enemies_htb:
                    i.kill()
                for i in htb:
                    i.kill()
                for i in p_htb:
                    i.kill()
                for i in particles:
                    i.kill()
                for i in moneyy:
                    i.kill()
                random_objects_group.empty()
                random_objects_group2.empty()
                bckg4.image = pygame.image.load(self.file[self.iterator][1].strip()).convert_alpha()
                bckg4.rect = bckg4.image.get_rect()
                # print(bckg1.rect.topleft, bckg4.rect.topleft)
                bckg1.rect.bottomleft = bckg4.rect.bottomleft
                ###
                camera.change_size(bckg4.image.get_width(), bckg4.image.get_height())
                # print(self.file[self.iterator][1])
            elif command == 'change_bg':
                for i in htb:
                    i.kill()
                for i in p_htb:
                    i.kill()
                bckg4.image = pygame.image.load(self.file[self.iterator][1].strip()).convert_alpha()
                bckg4.rect = bckg4.image.get_rect()
                bckg1.rect.bottomleft = bckg4.rect.bottomleft
                camera.change_size(bckg4.image.get_width(), bckg4.image.get_height())
            elif command == 'ev':
                if len(self.file[self.iterator]) <= 6:
                    EventBlock(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                               int(self.file[self.iterator][3]), int(self.file[self.iterator][4]),
                               self.file[self.iterator][5].strip())
                else:
                    if int(self.file[self.iterator][6]) == next_necessary_cutscene:
                        EventBlock(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                                   int(self.file[self.iterator][3]), int(self.file[self.iterator][4]),
                                   self.file[self.iterator][5].strip())
                        # print(next_necessary_cutscene)
            elif command == 'del_htb':
                for i in htb:
                    i.kill()
                for i in p_htb:
                    i.kill()
            elif command == 'music':
                if self.file[self.iterator][1].strip() == 'stop':
                    pygame.mixer.music.fadeout(int(self.file[self.iterator][2]))
                elif self.file[self.iterator][1].strip() == 'pause':
                    pygame.mixer.music.pause()
                elif self.file[self.iterator][1].strip() == 'unpause':
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.load(self.file[self.iterator][1].strip())
                    pygame.mixer.music.play(-1)
            elif command == 'obj':
                if len(self.file[self.iterator]) <= 5:
                    obj = pygame.sprite.Sprite(random_objects_group)
                    obj.image = pygame.image.load(self.file[self.iterator][4].strip()).convert_alpha()
                    obj.rect = obj.image.get_rect()
                    obj.rect.topleft = int(self.file[self.iterator][2]), int(self.file[self.iterator][3])
                    self.objcr(self.file[self.iterator][1].strip(), obj)
                else:
                    if int(self.file[self.iterator][5]) == next_necessary_cutscene:
                        obj = pygame.sprite.Sprite(random_objects_group)
                        obj.image = pygame.image.load(self.file[self.iterator][4].strip()).convert_alpha()
                        obj.rect = obj.image.get_rect()
                        obj.rect.topleft = int(self.file[self.iterator][2]), int(self.file[self.iterator][3])
                        self.objcr(self.file[self.iterator][1].strip(), obj)

            elif command == 'obj_move':
                self.moving_objects.append([self.file[self.iterator][1].strip(), int(self.file[self.iterator][2]),
                                            int(self.file[self.iterator][3])])
            elif command == 'obj_del':
                random_objects_slovar[self.file[self.iterator][1].strip()].image = pygame.Surface([0, 0])
            elif command == 'obj_stop':
                for i in range(len(self.moving_objects)):
                    if self.moving_objects[i][0] == self.file[self.iterator][1].strip():
                        self.moving_objects.pop(i)
                        break
            elif command == 'sound':
                sound = pygame.mixer.Sound(self.file[self.iterator][1].strip())
                sound.set_volume(float(self.file[self.iterator][2]))
                sound.play()
            elif command == 'trs':
                self.trs(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]))
            elif command == 'dir':
                spiike.direction = int(self.file[self.iterator][1])
            elif command == 'enemy':
                Enemy(self.file[self.iterator][1].strip(), int(self.file[self.iterator][2]),
                      int(self.file[self.iterator][3]),
                      (int(self.file[self.iterator][4]), int(self.file[self.iterator][5])),
                      (int(self.file[self.iterator][6]), int(self.file[self.iterator][7])),
                      (int(self.file[self.iterator][8]), int(self.file[self.iterator][9])),
                      int(self.file[self.iterator][10]), animated=bool(int(self.file[self.iterator][11])),
                      jump_anim=self.file[self.iterator][12].strip(), speed=int(self.file[self.iterator][13]),
                      anim_speed=int(self.file[self.iterator][14]), behavior=int(self.file[self.iterator][15]),
                      range=int(self.file[self.iterator][16]), particles=self.file[self.iterator][17].strip(),
                      hp=int(self.file[self.iterator][18]), dmg=int(self.file[self.iterator][19]),
                      atk_anim=self.file[self.iterator][20].strip(), loot=int(self.file[self.iterator][21]),
                      death_sound=self.file[self.iterator][22].strip(), jump_sound=self.file[self.iterator][23].strip())
                # Enemy('entity/slime/idle.png', 2, 1, (100, 90), (40, 50), (30, 60), 0, animated=True,
                #       jump_anim='entity/slime/jump.png',
                #       speed=3, anim_speed=8, behavior=2, range=300, particles='particles/slime.png', hp=100, dmg=9)
            elif command == 'hitbox':
                if len(self.file[self.iterator]) <= 5:
                    Border(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                           int(self.file[self.iterator][3]), int(self.file[self.iterator][4]))
                else:
                    Border(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                           int(self.file[self.iterator][3]), int(self.file[self.iterator][4]),
                           material=self.file[self.iterator][5].strip())
            elif command == 'phitbox':
                if len(self.file[self.iterator]) <= 5:
                    PassableBorder(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                                   int(self.file[self.iterator][3]), int(self.file[self.iterator][4]))
                else:
                    PassableBorder(int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                                   int(self.file[self.iterator][3]), int(self.file[self.iterator][4]),
                                   material=self.file[self.iterator][5].strip())
            elif command == 'spike_pos':
                spiike.rect.x = int(self.file[self.iterator][1])
                spiike.rect.y = int(self.file[self.iterator][2])
            elif command == 'ulk_dash':
                self.ulk_dash()
            elif command == 'spike_move':
                spiike.xspeed = int(self.file[self.iterator][1])
                spiike.yspeed = int(self.file[self.iterator][2])
            elif command == 'hp':
                spiike.invis = True
                update_hp(int(self.file[self.iterator][1]))
                pygame.time.set_timer(INVISIBILITY, 1000)
                if hp1 <= 0:
                    self.kill()
                    break
            elif command == 'cng_trs':
                self.cng_trs([int(self.file[self.iterator][1]), int(self.file[self.iterator][2]),
                              int(self.file[self.iterator][3])])
            elif command == 'dialog':
                self.dialog(self.file[self.iterator][1].strip())
                self.iterator += 1
                break
            elif command == 'cutscene':
                self.cutsc(bool(int(self.file[self.iterator][1])))
            elif command == 'nxt_ctsc':
                self.nxt_ctsc()
            elif command == 'save':
                self.savee(self.file[self.iterator][1].strip())
            elif command == 'end':
                self.kill()
                break
            elif command == 'end_wo_kill':
                self.wait_time = 0
                self.wait = 0
                self.iterator = 0
                break
            self.iterator += 1
            # print(self.iterator)

    def savee(self, file):
        global save_money, save_location, save_next_event, save_kvas
        save_money = money
        save_kvas = kvas_counter
        # save_hp = hp1
        save_location = file
        save_next_event = next_necessary_cutscene
        # print(save_money, save_hp, save_location, save_next_event)

    def ulk_dash(self):
        global dash_unlocked
        dash_unlocked = True

    def objcr(self, name, ob):
        random_objects_slovar[name] = ob

    def nxt_ctsc(self):
        global next_necessary_cutscene
        next_necessary_cutscene += 1

    def cng_trs(self, file):
        global trs_color
        trs_color = file

    def cutsc(self, bl):
        global cutscene
        cutscene = bl

    def trs(self, dire, sp):
        global transition, trs_speed  # , temp
        # if dire == 1:
        #     temp = 0
        # elif dire == 3:
        #     temp = 255
        transition = dire
        trs_speed = sp

    def ctrl(self, ct):
        global turn_off_ctrl, dash, left, right, up
        if ct == 1:
            turn_off_ctrl = True
            dash = left = right = up = False
            spiike.xspeed = 0
            pygame.time.set_timer(pygame.USEREVENT, 0)
        else:
            turn_off_ctrl = False

    def dialog(self, stri):
        global dialog, dtext, dtrect, dia_sp
        dialog = True
        dia_sp.clear()
        for i in range(len(stri) // 48):
            dia_sp.append(font1.render(stri[:48], True, (255, 255, 255)))
            stri = stri[48:]
        if stri:
            dia_sp.append(font1.render(stri, True, (255, 255, 255)))

        # dtext = font1.render(str, True, (255, 255, 255))
        # dtrect = dtext.get_rect()
        # dtrect.topleft = (50, 35)
        # 48


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, ticks, loop=True, group=None):
        if not group:
            group = all_spr
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = self.ticks = ticks
        self.dlina = len(self.frames)
        self.loop = loop

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.counter == self.ticks and not (not self.loop and self.cur_frame == self.dlina - 1):
            self.cur_frame = (self.cur_frame + 1) % self.dlina
            self.image = self.frames[self.cur_frame]
            self.counter = 0
        self.counter += 1


class Particle(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        super().__init__(particles)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect()
        self.add(particles)
        self.rect.x = x + random.choice(range(-1, 2))
        self.rect.y = y + random.choice(range(-1, 2))
        self.xspeed = random.choice([-1, 1])
        self.yspeed = random.choice(range(-1, 2))

    def update(self):
        self.yspeed += g
        self.rect.y += self.yspeed
        self.rect.x += self.xspeed
        if self.rect.y >= 980:
            self.kill()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, material='grass'):
        super().__init__()
        self.add(htb)
        self.image = pygame.Surface([x2 - x1, y2 - y1])
        pygame.draw.rect(self.image, (0, 0, 0), (x1, y1, x2 - x1, y2 - y1))
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.material = material


class PassableBorder(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, material='grass'):
        super().__init__()
        self.add(p_htb)
        self.image = pygame.Surface([x2 - x1, y2 - y1])
        pygame.draw.rect(self.image, (0, 0, 0), (x1, y1, x2 - x1, y2 - y1))
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.material = material


class Money(pygame.sprite.Sprite):
    def __init__(self, x, y, nominal):
        super().__init__()
        self.image = pygame.image.load('entity/coin/idle.png')
        self.rect = self.image.get_rect()
        self.add(moneyy)
        self.nominal = nominal
        self.rect.x = x
        self.rect.y = y
        self.xspeed = random.choice(range(-2, 3))
        self.yspeed = random.choice(range(6))
        self.iter = 0

    def update(self):
        self.yspeed += g
        self.rect.y += self.yspeed
        self.collide(0, self.yspeed)
        if self.xspeed:
            self.rect.x += self.xspeed
            self.collide(self.xspeed, 0)
        self.iter += 1
        if self.iter >= 900:
            self.kill()

    def collide(self, x_sp, y_sp):
        coly = pygame.sprite.spritecollideany(self, htb)
        if coly:
            if y_sp > 0:
                self.rect.bottom = coly.rect.top
                self.yspeed = 0
                self.xspeed = 0
            if y_sp < 0:
                self.rect.top = coly.rect.bottom
                self.yspeed = 0
            if x_sp > 0:
                self.rect.right = coly.rect.left
                self.xspeed = -self.xspeed
            if x_sp < 0:
                self.rect.left = coly.rect.right
                self.xspeed = -self.xspeed
        colp = pygame.sprite.spritecollideany(self, spike)
        if colp:
            update_money(self.nominal)
            self.kill()


class Attack(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, dmg, xsp=0, ysp=0, type='gun'):
        super().__init__()
        if type == 'gun':
            self.image = pygame.Surface([12, 12])
            self.rect = pygame.Rect(0, 0, 12, 12)
            self.sup = pygame.sprite.Sprite(atk)
            self.sup.image = pygame.image.load(sprite)
            self.sup.rect = pygame.Rect(0, 0, 12, 12)

        else:
            pass
        self.type = type
        self.add(atk_htb)
        self.start_x = x
        self.rect.x = x
        self.rect.y = y
        self.xspeed = xsp
        self.yspeed = ysp
        self.sup.rect.x = self.rect.x
        self.sup.rect.y = self.rect.y

    def update(self):
        if self.type == 'gun':
            self.rect.y += self.yspeed
            self.collide()
            self.rect.x += self.xspeed
            self.collide()
            self.sup.rect.x = self.rect.x
            self.sup.rect.y = self.rect.y
            if abs(self.rect.x - self.start_x) > 350:
                self.sup.kill()
                self.kill()
        else:
            pass

    def collide(self):
        coly = pygame.sprite.spritecollideany(self, htb)
        if coly:
            for i in range(4):
                Particle('particles/gun.png', self.rect.x, self.rect.y)
            self.sup.kill()
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite, col, row, coords, hitbox, offset, atk_prop, behavior=0, animated=False, anim_speed=4,
                 jump_anim=None, atk_anim=None, speed=4, range=300, dmg=10, hp=100,
                 particles='particles/blood.png', loot=5, death_sound='sounds/slimedth.wav',
                 jump_sound='sounds/slime.mp3'):
        super().__init__(enemies_htb)
        self.image = pygame.Surface(hitbox)
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, hitbox[0], hitbox[1]])
        self.rect = self.image.get_rect()
        if not animated:
            self.spr = pygame.sprite.Sprite(enemies)
            self.spr.image = pygame.image.load(sprite).convert_alpha()
            self.spr.rect = self.spr.image.get_rect()
        else:
            self.spr = AnimatedSprite(pygame.image.load(sprite).convert_alpha(), col, row, 0, 0, anim_speed,
                                      group=enemies)
        if jump_anim:
            self.js = pygame.mixer.Sound(jump_sound)
            self.jump_anim = True
            self.ja = pygame.sprite.Sprite()
            self.ja.image = pygame.image.load(jump_anim).convert_alpha()
            self.ja.rect = self.ja.image.get_rect()
        else:
            self.jump_anim = False
        self.atk_anim = False
        self.ds = pygame.mixer.Sound(death_sound)
        self.loot = loot
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        if isinstance(speed, int):
            self.enemyspeed = self.needspeed = speed
            if behavior != 5:
                self.yspeed = 0
            else:
                self.yspeed = -5
            self.xspeed = 0
        else:
            self.enemyspeed = self.needspeed = speed[0]
            self.xspeed = speed[0]
            self.yspeed = speed[1]
        self.jumpstrength = 8
        self.direction = -1
        self.behavior = behavior
        self.offset = offset
        self.dmg = dmg
        self.hp = hp
        self.partc = particles
        self.atk_timer = 0
        if behavior == 2:
            self.jump_timer = 0
        elif behavior == 3:
            self.aa = AnimatedSprite(pygame.image.load(atk_anim).convert_alpha(), col, row, 0, 0, anim_speed,
                                     loop=False, group=enemies)
            self.att_s = pygame.mixer.Sound('sounds/log_shoot.mp3')
        elif behavior == 4 or behavior == 6:
            self.xspeed = self.enemyspeed
            self.spr.rect.x = self.rect.x - self.offset[0]
            self.spr.rect.y = self.rect.y - self.offset[1]
        elif behavior == 5:
            self.aa1 = AnimatedSprite(pygame.image.load('entity/leshiy/attack1.png').convert_alpha(), 3, 1, 0, 0,
                                      4,
                                      loop=False, group=enemies)
            self.aa2 = AnimatedSprite(pygame.image.load('entity/leshiy/attack2.png').convert_alpha(), 5, 1, 0, 0,
                                      4, loop=False, group=enemies)
            self.xspeed = -1
            pygame.time.set_timer(WALKIN, 1000)
            self.atk_timer = 240
        self.onGround = False
        self.range = range
        self.phase = 1

    def update(self, spike_x, spike_y):
        if self.behavior == 0:
            if -self.range <= spike_x - self.rect.x <= self.range:
                if spike_x >= self.rect.x:
                    self.needspeed = self.enemyspeed
                else:
                    self.needspeed = -self.enemyspeed
                if self.xspeed != self.needspeed:
                    if self.needspeed > 0:
                        self.xspeed += 0.5
                    else:
                        self.xspeed -= 0.5
                if spike_y < self.rect.y and self.onGround:
                    self.yspeed -= self.jumpstrength
                    self.onGround = False
            else:
                self.xspeed = 0
        elif self.behavior == 2:
            s = spike_x - self.rect.x
            if -self.range <= s <= self.range:
                if self.jump_timer == 60 and self.onGround:
                    if spike_x > self.rect.x:
                        self.xspeed = s / 50 if s / 50 < self.enemyspeed else self.enemyspeed
                    else:
                        self.xspeed = s / 50 if s / 50 > -self.enemyspeed else -self.enemyspeed
                    self.yspeed = -self.jumpstrength * 0.8 if -self.enemyspeed < s / 50 < self.enemyspeed else \
                        -self.jumpstrength
                    self.onGround = False
                    self.jump_timer = 0
                    self.js.play()
                if self.onGround:
                    self.xspeed = 0
                    self.jump_timer += 1
            if self.onGround:
                self.xspeed = 0
        elif self.behavior == 3:
            if -self.range <= spike_x - self.rect.x <= 0:
                if self.atk_timer == 60:
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 10), (36, 36), (0, 0),
                          0, speed=-5, behavior=4, dmg=self.dmg, hp=15, particles='particles/bullet.png', loot=0,
                          death_sound='sounds/logdth.wav')
                    self.att_s.play()
                    self.atk_timer = 0
                    self.atk_anim = True
                    self.aa.counter = 4
                    self.aa.cur_frame = -1
                else:
                    self.atk_timer += 1
        elif self.behavior == 5:
            # print(self.atk_timer)
            if self.atk_timer == 360:
                atkk = random.choice([1, 2])
                # atkk = 2
                if atkk == 1:
                    self.atk_anim = True
                    self.aa = self.aa1
                    self.aa.counter = 4
                    self.aa.cur_frame = -1
                    pygame.mixer.Sound('sounds/boss1_atk_sound1.mp3').play()
                    if self.phase == 2:
                        pygame.time.set_timer(BOSSA1, 500)
                    else:
                        pygame.time.set_timer(BOSSA1, 800)
                else:
                    self.atk_anim = True
                    self.aa = self.aa2
                    self.aa.counter = 4
                    self.aa.cur_frame = -1
                    pygame.mixer.Sound('sounds/boss1_bird_sound.mp3').play()
                    if self.phase == 2:
                        pygame.time.set_timer(BOSSA2, 400)
                    else:
                        pygame.time.set_timer(BOSSA2, 500)
                    # pygame.mixer.Sound('sounds/bird.mp3').play()
                self.atk_timer = 0
            elif self.atk_timer == 240:
                self.atk_anim = False
                pygame.time.set_timer(BOSSA2, 0)
                pygame.time.set_timer(BOSSA1, 0)
                self.atk_timer += 1
            else:
                self.atk_timer += 1
        if self.xspeed >= 0:
            self.direction = 1
        else:
            self.direction = -1
        if self.behavior != 4 and self.behavior != 6:
            self.yspeed += g
        self.rect.y += self.yspeed
        self.collide(0, self.yspeed)
        if self.behavior != 5:
            self.rect.x += self.xspeed
        else:
            if not self.atk_anim:
                self.rect.x += self.xspeed
        self.collide(self.xspeed, 0)
        self.collideatk()
        if self.jump_anim and not self.onGround:
            self.ja.rect.x = self.rect.x - self.offset[0]
            self.ja.rect.y = self.rect.y - self.offset[1]
            self.ja.add(enemies)
        elif self.atk_anim:
            self.aa.rect.x = self.rect.x - self.offset[0]
            self.aa.rect.y = self.rect.y - self.offset[1]
            self.aa.add(enemies)
        else:
            self.spr.rect.x = self.rect.x - self.offset[0]
            self.spr.rect.y = self.rect.y - self.offset[1]
            self.spr.add(enemies)
        if self.behavior == 6:
            if not (-150 < self.rect.x < 790):
                self.kill()

    def collideatk(self):
        colatt = pygame.sprite.spritecollideany(self, atk_htb)
        if colatt:
            self.hp -= spiike.dmg
            # print(self.hp)
            for i in range(3):
                Particle('particles/gun.png', colatt.rect.x, colatt.rect.y)
            colatt.sup.kill()
            colatt.kill()
            if self.behavior == 5:
                if self.hp <= 500 and self.phase == 1:
                    pygame.mixer.Sound('sounds/boss1phase2.mp3').play()
                    self.phase = 2
                    self.xspeed *= 2
                    if not self.atk_anim:
                        self.yspeed = -5
            if self.hp <= 0:
                self.ds.play()
                for i in range(5):
                    Particle(self.partc, self.rect.centerx, self.rect.centery)
                if self.loot:
                    for i in range(self.loot):
                        Money(self.rect.centerx + random.randint(-3, 3), self.rect.y + random.randint(-3, 3), 1)
                if self.behavior == 5:
                    pygame.time.set_timer(BOSSA2, 0)
                    pygame.time.set_timer(BOSSA1, 0)
                    term = pygame.sprite.Sprite(random_objects_group2)
                    term.image = pygame.image.load('entity/leshiy/defeat.png')
                    term.rect = term.image.get_rect()
                    term.rect.topleft = self.spr.rect.topleft
                    exp = AnimatedSprite(pygame.image.load("spike/explosionbig.png"), 6, 3, 0, 0, 4, loop=False)
                    exp.rect.center = self.rect.center
                    exp.add(random_objects_group2)
                    Enemy('entity/bird/right.png', 6, 1, (self.rect.centerx, self.rect.y), (75, 75), (16, 16),
                          0, animated=True, speed=[5, -1], anim_speed=4, behavior=6, dmg=15, hp=10,
                          particles='particles/bullet.png', loot=100,
                          death_sound='sounds/logdth.wav')
                    EventBlock(0, 0, 640, 480, 'files/boss1defeat.txt')
                self.kill()

    def change_direction(self):
        if self.behavior == 5:
            self.xspeed *= -1

    def b1a1(self):
        if self.behavior == 5:
            if self.phase == 2:
                spd = 7
            else:
                spd = 5
            a = random.choice([1, 2])
            if a == 1:
                Enemy('entity/bird/left.png', 6, 1, (640, random.randint(0, 380)), (75, 75), (16, 16),
                      0, animated=True, anim_speed=4, speed=-spd, behavior=6, dmg=15, hp=15, loot=0,
                      death_sound='sounds/birddth.mp3')
            else:
                Enemy('entity/bird/right.png', 6, 1, (-100, random.randint(0, 380)), (75, 75), (16, 16),
                      0, animated=True, speed=spd, anim_speed=4, behavior=6, dmg=15, hp=15, loot=0,
                      death_sound='sounds/birddth.mp3')
            # pygame.mixer.Sound('sounds/feather.mp3').play()

    def b1a2(self):
        sin45 = math.sin(45)
        if self.behavior == 5:
            a = random.choice([1, 2])
            if a == 1:
                for i in [-5, 5]:
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[i, 0], behavior=4, dmg=self.dmg, hp=1000, particles='particles/bullet.png', loot=0,
                          death_sound='sounds/logdth.wav')
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[0, i], behavior=4, dmg=self.dmg, hp=1000, particles='particles/bullet.png', loot=0,
                          death_sound='sounds/logdth.wav')
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[i * sin45, i * sin45], behavior=4, dmg=self.dmg, hp=1000,
                          particles='particles/bullet.png',
                          loot=0, death_sound='sounds/logdth.wav')
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[i * sin45, -i * sin45], behavior=4, dmg=self.dmg, hp=1000,
                          particles='particles/bullet.png', loot=0,
                          death_sound='sounds/logdth.wav')
            else:
                for i in [-5, 5]:
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[i, i * 0.5], behavior=4, dmg=self.dmg, hp=1000, particles='particles/bullet.png',
                          loot=0, death_sound='sounds/logdth.wav')
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[i, -i * 0.5], behavior=4, dmg=self.dmg, hp=1000,
                          particles='particles/bullet.png', loot=0,
                          death_sound='sounds/logdth.wav')
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[i * 0.5, i], behavior=4, dmg=self.dmg, hp=1000, particles='particles/bullet.png',
                          loot=0, death_sound='sounds/logdth.wav')
                    Enemy('entity/bullet/idle.png', 1, 1, (self.rect.x - 15, self.rect.y + 20), (36, 36), (0, 0),
                          0, speed=[-i * 0.5, i], behavior=4, dmg=self.dmg, hp=1000,
                          particles='particles/bullet.png', loot=0,
                          death_sound='sounds/logdth.wav')
        pygame.mixer.Sound('sounds/bossatk.mp3').play()

    # DODELAT'
    def collide(self, x_sp, y_sp):
        coly = pygame.sprite.spritecollideany(self, htb)
        if coly and self.behavior != 6:
            if self.behavior == 4:
                for i in range(3):
                    Particle('particles/bullet.png', self.rect.x, self.rect.y)
                self.kill()
            if y_sp > 0:
                self.rect.bottom = coly.rect.top
                self.onGround = True
                self.yspeed = 0
            if y_sp < 0:
                self.rect.top = coly.rect.bottom
                self.yspeed = 0
            if x_sp > 0:
                self.rect.right = coly.rect.left
                if self.behavior == 1:
                    self.xspeed = -self.xspeed
            if x_sp < 0:
                self.rect.left = coly.rect.right
                if self.behavior == 1:
                    self.xspeed = -self.xspeed

        colplayer = pygame.sprite.spritecollideany(self, spike)
        if self.behavior == 4:
            if colplayer and not spiike.invis:
                spiike.invis = True
                update_hp(-self.dmg)
                pygame.time.set_timer(INVISIBILITY, 500)
                for i in range(3):
                    Particle('particles/spike.png', self.rect.x, self.rect.y)
                self.kill()
        elif self.behavior == 0 or self.behavior == 2 or self.behavior == 3 or self.behavior == 5 or self.behavior == 6:
            if colplayer and not spiike.invis:
                spiike.invis = True
                update_hp(-self.dmg)
                pygame.time.set_timer(INVISIBILITY, 1000)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(spike)
        # cur_ima = pygame.image.load('spike/right.png')
        self.image = pygame.Surface([40, 50])
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, 40, 50])
        self.rect = self.image.get_rect()
        self.rect.x = 230
        self.rect.y = 0
        self.xspeed = 0
        self.yspeed = 0
        self.dmg = 10
        self.spd = 5
        self.dash_spd = 20
        self.onGround = False
        self.direction = 1  # 1 - pravo; -1 - levo
        self.invis = False
        self.zapushen_chem_to = False
        self.dis_ctrl = False
        self.cur_sound = pygame.mixer.Sound('sounds/walk_wood.wav')
        self.playsound = False

    def update(self, left, right, up, dash, g):
        if not dash:
            self.yspeed += g
            if up:
                if self.onGround:
                    self.yspeed = -jump
                    self.onGround = False
            if not self.onGround:
                if self.direction == -1:
                    spike_anim.empty()
                    L_JUMP.add(spike_anim)
                elif self.direction == 1:
                    spike_anim.empty()
                    R_JUMP.add(spike_anim)
                # ПОД ОГРОМНЫМ ВОПРОСОМ
                # НАДО СНОВА СДЕЛАТЬ СНИЖЕНИЕ СКОРОСТИ В ВОЗДУХЕ НО ПРИ ПОЛУЧЕНИИ УРОНА ОТКЛЮЧАТЬ УПРАВЛЕНИЕ НА ЧУТЬ ЧУТЬ
            if left and not self.zapushen_chem_to:
                if -self.spd <= self.xspeed:
                    self.xspeed = -self.spd
                elif self.onGround:
                    self.xspeed += 0.5
                self.direction = -1
                if self.onGround:
                    spike_anim.empty()
                    L_WALK.add(spike_anim)
                else:
                    spike_anim.empty()
                    L_JUMP.add(spike_anim)

            if right and not self.zapushen_chem_to:
                if self.spd >= self.xspeed:
                    self.xspeed = self.spd
                elif self.onGround:
                    self.xspeed -= 0.5
                self.direction = 1
                if self.onGround:
                    spike_anim.empty()
                    R_WALK.add(spike_anim)
                else:
                    spike_anim.empty()
                    R_JUMP.add(spike_anim)
            if not (left or right):
                if not cutscene:
                    if self.xspeed != 0:
                        # self.xspeed -= self.direction
                        self.xspeed = self.xspeed - 1 if self.xspeed > 0 else self.xspeed + 1
                        if 1 > self.xspeed > 0 or -1 < self.xspeed < 0:
                            self.xspeed = 0
                if self.direction == -1 and self.onGround:
                    spike_anim.empty()
                    L_IDLE.add(spike_anim)
                elif self.direction == 1 and self.onGround:
                    spike_anim.empty()
                    R_IDLE.add(spike_anim)
                if cutscene:
                    if self.xspeed < 0:
                        if self.onGround:
                            spike_anim.empty()
                            L_WALK.add(spike_anim)
                        else:
                            spike_anim.empty()
                            L_JUMP.add(spike_anim)
                    elif self.xspeed > 0:
                        if self.onGround:
                            spike_anim.empty()
                            R_WALK.add(spike_anim)
                        else:
                            spike_anim.empty()
                            R_JUMP.add(spike_anim)
            if attack:
                if self.direction == 1:
                    spike_anim.empty()
                    R_GUN.add(spike_anim)
                    # add here dmg
                else:
                    spike_anim.empty()
                    L_GUN.add(spike_anim)
        elif dash:
            if self.direction == 1:
                if not cutscene:
                    self.xspeed = self.dash_spd
                else:
                    self.xspeed = 0
                spike_anim.empty()
                R_DASH.add(spike_anim)
            else:
                if not cutscene:
                    self.xspeed = -self.dash_spd
                else:
                    self.xspeed = 0
                spike_anim.empty()
                L_DASH.add(spike_anim)
            self.yspeed = 0
        old_y = self.rect.y
        self.rect.y += self.yspeed
        self.collide(0, self.yspeed)
        if self.rect.y != old_y:
            self.onGround = False
        self.rect.x += self.xspeed
        if not cutscene and self.xspeed != 0 and not self.playsound and self.onGround:
            self.cur_sound.set_volume(0.2)
            self.cur_sound.play(-1)
            self.playsound = True
        elif cutscene or self.xspeed == 0 or not self.onGround:
            self.playsound = False
            self.cur_sound.fadeout(250)
        self.collide(self.xspeed, 0)

    def collide(self, x_sp, y_sp):
        # НЕ ТРОГАТЬ!!!!!!!!!!!!
        coly = pygame.sprite.spritecollideany(self, htb)
        if coly:
            if y_sp > 0:
                self.rect.bottom = coly.rect.top
                self.onGround = True
                self.zapushen_chem_to = False
                self.cur_sound = obj_material[coly.material]
                self.yspeed = 0
            if y_sp < 0:
                self.rect.top = coly.rect.bottom
                self.yspeed = 0
            if x_sp > 0:
                self.rect.right = coly.rect.left
                if not cutscene:
                    self.xspeed = 0
            if x_sp < 0:
                self.rect.left = coly.rect.right
                if not cutscene:
                    self.xspeed = 0
        colh = pygame.sprite.spritecollideany(self, p_htb)
        if colh:
            if y_sp > 0 and self.rect.bottom <= colh.rect.bottom:
                self.rect.bottom = colh.rect.top
                self.onGround = True
                self.cur_sound = obj_material[colh.material]
                self.zapushen_chem_to = False
                self.yspeed = 0


# class Text():
#     def __init__(self, font, x, y, color, text, speed=10):
#         self.txt = text
#         self.iterator = 0
#         font.render(self.txt[self.iterator], True, color)


def update_hp(dmg):
    global hp1, hp_text, hp, hp_rect, dead, turn_off_ctrl
    hp1 += dmg
    if hp1 > 0:
        if hp1 > 100:
            hp1 = 100
        if dmg < 0:
            dmg_sound.play()
        hp_text = font2.render(str(hp1), True, (255, 255, 255))
        if hp1 > 50:
            hp.image = hpgood
        elif 50 >= hp1 > 20:
            hp.image = hpmed
        else:
            hp.image = hplow
        hp_rect = hp_text.get_rect()
        hp_rect.center = (168, 56)
    else:
        hp_text = font2.render('0', True, (255, 255, 255))
        hp_rect = hp_text.get_rect()
        hp_rect.center = (168, 56)
        dead = True
        turn_off_ctrl = True
        pygame.time.set_timer(BOSSA2, 0)
        pygame.time.set_timer(BOSSA1, 0)
        # deadspike = pygame.sprite.Sprite(deathscr)
        # deadspike.image = pygame.image.load('spike/left.png')
        # deadspike.rect = deadspike.image.get_rect()
        # deadspike.rect.x = spiike.rect.x - 30
        # deadspike.rect.y = spiike.rect.y - 30
        pygame.mixer.music.stop()
        pygame.mixer.stop()


def update_money(nom):
    global money, money_text, money_rect
    money += nom
    money_text = font1.render(str(money), True, (255, 255, 255))
    money_rect = money_text.get_rect()
    money_rect.center = (168, 95)
    money_sound.play()


size = 640, 480
scr = pygame.display.set_mode(size, pygame.RESIZABLE, vsync=1)
fullscr = False
pygame.display.set_caption('PELMENI')
pygame.mixer.init()
all_spr = pygame.sprite.Group()
spike = pygame.sprite.Group()
spike_anim = pygame.sprite.Group()
all_spike_anim = pygame.sprite.Group()
atk_htb = pygame.sprite.Group()
atk = pygame.sprite.Group()
particles = pygame.sprite.Group()
bg = pygame.sprite.Group()
htb = pygame.sprite.Group()
p_htb = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies_htb = pygame.sprite.Group()
ev_block = pygame.sprite.Group()
dialogg = pygame.sprite.Group()
deathscr = pygame.sprite.Group()
starts = pygame.sprite.Group()
moneyy = pygame.sprite.Group()
random_objects_group = pygame.sprite.Group()
random_objects_group2 = pygame.sprite.Group()
pygame.font.init()
font1 = pygame.font.Font('Hardpixel.OTF', 20)
font2 = pygame.font.Font('vcrosdmonorusbyd.ttf', 25)
hp1 = 100
money = 0
kvas_counter = 3
dead = False
load_save = False
load_save2 = False
dead_counter = 0

pygame.mixer.music.load('music/menu.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

dia_sp = []
random_objects_slovar = {}
obj_material = {'grass': pygame.mixer.Sound('sounds/walk_grass.wav'),
                'wood': pygame.mixer.Sound('sounds/walk_wood.wav')}

turn_off_ctrl = True
# !AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
money_sound = pygame.mixer.Sound('sounds/money.wav')
money_sound.set_volume(0.5)
dash_sound = pygame.mixer.Sound('sounds/dash.wav')
dash_sound.set_volume(0.5)
dmg_sound = pygame.mixer.Sound('sounds/damage.mp3')
kvas_sound = pygame.mixer.Sound('sounds/kvas.mp3')

dw = pygame.sprite.Sprite(dialogg)
dw.image = pygame.image.load('ui/dialog.png').convert_alpha()
dw.rect = dw.image.get_rect()

ui = pygame.sprite.Group()
hp = pygame.sprite.Sprite(ui)
hpgood = pygame.image.load('ui/ui1.png').convert_alpha()
hpmed = pygame.image.load('ui/ui2.png').convert_alpha()
hplow = pygame.image.load('ui/ui3.png').convert_alpha()
hp.image = hpgood
hp.rect = hp.image.get_rect()
hp.rect.topleft = (15, 15)
kvas = pygame.sprite.Sprite(ui)
kvas.image = pygame.image.load('ui/kvas.png').convert_alpha()
kvas.rect = kvas.image.get_rect()
kvas.rect.topright = (615, 25)
hp_text = font2.render(str(hp1), True, (255, 255, 255))
hp_rect = hp_text.get_rect()
hp_rect.center = (168, 56)
money_text = font1.render(str(money), True, (255, 255, 255))
money_rect = money_text.get_rect()
money_rect.center = (168, 95)
kvas_text = font1.render(str(kvas_counter), True, (255, 255, 255))
kvas_rect = kvas_text.get_rect()
kvas_rect.center = (559, 91)
# save
save_money = 0
# save_hp = 100
save_next_event = 2
save_kvas = 3
save_location = 'files/load_startroom.txt'

# cur_im = pygame.image.load('map/forest/f_room2.png')
transition_scr = pygame.sprite.Sprite()
transition_scr.image = pygame.image.load('ui/trs.png').convert_alpha()
transition_scr.rect = 640, 480
trs_color = [5, 2, 0]
bckg1 = pygame.sprite.Sprite()
bckg4 = pygame.sprite.Sprite(bg)
bckg1.image = pygame.image.load('bg/for_bg.png').convert_alpha()
bckg4.image = pygame.image.load('map/cutscene/sh_room1.png').convert_alpha()
bckg4.rect = bckg4.image.get_rect()
bckg1.rect = bckg1.image.get_rect()
bckg1.rect.bottomleft = bckg4.rect.bottomleft
total_size = bckg4.rect.width, bckg4.rect.height
R_WALK = AnimatedSprite(pygame.image.load("spike/rightw.png").convert_alpha(), 4, 1, 0, 0, 6)
R_IDLE = pygame.sprite.Sprite()
R_IDLE.image = pygame.image.load('spike/right.png').convert_alpha()
R_IDLE.rect = R_IDLE.image.get_rect()
L_WALK = AnimatedSprite(pygame.image.load("spike/leftw.png").convert_alpha(), 4, 1, 0, 0, 6)
L_IDLE = pygame.sprite.Sprite()
L_IDLE.image = pygame.image.load('spike/left.png').convert_alpha()
L_IDLE.rect = L_IDLE.image.get_rect()
L_JUMP = pygame.sprite.Sprite()
L_JUMP.image = pygame.image.load('spike/leftj.png').convert_alpha()
L_JUMP.rect = L_JUMP.image.get_rect()
R_JUMP = pygame.sprite.Sprite()
R_JUMP.image = pygame.image.load('spike/rightj.png').convert_alpha()
R_JUMP.rect = R_JUMP.image.get_rect()
L_DASH = AnimatedSprite(pygame.image.load("spike/leftd.png").convert_alpha(), 7, 1, 0, 0, 1)
R_DASH = AnimatedSprite(pygame.image.load("spike/rightd.png").convert_alpha(), 7, 1, 0, 0, 1)
L_SWORD = AnimatedSprite(pygame.image.load("spike/lefts.png"), 4, 1, 0, 0, 4, loop=False)
R_SWORD = AnimatedSprite(pygame.image.load("spike/rights.png"), 4, 1, 0, 0, 4, loop=False)
L_GUN = AnimatedSprite(pygame.image.load("spike/leftg.png").convert_alpha(), 3, 1, 0, 0, 4, loop=False)
R_GUN = AnimatedSprite(pygame.image.load("spike/rightg.png").convert_alpha(), 3, 1, 0, 0, 4, loop=False)
# R_IDLE.add(all_spike_anim)
# L_IDLE.add(all_spike_anim)
# R_JUMP.add(all_spike_anim)
# L_JUMP.add(all_spike_anim)
# R_DASH.add(all_spike_anim)
# L_DASH.add(all_spike_anim)
# L_GUN.add(all_spike_anim)
# R_GUN.add(all_spike_anim)

black_border = pygame.Surface([200, 680])
pygame.draw.rect(black_border, (0, 0, 0), (640, 0, 200, 680))
black_border2 = pygame.Surface([640, 200])
pygame.draw.rect(black_border2, (0, 0, 0), (0, 480, 640, 200))

special_death_image = pygame.sprite.Sprite()
special_death_image.image = pygame.image.load('spike/right.png').convert_alpha()
special_death_image.rect = special_death_image.image.get_rect()
special_death_image.rect.center = 320, 240

cur = pygame.sprite.Sprite()
cur.image = pygame.image.load('ui/cursor.png')
cur.rect = cur.image.get_rect()

spiike = Player()
camera = Camera(camera_configure, total_size[0], total_size[1])
Border(-30, 392, 500, 480)
# Border(680, 425, 1310, 480)
# Border(40, 0, 50, 480)
# PassableBorder(200, 310, 600, 311)
# EventBlock(1310, 0, 1311, 480, 'files/load_room5from4.txt')
# EventBlock(-40, 0, -39, 480, 'files/load_room1.txt')
# Enemy('entity/slime/idle.png', 2, 1, (100, 90), (40, 50), (30, 60), 0, animated=True, jump_anim='entity/slime/jump.png',
#       speed=3, anim_speed=8, behavior=2, range=300, particles='particles/slime.png', hp=100, dmg=9)
# Enemy('entity/evil_log/idle.png', 3, 1, (900, 90), (50, 50), (55, 45), 0,
#       speed=0, behavior=3, range=300, atk_anim='entity/evil_log/atk.png', particles='particles/bullet.png', hp=100,
#       dmg=9)
# Border(350, 350, 450, 425)
clock = pygame.time.Clock()
g = 0.35
jump = 10
fps = 60
left = right = up = dash = attack = False
ATT_EV = pygame.USEREVENT + 1
d_cd = True
weapon_cd = 500
DASH_COOLDOWN = pygame.USEREVENT + 2
SWORD_COOLDOWN = pygame.USEREVENT + 3
SHOTGUN_COOLDOWN = pygame.USEREVENT + 4
INVISIBILITY = pygame.USEREVENT + 5
ZAPUSHEN = pygame.USEREVENT + 6
TURNOFFGAMEOVER = pygame.USEREVENT + 7
BOSSA1 = pygame.USEREVENT + 8
BOSSA2 = pygame.USEREVENT + 9
WALKIN = pygame.USEREVENT + 10
running = True
transition = 3
trs_speed = 10
temp = 255
start = False
dash_unlocked = False
pb_clicked = False
cutscene = True
dialog = False
pygame.mouse.set_visible(False)
next_necessary_cutscene = 3
###
menu = pygame.sprite.Sprite(starts)
menu.image = pygame.image.load('ui/menu.png').convert_alpha()
menu.rect = menu.image.get_rect()
play = pygame.sprite.Sprite(starts)
play.image = pygame.image.load('ui/pb.png').convert_alpha()
play.rect = play.image.get_rect()
play.rect.bottomright = 600, 440
###
# 108 238
##
while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEMOTION:
            cur.rect.topleft = e.pos
        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            print(spiike.rect.topleft)
        if not start:
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and play.rect.right >= e.pos[0] >= play.rect.left
                    and play.rect.bottom >= e.pos[1] >= play.rect.top and not pb_clicked):
                pb_clicked = True
                pygame.mixer.music.fadeout(1000)
                transition = 1
                trs_speed = 5
                temp = 1
        else:
            if load_save:
                if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or (e.type == pygame.KEYUP):
                    load_save2 = True
                    load_save = False
                    spiike.rect.topleft = 0, 0
                    EventBlock(0, 0, 10, 10, save_location)
                    pygame.time.set_timer(TURNOFFGAMEOVER, 500)
            if not turn_off_ctrl:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    up = True
                if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                    up = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                    left = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                    right = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_f:
                    if kvas_counter > 0:
                        kvas_counter -= 1
                        kvas_sound.play()
                        kvas_text = font1.render(str(kvas_counter), True, (255, 255, 255))
                        kvas_rect = kvas_text.get_rect()
                        kvas_rect.center = (559, 91)
                        update_hp(15)
                if e.type == pygame.KEYUP and e.key == pygame.K_d:
                    right = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LSHIFT:
                    if not dash and d_cd and dash_unlocked:
                        dash_sound.play()
                        dash = True
                        d_cd = False
                        R_DASH.counter = 1
                        R_DASH.cur_frame = -1
                        L_DASH.counter = 1
                        L_DASH.cur_frame = -1
                        pygame.time.set_timer(pygame.USEREVENT, 100)
                        pygame.time.set_timer(DASH_COOLDOWN, 800)
                if e.type == pygame.KEYUP and e.key == pygame.K_a:
                    left = False
                if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or (
                        e.type == pygame.KEYUP and e.key == pygame.K_h):
                    if not dash and not attack:
                        attack = True
                        R_GUN.counter = 4
                        R_GUN.cur_frame = -1
                        L_GUN.counter = 4
                        L_GUN.cur_frame = -1
                        dir = spiike.direction
                        pygame.time.set_timer(ATT_EV, weapon_cd)
                        spiike.xspeed -= dir * 7
                        spiike.yspeed -= 2.5
                        for i in range(3):
                            Attack('atk/gun.png', spiike.rect.centerx + 50 * dir, spiike.rect.y - 10, 0,
                                   random.choice(range(19, 22)) * dir,
                                   random.choice(range(-2, 3)))
                        pygame.mixer.Sound('sounds/shoot.mp3').play()
            else:
                up, left, right = False, False, False
            if e.type == pygame.USEREVENT:
                if not cutscene:
                    dash = False
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    spiike.xspeed = 7 * spiike.direction
            if e.type == BOSSA1:
                for i in enemies_htb:
                    i.b1a2()
            if e.type == BOSSA2:
                for i in enemies_htb:
                    i.b1a1()
            if e.type == WALKIN:
                for i in enemies_htb:
                    i.change_direction()
            if e.type == TURNOFFGAMEOVER:
                hp1 = 100
                money = save_money
                kvas_counter = save_kvas
                kvas_text = font1.render(str(kvas_counter), True, (255, 255, 255))
                kvas_rect = kvas_text.get_rect()
                kvas_rect.center = (559, 91)
                money_text = font1.render(str(money), True, (255, 255, 255))
                money_rect = money_text.get_rect()
                money_rect.center = (168, 95)
                update_hp(0)
                # next_necessary_cutscene=save_next_event
                dead = False
                load_save2 = False
                deathscr.empty()
                dead_counter = 0
                pygame.time.set_timer(TURNOFFGAMEOVER, 0)
            if e.type == ZAPUSHEN:
                spiike.zapushen_chem_to = False
                pygame.time.set_timer(ZAPUSHEN, 0)
            if e.type == DASH_COOLDOWN:
                d_cd = True
                pygame.time.set_timer(DASH_COOLDOWN, 0)
            if e.type == INVISIBILITY:
                spiike.invis = False
                pygame.time.set_timer(INVISIBILITY, 0)
                # раздвоить атаку, сделать список и доабвить кд
            if e.type == ATT_EV:
                attack = False
                pygame.time.set_timer(ATT_EV, 0)
        if dialog:
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or (
                    e.type == pygame.KEYUP and e.key == pygame.K_h):
                dialog = False

        if e.type == pygame.KEYDOWN and e.key == pygame.K_F11 and not fullscr:
            scr = pygame.display.set_mode(size, pygame.FULLSCREEN, vsync=1)
            fullscr = True
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11 and fullscr:
            scr = pygame.display.set_mode(size, vsync=1)
            fullscr = False

    # spike
    if start and not dead:
        scr.fill((0, 0, 0))
        spike.update(left, right, up, dash, g)
        enemies.empty()
        enemies_htb.update(spiike.rect.x, spiike.rect.y)
        enemies.update()
        spike_anim.update()
        if not attack:
            for spr in spike_anim:
                spr.rect.x = spiike.rect.x - 30
                spr.rect.y = spiike.rect.y - 30
        else:
            if spiike.direction == 1:
                for spr in spike_anim:
                    spr.rect.x = spiike.rect.x - 30
                    spr.rect.y = spiike.rect.y - 30
            else:
                for spr in spike_anim:
                    spr.rect.x = spiike.rect.x - 75
                    spr.rect.y = spiike.rect.y - 30
        particles.update()
        atk_htb.update()
        ev_block.update()
        moneyy.update()
        random_objects_group.update()
        random_objects_group2.update()
        camera.update(spiike)
        scr.blit(bckg1.image, camera.apply(bckg1, mod=0.5))
        for i in random_objects_group:
            scr.blit(i.image, camera.apply(i))
        scr.blit(bckg4.image, camera.apply(bckg4))
        for i in random_objects_group2:
            scr.blit(i.image, camera.apply(i))
        for i in moneyy:
            scr.blit(i.image, camera.apply(i))
        for i in spike_anim:
            scr.blit(i.image, camera.apply(i))
        for i in enemies:
            scr.blit(i.image, camera.apply(i))
        for i in atk:
            scr.blit(i.image, camera.apply(i))
        for i in particles:
            scr.blit(i.image, camera.apply(i))
        # for i in ev_block:
        #     scr.blit(i.image, camera.apply(i))
        # for i in p_htb:
        #     scr.blit(i.image, camera.apply(i))
        # if not turn_off_ctrl:
        if not cutscene:
            if spiike.rect.y > 130:
                ui.draw(scr)
                scr.blit(hp_text, hp_rect)
                scr.blit(money_text, money_rect)
                scr.blit(kvas_text, kvas_rect)
            else:
                for i in ui:
                    scr.blit(i.image, (i.rect.x, i.rect.y + 325))
                scr.blit(hp_text, (hp_rect.x, hp_rect.y + 325))
                scr.blit(money_text, (money_rect.x, money_rect.y + 325))
                scr.blit(kvas_text, (kvas_rect.x, kvas_rect.y + 325))
        if dialog:
            dialogg.draw(scr)
            for i in range(len(dia_sp)):
                scr.blit(dia_sp[i], (35, i * 25 + 25))
        # bg.draw(scr)
        # p_htb.draw(scr)
        # ev_block.draw(scr)
    elif dead:
        if dead_counter == 0:
            pygame.mixer.music.load('music/gameover.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            transition = 0
            temp = 0
            scr.fill((5, 2, 0))
            if spiike.rect.left >= bckg4.rect.width or spiike.rect.right <= 0 or spiike.rect.bottom <= 0 or spiike.rect.top >= bckg4.rect.height:
                scr.blit(special_death_image.image, special_death_image.rect)
            else:
                for i in spike_anim:
                    scr.blit(i.image, camera.apply(i))
        elif dead_counter == 170:
            death_exp = AnimatedSprite(pygame.image.load("spike/explosion.png"), 6, 3, 0, 0, 4, loop=False)
            death_exp.rect.center = spiike.rect.center
            death_exp.add(deathscr)
        elif 240 > dead_counter >= 170:
            scr.fill((5, 2, 0))
            if spiike.rect.left >= bckg4.rect.width or spiike.rect.right <= 0 or spiike.rect.bottom <= 0 or spiike.rect.top >= bckg4.rect.height:
                scr.blit(death_exp.image, (250, 140))
            else:
                scr.blit(death_exp.image, camera.apply(death_exp))
        elif dead_counter == 240:
            deathscr.empty()
            dth = pygame.sprite.Sprite(deathscr)
            d_im = random.choice(['ui/gameover1.png', 'ui/gameover2.png', 'ui/gameover3.png', 'ui/gameover4.png'])
            dth.image = pygame.image.load(d_im).convert_alpha()
            dth.rect = dth.image.get_rect()
            transition = 3
            trs_speed = 2
            temp = 255
            load_save = True
        elif dead_counter >= 240:
            deathscr.draw(scr)
        if dead_counter <= 241:
            dead_counter += 1
        if load_save2:
            ev_block.update()
        deathscr.update()
    else:
        starts.draw(scr)
    # htb.draw(scr)
    if transition == 1:
        transition_scr.image.fill((*trs_color, temp))
        temp += trs_speed
        if temp >= 255:
            transition_scr.image.fill((*trs_color, 255))
            transition = 2
            temp = 255
        scr.blit(transition_scr.image, (0, 0))
    elif transition == 2:
        scr.blit(transition_scr.image, (0, 0))
        if not start:
            start = True
            turn_off_ctrl = True
            spiike.rect.bottomleft = 130, 390
            transition = 3
            trs_speed = 5
            temp = 255
            cutscene = False
            dash_unlocked = True
            EventBlock(0, 0, 640, 480, 'files/load_room7save.txt')
            # EventBlock(0, 0, 640, 480, 'files/cutscene1.txt')

    elif transition == 3:
        transition_scr.image.fill((*trs_color, temp))
        temp -= trs_speed
        if temp <= 0:
            transition_scr.image.fill((*trs_color, 0))
            transition = 0
            temp = 0
        scr.blit(transition_scr.image, (0, 0))
    if pygame.mouse.get_focused() and not dead:
        scr.blit(cur.image, cur.rect)
    if fullscr:
        scr.blit(black_border, (640, 0))
        scr.blit(black_border2, (0, 480))
    # atk.draw(scr)
    # spike_anim.draw(scr)
    # enemies.draw(scr)
    # particles.draw(scr)
    # atk_htb.draw(scr)
    # enemies_htb.draw(scr)
    # spike.draw(scr)
    # scr.blit(image,(0,0))

    pygame.display.flip()

pygame.quit()
