import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf


img_height = 256
img_width = 256
img_layer = 3
img_size = img_height * img_width

batch_size = 1
pool_size = 50

ngf = 32
ndf = 64


def instance_norm(x):

    with tf.variable_scope("intance_norm"):

        epsilon = 1e-5
        mean, var = tf.nn.moments(x, [1, 2], keep_dims=True)

        scale = tf.get_variable('scale', [x.get_shape()[-1]], initializer=tf.truncated_normal_initializer(mean=1.0, stddev=0.02))

        offset = tf.get_variable('offset', [x.get_shape()[-1]], initializer=tf.constant_initializer(0.0))

        output = scale * tf.div(x - mean, tf.sqrt(var + epsilon)) + offset

        return output


def leakyrelu(x, leaky=0.2, name='leakyrelu'):

    with tf.variable_scope(name):

        f1 = 0.5 * (1 + leaky)
        f2 = 0.5 * (1 - leaky)

    return f1 * x + f2 * abs(x)

def conv2d(inputconv, o_d=64, f_h=7, f_w=7, s_h=1, s_w=1, stddev=0.02, padding="VALID", name="conv2d", do_norm=True, do_relu=True, relufactor=0):
    with tf.variable_scope(name):

        conv = tf.contrib.layers.conv2d(inputconv, o_d, f_w, s_w, padding, activation_fn=None, weights_initializer=tf.truncated_normal_initializer(stddev=stddev),biases_initializer=tf.constant_initializer(0.0))
        if do_norm:
            conv = instance_norm(conv)
            # conv = tf.contrib.layers.batch_norm(conv, decay=0.9, updates_collections=None, epsilon=1e-5, scale=True, scope="batch_norm")

        if do_relu:
            if(relufactor == 0):
                conv = tf.nn.relu(conv,"relu")
            else:
                conv = leakyrelu(conv, relufactor, "leakyrelu")

        return conv

def deconv2d(inputconv, outshape, o_d=64, f_h=7, f_w=7, s_h=1, s_w=1, stddev=0.02, padding="VALID", name="deconv2d", do_norm=True, do_relu=True, relufactor=0):
    with tf.variable_scope(name):

        conv = tf.contrib.layers.conv2d_transpose(inputconv, o_d, [f_h, f_w], [s_h, s_w], padding, activation_fn=None, weights_initializer=tf.truncated_normal_initializer(stddev=stddev),biases_initializer=tf.constant_initializer(0.0))

        if do_norm:
            conv = instance_norm(conv)
            # conv = tf.contrib.layers.batch_norm(conv, decay=0.9, updates_collections=None, epsilon=1e-5, scale=True, scope="batch_norm")

        if do_relu:
            if(relufactor == 0):
                conv = tf.nn.relu(conv,"relu")
            else:
                conv = lrelu(conv, relufactor, "lrelu")

        return conv

def build_resnet_block(inputres, dim, name="resnet"):
    
    with tf.variable_scope(name):

        out_res = tf.pad(inputres, [[0, 0], [1, 1], [1, 1], [0, 0]], "REFLECT")
        out_res = conv2d(out_res, dim, 3, 3, 1, 1, 0.02, "VALID","c1")
        out_res = tf.pad(out_res, [[0, 0], [1, 1], [1, 1], [0, 0]], "REFLECT")
        out_res = conv2d(out_res, dim, 3, 3, 1, 1, 0.02, "VALID","c2",do_relu=False)
        
        return tf.nn.relu(out_res + inputres)


