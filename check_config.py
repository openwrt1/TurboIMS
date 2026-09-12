import urllib.request
import re

url = "https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/master/telephony/java/android/telephony/CarrierConfigManager.java"
try:
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    keys = re.findall(r'public static final String KEY_[A-Z0-9_]+', content)
    for k in keys:
        if 'CELL' in k or 'LOC' in k or 'ROAMING' in k or 'WFC' in k or 'IWLAN' in k or 'IKE' in k or 'NET' in k or 'PAN' in k:
            print(k)
except Exception as e:
    print("Error:", e)
