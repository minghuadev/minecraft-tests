package com.example.myfirstapp

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.app.Service
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanRecord
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.pm.PackageManager
import androidx.appcompat.app.AppCompatActivity
import android.os.IBinder
import android.os.ParcelUuid
import android.provider.Settings
import android.util.Log
import androidx.core.content.ContextCompat

/* search: android ble sample
   ref:    https://punchthrough.com/android-ble-guide/

   AndroidManifest.xml add:
        <uses-permission android:name="android.permission.BLUETOOTH" />
        <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
        <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />

        <uses-feature
                android:name="android.hardware.bluetooth_le"
                android:required="true" />
 */

/* search: android service example
   ref:    https://www.vogella.com/tutorials/AndroidServices/article.html
           https://www.geeksforgeeks.org/services-in-android-with-example/

   mention service in manifest:
        <!-- Mention the service name here -->
        <service android:name=".NewService"/>
 */

class BleUtilOp : Service() {

    private val ENABLE_BLUETOOTH_REQUEST_CODE = 1

    private var req_idx = 0
    private var ret_idx = 0
    private var ret_ok = false

    private val bluetoothAdapter: BluetoothAdapter by lazy {
        val bluetoothManager = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        bluetoothManager.adapter
    }

    private val bleScanner by lazy {
        bluetoothAdapter.bluetoothLeScanner
    }

    private val scanSettings = ScanSettings.Builder()
        .setScanMode(ScanSettings.SCAN_MODE_BALANCED)
        .build()

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            //Log.w("ScanCallback: ", "$callbackType $result")
            /* 1
               ScanResult{device=12:34:56:78:90:ab,
                        scanRecord=ScanRecord [mAdvertiseFlags=6,
                                    mServiceUuids=[00000001-0002-0003-0004-010203040506],
                                    mServiceSolicitationUuids=[], mManufacturerSpecificData={},
                                    mServiceData={},
                                    mTxPowerLevel=-2147483648, mDeviceName=ab-1234],
                                    rssi=-65, timestampNanos=988230279152291, eventType=27,
                                    primaryPhy=1, secondaryPhy=0, advertisingSid=255,
                                    txPower=127, periodicAdvertisingInterval=0}
            */
            with(result) {
                //Log.i("ScanCallback",
                //      "Found BLE device! Address: ${device}, Name: ${scanRecord?:"Unnamed"}")
                var rec: ScanRecord? = this.scanRecord
                var nam: String? = "<no-name>"
                var suuid: List<ParcelUuid>? = null
                if ( rec != null ) {
                    nam = rec.getDeviceName()
                    suuid = rec.getServiceUuids()
                }
                var vrssi = this.rssi
                if ( suuid != null &&
                     suuid.toString() == "[00000001-0002-0003-0004-010203040506]" ) {
                    Log.i("ScanCallback",
                        "Found BLE device! Address: ${device}, " +
                                "Name: ${nam?:"<null>"}, " +
                                "RSSI: ${vrssi}, " +
                                "Uuid: ${suuid?:"<null>"}")

                }
            }
        }
    }

    val isLocationPermissionGranted
        get() = hasPermission(Manifest.permission.ACCESS_FINE_LOCATION)

    fun Context.hasPermission(permissionType: String): Boolean {
        return ContextCompat.checkSelfPermission(this, permissionType) ==
                PackageManager.PERMISSION_GRANTED
    }

    private fun promptEnableBluetooth(activity: AppCompatActivity) {
        if (!bluetoothAdapter.isEnabled) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            activity.startActivityForResult(enableBtIntent, ENABLE_BLUETOOTH_REQUEST_CODE)
        }
    }

    fun on_resume_check(activity: AppCompatActivity) {
        if (!bluetoothAdapter.isEnabled) {
            promptEnableBluetooth(activity)
        }
    }

    fun progress_ble_actions() {
        if ( req_idx == 0 && ret_idx == 0 ) {
            Log.w("Ble scan: ", "enabled?")
            ret_ok = false
            req_idx = 1
            if ( bluetoothAdapter.isEnabled ) {
                Log.w("Ble scan: ", "enabled!")
                ret_ok = true
            }
            ret_idx = 1
        }
        if ( req_idx == 1 && ret_idx == 1 ) {
            Log.w("Ble scan: ", "location permission?")
            req_idx = 2
            if ( !ret_ok ) {
                Log.w("Ble scan: ", "enabled failed!")
                ret_idx = 999
            } else {
                ret_ok = false
                Log.w("Ble scan: ", "request location permission ...")
                if (isLocationPermissionGranted) {
                    ret_ok = true
                    ret_idx = 2
                    Log.w("Ble scan: ", "location permission ok!")
                }
            }
        }
        if ( req_idx == 2 && ret_idx == 2 ) {
            Log.w("Ble scan: ", "scan?")
            req_idx = 3
            if ( !ret_ok ) {
                Log.w("Ble scan: ", "location permission failed!")
                ret_idx = 999
            } else {
                ret_ok = false
                Log.w("Ble scan: ", "start scanning ...")
                bleScanner.startScan(null, scanSettings, scanCallback)
                ret_ok = true
                ret_idx = 3
            }
        }
    }

    // ref2:
    private var start_count = 0

    // execution of service will start
    // on calling this method
    override fun onStartCommand(intent: Intent, flags: Int, startId: Int): Int {

        start_count ++
        if ( start_count <= 0 ) { /* avoid wrapping and 0 */
            start_count = 1
        }

        // creating a media player which
        // will play the audio of Default
        // ringtone in android device
        ///player = MediaPlayer.create(this, Settings.System.DEFAULT_RINGTONE_URI)

        // providing the boolean
        // value as true to play
        // the audio on loop
        ///player.setLooping(true)

        // starting the process
        ///player.start()

        if ( start_count >= 3 ) {
            progress_ble_actions()
        }
        Log.w("User service: ", String.format("on-start() ${start_count}"))

        // returns the status
        // of the program
        return START_STICKY
    }

    // execution of the service will
    // stop on calling this method
    override fun onDestroy() {
        super.onDestroy()

        // stopping the process
        ///player.stop()

        Log.w("User service: ", "on-destroy()")
    }

    override fun onBind(intent: Intent): IBinder? {
        return null
    }
}