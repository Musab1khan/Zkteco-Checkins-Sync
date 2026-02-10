# ZKTeco Checkin Sync

**Enterprise-grade Frappe/ERPNext application for automated employee attendance synchronization from ZKTeco biometric devices**

---

## 🎯 Executive Summary

ZKTeco Checkin Sync automates the synchronization of employee attendance data from ZKTeco biometric devices into ERPNext Employee Checkin records. This solution eliminates manual data entry, provides real-time transaction management, and includes intelligent employee mapping with comprehensive audit logging.

<<<<<<< HEAD
- **Real-time Synchronization**: Configurable sync intervals (10 seconds to 1 hour)
- **Bidirectional Support**: Both API mode (ZKBio Time Server) and Device mode (Port 4370)
- **Intelligent Log Type Detection**: Sequence-based algorithm for CHECK-IN/CHECK-OUT classification
- **Employee Mapping**: Automatic mapping via Employee ID, User ID, or custom fields
- **Duplicate Prevention**: Smart duplicate detection with log_type awareness
- **Device Health Monitoring**: Quick connectivity status checks without token requirement
=======
**Key Value Proposition:**
- ✅ Real-time or scheduled synchronization (configurable 10 seconds to 1 hour)
- ✅ Bidirectional support (ZKBio API Server + Direct Device Connection)
- ✅ Intelligent IN/OUT detection with sequence-aware processing
- ✅ Automatic duplicate prevention and employee mapping
- ✅ Zero manual intervention after initial setup

---

## 🌟 Core Features

### Real-Time Sync Capabilities
- **Configurable Frequency**: 10 seconds to 1 hour sync intervals
- **Dual Mode Support**: 
  - ZKBio Time Server API (Recommended for most setups)
  - Direct Device Mode via Port 4370 (Real-time sync)
- **Smart Duplicate Prevention**: Log-type aware duplicate detection
- **Intelligent Log Type Detection**: 4-point algorithm ensuring accuracy

### Employee Management
- **Multi-method Mapping**: Employee ID, User ID, or custom field matching
- **Batch Import Support**: Mass employee synchronization
- **Mapping Validation**: Pre-sync verification with detailed reports
>>>>>>> upstream/multi-devices

### Advanced Capabilities
- **Dynamic Scheduler**: Auto-adjusting cron jobs based on frequency
- **Comprehensive Audit Trail**: Error tracking and sync statistics
- **Transaction Preview**: Pre-sync review with employee mapping validation
- **Separate IN/OUT Counting**: Distinct metrics for arrivals and departures
- **Device Health Monitoring**: Quick connectivity checks without authentication

### Maintenance Tools
- **One-Click Fixes**: Correct misclassified IN/OUT records
- **Duplicate Removal**: Clean up redundant transactions
- **Sync Status Dashboard**: Real-time statistics and health indicators

### 🆕 Maintenance & Fix Tools (NEW!)

- **🔧 One-Click Fix IN/OUT Types**: Automatically fix all existing records with incorrect log types
- **🗑️ Remove Duplicates**: Clean up duplicate checkin records with one click
- **Sequence-Based Detection**: Intelligent alternating IN/OUT logic (First=IN, Last=OUT, Middle=Alternate)
- **No Manual Intervention**: Fully automated fixes for common data issues

---

## 📋 Prerequisites

### System Requirements
- **Frappe**: v13.0 or higher
- **Python**: 3.10 or higher
- **Database**: MySQL 5.7+ or MariaDB 10.3+
- **Network**: Direct connectivity to ZKTeco device/server

### ZKTeco Requirements
- **Device**: ZKTeco T&A biometric terminal (T2391, K40, etc.)
- **ZKBio Software**: Latest stable version installed (for API mode)
- **Network Configuration**: Device accessible from ERPNext server
- **API Access**: Enabled in ZKBio Time settings
- **Credentials**: Superuser username and password available

### Network Checklist
- [ ] ZKTeco device is on the same network (or routable from ERPNext server)
- [ ] Firewall allows outbound connections to device IP and port
- [ ] Network cables are properly connected
- [ ] Device has stable power supply
- [ ] No IP conflicts on the network

---

## 📦 Installation Guide

### Step 1: Clone and Install the Application

```bash
# Navigate to your Frappe Bench directory
cd /path/to/frappe-bench

# Download the application
bench get-app https://github.com/Musab1khan/Zkteco-Checkins-Sync.git

# Install on your site
bench --site your-site.local install-app zkteco_checkins_sync

# Run database migrations
bench --site your-site.local migrate

# Rebuild front-end assets
bench build
```

### Step 2: Configure ZKTeco Device

#### For ZKBio Time Server Setup:

1. **Access ZKBio Time Software**
   - Open ZKBio Time application on your ZKTeco server
   - Navigate to: **System Settings → Communication**

2. **Record Device Details**
   - **Server IP**: IPv4 address (e.g., 192.168.1.100)
   - **Server Port**: Default 80 (or custom if configured)
   - **Superuser Credentials**: Username and password for API access

