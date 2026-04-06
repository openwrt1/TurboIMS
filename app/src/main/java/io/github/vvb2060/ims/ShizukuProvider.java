package io.github.vvb2060.ims;

import android.app.ActivityManager;
import android.app.IActivityManager;
import android.app.UiAutomationConnection;
import android.content.ComponentName;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.ServiceManager;
import android.util.Log;

import org.lsposed.hiddenapibypass.LSPass;

import rikka.shizuku.Shizuku;
import rikka.shizuku.ShizukuBinderWrapper;

public class ShizukuProvider extends rikka.shizuku.ShizukuProvider {

    @Override
    public boolean onCreate() {
        LSPass.setHiddenApiExemptions("");
        // 不再自动触发，只在用户手动点击"应用配置"时才执行
        return super.onCreate();
    }

    /**
     * 启动特权进程来应用 IMS 配置
     * 使用 Shizuku 的 Instrumentation API 来执行需要系统权限的操作
     * @param context 应用上下文
     */
    public static void startInstrument(Context context) {
        try {
            Log.i("ShizukuProvider", "Starting instrumentation...");
            var binder = ServiceManager.getService(Context.ACTIVITY_SERVICE);
            var am = IActivityManager.Stub.asInterface(new ShizukuBinderWrapper(binder));
            var name = new ComponentName(context, PrivilegedProcess.class);
            var flags = 0x00000001; // ActivityManager.INSTR_FLAG_NO_RESTART
            var connection = new UiAutomationConnection();
            Log.i("ShizukuProvider", "Calling startInstrumentation with component: " + name);
            am.startInstrumentation(name, null, flags, new Bundle(), null, connection, 0, null);
            Log.i("ShizukuProvider", "Instrumentation started successfully");
        } catch (Exception e) {
            Log.e("ShizukuProvider", "Failed to start instrumentation", e);
        }
    }
}
