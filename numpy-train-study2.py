#简单神经网络测试实例
import numpy as np

def tanh(x):  #双曲函数
    return np.tanh(x)

def tanh_deriv(x):#更新权重时，需要用到双曲函数的倒数
    return 1.0 - np.tanh(x)*np.tanh(x)

def logistic(x):#构建逻辑函数
    return 1/(1 + np.exp(-x))

def logistic_derivatic(x):  #逻辑函数的倒数
    return logistic(x)*(1 - logistic(x))

class NeuralNetwork:
    def __init__(self,layer,activation='tanh'):
        '''
        :param layer:A list containing the number of unit in each layer.
        Should be at least two values.每层包含的神经元数目
        :param activation: the activation function to be used.Can be
        "logistic" or "tanh"
        '''
        if activation == 'logistic':
            self.activation = logistic
            self.activation_deriv = logistic_derivatic
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_deriv = tanh_deriv

        self.weights = []
        for i in range(1,len(layer) - 1):#权重的设置
            self.weights.append((2*np.random.random((layer[i - 1] + 1,layer[i] + 1))-1)*0.25)
            self.weights.append((2*np.random.random((layer[i] + 1,layer[i+1]))-1)*0.25)
    '''训练神经网络，通过传入的数据，不断更新权重weights'''
    def fit(self,X,y,learning_rate=0.2,epochs=10000):
        '''
        :param X: 数据集
        :param y: 数据输出结果，分类标记
        :param learning_rate: 学习率
        :param epochs: 随机抽取的数据的训练次数
        :return:
        '''
        X = np.atleast_2d(X) #转化X为np数据类型，试数据类型至少是两维的
        temp = np.ones([X.shape[0],X.shape[1]+1])
        temp[:,0:-1] = X
        X = temp
        y = np.array(y)

        for k in range(epochs):
            i = np.random.randint(X.shape[0])  #随机抽取的行
            a = [X[i]]

            for I in range(len(self.weights)):#完成正向所有的更新
                a.append(self.activation(np.dot(a[I],self.weights[I])))#dot():对应位相乘后相加
            error = y[i] - a[-1]
            deltas = [error * self.activation_deriv(a[-1])]#*self.activation_deriv(a[I])#输出层误差
            # 反向更新
            for I in range(len(a) -2,0,-1):
                deltas.append(deltas[-1].dot(self.weights[I].T)*self.activation_deriv(a[I]))
            deltas.reverse()
            for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate*layer.T.dot(delta)

    def predict(self,x):
        x = np.array(x)
        temp = np.ones(x.shape[0] + 1)
        temp[0:-1] = x
        a = temp
        for I in range(0,len(self.weights)):
            a = self.activation(np.dot(a,self.weights[I]))
        return a  #只需要保存最后的值，就是预测出来的值
nn = NeuralNetwork([2,2,1], 'tanh')
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])
nn.fit(X, y)
for i in [[0, 0], [0, 1], [1, 0], [1,1]]:
    print(i, nn.predict(i))

#from sklearn.datasets import load_digits #导入数据集
#from sklearn.metrics import confusion_matrix,classification_report   #对结果的预测的包
#from sklearn.preprocessing import LabelBinarizer  #把数据转化为二维的数字类型
#from sklearn.cross_validation import train_test_split   #可以把数据拆分成训练集与数据集

#digits = load_digits()  #把数据改成0到1之间
#X = digits.data
#y = digits.target
#X -= X.min()
#X /= X.max()

#nn = NeuralNetwork([64,100,10],'logistic')
#X_train,X_test,y_train,y_test = train_test_split(X,y)
#labels_train = LabelBinarizer().fit_transform(y_train)
#labels_test = LabelBinarizer().fit_transform(y_test)
#print("start fitting")
#nn.fit(X_train,labels_train,epochs=3000)
#predictions = []
#for i in range(X_test.shape[0]):
#    o = nn.predict(X_test[i])
#    predictions.append(np.argmax(o))
#print(confusion_matrix(y_test,predictions))
#print(classification_report(y_test,predictions))