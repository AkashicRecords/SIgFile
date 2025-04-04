from models.affected_files import AffectedFiles

def main():
    # Create a new AffectedFiles instance
    affected = AffectedFiles()
    
    # Add some example files
    affected.add_new_file(
        "src/scripts/proxy_server.py",
        "Main proxy server implementation for Cursor traffic filtering"
    )
    affected.add_new_file(
        "src/scripts/traffic_filter.py",
        "Traffic filtering logic for extracting chat and thinking processes"
    )
    affected.add_modified_file(
        "src/scripts/cli.py",
        "Added proxy server integration and configuration options"
    )
    affected.add_deleted_file(
        "src/scripts/old_proxy.py",
        "Replaced with new proxy server implementation"
    )
    
    # Print in markdown format
    print("Markdown Format:")
    print(affected.to_markdown())
    
    print("\nYAML Format:")
    print(affected.to_yaml())
    
    # Validate paths
    errors = affected.validate_paths()
    if errors:
        print("\nValidation Errors:")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    main() 