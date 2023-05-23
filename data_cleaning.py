import re
import string
import pandas as pd

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

def handling_missing_values(df):
    df = df[df["english"].astype(bool)]
    df.dropna(how="any", inplace=True)
    return df

def handling_duplicate_values(df):
    df.drop_duplicates(inplace=True, keep="first")
    return df

def handling_punctuation(df):
    df = df[~df["english"].map(is_punctuation_only)]
    return df

# Function to keep only Hindi text
def keep_hindi_text(text):
    hindi_text = re.sub(r'[^\u0900-\u097F\s]', '', text)
    return hindi_text

# Function to keep only English text
def keep_english_text(text):
    if isinstance(text, str):
        english_text = re.sub(r'[^A-Za-z\s]', '', text)
        return english_text
    else:
        return ''

def handling_numbers(df):
    df = df[~df["english"].map(is_number)]
    return df

def filter_by_sentence_length(df, column_name, min_length):
    filtered_df = df[df[column_name].str.len() > min_length]
    return filtered_df

def clean_csv(csv_filepath):
    df = pd.read_csv(csv_filepath)
    df = handling_punctuation(df)
    df = handling_numbers(df)
    df = filter_by_sentence_length(df, 'hindi', 25)

    # Remove specific characters
    df = df.replace({'[%()/]': ''}, regex=True)

    # Replace underscores with whitespaces
    df['english'] = df['english'].str.replace('_', ' ')
    df['hindi'] = df['hindi'].str.replace('_', ' ')

    # Remove formatted strings "%s.%s" and "%d" from the dataframe
    df['english'] = df['english'].str.replace('"%s\.%s"|%d', '', regex=True)
    df['hindi'] = df['hindi'].str.replace('"%s\.%s"|%d', '', regex=True)

    df['hindi'] = df['hindi'].apply(lambda x: keep_hindi_text(x))
    df['english'] = df['english'].apply(lambda x: keep_english_text(x))

    # Trimming Whitespaces
    df['english'] = df['english'].str.strip()
    df['hindi'] = df['hindi'].str.strip()

    df = handling_duplicate_values(df)
    df = handling_missing_values(df)



    return df

if __name__ == '__main__':
    df = clean_csv("data/hindi_english_parallel.csv")
    df.to_csv("data/cleaned.csv",index=False)
    print(df.shape)


