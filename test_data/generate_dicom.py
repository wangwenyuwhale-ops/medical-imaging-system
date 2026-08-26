# test_data/generate_dicom.py
import os
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import numpy as np

# 确保目录存在
os.makedirs('valid', exist_ok=True)
os.makedirs('invalid', exist_ok=True)
os.makedirs('boundary', exist_ok=True)

def create_base_dicom(filepath, patient_id="P00001"):
    """生成一个基础的、完全合法的 DICOM 数据集"""
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # preamble 必须是 128 字节的 0，这是 DICOM 标准规定的头部
    ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # 设置我们要求的必需字段 (Tags)
    ds.PatientName = "Test^QA"
    ds.PatientID = patient_id
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.Modality = "CT"

    # 添加一个合法的假图像矩阵，防止更深度的解析器报错
    ds.Rows = 128
    ds.Columns = 128
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    # 生成全黑的 128x128 图像
    pixel_array = np.zeros((128, 128), dtype=np.uint16)
    ds.PixelData = pixel_array.tobytes()

    return ds

def generate_test_suite():
    print("开始生成 DICOM 测试用例数据...")

    # 1. 生成正常数据 (Valid)
    valid_ct_path = os.path.join('valid', 'valid_ct.dcm')
    ds_valid = create_base_dicom(valid_ct_path, "P_VALID_01")
    pydicom.filewriter.dcmwrite(valid_ct_path, ds_valid)
    print(f"✓ 生成正常数据: {valid_ct_path}")

    # 2. 生成缺失 PatientID 的数据 (Invalid)
    missing_id_path = os.path.join('invalid', 'missing_patient_id.dcm')
    ds_missing_id = create_base_dicom(missing_id_path)
    del ds_missing_id.PatientID  # 故意删除必需的 Tag
    pydicom.filewriter.dcmwrite(missing_id_path, ds_missing_id)
    print(f"✓ 生成异常数据 (缺失PatientID): {missing_id_path}")

    # 3. 生成缺失 Study UID 的数据 (Invalid)
    missing_study_path = os.path.join('invalid', 'missing_study_uid.dcm')
    ds_missing_study = create_base_dicom(missing_study_path)
    del ds_missing_study.StudyInstanceUID
    pydicom.filewriter.dcmwrite(missing_study_path, ds_missing_study)
    print(f"✓ 生成异常数据 (缺失StudyUID): {missing_study_path}")

    # 4. 生成损坏的 DICOM 数据 (Corrupted)
    # 直接写入乱码数据，模拟文件损坏、传输中断的情况
    corrupted_path = os.path.join('invalid', 'corrupted.dcm')
    with open(corrupted_path, 'wb') as f:
        f.write(b"This is not a real dicom file, just random binary garbage \x00\xFF\x88")
    print(f"✓ 生成异常数据 (文件损坏): {corrupted_path}")

    # 5. 生成非 DICOM 的伪装文件 (Invalid)
    fake_jpg_path = os.path.join('invalid', 'not_dicom.jpg')
    with open(fake_jpg_path, 'w') as f:
        f.write("I am actually just a text string pretending to be an image.")
    print(f"✓ 生成异常数据 (伪装格式): {fake_jpg_path}")

if __name__ == '__main__':
    # 切换当前工作目录到脚本所在目录，保证生成的文件夹位置正确
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_test_suite()
    print("所有测试数据生成完毕！")