3. **Enable API Access**
   - Ensure REST API is enabled in ZKBio settings
   - Verify SSL certificate (if HTTPS is configured)
   - Test connectivity using curl or Postman

#### For Direct Device Mode (Port 4370):

1. **Device Preparation**
   - Ensure device is on network (no ZKBio server required)
   - Device firmware must support USB fingerprint protocol
   - Network must have direct line of sight to device

2. **Library Installation**
   ```bash
   # SSH into your Frappe server
   cd /path/to/frappe-bench
   
   # Install pyzk library for device mode
   pip install pyzk --break-system-packages
   ```

### Step 3: Configure in ERPNext

#### Basic Setup

1. **Navigate to ZKTeco Config**
   - URL: `/app/zkteco-config`
   - Or: **Home → Setup → ZKTeco Checkin Sync → ZKTeco Config**

2. **Enable Synchronization**
   - Check: **Enable Sync** ☑️
   - Enter: **Server IP** (e.g., 192.168.1.100)
   - Enter: **Server Port** (e.g., 80 for API, 4370 for device mode)

3. **Set Credentials** (API Mode Only)
   - Enter: **Username** (ZKBio superuser account)
   - Enter: **Password** (Corresponding password)

4. **Register API Token** (API Mode Only)
   - Click: **"Register API Token"** button
   - System will generate and save token automatically
   - ✅ You'll see confirmation: "Token registered successfully"

5. **Configure Sync Frequency**
   - Select: **Sync Frequency** from dropdown
   - Recommended settings:
     - Small organizations (< 50 emp): 30-60 seconds
     - Medium organizations (50-200 emp): 2-5 minutes
     - Large organizations (500+ emp): 10-15 minutes

#### Validation Steps

```
Before saving configuration:
1. ☑️ Check Device Status
   - Click: 🔍 Check Device Status
   - Expected: Green indicator + "Device is online"

2. ☑️ Test Connection
   - Click: Test Connection
   - Expected: Lists today's transactions with employee mapping

3. ☑️ Manual Sync (Optional)
   - Click: Actions → Manual Sync
   - Check: Employee Checkin list for new records
```

---

## 🚀 Usage Guide

### Quick Start Workflow

```
1. Configure ZKTeco Device
   └─ Enter IP, Port, Credentials

2. Register API Token
   └─ Click "Register API Token" button

3. Check Device Status
   └─ Click 🔍 Check Device Status
   └─ Verify: 🟢 Green indicator

4. Test Connection
   └─ Click Test Connection
   └─ Verify: Transaction preview shows data

5. Trigger Manual Sync
   └─ Actions → Manual Sync
   └─ Check: Employee Checkin list updated

6. Enable Scheduled Sync
   └─ Sync Frequency dropdown
   └─ Save configuration
   └─ Automatic syncing now active
```

### Device Connection Status Check

The fastest way to verify your device is reachable:

1. **No Token Required**: This check works without API authentication
2. **Click**: 🔍 **Check Device Status** button
3. **Result Indicators**:
   - ✅ **GREEN**: Device online, responding normally
   - ❌ **RED**: Device unreachable (network issue, power off, firewall)

**What to do if RED:**
```bash
# Test from command line (SSH into Frappe server)
ping 192.168.1.100

# Check port connectivity
telnet 192.168.1.100 80
# Expected: Connected (or Connection refused if port wrong)

# For device mode, test port 4370
telnet 192.168.1.100 4370
```

### Testing Connection with Transactions

1. **Click**: **Test Connection** button
2. **System displays**:
   - Total transactions from today
   - Employee mapping status (✅ Found / ⚠️ Not Found)
   - Sample transaction preview (last 5 transactions)
   - IN/OUT classification for each

3. **Review Output**:
   ```
   Employee: john.doe (ERPNext) ✅ Mapped
   Time: 2024-12-08 08:30:45
   Type: IN (Check In)
   
   Employee: Unknown (⚠️ Not Found)
   Time: 2024-12-08 09:15:00
   Type: OUT (Check Out)
   ```

4. **If many unmapped**: See Employee Mapping section below

### Manual Sync Operations

Useful for testing or catching up on missed transactions:

```
Steps:
1. Open ZKTeco Config form
2. Click: Actions → Manual Sync
3. Wait for completion (1-2 minutes for large datasets)
4. Check: Employee Checkin list
5. Verify: New records created with correct dates/times
```

**Check sync results:**
- Navigate to: **Human Resources → Employee Checkin**
- Filter: `device_id` contains "ZKTeco"
- Sort: `creation` descending
- Verify: Latest records have today's date

### Monitoring Sync Status

Real-time dashboard showing synchronization health:

1. **Click**: **Actions → Sync Status**
2. **Dashboard shows**:
   - ✅ Sync enabled status
   - ⏱️ Configured frequency
   - 📊 Last sync timestamp
   - 📈 Recent check-ins (24h count)
   - 📍 IN/OUT breakdown
   - 🖧 Server and token configuration

