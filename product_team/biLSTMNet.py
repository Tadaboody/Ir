import tensorflow as tf
from tensorflow.contrib import rnn

from product_team import WORD2VEC_SIZE, load_index

index = load_index()


def cosine_similarity(x, y, axis=0, **kwargs):
    return tf.subtract(tf.constant(1.0), tf.losses.cosine_distance(x, y, axis, **kwargs))


def model(word2vec_size, max_sentence_length):
    timesteps = max_sentence_length  # Answers are in a dynamic length
    layer_size = 128
    num_hidden_layers = 5
    pooling_size = 3
    strides = [1]
    M = 2.0

    def lstm(layer_size, num_layers):
        return [rnn.BasicLSTMCell(num_units=layer_size, activation=tf.tanh) for _ in range(num_layers)]
    lstm_fw_cell = lstm(layer_size, num_hidden_layers)
    lstm_bw_cell = lstm(layer_size, num_hidden_layers)

    def pass_through_model():
        placeholder = tf.placeholder(
            "float", shape=[None, timesteps, word2vec_size])
        # placeholder_through_time = tf.unstack(
        #     placeholder, num=timesteps, axis=1)
        placeholder_through_time = placeholder
        outputs, _, _ = rnn.stack_bidirectional_dynamic_rnn(
            cells_fw=lstm_fw_cell, cells_bw=lstm_bw_cell, inputs=placeholder_through_time,
            dtype=tf.float32)
        outputs = tf.layers.average_pooling1d(
            outputs, pool_size=pooling_size, strides=strides)
        return placeholder, outputs

    answer_placeholder, answer_outputs = pass_through_model()
    question_placeholder, question_outputs = pass_through_model()
    rand_answer_placeholder, rand_answer_outputs = pass_through_model()
    loss = model_loss(M, answer_outputs, question_outputs, rand_answer_outputs)
    return answer_placeholder, question_placeholder, rand_answer_placeholder, answer_outputs, loss


def model_loss(M, answer_outputs, question_outputs, rand_answer_outputs):
    loss = tf.subtract(tf.constant(M), cosine_similarity(
        answer_outputs, question_outputs))
    loss = tf.add(loss, cosine_similarity(
        question_outputs, rand_answer_outputs))
    loss = tf.nn.relu(loss)
    return loss


def rnn_placeholder(timesteps, word2vec_size):
    questions = tf.placeholder("float", shape=[None, timesteps, word2vec_size])
    questions = tf.unstack(questions, timesteps, 1)
    return questions


def generate_batch(batch_size):
    return index.generate_batch(batch_size)


def train():
    word2vec_size = WORD2VEC_SIZE
    EPOCH_AMOUNT = 20
    BATCH_SIZE = 30
    max_sentence_length = index.max_sentence_length
    answer_placeholder, question_placeholder, rand_answer_placeholder, answer_outputs, loss = model(
        word2vec_size, max_sentence_length)
    optimizer = tf.train.AdamOptimizer().minimize(loss)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch_i in range(EPOCH_AMOUNT):
            for answer_batch, question_batch, random_answer_batch in generate_batch(BATCH_SIZE):
                sess.run(optimizer, feed_dict={
                         answer_placeholder: answer_batch, question_placeholder: question_batch, rand_answer_placeholder: random_answer_batch})
                print("batch!")
            print("epoch!")
