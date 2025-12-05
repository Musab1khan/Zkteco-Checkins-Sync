# ZKTeco Checkin Sync

---

## Executive Summary

**ZKTeco Checkin Sync** is an enterprise-grade Frappe/ERPNext application that automates the synchronization of employee attendance data from ZKTeco biometric devices. This solution provides real-time check-in/check-out transaction management with intelligent employee mapping, duplicate prevention, and comprehensive audit logging.

---

## Key Features

### Core Functionality

- **Real-time Synchronization**: Configurable sync intervals (10 seconds to 1 hour)
- **Bidirectional Support**: Both API mode (ZKBio Time Server) and Device mode (Port 4370)
- **Intelligent Log Type Detection**: 4-point detection algorithm for CHECK-IN/CHECK-OUT classification
- **Employee Mapping**: Automatic mapping via Employee ID, User ID, or custom fields
- **Duplicate Prevention**: Smart duplicate detection with log_type awareness
- **Device Health Monitoring**: Quick connectivity status checks without token requirement

### Advanced Capabilities

- **Dynamic Scheduler**: Auto-adjusting cron jobs based on configured frequency
- **Comprehensive Audit Logging**: Detailed error tracking and sync statistics
- **Transaction Preview**: Pre-sync transaction review with employee mapping validation
- **Separate IN/OUT Counting**: Distinct metrics for check-ins and check-outs
- **Multi-mode Support**: Automatic device mode detection (port 4370)

---


### ZKTeco Device Requirements

- **ZKBio Time Software**: Latest stable release installed
- **Network Configuration**: Device must be accessible from ERPNext server
- **API Access**: Enabled on ZKBio Time server
- **Authentication**: Superuser credentials available
- **Supported Models**: ZKTeco T&A devices with REST API support

---

## Installation Guide

### Step 1: Install the Application

```bash
# Navigate to your Frappe Bench directory
cd /path/to/frappe-bench

# Get the application
bench get-app https://github.com/Musab1khan/Zkteco-Checkins-Sync.git

# Install on your site
bench --site your-site.com install-app zkteco_checkins_sync

# Run database migrations
bench --site your-site.com migrate

# Rebuild assets
bench build
```

### Step 2: Configure ZKTeco Device

1. **Access ZKBio Time Software**
   - Open ZKBio Time on your ZKTeco server
   - Navigate to: System Settings → Communication

2. **Record Device Details**
   - Note the **Server IP** (e.g., 192.168.1.100)
   - Note the **Port** (typically 80 for API, 4370 for direct device)
   - Obtain **Superuser Username** and **Password**

3. **Enable API Access**
   - Ensure API/REST endpoints are enabled
   - Verify network connectivity from ERPNext server to ZKTeco device

### Step 3: Configure in ERPNext

1. **Navigate to ZKTeco Config**
   - URL: `/app/zkteco-config`
   - Or: Setup → ZKTeco Checkin Sync → ZKTeco Config

2. **Fill Basic Configuration**
   - Check **Enable Sync**
   - Enter **Server IP**
   - Enter **Server Port**

3. **Set Credentials**
   - Enter **Username** (ZKBio Time superuser)
   - Enter **Password** (corresponding password)

4. **Register API Token**
   - Click **"Register API Token"** button
   - Wait for token generation and save

5. **Configure Sync Settings**
   - Select **Sync Frequency** (recommended: 5 minutes for standard setups)
   - Frequency options: 10s, 30s, 1m, 2m, 5m, 10m, 15m, 30m, 1h

---

## Usage Guide

### Device Connection Status Check

**Before anything else, verify device connectivity:**

1. Fill in **Server IP** and **Server Port**
2. Click **"🔍 Check Device Status"** button
3. Result will show:
   - ✅ **GREEN**: Device is reachable and online
   - ❌ **RED**: Device unreachable (check power, network, firewall)

**No token required for this check!**

### Testing Connection with Transactions

