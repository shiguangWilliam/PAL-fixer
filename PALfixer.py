import base64
import math

def rgb62rgb8(rgbData,reverse=False):
    r=int(rgbData[0:2],16)
    g=int(rgbData[2:4],16)
    b=int(rgbData[4:6],16)
    if(reverse==False):    
        fector=255/63
    else:
        fector=63/255
    r=int(r*fector)
    g=int(g*fector)
    b=int(b*fector)
    #print(r,g,b)
    res=format(r,'02x')+format(g,'02x')+format(b,'02x')
    return res            
    
def generate_pal_file(content_hex):
    # Constants for PAL file header
    signal = b"RIFF"
    filetype = b"PAL "     #4
    dataSignal = b"data"
    version = b"\x00\x03"  # Version 3
    

    # Convert hex string to bytes
    content_bytes = bytes.fromhex(content_hex)

    # Calculate dynamic file size and data size
    data_size = len(content_bytes)  # Each byte is represented by 2 hex characters
    colourBlock = data_size // 3  # Each color is 3 bytes
    print(colourBlock.to_bytes(2,"little"))
    rgbInfo=bytes()
    for i in range(colourBlock):
    #    print(rgb62rgb8(content_hex[i*6:i*6+6]))
        rgbInfo+=bytes.fromhex(rgb62rgb8(content_hex[i*6:i*6+6]))+b"\x00"
    file_size = 4 + 4 + len(filetype) + 4 + 4 + 4 + 2 + len(rgbInfo)
    data_size=len(rgbInfo)
    print(file_size)
    print(colourBlock)
    # Create PAL content
    palContent = signal + file_size.to_bytes(4, 'little') + filetype + dataSignal + data_size.to_bytes(4, 'little') + version + colourBlock.to_bytes(2,"little") + rgbInfo

    return palContent

def MSpal2WSoal(content_hex):
    print(content_hex[44:48])
    colourBlock=int(content_hex[46:48]+content_hex[44:46],16)
    print(colourBlock)
    rgb_Info=content_hex[48:]
    palContent=bytes()
    for i in range(colourBlock):
        rgba=rgb_Info[i*8:i*8+8]
        rgb=rgb62rgb8(rgba,True)
        #print(rgb)
        palContent+=bytes.fromhex(rgb)
    if colourBlock<256:
        palContent+=b"\x00\x00\x00"*(256-colourBlock)  
    with open(output_pal_path,"wb") as wsPal:
            wsPal.write(palContent)

def GenPSpal(content_hex,reverse=False):
    if reverse==False:
        pal_content = generate_pal_file(content_hex)

        # Write the new PAL content to the output file
        with open(output_pal_path, "wb") as test:
            test.write(pal_content)
    else:
         MSpal2WSoal(content_hex)     #GEN ws pal  
                
# Replace with the actual path to your PAL file
input_pal_path = ""
output_pal_path = ""

# Read the original PAL file and convert its content to hex
with open(input_pal_path, "rb") as pal:
    content_hex = pal.read().hex()

# Generate the new PAL content
GenPSpal(content_hex,reverse=False)
