from sqlalchemy.orm import validates
import secrets
import validators
import ipaddress
from .base import Base, db
import os 

class LockedIps(Base):
    ip_address = db.Column(db.String(50), nullable=False, unique=True)
    locked_template = db.Column(db.Integer, db.ForeignKey('vm_templates.id', onupdate="CASCADE", ondelete="CASCADE"))
    locked_group = db.Column(db.String(30))

    vm_templates = db.relationship("VmTemplates", foreign_keys=[locked_template])
    # vm_groups = db.relationship("VmGroups", foreign_keys=[locked_group])

    def __init__(self, locked_ips):
        super()
        self.ip_address = locked_ips['ip_address']
        if 'locked_template' in locked_ips.keys():
            self.locked_template = locked_ips['locked_template']
        elif 'locked_group'  in locked_ips.keys():
            self.locked_group = locked_ips['locked_group']
    
    @validates('ip_address')
    def validate_ip_address(self, key, ip_address):
        ip0=os.environ.get('APP_VM_START_IP')
        ip1=os.environ.get('APP_VM_END_IP')
        start_ip=int(ipaddress.ip_address(ip0))
        end_ip=int(ipaddress.ip_address(ip1))
        ip_int=int(ipaddress.ip_address(ip_address))
        if ip_int < start_ip or ip_int > end_ip:
            raise AssertionError('Invalid IP Address!')
        return ip_address


