  ChatroomIPs.dat Generator for Ares Galaxy body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; } h1 { border-bottom: 2px solid #eee; padding-bottom: 10px; } h2 { margin-top: 30px; color: #2c3e50; } h3 { color: #34495e; } code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; } pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; } pre code { background-color: transparent; padding: 0; } ul { padding-left: 20px; } strong { color: #2c3e50; }

# ChatroomIPs.dat Generator for Ares Galaxy

A Python script that generates `ChatroomIPs.dat` files for Ares Galaxy from JSON chatroom server lists.

## Overview

This script converts chatroom server data from JSON format into the binary `ChatroomIPs.dat` format required by Ares Galaxy. It automatically writes the file to the correct user data directory, making it work for any Windows user without requiring administrator privileges.

## Features

*   **User-agnostic**: Works for any Windows user by using environment variables
*   **No admin required**: Writes to user's AppData directory instead of Program Files
*   **JSON input**: Load server lists from external JSON files
*   **Score calculation**: Automatically calculates server scores based on user count
*   **Error handling**: Graceful error messages for missing or malformed JSON files

## Requirements

*   Python 3.6+
*   Windows OS (uses `%LOCALAPPDATA%` environment variable)
*   Ares Galaxy installed

## File Format

The script generates binary files following the Ares Galaxy ChatroomIPs.dat format:

*   **Header** (6 bytes): IP placeholder, record size (12), padding
*   **Records** (12 bytes each): IP address (4), port (2), score (2), padding (4)
*   All integers are stored in little-endian format

## Usage

### 1\. Prepare JSON File

Create or download a `rooms.json` file with the following structure:

```
{  
  "Count": 2,  
  "Items": [  
    {  
      "port": 54321,  
      "users": 25,  
      "name": "Example Room",  
      "externalIp": "192.168.1.100"  
    },  
    {  
      "port": 5000,  
      "users": 10,  
      "name": "Another Room",  
      "externalIp": "10.0.0.50"  
    }  
  ]  
}
```

You can download the latest server list from: [http://chatrooms.mywire.org/rooms.json](http://chatrooms.mywire.org/rooms.json)

### 2\. Run the Script

```
python generate_chatroomips.py
```

The script will:

1.  Load server data from `rooms.json`
2.  Calculate scores based on user counts (users × 5, capped at 200)
3.  Create the binary `ChatroomIPs.dat` file
4.  Save it to `%LOCALAPPDATA%\Ares\Data\ChatroomIPs.dat`

### 3\. Output

```
Created ChatroomIPs.dat at: C:\Users\YourUsername\AppData\Local\Ares\Data\ChatroomIPs.dat  
Total servers: 53
```

## How It Works

### Score Calculation

Server scores are calculated based on active user count:

```
score = min(users * 5, 200)
```

Higher scores indicate more popular/reliable servers.

### File Location

The script uses `%LOCALAPPDATA%` to determine the output path, matching how Ares Galaxy itself locates user data.

Ares Galaxy checks this location first before falling back to the Program Files installation directory.

### Binary Format

IP addresses are converted to 32-bit little-endian integers:

```
ip_int = struct.unpack('<I', socket.inet_aton(ip_str))[0]
```

This matches the format expected by Ares Galaxy's chatroom loader.

## Configuration

### Change JSON File Path

Modify the `json_file_path` variable:

```
json_file_path = 'path/to/your/servers.json'
```

### Change Output Location

The script automatically uses the correct user data directory. To override:

```
output_path = 'C:/custom/path/ChatroomIPs.dat'
```

## Error Handling

The script handles common errors:

*   **File not found**: Clear error message if JSON file is missing
*   **Invalid JSON**: Reports JSON parsing errors with details
*   **Directory creation**: Automatically creates the Ares data directory if it doesn't exist

## Technical Details

### Minimum File Size

Ares Galaxy requires the file to be at least 600 bytes. With 53 servers, the generated file is 642 bytes (6-byte header + 53 × 12-byte records), meeting this requirement.

### IP Validation

Ares Galaxy filters out firewalled IPs during loading. The script doesn't perform this validation, relying on the source JSON to provide valid IPs.

## Troubleshooting

### Permission Denied Error

If you get a permission error, the script is likely trying to write to Program Files. Ensure you're using the environment variable approach (default behavior).

### File Not Found

Ensure `rooms.json` is in the same directory as the script, or provide the full path.

### Ares Not Loading Servers

*   Verify the file was created at the correct location
*   Check that Ares Galaxy is looking in `%LOCALAPPDATA%\Ares\Data\`
*   Ensure the file is at least 600 bytes

## License

This script is provided as-is for use with Ares Galaxy.

## Credits

Based on the Ares Galaxy file format specification from the CWBudde/AresGalaxy repository.
