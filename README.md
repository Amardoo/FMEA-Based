# FMEA-Based
This project is a simple web-based system designed to evaluate and manage risks in blood donation and transfusion processes using the Failure Mode and Effects Analysis (FMEA) methodology.
Users can input potential failure modes, rate them by severity, occurrence, and detectability, and the system automatically calculates the Risk Priority Number (RPN). A dashboard visualizes high-risk areas using interactive charts, and reports can be exported for documentation or analysis.
🔧 Features
    Add and manage failure modes
    Automatic RPN calculation
    Statistical summary (average, max, min RPN, high-risk count)
    Export reports (CSV or PDF)
    Simple database to store multiple entries


Setup and Usage

Directory Structure: Create the structure as shown (blood-risk-evaluation/ with app.py, config.py, models.py, templates/, static/, and database.db).
Install Dependencies: Run pip install flask.
Run the App: Execute python app.py and access http://127.0.0.1:5000/.
Login: Use admin/admin (default credentials; change the password in init_db() for security).
Features:

Login to access the dashboard.
Add donors with risk checks (e.g., anemia based on last donation).
Add requests with basic risk assessment.
Add FMEA entries for each process step, calculating RPN and triggering alerts for RPN > 60.
View all data and high-risk alerts on the dashboard.



Notes

Matching System: Currently basic; enhance by querying donors and requests tables to match blood types and update risk_assessment dynamically.
Reports: Add a /reports route with a template to export data (e.g., using jsPDF as in previous examples).
Mobile Scalability: Use responsive CSS (e.g., Bootstrap) and test on mobile browsers; later convert to a mobile app with Flask-RESTful or a framework like Flutter.
Alerts: The current alert is a console log; extend to email or push notifications using libraries like smtplib or a notification service.

This provides a simple, functional base. Let me know if you want to expand any section (e.g., matching logic, reports, or mobile features)!
