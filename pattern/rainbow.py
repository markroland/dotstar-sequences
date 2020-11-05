import colorsys

def rainbow(method):

    # Method 1: Pre-set
    if method == 1:
        return [
            (255,0,0),
            (255,165,0),
            (255,255,0),
            (0,128,0),
            (0,0,255),
            (75,0,130),
            (238,130,238)
        ]

    # Method 2: Calculated (not very good)
    # [(255, 0, 0), (255, 218, 0), (72, 255, 0), (0, 255, 145), (0, 145, 255), (72, 0, 255), (255, 0, 218)]
    rainbow = [(0,0,0)] * 7
    for i in range(7):
        color = colorsys.hsv_to_rgb(i/7, 1, 1);
        rainbow[i] = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
    # print(rainbow)

    return rainbow
