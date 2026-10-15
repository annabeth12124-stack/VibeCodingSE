# Memory Color Pattern Repair Lab

This project is a pattern recall memory game (Simon-style) using **Pygame**. It introduces students to finite state machines (`WATCH`, `PLAYER_TURN`, `GAME_OVER`), time-based sequence playback, index-matching input validation, and grid-based visual button feedback within an object-oriented codebase.
---

## What's Provided

A working Memory Color Pattern game with:

- A 2x2 grid of four colored buttons (Red, Blue, Green, Yellow) with dim and illuminated lighting states
- Automated timed playback that flashes the sequence step-by-step for the player to watch
- Click detection registering player inputs and checking order against the target sequence
- Score tracking, visual turn indicators, and a Game Over overlay with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left-click colored pads to repeat the sequence. Press R to restart after Game Over.


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the sequence duplication bug

Advancing to the next round causes the memory pattern to explode in length rather than extending by one step. Ensure that each successful round strictly appends a single new color step to the active sequence.

### Task 2: Implement dynamic playback acceleration

Sequences flash at the exact same slow, fixed speed throughout every round. Make the playback dynamically accelerate by decreasing the flash and pause durations as the player advances further into higher rounds.

### Task 3: Implement sound effects or audio frequencies

The memory puzzle is completely silent, relying only on visual illumination. Assign a distinct musical pitch or audio frequency to each of the four colored pads that sounds whenever a tile is flashed or clicked.

### Task 4: Implement a Player Turn Input Timer

Players currently have unlimited time to study the board between clicks. Introduce a dynamic countdown timer bar for the player's turn that triggers a game over if time expires before completing the pattern.

---

## Expected Behavior

- At the beginning of each round, the game displays the accumulated sequence step-by-step with illuminated button states.   
- Each round strictly appends one new step rather than duplicating previous patterns.  
- Left-clicking a pad illuminates it briefly and registers the player's guess.
- Entering any incorrect button immediately triggers the Game Over screen.
- Pressing R on the Game Over screen clears the sequence, score, and state back to round 1.
---

## Folder Structure

```
memory_color_pattern/
├── game/
│   ├── color_button.py
│   └── game_engine.py
├── main.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
