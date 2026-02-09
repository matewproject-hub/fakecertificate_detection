from pyzbar.pyzbar import decode
from PIL import Image
from pdf2image import convert_from_bytes
import io

def extract_qr(data:bytes):
    try:
        image=Image.open(io.BytesIO(data))
        decode=decode(image)
        if decode:
            return decode[0].data.decode("utf-8")
    except:
        pass
    
    try:
        pages=convert_from_bytes(data)
        first_page=pages[0]

        decode=decode(first_page)
        if decode:
            return decode[0].data.decode("utf-8")
    except:
        pass
    return None
    
    
