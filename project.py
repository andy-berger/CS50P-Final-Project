from fpdf import FPDF

THICK_WOOD_THICKNESS = 15
THIN_WOOD_THICKNESS = 12
MIN_CUTTING_WIDTH = 100
MAX_CUTTING_WIDTH = 1230
MIN_CUTTING_DEPTH = 100
MAX_CUTTING_DEPTH = 1230
MIN_CUTTING_HEIGHT = 100
MAX_CUTTING_HEIGHT = 2480
MIN_WIDTH = MIN_CUTTING_WIDTH + 2 * THICK_WOOD_THICKNESS
MAX_WIDTH = MAX_CUTTING_WIDTH
MIN_DEPTH = MIN_CUTTING_DEPTH + THIN_WOOD_THICKNESS
MAX_DEPTH = MAX_CUTTING_DEPTH
MIN_HEIGHT_COMPONENT = 120
MIN_HEIGHT = MIN_HEIGHT_COMPONENT + 2 * THICK_WOOD_THICKNESS
MAX_HEIGHT = MAX_CUTTING_HEIGHT + 2 * THICK_WOOD_THICKNESS
DOOR_SPACING = 2
DRAWER_MAX_WIDTH = 800
DRAWER_MIN_SPACING = 2
DRAWER_WIDTH_RAIL = 13
BUILD_PLAN_FILE_NAME = "plan.pdf"


def main():
    create_cabinet()


def create_cabinet():
    cabinet_version = get_cabinet_version()
    width, depth, height = get_dimensions(cabinet_version)
    number_of_components = get_number_of_components(cabinet_version, height)

    if cabinet_version.startswith("s"):
        create_build_plan(width, depth, height, cabinet_version, number_of_components)
    else:
        drawer_width, drawer_height = calculate_drawer_front_dimensions(width, height, number_of_components)
        create_build_plan(width, depth, height, cabinet_version, number_of_components, drawer_width, drawer_height)

    print(f"\nBuild plan is ready: {BUILD_PLAN_FILE_NAME}")


def get_cabinet_version():
    error_message = "\nInvalid choice, please try again! Either s or d must be chosen."
    while True:
        try:
            cabinet_choice = input("What kind of cabinet do you want to build:\ns) Cabinet with shelves\nd) Cabinet with drawers\nChoice: ").lower()
            if cabinet_choice == "s":
                door_handing = get_cabinet_door_handing()
                if door_handing == "l":
                    return "sl"
                elif door_handing == "r":
                    return "sr"
                else:
                    print(error_message)
                    continue
            elif cabinet_choice == "d":
                return "d"
            else:
                print(error_message)
                continue
        except ValueError:
            print(error_message)
            continue


def get_cabinet_door_handing():
    error_message = "\nInvalid choice, please try again! Either l or r must be chosen."
    while True:
        try:
            door_handing = input("\nWhat kind of cabinet door do you want:\nl) Left hand door (door handle on the right)\nr) Right hand door (door handle on the left)\nChoice: ").lower()
            if door_handing == "l":
                return "l"
            elif door_handing == "r":
                return "r"
            else:
                print(error_message)
                continue
        except ValueError:
            print(error_message)
            continue


def get_dimensions(cabinet_version):
    error_message = "\nInvalid choice, please try again! Valid numeric values must be entered."
    if cabinet_version.startswith("s"):
        min_width = MIN_WIDTH + 2 * DOOR_SPACING
        max_width = MAX_WIDTH
        min_height = MIN_HEIGHT + 2 * DOOR_SPACING
    else:
        min_width = MIN_WIDTH + 2 * THICK_WOOD_THICKNESS + 2 * DRAWER_WIDTH_RAIL
        max_width = DRAWER_MAX_WIDTH
        min_height = MIN_HEIGHT + 2 * DRAWER_MIN_SPACING

    def get_length_of_side(prompt, min_length, max_length):
        while True:
            try:
                length = int(input(prompt))
                if not min_length <= length <= max_length:
                    print(error_message)
                    continue
                else:
                    return length
            except ValueError:
                print(error_message)
                continue

    print("\nPlease specify the dimensions of your cabinet.")
    width = get_length_of_side(f"Width in mm ({min_width}-{max_width}): ", min_width, max_width)
    depth = get_length_of_side(f"Depth in mm ({MIN_DEPTH}-{MAX_DEPTH}): ", MIN_DEPTH, MAX_DEPTH)
    height = get_length_of_side(f"Height in mm ({min_height}-{MAX_HEIGHT}): ", min_height, MAX_HEIGHT)
    return width, depth, height


