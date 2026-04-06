package io.github.vvb2060.ims;

import android.app.IActivityManager;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.PersistableBundle;
import android.os.ServiceManager;
import android.system.Os;
import android.telephony.CarrierConfigManager;
import android.util.Log;

import rikka.shizuku.ShizukuBinderWrapper;

public class ImsConfigHelper {

    private static final String TAG = "ImsConfigHelper";
    private static final String PREFS_NAME = "ims_config";

    /**
     * 应用 IMS 配置到指定的订阅 ID
     * 使用 Shizuku 获取 shell 权限，然后通过 CarrierConfigManager 覆盖配置
     * @param context 应用上下文
     * @param subId 订阅 ID
     * @throws Exception 如果配置失败
     */
    public static void applyConfig(Context context, int subId) throws Exception {
        Log.i(TAG, "Starting to apply IMS configuration for subId: " + subId);

        // 获取 Shell 权限委托
        var binder = ServiceManager.getService(Context.ACTIVITY_SERVICE);
        var am = IActivityManager.Stub.asInterface(new ShizukuBinderWrapper(binder));
        am.startDelegateShellPermissionIdentity(Os.getuid(), null);

        try {
            SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
            boolean enableVoLTE = prefs.getBoolean("volte", true);
            boolean enableVoWiFi = prefs.getBoolean("vowifi", true);
            boolean enableVT = prefs.getBoolean("vt", true);
            boolean enableVoNR = prefs.getBoolean("vonr", true);
            boolean enableCrossSIM = prefs.getBoolean("cross_sim", true);
            boolean enableUT = prefs.getBoolean("ut", true);
            boolean enable5GNR = prefs.getBoolean("5g_nr", true);

            var cm = context.getSystemService(CarrierConfigManager.class);
            var values = buildConfigBundle(enableVoLTE, enableVoWiFi, enableVT, enableVoNR,
                                           enableCrossSIM, enableUT, enable5GNR);

            var bundle = cm.getConfigForSubId(subId, "vvb2060_config_version");
            if (bundle.getInt("vvb2060_config_version", 0) != BuildConfig.VERSION_CODE) {
                values.putInt("vvb2060_config_version", BuildConfig.VERSION_CODE);
                // 使用反射调用 overrideConfig
                try {
                    cm.getClass().getMethod("overrideConfig", int.class, PersistableBundle.class)
                        .invoke(cm, subId, values);
                    Log.i(TAG, "Applied config to subscription: " + subId);
                } catch (NoSuchMethodException e) {
                    // 如果不存在两参数方法，尝试三参数方法
                    cm.getClass().getMethod("overrideConfig", int.class, PersistableBundle.class, boolean.class)
                        .invoke(cm, subId, values, false);
                    Log.i(TAG, "Applied config (non-persistent) to subscription: " + subId);
                }
            } else {
                Log.i(TAG, "Config already up-to-date for subscription: " + subId);
            }

            Log.i(TAG, "IMS configuration applied successfully");
        } finally {
            // 停止权限委托
            am.stopDelegateShellPermissionIdentity();
        }
    }

    /**
     * 根据用户设置构建 IMS 配置包
     * 配置包括 VoLTE、VoWiFi、VT、VoNR、跨 SIM 通话、UT 服务和 5G NR 支持
     * @param enableVoLTE 是否启用 VoLTE
     * @param enableVoWiFi 是否启用 VoWiFi
     * @param enableVT 是否启用视频通话
     * @param enableVoNR 是否启用 VoNR
     * @param enableCrossSIM 是否启用跨 SIM 通话
     * @param enableUT 是否启用 UT 补充服务
     * @param enable5GNR 是否启用 5G NR
     * @return 配置包 PersistableBundle
     */
    private static PersistableBundle buildConfigBundle(boolean enableVoLTE, boolean enableVoWiFi,
                                                        boolean enableVT, boolean enableVoNR,
                                                        boolean enableCrossSIM, boolean enableUT,
                                                        boolean enable5GNR) {
        var bundle = new PersistableBundle();

        // VoLTE 配置
        if (enableVoLTE) {
            bundle.putBoolean(CarrierConfigManager.KEY_CARRIER_VOLTE_AVAILABLE_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_EDITABLE_ENHANCED_4G_LTE_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_HIDE_ENHANCED_4G_LTE_BOOL, false);
            bundle.putBoolean(CarrierConfigManager.KEY_HIDE_LTE_PLUS_DATA_ICON_BOOL, false);
        }

        // VT (视频通话) 配置
        if (enableVT) {
            bundle.putBoolean(CarrierConfigManager.KEY_CARRIER_VT_AVAILABLE_BOOL, true);
        }

        // UT 补充服务配置
        if (enableUT) {
            bundle.putBoolean(CarrierConfigManager.KEY_CARRIER_SUPPORTS_SS_OVER_UT_BOOL, true);
        }

        // 跨 SIM 通话配置
        if (enableCrossSIM) {
            bundle.putBoolean(CarrierConfigManager.KEY_CARRIER_CROSS_SIM_IMS_AVAILABLE_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_ENABLE_CROSS_SIM_CALLING_ON_OPPORTUNISTIC_DATA_BOOL, true);
        }

        // VoWiFi 配置
        if (enableVoWiFi) {
            bundle.putBoolean(CarrierConfigManager.KEY_CARRIER_WFC_IMS_AVAILABLE_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_CARRIER_WFC_SUPPORTS_WIFI_ONLY_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_EDITABLE_WFC_MODE_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_EDITABLE_WFC_ROAMING_MODE_BOOL, true);
            // KEY_SHOW_WIFI_CALLING_ICON_IN_STATUS_BAR_BOOL
            bundle.putBoolean("show_wifi_calling_icon_in_status_bar_bool", true);
            // KEY_WFC_SPN_FORMAT_IDX_INT
            bundle.putInt("wfc_spn_format_idx_int", 6);
        }

        // VoNR (5G 语音) 配置
        if (enableVoNR) {
            bundle.putBoolean(CarrierConfigManager.KEY_VONR_ENABLED_BOOL, true);
            bundle.putBoolean(CarrierConfigManager.KEY_VONR_SETTING_VISIBILITY_BOOL, true);
        }

        // 5G NR 配置
        if (enable5GNR) {
            bundle.putIntArray(CarrierConfigManager.KEY_CARRIER_NR_AVAILABILITIES_INT_ARRAY,
                    new int[]{CarrierConfigManager.CARRIER_NR_AVAILABILITY_NSA,
                            CarrierConfigManager.CARRIER_NR_AVAILABILITY_SA});
            bundle.putIntArray(CarrierConfigManager.KEY_5G_NR_SSRSRP_THRESHOLDS_INT_ARRAY,
                    // Boundaries: [-140 dBm, -44 dBm]
                    new int[]{
                            -128, /* SIGNAL_STRENGTH_POOR */
                            -118, /* SIGNAL_STRENGTH_MODERATE */
                            -108, /* SIGNAL_STRENGTH_GOOD */
                            -98,  /* SIGNAL_STRENGTH_GREAT */
                    });
        }

        return bundle;
    }
}
