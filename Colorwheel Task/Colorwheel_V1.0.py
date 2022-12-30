from psychopy import visual, core, gui, data, event, sound
import time as ts
import numpy as np 
import random, math
import pickle
import pandas as pd
from itertools import combinations

""" Functions """
# Selecting hue of memory items in single trial  
def select_hue(ss) :
    hue_array = list(range(360))
    target_hue = random.sample(hue_array, ss)
    
    return target_hue

# Selecting positions of stimuli in single trial 
def select_pos(stim_Pos, ss) :
    stim_Pos_coll = [[x, y] for x in stim_Pos for y in stim_Pos]
    random.shuffle(stim_Pos_coll)
    
    stim_Pos = random.sample(stim_Pos_coll, ss)
    
    return stim_Pos

# Selecting target between memory array in single trial
def select_target(ss) :
    target = random.choice(list(range(ss)))
    return target

# Drawing Colorwheel : The Colorwheel is a composite of 360 sectors with 1 of 360 Colors & 1 degree   
def drawing_Colorwheel(win, r, ori_angle) :
    Color_Circle = []
    for deg in list(range(360)) :
        Color_Arc = visual.Pie(win, start = deg, end = deg+ 1, radius = r, colorSpace = 'hsv', fillColor = [deg+ori_angle, 1, 1])
        Color_Circle.append(Color_Arc)
    
    return Color_Circle

# Blank Phase  
def show_Blank(dur) :
    win.flip()
    core.wait(dur)
""" ------------------------------------------------------------------------------------------------------------------------------------ """

""" Setting Parameters """
params = {
    'win_size' : [1200, 800], #size of window
    'nTrials' : 10, #number of Trials
    'stimDur' : 0.5, #stimuli duration
    'stimSize' : 24, #size of stimuli
    'stim_Pos' : [-50, 50, -150, 150], #coordinates of stimuli position
    'bgColor' : [0, 0, 0.5], #color of window background
    'centerPos' : [0, 0], #coordinate of center on window (0,0)
    'setsize' : [3, 5], #number of items in memory array
    'minColorDistance' : 60, #minimun color difference between memory items
    'r' : 400, #radius of colorwheel
    'inner_r' : 250 #radius of small concentric circle
}

""" ------------------------------------------------------------------------------------------------------------------------------------ """

""" Input Exp Info """
Dlg = gui.Dlg(title = "Colorwheel Recall Task")
Dlg.addField("Subject Name")
Dlg.addField("Debug", False)
input_info = Dlg.show()

subject_name = input_info[0] # Name of Subject
debug = input_info[1] # Debug mode
""" ------------------------------------------------------------------------------------------------------------------------------------ """

""" Initializing Experiment """

win = visual.Window(params["win_size"], monitor = "Monitor1", units = "pix", colorSpace = 'hsv', color = params['bgColor'])

trial_ss_conds = ([3] * int(params["nTrials"]/2)) + ([5] * int(params["nTrials"]/2)) 
random.shuffle(trial_ss_conds)

trial_hue_conds = [select_hue(ss) for ss in trial_ss_conds]
trial_pos_conds = [select_pos(params['stim_Pos'], ss) for ss in trial_ss_conds]
trial_target_conds = [select_target(ss) for ss in trial_ss_conds]
trial_ans_conds = [trial_hue_conds[tt][target] for tt, target in enumerate(trial_target_conds)]
trial_oriangle_conds = [random.choice(list(range(360))) for ii in range(params['nTrials'])]
trial_colorwheel_img = [drawing_Colorwheel(win, params['r'], ii) for ii in trial_oriangle_conds]

win.flip()

""" Instruction """ 
mouse = event.Mouse(visible = True, newPos = [0, -150], win = win)
while True :
    Instruction_text = visual.TextStim(win, "It's ColorWheel Recall Task (Zhang & Luck, 2008)\nClick anywhere to Start !"
        , color = [0, 0, 1], colorSpace = 'hsv', pos = [0, 0], height = 20, units = 'pix').draw()
    win.flip()
    
    if mouse.getPressed()[0] == 1 :
        break 
""" ------------------------------------------------------------------------------------------------------------------------------------ """

