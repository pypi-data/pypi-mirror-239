class dlcode:
    def __init__(self):
        pass

    def print_code(self, code):
        print(code)

    def dl1(self):
        code = """
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# Define the XOR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])

# Create a neural network model
model = Sequential()
model.add(Dense(8, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10000, verbose=0)

# Evaluate the model
loss, accuracy = model.evaluate(X, y)
print(f"Loss: {loss:.4f}, Accuracy: {accuracy*100:.2f}%")

# Make predictions
predictions = model.predict(X)
rounded_predictions = [round(pred[0]) for pred in predictions]
print("Predictions:")
for i in range(len(X)):
    print(f"Input: {X[i]}, Predicted: {rounded_predictions[i]}, Actual: {y[i]}")

"""
        self.print_code(code)

    def dl2(self):
        code = """
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np
import matplotlib.pyplot as plt

# Load and preprocess the MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_train = X_train / 255.0
X_test = X_test / 255.0
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# Create a CNN model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_test, y_test))

# Make predictions
predicted_probabilities = model.predict(X_test)
predicted_classes = np.argmax(predicted_probabilities, axis=1)

# Visualize predicted images
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.imshow(X_test[i].reshape(28, 28), cmap='gray')
    plt.title(f"Predicted: {predicted_classes[i]}")
    plt.axis('off')

plt.show()
        """
        self.print_code(code)

    def dl3(self):
        code = """
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
# Load the LFW dataset
lfw_dataset = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
# Extract the images and labels
images = lfw_dataset.images
labels = lfw_dataset.target
target_names = lfw_dataset.target_names
# Preprocess the data
images = images.astype('float32') / 255
labels = to_categorical(labels)
# Split the data into training and testing sets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels,
test_size=0.2)
# Create the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(50, 37, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(len(target_names), activation='softmax'))
# Compile and train the model
model.compile(optimizer='rmsprop',
 loss='categorical_crossentropy',
 metrics=['accuracy'])
model.fit(train_images, train_labels, batch_size=32, epochs=10)
# Evaluate the model
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)
# Select a sample image for prediction
11
sample_index = 0
sample_image = test_images[sample_index]
sample_label = np.argmax(test_labels[sample_index])
sample_name = target_names[sample_label]
# Make a prediction on the sample image
sample_image = np.expand_dims(sample_image, axis=0)
prediction = model.predict(sample_image)
predicted_label = np.argmax(prediction)
predicted_name = target_names[predicted_label]
# Display the sample image and the predicted and true labels
plt.imshow(sample_image[0], cmap='gray')
plt.title(f'Predicted: {predicted_name}\nTrue: {sample_name}')
plt.axis('off')
plt.show()
"""
        self.print_code(code)

    def dl4(self):
        code = """
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample text data
corpus = [
    'This is the first sentence.',
    'Here is the second sentence.',
    'Finally, the third sentence.'
]

# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1

# Create input sequences
input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad input sequences
max_sequence_length = max([len(seq) for seq in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')

# Create predictors and labels
X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

# Build an RNN model
model = Sequential()
model.add(Embedding(total_words, 64, input_length=max_sequence_length - 1))
model.add(LSTM(100))
model.add(Dense(total_words, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=100, verbose=1)

# Generate text
seed_text = "Here is"
next_words = 5

for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')
    predicted = np.argmax(model.predict(token_list), axis=-1)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    seed_text += " " + output_word

print(seed_text)
"""
        self.print_code(code)

    def dl5(self):
        code = """
import numpy as np
from keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences  # Updated import
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding

# Set the maximum number of words to consider in the vocabulary
max_words = 10000

# Load the IMDB dataset with only the most frequent max_words words
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_words)

# Pad the sequences to have the same length for inputting into the LSTM
max_len = 200
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

# Define the LSTM model
model = Sequential()
model.add(Embedding(max_words, 128, input_length=max_len))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=6, batch_size=40, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {accuracy*100:.2f}%')

# Function to predict sentiment from user input
def predict_sentiment(review):
    # Tokenize and pad the input review
    review_seq = [word_index[word] for word in review.lower().split() if word in word_index]
    review_seq = pad_sequences([review_seq], maxlen=max_len)
    # Predict sentiment using the trained model
    prediction = model.predict(review_seq)[0, 0]
    # Print the predicted sentiment
    if prediction >= 0.5:
        print("Positive sentiment!")
    else:
        print("Negative sentiment!")

# Get user input and make predictions
word_index = imdb.get_word_index()
while True:
    user_input = input("Enter a movie review (type 'exit' to stop): ")
    if user_input.lower() == 'exit':
        break
    predict_sentiment(user_input)

"""
        self.print_code(code)

    def dl6(self):
        code = """
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Training data
training_data = [
    ("The", "DT"),
    ("quick", "JJ"),
    ("brown", "JJ"),
    ("fox", "NN"),
    ("jumps", "VBZ"),
    ("over", "IN"),
    ("the", "DT"),
    ("lazy", "JJ"),
    ("dog", "NN"),
]

# Vocabularies
word_vocab = {word: idx for idx, (word, _) in enumerate(training_data)}
tag_vocab = {tag: idx for idx, (_, tag) in enumerate(training_data)}
reverse_tag_vocab = {idx: tag for tag, idx in tag_vocab.items()}

# Model
class Seq2Seq(nn.Module):
    def __init__(self, input_dim, emb_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.rnn = nn.LSTM(emb_dim, hidden_dim)
        self.out = nn.Linear(hidden_dim, output_dim)

    def forward(self, src):
        embedded = self.embedding(src)
        output, hidden = self.rnn(embedded)
        prediction = self.out(output)
        return prediction

# Dataset
class POSTaggingDataset(Dataset):
    def __init__(self, data, word_vocab, tag_vocab):
        self.data = data
        self.word_vocab = word_vocab
        self.tag_vocab = tag_vocab

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        word, tag = self.data[idx]
        word_idx = self.word_vocab[word]
        tag_idx = self.tag_vocab[tag]
        return word_idx, tag_idx

# Hyperparameters
INPUT_DIM = len(word_vocab)
OUTPUT_DIM = len(tag_vocab)
EMB_DIM = 32
HIDDEN_DIM = 64
BATCH_SIZE = 1
N_EPOCHS = 10

# Model, optimizer, dataloaders
model = Seq2Seq(INPUT_DIM, EMB_DIM, HIDDEN_DIM, OUTPUT_DIM)
optimizer = optim.Adam(model.parameters())

train_data = POSTaggingDataset(training_data, word_vocab, tag_vocab)
train_iterator = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)

# Training loop
for epoch in range(N_EPOCHS):
    for batch in train_iterator:
        src, trg = batch
        optimizer.zero_grad()

        output = model(src)

        # Clamp target indices before passing to loss
        trg = trg.clamp(max=OUTPUT_DIM-1)

        loss = F.cross_entropy(output, trg)
        loss.backward()
        optimizer.step()

# Inference
with torch.no_grad():
  example_word = "lazy"
  example_idx = torch.tensor([word_vocab[example_word]])
  predicted_tag_idx = model(example_idx).argmax()

  predicted_tag = reverse_tag_vocab[predicted_tag_idx.item()]

print(predicted_tag)
"""
        self.print_code(code)

    def dl7(self):
        code = """
with open('/kaggle/input/asssasa/deu-eng.txt', 'r', encoding='utf-8') as f:
  lines = f.read().split('\n')
input_texts = []
target_texts = []
input_characters = set()
target_characters = set()
num_samples = 10000
for line in lines[: min(num_samples, len(lines) - 1)]:
  input_text, target_text = line.split('\t')
  target_text = '\t' + target_text + '\n'
  input_texts.append(input_text)
  target_texts.append(target_text)
  for char in input_text:
    if char not in input_characters:
      input_characters.add(char)
  for char in target_text:
    if char not in target_characters:
      target_characters.add(char)
input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])
input_token_index = dict(
  [(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict(
  [(char, i) for i, char in enumerate(target_characters)])
import numpy as np

encoder_input_data = np.zeros(
  (len(input_texts), max_encoder_seq_length, num_encoder_tokens),
  dtype='float32')
decoder_input_data = np.zeros(
  (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
  dtype='float32')
decoder_target_data = np.zeros(
  (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
  dtype='float32')

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
  for t, char in enumerate(input_text):
    encoder_input_data[i, t, input_token_index[char]] = 1.
  for t, char in enumerate(target_text):
    # decoder_target_data is ahead of decoder_input_data by one timestep
    decoder_input_data[i, t, target_token_index[char]] = 1.
    if t > 0:
      # decoder_target_data will be ahead by one timestep
      # and will not include the start character.
      decoder_target_data[i, t - 1, target_token_index[char]] = 1.
import keras, tensorflow
from keras.models import Model
from keras.layers import Input, LSTM, Dense
import numpy as np
batch_size = 64  # batch size for training
epochs = 100  # number of epochs to train for
latent_dim = 256
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                     initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)
model = Model(inputs=[encoder_inputs, decoder_inputs], 
              outputs=decoder_outputs)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.2)
model.save('seq2seq_eng-ger.h5')
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.load_weights('/kaggle/working/seq2seq_eng-ger.h5')
encoder_model = Model(encoder_inputs, encoder_states)

decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_outputs, state_h, state_c = decoder_lstm(
  decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)

decoder_model = Model(
  [decoder_inputs] + decoder_states_inputs,
  [decoder_outputs] + decoder_states)
reverse_input_char_index = dict(
  (i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict(
  (i, char) for char, i in target_token_index.items())
def decode_sequence(input_seq):
  # encode the input sequence to get the internal state vectors.
  states_value = encoder_model.predict(input_seq)
  
  # generate empty target sequence of length 1 with only the start character
  target_seq = np.zeros((1, 1, num_decoder_tokens))
  target_seq[0, 0, target_token_index['\t']] = 1.
  
  # output sequence loop
  stop_condition = False
  decoded_sentence = ''
  while not stop_condition:
    output_tokens, h, c = decoder_model.predict(
      [target_seq] + states_value)
    
    # sample a token and add the corresponding character to the 
    # decoded sequence
    sampled_token_index = np.argmax(output_tokens[0, -1, :])
    sampled_char = reverse_target_char_index[sampled_token_index]
    decoded_sentence += sampled_char
    
    # check for the exit condition: either hitting max length
    # or predicting the 'stop' character
    if (sampled_char == '\n' or 
        len(decoded_sentence) > max_decoder_seq_length):
      stop_condition = True
      
    # update the target sequence (length 1).
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, sampled_token_index] = 1.
    
    # update states
    states_value = [h, c]
    
  return decoded_sentence
for seq_index in range(10):
  input_seq = encoder_input_data[seq_index: seq_index + 1]
  decoded_sentence = decode_sequence(input_seq)
  print('-')
  print('Input sentence:', input_texts[seq_index])
  print('Decoded sentence:', decoded_sentence)
"""
        self.print_code(code)

    def dl8(self):
        code = """
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# Load the MNIST dataset
(x_train, _), (_, _) = keras.datasets.mnist.load_data()

# Preprocess the dataset
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32')
x_train = (x_train - 127.5) / 127.5  # Normalize to the range [-1, 1]

# Define the generator model
def build_generator():
    model = keras.Sequential()
    model.add(layers.Dense(7 * 7 * 256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((7, 7, 256)))

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    return model

# Define the discriminator model
def build_discriminator():
    model = keras.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same', input_shape=(28, 28, 1)))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

# Define the loss functions
cross_entropy = keras.losses.BinaryCrossentropy(from_logits=True)

def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss

# Define the optimizers
generator_optimizer = keras.optimizers.Adam(1e-4)
discriminator_optimizer = keras.optimizers.Adam(1e-4)

# Define the generator and discriminator models
generator = build_generator()
discriminator = build_discriminator()

# Define the training loop
@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, 100])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

# Generate and save sample images
def generate_and_save_images(model, epoch, test_input):
    predictions = model(test_input, training=False)
    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
        plt.axis('off')

    plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
    plt.show()

# Training parameters
EPOCHS = 100
BATCH_SIZE = 64

# Training loop
seed = tf.random.normal([16, 100])

for epoch in range(EPOCHS):
    for i in range(0, x_train.shape[0], BATCH_SIZE):
        image_batch = x_train[i:i+BATCH_SIZE]
        train_step(image_batch)

    if (epoch + 1) % 10 == 0:
        generate_and_save_images(generator, epoch + 1, seed)

"""
        self.print_code(code)

