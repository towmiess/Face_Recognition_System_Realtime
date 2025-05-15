
## 🚀 **Features**

### **👨‍💼 Admin Dashboard**

- **Employee Management**  
  - Add, edit, authorize, and delete employees.
  - Upload multiple face embeddings for better recognition accuracy.
  
- **Department Management**  
  - Create, edit, and delete departments.

- **💸 Salary Management**  
  - Manage salary records, including creation, editing, and deletion.
  - Automatic salary deduction for unapproved leave.

- **🕒 Attendance Marking**  
  - Mark attendance with the default camera or IP cameras.
  - Track check-in/check-out times, total stay, and overtime.


- **⏰ Attendance Policies**  
  - Set check-in and check-out time policies.
  - Notify employees of late check-ins via email and apply salary deductions for unapproved absences.

- **🌴 Leave Management**  
  - Approve or reject employee leave requests.
  - Apply salary deductions for unapproved absences.

- **🦺 PPE Compliance Detection**  
  - Detect employee PPE compliance, such as wearing helmets and safety vests.


### **👩‍💻 Employee Dashboard**

- **Project Overview & Attendance**  
  - View the total number of projects, late check-ins, absences, and recent attendance logs (check-in/check-out times, stay time, overtime).
  
- **💰 Salary Details**  
  - View detailed salary breakdowns, including base salary, allowances, bonuses, overtime, deductions, and net salary.

- **📅 Leave Application**  
  - Easily apply for leave through the system.

---

## 🛠️ **Technology Stack**

- **Facial Recognition Models:**
  - **MTCNN** for face detection.
  - **InceptionResnetV1** for face embeddings.

- **Backend Framework:**
  - **Django** for seamless performance and easy management.
- **YOLOv8** for PPE detection helmet and vest
---

## 📝 **Installation Instructions**

### **Requirements**
- Python version: **3.10**
- Django (3.x or higher)
- Other dependencies (listed in `requirements.txt`)

### **Steps to Install:**

1. **Clone the repository:**

2. **Create and activate a virtual environment:**

   If you're using `venv`, run:

   ```cmd 
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   Make sure to have `pip` installed, then run:

   ```cmd
   pip install -r requirements.txt
   ```


4. **Run the development server:**

   ```bash
  uvicorn Project101.asgi:application
   ```

   The application will be available at `http://127.0.0.1:8000`.

---

## 🎬 **Usage**

- **Admin Dashboard:**
  - Log in as an admin to manage employees, departments, attendance, leave requests, and more.

- **Employee Dashboard:**
  - Employees can track their attendance logs, salary details, and apply for leave.

---

## 🛠️ **Pre-requisites**

- **Python 3.10** (Ensure that your Python version matches)
- **OpenCV**: For real-time facial recognition using the default camera or IP cameras.
- **MTCNN**: For face detection.
- **InceptionResnetV1**: For face embedding.
- **YOLOV8**: For PPE detection.
- **Django**: For building the web app.

---


