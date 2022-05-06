####################################################################################
# Creating Individual conductors in Maxwell from MotorCAD                          #
# Conductors are grouped by turns and assigned to same winding                     #
#   Created by Akeel                                                               #
####################################################################################

from pyaedt.desktop import Desktop
from pyaedt import Maxwell2d
#import pyaedt
import numpy as np

def main():

    ################Settings##################
    num_slots = 6 ##Number of Slots Drawn in Maxwell
    angle = 45 ## Maxwell Symmetry angle
    Drawn_Slot = [1] # Which Slots to Draw conductors
    #Rad = 2.393/2 ## Radius of conductors
    Rad = 0.9081 / 2
    file = "ACLoss_3.mot"
    #file = "ACLoss.mot"
    Create_exc = True
    Create_wdg = False
    Group_turn = True

#######################Finding Go and Return Slot#####################################
    data_go = []
    phase_go = []
    phase_return = []
    data_return = []
    phase_pos = []
    with open(file, 'rt') as myfile:
        for myline in myfile:
            xy = [item for item in myline.split()]
            if any("GoSlot" in string for string in xy):
                phase_go.append(xy.__str__().split("="))
            if any("ReturnSlot" in string for string in xy):
                phase_return.append(xy.__str__().split("="))

            if any("TangentialPosition" in string for string in xy):
                phase_pos.append(xy)

    for item in phase_go:
        data_go.append(item[1].strip("']"))

    #print(data_go)

    for item in phase_return:
        data_return.append(item[1].strip("']"))

    #print(data_return)
###########################################################################################

    d = Desktop("2022.1", False, False)
    #aedt_project = r"C:\Users\aauckloo\PycharmProjects\MCAD\Create_Conductors\ACLoss_3_ANSYSEM_2D.aedt"
    #m2d = Maxwell2d(specified_version="2022.1", projectname=aedt_project)
    m2d = Maxwell2d()

    m2d.modeler.model_units = "mm"
    #m2d.modeler.primitives.delete("Ph1_P2_C1_1")

    data = []
    with open(file, 'rt') as myfile:
        for myline in myfile:
            xy = [item for item in myline.split()]
            if any("CustomFEARegions_Magnetic=Type" in string for string in xy):
                data.append(xy)

    xyz = [item for item in data.__str__().split(";")]

    test = []
    for i in xyz:
        if i.startswith("Type:1") or i.startswith(r"[['CustomFEARegions_Magnetic=Type:1"):
            test.append(i)

    test1 = [item.split("$") for item in test]
    circle_test=[]
    circles_id_all =[]
    circles_name =[]
#    textfile = open("position.txt", "w")
#    for element in test1:
#        textfile.write(element[1] + "\t" + element[2] + "\t" + element[3] + "\t" + "0" + "\t" + "\t" + element[10] + "\t" + element[9] + "\n")
        #textfile.write(element[2].split('XPos:', 1)[1] + "\t" + element[3].split('YPos:', 1)[1] + "\t" + "0" + "\t" + element[1].split('Name:', 1)[1] + "\t" + element[10].replace("CondSide:S","_") + "\n")
#    textfile.close()
    for x in Drawn_Slot:
        circles_id = []
        circles_name = []
        circle_test = []
        accessed_list = []
        accessed_mapping = []
        for point in test1:
            circle = m2d.modeler.primitives.create_circle(position=[point[2].split('XPos:', 1)[1] + "mm",point[3].split('YPos:', 1)[1] + "mm",0],
                                                          radius=Rad,
                                                          num_sides=8,
                                                          name="Slot_" + str(x) + "_" + point[9].replace(":", "_")+"_"+point[1].split('Name:', 1)[1] + point[10].replace("CondSide:S","_"),
                                                          matname="copper")


            circles_id.append(circle.id)
            circle_test.append(str(point[9].replace("CondTurn:","")))
            circles_name.append(circle.name)
        circles_id_all.append(circles_id)

        #################GROUPING##########################
        A = (max(circle_test))
        Turns =[]
        for i in range(1,(int(A)+1)):
            pos = np.where(np.array(circle_test) == str(i))[0]
            accessed_mapping = map(circles_id.__getitem__, pos)
            accessed_list = list(accessed_mapping)
            m = m2d.modeler.create_group(accessed_list, "None", "None", "Slot_" + str(x) + "_Turn_" + str(i))
            Turns.append(m)

        m2d.modeler.create_group("None", "None", Turns, "Slot_" + str(x))
        ##########################################################

        m2d.modeler.rotate(circles_id, "Z", (-angle / num_slots))


        y = x
        if str(x - 1) in data_return:
            m2d.modeler.mirror(circles_id, [0, 0, 0],[0, -100, 0])
            y = x + 1
            if Create_wdg:
                for items in Turns:
                    m2d.assign_winding(None, "External", False, 0, 0, 0,0, len(m2d.modeler.get_objects_in_group(items)), name=str(items) + "_Neg_Wdg")
                    for a in m2d.modeler.get_objects_in_group(items):
                        m2d.assign_coil(a, 1, "Negative", str(a))
                        m2d.add_winding_coils(str(items) + "_Neg_Wdg", a)
                #m2d.add_winding_coils(str(item) + "_Neg_Wdg", [str(item) + "_Neg"])
            if Create_exc and not Create_wdg:
                for item in circles_name:
                    m2d.assign_coil(item, 1, "Negative", str(item) +"_Neg")

        else:
            if Create_wdg:
                for items in Turns:
                    m2d.assign_winding(None, "External", False, 0, 0, 0, 0, len(m2d.modeler.get_objects_in_group(items)), name=str(items) + "_Pos_Wdg")
                    for a in m2d.modeler.get_objects_in_group(items):
                        m2d.assign_coil(a,1,"Positive", str(a))
                        m2d.add_winding_coils(str(items) + "_Pos_Wdg", a)
            if Create_exc and not Create_wdg:
                for item in circles_name:
                    m2d.assign_coil(item, 1, "Positive", str(item) +"_Pos")
        # rotate half slot back
        m2d.modeler.rotate(circles_id, "Z", (angle/num_slots)*(y-1))

    m2d.release_desktop(close_projects=False, close_desktop=False)
    pass
if __name__ == "__main__":
     main()

