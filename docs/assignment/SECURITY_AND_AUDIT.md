# Security and Audit Considerations

**Document Version:** 1.0  
**Date:** December 10, 2024  
**Status:** Planning - For Production Implementation  
**Scope:** Faculty-level statistics feature security requirements

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Security Architecture](#security-architecture)
3. [Authentication & Authorization](#authentication--authorization)
4. [Data Privacy & GDPR](#data-privacy--gdpr)
5. [Audit Trail Requirements](#audit-trail-requirements)
6. [Logging Strategy](#logging-strategy)
7. [API Security](#api-security)
8. [Data Protection](#data-protection)
9. [Compliance & Governance](#compliance--governance)
10. [Implementation Roadmap](#implementation-roadmap)

---

## 1. Executive Summary

### Purpose

This document outlines security and audit requirements for the faculty-level statistics feature in 4TU.ResearchData repository. As a research data repository serving multiple institutions and handling personal data (faculty affiliations), security and auditability are critical.

### Key Principles

1. **Defense in Depth**: Multiple layers of security controls
2. **Least Privilege**: Users have minimum necessary permissions
3. **Audit Everything**: All changes and access are logged
4. **Privacy by Design**: GDPR compliance built-in from start
5. **Transparency**: Clear audit trails for accountability

### Security Posture

**Current State (Prototype):**
- ⚠️ No authentication documented
- ⚠️ No authorization controls
- ⚠️ No audit trails
- ⚠️ No logging strategy
- ✅ Read-only operations (lower risk)

**Target State (Production):**
- ✅ Role-based access control (RBAC)
- ✅ Comprehensive audit logging
- ✅ GDPR-compliant data handling
- ✅ Secure API with authentication
- ✅ Encrypted data at rest and in transit

### Critical Security Requirements

| Requirement | Priority | Phase | Status |
|-------------|----------|-------|--------|
| Authentication | P0 (Critical) | Phase 1 | ⚠️ Required for production |
| Authorization (RBAC) | P0 (Critical) | Phase 1 | ⚠️ Required for production |
| Audit Logging | P0 (Critical) | Phase 1 | ⚠️ Required for production |
| Data Encryption (Transit) | P0 (Critical) | Phase 1 | ⚠️ Required for production |
| GDPR Compliance | P0 (Critical) | Phase 1 | ⚠️ Required for production |
| Data Encryption (Rest) | P1 (High) | Phase 1 | ⚠️ Depends on Virtuoso config |
| Rate Limiting | P1 (High) | Phase 1 | ⚠️ Recommended |
| Input Validation | P1 (High) | Phase 1 | ✅ Partially implemented |
| Security Monitoring | P2 (Medium) | Phase 2 | 🔵 Future enhancement |
| Penetration Testing | P2 (Medium) | Pre-launch | 🔵 Before go-live |

---

## 2. Security Architecture

### 2.1 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   Layer 1: Network Security                  │
│  - HTTPS/TLS 1.3 (encryption in transit)                   │
│  - Firewall rules (restrict access to API endpoints)       │
│  - DDoS protection                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Layer 2: Application Security                   │
│  - Authentication (who are you?)                            │
│  - Authorization (what can you do?)                         │
│  - Input validation (prevent injection)                     │
│  - Rate limiting (prevent abuse)                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                Layer 3: Data Security                        │
│  - Encryption at rest (Virtuoso database)                   │
│  - Field-level encryption (sensitive data)                  │
│  - Data masking (logs don't expose personal data)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               Layer 4: Audit & Monitoring                    │
│  - Audit logs (who did what, when)                          │
│  - Security monitoring (detect anomalies)                   │
│  - Incident response (react to breaches)                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Threat Model

**Assets to Protect:**
1. **Personal Data**: Faculty affiliations (GDPR-sensitive)
2. **Research Data**: Datasets (valuable IP)
3. **System Integrity**: Prevent unauthorized modifications
4. **Service Availability**: Ensure uptime for users

**Potential Threats:**
1. **Unauthorized Access**: Attacker gains access to faculty data
2. **Data Tampering**: Malicious modification of faculty assignments
3. **Data Leakage**: Personal data exposed in logs or errors
4. **Denial of Service**: API overwhelmed by requests
5. **Privilege Escalation**: Regular user gains admin access
6. **Audit Log Tampering**: Attacker covers their tracks

**Mitigations:** See sections 3-8 below.

---

## 3. Authentication & Authorization

### 3.1 Authentication Strategy

**Approach: Leverage Existing Djehuty Authentication**

Assumption: Djehuty already has an authentication system (to be verified).

**If Djehuty has authentication:**
```python
# Faculty statistics endpoints inherit existing auth
@app.route('/v2/statistics/faculties')
@require_authentication  # Reuse existing decorator
def faculty_statistics():
    # Only authenticated users can view stats
    pass
```

**If Djehuty does NOT have authentication:**
Implement token-based authentication:

```python
# Token-based authentication
import jwt
from functools import wraps

def require_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Missing authentication token'}), 401
        
        try:
            # Verify JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = payload  # Attach user info to request
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
```

**Authentication Methods:**

**Option 1: Session-based (if existing)**
- User logs in via web UI
- Session cookie stored
- Cookie sent with API requests

**Option 2: Token-based (recommended for API)**
- User authenticates, receives JWT token
- Token sent in `Authorization: Bearer <token>` header
- Token expires after configurable time (e.g., 1 hour)

**Option 3: SSO Integration (future)**
- Integrate with university SSO (SAML, OAuth)
- Users authenticate with institutional credentials
- Seamless experience for university users

**Recommendation:** Start with existing Djehuty auth (if available), migrate to SSO in Phase 2.

### 3.2 Authorization (RBAC)

**Roles Defined:**

| Role | Can View Stats | Can Update Faculty | Can Modify Config | Can Access Audit Logs |
|------|----------------|--------------------|--------------------|------------------------|
| **Public** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Authenticated User** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Depositor** | ✅ Yes | ⚠️ Own account only | ❌ No | ❌ No |
| **Data Steward** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes (read-only) |
| **Repository Admin** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (full access) |

**Authorization Rules:**

**1. View Faculty Statistics:**
```python
@require_authentication
@require_role('authenticated_user')  # Any logged-in user
def faculty_statistics():
    # Anyone authenticated can view aggregate statistics
    return get_faculty_stats()
```

**2. Update Account Faculty:**
```python
@require_authentication
def update_account_faculty(account_uuid):
    current_user = get_current_user()
    
    # Rule 1: User can update their own account
    if account_uuid == current_user.uuid:
        return update_faculty(account_uuid, request.json['faculty_id'])
    
    # Rule 2: Data stewards can update any account
    if current_user.has_role('data_steward'):
        audit_log('faculty_assignment_updated', {
            'account_uuid': account_uuid,
            'updated_by': current_user.uuid,
            'new_faculty_id': request.json['faculty_id']
        })
        return update_faculty(account_uuid, request.json['faculty_id'])
    
    # Rule 3: Otherwise, forbidden
    return jsonify({'error': 'Insufficient permissions'}), 403
```

**3. Modify Faculty Configuration:**
```python
@require_authentication
@require_role('repository_admin')  # Admin only
def update_faculty_config():
    # Only admins can add/remove faculties
    audit_log('faculty_config_updated', {
        'updated_by': get_current_user().uuid,
        'changes': request.json
    })
    return update_config(request.json)
```

**Implementation:**

```python
# Role checking decorator
def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user.has_role(role_name):
                audit_log('unauthorized_access_attempt', {
                    'user_uuid': user.uuid,
                    'required_role': role_name,
                    'endpoint': request.endpoint
                })
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

---

## 4. Data Privacy & GDPR

### 4.1 Personal Data Classification

**Faculty Affiliation = Personal Data**

Under GDPR, linking a person (depositor/author) to their faculty affiliation is **personal data** because it:
- Identifies or relates to an individual
- Can be used to infer employment status
- Combined with other data, reveals more about the person

**Data Categories:**

| Data Element | Personal Data? | GDPR Category | Retention |
|--------------|----------------|---------------|-----------|
| Account email | ✅ Yes | Identifying | Active account + 7 years |
| Account name | ✅ Yes | Identifying | Active account + 7 years |
| Faculty assignment | ✅ Yes | Employment-related | Active account + 7 years |
| Faculty statistics (aggregated) | ❌ No | Anonymous | Indefinite |
| Audit logs (with UUIDs) | ✅ Yes | Activity logs | 7 years |

### 4.2 GDPR Compliance Requirements

**Lawful Basis for Processing:**

**Option 1: Legitimate Interest** (Most likely)
- Processing necessary for repository operations
- Faculty statistics support institutional goals
- Users' interests do not override institutional needs
- **Requirement**: Conduct Legitimate Interest Assessment (LIA)

**Option 2: Consent**
- Obtain explicit consent from users
- **Challenge**: Harder to enforce, users can withdraw consent
- **Not recommended** for core repository functionality

**Recommendation:** Use "Legitimate Interest" with clear transparency.

**GDPR Rights Implementation:**

**1. Right to Access (Art. 15)**
User can request: "What faculty data do you have about me?"

```python
@app.route('/v2/accounts/<uuid>/data-export', methods=['GET'])
@require_authentication
def export_personal_data(uuid):
    # User can only access their own data
    current_user = get_current_user()
    if uuid != current_user.uuid and not current_user.has_role('data_steward'):
        return jsonify({'error': 'Forbidden'}), 403
    
    # Export all personal data
    data = {
        'account': get_account_data(uuid),
        'faculty_assignment': get_faculty_assignment(uuid),
        'faculty_history': get_faculty_change_history(uuid),
        'audit_logs': get_user_audit_logs(uuid)
    }
    
    audit_log('personal_data_exported', {
        'user_uuid': uuid,
        'requested_by': current_user.uuid
    })
    
    return jsonify(data), 200
```

**2. Right to Rectification (Art. 16)**
User can request: "My faculty assignment is wrong, please correct it."

```python
# Already implemented via PATCH /v2/accounts/{uuid}
# Ensure clear process for users to request corrections
# Data stewards review and approve changes
```

**3. Right to Erasure / "Right to be Forgotten" (Art. 17)**

**Challenge:** Research data must be retained for reproducibility.

**Approach:**
- **Faculty assignment**: Can be deleted/anonymized when account is deleted
- **Datasets deposited**: Remain in repository (with anonymized depositor info)
- **Audit logs**: Retained for 7 years (legal requirement), then deleted

```python
@app.route('/v2/accounts/<uuid>', methods=['DELETE'])
@require_authentication
@require_role('data_steward')
def delete_account(uuid):
    # Soft delete: anonymize personal data, keep datasets
    account = get_account(uuid)
    
    # Anonymize account
    account.email = f"deleted-user-{uuid}@anonymized.example"
    account.first_name = "Deleted"
    account.last_name = "User"
    account.faculty_id = None  # Remove faculty assignment
    
    # Mark as deleted
    account.deleted_at = datetime.now()
    account.save()
    
    # Keep datasets (they are separate entities)
    # Depositor link becomes "Deleted User"
    
    audit_log('account_deleted_gdpr', {
        'account_uuid': uuid,
        'deleted_by': get_current_user().uuid,
        'reason': request.json.get('reason', 'User request')
    })
    
    return jsonify({'message': 'Account anonymized'}), 200
```

**4. Right to Restrict Processing (Art. 18)**
User can request: "Stop using my data for statistics."

```python
# Add flag to account
account.restrict_processing = True

# Exclude from statistics
def faculty_statistics():
    # Only include accounts without processing restriction
    accounts = Account.query.filter_by(restrict_processing=False).all()
    # ... calculate statistics
```

**5. Right to Data Portability (Art. 20)**
Export data in machine-readable format (JSON, CSV).

```python
# Already covered by "Right to Access" endpoint
# Ensure format is JSON (machine-readable) ✅
```

**6. Right to Object (Art. 21)**
Similar to "Restrict Processing" - user objects to being included in statistics.

### 4.3 Privacy Impact Assessment (PIA)

**Required Before Production Launch:**

```markdown
# Privacy Impact Assessment - Faculty Statistics

## 1. Description of Processing
- Storing faculty affiliations for depositors/authors
- Aggregating statistics by faculty
- Displaying statistics in dashboard

## 2. Purpose & Lawful Basis
- Purpose: Enable faculty-level reporting for stakeholders
- Lawful Basis: Legitimate interest (institutional need)

## 3. Data Minimization
- Only collect faculty affiliation (minimum necessary)
- No additional personal data required

## 4. Risks Identified
- Risk 1: Unauthorized access to faculty assignments
  - Mitigation: Role-based access control
- Risk 2: Data breach exposing affiliations
  - Mitigation: Encryption, audit logs
- Risk 3: Re-identification in aggregated stats
  - Mitigation: Don't display stats for faculties with <5 datasets

## 5. User Rights
- All GDPR rights implemented (see above)
- Clear privacy notice provided
- Users can update/delete their data

## 6. Data Retention
- Active accounts: Faculty data retained
- Deleted accounts: Data anonymized
- Audit logs: Retained 7 years, then deleted

## 7. Third-Party Sharing
- No third-party sharing of faculty assignments
- Aggregated statistics may be shared (anonymous)

## 8. Security Measures
- See Section 8 (Data Protection)

## 9. DPO Review
- [ ] Reviewed by Data Protection Officer
- [ ] Approved for production
- [ ] Date: [TBD]
```

**Action Required:** Conduct full PIA with university Data Protection Officer before launch.

### 4.4 Privacy Notice

**Add to User-Facing Documentation:**

```markdown
## Faculty Affiliation - Privacy Notice

### What Data We Collect
We store your faculty affiliation (e.g., "Faculty of Aerospace Engineering") 
to provide statistics for university stakeholders.

### Why We Collect It
Faculty-level statistics help universities understand research data output 
per faculty, supporting strategic planning and resource allocation.

### Legal Basis
We process this data based on legitimate interest (institutional need). 
Your interests do not override this need, as faculty affiliation is necessary 
for repository operations.

### How Long We Keep It
- While your account is active: We retain your faculty assignment
- After account deletion: We anonymize your data
- Audit logs: Retained for 7 years for compliance

### Your Rights
You have the right to:
- ✅ Access your data (download your information)
- ✅ Correct your data (update your faculty assignment)
- ✅ Delete your data (request account deletion)
- ✅ Restrict processing (opt out of statistics)
- ✅ Object to processing (contact us if you disagree)

### Contact
For privacy questions: privacy@4tu.nl
Data Protection Officer: dpo@4tu.nl
```

---

## 5. Audit Trail Requirements

### 5.1 What to Audit

**Critical Events (Must Log):**

| Event Type | When | What to Log |
|------------|------|-------------|
| **Faculty Assignment Created** | New account with faculty | `user_uuid`, `faculty_id`, `created_by`, `timestamp` |
| **Faculty Assignment Updated** | Faculty changed | `user_uuid`, `old_faculty_id`, `new_faculty_id`, `updated_by`, `timestamp`, `reason` |
| **Faculty Assignment Deleted** | Faculty removed | `user_uuid`, `faculty_id`, `deleted_by`, `timestamp`, `reason` |
| **Faculty Config Updated** | Faculty added/removed/modified | `config_changes`, `updated_by`, `timestamp` |
| **Statistics Accessed** | API called | `endpoint`, `user_uuid`, `parameters`, `timestamp` |
| **Unauthorized Access Attempt** | 403 Forbidden | `user_uuid`, `endpoint`, `required_permission`, `timestamp` |
| **Data Export** | GDPR data export | `user_uuid`, `exported_by`, `data_types`, `timestamp` |
| **Account Deleted** | GDPR erasure | `user_uuid`, `deleted_by`, `reason`, `timestamp` |

**Informational Events (Should Log):**

| Event Type | When | What to Log |
|------------|------|-------------|
| **Bulk Import** | Migration script run | `accounts_processed`, `success_count`, `error_count`, `timestamp` |
| **Dashboard Viewed** | User opens dashboard | `user_uuid`, `timestamp` (Optional, if tracking engagement) |
| **API Error** | 500 Internal Error | `endpoint`, `error_message`, `stack_trace`, `timestamp` |

### 5.2 Audit Log Schema

**Database Table: `audit_logs`**

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    user_uuid UUID,  -- Who performed the action
    target_uuid UUID,  -- What was affected (account UUID, etc.)
    details JSONB,  -- Event-specific data
    ip_address INET,  -- For security monitoring
    user_agent TEXT,  -- Browser/client info
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_user_uuid (user_uuid),
    INDEX idx_timestamp (timestamp)
);
```

**Example Audit Log Entries:**

```json
{
  "event_type": "faculty_assignment_updated",
  "user_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "target_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "details": {
    "old_faculty_id": 1,
    "new_faculty_id": 2,
    "old_faculty_name": "Faculty of Aerospace Engineering",
    "new_faculty_name": "Faculty of EEMCS",
    "reason": "User changed departments",
    "updated_by_role": "data_steward"
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "timestamp": "2025-01-15T14:30:00Z"
}
```

### 5.3 Audit Log Implementation

```python
import logging
import json
from datetime import datetime

class AuditLogger:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def log(self, event_type, user_uuid=None, target_uuid=None, details=None):
        """
        Log an audit event to database.
        
        Args:
            event_type: Type of event (e.g., 'faculty_assignment_updated')
            user_uuid: UUID of user who performed action
            target_uuid: UUID of affected resource
            details: Dict of event-specific data
        """
        # Get request context if available
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get('User-Agent') if request else None
        
        # Insert into database
        query = """
            INSERT INTO audit_logs 
            (event_type, user_uuid, target_uuid, details, ip_address, user_agent, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        self.db.execute(query, (
            event_type,
            user_uuid,
            target_uuid,
            json.dumps(details) if details else None,
            ip_address,
            user_agent,
            datetime.utcnow()
        ))
        
        self.db.commit()
        
        # Also log to application log for immediate visibility
        logging.info(f"AUDIT: {event_type}", extra={
            'event_type': event_type,
            'user_uuid': str(user_uuid) if user_uuid else None,
            'details': details
        })

# Usage in endpoints
audit = AuditLogger(db)

@app.route('/v2/accounts/<uuid>', methods=['PATCH'])
@require_authentication
def update_account(uuid):
    current_user = get_current_user()
    old_faculty_id = get_account(uuid).faculty_id
    new_faculty_id = request.json.get('faculty_id')
    
    # Perform update
    update_faculty_assignment(uuid, new_faculty_id)
    
    # Audit log
    audit.log('faculty_assignment_updated',
        user_uuid=current_user.uuid,
        target_uuid=uuid,
        details={
            'old_faculty_id': old_faculty_id,
            'new_faculty_id': new_faculty_id,
            'reason': request.json.get('reason', 'User update')
        }
    )
    
    return jsonify({'message': 'Faculty updated'}), 200
```

### 5.4 Audit Log Retention

**Retention Policy:**
- **Active logs**: Retained for 7 years (compliance requirement)
- **After 7 years**: Archived or deleted
- **Storage location**: Separate database or log aggregation system

**Retention Implementation:**

```python
# Scheduled task (run monthly)
def archive_old_audit_logs():
    """
    Archive audit logs older than 7 years.
    """
    cutoff_date = datetime.now() - timedelta(days=7*365)
    
    # Export to archive storage (S3, tape, etc.)
    old_logs = AuditLog.query.filter(AuditLog.timestamp < cutoff_date).all()
    
    if old_logs:
        export_to_archive(old_logs, f"audit_archive_{cutoff_date.year}.json")
        
        # Delete from active database
        AuditLog.query.filter(AuditLog.timestamp < cutoff_date).delete()
        db.commit()
        
        logging.info(f"Archived {len(old_logs)} audit logs older than 7 years")
```

### 5.5 Audit Log Access

**Who Can Access Audit Logs:**
- **Data Stewards**: Read-only access to all logs
- **Repository Admins**: Full access (read, export, delete if needed)
- **Regular Users**: Can view their own audit trail (GDPR right to access)

**Audit Log Viewer:**

```python
@app.route('/v2/audit-logs', methods=['GET'])
@require_authentication
@require_role('data_steward')
def view_audit_logs():
    """
    View audit logs (data stewards and admins only).
    """
    # Filters
    event_type = request.args.get('event_type')
    user_uuid = request.args.get('user_uuid')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build query
    query = AuditLog.query
    
    if event_type:
        query = query.filter_by(event_type=event_type)
    if user_uuid:
        query = query.filter_by(user_uuid=user_uuid)
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    
    # Paginate
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=per_page
    )
    
    return jsonify({
        'logs': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': logs.page
    })
```

---

## 6. Logging Strategy

### 6.1 Log Types

**1. Application Logs** (General system operation)
- Startup/shutdown events
- Configuration loaded
- Background jobs
- Performance metrics

**2. Security Logs** (Security events)
- Failed login attempts
- Unauthorized access attempts
- Suspicious activity patterns

**3. Audit Logs** (User actions) - See Section 5

**4. Error Logs** (Failures and exceptions)
- Uncaught exceptions
- Database errors
- External service failures

### 6.2 Log Levels

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/djehuty/faculty_statistics.log'),
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger('faculty_statistics')

# Usage:
logger.debug("Loading faculty configuration")  # Development only
logger.info("Faculty statistics endpoint called")  # Normal operation
logger.warning("Faculty ID not found, using 'Other'")  # Potential issue
logger.error("Failed to update faculty assignment", exc_info=True)  # Error with stack trace
logger.critical("Database connection lost")  # System failure
```

**Log Levels:**
- **DEBUG**: Detailed information for development (not in production)
- **INFO**: General informational messages (normal operation)
- **WARNING**: Unexpected situation, but system still works
- **ERROR**: Error occurred, functionality affected
- **CRITICAL**: Serious error, system may be unstable

### 6.3 Structured Logging

**Use JSON format for machine-readable logs:**

```python
import logging
import json
from pythonjsonlogger import jsonlogger

# Configure JSON logger
logHandler = logging.FileHandler('/var/log/djehuty/faculty_statistics.json')
formatter = jsonlogger.JsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Usage
logger.info('Faculty statistics accessed', extra={
    'user_uuid': str(user.uuid),
    'endpoint': '/v2/statistics/faculties',
    'response_time_ms': 45,
    'faculty_count': 3
})

# Output:
{
  "timestamp": "2025-01-15T14:30:00.123Z",
  "level": "INFO",
  "name": "faculty_statistics",
  "message": "Faculty statistics accessed",
  "user_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "endpoint": "/v2/statistics/faculties",
  "response_time_ms": 45,
  "faculty_count": 3
}
```

### 6.4 Log Rotation

**Prevent log files from growing indefinitely:**

```python
from logging.handlers import RotatingFileHandler

# Rotate after 10MB, keep 5 backup files
handler = RotatingFileHandler(
    '/var/log/djehuty/faculty_statistics.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
```

**Or use TimedRotatingFileHandler for daily rotation:**

```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    '/var/log/djehuty/faculty_statistics.log',
    when='midnight',  # Rotate at midnight
    interval=1,  # Every 1 day
    backupCount=30  # Keep 30 days
)
```

### 6.5 Log Security

**Don't Log Sensitive Data:**

```python
# ❌ BAD: Logs personal data
logger.info(f"User {user.email} updated faculty to {faculty.name}")

# ✅ GOOD: Logs UUIDs only
logger.info("Faculty assignment updated", extra={
    'user_uuid': str(user.uuid),
    'faculty_id': faculty.id
})

# ❌ BAD: Logs full request body (may contain sensitive data)
logger.debug(f"Request body: {request.json}")

# ✅ GOOD: Logs sanitized version
sanitized = {k: v for k, v in request.json.items() if k not in ['password', 'token']}
logger.debug("Request received", extra={'params': sanitized})
```

### 6.6 Centralized Logging (Future)

**For Production:**
Consider log aggregation system (ELK Stack, Splunk, Datadog):

```
Application → Logstash → Elasticsearch → Kibana (visualization)
                ↓
         Alerting (Anomaly detection)
```

**Benefits:**
- Centralized search across all logs
- Real-time dashboards
- Automated alerting (e.g., "Too many 500 errors")
- Log correlation (trace requests across services)

---

## 7. API Security

### 7.1 HTTPS/TLS

**Requirement:** All API endpoints must use HTTPS (TLS 1.3).

**Configuration:**

```nginx
# nginx configuration
server {
    listen 443 ssl http2;
    server_name data.4tu.nl;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    ssl_protocols TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name data.4tu.nl;
    return 301 https://$server_name$request_uri;
}
```

### 7.2 Input Validation

**Validate all API inputs:**

```python
from marshmallow import Schema, fields, validate, ValidationError

class UpdateFacultySchema(Schema):
    faculty_id = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=100),  # Valid faculty IDs
        error_messages={'required': 'Faculty ID is required'}
    )
    reason = fields.String(
        required=False,
        validate=validate.Length(max=500),  # Prevent excessively long strings
        missing=None
    )

@app.route('/v2/accounts/<uuid>', methods=['PATCH'])
@require_authentication
def update_account(uuid):
    # Validate UUID format
    try:
        UUID(uuid)  # Raises ValueError if invalid
    except ValueError:
        return jsonify({'error': 'Invalid UUID format'}), 400
    
    # Validate request body
    schema = UpdateFacultySchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    # Validate faculty exists
    faculty = Faculty.query.get(data['faculty_id'])
    if not faculty:
        return jsonify({'error': 'Faculty not found'}), 404
    
    # Proceed with update
    update_faculty_assignment(uuid, data['faculty_id'])
    return jsonify({'message': 'Updated'}), 200
```

**Prevent SQL Injection (even in SPARQL):**

```python
# ❌ BAD: String concatenation (SQL injection risk)
query = f"SELECT * FROM accounts WHERE faculty_id = {faculty_id}"

# ✅ GOOD: Parameterized queries
query = "SELECT * FROM accounts WHERE faculty_id = %s"
cursor.execute(query, (faculty_id,))

# For SPARQL:
# ❌ BAD:
sparql_query = f"SELECT ?s WHERE {{ ?s djht:faculty_id {faculty_id} }}"

# ✅ GOOD: Use SPARQL parameter binding
from rdflib.plugins.sparql import prepareQuery
query = prepareQuery("""
    SELECT ?s WHERE {
        ?s djht:faculty_id ?faculty_id
    }
""")
results = graph.query(query, initBindings={'faculty_id': Literal(faculty_id)})
```

### 7.3 Rate Limiting

**Prevent API abuse:**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"  # Use Redis for distributed rate limiting
)

# Apply to endpoints
@app.route('/v2/statistics/faculties')
@limiter.limit("100 per hour")  # More restrictive for statistics
@require_authentication
def faculty_statistics():
    return get_faculty_stats()

@app.route('/v2/accounts/<uuid>', methods=['PATCH'])
@limiter.limit("20 per hour")  # Very restrictive for write operations
@require_authentication
def update_account(uuid):
    # Update logic
    pass
```

**Rate Limit Response:**

```json
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 3600

{
  "error": "Rate limit exceeded",
  "message": "You have exceeded the rate limit of 100 requests per hour",
  "retry_after": 3600
}
```

### 7.4 CORS (Cross-Origin Resource Sharing)

**If dashboard is served from different domain:**

```python
from flask_cors import CORS

# Allow dashboard to call API
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://dashboard.4tu.nl"],
        "methods": ["GET", "POST", "PATCH", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 7.5 API Versioning

**Maintain backward compatibility:**

```
/api/v1/statistics  → Old version (if exists)
/api/v2/statistics  → New version with faculty support

# In future:
/api/v3/statistics  → Breaking changes go here
```

**Deprecation Policy:**
- Support old version for at least 12 months
- Send `Deprecation` header in responses
- Provide migration guide

```python
@app.route('/api/v1/statistics')
def old_statistics():
    response = make_response(jsonify(get_old_stats()))
    response.headers['Deprecation'] = 'true'
    response.headers['Link'] = '</api/v2/statistics>; rel="successor-version"'
    response.headers['Sunset'] = 'Sat, 31 Dec 2025 23:59:59 GMT'
    return response
```

---

## 8. Data Protection

### 8.1 Encryption at Rest

**Virtuoso Database Encryption:**

Check if Virtuoso supports encryption at rest (depends on version/edition).

**If supported:**
```sql
-- Enable encryption for database
-- (Virtuoso-specific commands - check documentation)
```

**If NOT supported:**
- Use filesystem-level encryption (LUKS, dm-crypt on Linux)
- Use cloud provider encryption (AWS EBS encryption, Azure Disk Encryption)

**Field-Level Encryption (for highly sensitive data):**

```python
from cryptography.fernet import Fernet

# Generate key (store securely, e.g., in AWS KMS or environment variable)
KEY = os.environ.get('ENCRYPTION_KEY')
cipher = Fernet(KEY)

def encrypt_field(plaintext):
    """Encrypt a sensitive field."""
    return cipher.encrypt(plaintext.encode()).decode()

def decrypt_field(ciphertext):
    """Decrypt a sensitive field."""
    return cipher.decrypt(ciphertext.encode()).decode()

# Usage (if needed for extra-sensitive data)
account.encrypted_email = encrypt_field(user_email)
```

**Note:** For faculty assignments, encryption at rest at database level is likely sufficient. Field-level encryption adds complexity and may not be necessary.

### 8.2 Encryption in Transit

**Already covered:** HTTPS/TLS (Section 7.1)

**Additional:** Encrypt database connections too.

```python
# PostgreSQL connection with SSL
import psycopg2

conn = psycopg2.connect(
    host="db.4tu.nl",
    database="djehuty",
    user="app_user",
    password="***",
    sslmode='require',  # Force SSL
    sslrootcert='/path/to/ca-cert.pem'
)
```

### 8.3 Secure Configuration

**Don't Hardcode Secrets:**

```python
# ❌ BAD: Hardcoded secret
SECRET_KEY = "my-secret-key-123"

# ✅ GOOD: Environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
```

**Use Secret Management:**
- **Development:** `.env` file (NOT committed to git)
- **Production:** AWS Secrets Manager, Azure Key Vault, HashiCorp Vault

```python
# Using python-decouple for .env files
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DATABASE_URL = config('DATABASE_URL')
```

### 8.4 Backup & Disaster Recovery

**Backup Strategy:**

```bash
# Daily backups of RDF database
#!/bin/bash
# backup_virtuoso.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/virtuoso"

# Dump RDF database
isql-vt -U dba -P *** << EOF
  backup_context_clear();
  backup_online('$BACKUP_DIR/full_$DATE', 150);
  checkpoint;
EOF

# Encrypt backup
gpg --encrypt --recipient admin@4tu.nl $BACKUP_DIR/full_$DATE

# Upload to offsite storage (S3, Azure Blob, etc.)
aws s3 cp $BACKUP_DIR/full_$DATE.gpg s3://4tu-backups/virtuoso/

# Delete local backup after 7 days
find $BACKUP_DIR -name "full_*.gpg" -mtime +7 -delete
```

**Disaster Recovery Plan:**

| Scenario | Recovery Time Objective (RTO) | Recovery Point Objective (RPO) | Procedure |
|----------|-------------------------------|--------------------------------|-----------|
| Server failure | 4 hours | 1 day | Restore from daily backup |
| Database corruption | 2 hours | 1 day | Restore from daily backup |
| Data center outage | 8 hours | 1 day | Failover to backup datacenter |
| Accidental deletion | 1 hour | Real-time | Restore from audit log + backup |
| Ransomware attack | 24 hours | 1 day | Restore from offsite encrypted backup |

---

## 9. Compliance & Governance

### 9.1 Compliance Requirements

**GDPR (General Data Protection Regulation):**
- ✅ Lawful basis for processing (Legitimate Interest)
- ✅ User rights implemented (Access, Rectification, Erasure, etc.)
- ✅ Privacy Impact Assessment conducted
- ✅ Data retention policy (7 years for audit logs)
- ✅ Privacy notice provided to users

**Institutional Policies:**
- ✅ Comply with university data governance policies
- ✅ Follow 4TU.ResearchData terms of use
- ✅ Adhere to research data management guidelines

**Audit Requirements:**
- ✅ Comprehensive audit logging
- ✅ Audit logs retained for 7 years
- ✅ Audit log access controls

### 9.2 Security Incident Response Plan

**In Case of Security Breach:**

**Phase 1: Detection & Triage (0-2 hours)**
1. Incident detected (automated alert or manual report)
2. Assemble incident response team
3. Assess severity (low/medium/high/critical)
4. Isolate affected systems if necessary

**Phase 2: Containment (2-6 hours)**
1. Stop the attack (revoke credentials, block IPs, etc.)
2. Preserve evidence (logs, database snapshots)
3. Notify stakeholders (CISO, Data Protection Officer)

**Phase 3: Investigation (6-24 hours)**
1. Analyze logs and forensic data
2. Identify root cause
3. Determine scope of breach (what data was accessed?)
4. Document findings

**Phase 4: Notification (24-72 hours)**
1. If personal data breach:
   - Notify Data Protection Officer within 24 hours
   - Notify Data Protection Authority within 72 hours (GDPR requirement)
   - Notify affected users if high risk
2. Internal communication (management, legal, PR)

**Phase 5: Recovery (1-7 days)**
1. Patch vulnerabilities
2. Restore from backups if needed
3. Reset credentials
4. Verify system integrity

**Phase 6: Post-Incident Review (1-2 weeks)**
1. Conduct post-mortem
2. Update security procedures
3. Implement preventive measures
4. Train staff on lessons learned

**Incident Classification:**

| Severity | Example | Response Time | Notification |
|----------|---------|---------------|--------------|
| **Low** | Failed login attempts (normal) | Best effort | None |
| **Medium** | Unauthorized access attempt (blocked) | 4 hours | Security team |
| **High** | Successful unauthorized access | 1 hour | CISO, DPO |
| **Critical** | Personal data breach | Immediate | All stakeholders + authorities |

### 9.3 Security Audit Schedule

**Internal Audits:**
- **Quarterly**: Review audit logs for anomalies
- **Bi-annually**: Penetration testing (internal team)
- **Annually**: Comprehensive security audit

**External Audits:**
- **Annually**: Third-party penetration test
- **Every 2 years**: ISO 27001 assessment (if applicable)
- **As needed**: Compliance audits (GDPR, institutional policies)

### 9.4 Security Training

**For Development Team:**
- OWASP Top 10 training (annual)
- Secure coding practices (annual)
- GDPR awareness (annual)

**For Data Stewards:**
- GDPR user rights training (annual)
- Data handling best practices (annual)
- Incident response procedures (annual)

---

## 10. Implementation Roadmap

### Phase 1: Core Security (Before Production Launch)

**Timeline:** 2-3 weeks  
**Priority:** P0 (Critical)

| Task | Effort | Owner | Deliverable |
|------|--------|-------|-------------|
| 1. Implement authentication | 2 days | Backend Dev | Auth middleware |
| 2. Implement RBAC | 3 days | Backend Dev | Role checking decorators |
| 3. Add audit logging | 3 days | Backend Dev | Audit log table + functions |
| 4. Configure HTTPS/TLS | 1 day | DevOps | nginx config |
| 5. Add input validation | 2 days | Backend Dev | Validation schemas |
| 6. Implement rate limiting | 1 day | Backend Dev | Flask-Limiter setup |
| 7. Privacy Impact Assessment | 3 days | DPO + Team | PIA document |
| 8. Privacy notice | 1 day | Legal + Team | User-facing docs |
| 9. Security testing | 3 days | QA | Test report |

**Total Effort:** ~19 days (3-4 weeks with 1 developer)

### Phase 2: Enhanced Security (Post-Launch)

**Timeline:** 1-2 months after launch  
**Priority:** P1 (High)

| Task | Effort | Owner | Deliverable |
|------|--------|-------|-------------|
| 1. Centralized logging (ELK) | 1 week | DevOps | ELK stack deployed |
| 2. Automated security monitoring | 1 week | DevOps | Alerting rules |
| 3. Penetration testing | 1 week | External | Pentest report |
| 4. Database encryption at rest | 2 days | DevOps | Encrypted database |
| 5. Backup automation | 2 days | DevOps | Backup scripts + monitoring |
| 6. Disaster recovery drills | 1 day | Team | DR procedures tested |
| 7. Security documentation | 3 days | Team | Complete security guide |

**Total Effort:** ~4-5 weeks

### Phase 3: Advanced Security (Ongoing)

**Timeline:** Continuous improvement  
**Priority:** P2 (Medium)

- SSO integration (6-8 weeks)
- Multi-factor authentication (2-3 weeks)
- Advanced threat detection (AI-based anomaly detection)
- Security certifications (ISO 27001, SOC 2)

### Checklist: Production Launch Security Requirements

**Before going live, ensure:**

- [ ] ✅ Authentication enabled and tested
- [ ] ✅ RBAC implemented and tested
- [ ] ✅ Audit logging active
- [ ] ✅ HTTPS/TLS configured (A+ rating on SSL Labs)
- [ ] ✅ Input validation on all endpoints
- [ ] ✅ Rate limiting configured
- [ ] ✅ Privacy Impact Assessment approved by DPO
- [ ] ✅ Privacy notice published
- [ ] ✅ GDPR user rights endpoints tested
- [ ] ✅ Backups configured and tested
- [ ] ✅ Incident response plan documented
- [ ] ✅ Security training completed (team)
- [ ] ✅ Penetration test conducted (and issues fixed)
- [ ] ✅ Security sign-off from CISO

**Without these, DO NOT launch in production.**

---

## Appendix A: Security Checklist

**Development Phase:**
- [ ] Code review includes security check
- [ ] No secrets in source code
- [ ] Dependencies scanned for vulnerabilities (e.g., `safety check`)
- [ ] OWASP Top 10 considerations addressed

**Testing Phase:**
- [ ] Authentication tested (valid/invalid credentials)
- [ ] Authorization tested (role boundaries)
- [ ] Input validation tested (malicious inputs)
- [ ] Rate limiting tested (burst requests)
- [ ] HTTPS enforced (HTTP redirects to HTTPS)
- [ ] Audit logs verified (events are logged)

**Deployment Phase:**
- [ ] Production secrets stored in secret manager
- [ ] Database encrypted at rest
- [ ] HTTPS certificate valid and auto-renewed
- [ ] Backups configured and tested
- [ ] Monitoring and alerting active
- [ ] Incident response team notified

**Post-Deployment:**
- [ ] Monitor security logs daily
- [ ] Review audit logs weekly
- [ ] Update dependencies monthly
- [ ] Conduct security audit annually
- [ ] Renew SSL certificates (automated)

---

## Appendix B: Glossary

- **RBAC**: Role-Based Access Control
- **GDPR**: General Data Protection Regulation
- **PIA**: Privacy Impact Assessment
- **DPO**: Data Protection Officer
- **TLS**: Transport Layer Security
- **JWT**: JSON Web Token
- **CORS**: Cross-Origin Resource Sharing
- **OWASP**: Open Web Application Security Project
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective

---

## Appendix C: References

- **GDPR Official Text**: https://gdpr-info.eu/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **ISO 27001**: Information security management standard
- **SSL Labs**: https://www.ssllabs.com/ssltest/ (test HTTPS configuration)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Dec 10, 2024 | Documentation Team | Initial security and audit requirements |

**Next Review:** Before production launch (estimated Jan 2025)

**Approval Required From:**
- [ ] Chief Information Security Officer (CISO)
- [ ] Data Protection Officer (DPO)
- [ ] Legal Department
- [ ] Repository Manager

---

**END OF DOCUMENT**