**Example Output:**
```
Sync Enabled: ✅ Yes
Sync Frequency: Every 300 seconds (5 minutes)
Last Sync: 2024-12-08 14:30:15
Recent Check-ins (24h): 245
  ✅ Check-ins IN: 122
  ❌ Check-outs OUT: 123
Server Configured: ✅ Yes
Token Configured: ✅ Yes
```

### 🆕 Maintenance Operations (NEW!)

#### Fix Incorrect IN/OUT Log Types

If you have existing records with wrong IN/OUT types (e.g., all showing as IN):

1. Open ZKTeco Config form
2. Click **"🔧 Fix IN/OUT Types"** in Maintenance menu
3. Confirm the action
4. System will automatically:
   - Analyze all checkin records by employee and date
   - Apply intelligent sequence logic (First punch = IN, Last = OUT, Middle = Alternate)
   - Update incorrect records
   - Show summary of fixed records

**Use this when:**
- All records show as "IN" but should have "OUT" entries
- After importing old data
- After fixing sync logic issues

#### Remove Duplicate Checkins

If you have duplicate records (same employee, same time, same log type):

1. Open ZKTeco Config form
2. Click **"🗑️ Remove Duplicates"** in Maintenance menu
3. Confirm the action
4. System will:
   - Find all duplicate records
   - Keep the oldest record (first created)
   - Delete newer duplicates
   - Show count of removed records

**Use this when:**
- Multiple syncs created duplicate entries
- Same transaction appears multiple times
- After data migration issues

---

## 👥 Employee Mapping

### How It Works

The system intelligently matches ZKTeco employee codes to ERPNext employees using this priority order:

#### Priority 1: Employee ID (Recommended) 🌟
```
ZKTeco emp_code = ERPNext Employee.employee

Example:
ZKTeco: "EMP001" 
↓
ERPNext Employee: ID = "EMP001"
✅ MATCHED
```

#### Priority 2: User ID
```
ZKTeco emp_code = ERPNext Employee.user_id

Example:
ZKTeco: "john.doe"
↓
ERPNext Employee: User ID = "john.doe"
✅ MATCHED
```

#### Priority 3: Custom Field (Advanced)
```
<<<<<<< HEAD
ZKTeco Device (Fingerprint Punch)
    ↓
[API Mode or Device Mode (Port 4370)]
    ↓
fetch_zkteco_transactions() → Get all transactions
    ↓
adjust_checkin_sequence() → Group by employee & date
    ↓
Sequence-Based Detection:
  - Single punch → IN
  - First punch of day → IN
  - Last punch of day → OUT
  - Middle punches → Alternate (IN→OUT→IN→OUT)
    ↓
create_employee_checkin() → With correct log_type
    ↓
[Duplicate Check: employee + time + log_type]
    ↓
ERPNext Employee Checkin Record
```

### Log Type Detection Logic (Sequence-Based)

**🆕 NEW: Intelligent Sequence Detection**

The system now uses a **smart sequence-based algorithm** that works perfectly for Device Mode (Port 4370):

1. **Group by Employee & Date**: All punches are grouped per employee per day
2. **Sort by Time**: Chronological order ensures correct sequence
3. **Apply Rules**:
   - If only **1 punch** → **IN** (employee forgot to punch out)
   - **First punch** of the day → **IN** (morning arrival)
   - **Last punch** of the day → **OUT** (evening departure)
   - **Middle punches** → Alternate between IN and OUT

**Example:**
```
Employee: John Doe | Date: 2025-12-08

09:00 AM → IN  (First punch)
12:00 PM → OUT (Previous was IN)
01:00 PM → IN  (Previous was OUT)
06:00 PM → OUT (Last punch)
```

**Benefits:**
- ✅ Works even when device doesn't send punch type
- ✅ Handles multiple breaks during the day
- ✅ Automatically fixes incorrect sequences
- ✅ No manual intervention needed

**Fallback Detection (API Mode):**

For API mode, the system also checks these fields:
=======
ZKTeco emp_code = ERPNext Employee.attendance_device_id

Requires: Custom field on Employee doctype
Example:
ZKTeco: "ZK_CODE_001"
↓
ERPNext Employee: Custom Field = "ZK_CODE_001"
✅ MATCHED
```

### Setup: Recommended Method (Employee ID)

#### Option A: Manual Setup (Small Team)
>>>>>>> upstream/multi-devices

```
For each employee:
1. Go to: HR → Employee List
2. Open employee record
3. Set: Employee ID = ZKTeco emp_code
   Example: "EMP001" (must match exactly)
4. Save
```

#### Option B: Bulk Import (Large Team)

```python
# In Frappe Console (Bench Console)
import frappe
from datetime import datetime

