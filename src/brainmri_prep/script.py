#!/usr/bin/env python3
""" 
    * Image Processing Pipeline: 
        1. Artifact reduction
        2. Resampling to 1mm3 voxel volums and size 256*256*256 (By Freesurfer Docker)
        3. Registration
        4. Bias Correction
        5. Normalisation
        6. Segmentation
        7. Segmentation correction
            4.1 False positive regions removing
            4.2 False negative regions (Hole Filling) correcting
        8. Skull stripping
        9. Visualisation
        
    * Written by Ali Golbaf
"""
################################################################################
# Import TKinter Libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
# For saving
import pickle
# Other libraries
################################################################################         
# Import Useful Libraries
import os
import sys
root_dir = os.path.dirname(os.path.abspath(__file__)) # This is the Project Root
################################################################################      
# Import Clasess
from Class_IP_InfReg import IP_InfReg
from Class_IP_Resam import IP_Resam
from Class_IP_Reg import IP_Reg
from Class_IP_BiCo import IP_BiCo
from Class_IP_Norm import IP_Norm
from Class_IP_Seg import IP_Seg
from Class_IP_ImaSho import IP_ImaSho
################################################################################
################################################################################
################################################################################
# Main app
master = tk.Tk()

# Set azure theme
master.tk.call("source", root_dir + "/azure/azure.tcl")
master.tk.call("set_theme", "dark")

# Set a minsize for the window, and place it in the middle
master.minsize(master.winfo_width(), master.winfo_height())
x_cord= int((master.winfo_screenwidth() / 2) - (master.winfo_width() / 2))
y_cord = int((master.winfo_screenheight() / 2) - (master.winfo_height() / 2))

# Add Logo
from Logo import logo_data_base64 
logo = tk.PhotoImage(data = logo_data_base64)
master.iconphoto(False, logo)

# Add description
master.title("BrainMRI-Prep")

################################################################################
# Style
def style_():
    style = ttk.Style(master)
    style.configure('TNotebook.Tab', tabposition='ns',width=20, height = 5, padding = [2,2])
    style.configure('TNotebook', tabposition='wn', tabmargins =  [2, 2, 0, 2], padding = [0,5])

# Add tabs
style = style_()
notebook = ttk.Notebook(master, style =  "lefttab.TNotebook")

################################################################################
# Add frames

# 1. Informative regions
frame_infromative_01 = ttk.Frame(notebook)
notebook.add(frame_infromative_01, text = "1. Informative Regions")

# 2. Resampling
frame_resampling_02 = ttk.Frame(notebook)
notebook.add(frame_resampling_02, text = "2. Resampling")

# 3. Registration
frame_registration_03 = ttk.Frame(notebook)
notebook.add(frame_registration_03, text = "3. Registration")

# 4. Registration
frame_biascorrection_04 = ttk.Frame(notebook)
notebook.add(frame_biascorrection_04, text = "4. Bias Correction")

# 5. Normalisation
frame_normalisation_05 = ttk.Frame(notebook)
notebook.add(frame_normalisation_05, text = "5. Normalisation")

# 6. Segmentation
frame_segmentation_06 = ttk.Frame(notebook)
notebook.add(frame_segmentation_06, text = "6. Segmentation")

# 7. Segmentation editor
frame_segmentation_editor_07 = ttk.Frame(notebook)
notebook.add(frame_segmentation_editor_07, text = "7. Segmentation Editor")

# # 8. Skull stripping
# frame_skull_stripping_08 = ttk.Frame(notebook)
# notebook.add(frame_skull_stripping_08, text = "8. Skull Stripping")

# 9. Visualisation
frame_visualisation_09 = ttk.Frame(notebook)
notebook.add(frame_visualisation_09, text = "Visualisation")

# Expand notebook
# notebook.pack(fill="both", expand=True)
notebook.pack(expand=True, fill=tk.BOTH)

