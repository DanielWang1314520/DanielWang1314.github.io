import numpy as np
import random
# import tensorflow as tf
import matplotlib.pyplot as plt
# tf.__version__
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow.examples.tutorials.mnist import input_data

k = 20


def shuffer_images_and_labels(images, labels):
    shuffle_indices = np.random.permutation(np.arange(len(images)))
    shuffled_images = images[shuffle_indices]
    shuffled_labels = labels[shuffle_indices]
    return shuffled_images, shuffled_labels


def get_label(label):
    return np.argmax(label)


def batch_iter(images, labels, batch_size, epoch_num, shuffle=True):
    data_size = len(images)

    num_batches_per_epoch = int(data_size / batch_size)  # 样本数/batch块大小,多出来的“尾数”，不要了

    for epoch in range(epoch_num):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))

            shuffled_data_feature = images[shuffle_indices]
            shuffled_data_label = labels[shuffle_indices]
        else:
            shuffled_data_feature = images
            shuffled_data_label = labels

        for batch_num in range(num_batches_per_epoch):  # batch_num取值0到num_batches_per_epoch-1
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)

            yield (shuffled_data_feature[start_index:end_index], shuffled_data_label[start_index:end_index])


def fcn_layer(inputs,  # 输入数据
              input_dim,  # 输入神经元数量
              output_dim,  # 输出神经元数量
              activation=None):  # 激活函数
    W = tf.Variable(tf.truncated_normal([input_dim, output_dim], stddev=0.1))  # 随机数生成的数据如果比标准差两倍还要大
    # 就要被替换掉
    b = tf.Variable(tf.zeros([output_dim]))  # 初始化为0

    XWb = tf.matmul(inputs, W) + b

    if activation is None:
        outputs = XWb
    else:
        outputs = activation(XWb)

    return outputs


def cross_validation(images, labels, k):
    X_train_images = []  # 大小为k-1
    y_train_labels = []
    X_test_images = []  # 大小为1
    y_test_labels = []

    zero_images = []
    zero_labels = []
    one_images = []
    one_labels = []
    two_images = []
    two_labels = []
    three_images = []
    three_labels = []
    four_images = []
    four_labels = []
    five_images = []
    five_labels = []
    six_images = []
    six_labels = []
    severn_images = []
    severn_labels = []
    eight_images = []
    eight_labels = []
    nine_images = []
    nine_labels = []

    for i in range(len(images)):
        if get_label(labels[i]) == 0:
            zero_images.append(images[i])
            zero_labels.append(labels[i])
        if get_label(labels[i]) == 1:
            one_images.append(images[i])
            one_labels.append(labels[i])
        if get_label(labels[i]) == 2:
            two_images.append(images[i])
            two_labels.append(labels[i])
        if get_label(labels[i]) == 3:
            three_images.append(images[i])
            three_labels.append(labels[i])
        if get_label(labels[i]) == 4:
            four_images.append(images[i])
            four_labels.append(labels[i])
        if get_label(labels[i]) == 5:
            five_images.append(images[i])
            five_labels.append(labels[i])
        if get_label(labels[i]) == 6:
            six_images.append(images[i])
            six_labels.append(labels[i])
        if get_label(labels[i]) == 7:
            severn_images.append(images[i])
            severn_labels.append(labels[i])
        if get_label(labels[i]) == 8:
            eight_images.append(images[i])
            eight_labels.append(labels[i])
        if get_label(labels[i]) == 9:
            nine_images.append(images[i])
            nine_labels.append(labels[i])

    total_images = [zero_images, one_images, two_images, three_images, four_images,
                    five_images, six_images, severn_images, eight_images, nine_images]

    total_labels = [zero_labels, one_labels, two_labels, three_labels, four_labels,
                    five_labels, six_labels, severn_labels, eight_labels, nine_labels]

    for i in range(10):
        k_total_images = []
        k_total_labels = []  # 大小为k

        for j in range(k):
            k_total_images.append(total_images[i][int(j * len(total_images[i]) / k):int(
                (j + 1) * len(total_images[i]) / k)])  # 长度为k*10，里面的列表长度为len(total_images[i])/k
            k_total_labels.append(
                total_labels[i][int(j * len(total_images[i]) / k):int((j + 1) * len(total_images[i]) / k)])

        idex = random.randrange(0, k, 1)
        X_test_images += k_total_images[idex]  # 大小为1
        y_test_labels += k_total_labels[idex]
        del k_total_images[idex]  # 大小为k-1
        del k_total_labels[idex]
        X_train_images += k_total_images  # 大小为k-1
        y_train_labels += k_total_labels

    f_X_train_images = []
    f_y_train_labels = []

    for i in range(10 * (k - 1)):
        for j in range(len(X_train_images[i])):
            f_X_train_images.append(X_train_images[i][j])  # 大小为k-1
            f_y_train_labels.append(y_train_labels[i][j])

    f_X_train_images, f_y_train_labels = np.array(f_X_train_images), np.array(f_y_train_labels)
    X_test_images, y_test_labels = np.array(X_test_images), np.array(y_test_labels)
    return (f_X_train_images, f_y_train_labels, X_test_images, y_test_labels)


