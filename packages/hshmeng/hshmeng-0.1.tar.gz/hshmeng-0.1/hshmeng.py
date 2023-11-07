# coding: utf-8
# -*- coding: utf-8 -*-
import sys



功能 = [
    '''
    print = 输出
    input = 输入
    help = 帮助
    type = 属性
    ''',
    '''
    values = "值"
    sep = "分隔符"
    end = "结束"
    file = "文件"
    flush = "刷新"
    '''
]

def 帮助(页码=None):
    整数(页码)
    if 页码 == None:
        print('''
        更新于2023年11月6日
        作者：hshmeng
        功能：将python原本的英文关键字替换成中文，英文字符还是要用的
        用法：我也不知道，慢慢研究吧（输入：帮助(页码)）
        邮箱：hshmeng@foxmail.com   代码有问题记得发邮箱哦~
        特别：有小彩蛋哦~    
        ''')
    Exception



def 属性(ttyyppee):
    print(type(ttyyppee))

values = "值"
sep = "分隔符"
end = "结束"
file = "文件"
flush = "刷新"

def 输出(值, 分隔符=None, 结束=None, 文件=None, 刷新=None):
    if 分隔符 is not None:
        separator = 分隔符
    else:
        separator = ''

    if 结束 is not None:
        ending = 结束
    else:
        ending = '\n'

    if 文件 is not None:
        output_file = 文件
    else:
        output_file = sys.stdout

    if 刷新 is not None:
        do_flush = 刷新
    else:
        do_flush = False

    output = separator.join(str(value) for value in 值) + ending
    output_file.write(output)

    if do_flush:
        output_file.flush()
    pass




def 输入(prompt):
    return input(prompt)
    pass

def 导入(模块名):
    return __import__(模块名)

def 导(模块名):
    return __import__(模块名)

