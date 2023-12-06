from __future__ import annotations


from io import StringIO


class DocumentationTemplate:
    def __init__(self):
        self._buffer = StringIO()

    def gen_documentation(self, documentation):
        for func in documentation:
            cls_name, fnc_name, (summary, desc, params) = func

            self._buffer.write(f"## {cls_name}.{fnc_name}\n")

            self._buffer.write("> "+(summary or "No provided summary")+"\n\n")
            self._buffer.write((desc or "No provided description")+"\n")

            for param in params:
                p_name, p_type, p_summary, p_long = param
                self._buffer.write(f" - {p_name} `{p_type}`\n\n")
                self._buffer.write(f"   {p_summary}\n\n")
                self._buffer.write(f"   {p_long}\n\n\n")

            self._buffer.write("\n")

        return self._buffer.getvalue()
