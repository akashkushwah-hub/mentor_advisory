<div align="center">

# 🎓 Batch Mentor Support & Academic Advisory System

**Automated Early Risk Detection & Intelligent Faculty Mentor Allocation Engine**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

*A data-driven decision-support web application built to identify academically at-risk students early and pair them with optimal faculty mentors based on subject specialization and workload capacity.*

</div>

---

## 📌 Overview

In large academic cohorts, manually tracking student attendance, exam performance, pending assignments, and subject backlogs is time-consuming—often delaying critical support for struggling students. 

The **Batch Mentor Support & Academic Advisory System** solves this by continuously evaluating student academic health metrics, classifying risk severity in real time, and automating faculty mentor assignments using a weighted matching algorithm.

---

## ✨ Key Features

* **📊 Cohort-Level Analytics:** Live summary metrics displaying total batch size, average attendance, average exam score, and overall at-risk student ratio.
* **🚨 Automated Risk Assessment Engine:** Evaluates four academic indicators (attendance, exam scores, pending tasks, and failed subjects) to compute a custom **Risk Index** and assign color-coded severity badges (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `NONE`).
* **🤝 Smart Mentor Allocation:** One-click **Auto-Assign Mentor** functionality for `HIGH` and `CRITICAL` risk students, balancing subject-domain expertise with faculty workload capacity.
* **🔍 Real-Time Search & Filtering:** Instantly filter student records by **Student ID**, **Name**, or **Risk Level**.
* **⚖️ Faculty Workload Monitor:** Live tracking of assigned mentees against each professor's maximum advising capacity.

---

## 🧠 Core Algorithms

### 1. Student Risk Index Calculation
Each student's `risk_index` is calculated dynamically using four weighted penalty factors:

$$\text{Risk Index} = \text{Attendance Factor} + \text{Performance Factor} + \text{Pending Factor} + \text{Backlog Factor}$$

| Factor | Formula / Rule | Max Cap |
| :--- | :--- | :--- |
| **Attendance Penalty** | $(75 - \text{Attendance\%}) \times 1.5$ *(if Attendance < 75%)* | — |
| **Exam Score Penalty** | $(50 - \text{Avg Score\%}) \times 1.2$ *(if Score < 50%)* | — |
| **Pending Assignments** | $\text{Pending Tasks} \times 10$ | `30.0` |
| **Subject Backlogs** | $\text{Failed Subjects} \times 15$ | `30.0` |

**Risk Classification Thresholds:**
* 🔴 **CRITICAL:** `Risk Index >= 60` OR `Attendance < 50%` OR `Failed Subjects >= 3`
* 🟠 **HIGH:** `Risk Index >= 40` OR `Attendance < 65%`
* 🟡 **MEDIUM:** `Risk Index >= 20` OR `Attendance < 75%`
* 🔵 **LOW:** `Risk Index > 0`
* 🟢 **NONE:** `Risk Index == 0`

---

### 2. Mentor Priority Score (MPS)
When allocating a mentor to a high-risk student, available professors (below `max_capacity`) are ranked using a weighted score:

$$\text{MPS} = (\text{Domain Match} \times 0.60) + (\text{Workload Score} \times 0.40)$$

* **Domain Match:** `100` if the professor's specialization matches the student's weak subject; otherwise `20`.
* **Workload Score:** $\left(\frac{\text{Max Capacity} - \text{Current Students}}{\text{Max Capacity}}\right) \times 100$

---

## 🏗️ Architecture & Project Structure

```text
academic-advisory-system/
├── app.py               # Flask web routes & request handling
├── engine.py            # Risk assessment, mentor matching & cohort analytics logic
├── database.py          # SQLAlchemy ORM models & automated initial database seeding
├── requirements.txt     # Project dependencies
└── templates/
    └── dashboard.html   # Interactive UI with cohort metrics, search & workload tables
