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
class IP_Norm:
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
            1. Normalisation using simpleitk
         
        """
        self.image_in_name = image_in_name
        self.image_in_directory = image_in_directory        
        ########################################################################
        # Check if the file exists in the directory or not
        # Write_image
        image_out_name = self.image_in_name.removesuffix(".nii.gz") + "_Norm.nii.gz"
        
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
            
            # change pixel type to float 32
            pixel_type = image_in.GetPixelIDTypeAsString()
            if pixel_type != "32-bit float":
                image_in_f32 = sitk.Cast(image_in, sitk.sitkFloat32)
            else: 
                image_in_f32 = image_in
            
            # Normalisation    
            norm_filter = sitk.NormalizeImageFilter()
            norm_iamge = norm_filter.Execute(image_in_f32)
        
            
            # Write_image
            self.image_writer.SetFileName(self.image_in_directory + "/" + image_out_name)
            self.image_writer.Execute(norm_iamge)
            self.status = "A normalised version of the "+  self.image_in_name + " has been generated!"

        return self.status
    