1. Click **"Test Connection"** button
2. System will display:
   - Total transactions from today
   - Employee mapping status (Found/Not Found)
   - Sample transaction preview with IN/OUT classification
   - Response status and timestamps

### Manual Sync Operations

1. Open ZKTeco Config form
2. Click **"Manual Sync"** in Actions menu
3. Monitor Employee Checkin list for new records
4. Check log for any errors: Error Log doctype

### Monitoring Sync Status

1. Click **"Sync Status"** in Actions menu
2. View dashboard showing:
   - Sync enabled status
   - Configured frequency
   - Last sync timestamp
   - Recent check-ins (total, IN count, OUT count)
   - Server and token configuration status

---

## Employee Mapping

### How It Works

The system matches ZKTeco employee codes to ERPNext employees using multiple methods in priority order:

1. **Employee ID field** (Primary method)
   - ZKTeco `emp_code` = ERPNext `Employee.employee`
   - Example: "EMP001" matches to Employee with ID "EMP001"

2. **User ID field** (Secondary method)
   - ZKTeco `emp_code` = ERPNext `Employee.user_id`
   - Example: "john.doe" matches to Employee with User ID "john.doe"

3. **Custom Attendance Device ID** (Advanced method)
   - Requires custom field `attendance_device_id` on Employee doctype
   - ZKTeco `emp_code` = ERPNext `Employee.attendance_device_id`

### Setup Best Practices

**Recommended: Use Employee ID Method**

```
Employee Master Configuration:
├─ Employee (primary key): EMP001
├─ Employee Name: John Doe
├─ User ID: (optional, alternate mapping)
└─ Department: Sales
```

**Verification Query:**

```sql
SELECT employee, employee_name, user_id FROM `tabEmployee` 
WHERE employee IN (SELECT DISTINCT emp_code FROM zkteco_transactions)
```

### Troubleshooting Unmapped Employees

If transactions show "Employee Not Found":

1. **Verify Employee Records Exist**
   ```
   HR → Employee List → Search for employee code
   ```

2. **Check Code Format Consistency**
   - ZKTeco: "EMP001" vs ERPNext: "emp001" (case sensitivity)
   - Remove leading/trailing spaces
   - Verify no special characters

3. **Enable Custom Field Method**
   - Customize Employee doctype
   - Add field: `attendance_device_id` (Data type)
   - Set values matching ZKTeco emp_codes

---

## Technical Architecture

### Transaction Flow Diagram

```
ZKTeco Device
    ↓
[API/Device Mode]
    ↓
detect_log_type() → Classify IN/OUT
    ↓
find_employee_by_code() → Employee lookup
    ↓
[Duplicate Check with log_type]
    ↓
create_employee_checkin() → Create record
    ↓
ERPNext Employee Checkin
```

### Log Type Detection Logic

The system uses a 4-point detection algorithm:

1. **punch_state (numeric)**: 0=IN, 1=OUT
2. **punch_state_display (text)**: "Check In"/"Check Out"
3. **log_type (direct field)**: Explicit IN/OUT value
4. **punch (device mode)**: 0=IN, 1=OUT (pyzk library)

This ensures compatibility with different ZKTeco API versions and configurations.

### Duplicate Prevention

**Before Creating Record:**

```python
existing = frappe.db.exists("Employee Checkin", {
    "employee": employee,
    "time": punch_datetime,
    "device_id": device_id,
    "log_type": log_type  # Critical: prevents false duplicates
})
```

Without `log_type` in the check, the same timestamp would incorrectly block the OUT transaction.

---

## API Configuration Modes

### Mode 1: ZKBio API Server (Recommended)

**Use When:**
- ZKBio Time server is running
- Port 80 (or custom) is available
- Need periodic (not real-time) sync

**Configuration:**
```
Server IP: 192.168.1.100
Server Port: 80
Credentials: Superuser username/password
Sync Frequency: 5-15 minutes recommended
```

