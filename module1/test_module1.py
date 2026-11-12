"""
Module 1 - Image Quality Assessment

End-to-End Test
"""

from quality_analyzer import QualityAnalyzer


def main():

    ###########################################################
    # PDF Path
    ###########################################################

    pdf_path = "module1/ilovepdf_merged.pdf"

    ###########################################################
    # Create Analyzer
    ###########################################################

    analyzer = QualityAnalyzer()

    ###########################################################
    # Analyze PDF
    ###########################################################
    document = analyzer.analyze(pdf_path)

    report = document.quality_report

    print("\n========== MODULE 1 REPORT ==========\n")

    print(f"Total Pages : {report['total_pages']}\n")


    for page in report["pages"]:

        print(f"Page {page['page_number']}")

        print(f"Status       : {page['status']}")

        print(f"Blur         : {page['blur']:.2f}")

        print(f"Brightness   : {page['brightness']:.2f}")

        print(f"Contrast     : {page['contrast']:.2f}")

        print(f"Noise        : {page['noise']:.2f}")

        print(f"Shadow       : {page['shadow_percentage']:.2f}%")

        print(f"Resolution   : {page['width']} x {page['height']}")

        print("\nChecks")

        for key, value in page["checks"].items():

            status = "PASS" if value else "FAIL"

            print(f"   {key:12} : {status}")

        print("-" * 50)

    print("\nQuality report saved successfully.")

    print("Visualization images generated.")

    print()


if __name__ == "__main__":

    main()