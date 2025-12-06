# Copyright (c) 2025, osama.ahmed@deliverydevs.com
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import requests
from frappe.utils import today, now_datetime, get_datetime, flt, cint
from datetime import datetime, timedelta
import json
import socket
try:
    from zk import ZK
except Exception:
    ZK = None


class ZKTecoConfig(Document):
    pass


def build_api_url(server_ip, server_port, endpoint="", use_https=None):
    """
    Build API URL with proper protocol (HTTP/HTTPS)

    Args:
        server_ip: Server IP address
        server_port: Server port
        endpoint: API endpoint path
        use_https: Force HTTPS (True), HTTP (False), or auto-detect (None)

    Returns:
        Full URL string
    """
    # Auto-detect protocol based on port if not specified
    if use_https is None:
        # Common HTTPS ports: 443, 8443
        # Common HTTP ports: 80, 8080, 4370
        port_int = int(str(server_port).strip())
        use_https = port_int in [443, 8443]

    protocol = "https" if use_https else "http"
    base_url = f"{protocol}://{server_ip}:{server_port}"

    if endpoint:
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        return base_url + endpoint

    return base_url


def detect_log_type(transaction):
    """
    Intelligently detect if transaction is IN or OUT
    Checks multiple possible fields from ZKTeco
    """
    # Try punch_state (numeric)
    punch_state = transaction.get('punch_state')
    if punch_state is not None:
        try:
            state_int = int(punch_state)
            return "OUT" if state_int == 1 else "IN"
        except (ValueError, TypeError):
            pass
    
    # Try punch_state_display (text)
    punch_state_display = transaction.get('punch_state_display', '').lower()
    if punch_state_display:
        if 'out' in punch_state_display or 'چیک آؤٹ' in punch_state_display:
            return "OUT"
        elif 'in' in punch_state_display or 'چیک ان' in punch_state_display:
            return "IN"
    
    # Try log_type field directly
    log_type = transaction.get('log_type', '').upper()
    if log_type in ['IN', 'OUT']:
        return log_type
    
    # Try punch (device mode)
    punch = transaction.get('punch')
    if punch is not None:
        try:
            punch_int = int(punch)
            return "OUT" if punch_int == 1 else "IN"
        except (ValueError, TypeError):
            pass
    
    return "IN"


@frappe.whitelist()
def check_device_status(server_ip=None, server_port=None):
    """
    Simple socket connection check to device
    Returns device status without needing token
    """
    server_ip = server_ip or frappe.db.get_single_value("ZKTeco Config", "server_ip")
    server_port = server_port or frappe.db.get_single_value("ZKTeco Config", "server_port")
    
    if not server_ip or not server_port:
        return {"connected": False, "error": "Server IP or Port not configured"}
    
    try:
        import socket
        import time
        
        start_time = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        
        result = s.connect_ex((server_ip, int(server_port)))
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        s.close()
        
        if result == 0:
            return {
                "connected": True,
                "ip": server_ip,
                "port": server_port,
                "response_time": round(response_time, 2),
                "message": "Device is online"
            }
        else:
            return {
                "connected": False,
                "ip": server_ip,
                "port": server_port,
                "error": "Connection refused or timeout"
            }
    
    except Exception as e:
        return {
            "connected": False,
            "ip": server_ip,
            "port": server_port,
            "error": str(e)
        }


