from pathlib import Path

import pandas as pd

from xmldtd.utils import validate

# Config
# --------------------------------------------------------------------------------
hw_dir = Path("hw-tp-xml-dtd")
students_csv = Path("students.csv")
output_csv = Path("evaluation.csv")
num_exos = 5

# Load student names
# --------------------------------------------------------------------------------
students_df = pd.read_csv(students_csv)
name_col = "name" if "name" in students_df.columns else students_df.columns[0]
students = students_df[name_col].dropna().astype(str).tolist()

# Evaluation loop
# --------------------------------------------------------------------------------
results = []
for student in students:
    student_dir = hw_dir / student
    student_row = {"Name": student}

    if not student_dir.is_dir():
        for exo in range(1, num_exos + 1):
            student_row[exo] = 0
    else:
        for exo in range(1, num_exos + 1):
            xml_path = student_dir / f"exo_{exo}.xml"
            dtd_path = student_dir / f"exo_{exo}.dtd"

            if xml_path.is_file() and dtd_path.is_file():
                try:
                    valid = validate(str(xml_path), str(dtd_path))
                    student_row[exo] = 1 if valid else 0
                except Exception:
                    student_row[exo] = 0
            else:
                student_row[exo] = 0

    results.append(student_row)

# Build and enrich df
# --------------------------------------------------------------------------------
df = pd.DataFrame(results)
df["Total"] = df[[exo for exo in range(1, num_exos + 1)]].sum(axis=1)

# Save to CSV
# --------------------------------------------------------------------------------
df.to_csv(output_csv, index=False)
print(f"Evaluation saved to {output_csv}.")
