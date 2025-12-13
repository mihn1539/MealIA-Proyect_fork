from PIL import Image, ImageSequence

def make_transparent(img):
    datas = img.getdata()
    newData = []
    for item in datas:
        # Check if pixel is white (or very close to white)
        # item is usually (R, G, B) or (R, G, B, A)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0)) # Transparent
        else:
            newData.append(item)
    
    img = img.convert("RGBA")
    img.putdata(newData)
    return img

def process_gif(input_path, output_path):
    print(f"Opening {input_path}...")
    try:
        im = Image.open(input_path)
    except FileNotFoundError:
        print("Error: Input file not found.")
        return

    frames = []
    
    print("Processing frames...")
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert("RGBA")
        transparent_frame = make_transparent(frame)
        frames.append(transparent_frame)

    print(f"Saving to {output_path}...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=im.info.get('duration', 100),
        loop=im.info.get('loop', 0),
        disposal=2 # Clear background before next frame
    )
    print("Done!")

if __name__ == "__main__":
    process_gif("assets/animation1.gif", "assets/animation1_transparent.gif")
