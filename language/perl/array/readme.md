* push @array,list 将列表的值放到数组的末尾
* pop @array 弹出数组最后一个值，并返回它 删除最后一个
* shift @array 弹出数组第一个值，并返回它。数组的索引值也依次减一 删除最开始一个
* unshift @array,list 将列表放在数组前面，并返回新数组的元素个数 
* splice @ARRAY, OFFSET [ , LENGTH [ , LIST ] ] @ARRAY：要替换的数组 OFFSET：起始位置 LENGTH：替换的元素个数 LIST：替换元素列表
* split [ PATTERN [ , EXPR [ , LIMIT ] ] ] 字符串到数组
* join EXPR, LIST 数组到字符串
* sort [ SUBROUTINE ] LIST 数组排序
* 特殊变量 $[ 表示数组的第一索引值，一般都为 0 ，如果我们将 $[ 设置为 1，则数组的第一个索引值即为 1，第二个为 2
* 数组的元素是以逗号来分割，我们也可以使用逗号来合并数组
* 一个列表可以当作一个数组使用，在列表后指定索引值可以读取指定的元素