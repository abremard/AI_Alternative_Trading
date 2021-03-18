""" BERT use fine-tuned model for prediction
"""

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from stocktwits.sentiment import preprocess
from stocktwits.bert import tokenize

def load(path="model/bert"):
    return tf.keras.models.load_model(path)

def predict(pred_sentences):
    # Load model
    model = load()
    # Tokenize
    tokenizer = tokenize.init_tokenizer()
    for i, sentence in enumerate(pred_sentences):
        tf_batch = tokenize.tokenizer_plus(tokenizer=tokenizer, sentence=sentence)
        tf_outputs = model(tf_batch)
        tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
        labels = ['Bearish','Bullish']
        label = tf.argmax(tf_predictions, axis=1)
        label = label.numpy()
        print(pred_sentences[i], ": \n", labels[label[i]])

if __name__ == "__main__":
    from transformers import TFBertForSequenceClassification
    import tensorflow as tf