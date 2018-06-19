from os.path import join

import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn

from product_team import SAVE_DIR, WORD2VEC_SIZE, load_index

index = load_index()


def cosine_similarity(x, y, axis=-1, **kwargs):
    x = tf.nn.l2_normalize(x, axis=axis)
    y = tf.nn.l2_normalize(y, axis=axis)

    return tf.subtract(tf.constant(1.0), tf.losses.cosine_distance(x, y, axis, **kwargs))


def model(word2vec_size, max_sentence_length):
    timesteps = max_sentence_length  # Answers are in a dynamic length
    layer_size = 128
    num_hidden_layers = 5
    pooling_size = 3
    strides = [1]
    M = 3.0

    def lstm(layer_size, num_layers):
        return [rnn.BasicLSTMCell(num_units=layer_size, activation=tf.tanh) for _ in range(num_layers)]

    def pass_through_model():
        placeholder = tf.placeholder(
            "float", shape=[None, timesteps, word2vec_size])
        placeholder_through_time = tf.unstack(
            placeholder, num=timesteps, axis=1)
        placeholder_through_time = placeholder
        with tf.variable_scope('RNN', reuse=tf.AUTO_REUSE):
            lstm_fw_cell = lstm(layer_size, num_hidden_layers)
            lstm_bw_cell = lstm(layer_size, num_hidden_layers)
            outputs, _, _ = rnn.stack_bidirectional_dynamic_rnn(
                cells_fw=lstm_fw_cell, cells_bw=lstm_bw_cell, inputs=placeholder_through_time,
                dtype=tf.float32)
            # outputs = tf.layers.conv1d(placeholder_through_time, filters=32, kernel_size=3)
            outputs = tf.layers.dense(outputs, layer_size)
            outputs = tf.layers.average_pooling1d(
                outputs, pool_size=pooling_size, strides=strides)
            return placeholder, outputs

    answer_placeholder, answer_outputs = pass_through_model()
    question_placeholder, question_outputs = pass_through_model()
    rand_answer_placeholder, rand_answer_outputs = pass_through_model()
    loss = model_loss(M, answer_outputs, question_outputs, rand_answer_outputs)
    return answer_placeholder, question_placeholder, rand_answer_placeholder, question_outputs, loss


# def sf_cosine_similarity(a, b, axis=-1):
#     normalize_a = tf.nn.l2_normalize(a, axis=axis)
#     normalize_b = tf.nn.l2_normalize(b, axis=axis)
#     return tf.reduce_sum(tf.multiply(normalize_a, normalize_b))


def model_loss(M, answer_outputs, question_outputs, rand_answer_outputs):
    loss = tf.subtract(tf.constant(M), cosine_similarity(
        answer_outputs, question_outputs))
    loss = tf.add(loss, cosine_similarity(
        question_outputs, rand_answer_outputs))
    loss = tf.maximum(0.0, loss)
    return loss


def rnn_placeholder(timesteps, word2vec_size):
    questions = tf.placeholder("float", shape=[None, timesteps, word2vec_size])
    questions = tf.unstack(questions, timesteps, 1)
    return questions


def generate_batch(batch_size):
    return index.generate_batch(batch_size)


MODEL_PATH = join(SAVE_DIR,'bilstmnet.ckpt')
def train(restore = False):
    word2vec_size = WORD2VEC_SIZE
    EPOCH_AMOUNT = 20
    BATCH_SIZE = index.test_size//80
    max_sentence_length = index.normalize_vector_length
    answer_placeholder, question_placeholder, rand_answer_placeholder, question_outputs, loss_op = model(
        word2vec_size, max_sentence_length)
    optimizer = tf.train.AdamOptimizer(
        learning_rate=0.001).minimize(loss_op)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        if restore:
            saver.restore(sess, MODEL_PATH)
        for epoch_i in range(EPOCH_AMOUNT):
            for batch_num, (answer_batch, question_batch, random_answer_batch) in enumerate(generate_batch(BATCH_SIZE)):
                _, loss_val = sess.run([optimizer, loss_op], feed_dict={
                    answer_placeholder: answer_batch, question_placeholder: question_batch, rand_answer_placeholder: random_answer_batch})
                print(f"batch #{batch_num} loss={loss_val}")
            print(f"epoch {epoch_i} done")
            saver.save(sess, MODEL_PATH)

def run(vector :np.ndarray):
    word2vec_size = WORD2VEC_SIZE
    max_sentence_length = index.normalize_vector_length
    answer_placeholder, question_placeholder, rand_answer_placeholder, question_outputs, loss_op = model(
        word2vec_size, max_sentence_length)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess,MODEL_PATH)
        return sess.run(question_outputs, feed_dict={question_placeholder: [vector]})[0]
