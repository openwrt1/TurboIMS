import android.telephony.AccessNetworkConstants;
public class test_rat {
    public static void main(String[] args) {
        System.out.println("EUTRAN: " + AccessNetworkConstants.AccessNetworkType.EUTRAN);
        System.out.println("IWLAN: " + AccessNetworkConstants.AccessNetworkType.IWLAN);
        System.out.println("NGRAN: " + AccessNetworkConstants.AccessNetworkType.NGRAN);
        System.out.println("CDMA2000: " + AccessNetworkConstants.AccessNetworkType.CDMA2000);
    }
}
