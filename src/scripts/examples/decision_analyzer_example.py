from models.decision_analyzer import DecisionAnalyzer
import gc

def analyze_decision_content():
    """Example of analyzing decision content with proper resource handling."""
    # Example decision content
    decision_content = """
    # Decision: Implement Cursor Proxy
    
    ## Context
    We need to create a proxy that filters Cursor traffic to extract chat and thinking processes.
    
    ## Implementation
    The implementation will involve:
    1. Creating a new proxy server in `src/scripts/proxy_server.py`
    2. Adding traffic filtering logic in `src/scripts/traffic_filter.py`
    3. Modifying `src/scripts/cli.py` to integrate the proxy
    4. Deleting the old implementation in `src/scripts/old_proxy.py`
    
    ## References
    See `docs/proxy_design.md` for more details.
    """
    
    # Use context manager to ensure proper cleanup
    with DecisionAnalyzer() as analyzer:
        # Analyze the decision content
        analysis = analyzer.analyze_decision(decision_content)
        
        try:
            # Print the analysis summary
            print("Analysis Summary:")
            print(analyzer.generate_summary(analysis))
            
            # Print detailed references
            print("\nDetailed References:")
            for section, files in analysis.references.items():
                if files:
                    print(f"\n{section.title()} Files:")
                    for file in files:
                        print(f"- `{file}`")
        finally:
            # Ensure analysis object is cleaned up
            del analysis

def analyze_decision_file(file_path: str):
    """Example of analyzing a decision file with proper resource handling."""
    with DecisionAnalyzer() as analyzer:
        try:
            analysis = analyzer.analyze_decision_file(file_path)
            print(analyzer.generate_summary(analysis))
        except Exception as e:
            print(f"Error analyzing file: {str(e)}")
        finally:
            # Ensure analysis object is cleaned up
            if 'analysis' in locals():
                del analysis

def main():
    try:
        # Example 1: Analyze content directly
        print("Analyzing decision content:")
        analyze_decision_content()
        
        # Example 2: Analyze a file
        print("\nAnalyzing decision file:")
        analyze_decision_file("tracked_projects/sigfile-cli/decisions/006_cursor_proxy_implementation.md")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
    finally:
        # Force garbage collection to ensure cleanup
        gc.collect()

if __name__ == "__main__":
    main() 