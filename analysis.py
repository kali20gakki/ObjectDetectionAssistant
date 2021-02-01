import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import shapely.geometry as shgeo
import time

# 设置风格，尺度
sns.set_style('darkgrid')
sns.set_context('paper')

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号



def TuplePoly2Poly(poly):
    outpoly = [poly[0][0], poly[0][1],
               poly[1][0], poly[1][1],
               poly[2][0], poly[2][1],
               poly[3][0], poly[3][1]
               ]
    return outpoly


def get_data(label_dir, bbox_type="hbb"):
    """ 
    data_dict = 
    {
        '0'：{
            'area':[],
            'center':[],
            'ratio':[]
        }
    }
    """
    data_dict = {}
    assert Path(label_dir).is_dir(), "label_dir is not exist"

    txts = os.listdir(label_dir)

    for txt in txts:
        with open(os.path.join(label_dir, txt), 'r') as f:
            lines = f.readlines()

        for line in lines:
            temp = line.split()
            coor_list = list(map(lambda x: int(x), temp[1:]))
            if bbox_type == "hbb":
                # label 格式：class_num x1 y1 w h
                area = coor_list[2] * coor_list[3]
                center = (int(coor_list[0] + 0.5*coor_list[2]),
                          int(coor_list[1] + 0.5*coor_list[3]))
                ratio = round(coor_list[2] / coor_list[3], 2)

            elif bbox_type == "obb":
                # label 格式：class_num x1 y1 x2 y2 x3 y3 x4 y4
                ploy = [
                    (float(coor_list[0]), float(coor_list[1])),
                    (float(coor_list[2]), float(coor_list[3])),
                    (float(coor_list[4]), float(coor_list[5])),
                    (float(coor_list[6]), float(coor_list[7])),
                ]
                gtpoly = shgeo.Polygon(ploy)
                area = gtpoly.area
                ploy_list = list(map(int, TuplePoly2Poly(ploy)))
                xmin, ymin, xmax, ymax = min(ploy_list[0::2]), min(ploy_list[1::2]),\
                    max(ploy_list[0::2]), max(ploy_list[1::2])
                width, height = xmax - xmin, ymax - ymin
                center = [int(xmin + 0.5 * width), int(ymin + 0.5 * height)]
                ratio = round(width / height, 2)

            if temp[0] not in data_dict:
                data_dict[temp[0]] = {}
                data_dict[temp[0]]['area'] = []
                data_dict[temp[0]]['center'] = []
                data_dict[temp[0]]['ratio'] = []

            data_dict[temp[0]]['area'].append(area)
            data_dict[temp[0]]['center'].append(center)
            data_dict[temp[0]]['ratio'].append(ratio)

    return data_dict


def analysis_bbox(data, label_path, save_name):
    nums = len(data)
    fig, axes = plt.subplots(3, nums, figsize=(10*nums, 3*5))
    fig.suptitle("各类bbox统计图\n Label path : %s" % label_path,  fontsize=20)

    for i, class_num in enumerate(data):
        # area
        ax = sns.distplot(data[class_num]['area'],
                          norm_hist=False, kde=False, ax=axes[0][i])
        ax.set_title("class: %s" % class_num)
        ax.set_xlabel('area')
        ax.set_ylabel('times')

        area_arr = np.array(data[class_num]['area'])
        nums_str = "nums : %d" % len(area_arr)
        aver_str = "aver : %d" % np.mean(area_arr)
        medi_str = "medi : %d" % np.median(area_arr)
        mode_str = "mode : %d" % stats.mode(area_arr)[0][0]
        ax.text(0.7, 0.9, nums_str, transform=ax.transAxes, color='red')
        ax.text(0.7, 0.86, aver_str, transform=ax.transAxes, color='purple')
        ax.text(0.7, 0.82, medi_str, transform=ax.transAxes, color='blue')
        ax.text(0.7, 0.78, mode_str, transform=ax.transAxes, color='navy')
        if i == 0 :
            ax.text(-0.5,0.5, "bbox area\n   分布",  transform=ax.transAxes, fontsize=20, color='blue')        

        # ratio
        ax = sns.distplot(data[class_num]['ratio'],
                          norm_hist=False, kde=False, ax=axes[1][i])
        ax.set_title("class: %s" % class_num)
        ax.set_xlabel('ratio')
        ax.set_ylabel('times')

        ratio_arr = np.array(data[class_num]['ratio'])
        nums_str = "nums : %d" % len(ratio_arr)
        aver_str = "aver : %.2f" % np.mean(ratio_arr)
        medi_str = "medi : %.2f" % np.median(ratio_arr)
        mode_str = "mode : %.2f" % stats.mode(ratio_arr)[0][0]
        ax.text(0.7, 0.9, nums_str, transform=ax.transAxes, color='red')
        ax.text(0.7, 0.86, aver_str, transform=ax.transAxes, color='purple')
        ax.text(0.7, 0.82, medi_str, transform=ax.transAxes, color='blue')
        ax.text(0.7, 0.78, mode_str, transform=ax.transAxes, color='navy')
        if i == 0 :
            ax.text(-0.5,0.5, "bbox ratio\n   分布",  transform=ax.transAxes, fontsize=20, color='blue')

        # center
        a = np.array(data[class_num]['center'])
        #ax = sns.scatterplot(a[..., 0], a[..., 1], ax=axes[2][i], marker='D', s=30, edgecolors='red')
        ax = sns.kdeplot(a[..., 0], a[..., 1], ax=axes[2][i], shade=True, bw="silverman", cmap="mako")
        #ax = sns.kdeplot(a[..., 0], a[..., 1], ax=axes[2][i], fill=True, thresh=0.5, levels=100, cmap="mako")
        ax.set_title("class: %s" % class_num)
        if i == 0 :
            ax.text(-0.5,0.5, "bbox center\n   分布",  transform=ax.transAxes, fontsize=20, color='blue')

    plt.savefig(save_name,dpi=500,bbox_inches = 'tight')
    #plt.show()


