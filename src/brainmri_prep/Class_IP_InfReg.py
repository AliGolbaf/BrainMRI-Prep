"""
    1. Extract informative regions
 * Steps:
     1. Make an 3D Array of the imported image
     2. Specify a threshold equal to the average of the data
     3. Make a binary image by assigning 0 and 1 to the arrays lower and higher than the average
     4. Connectivity check and drop unconnected regions. (this is applied only on the label image and do not have any effects
                                                          on the original image as here we want only to extratc a range of 
                                                          informative region and this range finaly is subtracted from the original image)
     To do this we detec connected componnents via ITK tool then specify the largest connected componnednt as our desiered componnent.
"""
################################################################################
# import usefull functions from main code
################################################################################
# import usefull libraries
import os
import SimpleITK as sitk
import numpy as np

################################################################################   
class IP_InfReg:
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
    
    ############################################################################
    def informative_region(self, image_in_name, image_in_directory, state_null_slices):
        ########################################################################
        # Crop the images so that keeping the informative regions
        
        self.image_in_name = image_in_name
        self.image_in_directory = image_in_directory
        self.state_null_slices = state_null_slices
        
        ########################################################################
        # Check if the file exists in the directory or not
        # Write_image
        image_out_name = self.image_in_name.removesuffix(".nii.gz") + "_Informative.nii.gz"
        
        # File Existence check
        directory_files = os.listdir(self.image_in_directory)
        directory_files.sort()
        
        if image_out_name in directory_files:
            self.status = "There is already an infromative version of the " +  self.image_in_name + " in the directory"
            
        else:
            
            # Import image
            # Set an image type for anytype we can use ""
            self.image_reader.SetImageIO("NiftiImageIO")
            self.image_reader.SetFileName(self.image_in_directory + "/" + self.image_in_name)
            image_in = self.image_reader.Execute()
        
            # A copy of image for being processed
            image_for_process = image_in
        
            # Statistical filter/ get Mean
            statistics_filter = sitk.StatisticsImageFilter()
            statistics_filter.Execute(image_for_process)
            mean_tresh = statistics_filter.GetMean()
        
            # sitk basic thresholding
            image_in_thresh = image_for_process > mean_tresh  
            
            # Extract the largest component           
            largest_component = self.select_largest_connected_components(image_in_thresh, number_of_components = 1)
                
            # Subtract
            image_out = self.subtract(image_in, largest_component)
            
            ####################################################################
            if self.state_null_slices == True:
                # Crop
                # Get image array
                largest_component_image_arr = sitk.GetArrayFromImage(largest_component)
            
                x_slices = []
                y_slices = []
                z_slices = []
                
                for i in range (largest_component_image_arr.shape[0]):
                    if  np.sum(largest_component_image_arr[i,:,:]) > 0:
                        x_slices.append(i)
                
                for i in range (largest_component_image_arr.shape[1]):
                    if  np.sum(largest_component_image_arr[:,i,:]) > 0:
                        y_slices.append(i)

                for i in range (largest_component_image_arr.shape[2]):
                    if  np.sum(largest_component_image_arr[:,:,i]) > 0:
                        z_slices.append(i)

                x_crop_bounds = [x_slices[0], x_slices[len(x_slices)-1]]
                y_crop_bounds = [y_slices[0], y_slices[len(y_slices)-1]]
                z_crop_bounds = [z_slices[0], z_slices[len(z_slices)-1]]

                # Crop that do not contain binaries from image_in
                # Note: (x,y,z) > (z,y,x)
                image_out = image_in[z_crop_bounds[0]: z_crop_bounds[1], y_crop_bounds[0]: y_crop_bounds[1], x_crop_bounds[0]: x_crop_bounds[1]]
                
            # Write_image
            self.image_writer.SetFileName(self.image_in_directory + "/" + image_out_name)
            self.image_writer.Execute(image_out)
            
            self.status = "Informative version of the "+  self.image_in_name + " has been generated!"

        return self.status

    ############################################################################
    def informative_region_for_showing_size(self, image_in_name, image_in_directory, state_null_slices):
        ########################################################################
        # Crop the images so that keeping the informative regions
        
        self.image_in_name = image_in_name
        self.image_in_directory = image_in_directory
        self.state_null_slices = state_null_slices
        
        ########################################################################
        # Check if the file exists in the directory or not
        # Write_image
        image_out_name = self.image_in_name.removesuffix(".nii.gz") + "_Informative.nii.gz"
        
        # File Existence check
        directory_files = os.listdir(self.image_in_directory)
        directory_files.sort()
        
        if 1<0:
            pass
            
        else:
            
            # Import image
            # Set an image type for anytype we can use ""
            self.image_reader.SetImageIO("NiftiImageIO")
            self.image_reader.SetFileName(self.image_in_directory + "/" + self.image_in_name)
            image_in = self.image_reader.Execute()
        
            # A copy of image for being processed
            image_for_process = image_in
        
            # Statistical filter/ get Mean
            statistics_filter = sitk.StatisticsImageFilter()
            statistics_filter.Execute(image_for_process)
            mean_tresh = statistics_filter.GetMean()
        
            # sitk basic thresholding
            image_in_thresh = image_for_process > mean_tresh  
            
            # Extract the largest component           
            largest_component = self.select_largest_connected_components(image_in_thresh, number_of_components = 1)
                
            # Subtract
            image_out = self.subtract(image_in, largest_component)
            
            ####################################################################
            if self.state_null_slices == True:
                # Crop
                # Get image array
                largest_component_image_arr = sitk.GetArrayFromImage(largest_component)
            
                x_slices = []
                y_slices = []
                z_slices = []
                
                for i in range (largest_component_image_arr.shape[0]):
                    if  np.sum(largest_component_image_arr[i,:,:]) > 0:
                        x_slices.append(i)
                
                for i in range (largest_component_image_arr.shape[1]):
                    if  np.sum(largest_component_image_arr[:,i,:]) > 0:
                        y_slices.append(i)

                for i in range (largest_component_image_arr.shape[2]):
                    if  np.sum(largest_component_image_arr[:,:,i]) > 0:
                        z_slices.append(i)

                x_crop_bounds = [x_slices[0], x_slices[len(x_slices)-1]]
                y_crop_bounds = [y_slices[0], y_slices[len(y_slices)-1]]
                z_crop_bounds = [z_slices[0], z_slices[len(z_slices)-1]]

                # Crop that do not contain binaries from image_in
                # Note: (x,y,z) > (z,y,x)
                image_out = image_in[z_crop_bounds[0]: z_crop_bounds[1], y_crop_bounds[0]: y_crop_bounds[1], x_crop_bounds[0]: x_crop_bounds[1]]
                
            image_out_size = image_out.GetSize()
            
        return image_out_size



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

    
    