//
//  sample_xcode_proj.m
//  sample_xcode_proj
//
//  Created by sentinel on 3/5/24.
//

#import "sample_xcode_proj.h"

@implementation sample_xcode_proj

- (void)test {
    int a = 10;
    int b = 5;

    // Call each function and log the results
    NSLog(@"%d + %d = %d", a, b, add(a, b));
    NSLog(@"%d - %d = %d", a, b, subtract(a, b));
    NSLog(@"%d * %d = %d", a, b, multiply(a, b));
    NSLog(@"%d / %d = %f", a, b, divide(a, b));
}

@end