@frappe.whitelist()
def register_api_token(server_ip: str | None = None, server_port: str | int | None = None, username: str | None = None, password: str | None = None):
    """
    Calls the remote API to obtain a token and returns it to the client.
    """
    # Prefer values provided by the form; fallback to saved Single DocType values
    server_ip = server_ip or frappe.db.get_single_value("ZKTeco Config", "server_ip")
    server_port = server_port or frappe.db.get_single_value("ZKTeco Config", "server_port")
    username = username or frappe.db.get_single_value("ZKTeco Config", "username")
    password = password or frappe.db.get_single_value("ZKTeco Config", "password")

    if str(server_port).strip() == "4370":
        return {"success": True, "device_mode": True, "message": _("Token not required for device on port 4370.")}
    if not all([server_ip, server_port, username, password]):
        frappe.throw(_("Please configure server IP, port, username, and password in ZKTeco Config."))

    # Build URL with proper protocol
    url = build_api_url(server_ip, server_port, "/api-token-auth/")

    payload = {
        "username": username,
        "password": password
    }

    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()

        data = resp.json()
        token = data.get("token")
        if not token:
            frappe.throw(_("Token not found in API response."))

        return {"success": True, "token": token}

    except requests.exceptions.RequestException as e:
        frappe.throw(_("Connection error: {0}").format(str(e)))


@frappe.whitelist()
def test_connection():
    """
    Enhanced test connection that shows latest transactions with detailed info
    """
    # Get token from the singleton config
    cfg = frappe.get_single("ZKTeco Config")
    token = (cfg.token or "").strip()
    server_ip = frappe.db.get_single_value("ZKTeco Config", "server_ip")
    server_port = frappe.db.get_single_value("ZKTeco Config", "server_port")
    
    if str(server_port).strip() == "4370":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((server_ip, int(server_port)))
            s.close()
            return {
                "ok": True,
                "status_code": 200,
                "url": f"{server_ip}:{server_port}",
                "total_transactions": 0,
                "transactions_preview": [],
                "message": _("Connected to device on port 4370. Token is not required."),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
    if not token:
        return {"ok": False, "error": _("Token not set in ZKTeco Config. Please register/save a token first.")}

    base_url = build_api_url(server_ip, server_port, "/iclock/api/transactions/")
    day = today()
    start_time = f"{day} 00:00:00"
    end_time = f"{day} 23:59:59"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    params = {
        "start_time": start_time,
        "end_time": end_time,
    }

    try:
        resp = requests.get(base_url, headers=headers, params=params, timeout=15)
        
        if resp.ok:
            try:
                data = resp.json()
                
                # Process and format transaction data for display
                formatted_transactions = []
                transaction_count = 0
                
                # Handle ZKTeco API response structure
                if isinstance(data, dict) and 'data' in data:
                    transactions = data['data']
                    transaction_count = data.get('count', len(transactions))
                elif isinstance(data, dict) and 'results' in data:
                    transactions = data['results']
                    transaction_count = len(transactions)
                elif isinstance(data, list):
                    transactions = data
                    transaction_count = len(transactions)
                else:
                    transactions = []
                
                # Format latest 5 transactions for preview
                for transaction in transactions[:5]:
                    try:
                        # Map ZKTeco transaction fields based on actual API response
                        emp_code = transaction.get('emp_code')
                        punch_time = transaction.get('punch_time')
                        punch_state = transaction.get('punch_state')
                        punch_state_display = transaction.get('punch_state_display')
                        device_id = transaction.get('terminal_alias') or transaction.get('terminal_sn')
                        first_name = transaction.get('first_name', '')
                        last_name = transaction.get('last_name', '') or ''
                        verify_type_display = transaction.get('verify_type_display')
                        
                        # Combine first and last name
                        zkteco_name = f"{first_name} {last_name}".strip()
                        
                        # Try to find employee name from ERPNext
                        employee_name = zkteco_name
                        erpnext_employee = None
                        if emp_code:
                            # Try to find employee by employee_id or user_id
                            employee = frappe.db.get_value("Employee", 
                                                         {"employee": emp_code}, 
                                                         ["name", "employee_name"])
                            if not employee:
                                employee = frappe.db.get_value("Employee", 
                                                             {"user_id": emp_code}, 
                                                             ["name", "employee_name"])
                            if employee:
                                erpnext_employee = employee[0] if isinstance(employee, tuple) else employee
                                employee_name = f"{employee[1]} (ERPNext)" if isinstance(employee, tuple) else f"{employee} (ERPNext)"
                        
                        # Determine log type based on punch_state
                        log_type = detect_log_type(transaction)
                        
                        formatted_transactions.append({
                            "id": transaction.get('id'),
                            "employee_code": emp_code,
                            "employee_name": employee_name,
                            "erpnext_employee": erpnext_employee,
                            "punch_time": punch_time,
                            "log_type": log_type,
                            "punch_state_display": punch_state_display,
                            "device_id": device_id,
                            "verify_method": verify_type_display,
                            "zkteco_name": zkteco_name,
                            "department": transaction.get('department'),
                            "raw_data": transaction
                        })
                    except Exception as e:
                        frappe.log_error(f"Error processing transaction: {e}", "ZKTeco Transaction Processing")
                        continue
                
                return {
                    "ok": True,
                    "status_code": resp.status_code,
                    "url": resp.url,
                    "total_transactions": transaction_count,
                    "transactions_preview": formatted_transactions,
                    "raw_sample": transactions[:2] if transactions else [],
                    "message": f"Found {transaction_count} transactions for {day}"
                }
                
            except json.JSONDecodeError as e:
                return {
                    "ok": False,
                    "status_code": resp.status_code,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_response": resp.text[:500]
                }
        else:
            return {
                "ok": False,
                "status_code": resp.status_code,
                "url": resp.url,
                "error": f"HTTP {resp.status_code}: {resp.text[:200]}"
            }
            
    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Connection error: {str(e)}"
        }


