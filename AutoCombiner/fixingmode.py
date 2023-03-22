from PIL import Image


fix = Image.open(fr"./classes/class1/class1_4.png")
print(fix.mode)
fixed= fix.convert("RGBA")
fixed.save(fr"./classes/class1/class1_4.png")