# CSV data: employee_id, employee_name, user_id
data = [
    ["EMP001", "John Doe", "john.doe"],
    ["EMP002", "Jane Smith", "jane.smith"],
    ["EMP003", "Bob Johnson", "bob.johnson"],
]

for row in data:
    emp_id, emp_name, user_id = row
    
    # Check if employee exists
    existing = frappe.db.get_value("Employee", {"employee": emp_id}, "name")
    
    if existing:
        # Update existing
        frappe.db.set_value("Employee", existing, {
            "employee_name": emp_name,
            "user_id": user_id
        })
    else:
        # Create new
        doc = frappe.new_doc("Employee")
        doc.employee = emp_id
        doc.employee_name = emp_name
        doc.user_id = user_id
        doc.status = "Active"
        doc.insert()

frappe.db.commit()
print(f"✅ Processed {len(data)} employees")
```

#### Option C: Custom Field Method (Most Flexible)

```python
# Step 1: Add custom field to Employee
doc = frappe.get_doc("Employee", "EMP001")
doc.set("attendance_device_id", "ZK_CODE_001")
doc.save()

# Step 2: Update code to use custom field
# (Already supported in zkteco_config.py find_employee_by_code())
```

### Verification Checklist

```sql
-- Check which employees are mapped
SELECT 
    employee,
    employee_name,
    user_id,
    CASE 
        WHEN employee IN (SELECT emp_code FROM zkteco_transactions) THEN '✅ HAS_DATA'
        ELSE '⚠️ NO_DATA'
    END as zkteco_status
FROM `tabEmployee`
WHERE status = 'Active'
ORDER BY employee;

-- Check unmapped ZKTeco codes
SELECT DISTINCT emp_code 
FROM zkteco_transactions
WHERE emp_code NOT IN (
    SELECT employee FROM `tabEmployee`
    UNION
    SELECT user_id FROM `tabEmployee`
)
ORDER BY emp_code;
```

### Troubleshooting: Unmapped Employees

**Symptom**: Transactions show "Employee Not Found" in preview

**Root Causes & Fixes**:

1. **Case Sensitivity Mismatch**
   ```
   ZKTeco: "EMP001"
   ERPNext: "emp001"  ❌ Wrong case
   
   Fix: Make codes match exactly (case-sensitive)
   ```

2. **Whitespace Issues**
   ```
   ZKTeco: "EMP001 " (trailing space)
   ERPNext: "EMP001" ❌ Doesn't match
   
   Fix: Trim whitespace in both systems
   ```

3. **Employee Record Doesn't Exist**
   ```
   Fix: Create missing employees in HR → Employee
   ```

4. **Wrong Field Used**
   ```
   Example: Employee ID = "EMP001" but User ID = "john.doe"
   If ZKTeco uses "john.doe", set that as the primary matching field
   ```

**Step-by-Step Recovery**:

```
1. Export ZKTeco employee codes
   → Actions → Sync Status → View pending
   → Copy all emp_codes

2. Compare with ERPNext
   → HR → Employee List
   → Filter by codes from step 1

3. For missing employees
   → Create new Employee record with matching ID

4. For wrong codes
   → Update Employee.employee_id to match ZKTeco

5. Retry sync
   → Manual Sync → Check results
```

---

## 🔧 Configuration Options

### Sync Frequency Guide

| Frequency | Use Case | Employees | Database Load |
|-----------|----------|-----------|---------------|
| 10-30s | Real-time tracking | <20 | Very High |
| 1 minute | Live attendance | 20-50 | High |
| 2-5 min | Standard setup | 50-200 | Medium |
| 10 min | Medium org | 200-500 | Low |
| 15-30 min | Large org | 500-1000 | Very Low |
| 1 hour | Minimal sync | 1000+ | Minimal |

**Default Recommendation**: 5 minutes (300 seconds)

### API Mode vs Device Mode

#### API Mode (ZKBio Server) - RECOMMENDED

**When to use:**
- ✅ ZKBio Time server is available
- ✅ Multiple devices to sync
- ✅ Historical data retrieval needed
- ✅ Stable periodic sync preferred

**Configuration:**
```
Server IP: 192.168.1.100
Server Port: 80 (or custom)
Credentials: Superuser username/password
Sync Frequency: 5-15 minutes
```

**Pros:**
- Well-documented REST API
- Supports flexible filtering
- Batch transaction retrieval
- Token-based authentication

**Cons:**
- Requires ZKBio server running
- Slightly more latency
- Token management needed

#### Device Mode (Port 4370) - REAL-TIME

**When to use:**
- ✅ Direct device access (no server)
- ✅ Real-time sync needed
- ✅ Single device setup
- ✅ Simpler infrastructure

**Configuration:**
```
Server IP: 192.168.1.200 (device IP)
Server Port: 4370 (MUST be 4370)
Credentials: None required
Sync Frequency: 10-30 seconds
```

**Pros:**
- No token needed
- Lowest latency
- Direct device communication
- Real-time data

**Cons:**
- Requires pyzk library
- Higher CPU usage (frequent sync)
- Limited to single device
- Port 4370 must be accessible

---

## 📊 Database Optimization

For large deployments (500+ employees), add these indexes:

```sql
-- Performance indexes
ALTER TABLE `tabEmployee Checkin` 
ADD INDEX `idx_device_time` (`device_id`, `time`);

