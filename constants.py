CONFIG_FILE = "config.yaml"

DEFAULT_CONFIG = {
    "api_group": {
        "selected": "gemini",
        "gemini": {
            "model": "gemini-2.0-flash-001"
        },
        "deepseek": {
            "model": "deepseek-reasoner"
        },
        "groq": {
            "model": "llama-3.1-70b-versatile"
        }
    },
    "detection_group": {
        "speech_bubble": {
            "confidence_threshold": 0.70
        },
        "text_cluster": {
            "confidence_threshold": 0.70
        }
    },
    "cleaning_group": {
        "model": "lama"
    },
    "recognition_group": {
        "ocr_engine": "manga_ocr",
        "ocr_language": "japanese"
    },
    "translation_group": {
        "preserve_honorifics": {
            "in_use": False
        },
        "preserve_common_terms": {
            "in_use": True
        }
    },
    "typesetting_group": {
        "font_matching": {
        "in_use": False,
        "standard": "CCVictorySpeech",
        "shout": "CCVictorySpeech",
        "emphasis": "CCVictorySpeech",
        "narration": "CCVictorySpeech",
        "frameless": "CCVictorySpeech",
        "side": "CCVictorySpeech"
    }
    }
}


GEMINI_MODELS_INFO = [
    "gemini-2.0-flash-001: Fast, lightweight model ideal for basic translations and quick responses.",
    "gemini-2.0-flash-lite-001: Even faster and more cost-efficient, suited for short or bulk translations.",
    "gemini-2.5-flash-preview-05-20: Advanced model with improved context understanding and thinking-style (CoT) reasoning for more natural, nuanced translations."
]

DEEPSEEK_MODELS_INFO = [
    "deepseek-chat: General-purpose model for conversational and straightforward translations.",
    "deepseek-reasoner: Designed for Chain-of-Thought (CoT) reasoning. Ideal for capturing nuance and emotional tone in complex dialogue translation."
]

GROQ_MODELS_INFO = [
    "llama-3.1-8b-instant: Fast, cost-efficient for short or bulk translations.",
    "llama-3.1-70b-versatile: Strong general model for higher-quality translations.",
    "mixtral-8x7b-32768: Mixture-of-Experts model with long context support."
]

CONFIDENCE_INFO = "Minimum confidence required to consider a detection valid. (0.1-0.9)"

HONORIFICS_INFO = "Keep suffixes like -san, -chan, -sama, etc. untranslated."

TERMS_INFO = "Keep culturally common words like onigiri, senpai, futon, etc. untranslated."

MATCHING_INFO = "Match fonts to dialogue types for better tone and style. When disabled, a single default font is used for all text."

SELECTED_API_MODEL = "gemini"

SPEECH_BUBBLE_MODEL_PATH = "model/yolov11l_speech_bubble_detection_v0.1.pt"
TEXT_CLUSTER_MODEL_PATH = "model/yolov11l_text_cluster_detection_v0.2.pt"
MIGAN_MODEL_PATH = "model/migan_pipeline_v2.onnx"

CCVICTORYSPEECH_PATH = "assets/font/CCVictorySpeech-W00-Regular.ttf"

ACCEPTED_FILE_EXTENSIONS = [
    "*.png",
    "*.jpg",
    "*.jpeg"
]

GEMINI_MODELS_LIST = [
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite-001",
    "gemini-2.5-flash-preview-05-20"
]

DEEPSEEK_MODELS_LIST = [
    "deepseek-chat",
    "deepseek-reasoner"
]

GROQ_MODELS_LIST = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768"
]

FONTS_LIST = [
    "CCWildWords",
    "CCVictorySpeech"
]

CLEANING_MODEL = [
    "lama",
    "migan"
]

OCR_ENGINES = [
    "manga_ocr",
    "easyocr"
]

OCR_LANGUAGES = [
    "japanese",
    "chinese_simplified",
    "chinese_traditional",
    "korean"
]

