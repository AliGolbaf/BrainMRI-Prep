'''
    * Useful Clasess 
'''

################################################################################
# import usefull functions from main code
################################################################################
# import usefull libraries
import os
import SimpleITK as sitk
import numpy as np

################################################################################   
class IP_Seg:
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
    
    def docker_ams_segmentation(self,image_in_name,image_in_directory, mode):
        
        self.image_in_name      = image_in_name
        self.image_in_directory = image_in_directory
        self.mode = mode
        
        if self.mode == "Select the Segmentation Method":
            self.status = "Please select the segmentation method"

        else:
            comm_01 = "docker run --rm -v "  + self.image_in_directory + ":/data --user 1000:1000 neuronets/ams:latest-"
            
            if self.mode == "Cpu-Based":
                comm_02 = "cpu "
            else: 
                comm_02 = "gpu " 
               
            comm_03 = self.image_in_name + " "
            comm_04 = self.image_in_name.removesuffix(".nii.gz") + "_Segmented"
            
            comm = comm_01 + comm_02 + comm_03 + comm_04
            
            # File Existence check
            check_file_name_in_directory_01 = comm_04 + ".nii.gz"
            
            directory_files = os.listdir(self.image_in_directory)
            directory_files.sort()
            
            if check_file_name_in_directory_01 in directory_files:
                self.status = "There is already a segmented version of the " + self.image_in_name + " in the directory!"
            else:
                os.system(comm)
                # Update Directory
                directory_files = os.listdir(self.image_in_directory)
                directory_files.sort()
                    
                if check_file_name_in_directory_01 in directory_files:
                    self.status = "The " + self.image_in_name + " has been segmented!"
                else:
                    self.status = "Neuronets/ams was unable to segment the " + self.image_in_name
            
            return self.status
                   
    def segmentation_correction(self, image_in_name, image_in_directory, num_of_tumours, hole_filling):
        
        self.image_in_name =image_in_name
        self.image_in_directory = image_in_directory
        self.num_of_tumours = num_of_tumours
        self.hole_filling = hole_filling
        # Import image
        # Set an image type for anytype we can use ""

        ########################################################################
        # Check if the file exists in the directory or not
        # Write_image
        image_out_name = self.image_in_name.removesuffix(".nii.gz") + "_Modified_L" + str(self.num_of_tumours) + ".nii.gz"
        
        # File Existence check
        directory_files = os.listdir(self.image_in_directory)
        directory_files.sort()
        
        if image_out_name in directory_files:
            self.status = "There is already a modefied version of the " +  self.image_in_name + " in the directory!"
        else:
            
            # Import image
            # Set an image type for anytype we can use ""
            self.image_reader.SetImageIO("NiftiImageIO")
            self.image_reader.SetFileName(self.image_in_directory + "/" + self.image_in_name)
            image_in = self.image_reader.Execute()
        
            # Check if the imported image is a label
            values, counts = np.unique(sitk.GetArrayFromImage(image_in), return_counts=True)
            
            if len(values) !=2:
                self.status = "The " +  self.image_in_name + " is not a label!"
                
            else:
                # A copy of image for being processed
                image_for_process = image_in
                
                # Find the largerst label
                image_out = self.select_largest_connected_components(image_for_process, self.num_of_tumours )
            
                # Hole filling
                if self.hole_filling == True:
                    image_out = self.hole_filling_func(image_out)
            
                # Write_image
                self.image_writer.SetFileName(self.image_in_directory + "/" + image_out_name)
                exec("self.image_writer.Execute(image_out)")
                self.status = "A modified version of "+  self.image_in_name + " has been generated!"

        return self.status
    
    # Functions
    ############################################################################
    def subtract(self,image_in,label_in):
        
        self.image_in = image_in
        self.label_in = label_in
        
        image_in_arr = sitk.GetArrayFromImage(self.image_in)
        label_in_arr = sitk.GetArrayFromImage(self.label_in)
        
        image_in_arr[label_in_arr == 0] = 0.0
        
        # Converting back to SimpleITK (assumes we didn't move the image in space as we copy the information from the original)
        image_out = sitk.GetImageFromArray(image_in_arr)
        image_out.CopyInformation(self.image_in)
        return image_out
    
        # Only Binaries
    def select_largest_connected_components(self,image_in, number_of_components):
        self.image_in = image_in
        self.number_of_components = number_of_components
        
        # Find the largerst labels and sort them based on theier size
        Connected_Componnets = sitk.ConnectedComponent(self.image_in)
        Connected_Componnets_sorted = sitk.RelabelComponent(Connected_Componnets, sortByObjectSize=True)
        
        # Select the largest labeles based on their sizes  
        it_lines = ""
        for i in range (1,self.number_of_components+1):
            exec("image_out_" + str(i) + "= Connected_Componnets_sorted ==" + str(i))
            it_lines += "image_out_" + str(i) + "+"
        
        image_out = eval(it_lines[:len(it_lines)-1])
        
        return image_out
        
   
    # Only Binaries
    def hole_filling_func(self, label_in): 
        # from scipy import ndimage
        self.label_in = label_in
        hole_filling_filter = sitk.BinaryFillholeImageFilter()
        label_out = hole_filling_filter.Execute(self.label_in)
        return label_out
    
    
    