""" Start Trials """
distance_coll = []
show_Blank(0.5)
for trial, ss in enumerate(trial_ss_conds) :
    win.mouseVisible = False 
    
    ## Stage1. Fixation 
    fixation = visual.Circle(win, fillColor = [-1, -1, -1], colorSpace = 'rgb', radius = params['stimSize']/2, units='pix', pos = params['centerPos']).draw()
    win.flip()
    core.wait(0.5)

    # Blank
    show_Blank(0.5)

    ## Stage2. Memory Array
    color1 = visual.Circle(win, fillColor = [trial_hue_conds[trial][0] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2, units='pix', pos = trial_pos_conds[trial][0]).draw()
    color2 = visual.Circle(win, fillColor = [trial_hue_conds[trial][1] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2, units='pix', pos = trial_pos_conds[trial][1]).draw()
    color3 = visual.Circle(win, fillColor = [trial_hue_conds[trial][2] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2, units='pix', pos = trial_pos_conds[trial][2]).draw()
    if ss == 5 : 
        color4 = visual.Circle(win, fillColor = [trial_hue_conds[trial][3] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2, units='pix', pos = trial_pos_conds[trial][3]).draw()
        color5 = visual.Circle(win, fillColor = [trial_hue_conds[trial][4] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2, units='pix', pos = trial_pos_conds[trial][4]).draw()

    # Blank
    show_Blank(params["stimDur"])
    
    ## Stage3. Colorwheel Recall
    mouse = event.Mouse(visible = True, newPos = [0, 0], win = win)
    waits = 0
    while True :
        [color_arcs.draw() for color_arcs in trial_colorwheel_img[trial]]
        blank_arc = visual.Circle(win, radius = params["inner_r"], units = 'pix', pos = [0, 0], colorSpace = 'hsv', fillColor = [0, 0, 0.5]).draw()
        [visual.Circle(win, fillColor = [0, 0, 1], colorSpace = 'hsv', radius = 3, units = 'pix', pos = pos).draw() for pos in trial_pos_conds[trial]]
        
        trial_target = trial_target_conds[trial]

        mouse = event.Mouse(visible = True, win = win)
        mouse_Pos = mouse.getPos()
        theta = math.atan2(mouse_Pos[1], mouse_Pos[0])
        pos_deg = divmod(math.floor(90 - np.rad2deg(theta)), 360)[1]
        
        ### Show Assistant when Debugging 
        if debug :
            color1 = visual.Circle(win, fillColor = [trial_hue_conds[trial][0] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2+15, units='pix', pos = trial_pos_conds[trial][0]).draw()
            color2 = visual.Circle(win, fillColor = [trial_hue_conds[trial][1] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2+15, units='pix', pos = trial_pos_conds[trial][1]).draw()
            color3 = visual.Circle(win, fillColor = [trial_hue_conds[trial][2] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2+15, units='pix', pos = trial_pos_conds[trial][2]).draw()
            if ss == 5 : 
                color4 = visual.Circle(win, fillColor = [trial_hue_conds[trial][3] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2+15, units='pix', pos = trial_pos_conds[trial][3]).draw()
                color5 = visual.Circle(win, fillColor = [trial_hue_conds[trial][4] + trial_oriangle_conds[trial], 1, 1], colorSpace = 'hsv', radius = params['stimSize']/2+15, units='pix', pos = trial_pos_conds[trial][4]).draw()
        ###
        
        current_hue = pos_deg + trial_oriangle_conds[trial]
        current_hsv = [current_hue, 1, 1]
        ans_hue = trial_ans_conds[trial] + trial_oriangle_conds[trial]
        ans_hsv = [ans_hue, 1, 1]
        
        if waits < 2 :
            current_hsv = [0, 0, 0]
            waits += 1 
        target_color = visual.Circle(win, fillColor = current_hsv, colorSpace = 'hsv', radius = params['stimSize']/2, units='pix', pos = trial_pos_conds[trial][trial_target]).draw()
        win.flip()
        
        if mouse.getPressed()[0] == 1 :
            deg_selected = pos_deg
            deg_ans = trial_ans_conds[trial]
            distance = deg_selected - deg_ans
            if abs(distance) > 180 :
                distance = np.sign(distance)*(math.floor(360 - abs(distance)))
            distance_coll.append(distance)
            win.mouseVisible = False 
            break
        
    # Blank 
    show_Blank(0.5)

    ## Stage4. Feedback
    text_ans = visual.TextStim(win, 'Target', color = [0, 0, 1], colorSpace = 'hsv', pos = [-100, 60], height = 30, units = 'pix').draw()
    color_ans = visual.Circle(win, fillColor = ans_hsv, colorSpace = 'hsv', radius = params['stimSize']/2 +10, units='pix', pos = [-100, 0]).draw()

    text_selected = visual.TextStim(win, 'Selected', color = [0, 0, 1], colorSpace = 'hsv', pos = [100, 60], height = 30, units = 'pix').draw()
    color_selected = visual.Circle(win, fillColor = current_hsv, colorSpace = 'hsv', radius = params['stimSize']/2 +10, units='pix', pos = [100, 0]).draw()
    
    if debug : 
        feedback_str = "Ans : {}, Selected : {}, Distance = {}".format(trial_ans_conds[trial], pos_deg, distance)
        feedbacks = visual.TextStim(win, feedback_str, color = [0, 0, 1], colorSpace = 'hsv', pos = [0, -100], height = 20, units = 'pix').draw()

    win.flip()
    core.wait(3)
    
    ## Stage5. Feedback Inspection
    if debug :
        arc_selected = visual.Pie(win, start = current_hue - trial_oriangle_conds[trial], end = current_hue + 1 - trial_oriangle_conds[trial], radius = params['r'], colorSpace = 'hsv', fillColor = current_hsv).draw()
        arc_ans = visual.Pie(win, start = ans_hue - trial_oriangle_conds[trial], end = ans_hue + 1 - trial_oriangle_conds[trial], radius = params['r'], colorSpace = 'hsv', fillColor = ans_hsv).draw()
    win.flip()
    core.wait(4)
    
    # ITI : 2 ~ 4s 
    if 'escape' in event.getKeys() :
        core.quit()
    ITI = np.random.uniform(low = 2, high = 4, size = 1)[0]
    show_Blank(ITI)
""" ---- Trial Ends ---- """

distance_df = pd.DataFrame({
    'trial' : list(range(1, len(distance_coll)+1)),
    'distance' : distance_coll
})

""" Save Experiment Data """
results_collection = {
    "params" : params,
    "subject_name" : subject_name, 
    "ss_condition" : trial_ss_conds,
    "hue_condition" : trial_hue_conds,
    "pos_condition" : trial_pos_conds,
    "target_condition" : trial_target_conds,
    "ans_condition" : trial_ans_conds, 
    "angle_condition" : trial_oriangle_conds,
    "distance" : distance_df
}
with open("colorwheel_{}.pickle".format(subject_name), "wb") as f :
    pickle.dump(results_collection, f)