import random
import pygame
from game.color_button import ColorButton
import math
import numpy as np


def generate_tone(frequency, duration=0.15, sample_rate=44100):
    samples = int(sample_rate * duration)
    wave = np.sin(
        2 * np.pi * frequency * np.arange(samples) / sample_rate
    )
    audio = (wave * 12000).astype(np.int16)
    stereo_audio = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(stereo_audio)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        pad_size = 130
        gap = 24
        start_x = width // 2 - pad_size - (gap // 2)
        start_y = 150

        self.buttons = [
            ColorButton(0, pygame.Rect(start_x, start_y, pad_size, pad_size), (110, 20, 20), (255, 50, 50)),                      # Red
            ColorButton(1, pygame.Rect(start_x + pad_size + gap, start_y, pad_size, pad_size), (15, 60, 150), (40, 170, 255)),   # Blue
            ColorButton(2, pygame.Rect(start_x, start_y + pad_size + gap, pad_size, pad_size), (15, 100, 30), (50, 255, 90)),    # Green
            ColorButton(3, pygame.Rect(start_x + pad_size + gap, start_y + pad_size + gap, pad_size, pad_size), (140, 110, 10), (255, 235, 40)), # Yellow
        ]

        pygame.mixer.init()

        self.tones = [
            generate_tone(261.63),  # Red: C4
            generate_tone(329.63),  # Blue: E4
            generate_tone(392.00),  # Green: G4
            generate_tone(523.25),  # Yellow: C5
        ]

        self.sequence = []
        self.player_input = []
        self.score = 0

        self.state = "WATCH"
        self.showing_step = 0
        self.step_start_time = 0
        self.flash_duration = 450
        self.pause_duration = 200
        self.is_flashing = False

        self.player_lit_button = None
        self.player_lit_start = 0
        self.player_flash_duration = 150
        self.turn_time_limit = 5000  # 5 seconds, in milliseconds
        self.player_turn_start = 0

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 28)

        self.start_next_round()

    def start_next_round(self):
        new_color = random.randint(0, 3)
        self.sequence.append(new_color)

        # Increase difficulty as the sequence grows.
        round_number = len(self.sequence)

        self.flash_duration = max(200, 450 - (round_number - 1) * 30)
        self.pause_duration = max(80, 200 - (round_number - 1) * 15)

        self.player_input.clear()
        self.state = "WATCH"
        self.showing_step = 0
        self.step_start_time = pygame.time.get_ticks()
        self.is_flashing = True
        self.buttons[self.sequence[0]].is_lit = True
        self.tones[self.sequence[0]].play()

    def update(self):
        now = pygame.time.get_ticks()

        if self.player_lit_button is not None:
            if now - self.player_lit_start >= self.player_flash_duration:
                self.player_lit_button.is_lit = False
                self.player_lit_button = None

        if self.state == "WATCH":
            current_btn_id = self.sequence[self.showing_step]

            if self.is_flashing:
                if now - self.step_start_time >= self.flash_duration:
                    self.buttons[current_btn_id].is_lit = False
                    self.is_flashing = False
                    self.step_start_time = now
            else:
                if now - self.step_start_time >= self.pause_duration:
                    self.showing_step += 1
                    if self.showing_step < len(self.sequence):
                        next_id = self.sequence[self.showing_step]
                        self.buttons[next_id].is_lit = True
                        self.tones[next_id].play()
                        self.is_flashing = True
                        self.step_start_time = now
                    else:
                        self.state = "PLAYER_TURN"
                        self.player_turn_start = now

    def handle_event(self, event):
        if self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if self.state == "PLAYER_TURN" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.contains(event.pos):
                    btn.is_lit = True
                    self.tones[btn.color_id].play()
                    self.player_lit_button = btn
                    self.player_lit_start = pygame.time.get_ticks()

                    self.register_player_click(btn.color_id)
                    break

    def register_player_click(self, color_id):
        self.player_input.append(color_id)
        current_idx = len(self.player_input) - 1

        if self.player_input[current_idx] != self.sequence[current_idx]:
            self.state = "GAME_OVER"
            return

        if len(self.player_input) == len(self.sequence):
            self.score += 1
            self.start_next_round()

    def reset(self):
        self.sequence.clear()
        self.player_input.clear()
        self.score = 0
        for btn in self.buttons:
            btn.is_lit = False
        self.player_lit_button = None
        self.start_next_round()

    def render(self, screen):
        screen.fill((22, 24, 30))

        title_surf = self.font_title.render("Memory Pattern Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 20))

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 60))

        status_text = "Watch the pattern..." if self.state == "WATCH" else "Your turn: Click the pattern!"
        if self.state == "PLAYER_TURN":
            elapsed = pygame.time.get_ticks() - self.player_turn_start

            if elapsed >= self.turn_time_limit:
                self.state = "GAME_OVER"
        status_color = (190, 195, 205) if self.state == "WATCH" else (80, 240, 130)
        status_surf = self.font_medium.render(status_text, True, status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 95))

        for btn in self.buttons:
            btn.render(screen)

        if self.state == "PLAYER_TURN":
            elapsed = pygame.time.get_ticks() - self.player_turn_start
            remaining = max(0, self.turn_time_limit - elapsed)
            fraction = remaining / self.turn_time_limit

            bar_x = 100
            bar_y = 475
            bar_width = 300
            bar_height = 14

            pygame.draw.rect(
                screen, (70, 70, 70),
                (bar_x, bar_y, bar_width, bar_height)
            )

            pygame.draw.rect(
                screen, (80, 220, 100),
                (bar_x, bar_y, int(bar_width * fraction), bar_height)
            )

        if self.state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_title.render("WRONG PATTERN! GAME OVER", True, (240, 70, 70))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_score_surf = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_score_surf, (self.width // 2 - final_score_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_medium.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