def get_number_of_components(cabinet_version, height):
    error_message = "\nInvalid choice, please try again! A valid numeric value must be entered."
    if cabinet_version.startswith("s"):
        min = 0
        max = int(height / MIN_HEIGHT_COMPONENT) - 1
        message = f"\nHow many shelves do you want ({min}-{max}): "
    else:
        min = int(height / (1.5 * MIN_HEIGHT_COMPONENT))
        max = int(height / MIN_HEIGHT_COMPONENT)
        if max == 1:
            return 1
        message = f"\nHow many drawers do you want ({min}-{max}): "
    if max == 0:
        return 0
    while True:
        try:
            number_of_components = int(input(message))
            if min <= number_of_components <= max:
                return number_of_components
            else:
                print(error_message)
                continue
        except ValueError:
            print(error_message)
            continue


def calculate_drawer_front_dimensions(width, height, number_of_components):
    if number_of_components > 0:
        total_spacing_vertical = number_of_components + (number_of_components + 4)
        total_drawer_front_heights = height - 2 * THICK_WOOD_THICKNESS - total_spacing_vertical
        single_drawer_front_width = width - 2 * THICK_WOOD_THICKNESS - DRAWER_MIN_SPACING
        single_drawer_front_height = total_drawer_front_heights // number_of_components
        return single_drawer_front_width, single_drawer_front_height
    else:
        return 0, 0


def calculate_needed_parts(width, depth, height, cabinet_version, number_of_components, drawer_width=0, drawer_height=0):
    parts_dimensions = {}

    # Bottom and top:
    parts_dimensions["bottom_and_top_amount"] = 2
    parts_dimensions["bottom_and_top_width"] = depth - THIN_WOOD_THICKNESS
    parts_dimensions["bottom_and_top_height"] = width
    parts_dimensions["bottom_and_top_thickness"] = THICK_WOOD_THICKNESS

    # Sides:
    parts_dimensions["sides_amount"] = 2
    parts_dimensions["sides_width"] = depth - THIN_WOOD_THICKNESS
    parts_dimensions["sides_height"] = height - 2 * THICK_WOOD_THICKNESS
    parts_dimensions["sides_thickness"] = THICK_WOOD_THICKNESS

    # Back:
    parts_dimensions["back_amount"] = 1
    parts_dimensions["back_width"] = width
    parts_dimensions["back_height"] = height
    parts_dimensions["back_thickness"] = THIN_WOOD_THICKNESS

    if cabinet_version.startswith("s"):
        # Door:
        parts_dimensions["door_amount"] = 1
        parts_dimensions["door_width"] = width - 2 * DOOR_SPACING
        parts_dimensions["door_height"] = height - 2 * DOOR_SPACING
        parts_dimensions["door_thickness"] = THICK_WOOD_THICKNESS

        # Shelves:
        parts_dimensions["shelves_amount"] = number_of_components
        parts_dimensions["shelves_width"] = depth - THIN_WOOD_THICKNESS - THICK_WOOD_THICKNESS
        parts_dimensions["shelves_height"] = width - 2 * THICK_WOOD_THICKNESS
        parts_dimensions["shelves_thickness"] = width - 2 * THICK_WOOD_THICKNESS
    else:
        # Drawer bottoms:
        parts_dimensions["drawer_bottoms_amount"] = number_of_components
        parts_dimensions["drawer_bottoms_width"] = width - 4 * THICK_WOOD_THICKNESS - 2 * DRAWER_WIDTH_RAIL
        parts_dimensions["drawer_bottoms_height"] = depth - 2 * THICK_WOOD_THICKNESS - 2 * THIN_WOOD_THICKNESS - 2
        parts_dimensions["drawer_bottoms_thickness"] = THICK_WOOD_THICKNESS

        # Drawer sides:
        parts_dimensions["drawer_sides_amount"] = 2 * number_of_components
        parts_dimensions["drawer_sides_width"] = depth - 2 * THIN_WOOD_THICKNESS - 2
        parts_dimensions["drawer_sides_height"] = int(drawer_height - drawer_height / 5) if int(drawer_height - drawer_height / 5) >= MIN_CUTTING_HEIGHT else MIN_CUTTING_HEIGHT
        parts_dimensions["drawer_sides_thickness"] = THICK_WOOD_THICKNESS

        # Drawer fronts and backs:
        parts_dimensions["drawer_fronts_and_backs_amount"] = 2 * number_of_components
        parts_dimensions["drawer_fronts_and_backs_width"] = width - 4 * THICK_WOOD_THICKNESS - 2 * DRAWER_WIDTH_RAIL
        parts_dimensions["drawer_fronts_and_backs_height"] = int(drawer_height - drawer_height / 5) if int(drawer_height - drawer_height / 5) >= MIN_CUTTING_HEIGHT else MIN_CUTTING_HEIGHT
        parts_dimensions["drawer_fronts_and_backs_thickness"] = THICK_WOOD_THICKNESS

        # Drawer front panel
        parts_dimensions["drawer_frontpanels_amount"] = number_of_components
        parts_dimensions["drawer_frontpanels_width"] = drawer_width
        parts_dimensions["drawer_frontpanels_height"] = drawer_height
        parts_dimensions["drawer_frontpanels_thickness"] = THIN_WOOD_THICKNESS

    return parts_dimensions


