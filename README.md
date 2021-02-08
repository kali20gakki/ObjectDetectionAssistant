# ObjectDetectionAssistant
 
分析数据集各类数量分布，BBox大小分布， BBox比率分布， BBox中心点分布；数据增强, 支持正框（HBB）和倾斜框（OBB）。

!["Pyqt界面"](./AnalysisResults/1.png)

### ✨ 特性
- 只需要选择label文件夹就能开始自动分析数据集类别，边界框的特点，自动生成可视化图，如下：
![bbox](./AnalysisResults/bbox_2021-02-08_20-16-17.jpg)
![total](./AnalysisResults/total_2021-02-08_20-16-17.jpg)
- 支持多种图像数据增强，同时生成增强后的图片和标注文件（txt）


    
### 📜说明
- 数据集格式：图片和label分别放在两个文件夹，标注文件为txt, 每张图片和label.txt的文件名必须一一对应
- 正框（HBB）标注格式： class x1 y1 w h
- 斜框（OBB）标注格式：class x1 y1 x2 y2 x3 y3 x4 y4


### ⚡ 环境依赖

- seaborn==0.9.0
- numpy==1.16.4
- scipy==1.2.1
- Shapely==1.7.1
- imgaug==0.4.0
- matplotlib==3.1.0
- imageio==2.9.0
- PyQt5==5.15.2


### ⌛️ 食用方法

- 克隆仓库
```ssh
git clone https://github.com/kali20gakki/ObjectDetectionAssistant.git
```

- 安装依赖
```ssh
pip install -r requirements
```

- 运行
```ssh
python run.py
```