# 读取数据集

mnist = input_data.read_data_sets('./mnist_dataset', one_hot=True)

# 把train数据集的标签和图像打乱
total_images = mnist.train.images
total_labels = mnist.train.labels
total_images, total_labels = shuffer_images_and_labels(total_images, total_labels)

# 验证集保持不变
total_validation_images = mnist.validation.images
total_validation_labels = mnist.validation.labels
total_validation_images, total_validation_labels = shuffer_images_and_labels(
    total_validation_images, total_validation_labels)

origin_images_train, origin_labels_train, origin_images_test, origin_labels_test = cross_validation(total_images, total_labels, k)

# 构建和训练模型
def train_and_test(images_train, labels_train, images_test,
                   labels_test,images_validation, labels_validation):
    
    #构建输入层
    x = tf.placeholder(tf.float32,[None,784],name="X")

    #0-9 一共10个数字=>10个类别
    y = tf.placeholder(tf.float32,[None,10],name="Y")
    
    
    #隐层层为2层
    h1 = fcn_layer(inputs=x,
              input_dim=784,
              output_dim=256,
              activation=tf.nn.relu)
    
    h2 = fcn_layer(inputs=h1,
              input_dim=256,
              output_dim=64,
              activation=tf.nn.relu)
    
    h3 = fcn_layer(inputs=h2,
        input_dim=64,
        output_dim=56,
        activation=tf.nn.relu)

    #输出层

    # 第一种模型
    forward = fcn_layer(inputs=h2,
                   input_dim=64,
                   output_dim=10,
                   activation=None)
    pred = tf.nn.softmax(forward)
    

    # 第二种模型
    # forward = fcn_layer(inputs=h3,
    #                input_dim=56,
    #                output_dim=10,
    #                activation=None)
    # pred = tf.nn.softmax(forward)


    loss_function = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(logits=forward,labels=y))
    
    
    train_epochs = 20 #训练轮数
    batch_size = 64   #单次训练样本数（批次大小）
    total_batch = int(mnist.train.num_examples/batch_size)  #一轮训练有多少批次
    display_step = 1  #显示粒度
    learning_rate = 0.001  #学习率
    
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss_function)
    
    correct_prediction = tf.equal(tf.argmax(pred,1),tf.argmax(y,1))

    #准确率，将布尔值转化为浮点数，并计算平均值
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    
    #save_step = 5
    
    #saver = tf.train.Saver()
    
    from time import time
    startTime = time()
    
    sess = tf.Session() #声明会话
    init = tf.global_variables_initializer() #初始化变量
    sess.run(init)
    
    for epoch in range(train_epochs):
        for a,b in batch_iter(images_train,labels_train, batch_size, 1, shuffle=True):
            xs,ys =a,b
            sess.run(optimizer,feed_dict={x:xs,y:ys})
            
        loss,acc = sess.run([loss_function,accuracy],
                       feed_dict = {x:images_validation,y:labels_validation})
    
        if(epoch+1) % display_step==0:
            print("train epoch:",'%02d' %(epoch+1),"Loss=","{:.9f}".format(loss),\
             "accuracy=","{:.4f}".format(acc))
    
    duration=time()-startTime    
    print("train finished takes:","{:.2f}".format(duration))
    
    #测试集测试
    accu_test = sess.run(accuracy,feed_dict={x:images_test,y:labels_test})
    print("test accuracy:",accu_test)
    
train_and_test(origin_images_train, origin_labels_train, origin_images_test,
origin_labels_test,total_validation_images, total_validation_labels)