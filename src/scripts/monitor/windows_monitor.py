from typing import List, Dict, Optional
import subprocess
import re
from .base_monitor import BaseMonitor, ProcessInfo

class WindowsMonitor(BaseMonitor):
    """Windows-specific monitor using native tools."""
    
    def _validate_platform(self) -> None:
        """Validate that we're running on Windows."""
        if self.system != 'windows':
            raise NotImplementedError("WindowsMonitor only works on Windows")
    
    def get_process_info(self, pid: Optional[int] = None) -> List[ProcessInfo]:
        """Get process information using tasklist and wmic commands."""
        processes = []
        
        # Use tasklist for basic process info
        tasklist_command = ['tasklist', '/FO', 'CSV', '/NH']
        if pid:
            tasklist_command.extend(['/FI', f'PID eq {pid}'])
        
        tasklist_output = self._run_command(tasklist_command)
        
        for line in tasklist_output.split('\n'):
            if not line.strip():
                continue
                
            # Parse CSV output
            parts = [p.strip('"') for p in line.split(',')]
            if len(parts) >= 5:
                try:
                    # Get detailed memory info using wmic
                    wmic_command = ['wmic', 'process', 'where', f'ProcessId={parts[1]}', 'get', 'WorkingSetSize,CommandLine', '/format:csv']
                    wmic_output = self._run_command(wmic_command)
                    
                    memory_bytes = 0
                    command = parts[0]
                    if wmic_output:
                        wmic_parts = wmic_output.split(',')
                        if len(wmic_parts) >= 3:
                            memory_bytes = int(wmic_parts[1]) if wmic_parts[1].isdigit() else 0
                            command = wmic_parts[2] if len(wmic_parts) > 2 else parts[0]
                    
                    process = ProcessInfo(
                        pid=int(parts[1]),
                        name=parts[0],
                        cpu_percent=0.0,  # Will be updated with performance counters
                        memory_percent=float(parts[4].rstrip(' K')) / 1024,  # Convert KB to MB
                        memory_bytes=memory_bytes,
                        status=parts[2],
                        command=command
                    )
                    processes.append(process)
                except (ValueError, IndexError):
                    continue
        
        return processes
    
    def get_system_metrics(self) -> Dict:
        """Get system-wide metrics using wmic and typeperf."""
        metrics = {
            'cpu': self._get_cpu_metrics(),
            'memory': self._get_memory_metrics(),
            'disk': self._get_disk_metrics(),
            'network': self._get_network_metrics()
        }
        return metrics
    
    def _get_cpu_metrics(self) -> Dict:
        """Get CPU metrics using typeperf command."""
        cpu_info = {}
        try:
            # Get CPU usage using typeperf
            typeperf_command = ['typeperf', '\\Processor(_Total)\\% Processor Time', '-sc', '1']
            typeperf_output = self._run_command(typeperf_command)
            
            if typeperf_output:
                # Parse the output to get CPU usage
                lines = typeperf_output.split('\n')
                if len(lines) >= 3:
                    value = float(lines[2].split(',')[1].strip('"'))
                    cpu_info.update({
                        'usage': value,
                        'idle': 100 - value
                    })
        except Exception:
            pass
        
        return cpu_info
    
    def _get_memory_metrics(self) -> Dict:
        """Get memory metrics using wmic command."""
        memory_info = {}
        try:
            # Get memory info using wmic
            wmic_command = ['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize', '/format:csv']
            wmic_output = self._run_command(wmic_command)
            
            if wmic_output:
                parts = wmic_output.split(',')
                if len(parts) >= 3:
                    free = int(parts[1]) * 1024  # Convert KB to bytes
                    total = int(parts[2]) * 1024  # Convert KB to bytes
                    memory_info.update({
                        'free': free,
                        'total': total,
                        'used': total - free
                    })
        except Exception:
            pass
        
        return memory_info
    
    def _get_disk_metrics(self) -> Dict:
        """Get disk metrics using wmic command."""
        disk_info = {}
        try:
            # Get disk info using wmic
            wmic_command = ['wmic', 'logicaldisk', 'where', 'DriveType=3', 'get', 'FreeSpace,Size', '/format:csv']
            wmic_output = self._run_command(wmic_command)
            
            if wmic_output:
                for line in wmic_output.split('\n')[1:]:
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 3:
                            drive = parts[0].strip('"')
                            free = int(parts[1]) if parts[1].isdigit() else 0
                            total = int(parts[2]) if parts[2].isdigit() else 0
                            disk_info[drive] = {
                                'free': free,
                                'total': total,
                                'used': total - free
                            }
        except Exception:
            pass
        
        return disk_info
    
    def _get_network_metrics(self) -> Dict:
        """Get network metrics using netstat command."""
        network_info = {}
        try:
            # Get network info using netstat
            netstat_command = ['netstat', '-e']
            netstat_output = self._run_command(netstat_command)
            
            if netstat_output:
                for line in netstat_output.split('\n'):
                    if 'Bytes' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            network_info.update({
                                'ibytes': int(parts[1]),
                                'obytes': int(parts[2])
                            })
                        break
        except Exception:
            pass
        
        return network_info 