**Advantages:**
- Stable, well-documented API
- Historical transaction retrieval
- Flexible filtering options

### Mode 2: Device Direct Connection (Port 4370)

**Use When:**
- Device is on network (no ZKBio server)
- Need real-time sync capability
- Prefer direct device communication

**Configuration:**
```
Server IP: 192.168.1.200
Server Port: 4370
Credentials: Not required (auto-detected)
Sync Frequency: 10-30 seconds recommended
```

**Advantages:**
- No token management required
- Real-time synchronization
- Direct device communication

**Requirements:**
- `pyzk` library must be installed
- Port 4370 must be accessible
- Device firmware supports USB fingerprint protocol

---

## Performance Optimization

### Recommended Settings by Organization Size

| Organization Size | Sync Frequency | Rationale |
|-------------------|----------------|-----------|
| **< 50 employees** | 30-60 seconds | Low transaction volume |
| **50-200 employees** | 2-5 minutes | Balanced load |
| **200-500 employees** | 5-10 minutes | Medium load management |
| **500+ employees** | 10-15 minutes | Heavy processing required |

### Database Optimization

Add these indexes to improve query performance:

```sql
-- Performance indexes
ALTER TABLE `tabEmployee Checkin` 
ADD INDEX `idx_device_time` (`device_id`, `time`);

ALTER TABLE `tabEmployee Checkin` 
ADD INDEX `idx_employee_time` (`employee`, `time`);

ALTER TABLE `tabEmployee Checkin` 
ADD INDEX `idx_log_type` (`log_type`, `creation`);

-- Reduce scan time for duplicate checks
ALTER TABLE `tabEmployee Checkin` 
ADD UNIQUE KEY `uq_emp_time_type` (`employee`, `time`, `log_type`);
```

### Scheduled Job Optimization

The system automatically adjusts cron jobs based on frequency:

```
10-30 seconds   → */1 * * * * (every minute)
30s-5 minutes   → */5 * * * * (every 5 minutes)
5-10 minutes    → */10 * * * * (every 10 minutes)
15+ minutes     → hourly or custom
```

---

## Troubleshooting Guide

### Issue: "Device Not Connected" Status

**Check List:**
1. Verify ZKTeco device is powered on
2. Ping device from ERPNext server: `ping 192.168.1.100`
3. Check firewall allows port 80 (or custom): `telnet 192.168.1.100 80`
4. Verify network cable connection
5. Check ZKBio Time software is running

**Command Line Verification:**
```bash
# Test connectivity
curl -I http://192.168.1.100:80/

# Test specific API endpoint
curl http://192.168.1.100:80/iclock/api/transactions/
```

### Issue: "Invalid Token" or "Token Expired"

**Solutions:**
1. Clear existing token in ZKTeco Config
2. Re-enter credentials
3. Click "Register API Token" again
4. Verify superuser credentials are correct
5. Check user has API access permissions in ZKBio Time

### Issue: "Employee Not Found" After Sync

**Diagnostics:**

```python
# In Frappe Console, check what's being mapped
frappe.db.get_list("Employee Checkin", {
    "device_id": ["like", "%ZKTeco%"],
    "creation": [">=", frappe.utils.get_datetime().date()]
}, ["name", "employee", "log_type", "time"])

# Check employee codes in ZKTeco vs ERPNext
SELECT DISTINCT emp_code FROM zkteco_transactions
SELECT employee FROM `tabEmployee`
```

**Resolution Steps:**
1. Export ZKTeco employee list with codes
2. Import to ERPNext Employee doctype
3. Ensure Employee ID field matches ZKTeco emp_code
4. Run Test Connection to verify mapping
5. Retry Manual Sync

### Issue: Only CHECK-IN Records, No CHECK-OUT

**Root Cause:** Old code didn't include `log_type` in duplicate check

