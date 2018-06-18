import tensorflow as tf
from tensorflow.contrib import rnn


def cosine_similarity(x, y, axis=0, **kwargs):
    return tf.subtract(tf.constant(1.0), tf.losses.cosine_distance(x, y, axis, **kwargs))


def model(word2vec_size):
    timesteps = None  # Answers are in a dynamic length
    num_hidden = 128
    pooling_size = 3
    answer_placeholder = rnn_placeholder(timesteps, word2vec_size)
    question_placeholder = rnn_placeholder(timesteps, word2vec_size)
    rand_answer_placeholder = rnn_placeholder(timesteps, word2vec_size)
    strides = [1]
    M = 2

    def lstm(num_hidden):
        return rnn.BasicLSTMCell(num_units=num_hidden, activation=tf.tanh)

    lstm_fw_cell = lstm(num_hidden)
    lstm_bw_cell = lstm(num_hidden)

    def bidirectional_pooled_rnn(placeholder):
        outputs, _, _ = rnn.stack_bidirectional_dynamic_rnn(
            cells_fw=lstm_fw_cell, cells_bw=lstm_bw_cell, inputs=placeholder, dtype=tf.float32)
        outputs = tf.layers.average_pooling1d(
            answer_outputs, pool_size=pooling_size, strides=strides)
        return outputs
    answer_outputs = bidirectional_pooled_rnn(answer_placeholder)
    question_outputs = bidirectional_pooled_rnn(question_placeholder)
    rand_answer_outputs = bidirectional_pooled_rnn(rand_answer_placeholder)

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
    yield None*3

if __name__ == '__main__':
    word2vec_size = 100
    EPOCH_AMOUNT = 20
    BATCH_SIZE = 30
    answer_placeholder, question_placeholder, rand_answer_placeholder, answer_outputs, loss = model(
        word2vec_size)
    optimizer = tf.train.AdamOptimizer().minimize(loss)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch_i in range(EPOCH_AMOUNT):
            for answer_batch,question_batch,random_answer_batch in generate_batch(BATCH_SIZE):
                sess.run(optimizer, feed_dict={
                         answer_placeholder: answer_batch, question_placeholder: question_batch, rand_answer_placeholder: random_answer_batch})
