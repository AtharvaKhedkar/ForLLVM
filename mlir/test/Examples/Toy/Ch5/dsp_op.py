# RUN: toyc-ch2 %s -emit=mlir 2>&1 | FileCheck %s

# User defined generic function that operates on unknown shaped arguments

# def func1( x , y){
#     var z = x + y;
#     return z;
# }
def func1(x , y){
    var z = delay(x,y);

    return z;
}

def main() {
  var a = 5 ;
  var a1 = 6;
  var b<2,3> = [1,2,3,4,5,6];

  # var c = delay(b);
  var d = delay(b, a);
  var g = delay(d, a1);
  var e = transpose(b);
  var g1 = func1(e,a);
  var f = b + b;
  # print(a);
  # print(b);
  print(g1);
  print(d);
  print(g);
  # var a1 = 10;
  # var a<2, 3> = [[1, 2, 3], [4, 5, 6]];
}

# CHECK-LABEL: toy.func @multiply_transpose(
# CHECK-SAME:                               [[VAL_0:%.*]]: tensor<*xf64>, [[VAL_1:%.*]]: tensor<*xf64>) -> tensor<*xf64>
# CHECK:         [[VAL_2:%.*]] = toy.transpose([[VAL_0]] : tensor<*xf64>) to tensor<*xf64>
# CHECK-NEXT:    [[VAL_3:%.*]] = toy.transpose([[VAL_1]] : tensor<*xf64>) to tensor<*xf64>
# CHECK-NEXT:    [[VAL_4:%.*]] = toy.mul [[VAL_2]], [[VAL_3]] :  tensor<*xf64>
# CHECK-NEXT:    toy.return [[VAL_4]] : tensor<*xf64>

# CHECK-LABEL: toy.func @main()
# CHECK-NEXT:    [[VAL_5:%.*]] = toy.constant dense<{{\[\[}}1.000000e+00, 2.000000e+00, 3.000000e+00], [4.000000e+00, 5.000000e+00, 6.000000e+00]]> : tensor<2x3xf64>
# CHECK-NEXT:    [[VAL_6:%.*]] = toy.reshape([[VAL_5]] : tensor<2x3xf64>) to tensor<2x3xf64>
# CHECK-NEXT:    [[VAL_7:%.*]] = toy.constant dense<[1.000000e+00, 2.000000e+00, 3.000000e+00, 4.000000e+00, 5.000000e+00, 6.000000e+00]> : tensor<6xf64>
# CHECK-NEXT:    [[VAL_8:%.*]] = toy.reshape([[VAL_7]] : tensor<6xf64>) to tensor<2x3xf64>
# CHECK-NEXT:    [[VAL_9:%.*]] = toy.generic_call @multiply_transpose([[VAL_6]], [[VAL_8]]) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<*xf64>
# CHECK-NEXT:    [[VAL_10:%.*]] = toy.generic_call @multiply_transpose([[VAL_8]], [[VAL_6]]) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<*xf64>
# CHECK-NEXT:    toy.print [[VAL_10]] : tensor<*xf64>
# CHECK-NEXT:    toy.return
