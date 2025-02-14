import os


def A5():
    log_dir = "./data/logs"
    output_file = "./data/logs-recent.txt"
    
    if not os.path.isdir(log_dir):
        raise FileNotFoundError("Logs directory not found")
    
    try:
        log_files = sorted(
            [f for f in os.listdir(log_dir) if f.endswith(".log")],
            key=lambda f: os.path.getmtime(os.path.join(log_dir, f)),
            reverse=True
        )[:10]
        
        with open(output_file, "w", encoding="utf-8") as outfile:
            for log_file in log_files:
                log_path = os.path.join(log_dir, log_file)
                with open(log_path, "r", encoding="utf-8") as infile:
                    first_line = infile.readline().strip()
                    outfile.write(first_line + "\n")
        
        return "Recent logs extracted successfully."
    except Exception as e:
        raise RuntimeError(f"Error processing log files: {e}")