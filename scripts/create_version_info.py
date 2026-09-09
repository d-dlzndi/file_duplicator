import os
from pathlib import Path


version = os.environ["VERSION"]

parts = version.split(".")

if len(parts) != 3 or not all(part.isdigit() for part in parts):
    raise ValueError(f"Unsupported version format: {version}")

major, minor, patch = map(int, parts)

version_info = f"""\
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({major}, {minor}, {patch}, 0),
        prodvers=({major}, {minor}, {patch}, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'DDL'),
                        StringStruct('FileDescription', 'File Duplicator'),
                        StringStruct('FileVersion', '{version}'),
                        StringStruct('InternalName', 'File Duplicator'),
                        StringStruct('OriginalFilename', 'File-Duplicator.exe'),
                        StringStruct('ProductName', 'File Duplicator'),
                        StringStruct('ProductVersion', '{version}'),
                    ]
                )
            ]
        ),
        VarFileInfo(
            [VarStruct('Translation', [1033, 1200])]
        )
    ]
)
"""

output = Path("build/version_info.txt")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(version_info, encoding="utf-8")

print(f"Created: {output}")
print(f"Version: {version}")