def sum_of_two(arr:list, target:int) -> tuple:
    result=list()
    for i in arr:
            if target-i in arr:
                result.append((i,target-i))
                del(arr[arr.index(i)])
    if len(result)==1:return result[0]
    return tuple(result)





list1=[1,3,5,8,10]
target1=13
print(sum_of_two(list1, target1));
list2=[1,3,5,8,10]
target2=7
print(sum_of_two(list2, target2));