################################################################################
################################################################################
################################################################################
"""1. Informative regions"""
# Variables
file_path_01 = ""
var_checkbutton_01_01 = tk.BooleanVar(value=True)
var_checkbutton_01_02 = tk.BooleanVar(value=False)
################################################################################
# Create a Frame for the input image
base_frame_01_01 = ttk.LabelFrame(frame_infromative_01, text="Input", padding=(20, 10))
base_frame_01_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_01_01_01 = ttk.Button(base_frame_01_01, text="Select File", command = lambda: frame_infromative_01_functions().select_file() )
button_frame_01_01_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the Checkbuttons (Options)
base_frame_01_02 = ttk.LabelFrame(frame_infromative_01, text="Options", padding=(20, 10))
base_frame_01_02.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Checkbuttons
# Check button for removing unconnected regions 
# 01
check_button_frame_01_02_01 = ttk.Checkbutton(base_frame_01_02, text="Drop Unconnected Non-Brain Voxels", variable = var_checkbutton_01_01)
check_button_frame_01_02_01.state(["disabled"])
check_button_frame_01_02_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

# 02
check_button_frame_01_02_02 = ttk.Checkbutton(base_frame_01_02, text="Drop Empty Slices \n (It will change the dimension of the image)",
                                              variable=var_checkbutton_01_02, 
                                              command = lambda: frame_infromative_01_functions().extract_informative_regions_for_showing_image_size() )
check_button_frame_01_02_02.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the out image
base_frame_01_03 = ttk.LabelFrame(frame_infromative_01, text="Output", padding=(20, 10))
base_frame_01_03.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for submit extraction
button_frame_01_03_01 = ttk.Button(base_frame_01_03, text="Start Extraction", command = lambda: frame_infromative_01_functions().extract_informative_regions() )
button_frame_01_03_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for image information
base_frame_01_04 = ttk.LabelFrame(frame_infromative_01, text="Information", padding=(20, 10))
base_frame_01_04.grid(row=1, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

class frame_infromative_01_functions:
    
    def select_file(self):
        # define global variables
        global file_path_01
        file_path_01 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_01) > 0 :
            
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_01)
            label_frame_01_01_01 = ttk.Label(base_frame_01_01, text=txt, padding=(0, 0))
            label_frame_01_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label in output section
            output_name = os.path.basename(file_path_01).removesuffix(".nii.gz") + "_Informative.nii.gz"
            txt = "Output file: "  + "\n" + "* " + output_name
            label_frame_01_03_01 = ttk.Label(base_frame_01_03, text=txt, padding=(0, 0))
            label_frame_01_03_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label for input image information in the information section
            txt = "Input image: "
            label_frame_01_04_01 = ttk.Label(base_frame_01_04, text=txt, padding=(0, 0))
            label_frame_01_04_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            image_reader = IP_InfReg().image_reader
            image_reader.SetImageIO("NiftiImageIO")
            image_reader.SetFileName(file_path_01)
            image_in =  image_reader.Execute()
            image_in_size = (image_in.GetSize())
            
            txt = "Size: " + str(image_in_size)
            label_frame_01_04_01 = ttk.Label(base_frame_01_04, text=txt, padding=(0, 0))
            label_frame_01_04_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label for output image information in the information section
            txt = "Output image: "
            label_frame_01_04_01 = ttk.Label(base_frame_01_04, text=txt, padding=(0, 0))
            label_frame_01_04_01.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label for output image information in the information section
            state_null_slices = var_checkbutton_01_02.get()
            image_in_directory, image_in_name = os.path.split(file_path_01)
            
            image_out_size = IP_InfReg().informative_region_for_showing_size(image_in_name, image_in_directory, state_null_slices)
            
            txt = "Size: " + str(image_out_size)
            label_frame_01_04_01 = ttk.Label(base_frame_01_04, text=txt, padding=(0, 0))
            label_frame_01_04_01.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
    def extract_informative_regions_for_showing_image_size(self):
        
        if len(file_path_01) > 0 :
            # label for output image information in the information section
            state_null_slices = var_checkbutton_01_02.get()
            image_in_directory, image_in_name = os.path.split(file_path_01)
        
            image_out_size = IP_InfReg().informative_region_for_showing_size(image_in_name, image_in_directory, state_null_slices)
        
            txt = "Size: " + str(image_out_size)
            label_frame_01_04_01 = ttk.Label(base_frame_01_04, text=txt, padding=(0, 0))
            label_frame_01_04_01.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
                     
    def extract_informative_regions(self):
        
        """1. Extract Informative region """
        ################################################################################
        state_null_slices = var_checkbutton_01_02.get()
        if len(file_path_01) == 0:
            status = "Please select the image"
            messagebox.showinfo(title='Status', message = status)
        else:
            # Import image
            image_in_directory, image_in_name = os.path.split(file_path_01)
            # Crop the images so that keeping the informative regions
            status = IP_InfReg().informative_region(image_in_name, image_in_directory, state_null_slices)
            messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""2. Resampling"""
# Variables
file_path_02 = ""

################################################################################
# Create a Frame for the input image
base_frame_02_01 = ttk.LabelFrame(frame_resampling_02, text="Input", padding=(20, 10))
base_frame_02_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_02_01_01 = ttk.Button(base_frame_02_01, text="Select File", command = lambda: frame_resampling_02_functions().select_file() )
button_frame_02_01_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the out image
base_frame_02_02 = ttk.LabelFrame(frame_resampling_02, text="Output", padding=(20, 10))
base_frame_02_02.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in the function
# Button for submit extraction
button_frame_02_02_01 = ttk.Button(base_frame_02_02, text="Start Conforming", command = lambda: frame_resampling_02_functions().conform())
button_frame_02_02_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for description
base_frame_02_03 = ttk.LabelFrame(frame_resampling_02, text="Description", padding=(20, 10))
base_frame_02_03.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in input section
txt = "A light version of FreeSurfer is containerised here using Docker." + "\n" + \
                "It conforms images to voxel sizes of 1mm³ and 256 slices in each"   + "\n" +  "spatial direction."
label_frame_02_03_01 = ttk.Label(base_frame_02_03, text=txt, padding=(0, 0))
label_frame_02_03_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

class frame_resampling_02_functions:
    
    def select_file(self):
        # define global variables
        global file_path_02
        file_path_02 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_02) > 0 :
            
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_02)
            label_frame_02_01_01 = ttk.Label(base_frame_02_01, text=txt, padding=(0, 0))
            label_frame_02_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label in output section
            output_name = os.path.basename(file_path_02).removesuffix(".nii.gz") + "_Conformed.nii.gz" 
            txt = "Output file: " + "\n" + "* "  + output_name
            label_frame_02_02_01 = ttk.Label(base_frame_02_02, text=txt, padding=(0, 0))
            label_frame_02_02_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")            
            
    def conform(self):

        """2. Conforming volume to 1mm^3 voxels and size 256x256x256 """
        ################################################################################
        
        if len(file_path_02) == 0:
            status = "Please select the image"
            messagebox.showinfo(title='Status', message = status)
        else:
            # Import image
            image_in_directory, image_in_name = os.path.split(file_path_02)

            # Conform image
            status = IP_Resam().docker_conform(image_in_name, image_in_directory)
            messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""3. Registration (SimpleElastic)"""
# Variables
file_path_03_01 = ""
file_path_03_02 = ""

################################################################################
# Create a Frame for the input image
base_frame_03_01 = ttk.LabelFrame(frame_registration_03, text="Fixed Image", padding=(20, 10))
base_frame_03_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_01_03_01 = ttk.Button(base_frame_03_01, text="Select File", command = lambda: frame_registration_03_functions().select_file_01() )
button_frame_01_03_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the tab menu option
base_frame_03_02 = ttk.LabelFrame(frame_registration_03, text="Options", padding=(20, 10))
base_frame_03_02.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in option section
txt = "SimpleElastix, a medical image registration library, is used here to apply"  + "\n" + "image registration." + \
        "\n" + "Options available:" + "\n * Rigid Registration \n * Affine Registration \n * Non-rigid Registration"
label_frame_03_02_01 = ttk.Label(base_frame_03_02, text=txt, padding=(0, 0))
label_frame_03_02_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
# Tab menu
# Combobox
combo_list = ["Rigid Registration", "Affine Registration", "Non-rigid Registration"]
combobox_frame_03_02_01 = ttk.Combobox(base_frame_03_02, textvariable=tk.StringVar(), values=combo_list)
combobox_frame_03_02_01['state'] = 'readonly'
combobox_frame_03_02_01.current(0)
combobox_frame_03_02_01.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
################################################################################
# Create a Frame for the out image
base_frame_03_03 = ttk.LabelFrame(frame_registration_03, text="Moving Image", padding=(20, 10))
base_frame_03_03.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_03_03_01 = ttk.Button(base_frame_03_03, text="Select File", command = lambda: frame_registration_03_functions().select_file_02() )
button_frame_03_03_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

#################################################################################
# Create a Frame for registration
base_frame_03_04 = ttk.LabelFrame(frame_registration_03, text="Registration", padding=(20, 10))
base_frame_03_04.grid(row=1, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for submit extraction
button_frame_01_03_01 = ttk.Button(base_frame_03_04, text="Start Registration", command = lambda: frame_registration_03_functions().start_registration() )
button_frame_01_03_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

class frame_registration_03_functions:
    
    def select_file_01(self):
        # define global variables
        global file_path_03_01
        
        file_path_03_01 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_03_01) > 0 :
            
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_03_01)
            label_frame_03_01_01 = ttk.Label(base_frame_03_01, text=txt, padding=(0, 0))
            label_frame_03_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
              
    def select_file_02(self):
        
        # define global variables
        global file_path_03_02
        
        file_path_03_02 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_03_02) > 0 :
            
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_03_02)
            label_frame_03_03_01 = ttk.Label(base_frame_03_03, text=txt, padding=(0, 0))
            label_frame_03_03_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")     
            
            # Label in registration section
            
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_03_02)
            label_frame_03_03_01 = ttk.Label(base_frame_03_03, text=txt, padding=(0, 0))
            label_frame_03_03_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew") 
            
            # Update label in the registration section for image output name (Just for the first time)
            registration_type = combobox_frame_03_02_01.get()
            
            if registration_type == "Rigid Registration":
               name_0 = "Rigid"
               
            if registration_type == "Affine Registration":
               name_0 = "Affine"
           
            if registration_type == "Non-rigid Registration":
               name_0 = "NonRigid"
            image_moving_directory, image_moving_name = os.path.split(file_path_03_02)   
            image_out_name = os.path.basename(image_moving_name).removesuffix(".nii.gz") + "_Reg("+ str(name_0) +").nii.gz" 
            label_frame_03_04_01 = ttk.Label(base_frame_03_04, text=image_out_name, padding=(0, 0))
            label_frame_03_04_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # Update label in the registration section for image output name
            combobox_frame_03_02_01.bind('<<ComboboxSelected>>', self.update_label)
            
    def update_label(self, event):
        
        registration_type = combobox_frame_03_02_01.get()
        
        if registration_type == "Rigid Registration":
            name_0 = "Rigid"
           
        if registration_type == "Affine Registration":
            name_0 = "Affine"
       
        if registration_type == "Non-rigid Registration":
            name_0 = "NonRigid"
           
        image_moving_directory, image_moving_name = os.path.split(file_path_03_02)   
        image_out_name = os.path.basename(image_moving_name).removesuffix(".nii.gz") + "_Reg("+ str(name_0) +").nii.gz" 
        label_frame_03_04_01 = ttk.Label(base_frame_03_04, text=image_out_name, padding=(0, 0))
        label_frame_03_04_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
    
    def start_registration(self):
        
        """3. Registration """
        ################################################################################
        registration_type = combobox_frame_03_02_01.get()
        
        if len(file_path_03_01) == 0:
            status = "Please select the fixed image"
            messagebox.showinfo(title='Status', message = status)
        else:
            
            if len(file_path_03_02) == 0:
                status = "Please select the moving image"
                messagebox.showinfo(title='Status', message = status)
        
            else:
                # Import images
                image_fixed_directory, image_fixed_name = os.path.split(file_path_03_01)
                image_moving_directory, image_moving_name = os.path.split(file_path_03_02)
                
                # Crop the images so that keeping the informative regions
                status = IP_Reg().registration(image_fixed_directory, image_fixed_name, image_moving_directory, image_moving_name, registration_type)
                messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""4. Bias Correction"""
# Variables
file_path_04 = ""

################################################################################
# Create a Frame for the input image
base_frame_04_01 = ttk.LabelFrame(frame_biascorrection_04, text="Input", padding=(20, 10))
base_frame_04_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_04_01_01 = ttk.Button(base_frame_04_01, text="Select File", command = lambda: frame_biascorrection_04_functions().select_file() )
button_frame_04_01_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the out image
base_frame_04_02 = ttk.LabelFrame(frame_biascorrection_04, text="Output", padding=(20, 10))
base_frame_04_02.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in the function

# Button for submit extraction
button_frame_04_02_01 = ttk.Button(base_frame_04_02, text="Start Correcting", command = lambda: frame_biascorrection_04_functions().bias_correction())
button_frame_04_02_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for description
base_frame_04_03 = ttk.LabelFrame(frame_biascorrection_04, text="Description", padding=(20, 10))
base_frame_04_03.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in input section
txt = "Here the SimpleITK 'N4BiasFieldCorrectionImageFilter' is utilised." + \
         "\nThis filter requires one input image affected by a bias field \
          \nthat needs correction."
label_frame_04_03_01 = ttk.Label(base_frame_04_03, text=txt, padding=(0, 0))
label_frame_04_03_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

class frame_biascorrection_04_functions:
    
    def select_file(self):
        # define global variables
        global file_path_04
        file_path_04 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_04) > 0 :
            
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_04)
            label_frame_04_01_01 = ttk.Label(base_frame_04_01, text=txt, padding=(0, 0))
            label_frame_04_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label in output section
            output_name = os.path.basename(file_path_04).removesuffix(".nii.gz") + "_BiCo.nii.gz" 
            txt = "Output file: " + "\n" + "* "  + output_name
            label_frame_04_02_01 = ttk.Label(base_frame_04_02, text=txt, padding=(0, 0))
            label_frame_04_02_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
              
    def bias_correction(self):

        """2. N4 Bias correction """
        ################################################################################
        
        if len(file_path_04) == 0:
            status = "Please select the image"
            messagebox.showinfo(title='Status', message = status)
        else:
            # Import image
            image_in_directory, image_in_name = os.path.split(file_path_04)

            # Conform image
            status = IP_BiCo().bias_correction(image_in_name, image_in_directory)
            messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""5. Normalisation"""
# Variables
file_path_05 = ""

################################################################################
# Create a Frame for the input image
base_frame_05_01 = ttk.LabelFrame(frame_normalisation_05, text="Input", padding=(20, 10))
base_frame_05_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_05_01_01 = ttk.Button(base_frame_05_01, text="Select File", command = lambda: frame_normalisation_05_functions().select_file() )
button_frame_05_01_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the out image
base_frame_05_02 = ttk.LabelFrame(frame_normalisation_05, text="Output", padding=(20, 10))
base_frame_05_02.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in the function

# Button for submit extraction
button_frame_05_02_01 = ttk.Button(base_frame_05_02, text="Start Normalising", command = lambda: frame_normalisation_05_functions().normalising())
button_frame_05_02_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for description
base_frame_05_03 = ttk.LabelFrame(frame_normalisation_05, text="Description", padding=(20, 10))
base_frame_05_03.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in input section
txt = "Here the SimpleITK 'NormalizeImageFilter' is utilised."
label_frame_05_03_01 = ttk.Label(base_frame_05_03, text=txt, padding=(0, 0))
label_frame_05_03_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

class frame_normalisation_05_functions:
    
    def select_file(self):
        # define global variables
        global file_path_05
        file_path_05 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_05) > 0 :
            
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_05)
            label_frame_05_01_01 = ttk.Label(base_frame_05_01, text=txt, padding=(0, 0))
            label_frame_05_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label in output section
            output_name = os.path.basename(file_path_05).removesuffix(".nii.gz") + "_Norm.nii.gz" 
            txt = "Output file: " + "\n" + "* "  + output_name
            label_frame_05_02_01 = ttk.Label(base_frame_05_02, text=txt, padding=(0, 0))
            label_frame_05_02_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
              
    def normalising(self):

        """5. Normalisation """
        ################################################################################
        
        if len(file_path_05) == 0:
            status = "Please select the image"
            messagebox.showinfo(title='Status', message = status)
        else:
            # Import image
            image_in_directory, image_in_name = os.path.split(file_path_05)

            # Conform image
            status = IP_Norm().bias_correction(image_in_name, image_in_directory)
            messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""6. Segmentation"""
# Variables
file_path_06 = ""
option_menu_list = ["", "Cpu-Based", "Gpu_Based"]
option_var_6 = tk.StringVar(value=option_menu_list[1])
################################################################################
# Create a Frame for the input image
base_frame_06_01 = ttk.LabelFrame(frame_segmentation_06, text="Input", padding=(20, 10))
base_frame_06_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_06_01_01 = ttk.Button(base_frame_06_01, text="Select File", command = lambda: frame_segmentation_06_functions().select_file() )
button_frame_06_01_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the out image
base_frame_06_02 = ttk.LabelFrame(frame_segmentation_06, text="Output", padding=(20, 10))
base_frame_06_02.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in the function

# Button for submit extraction
button_frame_06_02_01 = ttk.Button(base_frame_06_02, text="Start Segmentation", command = lambda: frame_segmentation_06_functions().segment())
button_frame_06_02_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a frame for option menu
base_frame_06_03 = ttk.LabelFrame(frame_segmentation_06, text="Options", padding=(20, 10))
base_frame_06_03.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# OptionMenu
optionmenu_frame_06_03_01 = ttk.OptionMenu(base_frame_06_03, option_var_6,* option_menu_list)
optionmenu_frame_06_03_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for description
base_frame_06_04 = ttk.LabelFrame(frame_segmentation_06, text="Description", padding=(20, 10))
base_frame_06_04.grid(row=1, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in input section
txt_01 = "Automated meningioma segmentation:" + "\n" + \
         "Neuronets/am; a publicly available deep learning model"  + "\n" +  \
         "is used here to segment the imported image."
txt_02 = "Note: \nThe imported image should be contrast-enhanced" + "\n" + "T1-weighted MRI."
txt = txt_01 + "\n" + txt_02
label_frame_06_03_01 = ttk.Label(base_frame_06_04, text=txt, padding=(0, 0))
label_frame_06_03_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

class frame_segmentation_06_functions:
    
    def select_file(self):
        # define global variables
        global file_path_06
        file_path_06 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_06) > 0 :
            
            # label in input section
            txt = "Input file: "+ "\n" + "* "  + os.path.basename(file_path_06)
            label_frame_06_01_01 = ttk.Label(base_frame_06_01, text=txt, padding=(0, 0))
            label_frame_06_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
            # label in output section
            output_name = os.path.basename(file_path_06).removesuffix(".nii.gz") + "_Segmented.nii.gz" 
            txt = "Output file: " + "\n" + "* "   + output_name
            label_frame_06_02_01 = ttk.Label(base_frame_06_02, text=txt, padding=(0, 0))
            label_frame_06_02_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            
    def segment(self):

        """6. Segmentation """
        ################################################################################
        
        if len(file_path_06) == 0:
            status = "Please select the image"
            messagebox.showinfo(title='Status', message = status)
        else:
            # Import image
            image_in_directory, image_in_name = os.path.split(file_path_06)
            mode = option_var_6.get()
            # Segment image
            status = IP_Seg().docker_ams_segmentation(image_in_name, image_in_directory, mode)
            messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""7. Segmentation Editor"""
# Variables
file_path_07 = ""
var_chackbutton_07_01 = tk.BooleanVar(value=True)
################################################################################
# Create a Frame for the input image
base_frame_07_01 = ttk.LabelFrame(frame_segmentation_editor_07, text="Input", padding=(20, 10))
base_frame_07_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Button for adding a nifti file
button_frame_07_01_01 = ttk.Button(base_frame_07_01, text="Select Label", command = lambda: frame_segmentation_editor_07_functions().select_file() )
button_frame_07_01_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a Frame for the out image
base_frame_07_02 = ttk.LabelFrame(frame_segmentation_editor_07, text="Output", padding=(20, 10))
base_frame_07_02.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label in the function

# Button for submit extraction
button_frame_07_02_01 = ttk.Button(base_frame_07_02, text="Start Editing", command = lambda: frame_segmentation_editor_07_functions().edit())
button_frame_07_02_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# Create a frame for options
base_frame_07_03 = ttk.LabelFrame(frame_segmentation_editor_07, text="Options", padding=(20, 10))
base_frame_07_03.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

# Spinbox
spinbox_frame_07_03_01 = ttk.Spinbox(base_frame_07_03, from_=1, to=20, increment=1, command = lambda: frame_segmentation_editor_07_functions().dynamic_changing_of_labels())
spinbox_frame_07_03_01.insert(0, "Number of Tumours")
spinbox_frame_07_03_01.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

# Check button for hole filling
check_button_frame_07_03_01 = ttk.Checkbutton(base_frame_07_03, text="Hole Filling", variable = var_chackbutton_07_01)
check_button_frame_07_03_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

class frame_segmentation_editor_07_functions():
    
    def select_file(self):
        # define global variables
        global file_path_07
        file_path_07 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_07) > 0 :
            number_of_tumours  = spinbox_frame_07_03_01.get()
            # label in input section
            txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_07)
            label_frame_07_01_01 = ttk.Label(base_frame_07_01, text=txt, padding=(0, 0))
            label_frame_07_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
    
    # Dynamic updating procedure for check button
    def dynamic_changing_of_labels(self):
         
         if len(file_path_07) > 0 :
             number_of_tumours  = spinbox_frame_07_03_01.get()
             # label in input section
             txt = "Input file: " + "\n" + "* " + os.path.basename(file_path_07)
             label_frame_07_01_01 = ttk.Label(base_frame_07_01, text=txt, padding=(0, 0))
             label_frame_07_01_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
             
             # label in output section
             output_name = os.path.basename(file_path_07).removesuffix(".nii.gz")  + "_Modified_L" + str(number_of_tumours) + ".nii.gz"
             txt = "Output file: " + "\n" + "* "  + output_name
             label_frame_07_02_01 = ttk.Label(base_frame_07_02, text=txt, padding=(0, 0))
             label_frame_07_02_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")    
            
    def edit(self):
        
        """3. Segmentation correction, (Select number of tumours in the image) """
        ################################################################################
        state_hole_filling = var_chackbutton_07_01.get()
        number_of_tumours  = spinbox_frame_07_03_01.get()
        if len(file_path_07) == 0:
            status = "Please select the label"
            messagebox.showinfo(title='Status', message = status)
        else:
            
            if number_of_tumours == "Number of Tumours":
                status = "Please enter number of tumors"
                messagebox.showinfo(title='Status', message = status)
            else:
                 
                # Import image
                image_in_directory, image_in_name = os.path.split(file_path_07)
                number_of_tumours = int(number_of_tumours)
                status = IP_Seg().segmentation_correction(image_in_name, image_in_directory, 
                                                                   num_of_tumours = number_of_tumours, 
                                                                   hole_filling = state_hole_filling)
                messagebox.showinfo(title='Status', message = status)

################################################################################
################################################################################
################################################################################
"""6. Visualisation Frame"""
# Variables
file_path_09 = ""
software_path_09 = ""
azure_theme = ""
################################################################################
# Create a Frame for the visualiser_app_button
base_frame_09_01 = ttk.LabelFrame(frame_visualisation_09, text="Select Software", padding=(20, 10))
base_frame_09_01.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# label for compatible versions in frame
txt = "Supported Software:" + "\n" +  "1. Fiji" + "\n" + "2. 3D Slicer" + "\n" + "3. ITK-SNAP" + "\n" + "4. ImageMagick"
label_frame_09_01_01 = ttk.Label(base_frame_09_01, text=txt, padding=(0, 0))
label_frame_09_01_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

# visualiser_app_button in frame
button_frame_09_01_01 = ttk.Button(base_frame_09_01, text="Select Software", 
                                   command = lambda: frame_visualisation_09_functions().visualiser_app(save = "no") )
button_frame_09_01_01.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# mode switching
# Create a Frame for the mode switching
base_frame_09_02 = ttk.LabelFrame(frame_visualisation_09, text="Mode", padding=(20, 10))
base_frame_09_02.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

# switch
switch_frame_09_01 = ttk.Checkbutton(base_frame_09_02, text="Dark/Light Mode", style="Switch.TCheckbutton", 
                                     command = lambda: frame_visualisation_09_functions().switch_mode_(save = "no") )
switch_frame_09_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

################################################################################
# image operation
# Create a Frame for the mode switching
base_frame_09_03 = ttk.LabelFrame(frame_visualisation_09, text="Visualisation", padding=(20, 10))
base_frame_09_03.grid(row=0, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")

button_frame_09_03_01 = ttk.Button(base_frame_09_03, text="Select File", command = lambda: frame_visualisation_09_functions().select_file() )
button_frame_09_03_01.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

# Row = 1 is occupied by label_frame_06_03_01 

button_frame_09_03_02 = ttk.Button(base_frame_09_03, text="Show", command = lambda: frame_visualisation_09_functions().image_show() )
button_frame_09_03_02.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

class frame_visualisation_09_functions:
    
    def switch_mode_(self, save):
        
        global azure_theme
        
        # To define whrere the command is going from
        self.save = save
        
        if self.save == "no":
            
            # NOTE: The theme's real name is azure-<mode>
            azure_theme = master.tk.call("ttk::style", "theme", "use")
            if azure_theme == "azure-dark":
                # Set light theme
                master.tk.call("set_theme", "light")
                
                # Maintain style
                style = style_()
                
                # save settings
                azure_theme = master.tk.call("ttk::style", "theme", "use")
                self.save_switch_mode_()
            else:
                # Set dark theme
                master.tk.call("set_theme", "dark")
                
                # Maintain style
                style = style_()
                
                # save settings
                azure_theme = master.tk.call("ttk::style", "theme", "use")
                self.save_switch_mode_()
                
        if self.save == "yes":
            print(azure_theme)
            
            if azure_theme == "azure-dark":
               # Set dark theme
               master.tk.call("set_theme", "dark")
               # Maintain style
               style = style_()
               
            else:
                # Set light theme
                master.tk.call("set_theme", "light")
                # Maintain style
                style = style_()
    
    def visualiser_app(self,save):
        
        # define global variables
        global software_path_09
        # To define whrere the command is going from
        self.save = save
        
        if self.save == "yes":
            # Dynamic labels
            # label
            txt = "Selected Software: " + os.path.basename(software_path_09)
            label_frame_09_01_02 = ttk.Label(base_frame_09_01, text=txt, padding=(0, 0))
            label_frame_09_01_02.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        
        else:
            software_path_09 = filedialog.askopenfilename(parent=master,title='Select Software')
            self.save_visualiser_app()
        
            # Dynamic labels
            if len(software_path_09) > 0 :
                # label
                txt = "Selected Software: " + os.path.basename(software_path_09)
                label_frame_09_01_02 = ttk.Label(base_frame_09_01, text=txt, padding=(0, 0))
                label_frame_09_01_02.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
    
    def select_file(self):
        # define global variables
        global file_path_09
        file_path_09 = filedialog.askopenfilename(parent=master,title='Select File', filetypes = (("NIfTI files","*.nii.gz"),("all files","*.*")))
        
        if len(file_path_09) > 0 :
            txt = "Selected file: " + os.path.basename(file_path_09)
            label_frame_09_03_01 = ttk.Label(base_frame_09_03, text=txt, padding=(0, 0))
            label_frame_09_03_01.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
          
    def image_show(self):
        status = IP_ImaSho().image_show(file_path_09,software_path_09)
        if len(status) > 0:
            messagebox.showinfo(title='Status', message = status)  
            
    # By now, I ignore the saving procedure of the theme and selected software. 
    def save_visualiser_app(self):
        config = {'software_path_09': software_path_09}
        # with open("saved_settings_visualiser_app.dat", "wb") as pickle_file:
        #     pickle.dump(config, pickle_file, pickle.HIGHEST_PROTOCOL)         

    def save_switch_mode_(self):
        config = {"azure_theme": azure_theme}
        # with open("saved_settings_switch_mode.dat", "wb") as pickle_file:
        #     pickle.dump(config, pickle_file, pickle.HIGHEST_PROTOCOL)

################################################################################
################################################################################
################################################################################
# Check saved files to be opened if exixt
# directory_files = os.listdir()
# directory_files.sort()

# # load Save setting for visualiser
# if "saved_settings_visualiser_app.dat" in directory_files:      
#     with open("saved_settings_visualiser_app.dat", "rb") as pickle_file:
#             config = pickle.load(pickle_file)
#             software_path_09 = config.get('software_path_09')
#             frame_visualisation_09_functions().visualiser_app(save = "yes")

# # load save setting for mode    
# if "saved_settings_switch_mode.dat" in directory_files:      
#     with open("saved_settings_switch_mode.dat", "rb") as pickle_file:
#             config = pickle.load(pickle_file)
#             azure_theme = config.get('azure_theme')
#             frame_visualisation_09_functions().switch_mode_(save = "yes")    

master.mainloop()
