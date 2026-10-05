"""
Build contact.vcf with your headshot embedded.
Edit the fields below, then run:  python make_vcard.py
"""
import base64, textwrap

FIRST, LAST = "Ben", "Luginbuhl"
TITLE   = "Sr. Scientific Software Developer - Materials Informatics"
ORG     = "Enthought"
PHONE   = "+15125361057"
EMAIL   = "bluginbuhl@enthought.com"
WEBSITE = "https://www.enthought.com"
LINKEDIN = "https://www.linkedin.com/in/benluginbuhl"
PHOTO   = "photo.jpg"   # set to None to skip

lines = [
    "BEGIN:VCARD", "VERSION:3.0",
    f"N:{LAST};{FIRST};;;", f"FN:{FIRST} {LAST}",
    f"ORG:{ORG}", f"TITLE:{TITLE}",
    f"TEL;TYPE=CELL:{PHONE}", f"EMAIL;TYPE=WORK:{EMAIL}",
    f"URL:{WEBSITE}", f"X-SOCIALPROFILE;TYPE=linkedin:{LINKEDIN}",
]
if PHOTO:
    b64 = base64.b64encode(open(PHOTO, "rb").read()).decode()
    # vCard lines are folded at 75 chars; continuation lines start with a space
    folded = textwrap.wrap("PHOTO;ENCODING=b;TYPE=JPEG:" + b64, 74)
    lines.append(folded[0])
    lines += [" " + f for f in folded[1:]]
lines.append("END:VCARD")

with open("contact.vcf", "w", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print("Wrote contact.vcf")