def sync_zkteco_transactions():
    """
    Main function to sync ZKTeco transactions with ERPNext Employee Checkin records
    """
    # Implement lock mechanism to prevent concurrent execution
    lock_key = "zkteco_sync_lock"
    if frappe.cache().get_value(lock_key):
        frappe.logger().info("ZKTeco sync already running, skipping this execution")
        return

    try:
        # Acquire lock with 5 minute timeout
        frappe.cache().set_value(lock_key, "locked", expires_in_sec=300)

        # Check if sync is enabled
        cfg = frappe.get_single("ZKTeco Config")
        if str(cfg.server_port).strip() == "4370":
            frappe.logger().info("ZKTeco Sync skipped: Device mode (port 4370) does not support API-based sync.")
            return

        if not cfg.enable_sync:
            frappe.log_error("ZKTeco sync is disabled", "ZKTeco Sync")
            return

        if not cfg.token:
            frappe.log_error("ZKTeco token not configured", "ZKTeco Sync")
            return
        # Get transactions from last sync or last hour (timezone-aware)
        last_sync = frappe.db.get_single_value("ZKTeco Config", "last_sync")
        if last_sync:
            last_sync = get_datetime(last_sync)
        else:
            last_sync = now_datetime() - timedelta(hours=1)

        current_time = now_datetime()

        transactions = fetch_zkteco_transactions(cfg, last_sync, current_time)

        processed_count = 0
        error_count = 0

        if transactions:
            for transaction in transactions:
                try:
                    if create_employee_checkin(transaction):
                        processed_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    frappe.log_error(f"Error creating checkin for transaction {transaction}: {str(e)}", "ZKTeco Sync Error")

        # Always update last sync time, even if no transactions found
        total_synced = frappe.db.get_single_value("ZKTeco Config", "total_synced_records") or 0
        frappe.db.set_single_value("ZKTeco Config", "last_sync", current_time)
        frappe.db.set_single_value("ZKTeco Config", "total_synced_records", total_synced + processed_count)
        frappe.db.commit()

        if transactions:
            frappe.logger().info(f"ZKTeco Sync completed: {processed_count} processed, {error_count} errors")
        else:
            frappe.logger().info("ZKTeco Sync completed: No new transactions found")

    except Exception as e:
        frappe.log_error(f"ZKTeco sync failed: {str(e)}", "ZKTeco Sync Fatal Error")
    finally:
        # Always release lock when done
        frappe.cache().delete_value(lock_key)


