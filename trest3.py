from xml.etree.ElementTree import Element, SubElement, tostring


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
    combinations = [
        ("lf.svg", "transparent", "transparent", "blue"),  # (lf)
        ("lf_mid.svg", "transparent", "yellow", "blue"),  # (lf, mid)
        ("lf_rf.svg", "red", "transparent", "blue"),  # (lf, rf)
        ("lf_mid_rt.svg", "red", "yellow", "blue"),  # (lf, mid, rt)
        ("rt.svg", "red", "transparent", "transparent"),  # (rt)
        ("rt_mid.svg", "red", "yellow", "transparent"),  # (rt, mid)
        ("mid.svg", "transparent", "yellow", "transparent")  # (mid)
    ]
    
    # Specify the path on your local machine where you want to save the SVG files
    save_path = "D:/MironovS/script/GitHub/MSL_MayaRename/core/resources/icon/"  # Change this path to your preferred location
    
    
    # Create and save SVGs for all combinations
    for file_name, left, mid, right in combinations:
        create_svg_combination(f"{save_path}{file_name}", left, mid, right)
    
    # Returning paths to the created SVGs
    print([save_path + file_name for file_name, _, _, _ in combinations])