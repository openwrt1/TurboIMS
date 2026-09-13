import android.telephony.ServiceState;
public class test_ril {
    public static void main(String[] args) {
        System.out.println("RIL_LTE: " + ServiceState.RIL_RADIO_TECHNOLOGY_LTE);
        System.out.println("RIL_IWLAN: " + ServiceState.RIL_RADIO_TECHNOLOGY_IWLAN);
        System.out.println("RIL_NR: " + ServiceState.RIL_RADIO_TECHNOLOGY_NR);
    }
}
