import re



def extract_markdown_codeblock(text: str) -> str:
    codeblock_pattern = r"^```(?:json)?\s*(.*?)\s*```$"
    match = re.match(codeblock_pattern, text.strip(), re.DOTALL)

    return match.group(1).strip() if match else text.strip()