from fontTools.ttLib import TTFont

# Load the TTF font
font = TTFont('font.ttf')

# Print all table tags
print("Tables in the font:")
for table in font.keys():
    print(table)
