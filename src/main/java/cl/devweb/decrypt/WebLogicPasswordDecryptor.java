package cl.devweb.decrypt;


import org.bouncycastle.jce.provider.BouncyCastleProvider;

import org.apache.commons.codec.binary.Base64;
//import sun.misc.BASE64Decoder;
//java.util.Base64 -- java >= 8

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.Security;
import java.security.spec.InvalidKeySpecException;



/**
 * 
 * from :
 * https://github.com/NetSPI/WebLogicPasswordDecryptor/blob/master/WebLogicPasswordDecryptor.java
 * 
 * @author German
 *
 *


WebLogicPasswordDecryptor "C:\SerializedSystemIni.dat" "{AES}8/rTjIuC4mwlrlZgJK++LKmAThcoJMHyigbcJGIztug="

WebLogicPasswordDecryptor "C:\SerializedSystemIni.dat" "{3DES}JMRazF/vClP1WAgy1czd2Q=="


java -cp .:/Users/German/development/jars/bcprov-jdk16-1.46.jar  cl.devweb.decrypt.WebLogicPasswordDecryptor /Users/German/Oracle/Middleware/Oracle_Home/user_projects/domains/base_domain/security/SerializedSystemIni.dat "{AES}Zq1DghDssa7DqW4xLl48YgV73rVnddgdGSt8NYg8flA="

java -cp .:/Users/German/development/jars/bcprov-jdk16-1.46.jar  cl.devweb.decrypt.WebLogicPasswordDecryptor /Users/German/tmp/SerializedSystemIni.dat "{AES}DKwQHNzkNRFh8/CJMxIeTDvVMV9dkWWbMoHC4+iJ7lI="
  
java -cp .:/Users/German/development/jars/bcprov-jdk16-1.46.jar:/Users/German/development/jars/commons-codec-1.10.jar  cl.devweb.decrypt.WebLogicPasswordDecryptor /Users/German/tmp/x/05-DS/SerializedSystemIni.dat "{AES}u1wHLIdnmWuhWoDeyubbyb7F6IXGvgbJjKKMMgMNg/s="
 
 
  
 */


public class WebLogicPasswordDecryptor {

    public static void main(String args[]) throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, InvalidKeySpecException, InvalidAlgorithmParameterException {

        Security.addProvider(new BouncyCastleProvider());
        String serializedSystemIniPath = args[0];
        String ciphertext = args[1];
        String cleartext = "";

        if (ciphertext.startsWith("{AES}")){
            ciphertext = ciphertext.replaceAll("^[{AES}]+", "");
            cleartext = decryptAES(serializedSystemIniPath,ciphertext);
        } else if (ciphertext.startsWith("{3DES}")){
            ciphertext = ciphertext.replaceAll("^[{3DES}]+", "");
            cleartext = decrypt3DES(serializedSystemIniPath, ciphertext);
        }

        System.out.println(cleartext);
    }

    public static String decryptAES(String SerializedSystemIni, String ciphertext) throws NoSuchAlgorithmException, InvalidKeySpecException, NoSuchPaddingException, InvalidAlgorithmParameterException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, IOException {

        //byte[] encryptedPassword1 = new BASE64Decoder().decodeBuffer(ciphertext);
        byte[] encryptedPassword1 = Base64.decodeBase64(ciphertext);
        
        
        byte[] salt = null;
        byte[] encryptionKey = null;

        String key = "0xccb97558940b82637c8bec3c770f86fa3a391a56";

        char password[] = new char[key.length()];

        key.getChars(0, password.length, password, 0);

        FileInputStream is = new FileInputStream(SerializedSystemIni);
        try {
            salt = readBytes(is);

            int version = is.read();
            if (version != -1) {
                encryptionKey = readBytes(is);
                if (version >= 2) {
                    encryptionKey = readBytes(is);
                }
            }
        } catch (IOException e) {
            System.out.println("excepcion. " + e);
        }

        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEWITHSHAAND128BITRC2-CBC");

        PBEKeySpec pbeKeySpec = new PBEKeySpec(password, salt, 5);

        SecretKey secretKey = keyFactory.generateSecret(pbeKeySpec);

        PBEParameterSpec pbeParameterSpec = new PBEParameterSpec(salt, 0);

        Cipher cipher = Cipher.getInstance("PBEWITHSHAAND128BITRC2-CBC");
        cipher.init(Cipher.DECRYPT_MODE, secretKey, pbeParameterSpec);
        SecretKeySpec secretKeySpec = new SecretKeySpec(cipher.doFinal(encryptionKey), "AES");

        byte[] iv = new byte[16];
        System.arraycopy(encryptedPassword1, 0, iv, 0, 16);
        int encryptedPasswordlength = encryptedPassword1.length - 16 ;
        byte[] encryptedPassword2 = new byte[encryptedPasswordlength];
        System.arraycopy(encryptedPassword1, 16, encryptedPassword2, 0, encryptedPasswordlength);
        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
        Cipher outCipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        outCipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameterSpec);

        byte[] cleartext = outCipher.doFinal(encryptedPassword2);

        return new String(cleartext, "UTF-8");

    }

    public static String decrypt3DES(String SerializedSystemIni, String ciphertext) throws NoSuchAlgorithmException, InvalidKeySpecException, NoSuchPaddingException, InvalidAlgorithmParameterException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, IOException {

        //byte[] encryptedPassword1 = new BASE64Decoder().decodeBuffer(ciphertext);
        byte[] encryptedPassword1 = Base64.decodeBase64(ciphertext);
        byte[] salt = null;
        byte[] encryptionKey = null;

        String PW = "0xccb97558940b82637c8bec3c770f86fa3a391a56";

        char password[] = new char[PW.length()];

        PW.getChars(0, password.length, password, 0);

        FileInputStream is = new FileInputStream(SerializedSystemIni);
        try {
            salt = readBytes(is);

            int version = is.read();
            if (version != -1) {
                encryptionKey = readBytes(is);
                if (version >= 2) {
                    encryptionKey = readBytes(is);
                }
            }


        } catch (IOException e) {
            System.out.println("excepcion. " + e);
        }

        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEWITHSHAAND128BITRC2-CBC");

        PBEKeySpec pbeKeySpec = new PBEKeySpec(password, salt, 5);

        SecretKey secretKey = keyFactory.generateSecret(pbeKeySpec);

        PBEParameterSpec pbeParameterSpec = new PBEParameterSpec(salt, 0);

        Cipher cipher = Cipher.getInstance("PBEWITHSHAAND128BITRC2-CBC");
        cipher.init(Cipher.DECRYPT_MODE, secretKey, pbeParameterSpec);
        SecretKeySpec secretKeySpec = new SecretKeySpec(cipher.doFinal(encryptionKey),"DESEDE");

        byte[] iv = new byte[8];
        System.arraycopy(salt, 0, iv, 0, 4);
        System.arraycopy(salt, 0, iv, 4, 4);

        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
        Cipher outCipher = Cipher.getInstance("DESEDE/CBC/PKCS5Padding");
        outCipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameterSpec);

        byte[] cleartext = outCipher.doFinal(encryptedPassword1);
        return new String(cleartext, "UTF-8");

    }

    public static byte[] readBytes(InputStream stream) throws IOException {
        int length = stream.read();
        byte[] bytes = new byte[length];
        int in = 0;
        int justread;
        while (in < length) {
            justread = stream.read(bytes, in, length - in);
            if (justread == -1) {
                break;
            }
            in += justread;
        }
        return bytes;
    }
}



