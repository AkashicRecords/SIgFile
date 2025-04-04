from typing import List, Dict, Optional
import subprocess
import re
import os
from .base_monitor import BaseMonitor, ProcessInfo

class LinuxMonitor(BaseMonitor):
    """Linux-specific monitor using native tools."""
    
    def _validate_platform(self) -> None:
        """Validate that we're running on Linux."""
        if self.system != 'linux':
            raise NotImplementedError("LinuxMonitor only works on Linux")
    
    def get_process_info(self, pid: Optional[int] = None) -> List[ProcessInfo]:
        """Get process information using ps and top commands."""
        processes = []
        
        # Use ps for basic process info
        ps_command = ['ps', '-eo', 'pid,comm,%cpu,%mem,rss,stat,command']
        if pid:
            ps_command.extend(['-p', str(pid)])
        
        ps_output = self._run_command(ps_command)
        
        # Skip header line
        for line in ps_output.split('\n')[1:]:
            if not line.strip():
                continue
                
            # Parse ps output
            parts = line.split(maxsplit=6)
            if len(parts) >= 7:
                try:
                    process = ProcessInfo(
                        pid=int(parts[0]),
                        name=parts[1],
                        cpu_percent=float(parts[2]),
                        memory_percent=float(parts[3]),
                        memory_bytes=int(parts[4]) * 1024,  # Convert KB to bytes
                        status=parts[5],
                        command=parts[6]
                    )
                    processes.append(process)
                except (ValueError, IndexError):
                    continue
        
        return processes
    
    def get_system_metrics(self) -> Dict:
        """Get system-wide metrics using /proc filesystem."""
        metrics = {
            'cpu': self._get_cpu_metrics(),
            'memory': self._get_memory_metrics(),
            'disk': self._get_disk_metrics(),
            'network': self._get_network_metrics()
        }
        return metrics
    
    def _get_cpu_metrics(self) -> Dict:
        """Get CPU metrics from /proc/stat."""
        cpu_info = {}
        try:
            with open('/proc/stat', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('cpu '):
                        parts = line.split()
                        total = sum(int(x) for x in parts[1:])
                        idle = int(parts[4])
                        cpu_info.update({
                            'usage': 100 - (idle * 100 / total),
                            'idle': idle * 100 / total
                        })
                        break
        except Exception:
            pass
        
        return cpu_info
    
    def _get_memory_metrics(self) -> Dict:
        """Get memory metrics from /proc/meminfo."""
        memory_info = {}
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = {}
                for line in f:
                    key, value = line.split(':')
                    meminfo[key.strip()] = int(value.strip().split()[0]) * 1024  # Convert KB to bytes
                
                memory_info.update({
                    'total': meminfo.get('MemTotal', 0),
                    'free': meminfo.get('MemFree', 0),
                    'buffers': meminfo.get('Buffers', 0),
                    'cached': meminfo.get('Cached', 0),
                    'used': meminfo.get('MemTotal', 0) - meminfo.get('MemFree', 0)
                })
        except Exception:
            pass
        
        return memory_info
    
    def _get_disk_metrics(self) -> Dict:
        """Get disk metrics using df command."""
        disk_info = {}
        try:
            df_command = ['df', '-B1']  # Show sizes in bytes
            df_output = self._run_command(df_command)
            
            for line in df_output.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 6:
                        mount = parts[5]
                        disk_info[mount] = {
                            'total': int(parts[1]),
                            'used': int(parts[2]),
                            'free': int(parts[3])
                        }
        except Exception:
            pass
        
        return disk_info
    
    def _get_network_metrics(self) -> Dict:
        """Get network metrics from /proc/net/dev."""
        network_info = {}
        try:
            with open('/proc/net/dev', 'r') as f:
                for line in f:
                    if ':' in line:
                        interface, data = line.split(':')
                        interface = interface.strip()
                        if interface != 'lo':  # Skip loopback
                            parts = data.split()
                            if len(parts) >= 16:
                                network_info[interface] = {
                                    'ibytes': int(parts[0]),
                                    'obytes': int(parts[8])
                                }
        except Exception:
            pass
        
        return network_info 