def fetch_zkteco_transactions(cfg, start_time, end_time):
    """
    Fetch transactions from ZKTeco device with pagination support
    """
    server_ip = cfg.server_ip
    server_port = cfg.server_port
    token = cfg.token

    base_url = build_api_url(server_ip, server_port, "/iclock/api/transactions/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    params = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    all_transactions = []
    current_url = base_url
    max_pages = 100  # Prevent infinite loops

    try:
        for page_num in range(max_pages):
            # First page uses params, subsequent pages use full URL from 'next'
            if page_num == 0:
                resp = requests.get(current_url, headers=headers, params=params, timeout=30)
            else:
                resp = requests.get(current_url, headers=headers, timeout=30)

            resp.raise_for_status()
            data = resp.json()

            # Extract transactions from response
            transactions = []
            next_url = None

            if isinstance(data, dict):
                # Check for pagination
                next_url = data.get('next')

                # Extract transactions
                if 'data' in data:
                    transactions = data['data']
                elif 'results' in data:
                    transactions = data['results']
                elif 'transactions' in data:
                    transactions = data['transactions']
            elif isinstance(data, list):
                transactions = data

            # Add transactions to the list
            if transactions:
                all_transactions.extend(transactions)

            # Check if there are more pages
            if not next_url:
                break

            current_url = next_url

            # Log pagination progress
            if page_num > 0:
                frappe.logger().info(f"ZKTeco pagination: Fetched page {page_num + 1}, total transactions so far: {len(all_transactions)}")

        if len(all_transactions) > 0:
            frappe.logger().info(f"ZKTeco fetch completed: {len(all_transactions)} transactions from {page_num + 1} page(s)")

        return all_transactions

    except Exception as e:
        frappe.log_error(f"Failed to fetch ZKTeco transactions: {str(e)}", "ZKTeco API Error")
        return all_transactions if all_transactions else []


def create_employee_checkin(transaction):
    """
    Create Employee Checkin record from ZKTeco transaction
    """
    try:
        # Extract transaction data based on ZKTeco API response structure
        emp_code = transaction.get('emp_code')
        punch_time = transaction.get('punch_time')
        punch_state = transaction.get('punch_state')
        device_id = transaction.get('terminal_alias') or transaction.get('terminal_sn')
        transaction_id = transaction.get('id')
        
        if not emp_code or not punch_time:
            frappe.log_error(f"Missing required fields in transaction: {transaction}", "ZKTeco Transaction Error")
            return False
        
        # Find employee
        employee = find_employee_by_code(emp_code)
        if not employee:
            frappe.log_error(f"Employee not found for code: {emp_code}", "ZKTeco Employee Mapping")
            return False
        
        # Convert punch_time to datetime
        if isinstance(punch_time, str):
            punch_datetime = get_datetime(punch_time)
        else:
            punch_datetime = punch_time

        # Validate timestamp is reasonable
        current_time = now_datetime()
        max_past_days = 90  # Don't sync records older than 90 days

        # Check if timestamp is in the future
        if punch_datetime > current_time + timedelta(minutes=5):
            frappe.log_error(
                f"Transaction timestamp is in the future: {punch_datetime} (current: {current_time})",
                "ZKTeco Invalid Timestamp"
            )
            return False

        # Check if timestamp is too old
        if punch_datetime < current_time - timedelta(days=max_past_days):
            frappe.logger().debug(
                f"Skipping old transaction: {punch_datetime} (older than {max_past_days} days)"
            )
            return False

        # Determine log type based on punch_state
        log_type = detect_log_type(transaction)

        # Build unique device_id with transaction ID to prevent duplicates
        unique_device_id = f"{device_id} (ZKTeco-{transaction_id})" if transaction_id else device_id or "ZKTeco Device"

        # Check if checkin already exists - single reliable check
        # Include log_type to allow both IN and OUT for same employee/time
        existing_checkin = frappe.db.exists("Employee Checkin", {
            "employee": employee,
            "time": punch_datetime,
            "log_type": log_type,
            "device_id": unique_device_id
        })

        if existing_checkin:
            return True  # Already processed
        
        # Create Employee Checkin
        checkin = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": employee,
            "time": punch_datetime,
            "log_type": log_type,
            "device_id": unique_device_id,
            "skip_auto_attendance": 0
        })
        
        checkin.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return True
        
    except Exception as e:
        frappe.log_error(f"Error creating Employee Checkin: {str(e)}", "ZKTeco Checkin Creation")
        return False