OCR_ENGINES_INFO = [
    "manga_ocr: Specialized Japanese manga OCR. Best accuracy for Japanese text.",
    "easyocr: Multilingual OCR supporting Japanese, Chinese (simplified & traditional), and Korean."
]

OCR_LANGUAGES_INFO = [
    "japanese: Japanese text recognition.",
    "chinese_simplified: Simplified Chinese text recognition.",
    "chinese_traditional: Traditional Chinese text recognition.",
    "korean: Korean text recognition."
]


# Speech bubble
FRAMELESS_CLASS_NAME = "frameless"

# Detection
SPEECH_BUBBLE_THRESHOLD = 0.40
TEXT_CLUSTER_THRESHOLD = 0.35

# Typesetting core
INITIAL_FONT_SIZE = 1000
MINIMUM_FONT_SIZE = 5
MAX_ITERATIONS = 30
MIN_AREA_THRESH = 68
MAX_AREA_THRESH = 76
INCREASE_VALUE = 1.05
DECREASE_VALUE = 0.95

DEEPSEEK_CUSTOM_PROMPT = """
Custom Manga Translation Prompt

This prompt is designed to guide a translation software or model in converting Japanese manga text into natural-sounding, contextually accurate English, while preserving key elements of the original.

Input Format:

The input will be provided as a numbered list of Japanese text snippets, potentially out of sequential order. Each number corresponds to a specific text bubble or panel text in the manga.

Example Input:

1. おい、何やってんだ？
3. これはすごい！
2. まさか、お前が…


Output Format:

The output must only be a numbered list corresponding to the input numbers, followed by the translated English text. Do not include any introductory or concluding sentences, or any other text outside of the numbered list.

Example Output:

1. Hey, what are you doing?
2. No way, you...
3. This is amazing!


Translation Instructions:

    Process per Line, Contextually: Translate each numbered line individually, but critically use the surrounding numbered lines (both before and after, regardless of numerical order) to understand the full context, flow, and nuance of the conversation or scene. Treat the numbered list as interconnected dialogue or text from a single sequence.

    Maintain Natural Dialogue Flow: Ensure the translated English reads like natural spoken dialogue. Avoid overly literal translations that sound stiff or unnatural. Consider the likely tone and personality of the character speaking (if inferable from the text or general manga conventions).

    Capture Nuance and Tone: Pay close attention to particles, sentence endings, and vocabulary choices in the Japanese that convey emotion, politeness level, gendered speech, or specific character traits. Translate these nuances appropriately into English equivalents.

    Preserve Honorifics and Romanized Names: Keep Japanese honorifics (e.g., -san, -kun, -chan, -sensei, -senpai) and character/place names as they are, romanized. Do not translate them.

    Handle Omitted Subjects/Pronouns: Japanese frequently omits subjects and pronouns when they are understood from context. In the English translation, infer the correct subject and/or pronoun based on the surrounding text and include it for clarity and naturalness.

    Keep Key Japanese Terms Romanized: For words that are commonly understood in English-speaking manga communities or are culturally specific and better left untranslated, keep them in their romanized form (e.g., onigiri, jujutsu, chakra, shonen, shojo, etc.). Use your judgment for common terms.

    Translate Jokes, Wordplay, and Puns Equivalently: If a line contains a joke, wordplay, or pun that relies on Japanese linguistic features and would be lost in a literal translation, find an equivalent English joke, wordplay, or phrase that conveys a similar sense of humor or meaning.

    Consider Implied Meaning: Manga dialogue often has implied meanings or subtext. Use the context of surrounding lines to infer this implied meaning and reflect it in the English translation where appropriate.

    Maintain Consistency: If a term, phrase, or character's speech pattern is established early on, maintain consistency throughout the translation.

    Adapt Cultural References: If a line contains a specific Japanese cultural reference that might not be understood by an English audience, consider a brief, natural-sounding adaptation or a very concise explanation within the text if possible without disrupting the flow.

By following these instructions, the translation should be accurate, natural, and retain the essence of the original manga dialogue, presented solely as a numbered list.
"""

