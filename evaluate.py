import tempfile
import zipfile
from pathlib import Path

import click
import pandas as pd

from xmldtd.utils import validate

# Utils
# --------------------------------------------------------------------------------


def failure_situation(student_row, num_exos, index=None):
    if index is not None:
        student_row[index] = 0
    else:
        for exo in range(1, num_exos + 1):
            student_row[exo] = 0
    return student_row


# Evaluations
# --------------------------------------------------------------------------------


def evaluate_xml_dtd(students, hw_dir, output_csv, num_exos=5):
    """
    Evaluates student submissions for XML/DTD exercises.
    The hw_dir should contain zipped folders for each student, each containing
    their XML and DTD files for the exercises under format `exo_{i}.ext` (e.g.,
    exo_1.xml, exo_1.dtd).
    """
    # Evaluation loop
    results = []

    for student in students:
        student_row = {"Name": student}
        student_zip = hw_dir / f"{student}.zip"

        if not student_zip.exists():
            student_row = failure_situation(student_row, num_exos)
            print(f"Student {student} | No zip")

        else:
            for exo in range(1, num_exos + 1):
                xml_name = f"exo_{exo}.xml"
                dtd_name = f"exo_{exo}.dtd"

                try:
                    with (
                        zipfile.ZipFile(student_zip, "r") as zf,
                        tempfile.TemporaryDirectory() as tmpdir,
                    ):
                        zf.extractall(tmpdir)
                        extracted_root = Path(tmpdir)

                        xml_matches = list(extracted_root.rglob(xml_name))
                        dtd_matches = list(extracted_root.rglob(dtd_name))

                        if xml_matches and dtd_matches:
                            xml_path = xml_matches[0]
                            dtd_path = dtd_matches[0]
                            try:
                                valid = validate(str(xml_path), str(dtd_path))
                                student_row[exo] = 1 if valid else 0
                            except Exception:
                                student_row = failure_situation(
                                    student_row, num_exos, index=exo
                                )
                                print(f"Student {student} | Exo {exo} validation error")
                        else:
                            student_row[exo] = 0
                            print(f"Student {student} | Exo {exo} missing files")

                except zipfile.BadZipFile:
                    student_row = failure_situation(student_row, num_exos, index=exo)
                    print(f"Student {student} | Bad zip file")

        results.append(student_row)

    # Build and enrich df
    df = pd.DataFrame(results)
    df["Total"] = df[[exo for exo in range(1, num_exos + 1)]].sum(axis=1)

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Evaluation saved to {output_csv}.")


#################################################################################
#################################################################################
#################################################################################


@click.command()
@click.option(
    "--students",
    "-s",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    default="./students.csv",
    help="CSV file with student names.",
)
@click.option(
    "--hw-dir",
    "--dir",
    "-h",
    "-d",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Directory containing student submissions (homework dir).",
)
@click.option(
    "--tp",
    type=click.INT,
    help="TP identifier (used to name output CSV).",
)
def main(students, hw_dir, tp):
    out_csv = Path("./evaluation") / f"{hw_dir.name}.csv"
    out_csv.parent.mkdir(exist_ok=True)

    students_df = pd.read_csv(students)
    name_col = "Name" if "Name" in students_df else students_df.columns[0]
    students = students_df[name_col].dropna().astype(str).tolist()

    if tp == 1:
        evaluate_xml_dtd(students, hw_dir, out_csv, num_exos=5)
    else:
        raise NotImplementedError(f"TP {tp} evaluation is not implemented.")


if __name__ == "__main__":
    main()
