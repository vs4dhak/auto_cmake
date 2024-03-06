#include <jni.h>
#include <string>

#ifdef __cplusplus
extern "C" {
#endif

#include <add.h>
#include <subtract.h>
#include <multiply.h>
#include <divide.h>


JNIEXPORT jstring JNICALL
Java_com_auto_1cmake_sample_1lib_1shared_1android_NativeLib_stringFromJNI(
        JNIEnv* env,
        jobject /* this */) {
    std::string hello = "Hello from C++";
    return env->NewStringUTF(hello.c_str());
}

JNIEXPORT jint JNICALL
Java_com_auto_1cmake_sample_1lib_1shared_1android_NativeLib_add(JNIEnv *env, jobject obj, jint a, jint b) {
    return (jint) add(a, b);
}

JNIEXPORT jint JNICALL
Java_com_auto_1cmake_sample_1lib_1shared_1android_NativeLib_subtract(JNIEnv *env, jobject obj, jint a, jint b) {
    return (jint) subtract(a, b);
}

JNIEXPORT jint JNICALL
Java_com_auto_1cmake_sample_1lib_1shared_1android_NativeLib_multiply(JNIEnv *env, jobject obj, jint a, jint b) {
    return (jint) multiply(a, b);
}

JNIEXPORT jfloat JNICALL
Java_com_auto_1cmake_sample_1lib_1shared_1android_NativeLib_divide(JNIEnv *env, jobject obj, jint a, jint b) {
    return (jfloat) divide(a, b);
}

#ifdef __cplusplus
}
#endif