from pdf_loader import PDFLoader

loader = PDFLoader()

images = loader.load("PDFReader_20260801_2348.pdf")

print(len(images))

print(images[0].shape)