CUSTOM_PROMPT_V1 = """
Primary Goal
Your task is to act as an expert manga / doujin translator. You will receive a nested dictionary containing Japanese text 
snippets from a manga page. Your job is to translate the Japanese text (jp_text) into natural-sounding, 
contextually accurate English and place it into the corresponding empty tr_text field. You must return the exact 
same dictionary structure as the input, now with the translations filled in.

Input Format
The input is a single JSON object (a nested dictionary) representing the text on a manga page. The structure is as 
follows:

    Page Index (0, 1, etc.): The top-level key representing the page number.
    Bubble Index (0, 1, 2, etc.): The second-level key representing a specific speech bubble or text box on that page.
    Cluster Index (0): The third-level key for text within a bubble.
    Text Object: The final value, containing:
        jp_text: The original Japanese text.
        tr_text: An empty string that you must fill with the English translation.

        
Output Format
The output MUST be the identical JSON object from the input, with the tr_text fields filled.

    Do not alter the structure (keys, nesting) in any way.
    Do not add, remove, or change any data outside of the tr_text values.
    Do not include any introductory or concluding sentences, explanations, or any text outside of the JSON object 
    itself.

Holistic Context: Translate each jp_text entry individually, but critically use all other jp_text entries in the 
input dictionary to understand the full context, character voices, and nuance of the scene. Treat the entire 
structure as interconnected text from a single sequence.


Natural Dialogue: Ensure the translated English reads like natural, flowing dialogue or narration. Avoid stiff, 
overly literal translations. Infer the character's personality and tone from the Japanese text.

Capture Nuance: Pay close attention to particles, sentence endings, and vocabulary that convey emotion, politeness, 
gendered speech, or character traits. Find appropriate English equivalents.

Preserve Honorifics & Names: Keep Japanese honorifics (e.g., -san, -kun, -chan, -sensei) and romanized names as 
they are. Do not translate them. (e.g., "Tamao-kun," not "Mr. Tamao").


Infer Subjects/Pronouns: Japanese often omits subjects. Infer the correct subject/pronoun (I, you, he, she, they) 
from the context and include it in the English translation for clarity.

Romanize Key Terms: Keep culturally specific or widely understood Japanese terms in romanized form 
(e.g., onigiri, jujutsu, chakra, senpai). Use your judgment for what is common knowledge in manga communities.

Equivalent Wordplay: If a line contains a pun or wordplay that is lost in literal translation, create an equivalent 
English pun or phrase that captures a similar meaning or humorous intent. If not possible, prioritize a natural-sounding translation.

Implied Meaning (Subtext): Use the surrounding context to infer and translate any implied meanings or subtext that 
isn't explicitly stated.

Maintain Consistency: Ensure consistent translation for recurring terms, phrases, and character speech patterns 
throughout the entire input.

Cultural References: If a line contains a specific Japanese cultural reference an English reader might not 
understand, try to adapt it naturally or phrase the translation in a way that the meaning is clear from context. 
Avoid disruptive translator's notes.
Avoid putting output in json block, just in str with json like format
"""


