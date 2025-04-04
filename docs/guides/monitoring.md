# Real-Time SigFile Monitoring Guide

## Overview
This guide explains how to use the real-time monitoring feature to track SigFile activities and performance. The monitor works with any shell, including zsh.

## Basic Usage

### Starting Monitoring
```shell
# Start basic monitoring
sigfile monitor

# Set update interval (seconds)
sigfile monitor --interval 1

# Focus on specific aspect
sigfile monitor --focus records
```

### Display Options
```shell
# Sort by CPU usage
sigfile monitor --sort cpu

# Filter active processes
sigfile monitor --filter active

# Show detailed view
sigfile monitor --show details
```

## Shell-Specific Features

### zsh Integration
- Tab completion for commands
- Command history integration
- Custom zsh aliases support
- zsh-specific key bindings

### Shell-Agnostic Features
- Works in any POSIX-compliant shell
- Consistent behavior across shells
- Standard terminal support
- Universal keyboard controls

## Monitoring Features

### Process Monitoring
- Active SigFile processes
- Process status
- Resource usage
- Performance metrics

### Resource Tracking
- CPU usage
- Memory usage
- Disk I/O
- Network activity

### Record Tracking
- Active records
- Record types
- Update frequency
- Storage usage

## Interactive Controls

### Keyboard Commands
- `q`: Quit monitoring
- `s`: Sort menu
- `f`: Filter menu
- `p`: Pause/Resume
- `h`: Help information

### Sorting Options
- CPU usage
- Memory usage
- Process ID
- Record count
- Update time

### Filtering Options
- Active processes
- Specific record types
- Resource thresholds
- Time ranges

## Examples

### Basic Monitoring
```shell
$ sigfile monitor
SigFile Monitor v1.0
Processes: 3 | Records: 5 | CPU: 2% | Memory: 45MB
----------------------------------------
PID    TYPE    STATUS    CPU%    MEM%    RECORDS
1234   CLI     Active    1.2     15      2
1235   AI      Active    0.8     25      3
1236   DB      Idle      0.0     5       0
```

### Focused Monitoring
```shell
$ sigfile monitor --focus records --sort count
Record Monitor
----------------------------------------
TYPE        COUNT    UPDATES    SIZE
Decision    3        5          45KB
Change      2        3          30KB
Debug       1        1          15KB
```

### Detailed View
```shell
$ sigfile monitor --show details
Detailed Monitor
----------------------------------------
Process: CLI (1234)
Status: Active
CPU: 1.2% | Memory: 15MB
Records: 2
- decision_013_realtime_monitoring.md
- change_20240404_0004.json
```

## Best Practices

1. **Regular Monitoring**
   - Check system regularly
   - Monitor resource usage
   - Track performance trends
   - Identify issues early

2. **Resource Management**
   - Set appropriate intervals
   - Use focused monitoring
   - Apply filters when needed
   - Monitor storage usage

3. **Troubleshooting**
   - Watch for high CPU usage
   - Monitor memory leaks
   - Track record growth
   - Check process status

4. **Performance Optimization**
   - Adjust update intervals
   - Use appropriate filters
   - Focus on key metrics
   - Monitor trends

## Troubleshooting

1. **High Resource Usage**
   - Reduce update interval
   - Apply more filters
   - Focus on specific aspects
   - Check for issues

2. **Display Issues**
   - Adjust terminal size
   - Check color support
   - Verify encoding
   - Update terminal

3. **Performance Problems**
   - Monitor system load
   - Check disk space
   - Verify permissions
   - Review logs

## Support

For additional help:
- Use `sigfile monitor --help`
- Check the documentation
- Contact support 