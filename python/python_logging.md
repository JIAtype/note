# 设置日志记录 Setup logging
try:
    # Ensure log directory exists
    log_dir = os.path.dirname(os.path.abspath("logs/mscdae_test.log"))
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/mscdae_test.log", mode='a'),  # 改为追加模式
            logging.StreamHandler()
        ]
    )
    # Force output of initial log to confirm logging system is working
    logging.info("Logging system initialized")
except Exception as e:
    print(f"Error setting up logging system: {str(e)}")

logger = logging.getLogger("MscdaeModule")

# Confirm logger is working properly
logger.info("Mscdae module initialized")

# 关闭日志记录
logging.shutdown()

# 删除日志文件
log_file_path = "logs/mscdae_test.log"
if os.path.exists(log_file_path):
    os.remove(log_file_path)
    print(f"日志文件 '{log_file_path}' 已删除。")
else:
    print(f"日志文件 '{log_file_path}' 不存在。")
