"""
Module 1 - Image Quality Assessment

Quality Analyzer

Main controller for Module 1.

Workflow

PDF
    ↓
PDF Loader
    ↓
Quality Metrics
    ↓
Quality Report
    ↓
Visualizer
    ↓
Return Document Object
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from document import Document
from page import Page

from pdf_loader import PDFLoader
from metrics import QualityMetrics
from quality_report import QualityReport
from visualizer import QualityVisualizer


class QualityAnalyzer:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.loader = PDFLoader()

        self.metrics = QualityMetrics()

        self.report = QualityReport()

        self.visualizer = QualityVisualizer()

    ###########################################################
    # Analyze PDF
    ###########################################################

    def analyze(self, pdf_path):

        """
        Analyze the quality of every page
        in the PDF.

        Parameters
        ----------
        pdf_path : str

        Returns
        -------
        Document
        """

        #######################################################
        # Create Document
        #######################################################

        document = Document(pdf_path=pdf_path)

        #######################################################
        # Load Pages
        #######################################################

        images = self.loader.load(pdf_path)

        #######################################################
        # Analyze Each Page
        #######################################################

        for page_number, image in enumerate(images, start=1):

            ###############################################
            # Create Page Object
            ###############################################

            page = Page(

                page_number=page_number,

                original_image=image

            )

            ###############################################
            # Calculate Metrics
            ###############################################

            metrics = self.metrics.evaluate(image)

            page.quality_metrics = metrics

            ###############################################
            # Add to Report
            ###############################################

            self.report.add_page(

                page_number,

                metrics

            )

            ###############################################
            # Visualization
            ###############################################

            visual = self.visualizer.draw(

                image,

                page_number,

                metrics

            )

            self.visualizer.save(

                page_number,

                visual

            )

            ###############################################
            # Add Page to Document
            ###############################################

            document.add_page(page)

        #######################################################
        # Save Quality Report
        #######################################################

        self.report.save()

        #######################################################
        # Store Report in Document
        #######################################################

        document.quality_report = self.report.build()

        #######################################################
        # Return Document
        #######################################################

        return document