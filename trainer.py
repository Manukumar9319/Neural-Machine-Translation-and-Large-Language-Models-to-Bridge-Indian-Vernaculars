import torch
import config
import numpy as np
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer


def df_to_dataset(filepath: str) -> DatasetDict:
    temp_df = pd.read_csv(filepath)
    temp_df = temp_df[[config.df_src,config.df_trg]]
    temp_df.dropna(inplace=True)
    temp_df = temp_df[:100]
    dataset = Dataset.from_pandas(temp_df)
    train_test = dataset.train_test_split(0.2)
    test_valid = train_test["test"].train_test_split(0.5)
    raw_dataset = DatasetDict({
        "train": train_test["train"],
        "test": test_valid["test"],
        "valid": test_valid["train"]
    })
    del temp_df, dataset, train_test, test_valid
    return raw_dataset


def preprocess_function(dataset: DatasetDict) -> DatasetDict:
    inputs = [ex for ex in dataset[config.INPUT_LANG]]
    targets = [ex for ex in dataset[config.TARGET_LANG]]
    model_inputs = tokenizer(inputs, max_length=config.MAX_LEN, truncation=True)

    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=config.MAX_LEN, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

    result = config.metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result


def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]
    return preds, labels


if __name__ == '__main__':
    torch.cuda.empty_cache()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(config.model_checkpoint)
    tokenizer.src_lang = config.src_lang
    tokenizer.tgt_lang = config.trg_lang
    raw_dataset = df_to_dataset(config.DATAPATH)
    tokenized_data = raw_dataset.map(preprocess_function, batched=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(config.model_checkpoint).to(device)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    args = Seq2SeqTrainingArguments(config.save_model,
                                    evaluation_strategy="epoch",
                                    learning_rate=2e-5,
                                    per_device_train_batch_size=config.batch_size,
                                    per_device_eval_batch_size=config.batch_size,
                                    weight_decay=0.01,
                                    save_total_limit=3,
                                    num_train_epochs=50,
                                    predict_with_generate=True
                                    )

    trainer = Seq2SeqTrainer(model,
                             args,
                             train_dataset=tokenized_data["train"],
                             eval_dataset=tokenized_data["valid"],
                             data_collator=data_collator,
                             tokenizer=tokenizer,
                             compute_metrics=compute_metrics
                             )

    trainer.train().to(device)