def find_employee_by_code(emp_code):
    """
    Find employee by various ID fields
    """
    # Try employee field first
    employee = frappe.db.get_value("Employee", {"employee": emp_code}, "name")
    if employee:
        return employee
    
    # Try user_id field
    employee = frappe.db.get_value("Employee", {"user_id": emp_code}, "name")
    if employee:
        return employee
    
    # Try attendance_device_id if it exists
    if frappe.db.has_column("Employee", "attendance_device_id"):
        employee = frappe.db.get_value("Employee", {"attendance_device_id": emp_code}, "name")
        if employee:
            return employee
    
    return None


@frappe.whitelist()
def manual_sync():
    """
    Manual sync trigger for testing
    """
    try:
        cfg = frappe.get_single("ZKTeco Config")
        if str(cfg.server_port).strip() == "4370":
            return device_mode_sync()
        sync_zkteco_transactions()
        return {"success": True, "message": "Sync completed successfully"}
    except Exception as e:
        frappe.log_error(f"Manual sync failed: {str(e)}", "ZKTeco Manual Sync")
        return {"success": False, "message": f"Sync failed: {str(e)}"}


def scheduled_sync():
    """
    Scheduled sync function that respects the frequency setting
    """
    try:
        cfg = frappe.get_single("ZKTeco Config")
        if not cfg.enable_sync:
            return
            
        # For frequent syncs (less than 60 seconds), check if we should actually run
        sync_seconds = int(cfg.seconds or 300)
        if sync_seconds < 60:
            last_run = frappe.cache().get_value("zkteco_last_sync_run")
            current_time = now_datetime()
            
            if last_run:
                time_diff = (current_time - get_datetime(last_run)).total_seconds()
                if time_diff < sync_seconds:
                    return  # Not yet time for next sync
            
            # Update last run time
            frappe.cache().set_value("zkteco_last_sync_run", current_time)
        
        if str(cfg.server_port).strip() == "4370":
            device_mode_sync()
        else:
            sync_zkteco_transactions()
        
    except Exception as e:
        frappe.log_error(f"Scheduled ZKTeco sync failed: {str(e)}", "ZKTeco Scheduled Sync Error")


def cleanup_scheduler_check():
    """
    Cleanup function to ensure scheduler is working properly
    """
    try:
        cfg = frappe.get_single("ZKTeco Config")
        if cfg.enable_sync:
            # Log that the scheduler is active
            frappe.logger().info("ZKTeco scheduler check: Active")
    except Exception as e:
        frappe.log_error(f"ZKTeco scheduler check failed: {str(e)}", "ZKTeco Scheduler Check")


@frappe.whitelist()
def get_sync_status():
    """
    Get current sync status and statistics
    """
    try:
        cfg = frappe.get_single("ZKTeco Config")
        
        # Get last sync time
        last_sync = frappe.db.get_single_value("ZKTeco Config", "last_sync")
        
        # Count recent employee checkins from ZKTeco
        recent_checkins = frappe.db.count("Employee Checkin", {
            "device_id": ["like", "%ZKTeco%"],
            "creation": [">=", frappe.utils.add_days(today(), -1)]
        })
        
        # Count IN and OUT separately
        checkins_in = frappe.db.count("Employee Checkin", {
            "device_id": ["like", "%ZKTeco%"],
            "log_type": "IN",
            "creation": [">=", frappe.utils.add_days(today(), -1)]
        })
        
        checkins_out = frappe.db.count("Employee Checkin", {
            "device_id": ["like", "%ZKTeco%"],
            "log_type": "OUT",
            "creation": [">=", frappe.utils.add_days(today(), -1)]
        })
        
        return {
            "enabled": cfg.enable_sync,
            "sync_frequency": cfg.seconds,
            "last_sync": last_sync,
            "recent_checkins_24h": recent_checkins,
            "checkins_in_24h": checkins_in,
            "checkins_out_24h": checkins_out,
            "server_configured": bool(cfg.server_ip and cfg.server_port),
            "token_configured": bool(cfg.token)
        }
        
    except Exception as e:
        return {"error": str(e)}