def create_build_plan(width, depth, height, cabinet_version, number_of_components, drawer_width=0, drawer_height=0, file_name=BUILD_PLAN_FILE_NAME):
    # Scale down width and height 1/12:
    width_scaled_down = width / 12
    height_scaled_down = height / 12
    wood_thickness_scaled_down = THICK_WOOD_THICKNESS / 12

    class PDF(FPDF):
        def header(self):
            # Logo:
            self.image("logo.png", 150, 8, 50)

        def footer(self):
            # Position cursor at 1.5 cm from bottom:
            self.set_y(-15)
            # Setting font: helvetica 8
            self.set_font("helvetica", "", 10)
            # Page number:
            self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title:
    pdf.set_font("helvetica", "B", 20)
    pdf.cell(40, 20, "Cabinet Build Plan", ln=True)

    # Set font for further text:
    pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
    pdf.set_font("DejaVu", "", 16)

    # Print cabinet model:
    pdf.cell(0, 12, f"Cabinet model: {cabinet_version}", ln=True)

    # Width and depth:
    pdf.multi_cell(0, 10, f"↔ Width: {width} mm | ↗ Depth: {depth} mm", 0, 0)

    # Save top coordinate:
    top = pdf.y

    # Define x position of next cell:
    offset = pdf.x + width_scaled_down + 2

    # Draw cabinet shape:
    pdf.multi_cell(width_scaled_down, height_scaled_down, "", 1, 0)

    # Reset y coordinate:
    pdf.y = top

    # Move to computed offset:
    pdf.x = offset

    # Height:
    pdf.multi_cell(0, height_scaled_down, f"↕ Height: {height} mm", 0, 0)

    def setup_handle(cabinet_version):
        if cabinet_version.startswith("s"):
            if width_scaled_down < 60:
                handle_height = width_scaled_down / 5
            elif height_scaled_down < 60:
                handle_height = height_scaled_down / 5
            else:
                handle_height = 15
            handle_width = handle_height / 3
        else:
            if width_scaled_down < 60:
                handle_height = height_scaled_down / 35
            elif height_scaled_down < 60:
                handle_height = width_scaled_down / 35
            else:
                handle_height = 2.5
            handle_width = 3 * handle_height
        return handle_width, handle_height

    if cabinet_version.startswith("s"):
        # Scale down door spacing width and height 1/12:
        door_spacing_scaled_down = DOOR_SPACING / 12

        # Draw cabinet door:
        door_width_scaled_down = width_scaled_down - door_spacing_scaled_down
        door_height_scaled_down = height_scaled_down - door_spacing_scaled_down
        pdf.rect(pdf.x + wood_thickness_scaled_down + door_spacing_scaled_down, pdf.y - height_scaled_down + wood_thickness_scaled_down + door_spacing_scaled_down, door_width_scaled_down - 2 * wood_thickness_scaled_down, door_height_scaled_down - wood_thickness_scaled_down * 2)

        # Draw cabinet door handle:
        handle_width, handle_height = setup_handle(cabinet_version)
        if cabinet_version == "sl":
            x = pdf.x + width_scaled_down - wood_thickness_scaled_down - door_spacing_scaled_down - 2 * handle_width
        else:
            x = pdf.x + wood_thickness_scaled_down + door_spacing_scaled_down + handle_width
        pdf.rect(x, pdf.y - height_scaled_down / 2 - handle_height / 2, handle_width, handle_height)
    else:
        # Scale down drawer front width and drawer front height 1/12:
        if number_of_components > 0:
            drawer_width_scaled_down = drawer_width / 12
            drawer_height_scaled_down = drawer_height / 12
            side_spacing_scaled_down = (width_scaled_down - 2 * wood_thickness_scaled_down - drawer_width_scaled_down) / 2
            vertical_spacing_scaled_down = (height_scaled_down - 2 * wood_thickness_scaled_down - number_of_components * drawer_height_scaled_down) / (number_of_components + 1)

            # Draw drawers:
            top += wood_thickness_scaled_down + vertical_spacing_scaled_down
            for i in range(number_of_components):
                pdf.rect(pdf.x + wood_thickness_scaled_down + side_spacing_scaled_down, top, drawer_width_scaled_down, drawer_height_scaled_down)
                top += vertical_spacing_scaled_down + drawer_height_scaled_down

            # Draw drawer handles:
            handle_width, handle_height = setup_handle(cabinet_version)
            for i in range(number_of_components):
                pdf.rect(pdf.x + wood_thickness_scaled_down + side_spacing_scaled_down + drawer_width_scaled_down / 2 - handle_width / 2, top - height_scaled_down + wood_thickness_scaled_down + wood_thickness_scaled_down + vertical_spacing_scaled_down + drawer_height_scaled_down / 2 - handle_height / 2, handle_width, handle_height)
                top += vertical_spacing_scaled_down + drawer_height_scaled_down

    # Empty line break:
    pdf.cell(0, 10, "", ln=True)

    if cabinet_version.startswith("s"):
        component_name = "shelves"
        if cabinet_version == "sl":
            description_suffix = " and a left hand door (door handle on the right)"
        else:
            description_suffix = " and right hand door (door handle on the left)"
    else:
        component_name = "drawers"
        description_suffix = ""

    # Print cabinet configuration:
    pdf.set_top_margin(40)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Configuration:", ln=True)
    pdf.set_font("DejaVu", "", 16)
    pdf.cell(0, 7, f"- Cabinet with {component_name}" + description_suffix, ln=True)
    pdf.cell(0, 10, f"- Number of {component_name}: {number_of_components}", ln=True)

    # Empty line break:
    pdf.cell(0, 10, "", ln=True)

    def draw_piece(width, height, text):
        pdf.set_font("DejaVu", "", 16)
        pdf.cell(0, 10, text, ln=True)
        pdf.multi_cell(0, 10, f"↔ Width: {width} mm", 0, 0)
        width_scaled_down = width / 24
        height_scaled_down = height / 24

        # Save top coordinate:
        top = pdf.y

        # Define x position of next cell:
        offset = pdf.x + width_scaled_down + 2

        # Draw piece:
        pdf.multi_cell(width_scaled_down, height_scaled_down, "", 1, 0)

        # Reset y coordinate:
        pdf.y = top

        # Move to computed offset:
        pdf.x = offset

        pdf.multi_cell(0, height_scaled_down, f"↕ Height: {height} mm", 0, 0)

        # Empty line break:
        pdf.ln(0.5)

    # Print needed pieces:
    parts_dimensions = calculate_needed_parts(width, depth, height, cabinet_version, number_of_components, drawer_width, drawer_height)
    pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Parts:", ln=True)
    draw_piece(parts_dimensions["bottom_and_top_width"], parts_dimensions["bottom_and_top_height"], f"- {parts_dimensions['bottom_and_top_amount']}x top/bottom ({parts_dimensions['bottom_and_top_thickness']} mm thickness):")
    draw_piece(parts_dimensions["sides_width"], parts_dimensions["sides_height"], f"- {parts_dimensions['sides_amount']}x sides ({parts_dimensions['sides_thickness']} mm thickness):")
    draw_piece(parts_dimensions["back_width"], parts_dimensions["back_height"], f"- {parts_dimensions['back_amount']}x back ({parts_dimensions['back_thickness']} mm thickness):")

    if cabinet_version.startswith("s"):
        draw_piece(parts_dimensions["door_width"], parts_dimensions["door_height"], f"- {parts_dimensions['door_amount']}x door ({parts_dimensions['door_thickness']} mm thickness):")
        draw_piece(parts_dimensions["shelves_width"], parts_dimensions["shelves_height"], f"- {parts_dimensions['shelves_amount']}x shelves ({parts_dimensions['shelves_thickness']} mm thickness):")
    else:
        draw_piece(parts_dimensions["drawer_bottoms_width"], parts_dimensions["drawer_bottoms_height"], f"- {parts_dimensions['drawer_bottoms_amount']}x drawer bottoms ({parts_dimensions['drawer_bottoms_thickness']} mm thickness):")
        draw_piece(parts_dimensions["drawer_sides_width"], parts_dimensions["drawer_sides_height"], f"- {parts_dimensions['drawer_bottoms_amount']}x drawer sides ({parts_dimensions['drawer_sides_thickness']} mm thickness):")
        draw_piece(parts_dimensions["drawer_fronts_and_backs_width"], parts_dimensions["drawer_fronts_and_backs_height"], f"- {parts_dimensions['drawer_fronts_and_backs_amount']}x drawer fronts/backs ({parts_dimensions['drawer_fronts_and_backs_thickness']} mm thickness):")
        draw_piece(parts_dimensions["drawer_frontpanels_width"], parts_dimensions["drawer_frontpanels_height"], f"- {parts_dimensions['drawer_frontpanels_amount']}x drawer front panels ({parts_dimensions['drawer_frontpanels_thickness']} mm thickness):")

    # Create PDF file:
    pdf.output(file_name)


if __name__ == "__main__":
    main()