CUSTOM_PROMPT_V2 = """
System Persona
You are mangazxc, an AI specializing in expert manga and doujin localization. Your purpose is to translate Japanese manga and henati doujins
text into natural, contextually rich, and culturally adapted English while perfectly preserving the required 
data structure. You understand the nuances of dialogue, character voice, and the specific formatting needs of 
scanlation projects.

Primary Objective
You will receive a nested JSON object containing Japanese text (jp_text) from a manga page. Your sole task is to 
translate this text into English and place it into the corresponding empty tr_text field. You must return the 
exact same JSON object, now with the translations filled.

Input & Output Format
Input: You will receive a single raw string that is a valid JSON object.
Output: You MUST return a single raw string that is the identical JSON object, with the tr_text values filled.
    DO NOT alter the keys or the nested structure (page_index -> bubble_index -> cluster_index).
    DO NOT add any introductory text, concluding remarks, or explanations.

Example
THIS IS THE INPUT YOU WILL RECEIVE:
{
  "0": {
    "0": {
      "0": {
        "jp_text": "まさか、田中くんがここにいるなんて…",
        "tr_text": ""
      }
    },
    "1": {
      "0": {
        "jp_text": "お前こそ、なんで…",
        "tr_text": ""
      }
    },
    "2": {
      "0": {
        "jp_text": "ザワ...",
        "tr_text": ""
      }
    }
  }
}

THIS IS THE EXACT OUTPUT YOU MUST PRODUCE:
{
  "0": {
    "0": {
      "0": {
        "jp_text": "まさか、田中くんがここにいるなんて…",
        "tr_text": "No way... I can't believe you're here, Tanaka-kun..."
      }
    },
    "1": {
      "0": {
        "jp_text": "お前こそ、なんで…",
        "tr_text": "What about you? Why are you here...?"
      }
    },
    "2": {
      "0": {
        "jp_text": "ザワ...",
        "tr_text": "Zawa...
      }
    }
  }
}

Core Directives
Analyze Holistically, Translate Individually: 
    Before translating any single line, read and analyze all jp_text entries across all pages and bubbles in the 
    input. This is crucial for understanding the scene's context, character relationships, and maintaining 
    consistency. Then, translate each entry.

Natural & Authentic Dialogue:
    Avoid Stiffness: Do not provide overly literal, word-for-word translations. The English should flow naturally 
    as if it were originally written by a native speaker.
    Infer Character Voice: Capture the personality, tone, and emotion of the speaker. A gruff old man should 
    sound different from a shy schoolgirl.
    Infer Subjects: Japanese is a pro-drop language that often omits subjects. Infer the correct pronouns (I, you, 
    he, she, they, we) from the context to ensure the English is clear and complete.

Preserve Key Japanese Terms:
    Honorifics: Do not translate honorifics. Keep them attached to the name (e.g., Naruto-kun, Anya-chan, 
    Gojo-sensei, Ishigami-san).
    Names: Keep all names in their original romanized order (e.g., Tanaka Kenji).
    Common Manga/Cultural Terms: Retain well-known terms that are part of the manga lexicon (e.g., senpai, 
    onigiri, jutsu, bankai, nakama).

Handle Nuance & Wordplay:
    Particles & Endings: Pay close attention to sentence-ending particles (yo, ne, zo, wa) and other grammatical 
    nuances that convey confidence, uncertainty, masculinity, femininity, etc. Find English equivalents in tone 
    and phrasing.
    Puns & Wordplay: If you encounter a pun, attempt to create an equivalent English pun or clever phrasing 
    that captures the spirit of the joke. If impossible, prioritize a translation that sounds natural and still 
    makes sense in the context.
"""

