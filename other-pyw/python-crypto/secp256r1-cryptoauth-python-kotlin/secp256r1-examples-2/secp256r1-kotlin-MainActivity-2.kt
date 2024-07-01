package com.example.myapplication2

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication2.ui.theme.MyApplication2Theme
import java.io.UnsupportedEncodingException
import java.math.BigInteger
import java.security.InvalidAlgorithmParameterException
import java.security.InvalidKeyException
import java.security.Key
import java.security.KeyFactory
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.security.NoSuchAlgorithmException
import java.security.NoSuchProviderException
import java.security.PrivateKey
import java.security.PublicKey
import java.security.SecureRandom
import java.security.Signature
import java.security.interfaces.ECPrivateKey
import java.security.interfaces.ECPublicKey
import java.security.spec.ECFieldFp
import java.security.spec.ECGenParameterSpec
import java.security.spec.ECParameterSpec
import java.security.spec.ECPoint
import java.security.spec.ECPublicKeySpec
import java.security.spec.PKCS8EncodedKeySpec
import javax.crypto.BadPaddingException
import javax.crypto.Cipher
import javax.crypto.IllegalBlockSizeException
import javax.crypto.KeyAgreement
import javax.crypto.NoSuchPaddingException
import javax.crypto.SecretKey
import javax.crypto.ShortBufferException
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplication2Theme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colors.background
                ) {
                    Greeting("Android")
                }
            }
        }
    }
}

fun hexStringToByteArray(hexString: String): ByteArray? {
    val sz = hexString.length
    if (sz % 2 != 0) { return null }
    val retv:ByteArray = ByteArray(sz/2)
    for (i in 0..sz/2-1) {
        val chunk:String = hexString.substring(i*2, i*2+2)
        val d:Byte = Integer.parseInt(chunk, 16).toByte()
        retv[i] = d
    }
    return retv
}

fun bytesToHexString(bytesValue: ByteArray): String {
    val sz = bytesValue.size
    var retv_buf = ""
    for (i in 0..sz-1) {
        retv_buf = retv_buf + String.format("%02x", bytesValue[i])
    }
    val retv = retv_buf
    return retv
}

fun bytesToString(bytesValue: ByteArray): String {
    val sz = bytesValue.size
    var retv_buf = ""
    for (i in 0..sz-1) {
        retv_buf = retv_buf +bytesValue[i].toChar()
    }
    val retv = retv_buf
    return retv
}

fun generateSharedSecret(privateKey: PrivateKey, publicKey: PublicKey): SecretKey? {
    try {
        val keyAgreement: KeyAgreement = KeyAgreement.getInstance("ECDH");
        keyAgreement.init(privateKey);
        keyAgreement.doPhase(publicKey, true);

        //val key: SecretKey = keyAgreement.generateSecret("AES");
        val key: SecretKey = keyAgreement.generateSecret("AES") // AES or AES_256
        return key;
    } catch (e: InvalidKeyException) {
        // TODO Auto-generated catch block
        e.printStackTrace();
        return null;
    } catch (e: NoSuchAlgorithmException) {
        // TODO Auto-generated catch block
        e.printStackTrace();
        return null;
    } catch (e: NoSuchProviderException) {
        // TODO Auto-generated catch block
        e.printStackTrace();
        return null;
    } catch (e: Exception) {
        // TODO Auto-generated catch block
        e.printStackTrace();
        return null;
    }
}

