import 'package:bridge/Globals/Globals.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' as GetX;
import 'package:lottie/lottie.dart';

class Dialogs {
  static successSnackBar(String message) =>
      GetX.Get.snackbar(
          "Message", message,
          colorText: Colors.white,
          snackPosition: GetX.SnackPosition.TOP,
          icon: const Icon(Icons.check_circle, color: Colors.green),
          duration: const Duration(seconds: 3),
          backgroundColor: Globals.colorBlack,
          isDismissible: true,
          dismissDirection: DismissDirection.vertical);

  static errorSnackBar(String message) =>
      GetX.Get.snackbar(
          "Error", message,
          colorText: Colors.white,
          snackPosition: GetX.SnackPosition.TOP,
          icon: const Icon(Icons.error, color: Colors.red),
          duration: const Duration(seconds: 3),
          backgroundColor: Globals.colorBlack,
          isDismissible: true,
          dismissDirection: DismissDirection.vertical);

  static loadingDialog() =>
      GetX.Get.defaultDialog(
          title: "",
          content: Lottie.network(
              "https://lottie.host/fc503ff8-25f9-4c43-b67c-d643f5e68538/vWdObm6Qlt.json",
              width: Globals.dimension * 0.2),
          backgroundColor: Colors.transparent,
          barrierDismissible: false
      );

  static uploadingDialog() => GetX.Get.dialog(
  PopScope(
    canPop: false,
    child: AlertDialog(
      elevation: 0,
      content: Lottie.network(
          "https://lottie.host/2e311d98-fe09-4266-85e3-91b4784f62a0/KguI2VLeVv.json",
          width: Globals.dimension * 0.2),
      shadowColor: Colors.transparent,
      backgroundColor: Colors.transparent,
    ),
  ),
    barrierDismissible: false,
  );

}