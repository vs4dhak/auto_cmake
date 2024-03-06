package com.auto_cmake.sample_lib_shared_android;

public class NativeLib {

    // Used to load the 'sample_lib_shared_android' library on application startup.
    static {
        System.loadLibrary("sample_lib_shared_android");
    }

    /**
     * A native method that is implemented by the 'sample_lib_shared_android' native library,
     * which is packaged with this application.
     */
    public native String stringFromJNI();

    public native int add(int a, int b);

    public native int subtract(int a, int b);

    public native int multiply(int a, int b);

    public native float divide(int a, int b);
}