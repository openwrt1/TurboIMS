import re

def update_strings(filepath, is_zh=False):
    with open(filepath, "r") as f:
        content = f.read()
    
    if is_zh:
        content = re.sub(r'<string name="app_name">Turbo IMS</string>', r'<string name="app_name">Pixel8电话适配助手</string>', content)
        content = re.sub(r'<string name="title">Turbo IMS 配置</string>', r'<string name="title">Pixel8电话适配助手</string>', content)
        content = re.sub(r'<string name="china_main_sim_tips">.*?</string>', r'<string name="china_main_sim_tips">检测到中国大陆主卡，必须开启 VoLTE 才能正常通话！（为避免 Pixel 8 耗电，建议不要开启 5G 和跨 SIM 卡通话）</string>', content)
        
        new_props = """
    <!-- Properties -->
    <string name="prop_volte">VoLTE (4G 高清通话)</string>
    <string name="prop_prov_req">资格审查</string>
    <string name="prop_roaming_wfc">漫游 WiFi Calling 支持</string>
    <string name="prop_wifi_only">纯 WiFi 支持</string>
    <string name="prop_wfc_avail">WiFi Calling 总开关</string>
</resources>"""
    else:
        content = re.sub(r'<string name="app_name">Turbo IMS</string>', r'<string name="app_name">Pixel 8 Call Assistant</string>', content)
        content = re.sub(r'<string name="title">Turbo IMS Configuration</string>', r'<string name="title">Pixel 8 Call Assistant</string>', content)
        content = re.sub(r'<string name="china_main_sim_tips">.*?</string>', r'<string name="china_main_sim_tips">Mainland China SIM detected. MUST enable VoLTE to make calls. (To save battery on Pixel 8, avoid enabling 5G and Cross-SIM calling)</string>', content)
        
        new_props = """
    <!-- Properties -->
    <string name="prop_volte">VoLTE (4G Voice)</string>
    <string name="prop_prov_req">Provisioning Required</string>
    <string name="prop_roaming_wfc">Roaming WiFi Calling</string>
    <string name="prop_wifi_only">WiFi Only Support</string>
    <string name="prop_wfc_avail">WiFi Calling Available</string>
</resources>"""

    content = content.replace("</resources>", new_props)
    
    with open(filepath, "w") as f:
        f.write(content)

update_strings("app/src/main/res/values/strings.xml", False)
update_strings("app/src/main/res/values-zh/strings.xml", True)
print("Strings updated")
