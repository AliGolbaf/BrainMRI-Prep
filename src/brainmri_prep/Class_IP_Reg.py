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
class IP_Reg:
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
                
    def registration(self, image_fixed_directory, image_fixed_name, image_moving_directory, image_moving_name, registration_type):
        ########################################################################
        """
            * Here SimpleElastic is used to register MRI images
        """
        self.image_fixed_directory = image_fixed_directory
        self.image_fixed_name = image_fixed_name
        self.image_moving_directory = image_moving_directory
        self.image_moving_name = image_moving_name
        
        self.registration_type = registration_type
        
        ########################################################################
        # Check if the file exists in the directory or not
        if self.registration_type == "Rigid Registration":
            name_0 = "Rigid"
            
        if self.registration_type == "Affine Registration":
            name_0 = "Affine"
        
        if self.registration_type == "Non-rigid Registration":
            name_0 = "NonRigid"
            
        image_out_name = self.image_moving_name.removesuffix(".nii.gz") + "_Reg("+ str(name_0) +").nii.gz"
        
        # File Existence check
        directory_files = os.listdir(self.image_moving_directory)
        directory_files.sort()
        
        if image_out_name in directory_files:
            self.status = "There is already a registered version of the " +  self.image_moving_name + " in the directory"
        else:
            
            # Import images
            # Set an image type for anytype we can use ""
            self.image_reader.SetImageIO("NiftiImageIO")
            self.image_reader.SetFileName(self.image_fixed_directory + "/" + self.image_fixed_name)
            image_fixed =  self.image_reader.Execute()
            
            # Set an image type for anytype we can use ""
            self.image_reader.SetImageIO("NiftiImageIO")
            self.image_reader.SetFileName(self.image_moving_directory + "/" + self.image_moving_name)
            image_moving =  self.image_reader.Execute()
            
            # Registration
            elastixImageFilter = sitk.ElastixImageFilter()
            elastixImageFilter.SetFixedImage(image_fixed)
            elastixImageFilter.SetMovingImage(image_moving)
            
            ["Rigid Registration", "Affine Registration", "Non-rigid Registration"]
            
            if self.registration_type == "Rigid Registration":
                name_0 = "Rigid"
                elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
                
            if self.registration_type == "Affine Registration":
                name_0 = "Affine"
                elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("affine"))  
            
            if self.registration_type == "Non-rigid Registration":
                name_0 = "NonRigid"
                parameterMapVector = sitk.VectorOfParameterMap()
                parameterMapVector.append(sitk.GetDefaultParameterMap("affine"))
                parameterMapVector.append(sitk.GetDefaultParameterMap("bspline"))
                elastixImageFilter.SetParameterMap(parameterMapVector)
                
            elastixImageFilter.Execute()
            image_out = elastixImageFilter.GetResultImage()
            
            # Write_image
            self.image_writer.SetFileName(self.image_moving_directory + "/" + image_out_name)
            self.image_writer.Execute(image_out)
            
            self.status = "Registered version of the "+  self.image_moving_name + " has been generated!"

        return self.status
    