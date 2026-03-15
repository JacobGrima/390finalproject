############################################################
# ERIKSEN FLANKER TASK 
#
# This version includes:
# - participant ID input
# - instruction screen
# - practice block with feedback
# - main block without feedback
# - reaction time recording
# - accuracy scoring
# - trial counter
# - CSV data saving
# - final summary screen
#
# RESPONSE KEYS
# - LEFT ARROW  = respond left
# - RIGHT ARROW = respond right
#
# Please read the comment block above each function before editing.
# Most changes to task timing / number of trials can be made in the BASIC EXPERIMENT SETTINGS section near the top of the script.
############################################################


############################################################
# IMPORT LIBRARIES
#
# pygame   -> used to show stimuli and collect keyboard input
# random   -> used to randomly generate trial types
# csv      -> used to save collected data to a CSV file
# sys      -> used to safely exit the script
# os       -> used to create/check folders for saving files
# datetime -> used to add timestamps to saved data files
############################################################
import pygame
import random
import csv
import sys
import os
from datetime import datetime


############################################################
# START PYGAME
#
# pygame.init() must be called before using pygame functions.
############################################################
pygame.init()


############################################################
# BASIC EXPERIMENT SETTINGS
#
# These variables control the overall experiment behaviour.
# If the group wants to adjust the task later, this is one of
# the main places to modify values.
############################################################

# Window size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Create the experiment window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Window title shown at the top of the pygame window
pygame.display.set_caption("Eriksen Flanker Task")

# Clock controls how fast the program updates
clock = pygame.time.Clock()

# Fonts used in different parts of the task
font_large = pygame.font.SysFont(None, 90)   # large text (stimulus, big titles)
font_medium = pygame.font.SysFont(None, 48)  # medium text (feedback, headings)
font_small = pygame.font.SysFont(None, 34)   # smaller text (instructions, counter)

# Colours
BG = (255, 255, 255)   # white background
BLACK = (0, 0, 0)      # black text

# Response keys
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

# Timing values (milliseconds)
FIXATION_TIME = 500    # how long the fixation cross "+" appears
STIM_TIMEOUT = 2000    # max response window for each trial
ITI = 700              # inter-trial interval (blank screen after each trial)
FEEDBACK_TIME = 700    # how long practice feedback stays on screen

# Number of trials
PRACTICE_TRIALS = 4
MAIN_TRIALS = 20

# Folder where CSV files will be saved
DATA_FOLDER = "data"

# Create the data folder automatically if it does not exist
os.makedirs(DATA_FOLDER, exist_ok=True)


############################################################
# DRAW TEXT FUNCTION
#
# Purpose:
# This is a helper function to draw centered text on the screen.
#
# Inputs:
# - text: the string to display
# - font: which font object to use
# - x, y: the center position of the text on the screen
#
# Why use a helper?
# Because many parts of the experiment need to draw text:
# instructions, fixation, feedback, trial counter, summary, etc.
############################################################
def draw_text(text, font, x, y):
    surf = font.render(text, True, BLACK)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)


############################################################
# QUIT TASK FUNCTION
#
# Purpose:
# Safely closes the pygame window and exits the script.
#
# This is used whenever:
# - the participant clicks the window close button
# - the participant presses ESC
############################################################
def quit_task():
    pygame.quit()
    sys.exit()


