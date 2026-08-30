# Medical Imaging Management System

Medical Imaging Management System 是一个面向医疗软件质量保障与自动化验证的轻量级项目，聚焦于 DICOM 文件校验、元数据提取、数据库一致性核验以及软件验证文档管理。

Medical Imaging Management System is a lightweight medical imaging QA and automated verification project focused on DICOM validation, metadata extraction, database consistency checks, and traceability documentation for software verification.

该项目模拟真实医疗影像系统中的关键质量检查流程，适合用于医疗软件验证、测试工程实践、DICOM 合规性检查和 CI/CD 自动化测试场景的研究与展示。

## 项目概览 / Overview

这个项目旨在验证医疗影像数据在传输、解析和落库过程中的完整性与一致性，并为质量保证流程提供可追溯的测试证据。

This project is designed to verify the integrity and consistency of medical imaging data during transmission, parsing, and persistence, while providing traceable evidence for software quality assurance workflows.

它主要包括以下能力：

- DICOM 文件格式与必填字段合法性校验
- Metadata 提取与结构化分析
- 数据库落库一致性检查
- 异常样本测试与容错验证
- 自动化测试与质量报告生成
- GitHub Actions 持续验证支持

## 核心功能 / Key Features

### 1. DICOM Validation Engine

基于 `pydicom` 实现 DICOM 文件解析与关键 Tag 校验，包括：

- `PatientID`
- `PatientName`
- `StudyInstanceUID`
- `SeriesInstanceUID`
- `Modality`
- `TransferSyntaxUID`

This is implemented with `pydicom` to validate file format and required DICOM tags, such as patient, study, modality, and transfer syntax metadata.

### 2. Data Consistency Check

对通过校验的 DICOM 文件提取元数据后，验证其与数据库中的持久化记录是否一致，从而模拟灰盒测试（gray-box validation）场景。

After metadata is extracted from valid DICOM files, the system checks whether the persisted database records match the extracted data to simulate a gray-box validation workflow.

### 3. Negative Testing & Fault Tolerance

项目集成异常样本，如：

- 缺失关键 Tag
- 非 DICOM 文件
- 二进制损坏
- 伪装格式文件

用于验证后端在异常输入下的稳定性和错误处理能力。

The project includes negative test cases such as missing required tags, non-DICOM files, corrupted binary data, and disguised file formats to validate back-end stability and fault tolerance.

### 4. Traceability Management

项目支持从需求到测试再到缺陷修复的全链路追踪，便于形成软件验证文档体系。

The project supports end-to-end traceability from requirements to test cases, defects, and verification results, enabling a structured software QA documentation flow.

### 5. CI/CD Continuous Verification

通过 GitHub Actions 自动执行测试，支持 Push 触发验证、结果归档与质量追踪。

Continuous verification is supported through GitHub Actions, enabling automated testing, artifact collection, and QA reporting on push events.

## 技术栈 / Tech Stack

- Python 3.10
- Flask
- Flask-SQLAlchemy
- pydicom
- Pytest
- Allure
- SQLite
- GitHub Actions

## 系统架构 / System Architecture

该项目主要分为以下几个层次：

- API Layer：Flask 接口层，处理 DICOM 上传与响应
- Validation Layer：DICOM 校验引擎，校验格式和元数据完整性
- Persistence Layer：SQLite 数据库，保存 Patient / Study 信息
- Test Layer：Pytest + Allure 自动化测试
- QA Documentation Layer：需求矩阵、缺陷报告、验证报告

The system is organized into the following layers:

- API Layer: Flask endpoints for DICOM upload and validation response
- Validation Layer: DICOM validation engine for format and metadata integrity checks
- Persistence Layer: SQLite database storing patient and study records
- Test Layer: Pytest and Allure automation framework
- QA Documentation Layer: requirement traceability and verification reports

## 项目结构 / Project Structure

```text
medical-imaging-system/
├── .github/
│   └── workflows/
│       └── test.yml
├── app/
│   ├── models/
│   │   └── database.py
│   ├── services/
│   │   └── dicom_service.py
│   └── utils/
├── docs/
│   ├── traceability_matrix.md
│   ├── defect_report.md
│   └── verification_report.md
├── tests/
├── test_data/
│   ├── valid/
│   ├── invalid/
│   └── corrupted/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 快速开始 / Getting Started

### 1. 安装依赖 / Install dependencies

```bash
pip install -r requirements.txt
```

### 2. 启动服务 / Run the app

```bash
python main.py
```

服务默认监听：

The application runs by default on:

```text
http://127.0.0.1:5000
```

### 3. 上传 DICOM 文件 / Upload DICOM file

通过以下接口上传医疗影像文件：

Use the following endpoint to upload a DICOM file:

```http
POST /api/dicom/upload
```

示例请求：

Example request:

```bash
curl -X POST -F "file=@sample.dcm" http://127.0.0.1:5000/api/dicom/upload
```

### 4. 运行测试 / Run tests

```bash
pytest
```

如需生成 Allure 报告，可使用：

To generate an Allure report, run:

```bash
allure generate allure-results -o allure-report --clean
```

## API 说明 / API Description

### 上传 DICOM 文件

```http
POST /api/dicom/upload
Content-Type: multipart/form-data
```

返回示例：

Example response:

```json
{
  "file": "sample.dcm",
  "status": "PASS",
  "validation_details": {
    "DICOM_Format": "PASS",
    "Transfer_Syntax": "PASS",
    "PatientID": "PASS",
    "PatientName": "PASS",
    "StudyInstanceUID": "PASS",
    "SeriesInstanceUID": "PASS",
    "Modality": "PASS"
  },
  "metadata": {
    "PatientID": "P-001",
    "PatientName": "Alice^Test",
    "StudyInstanceUID": "1.2.3.4.5",
    "SeriesInstanceUID": "1.2.3.4.5.1",
    "Modality": "CT"
  },
  "error_reason": null
}
```

## 质量保证与测试 / QA & Testing

本项目的重点不只是应用功能实现，而是通过测试验证系统在医疗影像场景中的稳定性与可追溯性。

The focus of this project is not only the application functionality itself, but also validating stability and traceability in medical imaging scenarios.

覆盖的测试方向包括：

- 正常 DICOM 文件校验
- 缺失字段检测
- 非法文件识别
- 数据库一致性检查
- 极端输入和故障恢复
- 自动化测试与持续集成

## 适用场景 / Use Cases

- 医疗软件验证与测试实践
- DICOM 文件格式校验研究
- 医疗影像系统 QA 流程演示
- 自动化测试与 CI/CD 学习
- 软件质量工程和追溯管理展示