'''单例模式

以模块的方式定义，使用时直接引入singleton1这个实例即可
'''


class Singleton1:
    def __init__(self):
        self.val = 1


singleton1 = Singleton1()
