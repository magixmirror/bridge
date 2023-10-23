import 'package:flutter/material.dart';
import 'package:get/get.dart' as GetX;
import 'package:bridge/Controllers/LoadingController.dart';

class Loading extends StatelessWidget {
  Loading({Key? key}) : super(key: key);
  final LoadingController loadingController = GetX.Get.put(LoadingController());
  @override
  Widget build(BuildContext context) {
    return const  Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child : Image(
          image: AssetImage("assets/Logo2.png"),
          width: 250,
        ),
      ),
    );
  }
}
