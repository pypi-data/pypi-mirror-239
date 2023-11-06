import itertools

lc = [
    (
        {
            "id": 5474,
            "range": [0, 3],
            "phrase": "*an A for effort",
            "phrase_html": "<p><strong>*</strong>an <strong>A for effort</strong></p>",
            "definition": "acknowledgement for having tried to do something, even if it was not successful. (*Typically: get ~; give someone ~.) _ The plan didn’t work, but I’ll give you an A for effort for trying.",
            "definition_html": "<p><em></em>acknowledgement for having tried to do something, even if it was not successful. (*Typically: <strong>get ~; give </strong>someone <strong>~</strong>.) <br>_ <em>The plan didn’t work, but</em> <em>I’ll give you an A for effort for trying.</em></p>",
            "alt": ["verb", "verb", "article", "constant"],
            "runs": ["get", "give", "an", "a for effort"],
            "patterns": [
                "a for effort",
                "an a for effort",
                "get a for effort",
                "give a for effort",
                "get an a for effort",
                "give an a for effort",
            ],
            "word_forms": [
                [["get", "got", "gettings", "gets", "getting", "gotten"]],
                [
                    [
                        "given",
                        "giving",
                        "givers",
                        "givings",
                        "gave",
                        "gives",
                        "giver",
                        "give",
                    ]
                ],
                [["an"]],
                [["a", "as"], ["for"], ["effort", "efforts"]],
            ],
            "multiple": False,
            "duplicate": False,
        },
        5,
        (31, 55),
    ),
    (
        {
            "id": 2013,
            "range": [29213, 29216],
            "phrase": "give something a try",
            "phrase_html": "<p><strong>give </strong>something <strong>a try</strong></p>",
            "definition": "to make a try at something. _ Why don’t you give it a go and see if you like it?",
            "definition_html": "<p>to make a try at something. <br>_ <em>Why don’t you give it a go and see if you like</em> <em>it?</em></p>",
            "alt": ["constant", "variable", "constant"],
            "runs": ["give", "something", "a try"],
            "patterns": ["give a try"],
            "word_forms": [
                [
                    [
                        "given",
                        "giving",
                        "givers",
                        "givings",
                        "gave",
                        "gives",
                        "giver",
                        "give",
                    ]
                ],
                "NA",
                [
                    ["a", "as"],
                    [
                        "trial",
                        "trying",
                        "tried",
                        "trials",
                        "triers",
                        "trier",
                        "try",
                        "tries",
                    ],
                ],
            ],
            "multiple": True,
            "duplicate": False,
        },
        3,
        (31, 66),
    ),
    (
        {
            "id": 10849,
            "range": [29234, 29236],
            "phrase": "give something for something",
            "phrase_html": "<p><strong>give </strong>something <strong>for </strong>something</p>",
            "definition": "to exchange something for something. _I will give two brownies for that piece of cake in your lunch box. _ Jed gave two pigs for an old motorcycle.",
            "definition_html": "<p>to exchange something for something. <br>_<em>I will give two brownies for that piece of cake</em> <em>in your lunch box. </em><br>_ <em>Jed gave two pigs for an old motorcycle.</em></p>",
            "alt": ["constant", "variable", "constant", "variable"],
            "runs": ["give", "something", "for", "something"],
            "patterns": ["give for"],
            "word_forms": [
                [
                    [
                        "given",
                        "giving",
                        "givers",
                        "givings",
                        "gave",
                        "gives",
                        "giver",
                        "give",
                    ]
                ],
                "NA",
                [["for"]],
                "NA",
            ],
            "multiple": False,
            "duplicate": False,
        },
        2,
        (31, 48),
    ),
    (
        {
            "id": 10849,
            "range": [29234, 29236],
            "phrase": "give something for something",
            "phrase_html": "<p><strong>give </strong>something <strong>for </strong>something</p>",
            "definition": "to exchange something for something. _I will give two brownies for that piece of cake in your lunch box. _ Jed gave two pigs for an old motorcycle.",
            "definition_html": "<p>to exchange something for something. <br>_<em>I will give two brownies for that piece of cake</em> <em>in your lunch box. </em><br>_ <em>Jed gave two pigs for an old motorcycle.</em></p>",
            "alt": ["constant", "variable", "constant", "variable"],
            "runs": ["give", "something", "for", "something"],
            "patterns": ["give for"],
            "word_forms": [
                [
                    [
                        "given",
                        "giving",
                        "givers",
                        "givings",
                        "gave",
                        "gives",
                        "giver",
                        "give",
                    ]
                ],
                "NA",
                [["for"]],
                "NA",
            ],
            "multiple": False,
            "duplicate": False,
        },
        2,
        (31, 48),
    ),
]

x = list(itertools.groupby([(item[0], item[2]) for item in lc[:10]]))

print(len(lc))
from pprint import pprint

pprint(x)
print(len(x))
