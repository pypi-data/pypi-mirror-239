import napari
from napari_time_slicer import time_slicer
from magicgui import magic_factory
from napari_tools_menu import register_function, register_dock_widget
from apoc import ObjectMerger
from qtpy.QtWidgets import QTableWidget
import warnings
from ._utilities import wrap_api


@register_dock_widget(menu="Segmentation post-processing > Merge objects (APOC)")
@magic_factory(
    model_filename=dict(widget_type='FileEdit', mode='w'),
)
def _Train_object_merger(image: "napari.types.ImageData",
                        labels : "napari.types.LabelsData",
                        annotation : "napari.types.LabelsData",
                        model_filename : "magicgui.types.PathLike" = "LabelMerger.cl",
                        max_depth : int = 2,
                        num_ensembles : int = 100,
                        mean_touch_intensity: bool = True,
                        touch_portion: bool = True,
                        touch_count: bool = False,
                        centroid_distance: bool = False,
                        mean_intensity_difference: bool = False,
                        standard_deviation_intensity_difference: bool = False,
                        area_difference: bool = False,
                        mean_max_distance_to_centroid_ratio_difference: bool = False,
                        show_classifier_statistics=False,
                        viewer : "napari.Viewer" = None
                        ) -> "napari.types.LabelsData":
    return Train_object_merger(image, labels, annotation, model_filename, max_depth, num_ensembles,
                               mean_touch_intensity, touch_portion, touch_count, centroid_distance,
                               mean_intensity_difference, standard_deviation_intensity_difference,
                               area_difference, mean_max_distance_to_centroid_ratio_difference,
                               show_classifier_statistics, viewer)

def Train_object_merger(image: "napari.types.ImageData",
                         labels: "napari.types.LabelsData",
                         annotation: "napari.types.LabelsData",
                         model_filename: "magicgui.types.PathLike" = "LabelMerger.cl",
                         max_depth: int = 2,
                         num_ensembles: int = 100,
                         mean_touch_intensity: bool = True,
                         touch_portion: bool = True,
                         touch_count: bool = False,
                         centroid_distance: bool = False,
                         mean_intensity_difference: bool = False,
                         standard_deviation_intensity_difference: bool = False,
                         area_difference: bool = False,
                         mean_max_distance_to_centroid_ratio_difference: bool = False,
                         show_classifier_statistics=False,
                         viewer: "napari.Viewer" = None
                         ) -> "napari.types.LabelsData":

    features = ","
    if mean_touch_intensity:
        features = features + "mean_touch_intensity,"
    if touch_portion:
        features = features + "touch_portion,"
    if touch_count:
        features = features + "touch_count,"
    if centroid_distance:
        features = features + "centroid_distance,"
    if mean_intensity_difference:
        features = features + "mean_intensity_difference,"
    if standard_deviation_intensity_difference:
        features = features + "standard_deviation_intensity_difference,"
    if area_difference:
        features = features + "area_difference,"
    if mean_max_distance_to_centroid_ratio_difference:
        features = features + "mean_max_distance_to_centroid_ratio_difference,"

    # remove first and last comma
    features = features[1:-1]

    clf = ObjectMerger(opencl_filename=model_filename, num_ensembles=num_ensembles,
                                           max_depth=max_depth)

    clf.train(features, labels, annotation, image)
    result = clf.predict(labels, image)

    if viewer is not None:
        if show_classifier_statistics:
            from ._dock_widget import update_model_analysis
            table = QTableWidget()
            update_model_analysis(table, clf)
            viewer.window.add_dock_widget(table, name="Classifier statistics")


    return result


def Apply_object_merger(image: "napari.types.ImageData",
                        labels: "napari.types.LabelsData",
                        model_filename : str = "LabelMerger.cl") -> "napari.types.LabelsData":
    warnings.warn("Apply_object_merger is deprecated. Use apply_object_merger instead.", DeprecationWarning)
    return apply_object_merger(image, labels, model_filename)


@register_function(menu="Segmentation post-processing > Merge objects (apply pretrained, APOC)")
@time_slicer
@wrap_api
def apply_object_merger(image: "napari.types.ImageData",
                        labels: "napari.types.LabelsData",
                        model_filename : str = "LabelMerger.cl") -> "napari.types.LabelsData":

    clf = ObjectMerger(opencl_filename=model_filename)
    result = clf.predict(labels, image)
    return result
