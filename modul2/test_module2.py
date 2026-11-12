"""
Module 2 - Image Preprocessing

End-to-End Test
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
print(project_root)
print(sys.path)

sys.path.append(str(project_root))

print((project_root / "module1").exists())


from module1.quality_analyzer import QualityAnalyzer
from preprocessor import Preprocessor


def main():

    ###########################################################
    # PDF Path
    ###########################################################

    pdf_path = "module1/ilovepdf_merged.pdf"

    ###########################################################
    # Module 1
    ###########################################################

    print("\nRunning Module 1...")

    analyzer = QualityAnalyzer()

    document = analyzer.analyze(pdf_path)

    ###########################################################
    # Module 2
    ###########################################################

    print("Running Module 2...")

    preprocessor = Preprocessor()

    document = preprocessor.process(document)

    ###########################################################
    # Print Summary
    ###########################################################

    print()

    print("=" * 60)
    print("PREPROCESSING SUMMARY")
    print("=" * 60)

    print()

    print(f"PDF : {document.pdf_path}")

    print(f"Pages : {document.total_pages}")

    print(f"Preprocessed PDF : {document.preprocessed_pdf_path}")

    print()

    for page in document.pages:

        print("-" * 60)

        print(f"Page {page.page_number}")

        print("-" * 60)

        report = page.preprocessing_report

        print()

        print("Deskew")

        print(report["deskew"])

        print()

        print("Denoise")

        print(report["denoise"])

        print()

        print("Contrast")

        print(report["contrast"])

        print()

        print("Shadow Removal")

        print(report["shadow_removal"])

        print()

        print("Thresholding")

        print(report["thresholding"])

        print()

        print(
            "Preprocessed Image :",
            page.preprocessed_image.shape
        )

        print()

    print("=" * 60)

    print("Module 2 completed successfully.")

    print("=" * 60)

    print()

    print("Generated Files")

    print("---------------------------")

    print(document.preprocessed_pdf_path)

    print("output/module_2/preprocessing_report.json")

    print("output/module_2/pages/")

    print()


if __name__ == "__main__":

    main()