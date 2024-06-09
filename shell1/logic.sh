#!/bin/bash
echo -n "are you a girl?(y/n): "
read response

if [ "$response" == "y" ]
then
 echo "she is a girl"
elif [ "$response" == "n" ]
then
 echo "she is boy"
else 
 echo "please enter only y or n: "
fi

echo -n "enter an integer: "
read int1
echo -n "enter another integer: "
read int2

sum=$(($int1+$int2))
product=$(($int1*$int2))

echo "The sum of $n1 and $n2 is $sum"
echo "The product of $n1 and $n2 is $product."

if [[ $sum == $product ]]
then 
    echo "equal"
elif [ $sum -gt $product ]
then 
    echo "greater"
elif [ $sum -lt $product ]
then 
    echo "less"
fi