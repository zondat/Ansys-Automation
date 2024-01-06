import fileinput

def change_file_content(original_content, tag_name, new_value, pattern = "{} {}\n", order = 0):
    # Create new file
    # new_file = open(new_file_path, 'w')
    new_content = []
    nb_met = 0

    # Open the file in read mode and create a temporary file for writing
    # with fileinput.FileInput(file_path, inplace=True) as file:
    #file = fileinput.input(files=(file_path))
    for line in original_content:
            # Check if the line starts with the tag name
        if line.startswith(tag_name):
            nb_met = nb_met + 1
            # Replace the existing value with the new value
            # line = "{} {}\n".format(tag_name, new_value)
            if nb_met >= order:
                line = pattern.format(tag_name, new_value)
                
        # Print the line to the temporary file
        new_content.append(line)
        # new_content = new_content + line
    # new_file.close()
    return new_content
    
def isInteger(number):
    if number == round(number):
        return True
    else:
        return False

# convert number to string
def convert2string(num):
    if isInteger(num):
        return str(int(num))
    else:
        return str(float(num))

# Main program
if __name__ == "__main__":

    # Init value
    v = 15
    tail_to_fuselage_angle = 0
    for i in range(0, 6, 1):
        for j in range(-8, 48, 1):

            # Derived value
            ModelName = 'avenger'
            Workspace = 'D:/Workspace/Ansys'
            original_file_path = Workspace + '/Journal/base.wbjn'
            wing_to_fuselage_angle = i/2.0
            fuselage_angle = j/4.0
            FileName = 'f' + convert2string(fuselage_angle)+ '_w' + convert2string(wing_to_fuselage_angle) + '_t' + convert2string (tail_to_fuselage_angle)
            GeometryPath = Workspace + '/Geometry/Geom_' + ModelName + '_' + FileName +'.agdb'
            SavedWorkbenchPath = '\"' + Workspace + '/Project/' + FileName+ '_v' + convert2string (v) + '.wbpj' + '\"' 

            # Specify the file path and the new value
            original_file = open(original_file_path, 'r')
            original_content = original_file.readlines() 
            
            tag_name_1  =  "Export File"
            fuselage_file = Workspace + '/ExportedData/Avenger/fuselage/' + FileName + '_v' + convert2string (v)+'.dat'
            new_content_1 = change_file_content(original_content, tag_name_1, fuselage_file, "{} = {}\n", 1)
            wing_file     = Workspace + '/ExportedData/Avenger/wing/' + FileName + '_v' + convert2string (v)+'.dat'
            new_content_2 = change_file_content(new_content_1, tag_name_1, wing_file, "{} = {}\n", 2)
            tail_file     = Workspace + '/ExportedData/Avenger/tail/' + FileName + '_v' + convert2string (v)+'.dat'
            new_content_3 = change_file_content(new_content_2, tag_name_1, tail_file, "{} = {}\n", 3)
            
            tag_name_2  =  "    FilePath="
            new_content_4 = change_file_content(new_content_3, tag_name_2, SavedWorkbenchPath, "{} {},\n", 1)
            
            # Create new file
            new_journal_file = Workspace + '/Journal/' + FileName + '_v' + convert2string (v)+ '.wbjn'
            new_file = open(new_journal_file, 'w')
            new_content = "".join(new_content_4)
            new_file.write(new_content)
            new_file.close()
            
            # After change the neccessary content, Run script
            try:
                RunScript(new_journal_file)
            except Exception as e:
                # Exception handling for other types of exceptions
                print("An error occurred:", str(e))
                continue