def analysis_total(data, label_path, save_name):
    x = []
    y = []
    for class_num in data:
        x.append("class %s" % class_num)
        y.append(len(data[class_num]['area']))

    fig, axes = plt.subplots(1, 3, figsize=(40, 6))
    fig.suptitle("数据集总体分析\n Label path : %s" % label_path,  fontsize=10)
    ax = sns.barplot(x, y, ax=axes[0])
    ax.set_title("类别数量分布")
    ax.set_xlabel('类别')
    ax.set_ylabel('数量')
    for i, v in enumerate(y, start=0):
        ax.text(i, v, "%d(%.2f%%)" %
                (v, v/sum(y) * 100), ha="center", va="bottom")

    y = []
    for class_num in data:
        y.extend(data[class_num]['area'])

    ax = sns.distplot(y, norm_hist=False, kde=False, ax=axes[1])
    ax.set_title("anchor 面积分布")
    ax.set_xlabel('area')
    ax.set_ylabel('times')
    area_arr = np.array(y)
    nums_str = "nums : %d" % len(area_arr)
    aver_str = "aver : %.2f" % np.mean(area_arr)
    medi_str = "medi : %.2f" % np.median(area_arr)
    mode_str = "mode : %.2f" % stats.mode(area_arr)[0][0]
    max_str = "max  : %.2f" % np.max(area_arr)
    min_str = "min  : %.2f" % np.min(area_arr)
    ax.text(0.7, 0.9, nums_str, transform=ax.transAxes, color='red')
    ax.text(0.7, 0.86, aver_str, transform=ax.transAxes, color='purple')
    ax.text(0.7, 0.82, medi_str, transform=ax.transAxes, color='blue')
    ax.text(0.7, 0.78, mode_str, transform=ax.transAxes, color='navy')
    ax.text(0.7, 0.74, max_str, transform=ax.transAxes, color='coral')
    ax.text(0.7, 0.70, min_str, transform=ax.transAxes, color='cyan')

    y = []
    for class_num in data:
        y.extend(data[class_num]['ratio'])
    ax = sns.distplot(y, norm_hist=False, kde=False, ax=axes[2])
    ax.set_title("anchor ratio(W/H) 分布")
    ax.set_xlabel('ratio')
    ax.set_ylabel('times')
    area_arr = np.array(y)
    nums_str = "nums : %d" % len(area_arr)
    aver_str = "aver : %.2f" % np.mean(area_arr)
    medi_str = "medi : %.2f" % np.median(area_arr)
    mode_str = "mode : %.2f" % stats.mode(area_arr)[0][0]
    max_str = "max  : %.2f" % np.max(area_arr)
    min_str = "min  : %.2f" % np.min(area_arr)
    ax.text(0.7, 0.9, nums_str, transform=ax.transAxes, color='red')
    ax.text(0.7, 0.86, aver_str, transform=ax.transAxes, color='purple')
    ax.text(0.7, 0.82, medi_str, transform=ax.transAxes, color='blue')
    ax.text(0.7, 0.78, mode_str, transform=ax.transAxes, color='navy')
    ax.text(0.7, 0.74, max_str, transform=ax.transAxes, color='coral')
    ax.text(0.7, 0.70, min_str, transform=ax.transAxes, color='cyan')

    plt.savefig(save_name,dpi=500,bbox_inches = 'tight')
    #plt.show()


def analysis(label_dir, bbox_type="hbb", img_size=(640, 640)):
    data = get_data(label_dir, bbox_type)

    save_time = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
    analysis_bbox(data, label_dir, "bbox_"+ save_time + ".jpg")
    analysis_total(data, label_dir, "total_"+ save_time + ".jpg")
    plt.show()


if __name__ == "__main__":
    label_dir = r"C:\Users\zhangwei\Desktop\label"
    analysis(label_dir, "obb")