############################################################
# WAIT FOR SPACE FUNCTION
#
# Purpose:
# Shows one instruction / transition / ending screen until the
# participant presses SPACE.
#
# Input:
# - lines: a list of strings to display line by line
#
# Example use:
# wait_for_space([
#     "Flanker Task",
#     "",
#     "Press SPACE to begin"
# ])
#
# ESC can always be used to quit the task.
############################################################
def wait_for_space(lines):
    while True:
        screen.fill(BG)

        # Starting y-position for the first line of text
        y = 250

        # Draw each line and move downward
        for line in lines:
            draw_text(line, font_small, SCREEN_WIDTH // 2, y)
            y += 45

        pygame.display.flip()

        # Check events while waiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_task()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_task()

                if event.key == pygame.K_SPACE:
                    return

        clock.tick(60)


############################################################
# GET PARTICIPANT ID
#
# Purpose:
# Lets the participant type an ID before the task starts.
#
# Why do this?
# The participant ID is used in the saved CSV filename so that
# data from different participants will not be mixed together.
#
# Example IDs:
# - P01
# - test1
# - S02
############################################################
def get_participant():
    pid = ""

    while True:
        screen.fill(BG)

        draw_text("Enter Participant ID", font_medium, SCREEN_WIDTH // 2, 250)
        draw_text("(letters/numbers only, then press ENTER)", font_small, SCREEN_WIDTH // 2, 300)
        draw_text(pid, font_large, SCREEN_WIDTH // 2, 380)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_task()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_task()

                # Press ENTER to confirm the typed ID
                if event.key == pygame.K_RETURN and pid != "":
                    return pid

                # BACKSPACE deletes the last typed character
                if event.key == pygame.K_BACKSPACE:
                    pid = pid[:-1]

                else:
                    # Only allow letters and numbers
                    if len(pid) < 20 and event.unicode.isalnum():
                        pid += event.unicode

        clock.tick(60)


############################################################
# FIXATION SCREEN
#
# Purpose:
# Shows a fixation cross "+" before each trial.
#
# Why include fixation?
# In attention tasks, fixation helps standardize where the
# participant is looking before the stimulus appears.
############################################################
def fixation():
    start = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start < FIXATION_TIME:
        screen.fill(BG)
        draw_text("+", font_large, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_task()

        clock.tick(60)


############################################################
# BLANK SCREEN
#
# Purpose:
# Shows a blank screen after each trial.
#
# Why include it?
# This creates an inter-trial interval (ITI), which separates
# one trial from the next.
############################################################
def blank():
    start = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start < ITI:
        screen.fill(BG)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_task()

        clock.tick(60)


############################################################
# SHOW FEEDBACK
#
# Purpose:
# Shows feedback after PRACTICE trials only.
#
# Possible feedback messages:
# - "Too Slow"   -> participant did not respond in time
# - "Correct"    -> response was correct
# - "Incorrect"  -> response was wrong
#
# Why only practice?
# The main block is usually run without trial-by-trial feedback.
############################################################
def show_feedback(result):
    if result["response"] == "no_response":
        message = "Too Slow"
    elif result["accuracy"] == 1:
        message = "Correct"
    else:
        message = "Incorrect"

    start = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start < FEEDBACK_TIME:
        screen.fill(BG)
        draw_text(message, font_medium, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_task()

        clock.tick(60)


############################################################
# CREATE ONE TRIAL
#
# Purpose:
# Randomly creates one Flanker trial.
#
# Two trial types:
# - congruent   -> flankers and target point the same direction
# - incongruent -> flankers and target point different directions
#
# Two target directions:
# - left
# - right
#
# Example stimuli:
# - congruent left   = <<<<<
# - congruent right  = >>>>>
# - incongruent left = >><>>
# - incongruent right= <<><<
#
# Returns:
# - trial_type  -> "congruent" or "incongruent"
# - direction   -> "left" or "right"
# - stim        -> the actual text stimulus to display
# - correct     -> which keyboard key is correct
# - label       -> human-readable correct response label
############################################################
def create_trial():
    trial_type = random.choice(["congruent", "incongruent"])
    direction = random.choice(["left", "right"])

    if trial_type == "congruent":
        if direction == "left":
            stim = "<<<<<"
            correct = LEFT_KEY
            label = "left"
        else:
            stim = ">>>>>"
            correct = RIGHT_KEY
            label = "right"

    else:
        if direction == "left":
            stim = ">><>>"
            correct = LEFT_KEY
            label = "left"
        else:
            stim = "<<><<"
            correct = RIGHT_KEY
            label = "right"

    return trial_type, direction, stim, correct, label


############################################################
# RUN ONE TRIAL
#
# Purpose:
# Runs one full trial from beginning to end.
#
# Trial flow:
# 1. Show fixation
# 2. Create one random trial
# 3. Present the stimulus
# 4. Wait for left/right response or timeout
# 5. Record:
#    - participant response
#    - accuracy
#    - reaction time
# 6. Show blank ITI
#
# Inputs:
# - trial_num  -> current trial number within the block
# - total      -> total number of trials in that block
# - block_name -> "practice" or "main"
#
# Output:
# A dictionary containing all trial data to save later.
############################################################
def run_trial(trial_num, total, block_name):
    fixation()

    # Randomly generate one trial
    trial_type, direction, stim, correct, label = create_trial()

    # Default values before participant responds
    responded = False
    response = "no_response"
    rt = None
    acc = 0

    # Start time for measuring reaction time
    start = pygame.time.get_ticks()

    # Keep showing the stimulus until timeout or response
    while pygame.time.get_ticks() - start < STIM_TIMEOUT and not responded:
        screen.fill(BG)

        # Show trial counter at the top
        draw_text(f"Trial {trial_num}/{total}", font_small, SCREEN_WIDTH // 2, 60)

        # Show stimulus in the center
        draw_text(stim, font_large, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_task()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_task()

                # LEFT ARROW response
                if event.key == LEFT_KEY:
                    rt = pygame.time.get_ticks() - start
                    response = "left"
                    responded = True

                    if correct == LEFT_KEY:
                        acc = 1

                # RIGHT ARROW response
                elif event.key == RIGHT_KEY:
                    rt = pygame.time.get_ticks() - start
                    response = "right"
                    responded = True

                    if correct == RIGHT_KEY:
                        acc = 1

        clock.tick(60)

    blank()

    return {
        "trial": trial_num,
        "block": block_name,
        "type": trial_type,
        "direction": direction,
        "stimulus": stim,
        "response": response,
        "accuracy": acc,
        "rt": rt
    }


############################################################
# SAVE DATA
#
# Purpose:
# Saves all collected trial data into a CSV file.
#
# File naming format:
# participantID_flanker_timestamp.csv
#
# Example:
# P01_flanker_20260315_153650.csv
#
# Why save as CSV?
# CSV is easy to open in Excel, R, Python, Jamovi, etc.
############################################################
def save_data(pid, data):
    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file = f"{DATA_FOLDER}/{pid}_flanker_{time}.csv"

    with open(file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return file


############################################################
# SUMMARY
#
# Purpose:
# Calculates summary statistics using MAIN trials only.
#
# Why only main trials?
# Practice trials are excluded because they are not part of the
# real experimental data.
#
# Output:
# - mean_rt -> average RT across valid main-trial responses
# - acc     -> percent correct in main trials
############################################################
def summary(data):
    # Keep only main block rows
    main_data = [d for d in data if d["block"] == "main"]

    # Keep only RT values that are not missing
    valid = [d["rt"] for d in main_data if d["rt"] is not None]

    # Mean RT
    if len(valid) > 0:
        mean_rt = round(sum(valid) / len(valid), 2)
    else:
        mean_rt = 0

    # Accuracy percentage
    if len(main_data) > 0:
        acc = round(sum(d["accuracy"] for d in main_data) / len(main_data) * 100, 2)
    else:
        acc = 0

    return mean_rt, acc


############################################################
# MAIN FUNCTION
#
# Purpose:
# Controls the full experiment flow.
#
# Full sequence:
# 1. Ask participant ID
# 2. Show instructions
# 3. Run practice block
# 4. Show feedback after each practice trial
# 5. Show transition screen
# 6. Run main block
# 7. Save all data
# 8. Show final summary screen
############################################################
def main():
    # Get participant ID first
    pid = get_participant()

    ########################################################
    # INSTRUCTIONS SCREEN
    ########################################################
    wait_for_space([
        "Flanker Task",
        "",
        "Respond to the CENTER arrow",
        "",
        "LEFT arrow key = left",
        "RIGHT arrow key = right",
        "",
        "Press SPACE to start practice"
    ])

    # This list will store ALL trials from both blocks
    results = []

    ########################################################
    # PRACTICE BLOCK
    #
    # Runs a smaller set of trials first.
    # Feedback is shown after each practice trial.
    ########################################################
    for i in range(1, PRACTICE_TRIALS + 1):
        res = run_trial(i, PRACTICE_TRIALS, "practice")
        results.append(res)
        show_feedback(res)

    ########################################################
    # PRACTICE END SCREEN
    #
    # Gives participant a transition before the real task.
    ########################################################
    wait_for_space([
        "Practice complete",
        "",
        "The real task will begin now",
        "No feedback will be shown",
        "",
        "Press SPACE to continue"
    ])

    ########################################################
    # MAIN BLOCK
    #
    # Runs the actual experimental trials.
    # No feedback is shown here.
    ########################################################
    for i in range(1, MAIN_TRIALS + 1):
        res = run_trial(i, MAIN_TRIALS, "main")
        results.append(res)

    ########################################################
    # SAVE DATA + CALCULATE SUMMARY
    ########################################################
    file = save_data(pid, results)

    mean_rt, acc = summary(results)

    ########################################################
    # FINAL SUMMARY SCREEN
    ########################################################
    wait_for_space([
        "Task Complete!",
        "",
        f"Mean RT (main trials): {mean_rt} ms",
        f"Accuracy (main trials): {acc} %",
        "",
        "Data saved to:",
        file,
        "",
        "Press SPACE to exit"
    ])

    quit_task()


############################################################
# START TASK
#
# This ensures main() runs only when this file is executed
# directly.
############################################################
if __name__ == "__main__":
    main()