import random
import pygame


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Arm position
        self.arm_position = 0.0
        self.target_limit = 100.0
        self.last_key = None

        # Player stamina
        self.stamina = 100.0
        self.max_stamina = 100.0
        self.stamina_cost = 2.0
        self.stamina_recovery = 12.0
        self.counter_stamina_recovery = 30.0

        # Game state
        self.winner = None
        self.game_state = "PLAYING"

        # AI configuration: force units per second
        self.ai_strength = 8.0
        self.ai_state = "NORMAL"
        self.ai_state_timer = 0.0

        # AI cycle durations in seconds
        self.ai_normal_duration = 5.0
        self.ai_surge_duration = 2.5
        self.ai_cooldown_duration = 4.0

        # AI force multipliers
        self.ai_surge_multiplier = 2.5
        self.ai_cooldown_multiplier = 0.25

        # Counter-surge configuration
        self.counter_window_duration = 1.5
        self.counter_bonus_duration = 2.0
        self.counter_push_multiplier = 2.0

        self.counter_window_timer = 0.0
        self.counter_bonus_timer = 0.0

        self.counter_surge_available = False
        self.counter_surge_active = False
        self.counter_surge_used = False

        # Timing
        self.last_update_time = pygame.time.get_ticks()

        # Fonts
        self.font_big = pygame.font.SysFont(None, 44)
        self.font_med = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

    def handle_event(self, event):
        # Restart after Game Over
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type != pygame.KEYDOWN:
            return

        # Only arrow keys affect the arm
        if event.key not in (pygame.K_LEFT, pygame.K_RIGHT):
            return

        # Block input when stamina is exhausted
        if self.stamina <= 10:
            return

        # Require alternating arrow keys
        if event.key == self.last_key:
            return

        # Determine player push strength
        push_strength = 4.2

        if self.counter_surge_active:
            push_strength *= self.counter_push_multiplier

        # Push toward the player's winning threshold
        self.arm_position -= push_strength

        # Reduce stamina
        self.stamina = max(
            0.0,
            self.stamina - self.stamina_cost
        )

        self.last_key = event.key

        # Activate the bonus if the player reacts in time
        if self.counter_surge_available:
            self.activate_counter_surge()

    def activate_counter_surge(self):
        if not self.counter_surge_available:
            return

        if self.counter_surge_used:
            return

        self.counter_surge_available = False
        self.counter_surge_used = True
        self.counter_surge_active = True
        self.counter_bonus_timer = self.counter_bonus_duration

        print("COUNTER-SURGE ACTIVATED!")

    def update_ai_state(self, dt):
        previous_state = self.ai_state

        self.ai_state_timer += dt

        if self.ai_state == "NORMAL":
            if self.ai_state_timer >= self.ai_normal_duration:
                self.ai_state = "SURGE"
                self.ai_state_timer = 0.0
                print("AI POWER SURGE!")

        elif self.ai_state == "SURGE":
            if self.ai_state_timer >= self.ai_surge_duration:
                self.ai_state = "COOLDOWN"
                self.ai_state_timer = 0.0
                print("AI ENTERING COOLDOWN!")

        elif self.ai_state == "COOLDOWN":
            if self.ai_state_timer >= self.ai_cooldown_duration:
                self.ai_state = "NORMAL"
                self.ai_state_timer = 0.0
                print("AI RETURNING TO NORMAL!")

        # Open the counter-surge window when the surge ends
        if (
            previous_state == "SURGE"
            and self.ai_state == "COOLDOWN"
        ):
            self.counter_surge_available = True
            self.counter_window_timer = self.counter_window_duration

            self.counter_surge_used = False
            self.counter_surge_active = False
            self.counter_bonus_timer = 0.0

            print("COUNTER-SURGE WINDOW OPEN!")

    def get_ai_state_info(self):
        if self.ai_state == "SURGE":
            return (
                "POWER SURGE!",
                (255, 65, 65),
                self.ai_surge_duration
            )

        if self.ai_state == "COOLDOWN":
            return (
                "AI COOLDOWN",
                (70, 230, 130),
                self.ai_cooldown_duration
            )

        return (
            "AI NORMAL",
            (220, 220, 220),
            self.ai_normal_duration
        )

    def update(self):
        if self.game_state != "PLAYING":
            return

        current_time = pygame.time.get_ticks()

        dt = (
            current_time - self.last_update_time
        ) / 1000.0

        self.last_update_time = current_time

        # Avoid huge timer jumps after pauses
        dt = min(dt, 0.1)

        # Update AI state
        self.update_ai_state(dt)

        # Update counter-surge activation window
        if self.counter_surge_available:
            self.counter_window_timer -= dt

            if self.counter_window_timer <= 0:
                self.counter_window_timer = 0.0
                self.counter_surge_available = False
                print("COUNTER-SURGE WINDOW EXPIRED!")

        # Update active bonus
        if self.counter_surge_active:
            self.counter_bonus_timer -= dt

            if self.counter_bonus_timer <= 0:
                self.counter_bonus_timer = 0.0
                self.counter_surge_active = False
                print("COUNTER-SURGE BONUS ENDED!")

        # Determine AI force
        if self.ai_state == "SURGE":
            current_ai_strength = (
                self.ai_strength * self.ai_surge_multiplier
            )

        elif self.ai_state == "COOLDOWN":
            current_ai_strength = (
                self.ai_strength * self.ai_cooldown_multiplier
            )

        else:
            current_ai_strength = self.ai_strength

        # Apply time-based opposing computer force
        ai_variance = random.uniform(0.3, 1.0)

        self.arm_position += (
            current_ai_strength * ai_variance * dt
        )

        # Recover stamina
        if self.stamina < self.max_stamina:
            if self.counter_surge_active:
                recovery = self.counter_stamina_recovery
            else:
                recovery = self.stamina_recovery

            self.stamina = min(
                self.max_stamina,
                self.stamina + recovery * dt
            )

        # Check winning conditions
        if self.arm_position <= -self.target_limit:
            self.winner = "PLAYER"
            self.game_state = "GAME_OVER"

        elif self.arm_position >= self.target_limit:
            self.winner = "COMPUTER"
            self.game_state = "GAME_OVER"

    def reset(self):
        # Reset arm and stamina
        self.arm_position = 0.0
        self.stamina = 100.0
        self.last_key = None

        # Reset game state
        self.winner = None
        self.game_state = "PLAYING"

        # Reset AI cycle
        self.ai_state = "NORMAL"
        self.ai_state_timer = 0.0

        # Reset counter-surge
        self.counter_window_timer = 0.0
        self.counter_bonus_timer = 0.0

        self.counter_surge_available = False
        self.counter_surge_active = False
        self.counter_surge_used = False

        # Reset timing
        self.last_update_time = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((25, 28, 35))

        # Title
        title_surf = self.font_big.render(
            "ARM WRESTLE SHOWDOWN",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                12
            )
        )

        # Player and computer labels
        player_header = self.font_med.render(
            "PLAYER",
            True,
            (80, 160, 255)
        )

        computer_header = self.font_med.render(
            "COMPUTER",
            True,
            (255, 100, 80)
        )

        screen.blit(player_header, (60, 55))
        screen.blit(
            computer_header,
            (self.width - 150, 55)
        )

        # AI state indicator
        state_text, state_color, state_duration = (
            self.get_ai_state_info()
        )

        state_surface = self.font_med.render(
            state_text,
            True,
            state_color
        )

        screen.blit(
            state_surface,
            (
                self.width // 2 - state_surface.get_width() // 2,
                70
            )
        )

        # AI countdown
        remaining_time = max(
            0.0,
            state_duration - self.ai_state_timer
        )

        timer_text = self.font_small.render(
            f"Next change in: {remaining_time:.1f}s",
            True,
            (210, 210, 210)
        )

        screen.blit(
            timer_text,
            (
                self.width // 2 - timer_text.get_width() // 2,
                95
            )
        )

        # Counter-surge warning
        if self.counter_surge_available:
            warning_text = (
                f"COUNTER-SURGE AVAILABLE! "
                f"{self.counter_window_timer:.1f}s"
            )

            warning_surface = self.font_small.render(
                warning_text,
                True,
                (255, 220, 60)
            )

            screen.blit(
                warning_surface,
                (
                    self.width // 2 - warning_surface.get_width() // 2,
                    118
                )
            )

        elif self.counter_surge_active:
            bonus_text = (
                f"COUNTER-SURGE ACTIVE! "
                f"{self.counter_bonus_timer:.1f}s"
            )

            bonus_surface = self.font_small.render(
                bonus_text,
                True,
                (80, 255, 150)
            )

            screen.blit(
                bonus_surface,
                (
                    self.width // 2 - bonus_surface.get_width() // 2,
                    118
                )
            )

        # Table
        table_rect = pygame.Rect(
            40,
            145,
            self.width - 80,
            265
        )

        pygame.draw.rect(
            screen,
            (110, 50, 15),
            table_rect,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (70, 30, 8),
            table_rect,
            width=5,
            border_radius=14
        )

        pygame.draw.line(
            screen,
            (45, 18, 4),
            (self.width // 2, 145),
            (self.width // 2, 410),
            4
        )

        # Arm position
        offset_x = (
            self.arm_position / self.target_limit
        ) * 95

        hand_x = (
            self.width // 2
        ) + int(offset_x)

        hand_y = 250

        p_shoulder = (70, 330)
        p_elbow = (140, 225)

        c_shoulder = (self.width - 70, 330)
        c_elbow = (self.width - 140, 225)

        # Player arm
        pygame.draw.line(
            screen,
            (200, 145, 110),
            p_shoulder,
            p_elbow,
            32
        )

        pygame.draw.line(
            screen,
            (215, 160, 125),
            p_elbow,
            (hand_x, hand_y),
            26
        )

        pygame.draw.circle(
            screen,
            (185, 130, 95),
            p_elbow,
            18
        )

        # Computer arm
        pygame.draw.line(
            screen,
            (170, 110, 85),
            c_shoulder,
            c_elbow,
            32
        )

        pygame.draw.line(
            screen,
            (185, 125, 95),
            c_elbow,
            (hand_x, hand_y),
            26
        )

        pygame.draw.circle(
            screen,
            (150, 95, 70),
            c_elbow,
            18
        )

        # Clasped hands
        pygame.draw.circle(
            screen,
            (225, 175, 140),
            (hand_x, hand_y),
            24
        )

        pygame.draw.circle(
            screen,
            (160, 115, 85),
            (hand_x, hand_y),
            24,
            width=3
        )

        # Stamina
        stamina_label = self.font_med.render(
            "STAMINA",
            True,
            (220, 220, 220)
        )

        screen.blit(stamina_label, (40, 445))

        stamina_bg = pygame.Rect(
            140,
            448,
            240,
            22
        )

        stamina_fill = pygame.Rect(
            140,
            448,
            int(
                240 * (
                    self.stamina / self.max_stamina
                )
            ),
            22
        )

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            stamina_bg,
            border_radius=6
        )

        bar_color = (
            (60, 210, 100)
            if self.stamina > 25
            else (220, 60, 60)
        )

        pygame.draw.rect(
            screen,
            bar_color,
            stamina_fill,
            border_radius=6
        )

        # Exhaustion warning
        if self.stamina <= 10:
            exhausted_surface = self.font_med.render(
                "EXHAUSTED! RECOVERING...",
                True,
                (255, 65, 65)
            )

            screen.blit(
                exhausted_surface,
                (
                    self.width // 2
                    - exhausted_surface.get_width() // 2,
                    485
                )
            )

        # Game Over screen
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            win_text = (
                "PLAYER WINS THE MATCH!"
                if self.winner == "PLAYER"
                else "COMPUTER WINS!"
            )

            color = (
                (80, 240, 100)
                if self.winner == "PLAYER"
                else (240, 80, 80)
            )

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2 - text_surf.get_width() // 2,
                    self.height // 2 - 45
                )
            )

            restart_surf = self.font_med.render(
                "Press [R] to Rematch",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )