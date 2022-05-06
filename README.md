# MotorCAD_Maxwell_ACLoss
Requirements: PyAEDT, Ansys MotorCAD, Ansys Maxwell (Ansys Electronic Desktop)
# Introduction
This is an example for creating individual conductors in Ansys Maxwell using data from Ansys MotorCAD. This example is licensed under the https://github.com/akeel-a/MotorCAD_Maxwell_ACLoss/blob/master/LICENSE.
# Setup
## Preparing the MotorCAD file:
![image](https://user-images.githubusercontent.com/104905123/167090497-4677cb53-60e8-4a76-9a58-54b2bff2dbf4.png)
Enable Custom Regions -> E-Magnetic
Save the MotorCAD file
Export Maxwell 2D model using Tools-> Ansys Electronic Desktop
![image](https://user-images.githubusercontent.com/104905123/167091398-2e942b89-55ff-4f8a-8b9c-a1aa6e466656.png)

## Prepare the Maxwell Model
Open Electronic Desktop
Run the .vbs script created from MotorCAD
![image](https://user-images.githubusercontent.com/104905123/167091605-82f82b48-e0c4-4f29-bb92-f1bf13fc3047.png)

## Configure Create_Conductors_MCAD_MXWL.py
    ################Settings##################
    num_slots = 6 ##Number of Slots Drawn in Maxwell
    angle = 45 ## Maxwell Symmetry angle
    Drawn_Slot = [1] # Which Slots to Draw conductors
    Rad = 0.9081 / 2
    file = "ACLoss_3.mot"
    Create_exc = True
    Create_wdg = False
    Group_turn = True
    
    Run Create_Conductors_MCAD_MXWL.py
