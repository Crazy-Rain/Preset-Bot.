# Automatic Reconnection Guide

## Overview

The Automatic Reconnection feature ensures that your Discord bot remains running even when connection issues occur. Instead of crashing and requiring manual intervention, the bot will automatically retry the connection with intelligent backoff strategies.

## Key Benefits

1. **Increased Uptime**: Bot automatically recovers from temporary connection issues
2. **Reduced Manual Intervention**: No need to manually restart the bot after network issues
3. **Intelligent Retry Logic**: Exponential backoff prevents overwhelming the Discord API
4. **Configurable Behavior**: Customize retry attempts, delays, and enable/disable as needed
5. **Clear Logging**: Detailed console output shows connection attempts and reasons for failures

## How It Works

When the bot encounters a connection error, it follows this process:

1. **Detect Failure**: The bot catches connection-related exceptions
2. **Classify Error**: Different errors are handled differently:
   - **Login Failures**: No retry (token needs to be fixed)
   - **HTTP Exceptions**: Retry with backoff
   - **Gateway Not Found**: Retry with backoff (Discord service may be down)
   - **Other Exceptions**: Retry with backoff
3. **Calculate Delay**: Uses exponential backoff formula: `min(base_delay * (2 ^ retry_count), max_delay)`
4. **Wait**: Pauses for the calculated delay
5. **Retry**: Creates a fresh bot instance and attempts to reconnect
6. **Repeat**: Continues until successful or max retries reached

## Configuration

### Default Settings

```json
{
  "discord": {
    "token": "YOUR_TOKEN",
    "reconnect": {
      "enabled": true,
      "max_retries": 10,
      "base_delay": 5,
      "max_delay": 300
    }
  }
}
```

### Configuration Options

#### `enabled` (boolean)
- **Default**: `true`
- **Description**: Master switch for automatic reconnection
- **Use Case**: Set to `false` for debugging or when you want the bot to exit on connection failures

#### `max_retries` (integer)
- **Default**: `10`
- **Description**: Maximum number of reconnection attempts before giving up
- **Use Case**: Increase for more persistent reconnection, decrease for faster failure detection

#### `base_delay` (integer, seconds)
- **Default**: `5`
- **Description**: Initial delay before the first retry attempt
- **Use Case**: Increase if you want to avoid rapid retries, decrease for faster recovery

#### `max_delay` (integer, seconds)
- **Default**: `300` (5 minutes)
- **Description**: Maximum delay between retry attempts (caps exponential backoff)
- **Use Case**: Adjust based on your tolerance for waiting between attempts

## Retry Delay Examples

With default settings (`base_delay=5`, `max_delay=300`):

| Attempt | Delay (seconds) | Cumulative Wait |
|---------|----------------|-----------------|
| 1       | 5              | 5s              |
| 2       | 10             | 15s             |
| 3       | 20             | 35s             |
| 4       | 40             | 1m 15s          |
| 5       | 80             | 2m 35s          |
| 6       | 160            | 5m 15s          |
| 7       | 300 (capped)   | 10m 15s         |
| 8       | 300 (capped)   | 15m 15s         |
| 9       | 300 (capped)   | 20m 15s         |
| 10      | 300 (capped)   | 25m 15s         |

## Error Handling

### Login Failure
```text
[ERROR] Login failed: Improper token has been passed.
Please check your Discord bot token in config.json
The token may be invalid or expired.
```
**Action**: Bot exits immediately (no retry). You must fix the token in config.json.

### HTTP Exception
```text
[ERROR] HTTP Exception: 503 Service Unavailable
Will retry in 5 seconds... (Attempt 1/10)
```
**Action**: Bot retries with exponential backoff. Discord API may be temporarily unavailable.

### Gateway Not Found
```text
[ERROR] Gateway not found: The gateway to connect to Discord was not found.
Discord's gateway service may be down.
Will retry in 5 seconds... (Attempt 1/10)
```
**Action**: Bot retries with exponential backoff. Discord's gateway service may be temporarily down.

### Unexpected Error
```text
[ERROR] Unexpected error: [Error details]
[Full stack trace]
Will retry in 5 seconds... (Attempt 1/10)
```
**Action**: Bot retries with exponential backoff. Unknown errors are treated as potentially recoverable.

### Max Retries Reached
```text
Max retries (10) reached. Giving up.
```
**Action**: Bot exits. Manual intervention required.

## Console Output

### Successful Connection
```text
Starting Discord bot... (Attempt 1)
[Bot connects successfully]
```

