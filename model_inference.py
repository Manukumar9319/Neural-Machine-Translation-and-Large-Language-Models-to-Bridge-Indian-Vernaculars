from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("salesken/translation-hi-en")
model = AutoModelForSeq2SeqLM.from_pretrained("salesken/translation-hi-en")

hin_snippet = "प्रवीण पागल है"
inputs = tokenizer.encode(
    hin_snippet, return_tensors="pt",padding=True,max_length=512,truncation=True)

outputs = model.generate(
    inputs, max_length=128, num_beams=4, early_stopping=True)

translated = tokenizer.decode(outputs[0]).replace('<pad>',"").replace("</s>","").strip().lower()
print(translated)
