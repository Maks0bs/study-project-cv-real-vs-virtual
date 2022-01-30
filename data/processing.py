from datasetinsights.datasets.unity_perception import AnnotationDefinitions, Captures
from datasetinsights.datasets.unity_perception.validation import DuplicateRecordError, NoRecordError
import os
import glob
import shutil


class PerceptionDatasetReader:
    ANNOTATIONS_DEFS_NAME_COL = 'name'
    ANNOTATIONS_DEFS_ID_COL = 'id'
    ANNOTATIONS_DEFS_ENTRIES_COL = 'spec'
    ENTRY_LABEL_ID = 'label_id'
    ENTRY_LABEL_NAME = 'label_name'
    CAPTURES_FILENAME = 'filename'
    CAPTURES_ID = 'id'
    ANNOTATIONS_ANN_DEF_COL = 'annotation_definition'
    ANNOTATIONS_VALUES_COL = 'values'
    ANNOTATIONS_CAPTURE_ID_COL = 'capture.id'

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.annotations_definitions = AnnotationDefinitions(dataset_dir).table
        captures_data = Captures(dataset_dir)
        self.captures = captures_data.captures
        self.annotations = captures_data.annotations
        self.bounding_box_labels = None
        self.bounding_box_annotation_id = None
        self.load_bounding_box_info()
        self.filename_to_objects_map = {}
        self.images_subdir = None
        self.load_images_objects_bounding_boxes()

    # loads bb labels and its annotation id
    def load_bounding_box_info(self, annotations_definitions=None):
        if not annotations_definitions:
            annotations_definitions = self.annotations_definitions
        name_column = annotations_definitions[
            PerceptionDatasetReader.ANNOTATIONS_DEFS_NAME_COL
        ]
        has_bounding_str = name_column.str.contains('bounding')
        has_box_str = name_column.str.contains('box')
        is_bounding_box = has_bounding_str & has_box_str
        selected_rows = annotations_definitions[is_bounding_box]

        if selected_rows.shape[0] == 0:
            raise NoRecordError(
                'Annotations file contains no bounding box definitions'
            )
        if selected_rows.shape[0] > 1:
            raise DuplicateRecordError(
                'More than one bounding box annotation definition was found'
            )

        columns = [
            PerceptionDatasetReader.ANNOTATIONS_DEFS_ENTRIES_COL,
            PerceptionDatasetReader.ANNOTATIONS_DEFS_ID_COL
        ]
        filtered_row_values = selected_rows[columns].values
        filtered_row_values = filtered_row_values.reshape(filtered_row_values.shape[1])
        self.bounding_box_labels = filtered_row_values[0]
        self.bounding_box_annotation_id = filtered_row_values[1]

    def load_images_objects_bounding_boxes(
            self,
            annotations=None,
            annotation_def=None,
            captures=None
    ):
        if not annotations:
            annotations = self.annotations
        if not annotation_def:
            annotation_def = self.bounding_box_annotation_id
        if not captures:
            captures = self.captures

        annotation_ids = annotations[PerceptionDatasetReader.ANNOTATIONS_ANN_DEF_COL]
        bounding_box_annotations = annotation_ids == annotation_def
        columns = [
            PerceptionDatasetReader.ANNOTATIONS_CAPTURE_ID_COL,
            PerceptionDatasetReader.ANNOTATIONS_VALUES_COL
        ]
        selected_rows = annotations[bounding_box_annotations][columns]
        joined_annotations = selected_rows.merge(
            captures,
            left_on=PerceptionDatasetReader.ANNOTATIONS_CAPTURE_ID_COL,
            right_on=PerceptionDatasetReader.CAPTURES_ID
        )
        columns = [
            PerceptionDatasetReader.CAPTURES_FILENAME,
            PerceptionDatasetReader.ANNOTATIONS_VALUES_COL
        ]
        filtered_annotations = joined_annotations[columns]
        self.filename_to_objects_map = {}
        path = filtered_annotations.values[0][0]
        self.images_subdir, _ = os.path.split(path)
        for i, row in filtered_annotations.iterrows():
            filename = os.path.basename(row[PerceptionDatasetReader.CAPTURES_FILENAME])
            annotations = row[PerceptionDatasetReader.ANNOTATIONS_VALUES_COL]
            self.filename_to_objects_map[filename] = annotations

    def get_bounding_box_labels(self):
        return self.bounding_box_labels

    def get_bounding_box_label_dict_map(self):
        labels = self.bounding_box_labels
        result = {}
        for label in labels:
            name = label[PerceptionDatasetReader.ENTRY_LABEL_NAME]
            key = label[PerceptionDatasetReader.ENTRY_LABEL_ID]
            result[key] = name
        return result

    def get_image_paths(self, abs_path=False, limit=None):
        # arr[:None] returns arr
        images = list(self.filename_to_objects_map.keys())
        if abs_path:
            images = [
                os.path.join(self.dataset_dir, self.images_subdir, i)
                for i in images
            ]

        return images[:limit]

    def get_objects_bounding_boxes(self, filename):
        return self.filename_to_objects_map[filename]


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


def write_label_map(raw_reader: PerceptionDatasetReader, output_file: str) -> bool:
    labels = raw_reader.get_bounding_box_labels()
    try:
        with open(output_file, 'w+') as file:
            for label in labels:
                file.writelines([
                    "item {\n",
                    f"\tname:'{label[PerceptionDatasetReader.ENTRY_LABEL_NAME]}'\n",
                    f"\tid:{label[PerceptionDatasetReader.ENTRY_LABEL_ID]}\n"
                    "}\n"
                ])
    except (IOError, OSError, FileNotFoundError):
        return False
    else:
        return True
