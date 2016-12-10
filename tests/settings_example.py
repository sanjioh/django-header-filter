# -*- coding: utf-8 -*-
HEADER_FILTER_GROUPS = {
    'group_A': (
        ('X-H-1', 'value'),
        ('X-H-2', callable),
    ),

    'group_B': (
        ('X-H-3', 'value'),
        ('X-H-4', callable),
    ),

    'group_C': (
        ('X-H-5', 'value'),
        ('X-H-6', callable),
    ),

    'group_D': (
        ('X-H-5', 'value'),
        ('X-H-6', callable),
    )
}
HEADER_FILTER_RULES = (
    {
        # request passes if all headers are present
        'ACTION': 'enforce',
        'HEADERS': 'group_A',
        'RESPONSE': (400, 'enforce rule matched'),
    },
    {
        # request passes if all headers are absent
        'ACTION': 'forbid',
        'HEADERS': 'group_B',
        'RESPONSE': (400, 'forbid rule matched'),
    },
    {
        # request passes if:
        # - both group C and group D are present
        # - both group C and group D are absent
        'ACTION': 'include',
        'HEADERS': ('group_C', 'group_D'),
        'RESPONSE': (400, 'include rule matched'),
    },
    {
        # request passes if:
        # - only group C is present
        # - only group D is present
        # - both group C and group D are absent
        'ACTION': 'exclude',
        'HEADERS': ('group_C', 'group_D'),
        'RESPONSE': (400, 'exclude rule matched'),
    }
)
