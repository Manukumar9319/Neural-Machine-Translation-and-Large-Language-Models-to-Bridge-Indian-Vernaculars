from datasets import load_metric

INPUT_LANG = "hindi"
TARGET_LANG = "english"
MAX_LEN = 128
metric = load_metric("sacrebleu")
model_checkpoint = "salesken/translation-hi-en"
DATAPATH = "hindi_english_parallel.csv"

save_model = 'checks'

batch_size = 16