fun encryptString(key: SecretKey, plainText: String, iv: ByteArray): String? {
    try {
        //val iv:ByteArray = SecureRandom().generateSeed(16) // 128 bits
        val ivSpec: IvParameterSpec = IvParameterSpec(iv)
        //val cipher: Cipher = Cipher.getInstance("AES/GCM/NoPadding") // works ok
        // AES/CBC/NoPadding fails.
        // AES/CBC/PKCS5PADDING ok. it's on developer.android.com kotlin/javax/crypto/Cipher
        // AES/CBC/PKCS7PADDING ok in emulator on API 33.
        val cipher: Cipher = Cipher.getInstance("AES_128/CBC/PKCS7PADDING")

        cipher.init(Cipher.ENCRYPT_MODE, key, ivSpec)

        val plainTextBytes: ByteArray = plainText.toByteArray() //plainText.getBytes("UTF-8")
        val cipherText: ByteArray = ByteArray(cipher.getOutputSize(plainTextBytes.size))
        var encryptLength: Int = cipher.update(
            plainTextBytes, 0,
            plainTextBytes.size, cipherText, 0
        )
        encryptLength += cipher.doFinal(cipherText, encryptLength)

        return bytesToHexString(cipherText)
    } catch (e: NoSuchAlgorithmException) {
        e.printStackTrace()
        return null
    } catch (e: NoSuchProviderException) {
        e.printStackTrace()
        return null
    } catch (e: NoSuchPaddingException) {
        e.printStackTrace()
        return null
    } catch (e: InvalidKeyException) {
        e.printStackTrace()
        return null
    } catch (e: InvalidAlgorithmParameterException) {
        e.printStackTrace()
        return null
    } catch (e: UnsupportedEncodingException) {
        e.printStackTrace()
        return null
    } catch (e: ShortBufferException) {
        e.printStackTrace()
        return null
    } catch (e: IllegalBlockSizeException) {
        e.printStackTrace()
        return null
    } catch (e: BadPaddingException) {
        e.printStackTrace()
        return null
    }
}

fun decryptString(key: SecretKey, cipherText: String, iv: ByteArray): String? {
    try {
        val decryptionKey: Key = SecretKeySpec(key.getEncoded(), key.getAlgorithm())
        val ivSpec: IvParameterSpec = IvParameterSpec(iv)
        //val cipher: Cipher = Cipher.getInstance("AES/GCM/NoPadding") // works ok
        // AES/CBC/PKCS5PADDING ok
        val cipher: Cipher = Cipher.getInstance("AES/CBC/PKCS7PADDING")
        cipher.init(Cipher.DECRYPT_MODE, decryptionKey, ivSpec);

        val cipherTextBytes: ByteArray? = hexStringToByteArray(cipherText)
        if ( cipherTextBytes == null ) {
            return null
        }

        val plainText: ByteArray = ByteArray( cipher.getOutputSize(cipherTextBytes.size) )
        var decryptLength: Int = cipher.update(
            cipherTextBytes, 0,
            cipherTextBytes.size, plainText, 0
        )
        decryptLength += cipher.doFinal(plainText, decryptLength)

        return bytesToString(plainText)
    } catch (e: NoSuchAlgorithmException ) {
        e.printStackTrace()
        return null
    } catch (e:NoSuchProviderException) {
        e.printStackTrace()
        return null
    } catch (e: NoSuchPaddingException) {
        e.printStackTrace()
        return null
    } catch (e:InvalidKeyException) {
        e.printStackTrace()
        return null
    } catch (e: InvalidAlgorithmParameterException) {
        e.printStackTrace()
        return null
    } catch (e: IllegalBlockSizeException) {
        e.printStackTrace()
        return null
    } catch (e: BadPaddingException) {
        e.printStackTrace()
        return null
    } catch (e: ShortBufferException) {
        e.printStackTrace()
        return null
    } catch (e: UnsupportedEncodingException) {
        e.printStackTrace()
        return null
    }
}