ALTER TABLE `tabEmployee Checkin` 
ADD INDEX `idx_employee_time` (`employee`, `time`);

ALTER TABLE `tabEmployee Checkin` 
ADD INDEX `idx_log_type` (`log_type`, `creation`);

-- Prevent duplicates
ALTER TABLE `tabEmployee Checkin` 
ADD UNIQUE KEY `uq_emp_time_type` 
    (`employee`, `time`, `log_type`);

-- Verify indexes
SHOW INDEX FROM `tabEmployee Checkin`;
```

**Expected Performance**:
- Duplicate check: < 10ms
- Sync of 1000 records: < 30 seconds
- Query recent checkins: < 100ms

---

## 🔍 Troubleshooting Guide

### Issue: "Device Not Connected" Status

**Diagnosis Checklist**:

```bash
# 1. Ping the device
ping 192.168.1.100
# Expected: Replies (0% packet loss)

# 2. Check port connectivity
telnet 192.168.1.100 80
# Expected: Connected or Connection refused

# 3. Check firewall rules
sudo ufw allow from any to 192.168.1.100 port 80
# (if using UFW on Linux)

# 4. Verify DNS resolution
nslookup 192.168.1.100
# or use IP directly

# 5. Test from Frappe server specifically
curl -I http://192.168.1.100:80/
# Expected: HTTP response (200, 301, etc.)
```

**Common Causes & Fixes**:

| Cause | Solution |
|-------|----------|
| Device powered off | Turn on device, check LED indicators |
| Network cable disconnected | Reconnect ethernet cable |
| Wrong IP address | Verify IP in device settings |
| Firewall blocking | Allow port in firewall settings |
| Wrong port | Verify port (80 for API, 4370 for device) |
| Device rebooting | Wait 2-3 minutes for full startup |
| IP conflict | Assign static IP to device |

### Issue: "Invalid Token" or "Token Expired"

**Fix Steps**:

```
1. ZKTeco Config form
2. Delete existing token (if any)
3. Verify credentials:
   - Username: Superuser account
   - Password: Correct and unchanged
4. Click: "Register API Token"
5. Wait for success message
6. Save configuration
7. Test Connection
```

**If still failing**:

```bash
# Test manually from Frappe console
import requests

url = "http://192.168.1.100:80/api-token-auth/"
payload = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(url, json=payload)
print(response.json())
# Should return: {"token": "eyJ0eXAi..."}
```

### Issue: "Employee Not Found" After Sync

**Diagnostic Steps**:

```python
# In Frappe Console

# 1. Check what codes were attempted
frappe.db.sql("""
    SELECT DISTINCT emp_code, COUNT(*) as attempts
    FROM zkteco_transactions
    WHERE emp_code NOT IN (
        SELECT employee FROM `tabEmployee`
        UNION ALL
        SELECT user_id FROM `tabEmployee`
    )
    GROUP BY emp_code
    ORDER BY attempts DESC
""")

# 2. Check existing employees
frappe.db.sql("""
    SELECT employee, employee_name, user_id
    FROM `tabEmployee`
    WHERE status = 'Active'
    LIMIT 20
""")

# 3. Check created checkins
frappe.db.sql("""
    SELECT employee, log_type, COUNT(*) as count
    FROM `tabEmployee Checkin`
    WHERE creation >= DATE_SUB(NOW(), INTERVAL 1 DAY)
    GROUP BY employee, log_type
""")
```

**Resolution**:

```
1. Export unmapped emp_codes from diagnostic results
2. Create missing employees:
   → HR → New Employee
   → Set: Employee ID = emp_code
3. For existing employees:
   → Edit employee
   → Update: Employee ID or User ID to match ZKTeco
4. Run: Manual Sync again
```

### Issue: Only CHECK-IN Records, No CHECK-OUT

<<<<<<< HEAD
**🆕 FIXED! Use the new maintenance tools:**

**Quick Fix (Recommended):**
1. Open ZKTeco Config form
2. Click **"🔧 Fix IN/OUT Types"** in Maintenance menu
3. Confirm and wait for completion
4. All records will be automatically corrected!

**What was the problem?**
- Device Mode (Port 4370) doesn't always send punch type from the device
- Old code couldn't differentiate between IN and OUT
- All punches were being marked as "IN" by default

**How it's fixed now:**
- Sequence-based detection algorithm
- Groups punches by employee and date
- First punch = IN, Last punch = OUT
- Middle punches alternate automatically
=======
**Root Cause**: Old code didn't include log_type in duplicate check

**Verification**:
>>>>>>> upstream/multi-devices

```python
<<<<<<< HEAD
# Check your data has both IN and OUT
=======
# Check your current data
>>>>>>> upstream/multi-devices
in_count = frappe.db.count("Employee Checkin", {
    "log_type": "IN",
    "device_id": ["like", "%:4370%"]
})

