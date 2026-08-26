# 需求追溯矩阵 (Requirements Traceability Matrix - RTM)

**项目名称**: Medical Imaging Management System — Software Verification
**系统版本**: v1.0.0
**编制日期**: 2026-04-15
**验证状态**: ALL PASSED (100% Coverage)

| 需求 ID | 需求描述 (Requirement) | 关联模块 | 测试用例 ID (Test Case) | 验证方式 | 执行结果 | 关联缺陷 (Defect) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | 系统应支持 DICOM 文件接收与格式合规性解析 | DICOM Validation Engine | `TC-DICOM-001` | Automated API & DB | PASS | - |
| **REQ-002** | 系统必须强制校验 DICOM 文件中的 PatientID | Validation Engine | `TC-DICOM-002` | Automated Negative Test | PASS | `DEF-001` |
| **REQ-003** | 系统必须强制校验 DICOM 文件中的 StudyInstanceUID | Validation Engine | `TC-DICOM-003` | Automated Negative Test | PASS | - |
| **REQ-004** | 系统应拒绝对损坏/乱码的二进制 DICOM 文件的处理，且系统不得崩溃 | Validation Engine | `TC-DICOM-004` | Fault Tolerance Test | PASS | `DEF-002` |
| **REQ-005** | 系统应拦截非 DICOM 格式的伪装文件 | Validation Engine | `TC-DICOM-005` | Format Verification | PASS | - |
| **REQ-006** | 上传成功的 DICOM Metadata 必须与 MySQL/SQLite 数据库保持 100% 落库一致 | Database Integrity | `TC-DICOM-001` | SQL Consistency Check | PASS | - |