#feature 1 - Recency decay 

import math 
from datetime import datetime, timezone

def exponential_decay(ts, now=None, half_life_days = 7 ):
    
    if now is None:
        now = datetime.now(timezone.utc)
        
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
        
    delta_days = (now - ts).total_seconds()/(3600*24)
    return math.exp(-math.log(2)* delta_days/half_life_days)    