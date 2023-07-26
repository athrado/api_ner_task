# Response for sample_text.txt when testing
correct_response_people = [
    {
        "name": "Sarah",
        "count": 5,
        "assosciated_places": [
            {"name": "Kyoto", "count": 2},
            {"name": "Barcelona", "count": 1},
            {"name": "Japan", "count": 1},
            {"name": "the United States", "count": 1},
        ],
    },
    {
        "name": "Carlos",
        "count": 4,
        "assosciated_places": [
            {"name": "Barcelona", "count": 1},
            {"name": "Brazil", "count": 1},
            {"name": "Louisiana", "count": 1},
            {"name": "New Orleans", "count": 1},
            {"name": "USA", "count": 1},
        ],
    },
    {
        "name": "Ahmed",
        "count": 2,
        "assosciated_places": [
            {"name": "Barcelona", "count": 1},
            {"name": "Egypt", "count": 1},
            {"name": "Kenya", "count": 1},
        ],
    },
    {
        "name": "Michaela",
        "count": 2,
        "assosciated_places": [
            {"name": "Spain", "count": 2},
            {"name": "Barcelona", "count": 1},
            {"name": "Dubai", "count": 1},
            {"name": "United Arab Emirates", "count": 1},
        ],
    },
    {
        "name": "Li Wei",
        "count": 2,
        "assosciated_places": [
            {"name": "Rome", "count": 2},
            {"name": "Barcelona", "count": 1},
            {"name": "China", "count": 1},
            {"name": "Italy", "count": 1},
        ],
    },
]

# Word span for search range to both sides of name
span = 100