**Fix Applied in v1.0:**
```python
# Correct duplicate check (now in place)
existing = frappe.db.exists("Employee Checkin", {
    "employee": employee,
    "time": punch_datetime,
    "device_id": device_id,
    "log_type": log_type  # ← This prevents false duplicates
})
```

**Verification:**
```python
# Check your data has both IN and OUT
frappe.db.count("Employee Checkin", {
    "log_type": "IN",
    "device_id": ["like", "%ZKTeco%"]
})

frappe.db.count("Employee Checkin", {
    "log_type": "OUT",
    "device_id": ["like", "%ZKTeco%"]
})
```

### Issue: Sync Takes Too Long

**Performance Tuning:**
1. Increase sync frequency interval (1 hour instead of 5 minutes)
2. Add database indexes (see Performance Optimization section)
3. Check database query log for slow queries: `SHOW PROCESSLIST;`
4. Reduce number of duplicate check methods

**Monitor Sync Performance:**
```python
# Check sync duration
frappe.db.get_single_value("ZKTeco Config", "last_sync")

# Count recent transactions
frappe.db.count("Employee Checkin", {
    "device_id": ["like", "%ZKTeco%"],
    "modified": [">=", frappe.utils.add_minutes(frappe.utils.now(), -5)]
})
```

---

## API Reference

### Core Functions

#### `check_device_status(server_ip, server_port)`

**Purpose:** Quick device connectivity check without authentication

**Parameters:**
- `server_ip` (string): Device IP address
- `server_port` (int): Device port number

**Returns:**
```json
{
    "connected": true,
    "ip": "192.168.1.100",
    "port": 80,
    "response_time": 45.23,
    "message": "Device is online"
}
```

**Usage:**
```python
frappe.call({
    method: "zkteco_checkins_sync...check_device_status",
    args: {server_ip: "192.168.1.100", server_port: 80},
    callback: (r) => console.log(r.message)
})
```

#### `register_api_token(server_ip, server_port, username, password)`

**Purpose:** Generate and register API authentication token

**Parameters:**
- `server_ip` (string): ZKBio server IP
- `server_port` (int): ZKBio server port
- `username` (string): Superuser username
- `password` (string): Superuser password

**Returns:**
```json
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### `test_connection()`

**Purpose:** Verify API connectivity and preview today's transactions

**Returns:**
```json
{
    "ok": true,
    "status_code": 200,
    "total_transactions": 150,
    "transactions_preview": [...],
    "message": "Found 150 transactions for 2025-12-05"
}
```

#### `manual_sync()`

**Purpose:** Trigger immediate synchronization of transactions

**Returns:**
```json
{
    "success": true,
    "message": "Sync completed successfully"
}
```

#### `get_sync_status()`

**Purpose:** Get current sync status and statistics

**Returns:**
```json
{
    "enabled": true,
    "sync_frequency": "300",
    "last_sync": "2025-12-05 14:30:15",
    "recent_checkins_24h": 245,
    "checkins_in_24h": 122,
    "checkins_out_24h": 123,
    "server_configured": true,
    "token_configured": true
}
```

---

## Security Considerations

### Authentication & Authorization

**API Token Security:**
- Tokens are stored encrypted in database
- Auto-expires after configured period (recommend 90 days)
- Rotate tokens regularly: `Register API Token` button
- Never share token in logs or error messages

**Access Control:**
- Restricted to System Manager and HR Manager roles
- HR User role can view only
- Audit trail maintained in database

**Best Practices:**
1. Use dedicated ZKBio superuser account for this integration
2. Limit superuser account IP access if possible
3. Change superuser password quarterly
4. Monitor "last_sync" for unusual patterns

### Data Security

**In Transit:**
- Use HTTPS for ZKBio API connections (if available)
- Verify SSL certificates if enabled
- Keep ZKTeco device on private network

**At Rest:**
- Employee Checkin records inherit ERPNext encryption
- Database backups automatically encrypted
- API tokens encrypted in database

**Audit & Compliance:**
- All sync operations logged in Error Log doctype
- Manual sync tracked with timestamps
- Device connection attempts logged
- Maintenance audit trail available

---

## Advanced Configuration

### Custom Employee Code Mapping

**Scenario:** Your ZKTeco uses custom employee codes not matching ERPNext

**Solution: Create Mapping Custom Field**

```python
# In Frappe Console:
doc = frappe.get_doc("Employee", "EMP001")
doc.set("custom_attendance_device_id", "ZK_CODE_001")
doc.save()

