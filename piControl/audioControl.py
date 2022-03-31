import synthIter as sIter

# This audio control is programmed to react to movement by quieting down the volume
# source. 

# Translate 'value' from 'left' range to 'right' range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # If value outside of range, apply ceiling
    if (value > leftMax): value = leftMax
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def translateInverse(value, leftMin, leftMax, rightMin, rightMax):
    return rightMax - translate(value, leftMin, leftMax, rightMin, rightMax)

class AudioControl:
    # Fields:
    # cur_volume            -> current volume
    # vol_control_iter      -> synthIter in charge of animating changes in volume
    # cur_dist
    # prev_dist
    # delta_dist

    # animation_state       -> state 0: init, no animation happening
    #                       -> state 1: (during) part 1 of quieting animation
    #                       -> state 2: (after) part 1 of quieting animation
    #                       -> state 3: (during) part 2 of quieting animation
    #                       -> state 4: (after) part 2 of quieting animation

    # change_state_counter  -> used to control changes in animation state

    # Constants:
    delta_thresh_movement = 5           # movement = any time delta_dist > thresh
    delta_thresh_stationary = 2         # stationary = any time delta_dist < thresh
    change_state_count_thresh = 5       # number of frames requires before state change triggered
    quiet_animation_1 = (1.0, 0.5, 0.4, 0.3, 0.2, 0.1)
    quiet_animation_2 = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    # values to flag end of animation, trigger 
    end_quiet_animation_1 = quiet_animation_1[len(quiet_animation_1)-1]     # last value of animation part 1
    end_quiet_animation_2 = quiet_animation_2[len(quiet_animation_2)-1]     # last value of animation part 2

    def __init__(self, cur_volume = 1.0, cur_dist = 0, prev_dist = 0, delta_dist = 0):
        self.cur_volume = cur_volume
        self.vol_control_iter = sIter.SynthIter(cur_volume)
        
        self.cur_dist = cur_dist
        self.prev_dist = prev_dist
        self.delta_dist = delta_dist
        self.animation_state = 0
        self.change_state_counter = 0

    # given the current movement state, return the current volume
    def getAudioUpdate(self):
        vol_iter = iter(self.vol_control_iter)
        self.cur_volume = next(vol_iter)
        return self.cur_volume

    def updateDistState(self, cur_dist):
        self.prev_dist = cur_dist
        self.cur_dist = cur_dist 
        self.delta_dist = abs(self.cur_dist - self.prev_dist)
        match self.animation_state:
            case 0:
                # in init state, change if constant movement occurs
                if (self.delta_dist > self.delta_thresh_stationary):
                    if (self.change_state_counter > self.change_state_count_thresh):
                        self.animation_state = 1
                        self.change_state_counter = 0
                        self.vol_control_iter.append(self.quiet_animation_1)
                    else:
                        self.change_state_counter += 1
                else:
                    self.change_state_counter = 0
            case 1:
                # in first part of animation. play animation then go to state 2
                if (self.change_state_counter >= len(self.quiet_animation_1)):
                    self.change_state_counter = 0
                    self.animation_state = 2
                else:
                    self.change_state_counter += 1
            case 2:
                # first part is done. only change if movement stops
                if (self.delta_dist < self.delta_thresh_stationary):
                    if (self.change_state_counter > self.change_state_count_thresh):
                        self.animation_state = 3
                        self.change_state_counter = 0
                        self.vol_control_iter.append(self.quiet_animation_2)
                    else:
                        self.change_state_counter += 1
                else:
                    self.change_state_counter = 0
            case 3:
                # in second part of animation. play animation then go to state 0 (reset)
                if (self.change_state_counter >= len(self.quiet_animation_2)):
                    self.change_state_counter = 0
                    self.animation_state = 0
                else:
                    self.change_state_counter += 1
            # case 4:
            #     # second part is done 
