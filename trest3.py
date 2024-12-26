from xml.etree.ElementTree import Element, SubElement, tostring


def create_svg_combination_circle(file_name, left_color, mid_color, right_color):
	width = 25
	height = 25
	circle_radius = width // 6  # Радиус круга (1/6 ширины)
	circle_spacing = width // 3  # Расстояние между центрами кругов
	
	svg = Element('svg', xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height))
	
	# Левый круг
	SubElement(svg, 'circle', cx=str(circle_radius), cy=str(height // 2), r=str(circle_radius), fill=left_color)
	# Средний круг
	SubElement(svg, 'circle', cx=str(circle_spacing + circle_radius), cy=str(height // 2), r=str(circle_radius),
	           fill=mid_color)
	# Правый круг
	SubElement(svg, 'circle', cx=str(2 * circle_spacing + circle_radius), cy=str(height // 2), r=str(circle_radius),
	           fill=right_color)
	
	# Save the SVG to a file
	with open(file_name, "wb") as f:
		f.write(tostring(svg))
		
# Function to create a single SVG with three colored bars based on input
def create_svg_combination(file_name, left_color, mid_color, right_color):
	width = 25
	height = 25
	bar_width = width // 3
	
	svg = Element('svg', xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height))
	SubElement(svg, 'rect', x="0", y="0", width=str(bar_width), height=str(height), fill=left_color)
	SubElement(svg, 'rect', x=str(bar_width), y="0", width=str(bar_width), height=str(height), fill=mid_color)
	SubElement(svg, 'rect', x=str(bar_width * 2), y="0", width=str(bar_width), height=str(height), fill=right_color)
	
	# Save the SVG to a file
	with open(file_name, "wb") as f:
		f.write(tostring(svg))

if __name__ == "__main__":
    # Colors for the combinations
    lf_color  = "#FF6F61" # #C0C0C0
    mid_color = "#FFD25A" # #FFD700
    rt_color  = "#8FD14F" # #CD7F32
    
    combinations = [
        ("lf.svg", "transparent", "transparent", lf_color),  # (lf)
        ("lf_mid.svg", "transparent", mid_color, lf_color),  # (lf, mid)
        ("lf_rf.svg", rt_color, "transparent", lf_color),  # (lf, rf)
        ("lf_mid_rt.svg", rt_color, mid_color, lf_color),  # (lf, mid, rt)
        ("rt.svg", rt_color, "transparent", "transparent"),  # (rt)
        ("rt_mid.svg", rt_color, mid_color, "transparent"),  # (rt, mid)
        ("mid.svg", "transparent", mid_color, "transparent")  # (mid)
    ]
    
    # Specify the path on your local machine where you want to save the SVG files
    save_path = "D:/MironovS/script/GitHub/MSL_MayaRename/core/resources/icon/"  # Change this path to your preferred location
    
    
    # Create and save SVGs for all combinations
    for file_name, left, mid, right in combinations:
        create_svg_combination_circle(f"{save_path}{file_name}", left, mid, right)
    
    # Returning paths to the created SVGs
    print([save_path + file_name for file_name, _, _, _ in combinations])