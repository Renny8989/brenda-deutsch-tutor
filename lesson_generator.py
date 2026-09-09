import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

USER_PROFILE = {
    "level": "B1/B2",
    "native_language": "italiano",
    "interests": "vita quotidiana in Germania, viaggi, lavoro",
}

SYSTEM_PROMPT = """Sei un tutor di tedesco che scrive brevi lezioni quotidiane per un'italiana di livello {level}.
Scrivi in modo naturale e utile per la vita reale in Germania, tenendo conto di questi interessi: {interests}.
Formatta l'output in HTML compatibile con Telegram: usa solo i tag <b> e <i>, più emoji.
Non usare MAI markdown (niente **, niente #, niente elenchi con -). Vai dritto al contenuto, senza premesse."""

PROMPTS = {
    "morning": """Scrivi una lezione mattutina di tedesco (massimo 120 parole). Struttura:
1. Una frase in tedesco utile nella vita reale, in grassetto.
2. La sua traduzione in italiano.
3. 2-3 parole o espressioni nuove con traduzione.
4. Una breve nota grammaticale.
Apri con l'emoji 🇩🇪.""",
    "midday": """Scrivi un breve testo in tedesco (4-6 frasi, massimo 150 parole) su un argomento di vita quotidiana.
Poi la traduzione completa in italiano.
Poi 3-4 parole nuove con traduzione.
Apri con l'emoji 🇩🇪.""",
    "evening": """Scrivi una lezione serale di ripasso (massimo 100 parole): riprendi 2-3 concetti o parole plausibili imparate durante una giornata di studio del tedesco, con un mini-esempio pratico da provare in una conversazione reale.
Apri con l'emoji 🌙.""",
}


def _generate(kind: str) -> str:
    system = SYSTEM_PROMPT.format(
        level=USER_PROFILE["level"],
        interests=USER_PROFILE["interests"],
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": PROMPTS[kind]},
        ],
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()


def morning_lesson() -> str:
    return _generate("morning")


def midday_lesson() -> str:
    return _generate("midday")


def evening_lesson() -> str:
    return _generate("evening")
