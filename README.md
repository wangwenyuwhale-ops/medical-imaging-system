\# Medical Imaging Management System — Software Verification \& Automated Testing



!\[CI Status](https://github.com/wangwenyuwhale-ops/medical-imaging-system/actions/workflows/test.yml/badge.svg)

!\[Python Version](https://img.shields.io/badge/python-3.10-blue.svg)

!\[Test Framework](https://img.shields.io/badge/test-Pytest%20%7C%20Allure-brightgreen)



面向医疗软件质量保障（Medical Software QA / Verification）的轻量级医疗影像管理与自动化测试平台。本项目模拟 DICOM 数据接收、Metadata 解析校验、数据库落库一致性校验以及质量追溯体系。



\## 🌟 核心特性 (Features)



\* \*\*DICOM Validation Engine\*\*: 基于 `pydicom` 实现 DICOM Tag 提取与合规校验（PatientID, Modality, Transfer Syntax 等）。

\* \*\*Gray-box Consistency Check\*\*: 结合 SQL 参数化查询，端到端验证 DICOM Metadata 与数据库落库记录的一致性。

\* \*\*Negative \& Fault Tolerance Testing\*\*: 自动生成缺失 Tag、二进制损坏及格式伪装的异常测试集，验证后端防崩溃能力。

\* \*\*Full Traceability\*\*: 建立完整的 `Requirement -> Test Case -> Defect -> Verification Report` 需求追溯链条。

\* \*\*CI/CD Continuous Verification\*\*: 接入 GitHub Actions，在无头环境中实现 Push 即测试与构建产物归档。



\## 📁 工程目录结构



```text

medical-imaging-system/

├── .github/workflows/   # GitHub Actions CI/CD 流水线配置

├── app/                  # Flask 后端服务 \& DICOM 验证引擎

├── tests/                # Pytest 自动化测试套件 (API \& DB Consistency)

├── test\_data/            # 动态测试数据生成脚本 (Valid / Invalid / Corrupted)

├── docs/                 # 质量验证文档体系

│   ├── traceability\_matrix.md   # 需求追溯矩阵 (RTM)

│   ├── defect\_report.md         # 缺陷报告与 RCA 根因分析

│   └── verification\_report.md   # 软件验证报告 (SVR)

└── main.py               # 服务启动入口

