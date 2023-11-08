
# gradio_pdf
Display PDFs in Gradio!

## Example usage

```python
import gradio as gr
from gradio_pdf import PDF
from pdf2image import convert_from_path
from transformers import pipeline
from pathlib import Path

dir_ = Path(__file__).parent

p = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa",
)

def qa(doc: str, question: str) -> str:
    img = convert_from_path(doc)[0]
    output = p(img, question)
    return sorted(output, key=lambda x: x["score"], reverse=True)[0]['answer']


demo = gr.Interface(
    qa,
    [PDF(label="Document"), gr.Textbox()],
    gr.Textbox(),
    examples=[[str(dir_ / "invoice_2.pdf"), "What is the total gross worth?"]]
)

demo.launch()
```

## Demo
![demo](https://gradio-builds.s3.amazonaws.com/assets/PDFDisplay.jpg)