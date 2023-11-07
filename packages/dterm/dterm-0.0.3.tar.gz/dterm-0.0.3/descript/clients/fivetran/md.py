from . import Connector


def markdown_header():
    return "| table | status  | docs |\n" +\
           "| ---   | ---     | ---  |"


def markdown_row(c: Connector):
    docs = c.docs
    cols = (
        # c.group.name if c.group else '',
        # c.schema,
        f"`{c.table}`",
        c.status + " " +\
        f"last success: {c.succeeded_at} " +\
        f"last failure: {c.failed_at}",
        # c.history
    )

    if docs is not None:
        erd = ""
        if docs.link_to_erd is not None:
            erd = f"[diagram]({docs.link_to_erd})"
        cols = cols + (
            f"[docs]({docs.link_to_docs})" + " " + erd,
        )
        print(docs.icon_url)

    return "| " + " | ".join(map(str, cols)) + " |"
