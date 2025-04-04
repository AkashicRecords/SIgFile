from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional
import platform
import subprocess
import json
import time

@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_bytes: int
    status: str
    command: str

class BaseMonitor(ABC):
    """Base class for native system monitoring integration."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self._validate_platform()
    
    @abstractmethod
    def _validate_platform(self) -> None:
        """Validate that the current platform is supported."""
        pass
    
    @abstractmethod
    def get_process_info(self, pid: Optional[int] = None) -> List[ProcessInfo]:
        """Get information about running processes."""
        pass
    
    @abstractmethod
    def get_system_metrics(self) -> Dict:
        """Get system-wide metrics."""
        pass
    
    def monitor_process(self, pid: int, interval: float = 1.0) -> None:
        """Monitor a specific process in real-time."""
        try:
            while True:
                process_info = self.get_process_info(pid)
                if process_info:
                    self._display_process_info(process_info[0])
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    
    def _display_process_info(self, process: ProcessInfo) -> None:
        """Display process information in a formatted way."""
        print(f"\nProcess: {process.name} (PID: {process.pid})")
        print(f"CPU: {process.cpu_percent:.1f}% | Memory: {process.memory_percent:.1f}% ({process.memory_bytes / 1024 / 1024:.1f} MB)")
        print(f"Status: {process.status}")
        print(f"Command: {process.command}")
    
    def _run_command(self, command: List[str]) -> str:
        """Run a system command and return its output."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command {' '.join(command)}: {e}")
            return ""
    
    def to_json(self, data: Dict) -> str:
        """Convert monitoring data to JSON format."""
        return json.dumps(data, indent=2)
    
    @staticmethod
    def create_monitor():
        """Factory method to create the appropriate monitor for the current platform."""
        system = platform.system().lower()
        if system == 'darwin':
            from .macos_monitor import MacOSMonitor
            return MacOSMonitor()
        elif system == 'windows':
            from .windows_monitor import WindowsMonitor
            return WindowsMonitor()
        elif system == 'linux':
            from .linux_monitor import LinuxMonitor
            return LinuxMonitor()
        else:
            raise NotImplementedError(f"Platform {system} is not supported") 