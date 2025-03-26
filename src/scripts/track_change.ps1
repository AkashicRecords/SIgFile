# SigFile.ai - Windows PowerShell Version
# Change tracking and backup system for Windows

# Configuration
$SIGFILE_DIR = "$env:USERPROFILE\sigfile"
$CONFIG_DIR = "$SIGFILE_DIR\config"
$CHANGES_DIR = "$SIGFILE_DIR\tracked_projects"
$BACKUPS_DIR = "$SIGFILE_DIR\backups"
$HANDOFF_DIR = "$SIGFILE_DIR\handoffs"

# Utility Functions
function Write-Log {
    param(
        [string]$Message,
        [string]$Type = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Type : $Message"
}

function Test-Command {
    param([string]$Command)
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

function New-Backup {
    param(
        [string]$File,
        [string]$Project
    )
    if (-not (Test-Path $File)) {
        Write-Log "File not found: $File" "ERROR"
        return $false
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = Join-Path $BACKUPS_DIR $Project $timestamp
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

    $fileName = Split-Path $File -Leaf
    $backupFile = Join-Path $backupDir $fileName
    Copy-Item $File $backupFile -Force

    Write-Log "Backup created: $backupFile"
    return $true
}

function Record-Change {
    param(
        [string]$Description,
        [string]$Files,
        [string]$Project
    )
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $dateDir = Get-Date -Format "yyyyMMdd"
    $changesDir = Join-Path $CHANGES_DIR $Project "changes" $dateDir
    New-Item -ItemType Directory -Path $changesDir -Force | Out-Null

    $changeFile = Join-Path $changesDir "changes_$timestamp.md"
    @"
# Change Record
- Description: $Description
- Files Changed: $Files
- Timestamp: $timestamp
"@ | Out-File -FilePath $changeFile -Encoding UTF8

    Write-Log "Change recorded: $changeFile"
}

function Show-History {
    param(
        [string]$Project,
        [string]$Date
    )
    if (-not $Date) {
        $Date = Get-Date -Format "yyyyMMdd"
    }

    $changesDir = Join-Path $CHANGES_DIR $Project "changes" $Date
    if (-not (Test-Path $changesDir)) {
        Write-Log "No changes found for date: $Date" "INFO"
        return
    }

    Get-ChildItem -Path $changesDir -Filter "*.md" | ForEach-Object {
        Write-Host "`n=== $($_.Name) ==="
        Get-Content $_.FullName
    }
}

function New-Handoff {
    param(
        [string]$ChatName,
        [string]$ChatId,
        [string]$Summary,
        [string]$NextSteps,
        [string]$Project
    )
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $dateDir = Get-Date -Format "yyyyMMdd"
    $handoffDir = Join-Path $HANDOFF_DIR $Project "handoffs" $dateDir
    New-Item -ItemType Directory -Path $handoffDir -Force | Out-Null

    $handoffFile = Join-Path $handoffDir "handoff_$timestamp.md"
    @"
# Handoff Document
- Chat Name: $ChatName
- Chat ID: $ChatId
- Timestamp: $timestamp

## Summary
$Summary

## Next Steps
$NextSteps
"@ | Out-File -FilePath $handoffFile -Encoding UTF8

    Write-Log "Handoff document created: $handoffFile"
}

function Initialize-SigFile {
    # Create necessary directories
    @($CONFIG_DIR, $CHANGES_DIR, $BACKUPS_DIR, $HANDOFF_DIR) | ForEach-Object {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }

    # Check dependencies
    $dependencies = @{
        "git" = "Git for Windows"
        "tree" = "Windows built-in tree command"
    }

    foreach ($dep in $dependencies.GetEnumerator()) {
        if (-not (Test-Command $dep.Key)) {
            Write-Log "Missing dependency: $($dep.Value)" "WARNING"
        }
    }

    Write-Log "SigFile initialized successfully"
}

# Main script
param(
    [string]$Command,
    [string]$Project = "default",
    [string]$Description,
    [string]$Files,
    [string]$ChatName,
    [string]$ChatId,
    [string]$Summary,
    [string]$NextSteps,
    [string]$Date
)

switch ($Command) {
    "setup" {
        Initialize-SigFile
    }
    "backup" {
        if (-not $Files) {
            Write-Log "Please specify a file to backup" "ERROR"
            exit 1
        }
        New-Backup -File $Files -Project $Project
    }
    "record" {
        if (-not $Description -or -not $Files) {
            Write-Log "Please provide both description and files changed" "ERROR"
            exit 1
        }
        Record-Change -Description $Description -Files $Files -Project $Project
    }
    "history" {
        Show-History -Project $Project -Date $Date
    }
    "handoff" {
        if (-not $ChatName -or -not $ChatId -or -not $Summary -or -not $NextSteps) {
            Write-Log "Please provide all required handoff information" "ERROR"
            exit 1
        }
        New-Handoff -ChatName $ChatName -ChatId $ChatId -Summary $Summary -NextSteps $NextSteps -Project $Project
    }
    default {
        Write-Host @"
Usage: .\track_change.ps1 [command] [options]

Commands:
  setup                    Initialize SigFile
  backup -Files <file>     Create a backup of a file
  record -Description "desc" -Files "files"  Record a change
  history [-Date YYYYMMDD] Show change history
  handoff -ChatName "name" -ChatId "id" -Summary "sum" -NextSteps "steps"  Generate handoff

Options:
  -Project <name>          Project name (default: default)
  -Date YYYYMMDD          Date for history (default: today)
"@
    }
} 