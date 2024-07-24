# test.py

import unittest
from app import DicomReader, JpegReader

class TestImageReaders(unittest.TestCase):
    def test_dicom_reader(self):
        dicom_reader = DicomReader()
        img_array, img2show = dicom_reader.read_file('ejemplo.dcm')
        # Realiza las aserciones según lo esperado
        self.assertIsNotNone(img_array)
        self.assertIsNotNone(img2show)

    def test_jpeg_reader(self):
        jpeg_reader = JpegReader()
        img_array, img2show = jpeg_reader.read_file('ejemplo2.jpeg')
        # Realiza las aserciones según lo esperado
        self.assertIsNotNone(img_array)
        self.assertIsNotNone(img2show)
    def tearDown(self):
        print("¡Las pruebas se ejecutaron exitosamente!")

# Ejecutar las pruebas
if __name__ == '__main__':
    unittest.main()


#python -m unittest test.py
#para poner en terminal y realizar test