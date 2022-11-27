dictionnaire = {
    'spawn': [(50, 120), (100, 150), (50, 270), (100, 50), (100, 50), (60,100), (100, 160), (290, 450)
              ],
    'door': [
        [],
        [],
        [],
        [[(10, 1), 0, False, False], [(16, 4), 1, True, True], [(10, 8), 2, False, False], [(5, 11), 3, True, True]],
        [[(4, 5), 0, False, False]],
        [[(10, 11), 0, False, False], [(16, 11), 1, False, False]],
        [[(14,1), 0, False, False], [(19, 7), 2, True, True]],
        [[(22, 11), 0, False, False], [(25, 9), 1, True, True], [(13, 6), 2, False, False]]
    ],
    'vent': [
        [],
        [],
        [[(6, 9), (21, 7), 0]],
        [[(5, 3), (1, 5), 0], [(8, 6), (1, 14), 2],[(1, 10), (14, 14), 3]],
        [[(23, 2), (2, 7), 0], [(6, 7), (20, 13), 1]],
        [[(3, 3), (1, 13), 0], [(14, 13), (3, 7), 1], [(15, 8), (18, 13), 2]],
        [],
        [[(1, 8), (1, 13), 0], [(16, 13), (9, 8), 1], [(16, 8), (18, 8), 2]]
        # ,[(15, 5), (11, 11), 1]
    ],
    "button": [
        [],
        [],
        [[(22, 7), [0]]],
        [[(10, 5), [0, 1]], [(12, 14), [2, 3]]],
        [[(23, 6), [0]], [(22, 13), [1]]],
        [[(3, 13), [0]], [(1, 7), [1]]],
        [[(10, 5), [4, 5]], [(12, 5), [0,2]]],
        [[(5, 8), [0, 1, 2]], [(5, 13), [2,3]]]
    ],
    'laser': [
        [],
        [],
        [[(22, 9), 0, 'left', False]],
        [],
        [[(6, 13), 1, 'right', False]],
        [[(14, 8), 2, 'left', False]],
        [[(17, 1), 3, 'down', False], [(18, 11), 4, 'right', False], [(8, 7), 5, 'down', True]],
        [[(18, 4), 3, 'right', False]]
    ],
    'portal': [
        [[2, 11, 'end'], [1, 2, 'start']],
        [[6, 11, 'end'], [1, 3, 'start']],
        [[9, 11, 'end'], [1, 6, 'start']],
        [[20, 12, 'end'], [2, 1, 'start']],
        [[2, 11, 'end'], [2, 1, 'start']],
        [[18, 3, 'end'], [1, 1, 'start']],
        [[1, 9, 'end'], [1, 3, 'start']],
        [[1, 1, 'end'], [7, 11, 'start']]
    ],
    'texts': [
        [[(15, 2), 'Use the left and right arrows to move'], [(15, 10), 'Use the up arrow to jump']],
        [[(20, 3), 'Pull the right action button'], [(20, 5), 'to throw your arms'], [(21, 12.5), 'Use the left action button to detach/reattach your head']],
        [[(10, 3), 'Use the vents to move to another location'], [(19, 8), 'Use the button to deactivate the laser']],
        [],
        [],
        [],
        [],
        []
    ]
}
