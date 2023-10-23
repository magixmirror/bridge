import 'package:get/get.dart' as GetX;
import 'package:flutter/material.dart';

class LoadingController extends GetX.GetxController{

  @override
  void onReady() async{
    GetX.Get.toNamed("/Home");
  }
}