### Reconnection Attempt
```text
Starting Discord bot... (Attempt 2)
  Reconnection enabled: True
  Max retries: 10

[ERROR] HTTP Exception: 503 Service Unavailable
Will retry in 5 seconds... (Attempt 2/10)
```

### Graceful Shutdown
```text
Bot shut down gracefully.
```

### Keyboard Interrupt
```text
[INFO] Received keyboard interrupt. Shutting down...
```

## Use Cases

### Temporary Network Issues
**Scenario**: Your server experiences a brief network interruption.
**Result**: Bot automatically reconnects once the network is restored, without any downtime beyond the retry delay.

### Discord API Rate Limiting
**Scenario**: Discord's API is rate-limiting connections.
**Result**: Exponential backoff ensures the bot doesn't hammer the API, eventually reconnecting successfully.

### Discord Service Outage
**Scenario**: Discord's gateway service is temporarily down.
**Result**: Bot keeps trying with increasing delays, reconnecting once Discord's service is restored.

### Invalid Token
**Scenario**: The bot token is invalid or has been regenerated.
**Result**: Bot immediately exits with a clear error message, prompting you to update the token.

## Best Practices

### For Production Deployments

1. **Keep Defaults**: The default settings are well-balanced for most use cases
2. **Monitor Logs**: Regularly check console output for connection issues
3. **Set Up Process Manager**: Use a process manager (systemd, PM2, Docker restart policies) as an additional layer of reliability
4. **Alert on Max Retries**: Set up monitoring to alert you when max retries are reached

### For Development

1. **Disable for Debugging**: Set `enabled: false` when debugging connection-related code
2. **Reduce Max Delay**: Set `max_delay: 30` for faster iteration during testing
3. **Increase Base Delay**: Set `base_delay: 10` to give yourself time to read error messages

### For Unstable Networks

1. **Increase Max Retries**: Set to 20 or higher for very unreliable networks
2. **Increase Max Delay**: Set to 600 (10 minutes) to handle longer outages
3. **Monitor Patterns**: Track when failures occur to identify underlying network issues

## Disabling Reconnection

To disable automatic reconnection, edit `config.json`:

```json
{
  "discord": {
    "token": "YOUR_TOKEN",
    "reconnect": {
      "enabled": false
    }
  }
}
```

With reconnection disabled, the bot will exit immediately on any connection failure, matching the previous behavior.

## Comparison with Discord.py's Built-in Reconnect

| Feature | Discord.py reconnect=True | Our Implementation |
|---------|---------------------------|-------------------|
| Handles WebSocket disconnects | ✅ Yes | ✅ Yes |
| Handles initial connection failures | ❌ No | ✅ Yes |
| Exponential backoff | ✅ Yes | ✅ Yes |
| Configurable retry count | ❌ No | ✅ Yes |
| Configurable delays | ❌ No | ✅ Yes |
| Login failure handling | ❌ Retries forever | ✅ Exits immediately |
| Clear logging | ⚠️ Minimal | ✅ Detailed |

**Note**: Our implementation works in conjunction with discord.py's built-in reconnection (`bot.run(token, reconnect=True)`), providing an additional layer of reliability for startup failures.

## Troubleshooting

### Bot Keeps Retrying Forever
**Problem**: Bot continues retrying even though the issue won't resolve automatically.
**Solution**: Press `Ctrl+C` to interrupt the bot, fix the underlying issue, then restart.

### Bot Exits Too Quickly
**Problem**: Bot gives up before connection is restored.
**Solution**: Increase `max_retries` in config.json.

### Bot Waits Too Long Between Attempts
**Problem**: Delays between retries are too long.
**Solution**: Decrease `max_delay` in config.json.

### Bot Retries Too Quickly
**Problem**: Bot hammers Discord's API with rapid retries.
**Solution**: Increase `base_delay` in config.json.

## Technical Implementation

The reconnection logic is implemented in the `main()` function of `bot.py`:

1. Infinite loop wraps the bot startup
2. Try-except blocks catch specific Discord exceptions
3. Exponential backoff calculated with: `min(base_delay * (2 ** (retry_count - 1)), max_delay)`
4. Fresh bot instance created on each retry (prevents state issues)
5. Break conditions:
   - Login failure (token issue)
   - Max retries reached
   - Keyboard interrupt
   - Graceful shutdown

## See Also

- [README.md](README.md) - Main documentation
- [INTERACTIVE_CONFIG_GUIDE.md](INTERACTIVE_CONFIG_GUIDE.md) - Interactive configuration
- Discord.py Documentation: [Bot.run()](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.Bot.run)
