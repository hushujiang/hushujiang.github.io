from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

mnist = tf.keras.datasets.mnist
#需要从 https://storage.googleapis.com/tensorflow/tf-keras-datasets/ 下载，执行过程非常缓慢，或者报证书错误可以直接从浏览器下载 https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz
#并保存到 ~/.kreas/datasets/ 目录下（c盘根目录）即可

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)