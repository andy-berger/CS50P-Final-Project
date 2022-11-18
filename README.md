# CS50P-Final-Project

## Screenshot

![Screenshot](/pdf.png?raw=true "PDF Screenshot")

## Description

**Cabinet Builder** helps you to create a plan for building a cabinet yourself.

Inputs:
* Kind of cabinet you want to build (cabinet with shelves or with drawers)
* Whether you want to build the cabinet with a left or right hand door (if you want to build a cabinet with shelves)
* The dimensions you want your cabinet to have (width/depth/height)
* The amount of shelves you want the cabinet to have (if you want to build a cabinet with shelves)
* Or the amount of drawers you want the cabinet to have (if you want to build a cabinet with drawers)

You can run the program as follows:
```
python project.py
```

Furthermore you can edit the constants such as MIN_CUTTING_WIDTH, MAX_CUTTING_WIDTH and THICK_WOOD_THICKNESS in project.py depending on the min/max cutting limits and wood thickness.

Output:

You will get a PDF file with:
* A sketch of your cabinet including the dimensions
* The configuration of your cabinet (cabinet type and number of shelves or drawers)
* An illustration of all pieces you'll need to build the cabinet including the dimensions for each piece

The output file name can be defined by changing the variable BUILD_PLAN_FILE_NAME.

## Technologies used

* fpdf (a library for PDF document generation under Python)

## Program structure

The program is structured as follows:
* the **main** function is launching the program
* the **create_cabinet** function is running all required parts of the program to create the build plan as a PDF file
* the **get_cabinet_version** function determines what kind of cabinet should be built
* the **get_cabinet_door_handing** determines what kind of door (left or right hand door) should be built (in case a cabinet with shelves should be built)
* the **get_dimensions** function determines the dimensions of the cabinet to build
* the **get_number_of_components** function determines the number of components (number of shelves or drawers)
* the **calculate_drawer_front_dimensions** function determines the dimensions of the drawer front panels (in case a cabinet with drawers should be built)
* the **calculate_needed_parts** function calculates the amount and dimensions of all needed parts to build the cabinet
* the **create_build_plan** function creates the build plan as a PDF file
