import os
import glob
import shutil
import pandas as pd
import cv2
from sys import maxsize as INT_MAX

from studienprojekt_cv_rvv.data.tf_records import TFRecordsGenerator

class DataframeColumns:
    FILENAME = 'filename'
    CLASS_ID = 'class_id'
    SPECIES_ID = 'species_id'
    BREED_ID = 'breed_id'
    CLASS_LABEL = 'class_label'
    SPECIES_LABEL = 'species_label'
    BREED_LABEL = 'breed_label'
    OBJECT_X = 'x'
    OBJECT_Y = 'y'
    OBJECT_W = 'w'
    OBJECT_H = 'h'
class OxfordRawDatasetClassDataReader:
    def __init__(self, list_path) -> None:
        self.list_path = list_path
        
    def read_as_df(self):
        data = pd.read_csv(self.list_path, sep=' ', header=None, comment='#', names=[DataframeColumns.FILENAME, DataframeColumns.CLASS_ID, DataframeColumns.SPECIES_ID, DataframeColumns.BREED_ID])
        data[DataframeColumns.CLASS_LABEL] = data[DataframeColumns.FILENAME].str.split('_').apply(lambda x: x[:-1]).str.join('_')
        data[DataframeColumns.BREED_LABEL] = data[DataframeColumns.CLASS_LABEL]
        data[DataframeColumns.SPECIES_LABEL] = data[DataframeColumns.SPECIES_ID].apply(lambda x: 'cat' if x == 1 else 'dog')
        return data
        

class OxfordRawDatasetObjectDetectionReader:
    def __init__(self, images_dir, annotations_dir, class_df, images_ext = 'jpg', annotations_ext = 'png'):
        self.annotations_dir = annotations_dir
        self.images_dir = images_dir
        self.class_df = class_df
        self.annotations_ext = annotations_ext
        self.images_ext = images_ext
        self.objects_df = self.load_objects_df()


    def load_objects_df(self):
        
        result_rows = []
        for _, row in self.class_df.iterrows():
            img_path = os.path.join(self.annotations_dir, row[DataframeColumns.FILENAME] + '.' + self.annotations_ext)
            # load image
            image_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            im_bw = cv2.threshold(image_gray, 1, 255, cv2.THRESH_BINARY)[1]
            im_bw = 255 - im_bw
            
            minX = minY = INT_MAX
            maxX = maxY = -INT_MAX
            contours, _ = cv2.findContours(im_bw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2:]
            for countour in contours:
                x, y, w, h = cv2.boundingRect(countour)
                x1, y1, x2, y2 = x, y, x + w, y + h
                minX = min(minX, x1, x2)
                maxX = max(maxX, x1, x2)
                minY = min(minY, y1, y2)
                maxY = max(maxY, y1, y2)
                
            filename = row[DataframeColumns.FILENAME]
            result_rows.append([filename, minX, minY, maxX - minX, maxY - minY])
            
            
        return pd.DataFrame(result_rows, columns=[DataframeColumns.FILENAME, DataframeColumns.OBJECT_X, DataframeColumns.OBJECT_Y, DataframeColumns.OBJECT_W, DataframeColumns.OBJECT_H])

    def get_bounding_box_labels(self):
        return self.class_df[[DataframeColumns.CLASS_ID, DataframeColumns.CLASS_LABEL]].drop_duplicates().reset_index()

    def get_image_paths(self, abs_path=False, limit=None):
        images = list(self.class_df[DataframeColumns.FILENAME].apply(lambda f: f + '.' + self.images_ext))
        if abs_path:
            images = [os.path.join(self.images_dir, i) for i in images]
        return images[:limit]

    def get_objects_bounding_boxes(self, filename):
        df = self.objects_df[self.objects_df[DataframeColumns.FILENAME] == filename].merge(self.class_df, on=DataframeColumns.FILENAME)
        df = df[[DataframeColumns.CLASS_ID, DataframeColumns.CLASS_LABEL, DataframeColumns.OBJECT_X, DataframeColumns.OBJECT_Y, DataframeColumns.OBJECT_W, DataframeColumns.OBJECT_H]]
        df = df.rename(columns={
            DataframeColumns.CLASS_ID: TFRecordsGenerator.IMAGE_OBJ_LABEL_ID,
            DataframeColumns.OBJECT_X: TFRecordsGenerator.IMAGE_OBJ_X,
            DataframeColumns.OBJECT_Y: TFRecordsGenerator.IMAGE_OBJ_Y,
            DataframeColumns.OBJECT_W: TFRecordsGenerator.IMAGE_OBJ_WIDTH,
            DataframeColumns.OBJECT_H: TFRecordsGenerator.IMAGE_OBJ_HEIGHT,
            DataframeColumns.CLASS_LABEL: TFRecordsGenerator.IMAGE_OBJ_LABEL_NAME
        })
        return df.to_dict(orient='records')


class ProcessedDatasetWriter:
    def __init__(self, dest_dir, images_ext='jpg', force_rewrite=True):
        self.dest_dir = dest_dir
        self.images_ext = images_ext
        self.force_rewrite = force_rewrite
        if not os.path.isdir(self.dest_dir):
            os.makedirs(self.dest_dir)

    def clean_processed_data(self):
        images_paths = self.get_processed_files()
        for f in images_paths:
            os.remove(f)

    def copy_to_destination(self, images_paths):
        for f in images_paths:
            basename = os.path.basename(f)
            copied_file_path = os.path.abspath(os.path.join(self.dest_dir, basename))
            if os.path.isfile(copied_file_path):
                if self.force_rewrite:
                    os.remove(copied_file_path)
                    shutil.copy(f, self.dest_dir)
                else:
                    shutil.copy(f, os.path.join(self.dest_dir, 'copy_' + basename))
            else:
                shutil.copy(f, self.dest_dir)

    def get_processed_files(self):
        if os.path.isdir(self.dest_dir):
            return glob.glob(os.path.join(self.dest_dir, '*.' + self.images_ext))
        else:
            return []


def write_label_map(raw_reader: OxfordRawDatasetObjectDetectionReader, output_file: str) -> bool:
    df = raw_reader.get_bounding_box_labels()
    try:
        with open(output_file, 'w+') as file:
            for _, row in df.iterrows():
                file.writelines([
                    "item {\n",
                    f"\tname:'{row[DataframeColumns.CLASS_LABEL]}'\n",
                    f"\tid:{row[DataframeColumns.CLASS_ID]}\n"
                    "}\n"
                ])
    except (IOError, OSError, FileNotFoundError):
        return False
    else:
        return True
