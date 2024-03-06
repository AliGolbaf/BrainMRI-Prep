'''
    * Useful Clasess 
'''

################################################################################
# import usefull functions from main code
################################################################################
# import usefull libraries
import SimpleITK as sitk

################################################################################   
class IP_ImaSho:
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
        

    def image_show(self,image_in_path, software_path):
        
        self.image_in_path = image_in_path
        self.software_path = software_path
        
        if len(self.software_path) == 0 :
            self.status = "Please select software"
        else:
            if len(self.image_in_path) == 0:
                self.status = "Please select the image"
            
            else:    
                # Set an image type for anytype we can use ""
                self.image_reader.SetImageIO("NiftiImageIO")
                self.image_reader.SetFileName(self.image_in_path)
                image_in = self.image_reader.Execute()
                # Select app for image_viewer
                self.image_viewer.SetApplication(self.software_path)
                self.image_viewer.Execute(image_in)
            
        return self.status
          
       
    
