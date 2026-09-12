import re

with open("app/src/main/java/io/github/vvb2060/ims/MainActivity.java", "r") as f:
    text = f.read()

# Fix the string builders
old_china = """            if (isChina) {
                sb.append(getString(R.string.china_main_sim_tips)).append("\\n");
                if (config != null) {
                    boolean volte = config.getBoolean("carrier_volte_available_bool", false);
                    sb.append(" - carrier_volte_available_bool: ").append(volte).append("\\n");
                }
            }"""

new_china = """            if (isChina) {
                sb.append(getString(R.string.china_main_sim_tips)).append("\\n");
                if (config != null) {
                    boolean volte = config.getBoolean("carrier_volte_available_bool", false);
                    sb.append(" - ").append(getString(R.string.prop_volte)).append(": ").append(volte ? "✅" : "❎").append("\\n");
                }
            }"""
text = text.replace(old_china, new_china)


old_foreign = """            if (isEsim || isForeign) {
                if (config != null) {
                    boolean provReq = config.getBoolean("carrier_wfc_provisioning_required_bool", false);
                    boolean roamingWfc = config.getBoolean("carrier_default_wfc_ims_roaming_enabled_bool", false);
                    boolean wifiOnly = config.getBoolean("carrier_wfc_supports_wifi_only_bool", false);
                    boolean wfcAvail = config.getBoolean("carrier_wfc_ims_available_bool", false);
                    
                    sb.append(" - carrier_wfc_provisioning_required_bool: ").append(provReq).append("\\n");
                    sb.append(" - carrier_default_wfc_ims_roaming_enabled_bool: ").append(roamingWfc).append("\\n");
                    sb.append(" - carrier_wfc_supports_wifi_only_bool: ").append(wifiOnly).append("\\n");
                    sb.append(" - carrier_wfc_ims_available_bool: ").append(wfcAvail).append("\\n");
                } else {
                    sb.append(" Cannot read carrier config.\\n");
                }
            }"""

new_foreign = """            if (isEsim || isForeign) {
                if (config != null) {
                    boolean provReq = config.getBoolean("carrier_wfc_provisioning_required_bool", false);
                    boolean roamingWfc = config.getBoolean("carrier_default_wfc_ims_roaming_enabled_bool", false);
                    boolean wifiOnly = config.getBoolean("carrier_wfc_supports_wifi_only_bool", false);
                    boolean wfcAvail = config.getBoolean("carrier_wfc_ims_available_bool", false);
                    
                    sb.append(" - ").append(getString(R.string.prop_prov_req)).append(": ").append(provReq ? "✅" : "❎").append("\\n");
                    sb.append(" - ").append(getString(R.string.prop_roaming_wfc)).append(": ").append(roamingWfc ? "✅" : "❎").append("\\n");
                    sb.append(" - ").append(getString(R.string.prop_wifi_only)).append(": ").append(wifiOnly ? "✅" : "❎").append("\\n");
                    sb.append(" - ").append(getString(R.string.prop_wfc_avail)).append(": ").append(wfcAvail ? "✅" : "❎").append("\\n");
                } else {
                    sb.append(" Cannot read carrier config.\\n");
                }
            }"""
text = text.replace(old_foreign, new_foreign)

# Also update the title setting in layout if it's hardcoded anywhere, but it's set in activity_main.xml?
# Let's check activity_main.xml
with open("app/src/main/java/io/github/vvb2060/ims/MainActivity.java", "w") as f:
    f.write(text)
print("Main activity patched")