def build_generator_resnet_6blocks(inputconv, name='generator'):

    with tf.variable_scope(name):

        pad_input = tf.pad(inputconv, [[0, 0], [3, 3], [3, 3], [0, 0]], 'REFLECT')
        o_c1 = conv2d(pad_input, 32, 7, 7, 1, 1, 0.02, name='c1')
        o_c2 = conv2d(o_c1, 32*2, 7, 7, 2, 2, 0.02, 'SAME', 'c2')
        o_c3 = conv2d(o_c2, 32*4, 7, 7, 2, 2, 0.02, 'SAME', 'c3')

        o_r1 = build_resnet_block(o_c3, 32*4, 'r1')
        o_r2 = build_resnet_block(o_r1, 32*4, 'r2')
        o_r3 = build_resnet_block(o_r2, 32*4, 'r3')
        o_r4 = build_resnet_block(o_r3, 32*4, 'r4')
        o_r5 = build_resnet_block(o_r4, 32*4, 'r4')
        o_r6 = build_resnet_block(o_r5, 32*4, 'r5')

        o_c4 = deconv2d(o_r6, [batch_size, 64, 64, 32*2], 32*2, 7, 7, 2, 2, 0.02, 'SAME', 'c4')
        o_c5 = deconv2d(o_c4, [batch_size, 128, 128, 32], 32, 7, 7, 2, 2, 0.02, 'SAME','c5')
        o_c5_padding = tf.pad(o_c5, [[0, 0], [3, 3], [3, 3], [0, 0]], 'REFLECT')
        o_c6 = conv2d(o_c5_padding, img_layer, 7, 7, 1, 1, 0.02, 'VALID','c6', do_relu=False)


        output = tf.nn.tanh(o_c6, 't1')

    return output


def build_generator_resnet_9blocks(inputgen, name="generator"):
    with tf.variable_scope(name):
        f = 7
        ks = 3
        
        pad_input = tf.pad(inputgen,[[0, 0], [ks, ks], [ks, ks], [0, 0]], "REFLECT")
        o_c1 = conv2d(pad_input, ngf, f, f, 1, 1, 0.02,name="c1")
        o_c2 = conv2d(o_c1, ngf*2, ks, ks, 2, 2, 0.02,"SAME","c2")
        o_c3 = conv2d(o_c2, ngf*4, ks, ks, 2, 2, 0.02,"SAME","c3")

        o_r1 = build_resnet_block(o_c3, ngf*4, "r1")
        o_r2 = build_resnet_block(o_r1, ngf*4, "r2")
        o_r3 = build_resnet_block(o_r2, ngf*4, "r3")
        o_r4 = build_resnet_block(o_r3, ngf*4, "r4")
        o_r5 = build_resnet_block(o_r4, ngf*4, "r5")
        o_r6 = build_resnet_block(o_r5, ngf*4, "r6")
        o_r7 = build_resnet_block(o_r6, ngf*4, "r7")
        o_r8 = build_resnet_block(o_r7, ngf*4, "r8")
        o_r9 = build_resnet_block(o_r8, ngf*4, "r9")

        o_c4 = deconv2d(o_r9, [batch_size,128,128,ngf*2], ngf*2, ks, ks, 2, 2, 0.02,"SAME","c4")
        o_c5 = deconv2d(o_c4, [batch_size,256,256,ngf], ngf, ks, ks, 2, 2, 0.02,"SAME","c5")
        o_c6 = conv2d(o_c5, img_layer, f, f, 1, 1, 0.02,"SAME","c6",do_relu=False)

        # Adding the tanh layer

        out_gen = tf.nn.tanh(o_c6,"t1")


        return out_gen

def build_discriminator(inputconv, name='discriminator'):


    with tf.variable_scope(name):

        o_c1 = conv2d(inputconv, 64, 4, 4, 2, 2, 0.02, 'SAME', 'c1', do_norm=False, relufactor=0.2)
        o_c2 = conv2d(o_c1, 64*2, 4, 4, 2, 2, 0.02, 'SAME', 'c2', relufactor=0.2)
        o_c3 = conv2d(o_c2, 64*4, 4, 4, 2, 2, 0.02, 'SAME', 'c3', relufactor=0.2)
        o_c4 = conv2d(o_c3, 64*8, 4, 4, 2, 2, 0.02, 'SAME', 'c4', relufactor=0.2)
        o_c5 = conv2d(o_c4, 1, 4, 4, 2, 2, 0.02, 'SAME', 'c5', relufactor=0.2)

    return o_c5

