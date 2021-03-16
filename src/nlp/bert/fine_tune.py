""" BERT fine-tune pre-trained model
"""

from transformers import TFBertForSequenceClassification
import tensorflow as tf

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from nlp.sentiment import preprocess

def fine_tune(max_length = 512, batch_size = 6, train_size = 200):
    """ Model fit for fine-tuning a BERT pre-trained model

    Args:
        max_length (int, optional): According to official Stocktwits docs, a stocktwit is limited to 1000 characters, so we can assume the message would not be longer than 512 tokens. However, if that happens to be the case, we can truncate the few overflow tokens. Can be up to 512 for BERT. Defaults to 512.
        batch_size (int, optional): the recommended batches size for BERT are 16,32 ... however on this dataset we are overfitting quite fast and smaller batches work like a regularization. Defaults to 6.
        train_size (int, optional): Defaults to 200.
    """

    train_encoded, test_encoded = preprocess.preprocess(train_size=train_size, max_length=max_length, batch_size=batch_size)
    
    # recommended learning rate for Adam 5e-5, 3e-5, 2e-5
    learning_rate = 2e-5

    # multiple epochs might be better as long as we will not overfit the model
    number_of_epochs = 1

    # model initialization
    model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')

    # classifier Adam recommended
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, epsilon=1e-08)

    # we do not have one-hot vectors, we can use sparce categorical cross entropy and accuracy
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

    model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

    print(model.summary())

    bert_history = model.fit(train_encoded, epochs=number_of_epochs, validation_data=test_encoded)
    
    model.save("model/bert")

# fine_tune()