# app/services/dicom_service.py
import pydicom
from pydicom.errors import InvalidDicomError
import os

class DicomValidationEngine:
    def __init__(self):
        # 定义必需的 DICOM Tag
        self.required_tags = [
            'PatientID',
            'PatientName',
            'StudyInstanceUID',
            'SeriesInstanceUID',
            'Modality'
        ]

    def validate_and_extract(self, file_path):
        result = {
            "file": os.path.basename(file_path),
            "status": "FAIL",
            "validation_details": {},
            "metadata": None,
            "error_reason": None
        }

        try:
            # 1. 验证文件格式 (File Format)
            ds = pydicom.dcmread(file_path)
            result["validation_details"]["DICOM_Format"] = "PASS"
            
            # 2. 验证 Transfer Syntax (Meta 信息)
            if hasattr(ds.file_meta, 'TransferSyntaxUID'):
                result["validation_details"]["Transfer_Syntax"] = "PASS"
            else:
                result["validation_details"]["Transfer_Syntax"] = "FAIL"
                raise ValueError("Missing Transfer Syntax UID")

            # 3. 验证必填字段完整性 (Required Tags)
            extracted_data = {}
            for tag in self.required_tags:
                if hasattr(ds, tag) and getattr(ds, tag):
                    result["validation_details"][tag] = "PASS"
                    # pydicom 读取的人名可能是特殊的 PersonName 对象，需要转字符串
                    extracted_data[tag] = str(getattr(ds, tag))
                else:
                    result["validation_details"][tag] = "FAIL"
                    raise ValueError(f"Missing required tag: {tag}")
            
            # 验证全部通过
            result["status"] = "PASS"
            result["metadata"] = extracted_data
            
        except InvalidDicomError:
            result["error_reason"] = "Not a valid DICOM file"
            result["validation_details"]["DICOM_Format"] = "FAIL"
        except ValueError as e:
            result["error_reason"] = str(e)
        except Exception as e:
            result["error_reason"] = f"Unexpected error: {str(e)}"
            
        return result