fun my_testing_1() {
    /* generate a key pair */
    val keyPairGentr:KeyPairGenerator = KeyPairGenerator.getInstance("EC")
    keyPairGentr.initialize(ECGenParameterSpec("secp256r1"))
    val keyPair:KeyPair = keyPairGentr.genKeyPair()
    val pubKey:PublicKey = keyPair.getPublic()
    val prvKey:PrivateKey = keyPair.getPrivate() // prvKey: OpenSSLECPPrivateKey{params={ECDSA-Parameters: (256 bit)\n}}

    /* extract public key x y */
    val pubFmt = pubKey.getFormat() // String "X.509"
    val ecPubKey: ECPublicKey = pubKey as ECPublicKey // OpenSSLECPublicKey 04, bytes of 32 for x, 32 for y
    val pubPoint: ECPoint = ecPubKey.getW()
    val pubX: BigInteger = pubPoint.getAffineX()
    val pubY: BigInteger = pubPoint.getAffineY()

    val pubXout = pubX.toByteArray()
    val pubYout = pubY.toByteArray()

    val pubXsz = pubXout.size   // 32, or 33 with first byte 0
    val pubX0 = pubXout[0]
    val pubX1 = pubXout[1]

    val pubYsz = pubYout.size   // 32, or 33 with first byte 0
    val pubY0 = pubYout[0]
    val pubY1 = pubYout[1]

    val pubXstr = pubX.toString(16) // hexadecimal
    val pubYstr = pubY.toString(16)
    val pubOtherHexStr = pubXstr + pubYstr

    //val pubXReconstruct = BigInteger.
    Log.w(
        "======== ======== ",
        "size pubx " + pubXsz + "  " + // 32
                "size puby " + pubYsz + "  " + // 32
                "format pub " + pubFmt
    )
    Log.w(
        "======== ======== ",
        "value "+
                " pubx " + String.format("%02X %02X", pubX0, pubX1) + "  " +
                " puby " + String.format("%02X %02X", pubY0, pubY1) + "  " +
                ""
    )
    Log.w(
        "======== ======== ",
        "value "+
                " pubx " + pubXstr.length + " " + pubXstr + "  " +
                " puby " + pubYstr.length + " " + pubYstr + "  " +
                ""
    )
    Log.w(
        "======== ======== ",
        "value "+
                " pubOther " + pubOtherHexStr.length + " " +
                pubOtherHexStr + "  " +
                ""
    )

    /* convert private key to hex string */
    val prvFmt = prvKey.getFormat()  // String "PKCS#8"
    val prvCoded = prvKey.getEncoded()  // byte[] of 138
    val prvCodedHexStr = bytesToHexString(prvCoded)
    Log.w("======== ========",
        "private coded hex " + prvCodedHexStr.length + " " +
                prvCodedHexStr + "  " +
                "format " + prvFmt
    )

    /* load private key from bytes */
    val kf:KeyFactory = KeyFactory.getInstance("EC")
    val prvK1:PrivateKey = kf.generatePrivate( PKCS8EncodedKeySpec(prvCoded) )
    val prvK1Coded = prvK1.getEncoded() // byte[] of 138
    val k2:ECPrivateKey = prvK1 as ECPrivateKey
    val p2: ECParameterSpec = k2.getParams()
    val p3:BigInteger = (p2.getCurve().getField() as ECFieldFp).getP() // BigInteger
    Log.w("======== ======== ", "again p=(dec)" + p3) // p3 not used in this example

    /* load public key from bytes */

    // get the key params from your own key
    val params: ECParameterSpec = pubKey.getParams()

    // get the other party 64 bytes
    //byte [] otherPub = crypto.getBlePubKeyBytes();
    val otherPub: ByteArray? = hexStringToByteArray(pubOtherHexStr)
    val xBytes = ByteArray(33)
    val yBytes = ByteArray(33)

    if ( otherPub != null ) {
        xBytes[0] = 0
        for (i in 0..31) {
            //xBytes.append(otherPub, 0, 32)
            xBytes[1 + i] = otherPub[i]
        }
        yBytes[0] = 0
        for (i in 0..31) {
            //yBytes.append(otherPub, 32, 32)
            yBytes[1 + i] = otherPub[32 + i]
        }
    }

    // generate the public key point
    val x: BigInteger = BigInteger(xBytes)
    val y: BigInteger = BigInteger(yBytes)
    val w = ECPoint(x, y)

    // generate the key of the other side
    val otherKeySpec = ECPublicKeySpec(w, params)
    val keyFactory: KeyFactory = KeyFactory.getInstance("EC")
    val blePubKey = keyFactory.generatePublic(otherKeySpec) as ECPublicKey

    Log.w("======== ======== ", "recreated other pub key")

    /* below the encoded format public key is not used.
     * we use x y of 64 bytes to load or recreate the public key.
     * the encoded private key can be saved and loaded to recreate the private key.
     */
    //val pubEncoded = pubKey.getEncoded() // ByteArray!, size 91.
    //val prvEncoded = prvKey.getEncoded() // ByteArray!, size 138. this can be used.
    //Log.w("======== ======== ",
    //    "size prv " + prvEncoded.size + "  " + // 138
    //            "size pub " + pubEncoded.size + "  " + // 91
    //            "format pub " + pubFmt + "  " + // "X.509"
    //            "format prv " + prvfmt        // "PKCS#8"
    //)

    /* ecdh aes */
    val shared_key1:SecretKey? = generateSharedSecret(prvKey, blePubKey)
    val k1b: ByteArray? = shared_key1?.getEncoded() // AES_256:32 bytes.
    val shared_key: SecretKey? = if ( k1b != null && k1b.size == 32) {
        SecretKeySpec(k1b, 0, k1b.size / 2, "AES") // AES or AES_128
    } else { null }
    // AES or AES_256 key is 32 bytes. AES or AES_128 key is 16 bytes.
    Log.w("======== ======== ", "created shared key " + shared_key)

    /* encryption decryption */
    val iv:ByteArray = SecureRandom().generateSeed(16) // 128 bits
    val input_string: String = "this is an input string"
    var encrypt_decrypt_ok = false
    if (shared_key != null) {
        val cipher_txt = encryptString(shared_key, input_string, iv)
        if (cipher_txt != null) {
            val plain_txt = decryptString(shared_key, cipher_txt, iv)
            if ( plain_txt != null ) {
                Log.w("======== ======== ", "encrypted input text: " + cipher_txt)
                Log.w("======== ======== ", "decrypted output text: " + plain_txt)
                encrypt_decrypt_ok = true
            }
        }
    }
    if ( encrypt_decrypt_ok != true ) {
        Log.w("======== ======== ", "encrypt-decrypt failed")
    }

    /* ecdsa sign */
    val message:ByteArray = input_string.toByteArray()
    val ss: Signature = Signature.getInstance("SHA256withECDSA")
        .apply {
            initSign(prvKey)
            update(message)
        }
    val signature: ByteArray = ss.sign()

    val sv: Signature = Signature.getInstance("SHA256withECDSA")
        .apply {
            initVerify(pubKey)
            update(message)
        }
    val valid: Boolean = sv.verify(signature)
    Log.w("======== ======== ", "sign-verify " + valid)
}

