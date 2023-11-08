# 安装本项目：pip install start-zero   

本深度学习框架主要功能：   

| 序号 | 完成度  | 内容               | 备注                         |
|:--:|:----:|:-----------------|:---------------------------|
| 1  | 100% | 数值微分、自动微分、高阶求导   | 高阶求导double backpropagation |
| 2  | 100% | 处理标量和张量          | 封装、兼容numpy                 |
| 3  | 100% | 支持GPU运算          | 只支持N卡                      |
| 4  | 100% | Define-by-Run    | 运行时动态图（核心）                 |
| 5  | 100% | 实现常用函数的正向传播和反向传播 | 目前一共支持38个函数                |
| 6  |  0%  | 封装层（layer）       | 如CNN、RNN等                  |
| 7  |  0%  | Define-and-Run   | 静态图（暂时不会去实现，因为涉及领域特定语言）    |

目前支持的函数：   

| 序号 |    函数    |          符号           |  备注  |
|:--:|:--------:|:---------------------:|:----:|
| 1  |    加     |           +           |      |
| 2  |    减     |           -           |      |
| 3  |    乘     |           *           |      |
| 4  |    除     |           /           |      |
| 5  |    幂     |          **           |      |
| 6  |    负数    |           -           |      |
| 7  |    模     |           %           |      |
| 8  |    正弦    |          sin          |      |
| 9  |    余弦    |          cos          |      |
| 10 |    正切    |          tan          |      |
| 11 |   双曲正切   |         tanh          |      |
| 12 |  e为底的指数  |          exp          |      |
| 13 | 10为底的对数  |          lg           |      |
| 14 |  e为底的对数  |          ln           |      |
| 15 |   合并求和   |        sum_to         |  难   |
| 16 |    广播    |     broadcast_to      |  难   |
| 17 |    求和    |          sum          |  难   |
| 18 |   平均数    |        average        |  难   |
| 19 | 矩阵相乘（点乘） |        matmul         |      |
| 20 |   矩阵转置   |      transpose/T      |  难   |
| 21 |   重塑形状   |        reshape        |      |
| 22 |   线性回归   |        linear         |      |
| 23 |  S型生长曲线  |        sigmoid        | 激活函数 |
| 24 |  线性整流函数  |         ReLU          | 激活函数 |
| 25 | 归一化指数函数  |        softmax        | 激活函数 |
| 26 | 归一化指数函数  |      log_softmax      | 激活函数 |
| 27 |  线性整流函数  |      leaky_relu       | 激活函数 |
| 28 |   均方误差   |  mean_squared_error   | 损失函数 |
| 29 |  交叉熵损失   | softmax_cross_entropy | 损失函数 |
| 30 |  交叉熵损失   | sigmoid_cross_entropy | 损失函数 |
| 31 |  二元交叉熵   | binary_cross_entropy  | 损失函数 |
| 32 |   最大值    |          max          | 其它函数 |
| 33 |   最小值    |          min          | 其它函数 |
| 34 | 限定数组上下界  |         clip          | 其它函数 |
| 35 |   准确度    |       accuracy        | 其它函数 |
| 36 |    退出    |        dropout        | 其它函数 |
| 37 |    批量    |      batch_norm       | 其它函数 |
| 38 |   嵌入ID   |       embed_id        | 其它函数 |

附录一：上传项目到PyPI   
1、官网：https://pypi.org/   
2、E:\pyhton\python.exe -m pip install --upgrade pip setuptools wheel  
3、E:\pyhton\python.exe -m pip install twine   
4、python setup.py sdist   
5、E:\pyhton\python.exe -m twine upload dist/*   
完成2FA认证后，username是：__token__，password是：生成的token   
