# -*- coding = utf-8 -*-
import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算

# 准备词云所需的文字（词）
# 创建一个空列表用于存储每行的文本内容
data = []

# 打开文本文件
with open("概况.txt", mode="r", encoding="utf-8") as file:
    # 逐行读取文件内容
    for line in file.readlines():
        # 将每行的内容添加到列表中
        data.append(line.strip())  # strip()函数用于移除每行末尾的换行符

text = ""
for item in data:
    text = text + item

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)

img = Image.open(r".\tree.jpg")  # 打开遮罩图片
img_array = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color="white",
    mask=img_array,
    font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis("off")  # 是否显示坐标轴

plt.show()  # 显示生成的词云图片

# 输出词云图片到文件
# plt.savefig(r".\word.jpg", dpi=500)
