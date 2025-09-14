# Data models for the application
import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Donor:
    def __init__(self, name, blood_type, medical_history, last_donation, risk_log):
        self.name = name
        self.blood_type = blood_type
        self.medical_history = medical_history
        self.last_donation = last_donation
        self.risk_log = risk_log

class Request:
    def __init__(self, hospital, blood_type, quantity, risk_assessment):
        self.hospital = hospital
        self.blood_type = blood_type
        self.quantity = quantity
        self.risk_assessment = risk_assessment

class FMEA:
    def __init__(self, process_step, failure_mode, cause, effect, severity, occurrence, detection, rpn):
        self.process_step = process_step
        self.failure_mode = failure_mode
        self.cause = cause
        self.effect = effect
        self.severity = severity
        self.occurrence = occurrence
        self.detection = detection
        self.rpn = rpn