out_count = frappe.db.count("Employee Checkin", {
    "log_type": "OUT",
    "device_id": ["like", "%:4370%"]
})

print(f"IN: {in_count}, OUT: {out_count}")
<<<<<<< HEAD
# Should show reasonable split, not all IN!
=======
# Should be roughly equal (within 5-10%)
```

**If OUT count is 0 or very low**:

```
1. Click: Maintenance → 🔧 Fix IN/OUT Types
2. System will:
   → Analyze employee punch sequences
   → Correct misclassified records
   → Show summary of changes
3. Verify: Check results in Employee Checkin list
>>>>>>> upstream/multi-devices
```

**Before Fix:**
```
Total Records: 121
IN: 121 ❌
OUT: 0 ❌
```

**After Fix:**
```
Total Records: 121
IN: 71 ✅
OUT: 50 ✅
```

### Issue: Duplicate Checkin Records

**🆕 FIXED! Use the duplicate removal tool:**

**Quick Fix:**
1. Open ZKTeco Config form
2. Click **"🗑️ Remove Duplicates"** in Maintenance menu
3. Confirm and wait for completion

**What causes duplicates?**
- Multiple sync runs on the same data
- Network issues causing retries
- System restart during sync

**How duplicates are detected:**
- Same employee
- Same timestamp
- Same log_type (IN/OUT)

Oldest record is kept, newer duplicates are deleted.

### Issue: Sync Takes Too Long

**Performance Diagnosis**:

```python
# Check sync duration
last_sync = frappe.db.get_single_value("ZKTeco Config", "last_sync")
print(f"Last sync: {last_sync}")

# Count recent transactions
recent_count = frappe.db.count("Employee Checkin", {
    "device_id": ["like", "%ZKTeco%"],
    "creation": [">=", frappe.utils.add_minutes(frappe.utils.now(), -10)]
})
print(f"Records in last 10 min: {recent_count}")

# Check database query performance
frappe.db.sql("SHOW PROCESSLIST;")
# Look for long-running queries
```

**Optimization Steps**:

```
1. Increase sync frequency interval
   → Change from 1 minute to 5-10 minutes
   → Reduces database load
   
2. Add database indexes
   → Run SQL commands from "Database Optimization" section
   → Improves duplicate check performance
   
3. Check database size
   → frappe.db.sql("SELECT COUNT(*) FROM `tabEmployee Checkin`")
   → If > 100k records, consider archiving old data
   
4. Reduce duplicate check methods
   → Simplify employee mapping to primary method only
```

### Issue: Device Mode (Port 4370) Not Working

**Requirements Check**:

```bash
# 1. Verify pyzk is installed
python -c "from zk import ZK; print('✅ pyzk installed')"
# If error: pip install pyzk --break-system-packages

# 2. Check network connectivity
ping 192.168.1.200
telnet 192.168.1.200 4370
# Expected: Connected

# 3. Verify device mode is active
# In ZKTeco Config: server_port = "4370"

# 4. Check device firmware
# Access device web interface and check version
```

**If still not working**:

```python
# Test direct connection in Frappe console
from zk import ZK

zk = ZK("192.168.1.200", port=4370, timeout=10)
try:
    conn = zk.connect()
    records = conn.get_attendance()
    print(f"✅ Connected! Got {len(records)} records")
    conn.disconnect()
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 🛠️ Maintenance & Administration

### Daily Tasks

```
☐ Monitor sync status
  → Actions → Sync Status
  → Verify: Last sync < frequency interval ago

☐ Check for errors
  → Error Log doctype
  → Search: "ZKTeco"
  → Resolve any critical errors

☐ Verify device status
  → Click: 🔍 Check Device Status
  → Expected: 🟢 Green
```

### Weekly Tasks

```
☐ Review sync statistics
  → Actions → Sync Status
  → Verify: IN/OUT counts roughly equal (~50/50)
  → Expected: Trending upward for active organization

☐ Check employee mapping quality
  → Generate report of unmapped employees
  → Create missing employee records
  → Verify no "Employee Not Found" in recent syncs

☐ Audit IN/OUT classification
  frappe.db.sql("""
    SELECT employee, log_type, COUNT(*) as count
    FROM `tabEmployee Checkin`
    WHERE creation >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    AND device_id LIKE '%ZKTeco%'
    GROUP BY employee, log_type
    HAVING ABS(
        COUNT(CASE WHEN log_type='IN' THEN 1 END) -
        COUNT(CASE WHEN log_type='OUT' THEN 1 END)
    ) > 5
  """)
  → Check results for anomalies
```

### Monthly Tasks

