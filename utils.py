import os
def create_coord_list(x1, y1, x2, y2):

    coord_list = []

    for x in range(x1, x2):

        for y in range(y1, y2):

            coord_list.append((x, y))

    return coord_list

def mcmeta_file(full_path_dir, file_count, reverse_animation=False):
    dir_name = os.path.dirname(full_path_dir)
    file_name = os.path.basename(full_path_dir)
    file_number = file_count
    with open(os.path.join(dir_name, f"{file_name}.mcmeta"), mode='w') as f:
        f.write("{\n")
        f.write("  \'animation\': {\n")
        f.write("    \"frametime\": 1, #Animation speed\n")
        f.write("    \"frames\": [\n")
        for loopnum in range(file_number):
            if loopnum == file_number - 1:
                if reverse_animation == False: 
                    f.write("      {}\n".format(loopnum))
            else:
                f.write("      {},\n".format(loopnum))
        if reverse_animation == True:
            f.write("      #----Reverse----\n")
            for loopnum in reversed(range(file_number - 2)):
                if loopnum == 1:
                    f.write("      {}\n".format(loopnum))
                    break
                else:
                    f.write("      {},\n".format(loopnum))
        f.write("    ]\n")
        f.write("  }\n")
        f.write("}")
    print("Mcmeta file created")

def properties_file(full_path_dir, w, h):
    dir_name = os.path.dirname(full_path_dir)
    file_name = os.path.basename(full_path_dir)
    with open(os.path.join(dir_name, f"{file_name}.properties"), mode='w') as f:
        f.write("duration=1\n")
        f.write(f"w={w}\n")
        f.write(f"h={h}\n")
        f.write("x=0\n")
        f.write("y=0\n")
        f.write(f"from=./{file_name}\n")
        f.write("to=textures/gui/container/inventory.png")
    print("Properties file created")