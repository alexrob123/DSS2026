import importlib.util
import tempfile
import zipfile
from pathlib import Path

import click
import pandas as pd

from xmldtd.utils import validate

STUDENTS_CSV = Path("./students.csv")
SUBMISSION_DIR = Path("./submission")
EVALUATION_DIR = Path("./evaluation")
MAP_TP = {1: "tp-xml-dtd", 2: "tp-dom"}


# Utils
# --------------------------------------------------------------------------------


def get_students(csv):
    df = pd.read_csv(csv)
    name_col = "Name" if "Name" in df else df.columns[0]
    return df[name_col].dropna().astype(str).tolist()


def failure_situation(row, num_exos, index=None):
    if index is not None:
        row[index] = 0
    else:
        for exo in range(1, num_exos + 1):
            row[exo] = 0
    return row


# class Evaluation:
#     def __init__(self, tp, num_exos, ext):
#         self.tp = tp
#         self.num_exos = num_exos
#         self.ext = ext

#         self.students = self._get_students(STUDENTS_CSV)
#         self.results = []


#     def _check_submsission(self, student, tp, ext):
#         expected_path = SUBMISSION_DIR / MAP_TP[tp] / f"{student}.{ext}"
#         return expected_path.exists(), expected_path

#     def _failure_situation(self, row, num_exos, index=None):
#         if index is not None:
#             row[index] = 0
#         else:
#             for exo in range(1, num_exos + 1):
#                 row[exo] = 0
#         return row

#     def evaluation_loop(self, tp, ext):
#         for student in self.students:
#             print(f"Student {student}")
#             student_row = {"Name": student}

#             submission_flag, submission_path = self._check_submsission(
#                 student,
#                 tp=tp,
#                 ext=ext,
#             )

#             if not submission_flag:
#                 student_row = self._failure_situation(student_row, self.num_exos)
#                 print("\t No submission")

#             else:


# Evaluations
# --------------------------------------------------------------------------------


@click.group()
def main():
    """Main command group for evaluation."""


#################################################################################
#################################################################################
#################################################################################


@main.command()
@click.option(
    "--num-exos",
    "-n",
    type=int,
    default=5,
    help="Number of exercises to evaluate.",
)
def tp_xml_dtd(num_exos=5):
    """
    Evaluates student submissions for XML/DTD exercises.
    The hw_dir should contain zipped folders for each student, each containing
    their XML and DTD files for the exercises under format `exo_{i}.ext` (e.g.,
    exo_1.xml, exo_1.dtd).
    """

    input_dir = SUBMISSION_DIR / "tp-xml-dtd"
    output_path = EVALUATION_DIR / "eval_xml_dtd.csv"

    students = get_students(str(STUDENTS_CSV))

    # Evaluation loop
    results = []

    for student in students:
        print(f"Student {student}")

        student_row = {"Name": student}
        student_zip = input_dir / f"{student}.zip"

        if not student_zip.exists():
            student_row = failure_situation(student_row, num_exos)
            print("\t No zip")

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
                                print(f"\t Exo {exo} OK: {valid}")
                            except Exception:
                                student_row = failure_situation(
                                    student_row, num_exos, index=exo
                                )
                                print(f"\t Exo {exo} validation error")
                        else:
                            student_row[exo] = 0
                            print(f"\t Exo {exo} missing files")

                except zipfile.BadZipFile:
                    student_row = failure_situation(student_row, num_exos, index=exo)
                    print(f"\t Bad zip file for student {student}")

        results.append(student_row)

    # Build and enrich df
    df = pd.DataFrame(results)
    df["Total"] = df[[exo for exo in range(1, num_exos + 1)]].sum(axis=1)

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Evaluation saved to {output_path}.")


#################################################################################
#################################################################################
#################################################################################


@main.command()
@click.option(
    "--num-exos",
    "-n",
    type=int,
    default=9,
    help="Number of exercises to evaluate.",
)
@click.option(
    "--ref-script",
    "--ref",
    "-r",
    "ref_script",
    type=click.Path(exists=True, file_okay=True, path_type=Path),
    help="Path to the reference implementation file (e.g., tp_dom_ref.py).",
)
@click.option(
    "--xml-file",
    "--test",
    "-t",
    "test_file",
    type=click.Path(exists=True, file_okay=True, path_type=Path),
    help="Path to the XML file used for testing student functions.",
)
def tp_dom(num_exos, ref_script, test_file):
    """
    Evaluates student submissions for DOM exercises.
    The hw_dir should contain py folders for each student, each containing
    their functions for the exercises under format `q{i}(xml_file)` (e.g.,
    q1(xml_file)).
    """

    input_dir = SUBMISSION_DIR / "tp-dom"
    output_path = EVALUATION_DIR / "eval_dom.csv"

    students = get_students(str(STUDENTS_CSV))

    # Load reference answers
    spec = importlib.util.spec_from_file_location("ref_module", ref_script)
    ref_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref_module)

    ref_answers = {}
    for i in range(1, num_exos + 1):
        func_name = f"q{i}"
        if hasattr(ref_module, func_name):
            ref_func = getattr(ref_module, func_name)
            ref_answers[i] = ref_func(str(test_file))
        else:
            print(f"Reference function {func_name} not found in {ref_script}.")
            ref_answers[i] = None

    # Evaluation loop
    results = []

    for student in students:
        print(f"Student {student}")

        student_row = {"Name": student}
        student_py = input_dir / f"{student}.py"

        if not student_py.exists():
            student_row = failure_situation(student_row, num_exos)
            print("\t No script found")

        else:
            spec = importlib.util.spec_from_file_location(
                f"{student}_module", student_py
            )
            student_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(student_module)

            for i in range(1, num_exos + 1):
                func_name = f"q{i}"
                if hasattr(student_module, func_name):
                    student_func = getattr(student_module, func_name)
                    try:
                        student_answer = student_func(str(test_file))
                        student_row[i] = 1 if student_answer == ref_answers[i] else 0
                        print(f"\t {func_name} OK: {student_answer == ref_answers[i]}")
                        if not student_answer == ref_answers[i]:
                            print(
                                f"\t\t Expected: \n{ref_answers[i]} \n Got: \n{student_answer}"
                            )

                    except Exception:
                        student_row = failure_situation(student_row, num_exos, index=i)
                        print(f"\t {func_name} execution error")
                else:
                    student_row[i] = 0
                    print(f"\t {func_name} not found")

        results.append(student_row)

    # Build and enrich df
    df = pd.DataFrame(results)
    df["Total"] = df[[exo for exo in range(1, num_exos + 1)]].sum(axis=1)

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Evaluation saved to {output_path}.")


#################################################################################
#################################################################################
#################################################################################


if __name__ == "__main__":
    main()
