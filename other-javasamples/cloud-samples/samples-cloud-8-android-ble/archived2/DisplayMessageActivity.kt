package com.example.myfirstapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.widget.TextView

class DisplayMessageActivity : AppCompatActivity() {

    private var call_cnt = 0
    private var call_msg = "msg0\n"
    private val call_this = this

    fun calculate_content():String {
        val numbers = listOf(1, 2, 3, 4, 5, 6)
        var retv = ""
        retv = retv + String.format("List: $numbers\n")
        ///println("List: $numbers")
        retv = retv + String.format("Size: ${numbers.size}\n")
        retv = retv + String.format("call_cnt: ${call_cnt}\n")
        call_cnt ++

        // Access elements of the list
        ///println("First element: ${numbers[0]}")
        ///println("Second element: ${numbers[1]}")
        ///println("Last index: ${numbers.size - 1}")
        ///println("Last element: ${numbers[numbers.size - 1]}")
        ///println("First: ${numbers.first()}")
        ///println("Last: ${numbers.last()}")

        // Use the contains() method
        ///println("Contains 4? ${numbers.contains(4)}")
        ///println("Contains 7? ${numbers.contains(7)}")
        return retv
    }

    /* https://stackoverflow.com/questions/55570990/kotlin-call-a-function-every-second/ */
    private lateinit var mainHandler: Handler
    private val updateTextTask = object : Runnable {
        override fun run() {
            //minusOneSecond()
            val textView = findViewById<TextView>(R.id.textView)
            textView.apply {
                var text_to_set = call_msg + calculate_content()
                text = text_to_set
            }
            mainHandler.postDelayed(this, 2000)

            startService(Intent(call_this, BleUtilOp::class.java))

            Log.w("User message: ", "handler-run()")
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        mainHandler.removeCallbacks(updateTextTask)

        stopService(Intent(this, BleUtilOp::class.java))

        Log.w("User message: ", "onDestroy()")
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        /*TODO */
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_display_message)

        // Get the Intent that started this activity and extract the string
        val message = intent.getStringExtra(EXTRA_MESSAGE)

        startService(Intent(this, BleUtilOp::class.java))

        // Capture the layout's TextView and set the string as its text
        call_msg += "My_First_App.app" + "\n" + message + "\n"
        call_cnt = 0
        val textView = findViewById<TextView>(R.id.textView)
        textView.apply {
            var text_to_set = call_msg + calculate_content()
            text = text_to_set
        }

        mainHandler = Handler(Looper.getMainLooper())
        mainHandler.post(updateTextTask)

        Log.w("User message: ", "onCreate()")

        /* modify the AndroidManifest.xml so that it contains parentActivityName:
        <activity
            android:name=".DisplayMessageActivity"
            android:parentActivityName=".MainActivity">
            <!-- The meta-data tag is required if you support API level 15 and lower -->
            <meta-data
                android:name="android.support.PARENT_ACTIVITY"
                android:value=".MainActivity" />
        </activity>
         */

    }
}