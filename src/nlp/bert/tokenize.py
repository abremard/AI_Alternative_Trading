""" Tokenize sentences for BERT input """

from transformers import BertTokenizer

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from utils import prettyprint as pp

def init_tokenizer():
    """ Initialize the tokenizer

    Returns:
        BertTokenizer.Object
    """    
    return BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

def tokenizer_plus(tokenizer, sentence, max_length=20):
    """ Tokenize plus function

    Args:
        tokenizer (BertTokenizer.Object)
        sentence (str): input sentence
        max_length (int, optional): Max length for padding. Defaults to 20.

    Returns:
        Dict: tokenized sentence
    """    
    # * Tokenization plus
    bert_input = tokenizer.encode_plus(
                            sentence,                      
                            add_special_tokens = True, # add [CLS], [SEP]
                            max_length = max_length, # max length of the text that can go to BERT
                            padding = 'max_length',
                            return_attention_mask = True, # add attention mask to not focus on pad tokens
                )
    return bert_input