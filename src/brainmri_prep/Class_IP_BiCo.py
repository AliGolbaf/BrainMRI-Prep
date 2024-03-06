'''
    * Useful Clasess 
'''

################################################################################
# import usefull functions from main code
################################################################################
# import usefull libraries
import os
import SimpleITK as sitk

################################################################################   
class IP_BiCo:
    ############################################################################
    def __init__(self):
        self.status = ""
        ################################################################################
        # SimpleITK Functions
        # Image reader
        self.image_reader = sitk.ImageFileReader()
        # Image Writer
        self.image_writer = sitk.ImageFileWriter()
        # Show Images (Object oriented interface)
        self.image_viewer = sitk.ImageViewer()
        
    def bias_correction(self, image_in_name, image_in_directory):
        ########################################################################
        # Crop the images so that keeping the informative regions
        """
            1. N4 Bias Correction using simpleitk
         
        """
        self.image_in_name = image_in_name
        self.image_in_directory = image_in_directory        
        ########################################################################
        # Check if the file exists in the directory or not
        # Write_image
        image_out_name = self.image_in_name.removesuffix(".nii.gz") + "_BiCo.nii.gz"
        
        # File Existence check
        directory_files = os.listdir(self.image_in_directory)
        directory_files.sort()
        
        if image_out_name in directory_files:
            self.status = "There is already a bias-corrected version of the " +  self.image_in_name + " in the directory"
        else:
            
            # Import image
            # Set an image type for anytype we can use ""
            self.image_reader.SetImageIO("NiftiImageIO")
            self.image_reader.SetFileName(self.image_in_directory + "/" + self.image_in_name)
            image_in = self.image_reader.Execute()
            
            # Mask preparation (Optional)
            image = image_in # Just to be sure that nothing will apply to the original image
            otsu_filter = sitk.OtsuThresholdImageFilter()
            otsu_filter.SetInsideValue(0)
            otsu_filter.SetOutsideValue(1)
            mask = otsu_filter.Execute(image)
            thresh = otsu_filter.GetThreshold()
                
            # change pixel type to float 32
            pixel_type = image_in.GetPixelIDTypeAsString()
            if pixel_type != "32-bit float":
                image_in_f32 = sitk.Cast(image_in, sitk.sitkFloat32)
            else: 
                image_in_f32 = image_in
        
            # N4 Bias Correction
            n4_filter = sitk.N4BiasFieldCorrectionImageFilter()
            n4_image = n4_filter.Execute(image_in_f32, mask)
        
            
            # Write_image
            self.image_writer.SetFileName(self.image_in_directory + "/" + image_out_name)
            self.image_writer.Execute(n4_image)
            self.status = "A bias-corrected version of the "+  self.image_in_name + " has been generated!"

        return self.status
    
