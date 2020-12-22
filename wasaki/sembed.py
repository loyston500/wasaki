from wasaki.wasaki.styles import Fonts

class Sembed:
    '''
    Since Whats App does not support embeds we can use this to kinda simulate it. 
    And that's where the name is derived from, Sembed (Simulated Embed).
    '''
    def __init__(self, **kwargs) -> None: # title: str, url: str, fields: list[tuple], footer: str
        self.title = kwargs.get("title", '')
        self.url = kwargs.get("url", '')
        self.fields = kwargs.get("fields", [])
        self.footer = kwargs.get("footer", '')
    
    def add_field(self, name: str, value: str) -> None:
        self.fields.append((name, value))

    def set_footer(self, text: str, stylize:bool=True) -> None:
        self.footer = (Fonts.small(text) if stylize else text)

    def _create(self) -> str: # If you have a good and more efficient alt for how this func works then you can do that.
        head = f"{self.title}" + ("\n" if self.title else "") + f"{self.url}" 
        name_values = "\n".join(f"_*{name}*_\n{value}" for name, value in self.fields)
        footer = self.footer
        return head + ("\n" if head else "") + name_values + ("\n" if name_values else "") + footer

    def __str__(self) -> str:
        return self._create()
