import re
import string
import pandas as pd
import numpy as np
from alphabet_detector import AlphabetDetector

ad = AlphabetDetector()

def is_arabic_only(text):
    if ad.is_arabic(text):
        return True
    return False

def is_english_only(text):
    text = str(text)
    text = re.search(r"[a-zA-Z0-9]", text)
    return bool(text)


def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def remove_punctuations_regex(text):
    text = re.sub(r'[^\w\s]', "", text)
    return text

def is_number(text):
    text = str(text)
    text = re.search(r"[0-9]", text)
    return bool(text)

def is_punctuation_only(text):
    text = str(text).replace(" ", "")
    return all(i in string.punctuation for i in text)

def handling_tr_pr_qa(df):
    _priority = {"QR": 3, "PR": 2, "TR": 1}
    df.sort_values(by="translator", key=lambda x: x.map(_priority), ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df[["src", "trg"]]
    return df



def handling_missing_values(df):
    df = df[df["src"].astype(bool)]
    df = df[df["trg"].astype(bool)]
    df.dropna(how="any", inplace=True)
    return df

def handling_duplicate_values(df):
    df.drop_duplicates(inplace=True, keep="first")
    return df

def handling_punctuation(df):
    df = df[~df["src"].map(is_punctuation_only)]
    df = df[~df["trg"].map(is_punctuation_only)]
    return df

def handling_numbers(df):
    df = df[~df["src"].map(is_number)]
    df = df[~df["trg"].map(is_number)]
    return df

def correcting_language_pair(df):
    ara_ara_mask = df["src"].map(is_arabic_only) & df["trg"].map(is_arabic_only)
    df = df[~ara_ara_mask]
    eng_eng_mask = df["src"].map(is_english_only) & df["trg"].map(is_english_only)
    df = df[~eng_eng_mask]
    eng_mask = df["trg"].map(is_english_only)
    ara_mask = df["src"].map(is_arabic_only)
    # print(f"Total Number of English Rows in target Column: {eng_mask.value_counts()[True]}")
    # print(f"Total Number of Arabic Rows in target Column: {ara_mask.value_counts()[True]}")
    temp_df = df[eng_mask]
    df = df[~eng_mask]
    df.rename({"src": "eng", "trg": "ara"}, axis=1, inplace=True)
    temp_df.rename({"src": "ara", "trg": "eng"}, axis=1, inplace=True)
    df = pd.concat([df, temp_df], ignore_index=True)
    return df

def handling_single_char(df):
    df = df[~df["eng"].map(lambda x: len(x) == 1)]
    df = df[~df["ara"].map(lambda x: len(x) == 1)]
    return df



def clean_tm(csv_filepath):
    df = pd.read_csv(csv_filepath)
    df.rename({'english':'src',"arabic":"trg"},axis=1, inplace=True)
    df = df[['src','trg']]
    # df = handling_tr_pr_qa(df)
    df = handling_missing_values(df)
    df = handling_duplicate_values(df)
    df = handling_punctuation(df)
    df = handling_numbers(df)
    df = correcting_language_pair(df)

    return df

if __name__ == '__main__':
    df = clean_tm("total_tm.csv")
    df.to_csv("data/latest_data.csv",index=False)
    print(df.shape)


