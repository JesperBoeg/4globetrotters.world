#!/usr/bin/env python
"""Convert the selected Ella/Arugam/Yala/Negombo photos to web JPG.

- longest side 1200px (2400 for panoramas), q85 progressive
- bake EXIF orientation into pixels, then STRIP the orientation tag (274)
  while KEEPING the DateTime timestamp
- descriptive output names, into wp-content/uploads/2026/07/
"""
import os
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

SRC = r"G:\My Drive\Pictures\2026 Sri Lanka Ella & Arugam Bay"
OUT = r"c:\Users\agile\VSCode projects\4globetrotters\option-b-static\site\wp-content\uploads\2026\07"

# source filename -> output basename (no extension)
MAP = {
    # ---- POST 1: ELLA ----
    "P1040477.JPG": "ella-train-station-morning",
    "IMG_7273.heic": "ella-train-doorway-view",
    "IMG_7299.heic": "ella-train-landscape",
    "IMG_7305.heic": "ella-train-hills",
    "IMG_7337.heic": "ella-train-tea-slopes",
    "IMG_7344.HEIC": "ella-arrival-guesthouse-view",
    "P1040484.JPG": "ella-little-adams-trail",
    "P1040492.JPG": "ella-little-adams-climb",
    "P1040496.JPG": "ella-little-adams-summit-family",
    "P1040501.JPG": "ella-little-adams-view",
    "IMG_7379.HEIC": "ella-town",
    "IMG_7453.heic": "ella-nine-arches-bridge",
    "IMG_7462.heic": "ella-nine-arches-frisbee",
    "IMG_7468.heic": "ella-nine-arches-train",
    "IMG_7518.heic": "ella-dinner-curry",
    "P1040506.JPG": "ella-rock-tracks-dawn",
    "P1040511.JPG": "ella-rock-trail",
    "P1040514.JPG": "ella-rock-climb",
    "P1040522.JPG": "ella-rock-noah-jesper",
    "P1040526.JPG": "ella-rock-summit-view",
    "P1040528.JPG": "ella-rock-summit-family",
    "P1040533.JPG": "ella-rock-noah-discgolf",
    "IMG_7537.HEIC": "ella-rock-descent",
    # ---- POST 2: ARUGAM BAY ----
    "IMG_7550.HEIC": "arugam-drive-elephant",
    "IMG_7555.HEIC": "arugam-drive-roadside",
    "IMG_7580.HEIC": "arugam-drive-elephant2",
    "20260801_105628 (1).jpg": "arugam-clinic-toe",
    "20260801_123159.jpg": "arugam-beach-arrival",
    "P1040559.JPG": "arugam-surf-vitus-ride",
    "P1040563.JPG": "arugam-surf-vitus-standing",
    "P1040589.JPG": "arugam-surf-jesper",
    "P1040626.JPG": "arugam-surf-beach",
    "P1040664.JPG": "arugam-surf-vitus-long-ride",
    "IMG_7295.MOV": "_video_arugam",  # video, not converted here
    "20260804_135749.jpg": "arugam-pizza-noah",
    "20260804_172131.jpg": "arugam-noah-disc-beach",
    # ---- POST 3: YALA & NEGOMBO ----
    "20260805_054318.jpg": "yala-safari-dawn-queue",
    "P1040705.JPG": "yala-safari-jeep",
    "P1040711.JPG": "yala-safari-buffalo",
    "P1040715.JPG": "yala-safari-elephant",
    "P1040721.JPG": "yala-safari-peacock",
    "P1040732.JPG": "yala-safari-leopard-tree",
    "P1040740.JPG": "yala-safari-crocodile",
    "P1040744.JPG": "yala-safari-deer",
    "P1040751.JPG": "yala-safari-birds",
    "P1040752.JPG": "yala-safari-landscape",
    "P1040756.JPG": "yala-homestay-paddies",
    "P1040759.JPG": "negombo-pool",
    "P1040763.JPG": "negombo-garden",
    "P1040767.JPG": "negombo-spices",
}

PANO = set()  # add basenames here if any are panoramas

os.makedirs(OUT, exist_ok=True)


def clean_exif(src_img):
    ex = src_img.getexif()
    if 274 in ex:
        del ex[274]
    return ex.tobytes() if len(ex) else None


def convert(src_name, out_base):
    src = os.path.join(SRC, src_name)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    longest = 2400 if out_base in PANO else 1200
    im.thumbnail((longest, longest), Image.LANCZOS)
    exif = clean_exif(Image.open(src))
    out = os.path.join(OUT, out_base + ".jpg")
    kw = dict(quality=85, optimize=True, progressive=True)
    if exif:
        kw["exif"] = exif
    im.save(out, "JPEG", **kw)
    w, h = im.size
    return out, w, h, round(w / h, 4)


def main():
    print("name,w,h,ar")
    for src_name, out_base in MAP.items():
        if out_base.startswith("_video"):
            continue
        try:
            out, w, h, ar = convert(src_name, out_base)
            print(f"{out_base}.jpg,{w},{h},{ar}")
        except Exception as e:
            print(f"ERROR {src_name}: {e}")


if __name__ == "__main__":
    main()
