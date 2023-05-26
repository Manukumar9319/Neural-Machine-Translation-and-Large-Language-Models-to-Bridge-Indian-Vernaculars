import torch
from typing import Union
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "salesken/translation-hi-en"
def inference(text: Union[str, list]) -> (list, list):
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_file_only=True, use_auth_token=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenized_text = tokenizer(text, return_tensors="pt", padding=True)
    translation = model.generate(**tokenized_text, return_dict_in_generate=True, output_scores=True)
    translated_text = tokenizer.batch_decode(translation.sequences, skip_special_tokens=True)
    probability_score = torch.exp(translation.sequences_scores).cpu().numpy()
    return translated_text, probability_score


def batched_inference( texts: list, batch_size: int = 6) -> (list, list):
    pred_loader = DataLoader(texts, batch_size=batch_size)
    processed_texts = 0
    translated_text, prob_score = list(), list()
    for batch in pred_loader:
        temp_translate, temp_prob = inference(text=texts)
        for i in range(len(temp_translate)):
            translated_text.append(temp_translate[i])
            prob_score.append(temp_prob[i])
        processed_texts += len(batch)
    print(translated_text)
    return translated_text, prob_score

if __name__ == '__main__':
    texts = ["आप कैसे हैं"]
    batched_inference(texts=texts)