from wasaki.styles import Fonts


class Sembed:
    """
    Since Whats App does not support embeds we can use this to kinda simulate it.
    And that's where the name is derived from, Sembed (Simulated Embed).
    example:
    ...
    sembed = Sembed(title="the title")
    sembed.set_footer(text="the footer")
    sembed.add_field(name="field_name", "field_value")
    return ctx.reply(sembed)
    """

    def __init__(
        self, **kwargs
    ) -> None:  # title: str, url: str, fields: list[tuple], footer: str
        self.title = kwargs.get("title", "")
        self.url = kwargs.get("url", "")
        self.fields = kwargs.get("fields", [])
        self.footer = kwargs.get("footer", "")

    def add_field(self, name: str, value: str) -> "self":
        self.fields.append((name, value))
        return self

    def set_footer(self, text: str, stylize: bool = True) -> "self":
        self.footer = Fonts.small(text) if stylize else text
        return self

    def _create(
        self,
    ) -> str:  # If you have a good and more efficient alt for how this func works then you can do that.
        head = (
            "*"
            + (f"{self.title}" + ("\n" if self.title else "") + f"{self.url}").strip()
            + "*"
        )
        name_values = "\n".join(f"\n*{name}*\n{value}" for name, value in self.fields)
        footer = self.footer
        return (
            head
            + ("\n" if head else "")
            + name_values
            + ("\n" if name_values else "")
            + footer
        )

    def __str__(self) -> str:
        return self._create()
