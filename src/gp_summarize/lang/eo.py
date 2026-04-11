name = "Esperanto"

system_instruction = """
You are an expert at analyzing and summarizing academic papers.
Please use $TeX$ to write mathematical equations.
Please only return the results, and do not include any comments.
Use a formal academic writing style in Esperanto.
""".strip()

prompts = [
    ("# Titolo", "Traduku nur la titolon de la artikolo al Esperanto."),
    ("# Abstrakto", "Traduku la Abstrakton komence de la dokumento al Esperanto."),
    ("# Superrigardo", "Resumigu la dokumenton per unu frazo en Esperanto."),
    ("## Problemdifino", "Kian problemon provas solvi la dokumento? Respondu en Esperanto."),
    ("## Metodaro", "Kian metodaron proponas la dokumento? Respondu en Esperanto."),
    ("## Noveco", "Kio estas la noveco de la dokumento? Respondu en Esperanto."),
    ("# Ĉapitrostrukturo", """Eligu la ĉapitrostrukturon kiel JSON-aron sen traduko. Ekzemplo:
```json
[
  "1 Introduction",
  "1.1 Background",
  "2 Methods",
  "2.1 Data",
  "2.1.1 Dataset"
]
```"""),
]

sprompt = ("Resumigu la sekcion '%s' en Esperanto.", "', '")