```
☐ Rotate API token (API mode)
  → Click: "Register API Token"
  → Verify token acceptance
  → Test: Test Connection

☐ Review and archive old records (optional)
  → Only if database size > 500k records
  → Archive Employee Checkin from 90+ days ago

☐ Update ZKBio Time software (if updates available)
  → Check: ZKBio vendor website
  → Test: In staging environment first
  → Verify: Sync still works after update

☐ Performance review
  → Check: Average sync time
  → Check: Database query performance
  → Optimize: If degradation detected
```

### Quarterly Tasks

```
☐ Database maintenance
  → OPTIMIZE TABLE `tabEmployee Checkin`
  → OPTIMIZE TABLE `tabEmployee`
  
☐ Policy review
  → Verify: Sync frequency still appropriate
  → Adjust: Based on organization growth
  → Test: New frequency in staging
  
☐ Security audit
  → Rotate superuser password
  → Review: API token expiration
  → Check: Access logs for anomalies
```

---

## 🚨 Advanced Troubleshooting

### Debugging Sync Issues

Enable detailed logging:

```python
# In Frappe Config (frappe_config.py)
logging_config = {
    'loggers': {
        'zkteco_checkins_sync': {
            'level': 'DEBUG',
        }
    }
}

# Restart Frappe
bench restart
```

Then check logs:

```bash
# Check Frappe logs
tail -f /path/to/frappe-bench/logs/bench.log | grep ZKTeco

# Or in Error Log doctype
frappe.get_list("Error Log", {
    "title": ["like", "%ZKTeco%"]
}, limit_page_length=50)
```

### Testing with Sample Data

```python
# In Frappe Console - Create sample transactions
from datetime import datetime, timedelta
import frappe

# Create test transactions
test_data = [
    {
        "emp_code": "EMP001",  # Must match existing employee
        "punch_time": "2024-12-08 08:30:00",
        "punch_state": 0,  # IN
        "punch_state_display": "Check In",
        "terminal_alias": "Test Device"
    },
    {
        "emp_code": "EMP001",
        "punch_time": "2024-12-08 17:30:00",
        "punch_state": 1,  # OUT
        "punch_state_display": "Check Out",
        "terminal_alias": "Test Device"
    }
]

# Test parsing and creation
for txn in test_data:
    from zkteco_checkins_sync.zkteco_checkin_sync.doctype.zkteco_config.zkteco_config import create_employee_checkin
    result = create_employee_checkin(txn)
    print(f"Transaction {txn['punch_time']}: {'✅ Created' if result else '❌ Failed'}")

# Verify in Employee Checkin list
frappe.db.get_list("Employee Checkin", {
    "employee": "EMP001",
    "creation": [">=", "2024-12-08 00:00:00"]
}, limit_page_length=10)
```

### Manual Cleanup (If Needed)

```python
# Remove all ZKTeco test records
frappe.db.sql("""
    DELETE FROM `tabEmployee Checkin`
    WHERE device_id LIKE '%Test Device%'
    AND creation >= DATE_SUB(NOW(), INTERVAL 1 DAY)
""")
frappe.db.commit()

print("✅ Test records removed")
```

---

## 📈 Performance Benchmarks

**Expected Performance** (based on 100 employees, 5-min sync frequency):

| Metric | Target | Typical |
|--------|--------|---------|
| Sync Duration | < 60s | 15-30s |
| CPU Usage | < 20% | 5-10% |
| Memory | < 500MB | 200-300MB |
| Database Queries | < 100 | 50-75 |
| Duplicate Detection | < 10ms | 2-5ms |

**For larger organizations**:
- 500+ employees: Increase frequency to 10-15 minutes
- 1000+ employees: Consider distributed syncing
- 5000+ employees: Archive old records (keep 1 year active)

---

## 🔐 Security Best Practices

### API Token Management

```
✅ DO:
  - Store token encrypted in database
  - Rotate token every 90 days
  - Use dedicated ZKBio superuser account
  - Monitor token usage in logs
  - Never log token values

❌ DON'T:
  - Share token in emails or chats
  - Hardcode token in code
  - Use personal user account
  - Log token in error messages
  - Store token in unencrypted config files
```

### Network Security

```
✅ DO:
  - Keep ZKTeco device on private network
  - Use firewall to restrict device access
  - Enable HTTPS if supported by device
  - Change default superuser password
  - Disable unnecessary ports

❌ DON'T:
  - Expose device port to internet
  - Use default factory credentials
  - Allow unauthorized access to ZKBio server
  - Disable security features
  - Share device IP publicly
```

### Access Control

```
Restricted to:
- ✅ System Manager (Full access)
- ✅ HR Manager (Full access)
- ✅ HR User (Read-only view)

Denied to:
- ❌ Employees (Cannot see configuration)
- ❌ Department Managers (Cannot modify config)
```

---

## 📚 API Reference

### Whitelisted Methods (Safe for Frontend Calls)

#### `check_device_status(server_ip, server_port)`
**Purpose**: Quick connectivity check without authentication

