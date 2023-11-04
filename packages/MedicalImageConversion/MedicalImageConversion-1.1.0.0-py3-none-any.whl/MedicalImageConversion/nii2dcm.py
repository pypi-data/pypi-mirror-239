import os
from pathlib import Path
import pydicom as pyd
import SimpleITK as sitk
import time
from typing import List


class Nii2Dicom:
    def __init__(self, input_path: str, out_dir: str):
        """
        This function is to convert multiple nifti files into dicom files
        Parameters
        ----------
        input_path: str
            path to source.
        out_dir: str
            path to where dicom will be saved.
        Returns
        -------
        None
        """
        if os.path.isdir(input_path):
            self._images_paths = list(map(lambda x: x.as_posix(), Path(input_path).rglob('*.nii.gz')))
        else:
            assert ".nii" in input_path[-7:]
            self._images_paths = list(input_path)
        self._out_dir = out_dir

    def __call__(self, *args, **kwargs):
        for image in self._images_paths:
            o_path = self._out_dir + '/' + os.path.basename(image)[:-7]
            os.makedirs(o_path, exist_ok=True)
            self._n2dconvertor(image, o_path)

    def _n2dconvertor(self, nifti_file_path: str, out_dir: str):
        """
        This function is to convert only one nifti file into dicom series
        Parameters
        ----------
        nifti_file_path: the path to the nifti file
        out_dir: the path to output
        Returns
        -------
        None
        """
        name = os.path.basename(nifti_file_path)[:-7]
        os.makedirs(out_dir, exist_ok=True)

        new_img = sitk.ReadImage(nifti_file_path)
        modification_time = time.strftime("%H%M%S")
        modification_date = time.strftime("%Y%m%d")
        study_uid = pyd.uid.generate_uid(None)
        series_uid = pyd.uid.generate_uid(None)
        direction = new_img.GetDirection()
        img_orientation = '\\'.join(map(str, (direction[0], direction[3], direction[6],
                                              direction[1], direction[4], direction[7])))
        series_tag_values = [
            ("0008|0031", modification_time),  # Series Time
            ("0008|0021", modification_date),  # Series Date
            ("0008|0023", modification_date),  # ContentDate
            ("0008|0033", modification_time),  # ContentTime
            ("0008|0020", modification_date),  # StudyDate
            ("0008|0030", modification_time),  # StudyTime
            ("0008|0022", modification_date),  # AcquisitionDate
            ("0008|0032", modification_time),  # AcquisitionTime
            ("0008|0012", modification_date),  # InstanceCreationDate
            ("0008|0013", modification_time),  # InstanceCreationTime
            ("0008|0008", "DERIVED\\SECONDARY"),  # Image Type
            ("0020|000d", study_uid),  # Study Instance UID
            ("0020|000e", series_uid),  # Series Instance UID
            ("0020|0037", img_orientation),  # Image Orientation (Patient)
            ("0008|0060", "CT"),  # set the type to CT
            ("0008|103e", f"{name}")  # Series Description
        ]
        # Write slices to output directory
        list(map(lambda i: self._createdcm(series_tag_values, new_img, i),
                 range(new_img.GetDepth())))

    def _createdcm(self, series_tag_values: list, new_img: sitk.Image, index: int):
        """
        Parameters
        ----------
        series_tag_values: List
            Tags created for dicom image
        new_img:
            simple Itk image
        index:
            index of slice

        Returns
        -------
        None
        """
        image_slice = new_img[:, :, index]
        writer = sitk.ImageFileWriter()
        writer.KeepOriginalImageUIDOn()

        # Tags shared by the series.
        list(map(
            lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

        # Slice specific tags.
        image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d"))  # Instance Creation Date
        image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S"))  # Instance Creation Time
        image_slice.SetMetaData("0008|0018", pyd.uid.generate_uid(None))
        image_slice.SetMetaData("0020|0032", '\\'.join(
            map(str, new_img.TransformIndexToPhysicalPoint((0, 0, index)))))  # Image Position (Patient)
        image_slice.SetMetaData("0020|0013", str(index))  # Instance Number

        # Write to the output directory and add the extension dcm, to force writing in DICOM format.
        writer.SetFileName(os.path.join(self._out_dir, 'slice' + str(index).zfill(4) + '.dcm'))
        writer.Execute(image_slice)
