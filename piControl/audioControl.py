import synthIter

# Translate 'value' from 'left' range to 'right' range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # If value outside of range, apply ceiling
    if (value > leftMax): 
    	value = leftMax

    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def translate_inverse(value, leftMin, leftMax, rightMin, rightMax):
    return rightMax - translate(value, leftMin, leftMax, rightMin, rightMax)


class AudioControl:
    # Fields:
    # volControlIter -> synthIter in charge of animating changes in volume