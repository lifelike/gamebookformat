# Counters Example #


## Introduction ##
 This example gamebook shows how to use counters.

Turn to 1 to begin.
<a name="section1">

## 1 ##
 This is where the gamebook starts. We have counters for Life Points and for Gold. You start the adventure with 10 Life Points and 12 Gold. You can never have less than 0 Gold. FIXME need to figure out best syntax for death when life points go below 1. Go to [9](#section9)
 to get more Gold or [8](#section8)
 to lose some Life Points. Go to [3](#section3)
 for testing the init value markup. 
<a name="section2">

## 2 ##
 OK, we increase that something counter by 1 here, and also increase the other counter by 1. You can go back to see the difference between set and init [here](#section3)
, stuck in an infinite loop.
<a name="section3">

## 3 ##
 The Something Counter starts at 5, but when you come back here it will not reset to that, unlike the Other Counter that will reset to 5 every time you get here. If we try to init gold to 999 nothing will happen because it was already set to something before you came yere. Go on to [2](#section2)
. 
<a name="section4">

## 4 ##
 Less than 1 Life Point means the adventure ends now. 
<a name="section5">

## 5 ##
 You have at least 16 gold. Go back to get some more at [9](#section9)
. 
<a name="section6">

## 6 ##
 You have more than 16 Gold. How nice. Go back to get some more at [9](#section9)
. 
<a name="section7">

## 7 ##
 You drop 5 Gold. It should not be possible to go below 0. Then go on to get gold at [9](#section9)
 or lose life at [8](#section8)
. 
<a name="section8">

## 8 ##
 You lose 1 Life Points. You can go to [9](#section9)
 to get some Gold. 
<a name="section9">

## 9 ##
 Congratulations, you found 2 Gold. If you have less than 1 Life Points, turn to [4](#section4)
. You can go to [8](#section8)
 to lose some life or to [7](#section7)
 to drop some gold. If you have at least 16 Gold you can turn to [5](#section5)
. If you have even more than 16 Gold you can turn to [6](#section6)
. 

