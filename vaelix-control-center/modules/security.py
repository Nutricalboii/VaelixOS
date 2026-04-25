"""
Vaelix Security Hardening Module
GrapheneOS-inspired desktop protections dashboard.
"""
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.ui_components import make_section, make_divider, CardFrame, VaelixButton

class SecurityModule(QScrollArea):
    """Security dashboard for hardening status and audits."""
    
    def __init__(self, logger, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.setWidgetResizable(True)
        self.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(24)
        
        self._build_ui()
        self.setWidget(content)

    def _build_ui(self):
        # Header
        self.main_layout.addWidget(make_section(
            "Security Hardening",
            "GrapheneOS-inspired protections for your desktop environment."
        ))

        # Hardening Status Cards
        status_layout = QHBoxLayout()
        self.aa_card = CardFrame()
        self._setup_status_card(self.aa_card, "AppArmor", "Enforced", "#4ade80")
        
        self.tpm_card = CardFrame()
        self._setup_status_card(self.tpm_card, "TPM2", "Active", "#22d3ee")
        
        status_layout.addWidget(self.aa_card)
        status_layout.addWidget(self.tpm_card)
        self.main_layout.addLayout(status_layout)

        self.main_layout.addWidget(make_divider())

        # Audit Section
        self.main_layout.addWidget(make_section(
            "Security Audit",
            "Run a deep inspection of system hardening layers."
        ))

        self.audit_log = QLabel("Ready for audit...")
        self.audit_log.setStyleSheet("color: #94a3b8; font-family: 'Space Mono'; font-size: 11px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;")
        self.main_layout.addWidget(self.audit_log)

        run_audit_btn = VaelixButton("Run Comprehensive Audit")
        run_audit_btn.clicked.connect(self._run_audit)
        self.main_layout.addWidget(run_audit_btn)

        self.main_layout.addStretch()

    def _setup_status_card(self, card, title, status, color):
        layout = QVBoxLayout(card)
        t_lbl = QLabel(title)
        t_lbl.setFont(QFont("Syne", 10, QFont.Weight.Bold))
        t_lbl.setStyleSheet("color: #94a3b8;")
        
        s_lbl = QLabel(status)
        s_lbl.setFont(QFont("Syne", 16, QFont.Weight.Bold))
        s_lbl.setStyleSheet(f"color: {color};")
        
        layout.addWidget(t_lbl)
        layout.addWidget(s_lbl)

    def _run_audit(self):
        self.audit_log.setText("Auditing system layers...")
        try:
            # Use the vx-security-audit tool we created
            result = subprocess.check_output(["vx", "security"], text=True)
            self.audit_log.setText(result)
            self.logger.log("Security audit completed.")
        except Exception as e:
            self.audit_log.setText(f"Audit Failed: {str(e)}")
            self.logger.log(f"Security audit failed: {e}", "ERROR")
