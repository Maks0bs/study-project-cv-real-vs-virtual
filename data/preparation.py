
from studienprojekt_cv_rvv.common.config import \
    RAW_DATASET_DEFINITIONS_DIRNAME as DEFINITIONS_DIRNAME, \
    RAW_DATASET_IMAGES_DIRNAME as IMAGES_DIRNAME
from studienprojekt_cv_rvv.common import config
import os
from studienprojekt_cv_rvv.data.processing import \
    PerceptionDatasetReader, ProcessedDatasetWriter
from sklearn.model_selection import train_test_split
from studienprojekt_cv_rvv.constants.paths import \
    PROCESSED_DATASET_TRAIN_DIRNAME as TRAIN_DIRNAME, \
    PROCESSED_DATASET_EVAL_DIRNAME as EVAL_DIRNAME
from studienprojekt_cv_rvv.constants.general import MODE_DEFAULT


def get_dataset_name():
    return config.get_reader().get_value(config.DATASET_NAME)


def get_raw_dataset_dir():
    raw_dir = config.get_reader().get_value(config.RAW_DATASETS_DIRECTORY)
    dataset_name = get_dataset_name()
    return os.path.join(raw_dir, dataset_name)


def get_annotations_dir():
    dataset_dir = get_raw_dataset_dir()
    definitions_dirname = config.get_reader().get_value(DEFINITIONS_DIRNAME)
    return os.path.join(dataset_dir, definitions_dirname)


def get_images_dir():
    dataset_dir = get_raw_dataset_dir()
    images_dirname = config.get_reader().get_value(IMAGES_DIRNAME)
    return os.path.join(dataset_dir, images_dirname)


def get_processed_dir():
    processed_datasets_dir = config.get_reader().get_value(config.PROCESSED_DATASETS_DIRECTORY)
    dataset_name = get_dataset_name()
    return os.path.join(processed_datasets_dir, dataset_name)


def get_train_data_dir():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, TRAIN_DIRNAME)


def get_eval_data_dir():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, EVAL_DIRNAME)


# options:
#   mode (verbose, silent)
#   train/eval split
def generate_processed_dataset(split_ratio=0.2, mode=MODE_DEFAULT):
    raw_dataset_reader = PerceptionDatasetReader(get_raw_dataset_dir())
    label_dict_map = raw_dataset_reader.get_bounding_box_label_dict_map()
    image_paths = raw_dataset_reader.get_image_paths()
    images_train, images_eval = train_test_split(image_paths, test_size=split_ratio)

    train_writer = ProcessedDatasetWriter(get_train_data_dir())
    train_writer.clean_processed_data()
    train_writer.copy_to_destination(images_train)
    images_train = train_writer.get_processed_files()

    eval_writer = ProcessedDatasetWriter(get_eval_data_dir())
    eval_writer.clean_processed_data()
    eval_writer.copy_to_destination(images_eval)
    images_eval = eval_writer.get_processed_files()

    return label_dict_map, images_train, images_eval


def execute():
    #TODO: pass args here
    label_dict_map, images_train, images_eval = generate_processed_dataset()
    #TODO generate tf records here


if __name__ == '__main__':
    execute()