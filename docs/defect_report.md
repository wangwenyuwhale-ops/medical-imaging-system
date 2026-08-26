# 软件缺陷报告与根因分析记录 (Defect Investigation & RCA)

---

### 缺陷编号: DEF-001
* **标题**: 上传缺失 PatientID 的文件时解析器抛出未捕获异常导致 HTTP 500
* **严重程度**: High (高)
* **优先级**: High (高)
* **发现阶段**: 阶段二 自动化异常测试 (Regression Run #3)
* **关联需求**: REQ-002

**复现步骤 (Steps to Reproduce)**:
1. 运行 `test_data/generate_dicom.py` 生成缺失 PatientID 的 `missing_patient_id.dcm`。
2. 发送 POST 请求至 `/api/dicom/upload` 上传该文件。

**预期结果 (Expected)**:
系统返回 HTTP 400，Validation 引擎显式提示 `PatientID = FAIL`，并附带错误原因 `Missing required tag: PatientID`。

**实际结果 (Actual)**:
系统抛出 `AttributeError: 'Dataset' object has no attribute 'PatientID'`，返回 HTTP 500 Internal Server Error。

**根因分析 (Root Cause Analysis - RCA)**:
`dicom_service.py` 内部直接访问 `ds.PatientID` 属性，缺乏对 DICOM Tag 存在性的防御性检查 (`hasattr`)。

**修复方案与验证 (Fix & Verification)**:
在 `DicomValidationEngine` 中引入 Tag 循环迭代逻辑与 `hasattr` 安全判断。重新运行 `TC-DICOM-002`，用例 PASS，防退化回归测试通过。

---

### 缺陷编号: DEF-002
* **标题**: 传入非 DICOM 损坏二进制文件导致 `dcmread` 挂起异常
* **严重程度**: High (高)
* **优先级**: High (高)
* **关联需求**: REQ-004

**根因分析 (RCA)**:
底层的 `pydicom.dcmread()` 在读取非法头部数据时抛出 `InvalidDicomError`，此前路由未捕获该特定异常。

**修复方案 (Fix)**:
捕获 `InvalidDicomError` 并在 JSON 中明确返回 `Not a valid DICOM file`，响应 HTTP 400。