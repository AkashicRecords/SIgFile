from typing import List, Dict, Optional
import subprocess
import re
from .base_monitor import BaseMonitor, ProcessInfo

class MacOSMonitor(BaseMonitor):
    """macOS-specific monitor using native tools."""
    
    def _validate_platform(self) -> None:
        """Validate that we're running on macOS."""
        if self.system != 'darwin':
            raise NotImplementedError("MacOSMonitor only works on macOS")
    
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
        """Get system-wide metrics using top and vm_stat."""
        metrics = {
            'cpu': self._get_cpu_metrics(),
            'memory': self._get_memory_metrics(),
            'disk': self._get_disk_metrics(),
            'network': self._get_network_metrics()
        }
        return metrics
    
    def _get_cpu_metrics(self) -> Dict:
        """Get CPU metrics using top command."""
        top_output = self._run_command(['top', '-l', '1', '-n', '0'])
        cpu_info = {}
        
        # Extract CPU usage
        cpu_match = re.search(r'CPU usage: ([\d.]+)% user, ([\d.]+)% sys, ([\d.]+)% idle', top_output)
        if cpu_match:
            cpu_info.update({
                'user': float(cpu_match.group(1)),
                'system': float(cpu_match.group(2)),
                'idle': float(cpu_match.group(3))
            })
        
        return cpu_info
    
    def _get_memory_metrics(self) -> Dict:
        """Get memory metrics using vm_stat command."""
        vm_stat_output = self._run_command(['vm_stat'])
        memory_info = {}
        
        # Extract memory statistics
        page_size = 4096  # Default page size in bytes
        stats = {}
        for line in vm_stat_output.split('\n'):
            if ':' in line:
                key, value = line.split(':')
                stats[key.strip()] = int(value.strip().rstrip('.'))
        
        # Calculate memory metrics
        if stats:
            memory_info.update({
                'free': stats.get('Pages free', 0) * page_size,
                'active': stats.get('Pages active', 0) * page_size,
                'inactive': stats.get('Pages inactive', 0) * page_size,
                'wired': stats.get('Pages wired down', 0) * page_size
            })
        
        return memory_info
    
    def _get_disk_metrics(self) -> Dict:
        """Get disk metrics using iostat command."""
        iostat_output = self._run_command(['iostat'])
        disk_info = {}
        
        # Parse iostat output
        lines = iostat_output.split('\n')
        if len(lines) >= 3:
            headers = lines[1].split()
            values = lines[2].split()
            if len(headers) == len(values):
                disk_info = dict(zip(headers, [float(v) for v in values]))
        
        return disk_info
    
    def _get_network_metrics(self) -> Dict:
        """Get network metrics using netstat command."""
        netstat_output = self._run_command(['netstat', '-ib'])
        network_info = {}
        
        # Parse netstat output
        for line in netstat_output.split('\n'):
            if 'en0' in line:  # Primary network interface
                parts = line.split()
                if len(parts) >= 10:
                    network_info.update({
                        'interface': parts[0],
                        'ibytes': int(parts[6]),
                        'obytes': int(parts[9])
                    })
                break
        
        return network_info 