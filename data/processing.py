from datasetinsights.datasets.unity_perception import AnnotationDefinitions, Captures
from datasetinsights.datasets.unity_perception.validation import DuplicateRecordError, NoRecordError
import os
import glob
import shutil

class PerceptionDatasetReader:
    ANNOTATIONS_NAME_COL = 'name'
    ANNOTATIONS_ID_COL = 'id'
    ANNOTATIONS_ENTRIES_COL = 'spec'
    ENTRY_LABEL_ID = 'label_id'
    ENTRY_LABEL_NAME = 'label_name'
    CAPTIONS_FILENAME = 'filename'

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.annotations_definitions = AnnotationDefinitions(dataset_dir)
        self.captures_data = Captures(dataset_dir)
        self.bounding_box_labels = None

    def load_bounding_box_labels(self):
        annotations_dataframe = self.annotations_definitions.table
        name_column = annotations_dataframe[PerceptionDatasetReader.ANNOTATIONS_NAME_COL]
        has_bounding_str = name_column.str.contains('bounding')
        has_box_str = name_column.str.contains('box')
        is_bounding_box = has_bounding_str & has_box_str
        selected_rows = annotations_dataframe[is_bounding_box]
        bounding_box_def_id_series = selected_rows[
            PerceptionDatasetReader.ANNOTATIONS_ID_COL
        ]
        if bounding_box_def_id_series.size == 0:
            raise NoRecordError(
                'Annotations file contains no bounding box definitions'
            )
        if bounding_box_def_id_series.size > 1:
            raise DuplicateRecordError(
                'More than one bounding box annotation definition was found'
            )
        bounding_box_def_id = bounding_box_def_id_series.item()
        definitions_dict = self.annotations_definitions.get_definition(bounding_box_def_id)
        self.bounding_box_labels = definitions_dict[
            PerceptionDatasetReader.ANNOTATIONS_ENTRIES_COL
        ]

    def get_bounding_box_labels(self):
        if not self.bounding_box_labels:
            self.load_bounding_box_labels()
        return self.bounding_box_labels

    def get_bounding_box_label_dict_map(self):
        labels = self.get_bounding_box_labels()
        result = {}
        for label in labels:
            name = label[PerceptionDatasetReader.ENTRY_LABEL_NAME]
            result[label[PerceptionDatasetReader.ENTRY_LABEL_ID]] = name
        return result

    def get_image_paths(self, limit=None):
        # arr[:None] returns arr
        relative_paths = self.captures_data.captures[
            [PerceptionDatasetReader.CAPTIONS_FILENAME]
        ]
        relative_paths = relative_paths.to_numpy().reshape(relative_paths.shape[0])
        abs_paths = [
            os.path.abspath(os.path.join(self.dataset_dir, p))
            for p in relative_paths
        ]
        return abs_paths[:limit]


class ProcessedDatasetWriter:
    def __init__(self, dest_dir, force_rewrite=True):
        self.dest_dir = dest_dir
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
            return glob.glob(os.path.join(self.dest_dir, '*.png'))
        else:
            return []
