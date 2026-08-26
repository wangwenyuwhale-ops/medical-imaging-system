# tests/api/test_dicom_api.py
import os
import pytest
import requests
import sqlite3
import allure

BASE_URL = "http://127.0.0.1:5000/api/dicom/upload"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, '../../test_data')

# 寻找数据库文件位置 (Flask 3.x 默认在 instance 文件夹，较早版本在根目录)
DB_PATH = os.path.join(CURRENT_DIR, '../../instance/medical_qa.db')
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(CURRENT_DIR, '../../medical_qa.db')

def upload_file(file_path):
    """辅助方法：封装 HTTP POST 文件上传"""
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'application/dicom')}
        response = requests.post(BASE_URL, files=files)
    return response

@allure.epic("Medical Imaging Management System")
@allure.feature("DICOM 文件上传与解析验证 (DICOM Validation Engine)")
class TestDicomUploadAPI:
    
    @allure.story("正常业务流：有效 DICOM 文件上传")
    @allure.title("TC-DICOM-001: 验证合法 DICOM 上传及数据库落库一致性")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("REQ-003", name="关联需求：系统应支持 DICOM 上传并解析")
    def test_tc_dicom_001_valid_upload(self):
        file_path = os.path.join(TEST_DATA_DIR, 'valid', 'valid_ct.dcm')
        
        with allure.step("1. 调用 API 上传合法的 CT DICOM 文件"):
            response = upload_file(file_path)
        
        with allure.step("2. 验证 API 响应状态码及 JSON 结构 (Black-box)"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert data['status'] == 'PASS'
            assert data['metadata']['PatientID'] == 'P_VALID_01'
            assert data['metadata']['Modality'] == 'CT'
            assert data['validation_details']['DICOM_Format'] == 'PASS'
            
            # 提取动态生成的 Study UID，作为查库的线索
            study_uid = data['metadata']['StudyInstanceUID']

        with allure.step("3. 执行 SQL 验证数据库落库一致性 (Gray-box)"):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            try:
                # 验证一：Patient 表记录
                cursor.execute("SELECT patient_name FROM patients WHERE patient_id = 'P_VALID_01'")
                patient_record = cursor.fetchone()
                assert patient_record is not None, "数据库中未找到该患者记录"
                assert patient_record[0] == "Test^QA", "数据库中患者姓名与 DICOM 数据不一致"

                # 验证二：Study 表记录与外键关系
                cursor.execute("SELECT patient_id, modality FROM studies WHERE study_uid = ?", (study_uid,))
                study_record = cursor.fetchone()
                assert study_record is not None, "数据库中未找到该检查(Study)记录"
                assert study_record[0] == 'P_VALID_01', "Study 记录绑定的患者 ID 错误"
                assert study_record[1] == 'CT', "Modality 落库错误"
            finally:
                cursor.close()
                conn.close()

    @allure.story("异常业务流：数据完整性校验 (Data Integrity)")
    @allure.title("TC-DICOM-002: 验证上传缺失 PatientID 的 DICOM 文件")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.issue("DEF-001", name="缺陷追踪：验证引擎未拦截缺失的 PatientID")
    @allure.testcase("REQ-005", name="关联需求：DICOM必须包含Patient ID")
    def test_tc_dicom_002_missing_patient_id(self):
        file_path = os.path.join(TEST_DATA_DIR, 'invalid', 'missing_patient_id.dcm')
        
        with allure.step("1. 上传缺失 PatientID 的文件，期望被拦截"):
            response = upload_file(file_path)
            assert response.status_code == 400
            
        with allure.step("2. 验证 Validation 引擎是否正确返回 FAIL 原因"):
            data = response.json()
            assert data['status'] == 'FAIL'
            assert data['validation_details']['PatientID'] == 'FAIL'
            assert "Missing required tag: PatientID" in data['error_reason']

    @allure.story("异常业务流：数据完整性校验 (Data Integrity)")
    @allure.title("TC-DICOM-003: 验证上传缺失 StudyInstanceUID 的 DICOM 文件")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("REQ-006", name="关联需求：DICOM必须包含Study UID")
    def test_tc_dicom_003_missing_study_uid(self):
        file_path = os.path.join(TEST_DATA_DIR, 'invalid', 'missing_study_uid.dcm')
        
        with allure.step("1. 上传缺失 Study UID 的文件"):
            response = upload_file(file_path)
            assert response.status_code == 400
            
        with allure.step("2. 验证引擎拒绝接收并明确标记字段失败"):
            data = response.json()
            assert data['status'] == 'FAIL'
            assert data['validation_details']['StudyInstanceUID'] == 'FAIL'

    @allure.story("异常业务流：系统防崩溃与容错性 (Fault Tolerance)")
    @allure.title("TC-DICOM-004: 验证上传完全损坏的二进制 DICOM 文件")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.issue("DEF-002", name="缺陷追踪：底层解析库报错导致 HTTP 500")
    def test_tc_dicom_004_corrupted_file(self):
        file_path = os.path.join(TEST_DATA_DIR, 'invalid', 'corrupted.dcm')
        
        with allure.step("1. 上传乱码/损坏的二进制文件"):
            response = upload_file(file_path)
            
        with allure.step("2. 验证系统未崩溃 (非 HTTP 500)，并正确处理异常"):
            assert response.status_code == 400
            data = response.json()
            assert data['status'] == 'FAIL'
            assert data['validation_details']['DICOM_Format'] == 'FAIL'
            assert "Not a valid DICOM file" in data['error_reason']

    @allure.story("异常业务流：非法文件类型拦截")
    @allure.title("TC-DICOM-005: 验证上传伪装成图片的非 DICOM 文件")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("REQ-004", name="关联需求：非 DICOM 文件应被拒绝")
    def test_tc_dicom_005_fake_image_file(self):
        file_path = os.path.join(TEST_DATA_DIR, 'invalid', 'not_dicom.jpg')
        
        with allure.step("1. 上传假装成图片的普通文本文件"):
            response = upload_file(file_path)
            
        with allure.step("2. 验证格式校验拦截"):
            assert response.status_code == 400
            data = response.json()
            assert data['status'] == 'FAIL'
            assert data['validation_details']['DICOM_Format'] == 'FAIL'