fun my_testing_2() {
    /* generate a key pair to use its param */
    val preKPG:KeyPairGenerator = KeyPairGenerator.getInstance("EC")
    preKPG.initialize(ECGenParameterSpec("secp256r1"))
    val preKP:KeyPair = preKPG.genKeyPair()
    val prePubKey:ECPublicKey = preKP.getPublic() as ECPublicKey

    /* load a key pair */
    val prv_hex = "308187020100301306072A8648CE3D020106082A8648CE3D030107046D30" +
            "6B020101042019A76210314C46D3F1A70677B9425E15E31FA590DEA5393B" +
            "6D4BAA420E557A42A144034200044528FFBF5359F7CA96EC3668B8353C92" +
            "BAD5103B105B4C9592255A602B5AA64E4E4E12F0E42C85672EF14ACF823D" +
            "E74FD0A859A0A8A1E955E58F25A0CD413491" // der encoding 138 bytes
    val pub_hex = "4528FFBF5359F7CA96EC3668B8353C92BAD5103B105B4C9592255A602B5A" +
            "A64E4E4E12F0E42C85672EF14ACF823DE74FD0A859A0A8A1E955E58F25A0" +
            "CD413491" // rs values 64 bytes

    /* load public key from bytes */

    // get the key params from your own key
    val params: ECParameterSpec = prePubKey.getParams()

    // get the 64 bytes
    //byte [] otherPub = crypto.getBlePubKeyBytes();
    val pubKeyBytes: ByteArray? = hexStringToByteArray(pub_hex)
    val pubXBytes = ByteArray(33)
    val pubYBytes = ByteArray(33)

    if ( pubKeyBytes != null ) {
        pubXBytes[0] = 0
        for (i in 0..31) {
            //xBytes.append(otherPub, 0, 32)
            pubXBytes[1 + i] = pubKeyBytes[i]
        }
        pubYBytes[0] = 0
        for (i in 0..31) {
            //yBytes.append(otherPub, 32, 32)
            pubYBytes[1 + i] = pubKeyBytes[32 + i]
        }
    }

    // generate the public key point
    val pubX: BigInteger = BigInteger(pubXBytes)
    val pubY: BigInteger = BigInteger(pubYBytes)
    val pubW = ECPoint(pubX, pubY)

    // generate the key of the other side
    val pubKeySpec = ECPublicKeySpec(pubW, params)
    val pubKeyFactory: KeyFactory = KeyFactory.getInstance("EC")
    val pubKey: ECPublicKey = pubKeyFactory.generatePublic(pubKeySpec) as ECPublicKey

    Log.w(
        "======== ======== ",
        "value "+
                " pubKey " + pub_hex.length + " " +
                pub_hex + "  " +
                ""
    )

    /* load private key from bytes */
    val prvCoded = hexStringToByteArray(prv_hex)
    val prvKey = if (prvCoded != null) {
        val prvKF: KeyFactory = KeyFactory.getInstance("EC")
        val prvK1: PrivateKey = prvKF.generatePrivate(PKCS8EncodedKeySpec(prvCoded))
        //val prvK2: ECPrivateKey = prvK1 as ECPrivateKey
        prvK1
    } else {
        null
    }

    /* ecdsa sign */
    val input_string:String = "this is an input example message"
    val message:ByteArray = input_string.toByteArray()
    //val ss: Signature = Signature.getInstance("SHA256withECDSA")
    //    .apply {
    //        initSign(prvKey)
    //        update(message)
    //    }
    //val signature: ByteArray = ss.sign()
    val sig_hex = "3046022100E007FC30C3A2835104103682C8A74E7EBC84A8134CC46769E3DBDE5ADB2AA692022100FD4B9005140C9A4D9A24046E304D5E3919FB7643F0D19C99B7E183473368525C"
    val signature = hexStringToByteArray(sig_hex)

    val sv: Signature = Signature.getInstance("SHA256withECDSA")
        .apply {
            initVerify(pubKey)
            update(message)
        }
    val valid: Boolean = sv.verify(signature)
    Log.w("======== ======== ", "sign-verify " + valid)

    /* ecdh aes */
    val shared_key1:SecretKey? = if ( prvKey != null ) {
        generateSharedSecret(prvKey, pubKey)
    } else { null }
    val k1b: ByteArray? = shared_key1?.getEncoded() // AES_256:32 bytes.
    val shared_key: SecretKey? = if ( k1b != null && k1b.size == 32) {
        SecretKeySpec(k1b, 0, k1b.size / 2, "AES") // AES or AES_128
    } else { null }
    val k1b_hex = if ( k1b != null ) {
        bytesToHexString(k1b)
    } else { null }
    // AES or AES_256 key is 32 bytes. AES or AES_128 key is 16 bytes.
    Log.w("======== ======== ", "created shared key hex " +
            "  " + k1b_hex?.length + "  " + k1b_hex)

    /* encryption decryption */
}

@Composable
fun Greeting(name: String) {
    Column() {
        Row() { Text(text = "Hello $name!") }

        my_testing_2()
        Log.w("======== ======== ", "my_testing_2() returned")

        Row() { Text(text = "Hello $name!") }
    }
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    MyApplication2Theme {
        Greeting("An Droid")
    }
}