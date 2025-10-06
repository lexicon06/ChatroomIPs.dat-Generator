import struct    
import socket    
import json    
import os  
  
def ip_to_int(ip_str):    
    """Convert IP string to 32-bit integer (little-endian)"""  
    return struct.unpack('<I', socket.inet_aton(ip_str))[0]    
  
def create_chatroomips_dat(filename, servers):    
    """    
    Create ChatroomIPs.dat file with server entries    
        
    Args:    
        filename: Output file path    
        servers: List of tuples (ip_string, port, score)    
    """    
    with open(filename, 'wb') as f:    
        # Write header (6 bytes) - Required by Ares Galaxy file format  
        header = struct.pack('<I', 0)  # IP placeholder (4 bytes)    
        header += struct.pack('B', 12)  # Record size (1 byte) - tells Ares each record is 12 bytes  
        header += struct.pack('B', 0)   # Padding (1 byte)    
        f.write(header)    
            
        # Write server records (12 bytes each)    
        for ip_str, port, score in servers:    
            ip_int = ip_to_int(ip_str)    
            record = struct.pack('<I', ip_int)      # IP (4 bytes) - little-endian format  
            record += struct.pack('<H', port)       # Port (2 bytes)    
            record += struct.pack('<H', score)      # Score (2 bytes) - higher = better server  
            record += struct.pack('<I', 0)          # Padding (4 bytes) - required by format  
            f.write(record)    
  
# Load JSON data from file instead of hardcoded string  
# This allows you to update the server list without modifying the script  
# From: http://chatrooms.mywire.org/rooms.json
json_file_path = 'rooms.json'  # Change this to your JSON file path  
  
try:  
    with open(json_file_path, 'r', encoding='utf-8') as f:  
        data = json.load(f)  # Directly parse JSON from file  
except FileNotFoundError:  
    print(f"Error: Could not find JSON file at {json_file_path}")  
    exit(1)  
except json.JSONDecodeError as e:  
    print(f"Error: Invalid JSON format in {json_file_path}: {e}")  
    exit(1)  
    
# Extract servers and calculate scores based on user count    
servers = []    
for item in data['Items']:    
    ip = item['externalIp']    
    port = item['port']    
    users = item['users']    
    # Score based on user count (higher users = higher score)    
    # Cap at 200 to avoid overflow (Word type max is 65535, but we keep it reasonable)  
    score = min(users * 5, 200)    
    servers.append((ip, port, score))    
  
# Use environment variable for user-agnostic path  
# This makes the script work for ANY Windows user, not just "Dev"  
local_appdata = os.environ.get('LOCALAPPDATA')  # Gets C:\Users\{CurrentUser}\AppData\Local  
    
# Create the file path using os.path.join for cross-platform compatibility  
# Ares Galaxy checks data_path\Data\ChatroomIPs.dat first (user directory)  
# before falling back to app_path\Data\ChatroomIPs.dat (Program Files)  
output_path = os.path.join(local_appdata, 'Ares', 'Data', 'ChatroomIPs.dat')    
    
# Ensure directory exists before writing file  
# exist_ok=True prevents errors if directory already exists  
# This avoids "FileNotFoundError: No such file or directory" errors  
os.makedirs(os.path.dirname(output_path), exist_ok=True)    
    
create_chatroomips_dat(output_path, servers)    
print(f"Created ChatroomIPs.dat at: {output_path}")    
print(f"Total servers: {data['Count']}")
