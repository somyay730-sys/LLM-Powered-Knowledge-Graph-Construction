from ollama import chat

from schemas import KnowledgeGraph


ALLOWED_ENTITY_TYPES = [
    "PERSON",
    "COMPANY",
    "LOCATION",
    "PRODUCT",
    "DATE"
]


ALLOWED_RELATIONS = [
    "CEO_OF",
    "ACQUIRED",
    "HEADQUARTERED_IN",
    "DEVELOPED",
    "FOUNDED_BY",
    "WORKS_AT",
    "LOCATED_IN",
    "CREATED"
]


def extract_knowledge(text):

    prompt = f"""
You are a precise knowledge graph information extraction system.

Your task is to extract entities and relationships from unstructured text.

ALLOWED ENTITY TYPES:

PERSON
COMPANY
LOCATION
PRODUCT
DATE

ALLOWED RELATIONSHIP TYPES:

CEO_OF
ACQUIRED
HEADQUARTERED_IN
DEVELOPED
FOUNDED_BY
WORKS_AT
LOCATED_IN
CREATED


ENTITY EXTRACTION RULES:

1. Extract every explicitly mentioned named entity.

2. Extract years and explicit dates as DATE entities.

Example:

"Microsoft acquired GitHub in 2018."

Entities:

Microsoft -> COMPANY
GitHub -> COMPANY
2018 -> DATE

3. Do not add words that are not present in the text.

Incorrect:

GitHub -> GitHub Inc

Correct:

GitHub -> GitHub

4. Preserve the entity name exactly as written in the sentence.

5. Do not invent company suffixes such as:

Inc
Corp
Corporation
Ltd

unless they explicitly appear in the text.


RELATIONSHIP EXTRACTION RULES:

1. Extract every relationship explicitly stated in the text.

2. Use ONLY relationship types from the allowed relationship list.

3. Do not create new relationship labels.

4. Relationship source and target must exist in the entities list.

5. Interpret these patterns carefully:
6. Never extract information from your own background knowledge.

7. Every entity name must appear explicitly in the provided TEXT.

8. Do not infer dates, founding years, release years, acquisition years,
or any other facts unless they are explicitly written in the TEXT.

Incorrect:

TEXT:
Tim Cook is the CEO of Apple.

Extract:
2011 -> DATE

Reason:
2011 does not appear in the TEXT.

Incorrect:

TEXT:
Elon Musk is the CEO of Tesla.

Extract:
2010 -> DATE

Reason:
2010 does not appear in the TEXT.

Before returning the result, verify that every extracted entity name
appears in the input text.

"X is the CEO of Y"

X --CEO_OF--> Y


"X acquired Y"

X --ACQUIRED--> Y


"X is headquartered in Y"

X --HEADQUARTERED_IN--> Y


"X developed Y"

X --DEVELOPED--> Y

"X founded Y"

Y --FOUNDED_BY--> X


IMPORTANT RELATIONSHIP DIRECTION RULE:

FOUNDED_BY always points from the organization or company
to the founder.

Correct:

Meta --FOUNDED_BY--> Mark Zuckerberg

Incorrect:

Mark Zuckerberg --FOUNDED_BY--> Meta

EXAMPLE:

TEXT:

Satya Nadella is the CEO of Microsoft.
Microsoft acquired GitHub in 2018.
GitHub is headquartered in San Francisco.

EXPECTED EXTRACTION:

{{
    "entities": [
        {{
            "name": "Satya Nadella",
            "type": "PERSON"
        }},
        {{
            "name": "Microsoft",
            "type": "COMPANY"
        }},
        {{
            "name": "GitHub",
            "type": "COMPANY"
        }},
        {{
            "name": "2018",
            "type": "DATE"
        }},
        {{
            "name": "San Francisco",
            "type": "LOCATION"
        }}
    ],
    "relationships": [
        {{
            "source": "Satya Nadella",
            "relation": "CEO_OF",
            "target": "Microsoft"
        }},
        {{
            "source": "Microsoft",
            "relation": "ACQUIRED",
            "target": "GitHub"
        }},
        {{
            "source": "GitHub",
            "relation": "HEADQUARTERED_IN",
            "target": "San Francisco"
        }}
    ]
}}


Now extract knowledge from the following text.

TEXT:

{text}
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=KnowledgeGraph.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    knowledge = (
        KnowledgeGraph.model_validate_json(
            response.message.content
        )
    )

    return knowledge.model_dump()