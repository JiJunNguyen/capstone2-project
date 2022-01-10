import time
from datetime import timedelta
start_time = time.monotonic()
time.sleep(5)
end_time = time.monotonic()
tt = timedelta(seconds=end_time - start_time)
print(tt)