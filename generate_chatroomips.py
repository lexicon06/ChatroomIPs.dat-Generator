import struct
import socket
import json
import os


def ip_to_int(ip_str):
    """
    Convert an IPv4 address string into a 32-bit integer (little-endian).
    """
    return struct.unpack('<I', socket.inet_aton(ip_str))[0]


def create_chatroomips_dat(filename, servers):
    """
    Generate a ChatroomIPs.dat file compatible with Ares Galaxy.

    Args:
        filename (str): Path to the output file.
        servers (list[tuple]): List of (ip_string, port, score) server entries.
    """
    with open(filename, 'wb') as f:
        # File header: 6 bytes total
        #   [0–3] Placeholder IP (always 0)
        #   [4]   Record size (12 bytes)
        #   [5]   Padding (0)
        header = struct.pack('<I', 0)
        header += struct.pack('B', 12)
        header += struct.pack('B', 0)
        f.write(header)

        # Server records: 12 bytes each
        #   [0–3]   IP (little-endian)
        #   [4–5]   Port (uint16)
        #   [6–7]   Score (uint16)
        #   [8–11]  Reserved (zero)
        for ip_str, port, score in servers:
            ip_int = ip_to_int(ip_str)
            record = struct.pack('<I', ip_int)
            record += struct.pack('<H', port)
            record += struct.pack('<H', score)
            record += struct.pack('<I', 0)
            f.write(record)


# --------------------------
# Load server list from JSON
# --------------------------
json_file_path = 'rooms.json'  # External file containing room info

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found: {json_file_path}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in {json_file_path}: {e}")
    exit(1)

# Extract (ip, port, score) from JSON
servers = []
for item in data['Items']:
    ip = item['externalIp']
    port = item['port']
    users = item['users']
    # Scoring heuristic: proportional to user count, capped at 200
    score = min(users * 5, 200)
    servers.append((ip, port, score))


# -------------------------
# Resolve output file path
# -------------------------
local_appdata = os.environ.get('LOCALAPPDATA')  # User-specific AppData dir
output_path = os.path.join(local_appdata, 'Ares', 'Data', 'ChatroomIPs.dat')

# Ensure target directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write ChatroomIPs.dat
create_chatroomips_dat(output_path, servers)

print(f"Created ChatroomIPs.dat at: {output_path}")
print(f"Total servers: {data['Count']}")
