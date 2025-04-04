# SigFile Project

## Protection Methods
- Unix/Linux: chmod 444 + chattr +i
- macOS: chmod 444 + chflags uchg
- Windows: attrib +R +S +H + ACL restrictions

## Directory Structure
- changes: Contains daily change records and change history
- backups: Stores backup copies of changed files
- logs: Contains system and change tracking logs
- docs: Project documentation and file structure info
- ai_conversations: Stores AI interaction records
- thinking: Contains AI thinking process records
- handoffs: Stores handoff records between systems
