from datasets import load_metric

metric = load_metric("sacrebleu")

# Key Parameter
from_and_to_nmt = "hindi-to-gujrati"


batch_size = 16
MAX_LEN = 40

# LLM checkpoints settings
if from_and_to_nmt == "hindi-to-english":
    model_checkpoint = "salesken/translation-hi-en"
    DATAPATH = "data/hi-en.csv"

else:
    model_checkpoint = "facebook/mbart-large-50-many-to-many-mmt"
    DATAPATH = "data/Neural-Machine-Translation-Training-Data.csv"



if from_and_to_nmt == "hindi-to-english":
    INPUT_LANG = "hindi"
    TARGET_LANG = "english"
    src_lang = 'hi'
    trg_lang = 'en'
    df_src = 'hindi'
    df_trg = 'english'
    save_model = 'translation-hi-en'

elif from_and_to_nmt == 'hindi-to-gujrati':
    INPUT_LANG = "hindi"
    TARGET_LANG = "gujrati"
    src_lang = 'hi_IN'
    trg_lang = 'gu_IN'
    df_src = 'hindi'
    df_trg = 'gujrati'
    save_model = 'translation-hi-gu'

elif from_and_to_nmt == 'hindi-to-telugu':
    INPUT_LANG = "hindi"
    TARGET_LANG = "telugu"
    src_lang = 'hi_IN'
    trg_lang = 'te_IN'
    df_src = 'hindi'
    df_trg = 'telugu'
    save_model = 'translation-hi-te'

elif from_and_to_nmt == 'hindi-to-bengali':
    INPUT_LANG = "hindi"
    TARGET_LANG = "bengali"
    src_lang = 'hi_IN'
    trg_lang = 'bn_IN'
    df_src = 'hindi'
    df_trg = 'bengali'
    save_model = 'translation-hi-bn'

elif from_and_to_nmt == "gujrati-to-telugu":
    INPUT_LANG = "gujrati"
    TARGET_LANG = "telugu"
    src_lang = 'gu_IN'
    trg_lang = 'te_IN'
    df_src = 'gujrati'
    df_trg = 'telugu'
    save_model = 'translation-gu-te'

elif from_and_to_nmt == "bengali-to-hindi":
    INPUT_LANG = "bengali"
    TARGET_LANG = "hindi"
    src_lang = 'bn_IN'
    trg_lang = 'hi_IN'
    df_src = 'bengali'
    df_trg = 'hindi'
    save_model = 'translation-bn-hi'
else:
    print("Please modify your config file.")