@frappe.whitelist()
def set_config(server_ip: str, server_port: str | int, enable_sync: int = 1, seconds: int | None = None):
    cfg = frappe.get_single("ZKTeco Config")
    cfg.server_ip = server_ip
    cfg.server_port = str(server_port)
    cfg.enable_sync = cint(enable_sync)
    if seconds is not None:
        cfg.seconds = str(seconds)
    cfg.save(ignore_permissions=True)
    frappe.db.commit()
    return {
        "ok": True,
        "server_ip": cfg.server_ip,
        "server_port": cfg.server_port,
        "enable_sync": cfg.enable_sync,
        "seconds": cfg.seconds,
    }


@frappe.whitelist()
def device_mode_sync():
    # Implement lock mechanism to prevent concurrent execution
    lock_key = "zkteco_device_sync_lock"
    if frappe.cache().get_value(lock_key):
        return {"success": False, "message": "Device sync already running"}

    try:
        # Acquire lock with 5 minute timeout
        frappe.cache().set_value(lock_key, "locked", expires_in_sec=300)

        cfg = frappe.get_single("ZKTeco Config")
        ip = cfg.server_ip
        port = int(str(cfg.server_port or "4370").strip())
        if port != 4370:
            return {"success": False, "message": "Device mode only supports port 4370"}
        if not ZK:
            return {"success": False, "message": "Device library not available"}

        zk = ZK(ip, port=port, timeout=10, ommit_ping=True)
        conn = zk.connect()
        records = conn.get_attendance()
        created = 0
        for att in records or []:
            if create_checkin_from_attendance(att, f"{ip}:{port}"):
                created += 1
        conn.disconnect()
        frappe.db.set_single_value("ZKTeco Config", "last_sync", now_datetime())
        total_synced = frappe.db.get_single_value("ZKTeco Config", "total_synced_records") or 0
        frappe.db.set_single_value("ZKTeco Config", "total_synced_records", total_synced + created)
        frappe.db.commit()
        return {"success": True, "created": created}
    except Exception as e:
        frappe.log_error(f"Device mode sync failed: {str(e)}", "ZKTeco Device Sync Error")
        return {"success": False, "message": str(e)}
    finally:
        # Always release lock when done
        frappe.cache().delete_value(lock_key)


def create_checkin_from_attendance(att, device_id):
    try:
        emp_code = str(getattr(att, "user_id", "") or "").strip()
        if not emp_code:
            return False
        employee = find_employee_by_code(emp_code)
        if not employee:
            return False
        punch_datetime = getattr(att, "timestamp", None)
        if not punch_datetime:
            return False

        # Validate timestamp is reasonable
        current_time = now_datetime()
        max_past_days = 90

        # Check if timestamp is in the future
        if punch_datetime > current_time + timedelta(minutes=5):
            return False

        # Check if timestamp is too old
        if punch_datetime < current_time - timedelta(days=max_past_days):
            return False

        log_type = "IN"
        try:
            punch_val = int(getattr(att, "punch", 0))
            log_type = "OUT" if punch_val == 1 else "IN"
        except Exception:
            log_type = "IN"
        # Fixed: Include log_type in duplicate check to allow both IN and OUT
        existing = frappe.db.exists("Employee Checkin", {
            "employee": employee,
            "time": punch_datetime,
            "device_id": device_id,
            "log_type": log_type
        })
        if existing:
            return True
        checkin = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": employee,
            "time": punch_datetime,
            "log_type": log_type,
            "device_id": device_id,
            "skip_auto_attendance": 0
        })
        checkin.insert(ignore_permissions=True)
        frappe.db.commit()
        return True
    except Exception:
        return False
