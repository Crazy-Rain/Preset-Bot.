# Catbox.moe Avatar Upload Integration

## Overview

When users add or update character avatars via the GUI by selecting a local image file, the image is automatically uploaded to catbox.moe (a free image hosting service) and the returned URL is used as the `avatar_url`. This ensures webhooks can display character avatars properly.

## How It Works

### GUI Integration

1. **Character Creation/Update**: When a user browses and selects an avatar file in the Characters or User Characters tab:
   - The file is automatically uploaded to catbox.moe
   - The upload URL is set as the `avatar_url` field
   - A local copy is still saved as backup in `character_avatars/`
   - Success/failure messages are shown to the user

2. **Upload Method**: `upload_to_catbox(file_path)`
   - Uploads the image to catbox.moe API
   - Returns the hosted URL on success
   - Returns None on failure
   - Has 30-second timeout for reliability

### API Details

- **Endpoint**: `https://catbox.moe/user/api.php`
- **Method**: POST with multipart/form-data
- **Parameters**:
  - `reqtype`: "fileupload"
  - `fileToUpload`: The image file
- **Response**: Plain text URL on success

### Benefits

1. **Webhooks Work**: Discord webhooks require URLs, not local files
2. **Real-time Updates**: Character changes (including avatars) are immediately visible without restart
3. **Persistent**: Uploaded images remain accessible even if local files are deleted
4. **Free**: Catbox.moe is a free service with no API key required

## User Experience

When adding a character with an avatar file:
1. User clicks "Browse..." and selects an image
2. User fills in other character details
3. User clicks "Add Character" or "Update Selected"
4. Message appears: "Uploading avatar to catbox.moe..."
5. On success: "Avatar uploaded successfully! URL: https://files.catbox.moe/..."
6. Character is saved with the catbox URL
7. Webhooks can now use the avatar

## Error Handling

- If upload fails, user is notified
- Character is still created/updated, just without avatar URL
- Local backup is always saved regardless of upload status
- Network timeouts are handled gracefully (30s timeout)

## Requirements

- Added `requests>=2.28.0` to requirements.txt for HTTP requests

## Files Modified

- `gui.py`: Added `upload_to_catbox()` method and integrated into character add/update flows
- `requirements.txt`: Added requests library
