import re
import os

filepath = "app/src/main/java/io/github/vvb2060/ims/MainActivity.java"

with open(filepath, "r") as f:
    content = f.read()

# Add imports
imports_to_add = """import android.Manifest;
import android.telephony.CarrierConfigManager;
import android.telephony.SubscriptionInfo;
import android.telephony.SubscriptionManager;
import android.os.PersistableBundle;
import java.util.List;
"""
content = re.sub(r'import android.app.Activity;', imports_to_add + 'import android.app.Activity;', content, count=1)

# Add class fields
fields_to_add = """    private View layoutSimPermission;
    private Button btnGrantSimPermission;
    private TextView tvActiveSimDetails;
"""
content = re.sub(r'(private Switch switchEsimWfcRoaming;\n    private Button btnApply;)', r'\1\n' + fields_to_add, content, count=1)

# Add to initViews
init_views_to_add = """        layoutSimPermission = findViewById(R.id.layout_sim_permission);
        btnGrantSimPermission = findViewById(R.id.btn_grant_permission);
        tvActiveSimDetails = findViewById(R.id.tv_active_sim_details);

        btnGrantSimPermission.setOnClickListener(v -> {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                requestPermissions(new String[]{Manifest.permission.READ_PHONE_STATE}, 100);
            }
        });
"""
content = re.sub(r'(btnSelectSim = findViewById\(R.id.btn_select_sim\);\n        btnSwitchLanguage = findViewById\(R.id.btn_switch_language\);)', r'\1\n\n' + init_views_to_add, content, count=1)

# Add onResume to refresh info
on_resume_method = """
    @Override
    protected void onResume() {
        super.onResume();
        refreshActiveSimInfo();
    }
"""
content = re.sub(r'(@Override\n    protected void onDestroy\(\) {)', on_resume_method + r'\n    \1', content, count=1)

# Add onRequestPermissionsResult and refreshActiveSimInfo methods
methods_to_add = """
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 100) {
            refreshActiveSimInfo();
        }
    }

    private void refreshActiveSimInfo() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && checkSelfPermission(Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED) {
            tvActiveSimDetails.setVisibility(View.GONE);
            layoutSimPermission.setVisibility(View.VISIBLE);
            return;
        }

        layoutSimPermission.setVisibility(View.GONE);
        tvActiveSimDetails.setVisibility(View.VISIBLE);

        SubscriptionManager sm = getSystemService(SubscriptionManager.class);
        CarrierConfigManager cm = getSystemService(CarrierConfigManager.class);
        if (sm == null || cm == null) {
            tvActiveSimDetails.setText(R.string.no_active_sim_details);
            return;
        }

        List<SubscriptionInfo> activeList = null;
        try {
            activeList = sm.getActiveSubscriptionInfoList();
        } catch (SecurityException e) {
            Log.e(TAG, "No permission to get active subscriptions", e);
        }

        if (activeList == null || activeList.isEmpty()) {
            tvActiveSimDetails.setText(R.string.no_active_sim_details);
            return;
        }

        StringBuilder sb = new StringBuilder();
        for (SubscriptionInfo info : activeList) {
            int subId = info.getSubscriptionId();
            String mcc = info.getMccString();
            boolean isChina = mcc != null && mcc.startsWith("460");
            boolean isEsim = info.isEmbedded();
            boolean isForeign = mcc != null && !mcc.startsWith("460");
            
            sb.append("SIM ").append(info.getSimSlotIndex() + 1).append(" (SubId: ").append(subId).append(")\n");
            CharSequence carrierName = info.getCarrierName();
            sb.append("Carrier: ").append(carrierName != null ? carrierName.toString() : "Unknown").append("\n");
            
            PersistableBundle config = cm.getConfigForSubId(subId);
            
            if (isChina) {
                sb.append(getString(R.string.china_main_sim_tips)).append("\n");
                if (config != null) {
                    boolean volte = config.getBoolean("carrier_volte_available_bool", false);
                    sb.append(" - carrier_volte_available_bool: ").append(volte).append("\n");
                }
            }
            
            if (isEsim || isForeign) {
                if (config != null) {
                    boolean provReq = config.getBoolean("carrier_wfc_provisioning_required_bool", false);
                    boolean roamingWfc = config.getBoolean("carrier_default_wfc_ims_roaming_enabled_bool", false);
                    boolean wifiOnly = config.getBoolean("carrier_wfc_supports_wifi_only_bool", false);
                    boolean wfcAvail = config.getBoolean("carrier_wfc_ims_available_bool", false);
                    
                    sb.append(" - carrier_wfc_provisioning_required_bool: ").append(provReq).append("\n");
                    sb.append(" - carrier_default_wfc_ims_roaming_enabled_bool: ").append(roamingWfc).append("\n");
                    sb.append(" - carrier_wfc_supports_wifi_only_bool: ").append(wifiOnly).append("\n");
                    sb.append(" - carrier_wfc_ims_available_bool: ").append(wfcAvail).append("\n");
                } else {
                    sb.append(" Cannot read carrier config.\n");
                }
            }
            sb.append("\n");
        }
        
        tvActiveSimDetails.setText(sb.toString().trim());
    }
"""
content = re.sub(r'(@Override\n    protected void attachBaseContext)', methods_to_add + r'\n    \1', content, count=1)

with open(filepath, "w") as f:
    f.write(content)
print("Patch applied to MainActivity.java")