```python
frappe.call({
    method: "zkteco_checkins_sync...check_device_status",
    args: {server_ip: "192.168.1.100", server_port: 80},
    callback: (r) => console.log(r.message)
})

# Response
{
    "connected": true,
    "ip": "192.168.1.100",
    "port": 80,
    "response_time": 45.23,
    "message": "Device is online"
}
```

#### `register_api_token(server_ip, server_port, username, password)`
**Purpose**: Generate API authentication token

```python
# Returns
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### `test_connection()`
**Purpose**: Verify API connectivity and preview transactions

```python
# Returns
{
    "ok": true,
    "status_code": 200,
    "total_transactions": 150,
    "transactions_preview": [
        {
            "id": "123",
            "employee_code": "EMP001",
            "punch_time": "2024-12-08 08:30:00",
            "log_type": "IN",
            "erpnext_employee": "Employee Name"
        }
    ],
    "message": "Found 150 transactions for 2024-12-08"
}
```

#### `manual_sync()`
**Purpose**: Trigger immediate synchronization

```python
# Returns
{
    "success": true,
    "message": "Sync completed successfully"
}
```

#### `get_sync_status()`
**Purpose**: Get current sync statistics

```python
# Returns
{
    "enabled": true,
    "sync_frequency": "300",
    "last_sync": "2024-12-08 14:30:15",
    "recent_checkins_24h": 245,
    "checkins_in_24h": 122,
    "checkins_out_24h": 123,
    "server_configured": true,
    "token_configured": true
}
```

---

## 🎓 Common Use Cases

### Use Case 1: Multiple Device Setup

**Scenario**: Organization with 3 ZKTeco devices in different locations

**Solution**:
```
Option A: Separate Instances (Recommended)
├─ Device 1 → ZKTeco Config 1 (with different IP)
├─ Device 2 → ZKTeco Config 2 (with different IP)
└─ Device 3 → ZKTeco Config 3 (with different IP)

Option B: Centralized ZKBio Server
├─ All devices → Single ZKBio Time Server
├─ Single ZKTeco Config pointing to server
└─ Server aggregates all device data
```


## 📝 License

MIT License - See LICENSE file for details

---

## 👨‍💼 Author

<<<<<<< HEAD
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

## Version History & Changelog

### v2.0.0 (December 2025) - 🆕 Major Update

**New Features:**
- ✅ **Intelligent Sequence-Based Log Type Detection**
  - Automatic IN/OUT detection for Device Mode (Port 4370)
  - No longer depends on device sending punch type
  - Groups by employee and date, applies smart rules

- ✅ **One-Click Maintenance Tools**
  - "Fix IN/OUT Types" button in Maintenance menu
  - "Remove Duplicates" button in Maintenance menu
  - No coding required, fully automated

- ✅ **Enhanced Device Mode Support**
  - Proper sequence adjustment for all transactions
  - Works even when device doesn't send punch state
  - Handles multiple breaks during the day

**Bug Fixes:**
- Fixed: All records showing as "IN" in Device Mode
- Fixed: Duplicate records created during sync
- Fixed: Middle punches not alternating correctly
- Improved: Transaction processing performance

**Breaking Changes:**
- None - fully backward compatible

### v1.0.0 (Initial Release)

**Core Features:**
- Real-time sync with ZKTeco devices
- API Mode and Device Mode support
- Employee mapping
- Basic log type detection
- Dynamic scheduler

---

## Upgrade Guide

### Upgrading to v2.0.0 from v1.x

```bash
# Navigate to bench directory
cd /path/to/frappe-bench

# Update app from GitHub
cd apps/zkteco_checkins_sync
git pull origin main

# Navigate back to bench root
cd ../..

# Run migrations (if any)
bench --site your-site.com migrate

# Clear cache
bench --site your-site.com clear-cache

# Rebuild assets (important for new buttons!)
bench build --app zkteco_checkins_sync

# Restart
bench restart
```

### Post-Upgrade Steps

After upgrading to v2.0.0:

1. **Fix Existing Data:**
   - Open ZKTeco Config: `/app/zkteco-config`
   - Click "🗑️ Remove Duplicates" if you have duplicates
   - Click "🔧 Fix IN/OUT Types" to correct all records

2. **Verify New Features:**
   - Check that both buttons appear in Maintenance menu
   - Test connection to ensure sync still works
   - Monitor next sync to verify proper IN/OUT detection

3. **Optional: Clean Up:**
   - Review Employee Checkin list
   - Verify IN/OUT ratio is reasonable (~50/50)
   - Check sync logs for any warnings

**Rollback (if needed):**
```bash
cd apps/zkteco_checkins_sync
git checkout v1.0.0
cd ../..
bench --site your-site.com clear-cache
bench build --app zkteco_checkins_sync
bench restart
```



---
=======
**Osama Ahmed**  
Email: osama.ahmed@deliverydevs.com
>>>>>>> upstream/multi-devices

**Last Updated**: December 8, 2024  
**Status**: Production Ready ✅
