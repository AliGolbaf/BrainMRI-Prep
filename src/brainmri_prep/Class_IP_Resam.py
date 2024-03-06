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
class IP_Resam:
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
    
    def docker_conform(self, image_in_name, image_in_directory):
        '''
        Command:
        docker run -it --rm -v $(pwd):/data --user 1000:1000 agolbaf/uop_frs:latest conform T1_001.nii.gz output.nii.gz
        ''' 
        self.image_in_name = image_in_name
        self.image_in_directory = image_in_directory
        
        # Cmommand
        comm_01 = "docker run --rm -v "  + self.image_in_directory + ":/data agolbaf/uop_frs:latest conform "
                   
        comm_02 = self.image_in_name + " "
        comm_03 = self.image_in_name.removesuffix(".nii.gz") + "_Conformed.nii.gz" 
        
        comm = comm_01 + comm_02 + comm_03
        
        # File Existence check
        check_file_name_in_directory_01 = comm_03
        
        directory_files = os.listdir(self.image_in_directory)
        directory_files.sort()
        
        if check_file_name_in_directory_01 in directory_files:
            self.status = "There is already a conformed version of the " + self.image_in_name + " in the directory"
        else:
            os.system(comm)
            # Update Directory
            directory_files = os.listdir(self.image_in_directory)
            directory_files.sort()
                
            if check_file_name_in_directory_01 in directory_files:
                self.status = "The " + self.image_in_name + " has been conformed!"
            else:
                self.status = "uop_frs was unable to conform the " + self.image_in_name
        
        return self.status
    