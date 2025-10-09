# ChatroomIPs.dat Generator for Ares Galaxy

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Python utility that generates `ChatroomIPs.dat` files for Ares Galaxy from JSON chatroom server lists.

## Overview

This script converts chatroom server data from JSON format into the binary `ChatroomIPs.dat` format required by Ares Galaxy. It automatically writes to the correct user data directory, making it work for any Windows user without requiring administrator privileges.

## Features

- **User-agnostic**: Works for any Windows user via environment variables
- **No admin required**: Writes to user's AppData directory instead of Program Files
- **JSON input**: Load server lists from external JSON files
- **Score calculation**: Automatically calculates server scores based on user count
- **Error handling**: Graceful error messages for missing or malformed JSON files

## Requirements

- Python 3.6 or higher
- Windows OS (uses `%LOCALAPPDATA%` environment variable)
- Ares Galaxy installed

## Installation

1. Clone this repository or download `generate_chatroomips.py`
2. Ensure Python 3.6+ is installed on your system
3. No additional dependencies required (uses standard library only)

## Usage

### Quick Start

1. **Prepare your JSON file**

   Create or download a `rooms.json` file with this structure:

   ```json
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

   You can download the latest server list from: http://chatrooms.mywire.org/rooms.json

2. **Run the script**

   ```bash
   python generate_chatroomips.py
   ```

3. **Expected output**

   ```
   Created ChatroomIPs.dat at: C:\Users\YourUsername\AppData\Local\Ares\Data\ChatroomIPs.dat
   Total servers: 53
   ```

## How It Works

### Score Calculation

Server scores are calculated based on active user count:

```python
score = min(users * 5, 200)
```

Higher scores indicate more popular/reliable servers.

### File Location

The script uses `%LOCALAPPDATA%` to determine the output path, matching how Ares Galaxy itself locates user data:

```
%LOCALAPPDATA%\Ares\Data\ChatroomIPs.dat
```

Ares Galaxy checks this location first before falling back to the Program Files installation directory.

### Binary Format

The script generates binary files following the Ares Galaxy ChatroomIPs.dat format:

| Component | Size | Description |
|-----------|------|-------------|
| Header | 6 bytes | IP placeholder, record size (12), padding |
| Records | 12 bytes each | IP address (4), port (2), score (2), padding (4) |

All integers are stored in little-endian format.

IP addresses are converted to 32-bit little-endian integers:

```python
ip_int = struct.unpack('<I', socket.inet_aton(ip_str))[0]
```

## Configuration

### Change JSON File Path

Modify the `json_file_path` variable in the script:

```python
json_file_path = 'path/to/your/servers.json'
```

### Change Output Location

The script automatically uses the correct user data directory. To override:

```python
output_path = 'C:/custom/path/ChatroomIPs.dat'
```

## Troubleshooting

### Permission Denied Error

If you get a permission error, the script is likely trying to write to Program Files. Ensure you're using the environment variable approach (default behavior).

### File Not Found

Ensure `rooms.json` is in the same directory as the script, or provide the full path.

### Ares Not Loading Servers

- Verify the file was created at the correct location
- Check that Ares Galaxy is looking in `%LOCALAPPDATA%\Ares\Data\`
- Ensure the file is at least 600 bytes (minimum requirement)

## Technical Details

### Minimum File Size

Ares Galaxy requires the file to be at least 600 bytes. With 53 servers, the generated file is 642 bytes (6-byte header + 53 × 12-byte records), meeting this requirement.

### IP Validation

Ares Galaxy filters out firewalled IPs during loading. The script doesn't perform this validation, relying on the source JSON to provide valid IPs.

## Error Handling

The script handles common errors gracefully:

- **File not found**: Clear error message if JSON file is missing
- **Invalid JSON**: Reports JSON parsing errors with details
- **Directory creation**: Automatically creates the Ares data directory if it doesn't exist

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Based on the Ares Galaxy file format specification from the [CWBudde/AresGalaxy](https://github.com/CWBudde/AresGalaxy) repository.

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

_Made for the Ares Galaxy community_
