from PIL import Image
image = Image.open(".png")
new= image.resize((1240,1240), Image.NEAREST)
new.save("./as.png")