# Verify
frappe.db.get_value("Employee", "EMP001", "custom_attendance_device_id")
```

**Then modify `find_employee_by_code()` to use it:**

```python
def find_employee_by_code(emp_code):
    # Try employee field first
    employee = frappe.db.get_value("Employee", {"employee": emp_code}, "name")
    if employee:
        return employee
    
    # Try custom field
    employee = frappe.db.get_value("Employee", 
        {"custom_attendance_device_id": emp_code}, "name")
    if employee:
        return employee
    
    return None
```

### Batch Employee Import

**Mass Sync ZKTeco Employees:**

```python
import frappe
from frappe.client import insert

zkteco_employees = [
    {"emp_code": "001", "name": "John Doe"},
    {"emp_code": "002", "name": "Jane Smith"},
]

for emp in zkteco_employees:
    doc = frappe.new_doc("Employee")
    doc.employee = emp["emp_code"]
    doc.employee_name = emp["name"]
    doc.status = "Active"
    doc.insert()

frappe.db.commit()
print(f"Imported {len(zkteco_employees)} employees")
```

---

## Monitoring & Reporting

### Sync Status Dashboard

Navigate to ZKTeco Config and click "Sync Status" to see:
- Real-time sync state
- Last sync timestamp
- 24-hour check-in counts (IN vs OUT)
- Configuration status indicators

### Custom Reports

**Report 1: Today's Attendance Summary**

```python
frappe.db.sql("""
    SELECT 
        employee,
        COUNT(CASE WHEN log_type='IN' THEN 1 END) as checkins,
        COUNT(CASE WHEN log_type='OUT' THEN 1 END) as checkouts
    FROM `tabEmployee Checkin`
    WHERE DATE(creation) = CURDATE()
    AND device_id LIKE '%ZKTeco%'
    GROUP BY employee
    ORDER BY employee
""")
```

**Report 2: Device Sync Performance**

```python
frappe.db.sql("""
    SELECT 
        COUNT(*) as total_synced,
        COUNT(CASE WHEN log_type='IN' THEN 1 END) as in_count,
        COUNT(CASE WHEN log_type='OUT' THEN 1 END) as out_count,
        DATE(last_modified) as sync_date
    FROM `tabEmployee Checkin`
    WHERE device_id LIKE '%ZKTeco%'
    GROUP BY DATE(last_modified)
    ORDER BY sync_date DESC
    LIMIT 30
""")
```

### Error Log Monitoring

Check for sync errors:

```python
frappe.db.get_list("Error Log", {
    "title": ["like", "%ZKTeco%"],
    "creation": [">=", frappe.utils.get_datetime().subtract(days=1)]
}, ["error", "creation"])
```

---

## Maintenance & Support

### Regular Maintenance Tasks

**Daily:**
- Check Error Log for ZKTeco errors
- Monitor Device Status button shows green
- Verify sync completing on schedule

**Weekly:**
- Review sync statistics
- Check employee mapping quality
- Audit IN/OUT count ratio (~50/50 expected)

**Monthly:**
- Rotate API token
- Update ZKBio Time software if new version available
- Review performance metrics
- Backup configuration


---

## Upgrade Guide

### Upgrading to Latest Version

```bash
# Navigate to bench directory
cd /path/to/frappe-bench

# Update app
bench pull zkteco_checkins_sync

# Run migrations
bench --site your-site.com migrate

# Rebuild assets
bench build

# Clear cache
bench --site your-site.com clear-cache
```



---

