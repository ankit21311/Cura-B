import os
import ast

def analyze_code(root_dir):
    total_modules = 0
    total_functions = 0
    total_parameters = 0
    
    # Exclude these directories
    excludes = {'venv', '.git', '__pycache__', 'migrations'}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in excludes]
        
        for filename in filenames:
            if filename.endswith('.py'):
                total_modules += 1
                filepath = os.path.join(dirpath, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                            total_functions += 1
                            # Count args
                            args = node.args
                            # standard args + keyword only args + vararg + kwarg
                            param_count = len(args.args) + len(args.posonlyargs) + len(args.kwonlyargs)
                            if args.vararg: param_count += 1
                            if args.kwarg: param_count += 1
                            
                            total_parameters += param_count
                            
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")

    print(f"Modules: {total_modules}")
    print(f"Functions: {total_functions}")
    print(f"Parameters: {total_parameters}")

if __name__ == "__main__":
    analyze_code(r"c:\Users\sarthak\Downloads\hospital-system (2)\hospital-system")
