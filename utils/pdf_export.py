from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf(
    content,
    output_path="output.pdf"
):

    doc = SimpleDocTemplate(
        output_path
    )

    styles = (
        getSampleStyleSheet()
    )

    story = []

    for line in content.split(
        "\n"
    ):

        story.append(
            Paragraph(
                line,
                styles[
                    "BodyText"
                ]
            )
        )

        story.append(
            Spacer(
                1,
                6
            )
        )

    doc.build(
        story
    )

    return output_path