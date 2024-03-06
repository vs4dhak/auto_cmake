package com.auto_cmake.sample_lib_shared_android;

import android.content.Context;

import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Test;
import org.junit.Before;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Instrumented test for NativeLib, which will execute on an Android device.
 */
@RunWith(AndroidJUnit4.class)
public class NativeLibInstrumentedTest {

    private NativeLib nativeLib;

    @Before
    public void setUp() {
        nativeLib = new NativeLib();
    }

    @Test
    public void testStringFromJNI() {
        // Assuming the stringFromJNI native method is supposed to return a non-null, specific string.
        // Adjust the expected value according to your native implementation.
        String expected = "Hello from C++";
        assertEquals(expected, nativeLib.stringFromJNI());
    }

    @Test
    public void testAdd() {
        assertEquals(5, nativeLib.add(2, 3));
    }

    @Test
    public void testSubtract() {
        assertEquals(1, nativeLib.subtract(3, 2));
    }

    @Test
    public void testMultiply() {
        assertEquals(6, nativeLib.multiply(2, 3));
    }

    @Test
    public void testDivide() {
        // Be cautious with floating-point division; consider acceptable delta for assertEquals with floats.
        float result = nativeLib.divide(4, 2);
        assertEquals(2.0, result, 0.001);

        // Optionally, add a test for division by zero if your native code handles it in a specific way,
        // for example, by returning a predefined error value or infinity.
    }
}
