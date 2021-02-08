import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox
import imageio
import cv2
import os
import random
import numpy as np
from pathlib import Path


def get_seq(flag_normal, flag_affine, flag_noise, flag_snow, flag_cloud, flag_fog, flag_snowflakes, flag_rain, flag_dropout):
    if flag_normal:
        seq_list = [
            iaa.SomeOf((1, 2), [
                iaa.LinearContrast((0.5, 2.0), per_channel=0.5),
                iaa.Grayscale(alpha=(0.0, 1.0)),
                iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),
            ]
            )
        ]
    else:
        seq_list = []

    if flag_affine:
        seq_list.append(
            iaa.Sometimes(
                0.7,
                iaa.Affine(
                    scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                    translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
                    rotate=(-25, 25),
                    shear=(-8, 8)
                )
            )
        )

    if flag_noise:
        seq_list.append(
            iaa.OneOf([
                iaa.GaussianBlur((0, 3.0)),
                iaa.AverageBlur(k=(2, 7)),
                iaa.MedianBlur(k=(3, 11)),
            ])
        )

    if flag_snow:
        seq_list.append(
            iaa.FastSnowyLandscape(
                lightness_threshold=(100, 255),
                lightness_multiplier=(1.0, 4.0)
            )
        )
    elif flag_cloud:
        seq_list.append(iaa.Clouds())
    elif flag_fog:
        seq_list.append(iaa.Fog())
    elif flag_snowflakes:
        seq_list.append(iaa.Snowflakes(
            flake_size=(0.2, 0.7), speed=(0.007, 0.03)))
    elif flag_rain:
        seq_list.append(iaa.Rain())

    if flag_dropout:
        seq_list.append(
            iaa.OneOf([
                iaa.Dropout((0.01, 0.1), per_channel=0.5),
                iaa.CoarseDropout(
                    (0.03, 0.15), size_percent=(0.02, 0.05),
                    per_channel=0.2
                ),
            ])
        )

    return iaa.Sequential(seq_list, random_order=True)


def augment_half(seq, images_dir, lables_dir, output_dir, start_num=1, bbox_type="obb"):
    assert Path(images_dir).is_dir(), "images_dir is not exist"
    assert Path(lables_dir).is_dir(), "lables_dir is not exist"
    assert Path(output_dir).is_dir(), "output_dir is not exist"

    #seq=get_seq(0, 0, 0, 0, 0, 0, 0, 1)

    end = os.listdir(images_dir)[0].split(".")[-1]
    txts_list = os.listdir(lables_dir)
    nums = int(len(txts_list) * 0.5)
    random.shuffle(txts_list)

    if bbox_type == "obb":
        for txt in txts_list[:nums]:
            print("process: ", txt)
            polygons_list = []
            with open(os.path.join(lables_dir, txt), 'r') as f:
                lines = f.readlines()

            # 读label
            for line in lines:
                label = line.split()[0]
                coors = np.array(
                    list(map(lambda x: int(x), line.split()[1:]))).reshape((4, 2))
                coor_list = [tuple(x) for x in coors]
                # polygons = ia.Polygon(coor_list, label=label)
                polygons_list.append(ia.Polygon(coor_list, label=label))

            # 读image
            img_path = os.path.join(images_dir, txt.split(".")[0] + "." + end)
            img = cv2.imread(img_path)
            image_aug, polygons_aug = seq(image=img, polygons=polygons_list)
            cv2.imwrite(os.path.join(output_dir, "images",
                                     str(start_num)+"."+end), image_aug)

            # save label
            with open(os.path.join(output_dir, "label", str(start_num)+".txt"), "w") as f:
                for x in polygons_aug:
                    wr_str = str(x.label) + " " + \
                        str(int(round(x[0][0]))) + " " + str(int(round(x[0][1]))) + " " + \
                        str(int(round(x[1][0]))) + " " + str(int(round(x[1][1]))) + " " + \
                        str(int(round(x[2][0]))) + " " + str(int(round(x[2][1]))) + " " + \
                        str(int(round(x[3][0]))) + " " + \
                        str(int(round(x[3][1]))) + "\n"
                    f.write(wr_str)

            start_num += 1

        return start_num

    elif bbox_type == "hbb":
        for txt in txts_list[:nums]:
            print("process: ", txt)
            bbox_list = []
            with open(os.path.join(lables_dir, txt), 'r') as f:
                lines = f.readlines()

            # 读label
            for line in lines:
                print(line)
                label = line.split()[0]
                coor = list(map(lambda x: int(x), line.split()[1:]))
                #coor_list = [tuple([coor[0], coor[1]]), tuple([coor[0]+coor[2], coor[1]+coor[3]])]
                bbox_list.append(BoundingBox(coor[0], coor[1], coor[0]+coor[2], coor[1]+coor[3], label))
            #print(bbox_list)

            # 读image
            img = cv2.imread(os.path.join(images_dir, txt.split(".")[0] + "." + end))
            image_aug, bbox_aug = seq(image=img, bounding_boxes=bbox_list)

            if not os.path.exists(os.path.join(output_dir, "images")):
                os.makedirs(os.path.join(output_dir, "images"))
            if not os.path.exists(os.path.join(output_dir, "labels")):
                os.makedirs(os.path.join(output_dir, "labels"))

            #  save image
            cv2.imwrite(os.path.join(output_dir, "images",str(start_num)+"."+end), image_aug)

            # save label
            with open(os.path.join(output_dir, "labels", str(start_num)+".txt"), "w") as f:
                print(bbox_aug[0])
                print(bbox_aug[0][0])
                print(bbox_aug[0][1])
                for x in bbox_aug:
                    wr_str = str(x.label) + " " + \
                             str(int(round(x[0][0]))) + " " + \
                             str(int(round(x[0][1]))) + " " + \
                             str(int(round(x[1][0] - x[0][0]))) + " " + \
                             str(int(round(x[1][1] - x[0][1]))) + "\n"
                    f.write(wr_str)
            
            start_num += 1
        return start_num



if __name__ == "__main__":
    seq = get_seq(0, 1, 0, 0, 0, 0, 0, 0, 0)
    augment_half(seq, r"C:\Users\zhangwei\Desktop\img",
                 r"C:\Users\zhangwei\Desktop\txt", r"C:\Users\zhangwei\Desktop\output", bbox_type="hbb")
