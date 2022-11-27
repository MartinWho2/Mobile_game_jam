dictionnaire = {
    'spawn': [(50, 120), (100, 150), (50, 270), (100, 50), (100, 50), (60,100),(80, 350), (100, 160)
              ],
    'door': [
        [],
        [],
        [],
        [[(10, 1), 0, False, False], [(16, 4), 1, True, True], [(10, 8), 2, False, False], [(5, 11), 3, True, True]],
        [[(4, 5), 0, False, False]],
        [[(10, 11), 0, False, False], [(16, 11), 1, False, False]],
        [[(9, 9), 0, False, False], [(11, 7), 1, True, True]],
        [[(14,1), 0, False, False], [(18, 3), 2, True, False]]

    ],
    'vent': [
        [],
        [],
        [[(6, 9), (21, 7), 0]],
        [[(5, 3), (1, 5), 0], [(8, 6), (1, 14), 2],[(1, 10), (14, 14), 3]],
        [[(23, 2), (2, 7), 0], [(6, 7), (20, 13), 1]],
        [[(3, 3), (1, 13), 0], [(14, 13), (3, 7), 1], [(15, 8), (18, 13), 2]],
        [[(5, 11), (7, 5), 0]],
        []
    ],
    "button": [
        [],
        [],
        [[(22, 7), [0]]],
        [[(10, 5), [0, 1]], [(12, 14), [2, 3]]],
        [[(23, 6), [0]], [(22, 13), [1]]],
        [[(3, 13), [0]], [(1, 7), [1]]],
        [[(5, 5), [0, 1]], [(1, 5), [2,3,4]]],
        [[(10, 5), [4, 5]], [(12, 5), [0,2]]]

    ],
    'laser': [
        [],
        [],
        [[(22, 9), 0, 'left', False]],
        [],
        [[(6, 13), 1, 'right', False]],
        [[(14, 8), 2, 'left', False]],
        [[(18, 1), 2, 'down', False],[(19,1),3,'down',False],[(20,1),4,'down',False]],
        [[(17, 1), 3, 'down', False], [(21, 11), 4, 'left', False], [(8, 7), 5, 'down', True]]
    ],
    'portal': [
        [[2, 11, 'end'], [1, 2, 'start']],
        [[6, 11, 'end'], [1, 3, 'start']],
        [[9, 11, 'end'], [1, 6, 'start']],
        [[20, 12, 'end'], [2, 1, 'start']],
        [[2, 11, 'end'], [2, 1, 'start']],
        [[18, 3, 'end'], [1, 1, 'start']],
        [[21, 3, 'end'], [2, 9, 'start']],
        [[1, 9, 'end'], [1, 3, 'start']]
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