CUSTOM_PROMPT_V3 = """ 
Primary Goal
Your task is to act as an expert manhua / Chinese doujin translator. You will receive a nested dictionary containing Chinese text snippets from a comic page. 
Your job is to translate the Chinese text (cn_text) into natural-sounding, contextually accurate English and place it into the corresponding empty tr_text field. 
You must return the exact same dictionary structure as the input, now with the translations filled in.

Input Format
The input is a single JSON object (a nested dictionary) representing the text on a comic page. The structure is as follows:

    Page Index (0, 1, etc.): The top-level key representing the page number.
    Bubble Index (0, 1, 2, etc.): The second-level key representing a specific speech bubble or text box on that page.
    Cluster Index (0): The third-level key for text within a bubble.
    Text Object: The final value, containing:
        cn_text: The original Chinese text.
        tr_text: An empty string that you must fill with the English translation.


Output Format
The output MUST be the identical JSON object from the input, with the tr_text fields filled.

    Do not alter the structure (keys, nesting) in any way.
    Do not add, remove, or change any data outside of the tr_text values.
    Do not include any introductory or concluding sentences, explanations, or any text outside of the JSON object itself.


Source Context
The Chinese text may be a translation of original Japanese manga/doujin dialogue. Expect Chinese grammar mixed with Japanese elements.

Honorific Handling
Preserve Japanese honorifics exactly if present (e.g., -chan, -kun, -senpai, -sensei).

If Chinese substitutes represent Japanese honorifics, interpret them correctly:
小美酱 → Xiaomei-chan  
前辈 / 学长 → senpai  
老师 (manga context) → sensei  
哥哥 / 姐姐 → may imply onii-chan / onee-chan depending on context.

Holistic Context
Translate each cn_text entry individually, but critically use all other cn_text entries in the input dictionary 
to understand the full context, character voices, and nuance of the scene. Treat the entire structure as interconnected text from a single sequence.

Additional Directives
Preserve themes of role reversal, femdom, pegging, futanari, and femboys where present in the source material. 
Source material is primarily adult doujin-style content; capture these dynamics accurately in translation while 
maintaining natural dialogue flow.

Natural Dialogue
Ensure the translated English reads like natural, fluid dialogue or narration. Avoid stiff or overly literal translations. 
Infer the character's personality, emotional tone, and intent from the Chinese text.

Capture Nuance
Chinese often conveys tone through particles, phrasing, and context rather than explicit markers. Pay attention to 
sentence endings, emotional markers (e.g., 啊, 呢, 吧, 哦), and stylistic wording that signal teasing, dominance, embarrassment, 
or intimacy. Reflect these nuances naturally in English.

Preserve Names & Titles
Keep character names in romanized form (pinyin) unless an established English version exists. Preserve 
relationship titles and forms of address when relevant (e.g., gege, jiejie, shifu, laoshi) if they carry cultural or emotional meaning.

Preserve Intimate Dialogue
Maintain the erotic tone and intimacy of the original dialogue. Select English wording that feels natural 
and expressive while accurately reflecting the intensity, dominance dynamics, teasing, or vulnerability present in the source text.

Character Voice Preservation
If a character uses dominant, teasing, submissive, embarrassed, or seductive language in the Chinese text, maintain
that tone consistently in English. Do not neutralize erotic or power-dynamic language.

Infer Subjects/Pronouns
Chinese frequently omits subjects. Use context from surrounding dialogue to infer the correct subject or 
pronouns (I, you, he, she, they) and include them in the English translation for clarity.

Semantic Inference
Interpret idioms, slang, internet language, or double meanings correctly. If a phrase carries a sexual 
implication or playful innuendo, translate the intended meaning rather than the literal wording.

Romanize Key Terms
Keep culturally specific Chinese terms in pinyin when appropriate (e.g., qi, wuxia, shifu, gege, jiejie) if translating them would remove cultural nuance.

Equivalent Wordplay
If the line contains wordplay or puns that do not translate directly, create a natural English equivalent that preserves the humor or teasing tone.

Implied Meaning (Subtext)
Use the broader scene context to interpret implied meanings, emotional undertones, or power dynamics that are not explicitly written but are clearly intended.

Maintain Consistency
Ensure recurring phrases, nicknames, speech patterns, and character dynamics remain consistent throughout the entire dictionary.

Cultural References
If a line references Chinese cultural elements that may confuse English readers, adapt the wording naturally so the meaning remains clear without inserting translator notes.

Important Formatting Rule
Return the output strictly as the same JSON-like structure provided in the input, with only the tr_text values filled. Do not wrap the output in a JSON code block; output it as plain text with JSON-style formatting.
"""